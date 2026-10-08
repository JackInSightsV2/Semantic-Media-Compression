"""Run with python -m model_harness from 11-validation-tests."""
import argparse
import json
from pathlib import Path

from .core import command_predictor, load_dataset, run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dataset', type=Path, required=True)
    parser.add_argument('--config', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--repeats', type=int, default=1)
    args = parser.parse_args()
    try:
        data = load_dataset(args.dataset)
        config = json.loads(args.config.read_text())
        for key in ('model', 'revision', 'runtime', 'hardware', 'parameters', 'mode'):
            if key not in config:
                raise ValueError(f'Config requires {key}')
        if config['mode'] not in ('smoke', 'live'):
            raise ValueError('mode must be smoke or live')
        argv = config['command']
        if not isinstance(argv, list) or not argv or any(not isinstance(x, str) for x in argv):
            raise ValueError('command must be a nonempty argv array')
        timeout = config.get('timeout_seconds', 60)
        if not isinstance(timeout, (int, float)) or not 0 < timeout <= 3600:
            raise ValueError('timeout_seconds must be in (0, 3600]')
        report = run(data, args.dataset.resolve().parent,
                     command_predictor(argv, timeout), config, args.repeats)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')
        print(json.dumps(report['summary'], indent=2))
        return int(any(r['status'] != 'ok' for r in report['results']))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    raise SystemExit(main())
