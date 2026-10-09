#!/usr/bin/env python3
"""Encode length-prefixed JSON bytes as luma pixels; test AV1 exact recovery."""
import argparse
import gzip
import hashlib
import io
import json
import math
import subprocess
import zipfile
from datetime import datetime, timezone
from pathlib import Path


def run(source, output):
    raw=source.read_bytes()
    json.loads(raw)
    output.mkdir(parents=True,exist_ok=False)
    framed=len(raw).to_bytes(4,'big')+raw
    stream=io.BytesIO()
    entry=zipfile.ZipInfo('payload',date_time=(1980,1,1,0,0,0))
    with zipfile.ZipFile(stream,'w') as z:
        z.writestr(entry,raw,compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    report={'created_at':datetime.now(timezone.utc).isoformat(),'source_sha256':hashlib.sha256(raw).hexdigest(),
            'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'raw_json_bytes':len(raw),'zip9_bytes':len(stream.getvalue()),'gzip9_bytes':len(gzip.compress(raw,compresslevel=9,mtime=0)),
            'mapping':'4-byte big-endian JSON byte count then UTF-8 bytes, row-major in 8-bit Y plane; zero padding, constant U/V=128. No colour conversion, rendering or OCR.',
            'ffmpeg':subprocess.check_output(['ffmpeg','-version'],text=True),'results':[]}
    for width in (64,128,256):
        height=max(64,math.ceil(len(framed)/width/2)*2)
        n=width*height
        pixels=framed.ljust(n,b'\0')+bytes([128])*(n//2)
        yuv=output/f'{width}x{height}.yuv';yuv.write_bytes(pixels)
        for label,settings in [('lossless',['-svtav1-params','lossless=1:lp=1']),('crf35',['-crf','35','-svtav1-params','lp=1'])]:
            target=output/f'{width}x{height}-{label}.avif'
            cmd=['ffmpeg','-hide_banner','-loglevel','warning','-nostdin','-f','rawvideo','-pixel_format','yuv420p',
                 '-video_size',f'{width}x{height}','-framerate','1','-i',str(yuv),'-frames:v','1','-c:v','libsvtav1','-preset','0',*settings,str(target)]
            p=subprocess.run(cmd,capture_output=True)
            (output/f'{target.stem}.log').write_bytes(p.stderr)
            result={'width':width,'height':height,'mode':label,'command':cmd,'returncode':p.returncode}
            if p.returncode==0:
                decoded=subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(target),'-frames:v','1','-pix_fmt','yuv420p','-f','rawvideo','-'],capture_output=True,check=True).stdout
                restored=decoded[4:4+len(raw)]
                count=int.from_bytes(decoded[:4],'big')
                result.update(avif_bytes=target.stat().st_size,length_header_correct=count==len(raw),
                              exact_json_recovery=count==len(raw) and restored==raw,
                              changed_json_bytes=sum(a!=b for a,b in zip(raw,restored))+abs(len(raw)-len(restored)),
                              decoded_sha256=hashlib.sha256(restored).hexdigest())
                # Remux AV1 into a raw elementary stream to separate container cost.
                obu=output/f'{target.stem}.obu'
                subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-i',str(target),'-c:v','copy','-f','obu',str(obu)],check=True)
                result['raw_av1_obu_bytes']=obu.stat().st_size
            report['results'].append(result)
            print(json.dumps({k:v for k,v in result.items() if k!='command'}),flush=True)
    (output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path);p.add_argument('output',type=Path)
    a=p.parse_args();run(a.source,a.output)
