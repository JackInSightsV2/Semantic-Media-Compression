#!/usr/bin/env python3
"""Offline repository inventory and Markdown link/claim-signal audit; no APIs."""
import argparse
import json
import re
import subprocess
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    'quantitative_claim': r'\d[\d,.]*(?:\s?%|\s?[x×]|\s?:\s?1)|[$£€]\s?\d',
    'certainty_claim': r'\b(?:proves?|guarantee[ds]?|validated|legally admissible|production.ready|mathematical proof)\b',
    'time_sensitive': r'\b(?:current(?:ly)?|state.of.the.art|today|202[345])\b',
}


def inspect(root=ROOT):
    files = sorted(set(subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=root).decode().strip('\0').split('\0')) - {''})
    inventory, broken = [], []
    for rel in files:
        path = root / rel
        if not path.is_file():
            continue
        kind = 'markdown' if path.suffix == '.md' else 'source' if path.suffix in ('.py','.js','.mjs','.ts','.tsx','.css','.html','.bat') else 'artifact_or_config'
        item = {'path':rel,'kind':kind,'bytes':path.stat().st_size}
        if kind == 'markdown':
            text = path.read_text()
            item['signals'] = {name: len(re.findall(pattern,text,re.I)) for name,pattern in PATTERNS.items()}
            item['evidence_notice'] = 'AUDIT-STATUS: 2026-10-08' in text
            # Ignore fenced code examples. Fragments are not validated by this check.
            in_code=False
            for lineno,line in enumerate(text.splitlines(),1):
                if line.lstrip().startswith('```'):
                    in_code=not in_code
                    continue
                if in_code: continue
                for target in re.findall(r'\]\(([^)]+)\)',line):
                    target=target.strip().strip('<>')
                    if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',target) or target.startswith('#'): continue
                    target=unquote(target.split('#',1)[0])
                    if target and not (path.parent/target).exists():
                        broken.append({'path':rel,'line':lineno,'target':target})
        inventory.append(item)
    return {'scope':'All tracked and nonignored working-tree files. Static signals identify review candidates; they do not establish truth. Binary contents and remote links are not verified.',
            'counts':dict(Counter(x['kind'] for x in inventory)), 'files':inventory,
            'missing_local_markdown_targets':broken}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    parser.add_argument('--check-links',action='store_true',help='Exit nonzero when local Markdown file targets are missing')
    args=parser.parse_args()
    report=inspect()
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'counts':report['counts'],'missing_local_markdown_targets':report['missing_local_markdown_targets']},indent=2))

    if args.check_links and report['missing_local_markdown_targets']:
        raise SystemExit(1)

if __name__=='__main__': main()
