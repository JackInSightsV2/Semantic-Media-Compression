import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from model_harness.core import command_predictor, load_dataset, request_for, run, score

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / 'benchmarks/smoke/dataset.json'


class HarnessTests(unittest.TestCase):
    def setUp(self):
        self.data = load_dataset(DATASET)

    def test_scoring(self):
        self.assertAlmostEqual(score({'type': 'binary'}, True, .8)['brier'], .04)
        self.assertEqual(score({'type': 'score', 'range': [0, 4]}, 4, 2)['normalized_mae'], .5)
        result = score({'type': 'facts'}, ['a', 'b'], ['b', 'c'])
        self.assertEqual(result, {'precision': .5, 'recall': .5, 'f1': .5})

    def test_invalid_numbers_and_choices(self):
        for value in (True, -1, 1.1, float('nan'), float('inf'), '0.5'):
            with self.assertRaises(ValueError):
                score({'type': 'binary'}, True, value)
        with self.assertRaises(ValueError):
            score({'type': 'choice', 'options': ['a']}, 'a', 'b')

    def test_request_excludes_reference_and_annotations(self):
        case = copy.deepcopy(self.data['cases'][2])
        case['annotation'] = 'secret answer'
        req = request_for(case, DATASET.parent)
        self.assertNotIn('expected', req)
        self.assertNotIn('annotation', req)
        self.assertTrue(Path(req['input']['media'][0]['path']).is_absolute())
        self.assertFalse(Path(case['input']['media'][0]['path']).is_absolute())

    def test_failures_remain_in_denominator(self):
        report = run(self.data, DATASET.parent, lambda req: {'answers': {}}, {'mode': 'smoke'}, 2)
        self.assertEqual(len(report['results']), 10)
        self.assertTrue(all(s['coverage'] == 0 for s in report['summary'].values()))
        self.assertTrue(all(s['metrics_valid_only'] == {} for s in report['summary'].values()))

    def test_perfect_reference_scores_for_scorer_only(self):
        gold = {c['id']: c['expected'] for c in self.data['cases']}
        def oracle(req):
            return {'answers': {q['id']: int(gold[req['id']][q['id']]) if q['type'] == 'binary'
                                else gold[req['id']][q['id']] for q in req['questions']}}
        report = run(self.data, DATASET.parent, oracle, {'mode': 'unit-test-oracle'})
        self.assertTrue(all(r['status'] == 'ok' for r in report['results']))
        self.assertEqual(report['summary']['decision']['metrics_valid_only']['binary.brier'], 0)

    def test_corrupt_and_escaping_assets(self):
        for path, checksum in [('assets/frame-001.png', 'bad'), ('../../README.md', 'bad')]:
            data = copy.deepcopy(self.data)
            data['cases'][2]['input']['media'][0].update(path=path, sha256=checksum)
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', dir=DATASET.parent) as f:
                json.dump(data, f); f.flush()
                with self.assertRaises(ValueError):
                    load_dataset(f.name)

    def test_timeout_and_non_json(self):
        with self.assertRaises(subprocess.TimeoutExpired):
            command_predictor([sys.executable, '-c', 'import time; time.sleep(2)'], .05)({})
        with self.assertRaises(json.JSONDecodeError):
            command_predictor([sys.executable, '-c', 'print("invalid")'], 2)({})

    def test_nonfinite_output_does_not_break_report(self):
        report = run(self.data, DATASET.parent,
                     lambda req: {'answers': {}, 'usage': float('nan')}, {'mode': 'smoke'})
        json.dumps(report, allow_nan=False)
        self.assertTrue(all(r['status'] == 'error' for r in report['results']))

    def test_cli_smoke_and_failure_exit(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'report.json'
            argv = [sys.executable, '-m', 'model_harness', '--dataset', str(DATASET),
                    '--config', str(DATASET.parent / 'config.json'), '--output', str(output)]
            result = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads(output.read_text())
            self.assertEqual(report['run']['mode'], 'smoke')
            self.assertEqual(report['summary']['image']['metrics_valid_only']['choice.accuracy'], 0)
            config = json.loads((DATASET.parent / 'config.json').read_text())
            config['command'] = [sys.executable, '-c', 'print("{}")']
            cfg = Path(tmp) / 'bad.json'; cfg.write_text(json.dumps(config))
            argv[argv.index('--config') + 1] = str(cfg)
            self.assertEqual(subprocess.run(argv, cwd=ROOT, capture_output=True).returncode, 1)


if __name__ == '__main__':
    unittest.main()
