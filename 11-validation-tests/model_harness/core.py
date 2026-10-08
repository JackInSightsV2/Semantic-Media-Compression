"""Dataset validation, isolated requests and independently computed metrics."""
from __future__ import annotations

import hashlib
import json
import math
import statistics
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def number(value, low, high):
    if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError(f"Expected finite number in [{low}, {high}]")
    return value


def strings(value):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x for x in value):
        raise ValueError("Expected a list of nonempty strings")
    if len(value) != len(set(value)):
        raise ValueError("Duplicate items are not allowed")
    return value


def score(question, expected, prediction):
    kind = question['type']
    if kind == 'binary':
        p = number(prediction, 0, 1)
        if type(expected) is not bool:
            raise ValueError('Binary reference must be boolean')
        return {'accuracy': float((p >= 0.5) == expected), 'brier': (p - int(expected)) ** 2}
    if kind == 'choice':
        options = strings(question['options'])
        if expected not in options or prediction not in options:
            raise ValueError('Choice outside declared options')
        return {'accuracy': float(prediction == expected)}
    if kind == 'score':
        low, high = question['range']
        number(low, -1e9, 1e9)
        number(high, -1e9, 1e9)
        if high <= low:
            raise ValueError('Score range must increase')
        return {'normalized_mae': abs(number(prediction, low, high) - number(expected, low, high)) / (high - low)}
    if kind == 'facts':
        gold, found = set(strings(expected)), set(strings(prediction))
        tp = len(gold & found)
        return {'precision': tp / len(found) if found else float(not gold),
                'recall': tp / len(gold) if gold else 1.0,
                'f1': 2 * tp / (len(gold) + len(found)) if gold or found else 1.0}
    raise ValueError(f'Unknown question type: {kind}')


def load_dataset(path):
    path = Path(path).resolve()
    data = json.loads(path.read_text())
    if data['schema_version'] != 1 or not data['cases']:
        raise ValueError('Expected schema_version 1 and nonempty cases')
    ids = set()
    for case in data['cases']:
        if not isinstance(case['id'], str) or not case['id'] or case['id'] in ids:
            raise ValueError('Case IDs must be unique nonempty strings')
        ids.add(case['id'])
        if case['track'] not in ('decision', 'image', 'video_frames', 'blueprint_qa'):
            raise ValueError('Unsupported track')
        if not isinstance(case['input'], dict) or not case['questions']:
            raise ValueError('Expected input object and nonempty questions')
        qids = set()
        for q in case['questions']:
            if not isinstance(q['id'], str) or not q['id'] or q['id'] in qids or not q['prompt']:
                raise ValueError('Invalid or duplicate question ID / empty prompt')
            qids.add(q['id'])
            gold = case['expected'][q['id']]
            score(q, gold, int(gold) if q['type'] == 'binary' else gold)
        if qids != set(case['expected']):
            raise ValueError('Reference keys must match questions exactly')
        media = case['input'].get('media', [])
        if case['track'] in ('image', 'video_frames') and not media:
            raise ValueError('Visual tracks require actual media')
        if case['track'] in ('decision', 'blueprint_qa') and media:
            raise ValueError('Text tracks must not include source media')
        timestamps = []
        for asset in media:
            target = (path.parent / asset['path']).resolve()
            if not target.is_relative_to(path.parent) or not target.is_file():
                raise ValueError('Media must exist inside dataset directory')
            actual = hashlib.sha256(target.read_bytes()).hexdigest()
            if asset.get('sha256') != actual:
                raise ValueError('Media checksum mismatch')
            if case['track'] == 'video_frames':
                timestamps.append(number(asset['timestamp_seconds'], 0, 1e9))
        if timestamps and (len(timestamps) < 2 or any(a >= b for a, b in zip(timestamps, timestamps[1:]))):
            raise ValueError('Video requires at least two frames with increasing timestamps')
    return data


def request_for(case, root):
    # Explicit allowlist: annotations and reference answers never enter this object.
    request = {k: case[k] for k in ('id', 'track', 'input', 'questions')}
    request = json.loads(json.dumps(request))
    for asset in request['input'].get('media', []):
        asset['path'] = str((Path(root) / asset['path']).resolve())
    return request


def run(data, root, predict, metadata, repeats=1):
    if type(repeats) is not int or repeats < 1:
        raise ValueError('repeats must be positive')
    rows = []
    for repeat in range(repeats):
        for case in data['cases']:
            request = request_for(case, root)
            row = {'case_id': case['id'], 'track': case['track'], 'repeat': repeat,
                   'request_sha256': digest(request), 'status': 'error'}
            started = time.perf_counter()
            try:
                response = predict(request)
                # Reject non-JSON numbers before storing raw output in a report.
                json.dumps(response, allow_nan=False)
                row['response'] = response
                answers = response['answers']
                if set(answers) != set(case['expected']):
                    raise ValueError('Missing or extra answer keys')
                metrics = {q['id']: score(q, case['expected'][q['id']], answers[q['id']])
                           for q in case['questions']}
                row.update(status='ok', metrics=metrics)
            except Exception as exc:
                # Do not persist exception text: provider errors may contain credentials.
                row['error_type'] = type(exc).__name__
            row['wall_seconds'] = time.perf_counter() - started
            rows.append(row)
    groups = {}
    for track in sorted({r['track'] for r in rows}):
        selected = [r for r in rows if r['track'] == track]
        valid = [r for r in selected if r['status'] == 'ok']
        metrics = {}
        for row in valid:
            for qid, values in row['metrics'].items():
                case = next(c for c in data['cases'] if c['id'] == row['case_id'])
                kind = next(q['type'] for q in case['questions'] if q['id'] == qid)
                for key, value in values.items():
                    metrics.setdefault(f'{kind}.{key}', []).append(value)
        times = sorted(r['wall_seconds'] for r in selected)
        groups[track] = {'attempted': len(selected), 'valid': len(valid),
                         'coverage': len(valid) / len(selected),
                         'p50_wall_seconds': statistics.median(times),
                         'p95_wall_seconds': times[math.ceil(.95 * len(times)) - 1],
                         'metrics_valid_only': {k: statistics.mean(v) for k, v in metrics.items()}}
    return {'schema_version': 1, 'created_at': datetime.now(timezone.utc).isoformat(),
            'dataset_id': data['id'], 'dataset_sha256': digest(data),
            'run': metadata, 'repeats': repeats, 'summary': groups, 'results': rows}


def command_predictor(argv, timeout):
    def predict(request):
        completed = subprocess.run(argv, input=json.dumps(request), text=True,
                                   capture_output=True, timeout=timeout, check=True)
        return json.loads(completed.stdout)
    return predict
