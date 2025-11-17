#!/usr/bin/env python3
"""
Standalone reinflation script.
Reinflates a document from a blueprint JSON file.
"""

import sys
import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

from config import OUTPUT_DIR, SCHEMAS_DIR, CATEGORY_MAP
from schema_loader import load_schema
from reinflation import reinflate_document


def find_schema_from_blueprint(blueprint_data: Dict[str, Any]) -> Path:
    """
    Find the schema path from blueprint metadata.
    
    Args:
        blueprint_data: The full blueprint JSON data (with schema_id, etc.)
    
    Returns:
        Path to the schema.json file
    """
    schema_id = blueprint_data.get("schema_id", "")
    
    # Try to find schema by schema_id
    if schema_id:
        # Map schema_id to schema folder
        for category_key, (data_folder, schema_folder, cat_schema_id) in CATEGORY_MAP.items():
            if cat_schema_id == schema_id:
                schema_path = SCHEMAS_DIR / schema_folder / "v1" / "schema.json"
                if schema_path.exists():
                    return schema_path
    
    # Fallback: try to infer from blueprint structure
    blueprint = blueprint_data.get("blueprint", blueprint_data)
    
    # Check for narrative fiction indicators
    if blueprint.get("story_overview") or blueprint.get("plot_structure"):
        schema_path = SCHEMAS_DIR / "narrative_fiction" / "v1" / "schema.json"
        if schema_path.exists():
            return schema_path
    
    # Check for business plan indicators
    if blueprint.get("executive_summary") or blueprint.get("market_analysis"):
        schema_path = SCHEMAS_DIR / "business_plan" / "v1" / "schema.json"
        if schema_path.exists():
            return schema_path
    
    # Check for technical documentation indicators
    if blueprint.get("api_endpoints") or blueprint.get("technical_specifications"):
        schema_path = SCHEMAS_DIR / "technical_documentation" / "v1" / "schema.json"
        if schema_path.exists():
            return schema_path
    
    # Check for report indicators
    if blueprint.get("report_metadata") or blueprint.get("findings"):
        schema_path = SCHEMAS_DIR / "report" / "v1" / "schema.json"
        if schema_path.exists():
            return schema_path
    
    # Default to research paper
    schema_path = SCHEMAS_DIR / "research_paper" / "v1" / "schema.json"
    if schema_path.exists():
        return schema_path
    
    raise ValueError(f"Could not determine schema from blueprint. schema_id: {schema_id}")


def find_prompt_from_schema(schema_path: Path) -> Path:
    """
    Find the prompt.json file from schema path.
    
    Args:
        schema_path: Path to schema.json
    
    Returns:
        Path to prompt.json (or prompt.md as fallback)
    """
    prompt_path = schema_path.parent / "prompt.json"
    if prompt_path.exists():
        return prompt_path
    
    # Fallback to prompt.md
    prompt_path = schema_path.parent / "prompt.md"
    if prompt_path.exists():
        return prompt_path
    
    raise FileNotFoundError(f"Prompt file not found in {schema_path.parent}")


def main():
    """Main reinflation workflow."""
    parser = argparse.ArgumentParser(
        description="Reinflate a document from a blueprint JSON file",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python reinflate.py blueprint_file.json
  python reinflate.py -o output_dir blueprint_file.json
  python reinflate.py --output-dir custom_output blueprint_file.json
        """
    )
    parser.add_argument(
        "blueprint_file",
        type=str,
        help="Path to blueprint JSON file"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: same directory as blueprint file, or OUTPUT_DIR)"
    )
    parser.add_argument(
        "--schema",
        type=str,
        default=None,
        help="Explicit schema path (optional, will auto-detect if not provided)"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default=None,
        help="Explicit prompt path (optional, will auto-detect if not provided)"
    )
    
    args = parser.parse_args()
    
    # Load blueprint file
    blueprint_path = Path(args.blueprint_file)
    if not blueprint_path.exists():
        print(f"\n[ERROR] Blueprint file not found: {blueprint_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("Reinflating Document from Blueprint")
    print("=" * 60)
    print(f"\n[INFO] Loading blueprint: {blueprint_path.name}")
    
    try:
        with open(blueprint_path, "r", encoding="utf-8") as f:
            blueprint_data = json.load(f)
    except Exception as e:
        print(f"\n[ERROR] Failed to load blueprint: {e}")
        sys.exit(1)
    
    # Extract blueprint (handle both wrapped and unwrapped formats)
    if "blueprint" in blueprint_data:
        blueprint = blueprint_data["blueprint"]
    else:
        blueprint = blueprint_data
    
    print("  [OK] Blueprint loaded")
    
    # Find schema and prompt
    if args.schema:
        schema_path = Path(args.schema)
        if not schema_path.exists():
            print(f"\n[ERROR] Schema file not found: {schema_path}")
            sys.exit(1)
    else:
        try:
            schema_path = find_schema_from_blueprint(blueprint_data)
            print(f"\n[INFO] Auto-detected schema: {schema_path.relative_to(SCHEMAS_DIR)}")
        except Exception as e:
            print(f"\n[ERROR] Could not determine schema: {e}")
            print("  Use --schema to specify explicitly")
            sys.exit(1)
    
    if args.prompt:
        prompt_path = Path(args.prompt)
        if not prompt_path.exists():
            print(f"\n[ERROR] Prompt file not found: {prompt_path}")
            sys.exit(1)
    else:
        try:
            prompt_path = find_prompt_from_schema(schema_path)
            print(f"  [OK] Found prompt: {prompt_path.name}")
        except Exception as e:
            print(f"\n[ERROR] Could not find prompt: {e}")
            print("  Use --prompt to specify explicitly")
            sys.exit(1)
    
    # Determine output directory
    if args.output_dir:
        run_output_dir = Path(args.output_dir)
    else:
        # Use same directory as blueprint file, or create a new timestamped directory
        run_output_dir = blueprint_path.parent
    
    run_output_dir.mkdir(exist_ok=True)
    
    # Create run timestamp
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"\n[INFO] Output directory: {run_output_dir}")
    print(f"  Run timestamp: {run_timestamp}")
    
    # Reinflate
    try:
        reinflated_path = reinflate_document(
            blueprint,
            prompt_path,
            run_timestamp,
            run_output_dir
        )
        
        print("\n" + "=" * 60)
        print("Reinflation Complete")
        print("=" * 60)
        print(f"\n[OK] Reinflated document saved to: {reinflated_path}")
        print(f"  - Blueprint: {blueprint_path.name}")
        print(f"  - Reinflated: {reinflated_path.name}")
        
    except Exception as e:
        print(f"\n[ERROR] Reinflation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

