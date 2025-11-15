#!/usr/bin/env python3
"""Analyze token usage and scores across multiple pipeline runs."""

import json
from pathlib import Path
from collections import defaultdict

# Run timestamps from the 5 runs
runs = [
    '20251115_171634',  # Run 1 (from earlier)
    '20251115_172353',  # Run 2
    '20251115_172846',  # Run 3
    '20251115_184204',  # Run 4
    '20251115_184719',  # Run 5
    '20251115_185201',  # Run 6 (actually 5th in our test)
]

# Known scores from terminal output
scores_data = {
    '20251115_171634': {'semantic': 88, 'structure': 75, 'layout': 65, 'overall': 77},
    '20251115_172353': {'semantic': 92, 'structure': 85, 'layout': 78, 'overall': 88},
    '20251115_172846': {'semantic': 85, 'structure': 80, 'layout': 75, 'overall': 82},
    '20251115_184204': {'semantic': 88, 'structure': 82, 'layout': 78, 'overall': 85},
    '20251115_184719': {'semantic': 92, 'structure': 85, 'layout': 78, 'overall': 88},
    '20251115_185201': {'semantic': 88, 'structure': 82, 'layout': 78, 'overall': 85},
}

results = {}

for run_id in runs:
    resp_dir = Path(f'responses/{run_id}')
    if not resp_dir.exists():
        continue
    
    tokens = {
        'prompt_tokens': 0,
        'completion_tokens': 0,
        'total_tokens': 0,
        'reasoning_tokens': 0
    }
    
    # Read all response files
    for resp_file in resp_dir.glob('*.json'):
        try:
            with open(resp_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            usage = data.get('response', {}).get('usage', {})
            tokens['prompt_tokens'] += usage.get('prompt_tokens', 0)
            tokens['completion_tokens'] += usage.get('completion_tokens', 0)
            tokens['total_tokens'] += usage.get('total_tokens', 0)
            
            # Get reasoning tokens if available
            comp_details = usage.get('completion_tokens_details', {})
            if comp_details:
                tokens['reasoning_tokens'] += comp_details.get('reasoning_tokens', 0)
        except Exception as e:
            print(f"Error reading {resp_file}: {e}")
    
    results[run_id] = {
        'tokens': tokens,
        'scores': scores_data.get(run_id, {})
    }

# Print comparison table
print("=" * 100)
print("CONSISTENCY TEST RESULTS - 5 RUNS COMPARISON")
print("=" * 100)
print()

print(f"{'Run ID':<20} {'Semantic':<12} {'Structure':<12} {'Layout':<12} {'Overall':<12} {'Total Tokens':<15}")
print("-" * 100)

for run_id in runs:
    if run_id not in results:
        continue
    r = results[run_id]
    scores = r['scores']
    tokens = r['tokens']
    
    print(f"{run_id:<20} {scores.get('semantic', 0):<12} {scores.get('structure', 0):<12} {scores.get('layout', 0):<12} {scores.get('overall', 0):<12} {tokens['total_tokens']:,}")

print()
print("=" * 100)
print("DETAILED TOKEN USAGE PER RUN")
print("=" * 100)
print()

for run_id in runs:
    if run_id not in results:
        continue
    r = results[run_id]
    tokens = r['tokens']
    scores = r['scores']
    
    print(f"Run: {run_id}")
    print(f"  Scores: Semantic={scores.get('semantic', 0)}/100, Structure={scores.get('structure', 0)}/100, Layout={scores.get('layout', 0)}/100, Overall={scores.get('overall', 0)}/100")
    print(f"  Tokens: Prompt={tokens['prompt_tokens']:,}, Completion={tokens['completion_tokens']:,}, Total={tokens['total_tokens']:,}")
    if tokens['reasoning_tokens'] > 0:
        print(f"  Reasoning Tokens: {tokens['reasoning_tokens']:,}")
    print()

print("=" * 100)
print("STATISTICAL SUMMARY")
print("=" * 100)
print()

# Calculate statistics
valid_runs = [r for r in runs if r in results]
if valid_runs:
    semantic_scores = [results[r]['scores'].get('semantic', 0) for r in valid_runs]
    structure_scores = [results[r]['scores'].get('structure', 0) for r in valid_runs]
    layout_scores = [results[r]['scores'].get('layout', 0) for r in valid_runs]
    overall_scores = [results[r]['scores'].get('overall', 0) for r in valid_runs]
    total_tokens = [results[r]['tokens']['total_tokens'] for r in valid_runs]
    
    print(f"Semantic Similarity:")
    print(f"  Average: {sum(semantic_scores)/len(semantic_scores):.1f}/100")
    print(f"  Range: {min(semantic_scores)}-{max(semantic_scores)}")
    print(f"  Variance: {max(semantic_scores) - min(semantic_scores)} points")
    print()
    
    print(f"Structure:")
    print(f"  Average: {sum(structure_scores)/len(structure_scores):.1f}/100")
    print(f"  Range: {min(structure_scores)}-{max(structure_scores)}")
    print(f"  Variance: {max(structure_scores) - min(structure_scores)} points")
    print()
    
    print(f"Layout:")
    print(f"  Average: {sum(layout_scores)/len(layout_scores):.1f}/100")
    print(f"  Range: {min(layout_scores)}-{max(layout_scores)}")
    print(f"  Variance: {max(layout_scores) - min(layout_scores)} points")
    print()
    
    print(f"Overall Fidelity:")
    print(f"  Average: {sum(overall_scores)/len(overall_scores):.1f}/100")
    print(f"  Range: {min(overall_scores)}-{max(overall_scores)}")
    print(f"  Variance: {max(overall_scores) - min(overall_scores)} points")
    print()
    
    print(f"Token Usage:")
    print(f"  Average: {sum(total_tokens)/len(total_tokens):,.0f} tokens")
    print(f"  Range: {min(total_tokens):,}-{max(total_tokens):,} tokens")
    print(f"  Variance: {max(total_tokens) - min(total_tokens):,} tokens ({((max(total_tokens) - min(total_tokens)) / (sum(total_tokens)/len(total_tokens)) * 100):.1f}%)")
    print(f"  Total across all runs: {sum(total_tokens):,} tokens")

