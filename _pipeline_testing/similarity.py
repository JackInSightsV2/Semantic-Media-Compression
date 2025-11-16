"""Similarity comparison between original and reinflated content."""

import json
from pathlib import Path
from typing import Dict, Any
from llm_client import call_openrouter, extract_json_from_response
from config import RESPONSES_DIR


def compare_similarity(original_text: str, reinflated_text: str, run_timestamp: str, run_output_dir: Path) -> Path:
    """
    Compare semantic similarity between original and reinflated content.
    
    Returns:
        Path to similarity report JSON file
    """
    print("\n" + "=" * 60)
    print("Comparing Semantic Similarity")
    print("=" * 60)
    
    system_msg = """You are an expert evaluator of semantic fidelity in document compression and reinflation.
Your task is to compare an original document with its reinflated version and assess how well the reinflated version preserves the semantic content, structure, and key information of the original.

Evaluate across these dimensions:
1. Semantic Similarity (0-100): How well does the reinflated version capture the core meaning, concepts, and ideas?
2. Structure Preservation (0-100): How well does it preserve the document structure, organization, and flow?
3. Layout Fidelity (0-100): How well does it match the original formatting, headings, and visual organization?
4. Information Completeness (0-100): What percentage of key information, facts, and details are preserved?

Provide a detailed analysis with specific examples of what was preserved well and what was lost or changed."""

    # Use more context for better comparison
    original_sample = original_text[:80000] if len(original_text) > 80000 else original_text
    reinflated_sample = reinflated_text[:80000] if len(reinflated_text) > 80000 else reinflated_text
    
    user_msg = f"""Compare these two documents and provide a similarity assessment:

ORIGINAL DOCUMENT:
---
{original_sample}
---

REINFLATED DOCUMENT:
---
{reinflated_sample}
---

Provide your assessment as JSON with these fields:
- semantic_similarity: integer 0-100
- structure_preservation: integer 0-100
- layout_fidelity: integer 0-100
- information_completeness: integer 0-100
- overall_fidelity: integer 0-100 (average of above)
- strengths: array of strings describing what was preserved well
- weaknesses: array of strings describing what was lost or changed
- detailed_analysis: string with detailed explanation

Return ONLY valid JSON."""

    try:
        response = call_openrouter(system_msg, user_msg, temperature=0.3, response_format_json=True)
        
        # Save response
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_responses_dir = RESPONSES_DIR / run_timestamp
        run_responses_dir.mkdir(exist_ok=True)
        
        response_file = run_responses_dir / f"pass8_attempt1_{timestamp}_similarity_report.json"
        with open(response_file, "w", encoding="utf-8") as f:
            json.dump({
                "metadata": {
                    "pass_number": 8,
                    "attempt_number": 1,
                    "timestamp": timestamp,
                    "description": "similarity_report",
                    "model": response.get("model", "unknown")
                },
                "response": response
            }, f, indent=2)
        
        # Extract and save report
        report_data = extract_json_from_response(response)
        
        report_path = run_output_dir / f"report_{run_timestamp}.json"
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2)
        
        # Print summary
        print(f"\n[OK] Similarity Report:")
        print(f"  Semantic Similarity: {report_data.get('semantic_similarity', 'N/A')}")
        print(f"  Structure: {report_data.get('structure_preservation', 'N/A')}")
        print(f"  Layout: {report_data.get('layout_fidelity', 'N/A')}")
        print(f"  Overall Fidelity: {report_data.get('overall_fidelity', 'N/A')}")
        print(f"\n[OK] Report saved to: {report_path.name}")
        
        return report_path
        
    except Exception as e:
        print(f"\n[ERROR] Similarity comparison failed: {e}")
        import traceback
        traceback.print_exc()
        raise


