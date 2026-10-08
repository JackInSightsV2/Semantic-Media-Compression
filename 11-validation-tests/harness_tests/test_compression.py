import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from model_harness.compression import qa, select_facts, measure_payload, summarize, experiment, pack_facts
from model_harness.providers import OpenAI, ProviderError, Transport
from model_harness.version import provenance

class CompressionTests(unittest.TestCase):
    def test_qa_never_exposes_reference(self):
        class Model:
            def generate(self, instruction, context, schema):
                self.request=context
                return {'q':'unknown'}
        model=Model()
        q={'id':'q','prompt':'Why?','options':{'a':'Fear','unknown':'Not stated'},'expected':'unknown'}
        self.assertEqual(qa(model,'Silent.',[q])['accuracy'],1)
        self.assertNotIn('expected',model.request['questions'][0])
        self.assertEqual(set(model.request),{'context','questions'})

    def test_ranking_budget_and_quote_grounding(self):
        class Jev:
            def decide(self,state,questions):
                return {'support_0':{'noul':.99},'importance_0':{'score':1},'support_1':{'noul':.99},'importance_1':{'score':3}}
        facts=[{'text':'Decorative.','quote':'Grey.'},{'text':'Exit opened.','quote':'Exit opened.'}]
        text,audit=select_facts('Grey. Exit opened.',facts,Jev(),15)
        self.assertEqual(text,'Exit opened.')
        self.assertEqual(audit['kept_indices'],[1])
        facts[0]['quote']='Invented.'
        with self.assertRaises(ValueError): select_facts('Grey. Exit opened.',facts,Jev(),15)

    def test_utf8_size(self):
        size=measure_payload('é'*100,'é'*10)
        self.assertEqual(size['source_bytes'],200)
        self.assertEqual(size['blueprint_bytes'],20)
        self.assertAlmostEqual(size['byte_reduction'],.9)
        self.assertLess(size['source_gzip_bytes'],200)

    def test_hard_budget_keeps_whole_facts(self):
        self.assertEqual(pack_facts(['Too long to retain.', 'éé', 'A'], 6), 'éé\nA')

    def test_failures_in_denominator(self):
        rows=[{'questions':[{}],'arms':{'full_source':{'status':'ok','correct':{'q':True}},'openai_blueprint':{'status':'ok','correct':{'q':True}}}}, {'questions':[{}],'arms':{'openai_blueprint':{'status':'error'}}}]
        m=summarize(rows)['openai_blueprint']
        self.assertEqual(m['accuracy_all_questions'],.5)
        self.assertEqual(m['coverage'],.5)
        self.assertEqual(m['retention_on_full_source_correct'],1)

    def test_wire_contract_pixels_and_isolation(self):
        class Fake:
            def post(self,provider,url,key,payload):
                self.payload=payload
                return {'status':'completed','output':[{'type':'message','content':[{'type':'output_text','text':'{"answer":1}'}]}]}
        fake=Fake()
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'image.png';p.write_bytes(b'PNG')
            result=OpenAI(fake).generate('test',{'data':'x'},{'type':'object'},[{'path':str(p),'mime_type':'image/png','timestamp_seconds':2}])
        self.assertEqual(result,{'answer':1})
        self.assertFalse(fake.payload['store'])
        self.assertNotIn('previous_response_id',fake.payload)
        self.assertEqual(fake.payload['input'][0]['content'][-1]['image_url'],'data:image/png;base64,UE5H')

    def test_provenance(self):
        p=provenance()
        self.assertIn('compression.py',p['files'])
        self.assertIn('dashboard/app.js',p['files'])
        self.assertEqual(len(p['source_sha256']),64)

    def test_call_budget(self):
        with patch.dict('os.environ',{'OPENAI_API_KEY':'test-only'}):
            with self.assertRaises(ProviderError): Transport(max_calls=0).post('openai','https://api.openai.com/v1/responses','OPENAI_API_KEY',{'model':'x'})

    def test_experiment_snapshots_and_arms(self):
        class Model:
            model='fake-unit-test'
            def generate(self,instruction,context,schema):
                if 'facts' in schema['properties']:
                    self.extraction=context
                    return {'facts':[{'text':'Key opens exit.','quote':'key opens exit'}]}
                if 'units' in schema['properties']:
                    self.compression=context
                    return {'units':['Key opens exit.']}
                return {'q':'a'}
        class Jev:
            model='fake-unit-test'
            def decide(self,state,questions): return {'support_0':{'noul':.99},'importance_0':{'score':3}}
        class T:
            max_calls=10
            calls=[]
        model=Model()
        data={'schema_version':1,'id':'test','cases':[{'id':'a','source':'The key opens exit. '*10,'questions':[{'id':'q','prompt':'What opens exit?','options':{'a':'key','unknown':'unknown'},'expected':'a'}]}]}
        with tempfile.TemporaryDirectory() as tmp:
            report=experiment(data,model,Jev(),T(),Path(tmp)/'run')
            self.assertEqual(report['status'],'completed')
            self.assertEqual(len(report['results'][0]['arms']),5)
            self.assertTrue((Path(tmp)/'run/harness_source/compression.py').exists())
            self.assertTrue((Path(tmp)/'run/report.json').exists())
            with self.assertRaises(FileExistsError): experiment(data,model,Jev(),T(),Path(tmp)/'run')
        self.assertNotIn('questions',model.compression)
        self.assertNotIn('questions',model.extraction)

if __name__=='__main__': unittest.main()

class DashboardTests(unittest.TestCase):
    def test_server_only_exposes_known_routes(self):
        from model_harness.dashboard_server import Handler
        from unittest.mock import Mock
        handler=object.__new__(Handler)
        handler.send_error=Mock()
        handler.send_data=Mock()
        for route in ('/.env','/../.env','/harness_source/providers.py','/api/key'):
            handler.path=route
            handler.do_GET()
            handler.send_error.assert_called_with(404)
        handler.send_data.assert_not_called()

    def test_report_errata_preserves_original_file(self):
        from model_harness.dashboard_server import reports
        import json
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/'run';folder.mkdir()
            raw=json.dumps({'kind':'semantic_compression','limitations':['old']})
            (folder/'report.json').write_text(raw)
            (folder/'errata.json').write_text(json.dumps({'correction':'fixed','corrected_limitations':['new']}))
            result=reports(tmp)
            self.assertEqual(result[0]['limitations'],['new'])
            self.assertEqual(result[0]['errata']['correction'],'fixed')
            self.assertEqual((folder/'report.json').read_text(),raw)
