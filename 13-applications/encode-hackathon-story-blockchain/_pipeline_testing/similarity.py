"""Similarity comparison between original and reinflated content."""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from llm_client import call_openrouter, extract_json_from_response
from config import RESPONSES_DIR


def compare_similarity(original_text: str, reinflated_text: str, run_timestamp: str, run_output_dir: Path, logging_service: Optional[Any] = None) -> Path:
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

CRITICAL: If the original text is explicitly stated as "not available" or is a placeholder message, you MUST score ALL dimensions low (0-20) because there is no basis for comparison. You cannot assess preservation without the original document.

Evaluate across these dimensions:
1. Semantic Similarity (0-100): How well does the reinflated version capture the core meaning, concepts, and ideas? If original is not available, score 0.
2. Structure Preservation (0-100): How well does it preserve the document structure, organization, and flow? If original is not available, you can only assess if the reinflated document has reasonable structure (score 20-40 max), but you cannot assess preservation without the original.
3. Layout Fidelity (0-100): Focus on STRUCTURAL ALIGNMENT - do chapters, sections, and headings align between original and reinflated? If original is not available, you can only assess if the reinflated document has reasonable layout (score 20-40 max), but you cannot assess fidelity without the original.
4. Information Completeness (0-100): What percentage of key information, facts, and details are preserved? If original is not available, score 0.

CRITICAL RULES:
- If original text is "not available" or a placeholder: ALL scores must be 0-20 (semantic and completeness = 0, structure/layout = 20-40 max for internal consistency only)
- DO NOT give high scores (80+) for structure/layout if you cannot compare to an original
- DO NOT penalize plain text vs markdown formatting (e.g., "# Title" vs "Title" is fine if they align)
- DO penalize missing chapters/sections, misaligned headings, or structural mismatches when original IS available
- Format differences (plain text vs markdown) should NOT reduce the score

Provide a detailed analysis with specific examples of what was preserved well and what was lost or changed. If original is not available, clearly state this limitation in your analysis."""

    # Check if original text is actually available or just a placeholder
    is_placeholder = (
        "not available" in original_text.lower() or 
        "placeholder" in original_text.lower() or
        "ORIGINAL TEXT NOT AVAILABLE" in original_text or
        len(original_text) < 200  # Very short text is likely a placeholder
    )
    
    # Use more context for better comparison
    original_sample = original_text[:80000] if len(original_text) > 80000 else original_text
    reinflated_sample = reinflated_text[:80000] if len(reinflated_text) > 80000 else reinflated_text
    
    if is_placeholder:
        user_msg = f"""⚠️ CRITICAL: THE ORIGINAL DOCUMENT TEXT IS NOT AVAILABLE ⚠️

You are comparing a reinflated document against a PLACEHOLDER MESSAGE, NOT against the actual original document.

ORIGINAL DOCUMENT STATUS:
---
{original_sample}
---

REINFLATED DOCUMENT:
---
{reinflated_sample}
---

⚠️ MANDATORY SCORING RULES (BECAUSE ORIGINAL IS NOT AVAILABLE):
- semantic_similarity: MUST be 0 (cannot assess semantic preservation without original)
- structure_preservation: MUST be 0-20 (can only assess if reinflated has reasonable structure, but CANNOT assess preservation without original)
- layout_fidelity: MUST be 0-20 (can only assess if reinflated has reasonable layout, but CANNOT assess fidelity without original)
- information_completeness: MUST be 0 (cannot assess completeness without original)
- overall_fidelity: MUST be 0-10 (average of above, will be very low)

DO NOT give high scores (80+) for structure/layout just because the reinflated document looks organized. Without the original, you CANNOT assess preservation or fidelity - only internal consistency.

Provide your assessment as JSON with these fields:
- semantic_similarity: MUST be 0
- structure_preservation: MUST be 0-20
- layout_fidelity: MUST be 0-20
- information_completeness: MUST be 0
- overall_fidelity: MUST be 0-10
- strengths: array of strings (but note limitations - cannot assess preservation)
- weaknesses: array of strings (MUST include "Original text not available for comparison")
- detailed_analysis: string (MUST explain that original is not available and scores are low because of this)

Return ONLY valid JSON."""
    else:
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
        response, metrics = call_openrouter(system_msg, user_msg, temperature=0.3, response_format_json=True)
        
        # Log metrics if logging service is provided
        if logging_service:
            usage = metrics.get("usage", {})
            response_time_ms = metrics.get("response_time_ms", 0)
            logging_service.record_llm_call(response, response_time_ms)
        
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


