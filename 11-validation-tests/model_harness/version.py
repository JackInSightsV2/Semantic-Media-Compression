"""Identify the exact harness code, including uncommitted changes."""
import hashlib
import platform
import subprocess
from pathlib import Path

VERSION = '0.5.0'


def provenance():
    root = Path(__file__).resolve().parent
    files = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
             for p in sorted(root.rglob('*')) if p.is_file() and p.suffix in ('.py', '.html', '.js', '.css')}
    from .core import digest
    try:
        commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
        dirty = bool(subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True).strip())
    except (OSError, subprocess.CalledProcessError):
        commit, dirty = None, None
    return {'version': VERSION, 'source_sha256': digest(files), 'files': files,
            'git_commit': commit, 'git_dirty': dirty, 'python': platform.python_version(),
            'platform': platform.platform()}
