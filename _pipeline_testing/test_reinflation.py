#!/usr/bin/env python3
"""Quick test script to reinflate from existing blueprint JSON."""

import json
import sys
from pathlib import Path
from datetime import datetime
from reinflation import reinflate_document
from config import OUTPUT_DIR, SCHEMAS_DIR

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_reinflation.py <blueprint_json_path>")
        sys.exit(1)
    
    blueprint_path = Path(sys.argv[1])
    if not blueprint_path.exists():
        print(f"Error: Blueprint file not found: {blueprint_path}")
        sys.exit(1)
    
    # Load blueprint
    print(f"Loading blueprint from: {blueprint_path}")
    with open(blueprint_path, "r", encoding="utf-8") as f:
        blueprint_data = json.load(f)
    
    blueprint = blueprint_data.get("blueprint", blueprint_data)
    
    # Determine category from schema_id
    schema_id = blueprint_data.get("schema_id", "")
    if "narrative_fiction" in schema_id:
        category = "narrative_fiction"
    elif "business_plan" in schema_id:
        category = "business_plan"
    elif "report" in schema_id:
        category = "report"
    elif "technical_documentation" in schema_id:
        category = "technical_documentation"
    elif "research_paper" in schema_id:
        category = "research_paper"
    else:
        category = "business_plan"  # Default
    
    # Get prompt path
    prompt_path = SCHEMAS_DIR / category / "v1" / "prompt.json"
    if not prompt_path.exists():
        prompt_path = SCHEMAS_DIR / category / "v1" / "prompt.md"
    
    if not prompt_path.exists():
        print(f"Error: Prompt file not found: {prompt_path}")
        sys.exit(1)
    
    # Create output directory
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_output_dir = OUTPUT_DIR / f"test_reinflation_{run_timestamp}"
    run_output_dir.mkdir(exist_ok=True)
    
    print(f"Reinflating with prompt: {prompt_path}")
    print(f"Output directory: {run_output_dir}")
    
    # Reinflate
    try:
        reinflated_path = reinflate_document(
            blueprint,
            prompt_path,
            run_timestamp,
            run_output_dir
        )
        print(f"\n✅ Reinflation complete!")
        print(f"Output: {reinflated_path}")
    except Exception as e:
        print(f"\n❌ Reinflation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

