import unittest
from model_harness.scene_semantics import pack, encode, answer


class SceneSemanticsTests(unittest.TestCase):
    def test_budget_counts_json_envelope_and_unicode(self):
        facts=[{'start':0,'end':2,'text':'é'*90},{'start':3,'end':4,'text':'Rabbit approaches flowers.'}]
        result,kept=pack(facts,[0,1],230)
        self.assertLessEqual(len(encode(result)),230)
        self.assertEqual(kept,[1])
        self.assertEqual(result['events'][0]['text'],facts[1]['text'])
        with self.assertRaises(ValueError):pack(facts,[0,1],10)

    def test_question_references_withheld_and_split_metrics(self):
        class Model:
            def generate(self,instruction,context,schema,images):
                self.context=context;self.images=images
                return {'known':'a','unknown':'unknown'}
        model=Model();options={'a':'Rabbit','unknown':'Not established'}
        qs=[{'id':'known','prompt':'Animal?','options':options,'expected':'a','evidence_frame_seconds':[1]},
            {'id':'unknown','prompt':'Name?','options':options,'expected':'unknown','evidence_frame_seconds':[]}]
        result=answer(model,{},qs,images=[{'path':'frame.png'}])
        self.assertEqual((result['answerable_correct'],result['unknown_correct']),(1,1))
        self.assertNotIn('expected',model.context['questions'][0])
        self.assertNotIn('evidence_frame_seconds',model.context['questions'][0])
        self.assertEqual(model.images,[{'path':'frame.png'}])

    def test_4k_fixture_is_not_interpreted_as_360p_raw_video(self):
        import tempfile
        from pathlib import Path
        from unittest.mock import patch
        from model_harness.scene_semantics import experiment
        scene = {'duration_seconds': 30, 'fps': 30, 'width': 3840, 'height': 2160,
                 'reference_sha256': 'fixture'}
        with tempfile.TemporaryDirectory() as temp, \
             patch('model_harness.scene_semantics.sha', return_value='fixture'), \
             patch('model_harness.scene_semantics.subprocess.run', side_effect=RuntimeError('stop before API')) as ffmpeg:
            with self.assertRaisesRegex(RuntimeError, 'stop before API'):
                experiment(Path(temp)/'raw.yuv', scene, {}, None, None, None, Path(temp)/'out')
            command = ffmpeg.call_args.args[0]
            self.assertEqual(command[command.index('-video_size')+1], '3840x2160')
            self.assertEqual(command[command.index('-framerate')+1], '30')
            self.assertIn('mod(n,30)', command[command.index('-vf')+1])

    def test_validity_separates_reader_and_control_failures(self):
        from model_harness.scene_semantics import validity
        annotations = {'predeclared_validity': {'minimum_source_answerable_accuracy': .8,
                                               'maximum_no_context_answerable_accuracy': .25}}
        def rows(source, control):
            return [{'method': name, 'status': 'ok', 'answerable_total': 20, 'answerable_correct': n}
                    for name, n in [('sampled_frames', source), ('no_context', control)]]
        self.assertEqual(validity(rows(18, 0), annotations)['status'], 'controls_passed')
        self.assertEqual(validity(rows(8, 0), annotations)['status'], 'reader_limited')
        self.assertEqual(validity(rows(18, 10), annotations)['status'], 'control_failed')
        self.assertEqual(validity([], annotations)['status'], 'incomplete_controls')

    def test_codec_inputs_reject_mismatched_reference(self):
        import json, tempfile
        from pathlib import Path
        from model_harness.scene_semantics import codec_inputs
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp)
            (p/'report.json').write_text(json.dumps({'status':'completed','scene':{'reference_sha256':'wrong'}}))
            with self.assertRaisesRegex(ValueError, 'match'):
                codec_inputs(p, {'reference_sha256':'correct'})

    def test_codec_inputs_reject_tampered_media(self):
        import json, tempfile
        from pathlib import Path
        from model_harness.scene_semantics import codec_inputs
        scene = {'reference_sha256':'reference','width':3840,'height':1714,'fps':24,'duration_seconds':30}
        with tempfile.TemporaryDirectory() as temp:
            p = Path(temp); (p/'libx264.mp4').write_bytes(b'tampered')
            (p/'report.json').write_text(json.dumps({'status':'completed','scene':scene,
              'rows':[{'file':'libx264.mp4','sha256':'wrong'}]}))
            with self.assertRaisesRegex(ValueError, 'hash mismatch'):
                codec_inputs(p, scene)
