"""Sample actual scene frames, extract facts, pack JSON budgets, and measure isolated QA."""
import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from .core import digest, number
from .compression import ANSWER, atomic_report
from .lossless import measure, zip_bytes
from .media_baseline import sha
from .providers import Jev, OpenAI, Transport, load_env, object_schema
from .version import provenance

EXTRACT = ('Describe only visible evidence from these ordered timestamped images. They are sampled at 1 fps; '
           'do not infer unseen intermediate motion, audio, names, motives or dates. Do not identify the film or use prior plot knowledge. '
           'Extract 12-20 short self-contained visual facts covering subjects, appearance, setting, actions/changes, '
           'objects, their colours, spatial relationships and camera/viewpoint sequence. Each text must name its subject '
           'without referring to another fact. Give first and last supplied frame seconds supporting each fact. '
           'Avoid repetitive facts. Evaluation questions are deliberately withheld.')


def encode(payload):
    return json.dumps(payload, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode('utf-8')


def payload(facts):
    return {'v': 1, 'duration_s': 30, 'sample_fps': 1, 'audio': False,
            'evidence': 'sampled frames; omitted details unknown',
            'events': [{'t': [f['start'], f['end']], 'text': f['text']} for f in facts]}


def pack(facts, order, budget):
    if len(encode(payload([]))) > budget:
        raise ValueError('Budget too small for envelope')
    kept = []
    for index in order:
        candidate = sorted(kept + [index])
        if len(encode(payload([facts[i] for i in candidate]))) <= budget:
            kept = candidate
    return payload([facts[i] for i in kept]), kept


def answer(model, context, questions, images=()):
    public = [{k: q[k] for k in ('id', 'prompt', 'options')} for q in questions]
    schema = object_schema({q['id']: {'type': 'string', 'enum': list(q['options'])} for q in questions})
    result = model.generate(ANSWER, {'context': context, 'questions': public}, schema, images)
    if set(result) != {q['id'] for q in questions} or any(result[q['id']] not in q['options'] for q in questions):
        raise ValueError('Invalid QA answer keys/options')
    correct = {q['id']: result[q['id']] == q['expected'] for q in questions}
    known = [q for q in questions if q['expected'] != 'unknown']
    unknown = [q for q in questions if q['expected'] == 'unknown']
    return {'answers': result, 'correct': correct, 'correct_count': sum(correct.values()), 'total': len(questions),
            'answerable_correct': sum(correct[q['id']] for q in known), 'answerable_total': len(known),
            'unknown_correct': sum(correct[q['id']] for q in unknown), 'unknown_total': len(unknown)}


def codec_inputs(directory, scene):
    directory = Path(directory)
    report = json.loads((directory/'report.json').read_text())
    if report['status'] != 'completed' or any(report['scene'][k] != scene[k] for k in
            ('reference_sha256', 'width', 'height', 'fps', 'duration_seconds')):
        raise ValueError('Codec run must be completed and match the semantic reference')
    inputs = []
    for name in ('libx264.mp4', 'libx265.mp4', 'libsvtav1.mp4'):
        row = next(r for r in report['rows'] if r['file'] == name)
        path = directory/name
        if sha(path) != row['sha256']:
            raise ValueError('Codec file hash mismatch')
        inputs.append((path, row))
    return report, inputs


def validity(rows, annotations):
    thresholds = annotations.get('predeclared_validity')
    if not thresholds:
        return {'status': 'not_predeclared'}
    by_name = {r['method']: r for r in rows}
    source, control = by_name.get('sampled_frames', {}), by_name.get('no_context', {})
    if any(r.get('status') != 'ok' or not r.get('answerable_total') for r in (source, control)):
        return {'status': 'incomplete_controls', 'thresholds': thresholds}
    s = source['answerable_correct']/source['answerable_total']
    c = control['answerable_correct']/control['answerable_total']
    status = ('control_failed' if c > thresholds['maximum_no_context_answerable_accuracy'] else
              'reader_limited' if s < thresholds['minimum_source_answerable_accuracy'] else 'controls_passed')
    return {'status': status, 'source_accuracy': s, 'no_context_accuracy': c, 'thresholds': thresholds}


def experiment(reference, scene, annotations, model, jev, transport, out, codec_run=None):
    if scene['duration_seconds'] != 30 or scene['fps'] != int(scene['fps']):
        raise ValueError('Semantic fixture requires 30 seconds at an integer frame rate')
    if sha(reference) != scene['reference_sha256']:
        raise ValueError('Reference hash does not match the pinned scene')
    codec_report, codecs = codec_inputs(codec_run, scene) if codec_run else (None, [])
    out = Path(out); out.mkdir(parents=True, exist_ok=False)
    frame_dir = out / 'frames'; frame_dir.mkdir()
    command = ['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-f','rawvideo','-pixel_format','yuv420p',
               '-video_size',f"{scene['width']}x{scene['height']}",'-framerate',str(scene['fps']),'-i',str(reference),'-vf',f"select='not(mod(n,{scene['fps']}))'",
               '-fps_mode','vfr','-frames:v','30',str(frame_dir/'frame-%02d.png')]
    subprocess.run(command, check=True)
    paths = sorted(frame_dir.glob('*.png'))
    if len(paths) != 30:
        raise ValueError('Expected exactly 30 sampled frames')
    images = [{'path': str(p), 'mime_type': 'image/png', 'timestamp_seconds': i} for i, p in enumerate(paths)]
    report = {'schema_version': 1, 'kind': 'scene_semantics', 'run_id': out.name, 'status': 'running',
              'created_at': datetime.now(timezone.utc).isoformat(), 'harness': provenance(),
              'scene': scene, 'annotations': annotations, 'annotation_sha256': digest(annotations),
              'config': {'model': model.model, 'jev_model': jev.model, 'max_calls': transport.max_calls,
                         'budgets': [512,1024,2048,4096], 'extract_prompt': EXTRACT, 'qa_prompt': ANSWER,
                         'max_output_tokens':2400},
              'sampling_command': command, 'frames': [{'seconds': i, 'file':p.name, 'bytes':p.stat().st_size, 'sha256':sha(p)} for i,p in enumerate(paths)],
              'calls': transport.calls, 'rows': [],
              'limitations': ['One well-known public scene; agent-authored references, no independent annotation.',
                  'Full-resolution PNGs are submitted; provider-side image preprocessing may resize them. This does not prove retention of every 4K pixel.',
                  '1 fps omits unsampled motion; all audio omitted. Same model extracts and answers, single trial.',
                  'JEV ranks text facts, does not see or independently verify image evidence.',
                  'ZIP restores JSON only; no video reconstruction was attempted. Sizes exclude model, prompts, provenance and referenced assets.',
                  'Best means smallest tested payload at an observed QA score; no optimality or generalisation claim.']}
    for rel in report['harness']['files']:
        dest = out/'harness_source'/rel; dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_bytes((Path(__file__).parent/rel).read_bytes())
    atomic_report(out/'report.json',report)
    if codec_report:
        report['codec_comparison'] = {'run_id': codec_report['run_id'], 'harness': codec_report['harness'],
                                    'report_sha256': sha(Path(codec_run)/'report.json')}
    try:
        schema = object_schema({'facts': {'type':'array','minItems':12,'maxItems':20,
            'items':object_schema({'start':{'type':'integer','minimum':0,'maximum':29},
                                   'end':{'type':'integer','minimum':0,'maximum':29}, 'text':{'type':'string'}})}})
        facts = model.generate(EXTRACT, {'duration_s':30,'sample_fps':1,'audio':False},schema,images)['facts']
        if not 12 <= len(facts) <= 20 or any(not f['text'].strip() or not 0 <= f['start'] <= f['end'] <=29 for f in facts):
            raise ValueError('Invalid visual facts')
        report['extracted_facts'] = facts
        decisions = jev.decide({'facts':facts}, {f'importance_{i}':{'type':'score',
            'instructions':f'How valuable is facts[{i}] for retaining visual scene meaning for unspecified future questions? Avoid repetitive details. You have text descriptions only; do not infer or verify pixels.',
            'criteria':['Repetitive minor detail','Useful detail','Important subject/action/viewpoint','Essential subject, change or relationship']}
            for i in range(len(facts))})
        report['jev_decisions'] = decisions
        order=sorted(range(len(facts)),key=lambda i:(-number(decisions[f'importance_{i}']['score'],0,3),i))
        contexts=[('sampled_frames',None,None),('no_context','',None),('full_json',payload(facts),None)]
        for budget in report['config']['budgets']:
            packed,indices=pack(facts,order,budget)
            contexts.append((f'jev_json_{budget}',packed,{'budget':budget,'kept_indices':indices}))
        packed,indices=pack(facts,list(range(len(facts))),1024)
        contexts.append(('chronological_json_1024',packed,{'budget':1024,'kept_indices':indices}))
        codec_images = {}
        for path, codec in codecs:
            directory = out/path.stem; directory.mkdir()
            args = ['ffmpeg','-hide_banner','-loglevel','error','-nostdin','-i',str(path),
                    '-vf',f"select='not(mod(n,{scene['fps']}))'",'-fps_mode','vfr','-frames:v','30',
                    str(directory/'frame-%02d.png')]
            subprocess.run(args, check=True)
            samples = sorted(directory.glob('*.png'))
            if len(samples) != 30:
                raise ValueError('Expected 30 codec sample frames')
            name = 'codec_'+path.stem
            codec_images[name] = [{'path':str(p),'mime_type':'image/png','timestamp_seconds':i}
                                  for i,p in enumerate(samples)]
            contexts.append((name, None, {'video_bytes':codec['bytes'], 'codec':codec['method'],
                             'video_sha256':codec['sha256'], 'sampling_command':args,
                             'sample_sha256':[sha(p) for p in samples]}))
        atomic_report(out/'report.json',report)
        for name, context, meta in contexts:
            row={'method':name,'status':'running',**(meta or {})};report['rows'].append(row)
            try:
                if isinstance(context,dict):
                    raw=encode(context);row['bytes']=measure(raw);row['payload']=context
                    (out/f'{name}.json').write_bytes(raw)
                    (out/f'{name}.zip').write_bytes(zip_bytes(raw))
                row.update(answer(model,context,annotations['questions'],
                           images if name=='sampled_frames' else codec_images.get(name, ())),status='ok')
            except Exception as exc:
                row.update(status='error',error_type=type(exc).__name__)
            atomic_report(out/'report.json',report)
            print(name,row['status'],row.get('correct_count'),row.get('bytes'),flush=True)
        report['status']='completed' if all(r['status']=='ok' for r in report['rows']) else 'partial'
        report['validity'] = validity(report['rows'], annotations)
    except Exception as exc:
        report['status']='failed';report['error_type']=type(exc).__name__
        raise
    finally:
        report['finished_at']=datetime.now(timezone.utc).isoformat()
        atomic_report(out/'report.json',report)
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--reference',type=Path,required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--model',default='gpt-4.1-mini-2025-04-14')
    root=Path(__file__).resolve().parents[1]/'benchmarks/media'
    p.add_argument('--scene',type=Path,default=root/'scene.json')
    p.add_argument('--questions',type=Path,default=root/'questions.json')
    p.add_argument('--codec-run',type=Path,help='Completed codec run from the identical pinned reference')
    a=p.parse_args();load_env()
    t=Transport(max_calls=13 if a.codec_run else 10, timeout=240)
    r=experiment(a.reference,json.loads(a.scene.read_text()),json.loads(a.questions.read_text()),
                 OpenAI(t,a.model),Jev(t),t,a.output,codec_run=a.codec_run)
    raise SystemExit(0 if r['status']=='completed' else 1)

if __name__=='__main__': main()
