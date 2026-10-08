"""Deliberately naive baseline; exercises the protocol, never a model benchmark."""
import json
import sys

request = json.load(sys.stdin)
answers = {}
for q in request['questions']:
    answers[q['id']] = {'binary': lambda: 0.5,
                        'choice': lambda: q['options'][0],
                        'score': lambda: sum(q['range']) / 2,
                        'facts': lambda: []}[q['type']]()
json.dump({'answers': answers}, sys.stdout)
