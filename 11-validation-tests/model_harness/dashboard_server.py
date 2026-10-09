"""Read-only local dashboard. Never serves the repository or .env."""
import argparse
import json
import re
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from .lossless import compare_report

STATIC = Path(__file__).resolve().parent / 'dashboard'


def reports(root):
    result = []
    for path in sorted(Path(root).glob('*/report.json'), reverse=True):
        if not re.fullmatch(r'[A-Za-z0-9_-]+', path.parent.name) or path.is_symlink() or path.parent.is_symlink():
            continue
        try:
            data = json.loads(path.read_text())
            if data.get('kind') == 'semantic_compression':
                errata = path.parent / 'errata.json'
                if errata.is_file() and not errata.is_symlink():
                    data['errata'] = json.loads(errata.read_text())
                    data['limitations'] = data['errata'].get('corrected_limitations', data.get('limitations', []))
                data['lossless_comparison'] = compare_report(data)
                result.append(data)
        except (ValueError, OSError):
            continue
    return result


class Handler(BaseHTTPRequestHandler):
    def __init__(self, *args, runs, media_runs=None, **kwargs):
        self.runs = runs
        self.media_runs = Path(media_runs) if media_runs else Path(runs).parent / 'media_runs'
        super().__init__(*args, **kwargs)

    def do_GET(self):
        route = urlparse(self.path).path
        if route == '/api/runs':
            self.send_data(json.dumps(reports(self.runs), allow_nan=False).encode(), 'application/json')
        elif route in ('/api/media', '/api/scene'):
            result = []
            root = self.media_runs if route == '/api/media' else Path(self.runs).parent / 'scene_runs'
            kind = 'media_codec_baseline' if route == '/api/media' else 'scene_semantics'
            for path in sorted(root.glob('*/report.json'), reverse=True):
                if path.is_symlink() or path.parent.is_symlink() or not re.fullmatch(r'[A-Za-z0-9_-]+', path.parent.name):
                    continue
                try:
                    data = json.loads(path.read_text())
                    if data.get('kind') == kind:
                        errata = path.parent / 'errata.json'
                        if errata.is_file() and not errata.is_symlink():
                            data['errata'] = json.loads(errata.read_text())
                            data['status'] = data['errata'].get('status', data['status'])
                            data['limitations'].append(data['errata'].get('reason', 'See errata'))
                            for row in data['rows']:
                                row.pop('quality', None)
                        result.append(data)
                except (OSError, ValueError):
                    continue
            self.send_data(json.dumps(result, allow_nan=False).encode(), 'application/json')
        elif re.fullmatch(r'/media-preview/[A-Za-z0-9_-]+', route):
            directory = self.media_runs / route.rsplit('/', 1)[1]
            path = directory / 'libx264.mp4'
            if directory.is_symlink() or path.is_symlink() or not path.is_file():
                self.send_error(404)
            else:
                self.send_data(path.read_bytes(), 'video/mp4')
        elif route in ('/', '/index.html', '/app.js', '/style.css'):
            name = 'index.html' if route == '/' else route[1:]
            mime = {'html': 'text/html', 'js': 'text/javascript', 'css': 'text/css'}[name.rsplit('.', 1)[1]]
            self.send_data((STATIC / name).read_bytes(), mime)
        else:
            self.send_error(404)

    def send_data(self, content, mime):
        self.send_response(200)
        self.send_header('Content-Type', mime if mime.startswith('video/') else mime + '; charset=utf-8')
        self.send_header('Content-Length', str(len(content)))
        self.send_header('Cache-Control', 'no-store')
        self.send_header('X-Content-Type-Options', 'nosniff')
        self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; frame-ancestors 'none'")
        self.end_headers()
        self.wfile.write(content)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--runs', type=Path, default=Path(__file__).resolve().parents[1] / 'testing_outputs/benchmark_runs')
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), partial(Handler, runs=args.runs))
    print(f'Local dashboard: http://127.0.0.1:{server.server_port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
