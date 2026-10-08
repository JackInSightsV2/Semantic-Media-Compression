"""Small HTTP clients. Keys stay in process memory; no SDK dependency."""
from __future__ import annotations

import base64
import json
import os
import ssl
import time
import urllib.error
import urllib.request
from pathlib import Path

from .core import digest

REPO = Path(__file__).resolve().parents[2]


def load_env(path=None):
    path = Path(path or REPO / '.env')
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        name, sep, value = line.partition('=')
        name = name.removeprefix('export ').strip()
        if sep and name.replace('_', '').isalnum():
            os.environ.setdefault(name, value.strip().strip('\"\''))


class ProviderError(RuntimeError):
    """Messages contain only status categories, never response bodies or keys."""


class Transport:
    def __init__(self, max_calls=40, timeout=90):
        self.max_calls = max_calls
        self.timeout = timeout
        self.calls = []
        # macOS framework Python may not ship a CA bundle; use the OS trust bundle.
        cafile = os.environ.get('SSL_CERT_FILE')
        if not cafile and Path('/etc/ssl/cert.pem').is_file():
            cafile = '/etc/ssl/cert.pem'
        self.ssl_context = ssl.create_default_context(cafile=cafile)

    def post(self, provider, url, key_name, payload):
        key = os.environ.get(key_name)
        if not key:
            raise ProviderError(f'Missing {key_name}')
        if len(self.calls) >= self.max_calls:
            raise ProviderError('Run call limit reached')
        record = {'provider': provider, 'requested_model': payload['model'],
                  'request_sha256': digest(payload), 'status': 'error'}
        self.calls.append(record)
        start = time.perf_counter()
        try:
            req = urllib.request.Request(url, json.dumps(payload, allow_nan=False).encode(),
                                         {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=self.timeout, context=self.ssl_context) as response:
                data = json.load(response)
            record.update(status='ok', resolved_model=data.get('model'), usage=data.get('usage'),
                          response_id=data.get('id'))
            return data
        except urllib.error.HTTPError as exc:
            record['http_status'] = exc.code
            raise ProviderError(f'{provider} HTTP {exc.code}') from None
        except (urllib.error.URLError, TimeoutError):
            raise ProviderError(f'{provider} network/timeout failure') from None
        finally:
            record['wall_seconds'] = time.perf_counter() - start


def object_schema(properties):
    return {'type': 'object', 'properties': properties, 'required': list(properties), 'additionalProperties': False}


class OpenAI:
    def __init__(self, transport, model='gpt-4.1-mini-2025-04-14'):
        self.transport, self.model = transport, model

    def generate(self, instruction, context, schema, media=()):
        content = [{'type': 'input_text', 'text': json.dumps(context, ensure_ascii=False)}]
        for asset in media:
            if 'timestamp_seconds' in asset:
                content.append({'type': 'input_text', 'text': f"Frame at {asset['timestamp_seconds']} seconds"})
            raw = Path(asset['path']).read_bytes()
            content.append({'type': 'input_image', 'detail': 'high',
                            'image_url': f"data:{asset['mime_type']};base64,{base64.b64encode(raw).decode()}"})
        payload = {'model': self.model, 'store': False, 'max_output_tokens': 2400,
                   'instructions': instruction,
                   'input': [{'role': 'user', 'content': content}],
                   'text': {'format': {'type': 'json_schema', 'name': 'benchmark_output',
                                       'strict': True, 'schema': schema}}}
        data = self.transport.post('openai', 'https://api.openai.com/v1/responses', 'OPENAI_API_KEY', payload)
        if data.get('status') != 'completed':
            raise ProviderError('OpenAI response incomplete')
        texts = [part['text'] for item in data.get('output', []) if item.get('type') == 'message'
                 for part in item.get('content', []) if part.get('type') == 'output_text']
        if not texts:
            raise ProviderError('OpenAI returned no structured text')
        return json.loads(''.join(texts))


class Jev:
    def __init__(self, transport, model='jev-1.13.0'):
        self.transport, self.model = transport, model

    def decide(self, state, questions):
        data = self.transport.post('jev', 'https://api.typesafe.ai/v1/systemone', 'TYPESAFE_API_KEY',
                                   {'model': self.model, 'state': state, 'questions': questions})
        return data['answers']
