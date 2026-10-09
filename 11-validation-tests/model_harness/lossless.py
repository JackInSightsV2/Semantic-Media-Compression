"""Deterministic lossless payload baselines; ZIP includes one-file container overhead."""
import hashlib
import platform
import zlib
from datetime import datetime, timezone
from pathlib import Path
import gzip
import io
import lzma
import zipfile


def zip_bytes(payload):
    stream = io.BytesIO()
    info = zipfile.ZipInfo('payload', date_time=(1980, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile(stream, 'w') as archive:
        archive.writestr(info, payload, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    return stream.getvalue()


def measure(payload):
    """Return full encoded sizes only after verifying exact byte round trips."""
    gz = gzip.compress(payload, compresslevel=9, mtime=0)
    xz = lzma.compress(payload, preset=6)
    zipped = zip_bytes(payload)
    with zipfile.ZipFile(io.BytesIO(zipped)) as archive:
        restored = archive.read('payload')
    if restored != payload or gzip.decompress(gz) != payload or lzma.decompress(xz) != payload:
        raise ValueError('Lossless round-trip mismatch')
    return {'raw': len(payload), 'zip_deflate9': len(zipped), 'gzip9': len(gz), 'xz6': len(xz)}


def compare_report(report):
    """Derived analysis; never mutate historical reports or imply a new model run.

    Sum one independently compressed file per case. Failed/missing blueprints
    use only their paired sources and explicitly expose their case coverage.
    """
    sources = {c['id']: c['source'] for c in report.get('dataset', {}).get('cases', [])}
    rows = []
    for arm in ('full_source', 'openai_blueprint', 'jev_blueprint'):
        totals, source_totals = {}, {}
        count = 0
        for row in report.get('results', []):
            if row.get('case_id') not in sources:
                continue
            a = row.get('arms', {}).get(arm, {})
            if a.get('status') != 'ok' or not isinstance(a.get('context'), str):
                continue
            source = measure(sources[row['case_id']].encode('utf-8'))
            payload = measure(a['context'].encode('utf-8'))
            count += 1
            for name in source:
                source_totals[name] = source_totals.get(name, 0) + source[name]
                totals[name] = totals.get(name, 0) + payload[name]
        rows.append({'arm': arm, 'cases': count, 'attempted_cases': len(report.get('results', [])),
                     'bytes': totals, 'paired_source_bytes': source_totals,
                     'reduction_vs_same_encoding': {k: 1 - totals[k] / source_totals[k]
                         if source_totals[k] else None for k in totals}})
    return {'method': 'lossless-v1', 'derived_at': datetime.now(timezone.utc).isoformat(),
            'analysis_provenance': {'implementation_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                    'python': platform.python_version(), 'zlib': zlib.ZLIB_RUNTIME_VERSION}, 'aggregation': 'Sum of independently encoded files, one per successful case; ZIP member name payload; ZIP container included; gzip9 mtime=0; xz preset6.',
            'interpretation': 'Lossless decoders restore exact input bytes. QA is not rerun: source archives restore full source; blueprint archives restore only the lossy blueprint. No codec includes model, prompt or provenance storage.',
            'rows': rows}
