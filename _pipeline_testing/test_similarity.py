#!/usr/bin/env python3
"""Quick test script to compare original and reinflated documents."""

import json
import sys
from pathlib import Path
from datetime import datetime
from file_handlers import extract_text_from_file
from similarity import compare_similarity
from config import OUTPUT_DIR

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 test_similarity.py <original_file> <reinflated_file>")
        sys.exit(1)
    
    original_path = Path(sys.argv[1])
    reinflated_path = Path(sys.argv[2])
    
    if not original_path.exists():
        print(f"Error: Original file not found: {original_path}")
        sys.exit(1)
    
    if not reinflated_path.exists():
        print(f"Error: Reinflated file not found: {reinflated_path}")
        sys.exit(1)
    
    # Extract original text
    print(f"Extracting text from: {original_path}")
    original_text = extract_text_from_file(original_path)
    print(f"  Original: {len(original_text)} characters")
    
    # Read reinflated text
    print(f"Reading reinflated text from: {reinflated_path}")
    with open(reinflated_path, "r", encoding="utf-8") as f:
        reinflated_text = f.read()
    print(f"  Reinflated: {len(reinflated_text)} characters")
    
    # Create output directory
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_output_dir = OUTPUT_DIR / f"test_similarity_{run_timestamp}"
    run_output_dir.mkdir(exist_ok=True)
    
    # Compare
    print(f"\nComparing similarity...")
    report_path = compare_similarity(original_text, reinflated_text, run_timestamp, run_output_dir)
    
    # Read and display results
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)
    
    print(f"\n{'='*60}")
    print("SIMILARITY RESULTS")
    print(f"{'='*60}")
    print(f"Semantic Similarity: {report.get('semantic_similarity', 'N/A')}/100")
    print(f"Structure: {report.get('structure_preservation', 'N/A')}/100")
    print(f"Layout: {report.get('layout_fidelity', 'N/A')}/100")
    print(f"Overall Fidelity: {report.get('overall_fidelity', 'N/A')}/100")
    if 'information_completeness' in report:
        print(f"Information Completeness: {report.get('information_completeness', 'N/A')}/100")
    print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    main()


