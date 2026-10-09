import io
import unittest
import zipfile
from model_harness.lossless import compare_report, measure, zip_bytes


class LosslessTests(unittest.TestCase):
    def test_zip_roundtrip_and_reproducibility(self):
        for payload in (b'', 'é\n'.encode() * 100, bytes(range(256)) * 4):
            encoded = zip_bytes(payload)
            self.assertEqual(encoded, zip_bytes(payload))
            with zipfile.ZipFile(io.BytesIO(encoded)) as archive:
                self.assertEqual(archive.read('payload'), payload)
            self.assertEqual(measure(payload)['zip_deflate9'], len(encoded))
        self.assertGreater(measure(b'x')['zip_deflate9'], 1)

    def test_pairing_coverage_and_aggregation(self):
        source = 'A fact. ' * 100
        report = {'dataset': {'cases': [{'id': 'a', 'source': source}, {'id': 'b', 'source': 'other'}]},
                  'results': [{'case_id': 'a', 'arms': {'jev_blueprint': {'status': 'ok', 'context': 'A fact.'}}},
                              {'case_id': 'b', 'arms': {'jev_blueprint': {'status': 'error'}}}]}
        row = compare_report(report)['rows'][2]
        self.assertEqual((row['cases'], row['attempted_cases']), (1, 2))
        self.assertEqual(row['paired_source_bytes'], measure(source.encode()))
        self.assertEqual(row['bytes'], measure(b'A fact.'))
        self.assertAlmostEqual(row['reduction_vs_same_encoding']['zip_deflate9'],
                               1 - len(zip_bytes(b'A fact.')) / len(zip_bytes(source.encode())))


class MediaBoundaryTests(unittest.TestCase):
    def test_archive_and_source_mismatch(self):
        import tempfile
        from pathlib import Path
        from model_harness.media_baseline import archive, run
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);source=root/'input';source.write_bytes(bytes(range(256))*200)
            archive(source,root/'output.zip')
            with zipfile.ZipFile(root/'output.zip') as z:
                self.assertEqual(z.read('payload'),source.read_bytes())
            with self.assertRaisesRegex(ValueError,'Source hash'):
                run(source,{'source_sha256':'wrong'},root/'run')
            self.assertFalse((root/'run').exists())

    def test_dashboard_media_errata_and_symlink(self):
        import tempfile, json
        from pathlib import Path
        from unittest.mock import Mock
        from model_harness.dashboard_server import Handler
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);run=root/'run';run.mkdir()
            raw=json.dumps({'kind':'media_codec_baseline','status':'completed','limitations':[],
                            'rows':[{'quality':{'ssim':.9}}]})
            (run/'report.json').write_text(raw)
            (run/'errata.json').write_text(json.dumps({'status':'invalid_quality_metrics','reason':'bad alignment'}))
            (run/'libx264.mp4').symlink_to(run/'report.json')
            h=object.__new__(Handler);h.media_runs=root;h.send_data=Mock();h.send_error=Mock()
            h.path='/api/media';h.do_GET()
            data=json.loads(h.send_data.call_args.args[0])
            self.assertEqual(data[0]['status'],'invalid_quality_metrics')
            self.assertNotIn('quality',data[0]['rows'][0])
            self.assertEqual((run/'report.json').read_text(),raw)
            h.path='/media-preview/run';h.do_GET();h.send_error.assert_called_with(404)
