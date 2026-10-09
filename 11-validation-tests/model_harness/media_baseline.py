"""Offline, video-only codec baseline for a pinned 30-second scene. Requires FFmpeg."""
import argparse
import hashlib
import json
import re
import subprocess
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from .version import provenance
from .compression import atomic_report


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def archive(path, output):
    # Stream files instead of loading raw video into RAM. Fixed member metadata.
    info = zipfile.ZipInfo('payload', date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info._compresslevel = 9
    with zipfile.ZipFile(output, 'w') as z, z.open(info, 'w', force_zip64=True) as dest, path.open('rb') as src:
        for block in iter(lambda: src.read(1024 * 1024), b''):
            dest.write(block)
    h = hashlib.sha256()
    with zipfile.ZipFile(output) as z, z.open('payload') as src:
        for block in iter(lambda: src.read(1024 * 1024), b''):
            h.update(block)
    if h.hexdigest() != sha(path):
        raise ValueError('ZIP round-trip failed')


def probe_source(source, scene):
    data = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
                     '-show_streams', '-of', 'json', str(source)], text=True))
    stream = data['streams'][0]
    if stream['width'] < scene['width'] or stream['height'] < scene['height']:
        # The historical 359-row fixture explicitly pads one cropped row pair.
        legacy_padding = (scene.get('id') == 'big-buck-bunny-flowers-30s-v1'
                          and (stream['width'], stream['height'], scene['width'], scene['height']) == (640, 359, 640, 360))
        if not legacy_padding:
            raise ValueError('Source resolution is below target; upscaled baselines are not permitted')
    return {k: stream.get(k) for k in ('codec_name', 'width', 'height', 'pix_fmt', 'avg_frame_rate', 'duration')}


def run(source, scene, out):
    if sha(source) != scene['source_sha256']:
        raise ValueError('Source hash does not match pinned scene')
    source_probe = probe_source(source, scene)
    out = Path(out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    report = {'schema_version': 1, 'kind': 'media_codec_baseline', 'run_id': out.name,
              'created_at': datetime.now(timezone.utc).isoformat(), 'status': 'running',
              'scene': scene, 'source_probe': source_probe, 'harness': provenance(), 'rows': [], 'commands': [],
              'ffmpeg': subprocess.check_output(['ffmpeg', '-version'], text=True),
              'limitations': ['Video only; all audio excluded.', 'Lossy distribution source is the decoded reference, not an original render.',
                             'Single codec settings are not matched-quality rate-distortion comparisons.',
                             'PSNR/SSIM measure decoded pixels, not semantic retention. No model or JEV was run in this codec experiment.',
                             'Wall time includes local runtime overhead; no hardware-controlled speed ranking.']}
    snap = out / 'harness_source'
    for rel in report['harness']['files']:
        dest = snap / rel; dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes((Path(__file__).parent / rel).read_bytes())
    def command(args):
        start = time.perf_counter()
        proc = subprocess.run(['ffmpeg', '-hide_banner', '-nostdin', '-y'] + [str(a) for a in args], capture_output=True, text=True)
        report['commands'].append({'argv': ['ffmpeg', '-hide_banner', '-nostdin', '-y'] + [str(a) for a in args], 'wall_seconds': time.perf_counter()-start, 'returncode': proc.returncode})
        (out / f'command-{len(report["commands"]):02}.log').write_text(proc.stderr)
        if proc.returncode:
            raise RuntimeError('FFmpeg failed; inspect saved command log')
        return proc.stderr
    def row(name, path, lossless, **extra):
        data = {'method': name, 'file': path.name, 'bytes': path.stat().st_size, 'sha256': sha(path),
                'lossless_to_decoded_reference': lossless, **extra}
        report['rows'].append(data)
        atomic_report(out / 'report.json', report)
        return data
    try:
        frames = round(scene['duration_seconds'] * scene['fps'])
        raw = out / 'reference.yuv'
        command(['-ss', scene['start_seconds'], '-i', source, '-map', '0:v:0', '-an', '-vf', scene['filter'],
                 '-frames:v', frames, '-f', 'rawvideo', raw])
        expected = scene['width'] * scene['height'] * 3 // 2 * frames
        if raw.stat().st_size != expected:
            raise ValueError('Unexpected reference frame count/size')
        if sha(raw) != scene['reference_sha256']:
            raise ValueError('Decoded reference hash differs from pinned scene; do not compare runs')
        row('Decoded raw YUV420p', raw, True)
        raw_input = ['-f','rawvideo','-pixel_format',scene['pixel_format'],'-video_size',f"{scene['width']}x{scene['height']}",'-framerate',scene['fps'],'-i',raw]
        codecs = [('H.264 CRF23 medium', 'libx264', ['-crf','23','-preset','medium'], '.mp4', False),
                  ('H.265 CRF28 medium', 'libx265', ['-crf','28','-preset','medium'], '.mp4', False),
                  ('AV1 CRF35 preset8', 'libsvtav1', ['-crf','35','-preset','8','-svtav1-params','lp=4'], '.mp4', False),
                  ('FFV1', 'ffv1', ['-level','3'], '.mkv', True)]
        for index, (name, encoder, opts, ext, lossless) in enumerate(codecs):
            path = out / f'{encoder}{ext}'
            command(raw_input + ['-an','-c:v',encoder] + opts + ['-threads','4',path])
            seconds = report['commands'][-1]['wall_seconds']
            decoded = out / 'decoded-check.yuv'
            command(['-i',path,'-map','0:v:0','-an','-pix_fmt',scene['pixel_format'],'-f','rawvideo',decoded])
            if decoded.stat().st_size != expected:
                raise ValueError('Decoded frame count/size mismatch')
            exact = sha(decoded) == sha(raw)
            decoded.unlink()
            if lossless and not exact:
                raise ValueError('Lossless video round-trip mismatch')
            metrics = {}
            for metric, pattern in [('ssim', r'All:([0-9.]+)'), ('psnr', r'average:([0-9.]+|inf)')]:
                log = command(['-i',path] + raw_input + ['-lavfi', f'[0:v]settb=expr=1/{scene["fps"]},setpts=N[a];[1:v]settb=expr=1/{scene["fps"]},setpts=N[b];[a][b]{metric}', '-an','-f','null','-'])
                match = re.search(pattern, log)
                if not match:
                    raise ValueError(f'Missing {metric} result')
                metrics[metric] = 'infinity' if match[1] == 'inf' else float(match[1])
            if exact and (metrics['ssim'] != 1.0 or metrics['psnr'] != 'infinity'):
                raise ValueError('Exact frames must have perfect metrics; check frame alignment')
            row(name, path, lossless, encode_seconds=seconds, decoded_exact=exact, quality=metrics)
            zipped = out / f'{encoder}.zip'; start=time.perf_counter(); archive(path, zipped)
            row(f'ZIP of {name}', zipped, lossless, encode_seconds=time.perf_counter()-start,
                quality=metrics, roundtrip_verified=True, zipped_codec=name)
        zipped = out / 'reference-yuv.zip'; start = time.perf_counter(); archive(raw, zipped)
        row('ZIP of raw YUV420p', zipped, True, encode_seconds=time.perf_counter()-start, roundtrip_verified=True)
        for item in report['rows']:
            item['reduction_vs_decoded_raw'] = 1-item['bytes']/expected
        report['status'] = 'completed'
    except Exception as exc:
        report['status'] = 'failed'; report['error'] = str(exc)
        raise
    finally:
        report['finished_at'] = datetime.now(timezone.utc).isoformat()
        atomic_report(out / 'report.json', report)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,required=True)
    p.add_argument('--scene',type=Path,default=Path(__file__).resolve().parents[1]/'benchmarks/media/scene.json')
    p.add_argument('--output',type=Path,required=True)
    a=p.parse_args()
    report=run(a.source.resolve(),json.loads(a.scene.read_text()),a.output)
    print(json.dumps({'status':report['status'],'rows':report['rows']},indent=2))

if __name__=='__main__': main()
