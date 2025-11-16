"""Schema-driven pass planning - determines passes from schema.json."""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json


def load_pass_config(schema_path: Path) -> Dict[str, Any]:
    """
    Load pass configuration from schema.json.
    Looks for 'distillation_config' in schema_metadata.
    
    Returns:
        Pass configuration dict or None if not found
    """
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
    
    metadata = schema.get("schema_metadata", {})
    return metadata.get("distillation_config")


def plan_passes_from_schema(full_schema: Dict[str, Any], pass_config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    """
    Plan distillation passes based on schema structure.
    
    If pass_config is provided, use it. Otherwise, automatically group fields.
    
    Args:
        full_schema: Complete schema definition
        pass_config: Optional pass configuration from schema metadata
    
    Returns:
        List of pass configurations, each with:
        - pass_number: int
        - pass_name: str (template name in prompt.md)
        - fields: List[str] (field names to extract)
        - always_include: List[str] (fields to always include)
    """
    if pass_config:
        # Use explicit configuration from schema
        passes = []
        for i, pass_def in enumerate(pass_config.get("passes", []), 1):
            passes.append({
                "pass_number": i,
                "pass_name": pass_def.get("name", f"Pass {i}"),
                "fields": pass_def.get("fields", []),
                "always_include": pass_def.get("always_include", []),
            })
        return passes
    
    # Auto-plan based on schema structure
    required_fields = full_schema.get("required", [])
    all_fields = list(full_schema.get("properties", {}).keys())
    
    # Group fields logically
    # Pass 1: Overview, structure, metadata (NO layout - too complex)
    pass1_fields = [
        "problem_and_motivation", "prior_work", "executive_summary",
        "story_overview", "overview", "purpose_and_scope",
        "document_structure", "tone_metadata"
    ]
    
    # Pass 2: Core content (NO examples - too many)
    pass2_fields = [
        "contributions", "setup_and_assumptions", "products_and_services",
        "characters", "plot_structure", "setting", "methodology"
    ]
    
    # Pass 3: Detailed content
    pass3_fields = [
        "methodology", "implementation", "narrative_style",
        "quotes_and_dialogue", "quotes_and_anecdotes"
    ]
    
    # Pass 4: Results, conclusions, advanced features
    pass4_fields = [
        "results", "limitations", "implications", "conclusion",
        "narrative_sequence", "scenes", "narrative_flow", "storytelling_techniques"
    ]
    
    # Pass 5: Metadata, references (research papers)
    pass5_fields = [
        "references"
    ]
    
    # Pass 6: Detailed table/figure data (research papers)
    pass6_fields = [
        # Tables and figures are in document_structure, but we extract detailed data
    ]
    
    # Filter to only fields that exist in schema
    def filter_fields(candidates: List[str]) -> List[str]:
        return [f for f in candidates if f in all_fields]
    
    passes = []
    
    # Pass 1
    p1_fields = filter_fields(pass1_fields)
    if p1_fields or "document_structure" in all_fields or "tone_metadata" in all_fields:
        passes.append({
            "pass_number": 1,
            "pass_name": "Pass 1",
            "fields": p1_fields,
            "always_include": ["document_structure", "tone_metadata"] if "document_structure" in all_fields else [],
        })
    
    # Pass 2
    p2_fields = filter_fields(pass2_fields)
    if p2_fields:
        passes.append({
            "pass_number": 2,
            "pass_name": "Pass 2",
            "fields": p2_fields,
            "always_include": [],
        })
    
    # Pass 3
    p3_fields = filter_fields(pass3_fields)
    if p3_fields:
        passes.append({
            "pass_number": 3,
            "pass_name": "Pass 3",
            "fields": p3_fields,
            "always_include": [],
        })
    
    # Pass 4
    p4_fields = filter_fields(pass4_fields)
    if p4_fields:
        passes.append({
            "pass_number": 4,
            "pass_name": "Pass 4",
            "fields": p4_fields,
            "always_include": [],
        })
    
    # Pass 5: Metadata (author affiliations, acknowledgements)
    # Pass 5 updates document_structure.title_page only
    if 'document_structure' in all_fields:
        passes.append({
            "pass_number": 5,
            "pass_name": "Pass 5",
            "fields": [],
            "always_include": ["document_structure"],  # Update title_page only
        })
    
    # Pass 6: Detailed table/figure data
    # Check if document_structure has tables/figures that need detailed extraction
    if 'document_structure' in all_fields:
        # We'll enhance tables/figures in document_structure
        passes.append({
            "pass_number": 6,
            "pass_name": "Pass 6",
            "fields": [],
            "always_include": ["document_structure"],  # Re-extract with detailed data
        })
    
    # Pass 7: References (isolated for better extraction and formatting)
    # Pass 7 updates document_structure.references only
    if 'document_structure' in all_fields:
        passes.append({
            "pass_number": 7,
            "pass_name": "Pass 7",
            "fields": [],
            "always_include": ["document_structure"],  # Update references only
        })
    
    # Pass 8: Layout metadata (isolated for focused extraction)
    if 'layout_metadata' in all_fields:
        passes.append({
            "pass_number": 8,
            "pass_name": "Pass 8",
            "fields": ["layout_metadata"],
            "always_include": [],
        })
    
    # Pass 9: Examples and case studies (isolated - can be 100+ examples)
    if 'examples_and_case_studies' in all_fields:
        passes.append({
            "pass_number": 9,
            "pass_name": "Pass 9",
            "fields": ["examples_and_case_studies"],
            "always_include": [],
        })
    
    # Additional passes for any remaining required fields
    extracted_fields = set()
    for p in passes:
        extracted_fields.update(p["fields"])
        extracted_fields.update(p["always_include"])
    
    remaining_required = [f for f in required_fields if f not in extracted_fields]
    remaining_optional = [f for f in all_fields if f not in extracted_fields and f not in required_fields]
    
    if remaining_required or remaining_optional:
        # Create additional passes for remaining fields
        pass_num = len(passes) + 1
        remaining_fields = remaining_required + remaining_optional[:10]  # Limit to 10 per pass
        
        if remaining_fields:
            passes.append({
                "pass_number": pass_num,
                "pass_name": f"Pass {pass_num}",
                "fields": remaining_fields,
                "always_include": [],
            })
    
    return passes

