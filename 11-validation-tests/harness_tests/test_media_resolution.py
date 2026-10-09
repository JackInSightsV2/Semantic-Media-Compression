import json
import unittest
from unittest.mock import patch
from model_harness.media_baseline import probe_source

class ResolutionTests(unittest.TestCase):
    def probe(self, width, height, target):
        data = {'streams': [{'width': width, 'height': height, 'codec_name': 'h264'}]}
        with patch('model_harness.media_baseline.subprocess.check_output', return_value=json.dumps(data)):
            return probe_source('fixture.mp4', target)

    def test_rejects_1080p_source_for_4k_target(self):
        with self.assertRaisesRegex(ValueError, 'upscaled'):
            self.probe(1920, 1080, {'width': 3840, 'height': 2160})

    def test_preserves_4k_source_dimensions(self):
        result = self.probe(3840, 2160, {'width': 3840, 'height': 2160})
        self.assertEqual((result['width'], result['height']), (3840, 2160))
