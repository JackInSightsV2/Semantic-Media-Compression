"""
Automatically fix extraction issues identified in quality reports.
Targets specific problems and re-extracts missing or incomplete data.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import json


def analyze_quality_issues(quality_report: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze quality report and identify fixable issues.
    
    Returns a plan of what can be fixed:
    - missing_sections: Sections to re-extract
    - missing_references: Whether to re-run reference extraction
    - duplicates: Whether to run deduplication
    - incomplete_fields: Fields that need re-extraction
    """
    plan = {
        "fixes_needed": [],
        "missing_sections": [],
        "missing_references": False,
        "has_duplicates": False,
        "incomplete_fields": []
    }
    
    warnings = quality_report.get("warnings", [])
    metrics = quality_report.get("metrics", {})
    completeness = quality_report.get("completeness", {})
    
    # Check for missing sections
    for warning in warnings:
        if "Missing" in warning and "sections" in warning:
            # Extract missing section titles from warning
            # Format: "Missing 2 sections from blueprint: ['title1', 'title2']"
            import re
            match = re.search(r"\[(.*?)\]", warning)
            if match:
                missing_titles = [t.strip().strip("'\"") for t in match.group(1).split(",")]
                plan["missing_sections"] = missing_titles
                plan["fixes_needed"].append("re_extract_sections")
    
    # Check for missing references
    ref_completeness = completeness.get("references", 100)
    if ref_completeness < 80:  # Less than 80% of references extracted
        plan["missing_references"] = True
        plan["fixes_needed"].append("re_extract_references")
    
    # Check for duplicates
    for warning in warnings:
        if "Extra sections" in warning or "duplicates" in warning.lower():
            plan["has_duplicates"] = True
            plan["fixes_needed"].append("deduplicate_sections")
    
    # Check for missing key fields
    for warning in warnings:
        if "Missing title" in warning:
            plan["incomplete_fields"].append("title")
            plan["fixes_needed"].append("re_extract_title_page")
        if "Missing problem statement" in warning:
            plan["incomplete_fields"].append("problem")
            plan["fixes_needed"].append("re_extract_problem")
    
    return plan


def fix_blueprint(
    blueprint: Dict[str, Any],
    original_text: str,
    quality_report: Dict[str, Any],
    fix_plan: Dict[str, Any],
    schema_path: Path,
    prompt_path: Path,
    run_timestamp: str
) -> Dict[str, Any]:
    """
    Apply fixes to blueprint based on quality report.
    
    Returns updated blueprint with fixes applied.
    """
    from distillation import run_distillation_pass
    from schema_loader import load_schema
    from pass_planner import plan_passes_from_schema
    
    fixed_blueprint = blueprint.copy()
    
    # Load schema for targeted re-extraction
    full_schema = load_schema(schema_path)
    
    # Fix 1: Re-extract missing sections (re-run Pass 1 on specific sections)
    if "re_extract_sections" in fix_plan["fixes_needed"]:
        print("\n[Fix] Re-extracting missing sections...")
        # Re-run Pass 1 to get complete section structure
        # This will merge with existing sections
        try:
            planned_passes = plan_passes_from_schema(full_schema)
            pass1_def = next((p for p in planned_passes if p["pass_name"] == "Pass 1"), None)
            
            if pass1_def:
                result = run_distillation_pass(
                    pass1_def["pass_number"],
                    pass1_def["pass_name"],
                    original_text,
                    full_schema,
                    prompt_path,
                    pass1_def["fields"],
                    pass1_def["always_include"],
                    text_limit=100000,
                    run_timestamp=run_timestamp,
                    use_chunking=True
                )
                # Merge new sections with existing
                from distillation import _deep_merge
                fixed_blueprint = _deep_merge(fixed_blueprint, result)
                print("  [OK] Sections re-extracted and merged")
        except Exception as e:
            print(f"  [WARNING] Failed to re-extract sections: {e}")
    
    # Fix 2: Re-extract references (re-run Pass 7)
    if "re_extract_references" in fix_plan["fixes_needed"]:
        print("\n[Fix] Re-extracting references...")
        try:
            planned_passes = plan_passes_from_schema(full_schema)
            pass7_def = next((p for p in planned_passes if p["pass_name"] == "Pass 7"), None)
            
            if pass7_def:
                # Get NER hints if available
                from entity_extraction import extract_citation_entities, format_ner_hints_for_prompt
                from preprocessing_config import get_preprocessing_config
                
                prep_config = get_preprocessing_config("research_paper")
                ner_hints = None
                if prep_config.use_ner:
                    ner_results = extract_citation_entities(original_text, focus=prep_config.ner_focus)
                    ner_hints = format_ner_hints_for_prompt(ner_results, focus=prep_config.ner_focus)
                
                result = run_distillation_pass(
                    pass7_def["pass_number"],
                    pass7_def["pass_name"],
                    original_text,
                    full_schema,
                    prompt_path,
                    pass7_def["fields"],
                    pass7_def["always_include"],
                    text_limit=100000,
                    run_timestamp=run_timestamp,
                    use_chunking=True,
                    ner_hints=ner_hints
                )
                # Merge new references with existing
                from distillation import _deep_merge
                fixed_blueprint = _deep_merge(fixed_blueprint, result)
                print("  [OK] References re-extracted and merged")
        except Exception as e:
            print(f"  [WARNING] Failed to re-extract references: {e}")
    
    # Fix 3: Deduplicate sections
    if "deduplicate_sections" in fix_plan["fixes_needed"]:
        print("\n[Fix] Deduplicating sections...")
        sections = fixed_blueprint.get("document_structure", {}).get("sections", [])
        if sections:
            deduplicated = _deduplicate_sections(sections)
            fixed_blueprint["document_structure"]["sections"] = deduplicated
            print(f"  [OK] Removed {len(sections) - len(deduplicated)} duplicate sections")
    
    # Fix 4: Re-extract title page
    if "re_extract_title_page" in fix_plan["fixes_needed"]:
        print("\n[Fix] Re-extracting title page...")
        try:
            planned_passes = plan_passes_from_schema(full_schema)
            pass5_def = next((p for p in planned_passes if p["pass_name"] == "Pass 5"), None)
            
            if pass5_def:
                result = run_distillation_pass(
                    pass5_def["pass_number"],
                    pass5_def["pass_name"],
                    original_text,
                    full_schema,
                    prompt_path,
                    pass5_def["fields"],
                    pass5_def["always_include"],
                    text_limit=100000,
                    run_timestamp=run_timestamp,
                    use_chunking=False  # Title page is usually at the start
                )
                from distillation import _deep_merge
                fixed_blueprint = _deep_merge(fixed_blueprint, result)
                print("  [OK] Title page re-extracted")
        except Exception as e:
            print(f"  [WARNING] Failed to re-extract title page: {e}")
    
    # Fix 5: Re-extract problem statement
    if "re_extract_problem" in fix_plan["fixes_needed"]:
        print("\n[Fix] Re-extracting problem statement...")
        try:
            planned_passes = plan_passes_from_schema(full_schema)
            pass1_def = next((p for p in planned_passes if p["pass_name"] == "Pass 1"), None)
            
            if pass1_def:
                result = run_distillation_pass(
                    pass1_def["pass_number"],
                    pass1_def["pass_name"],
                    original_text,
                    full_schema,
                    prompt_path,
                    pass1_def["fields"],
                    pass1_def["always_include"],
                    text_limit=100000,
                    run_timestamp=run_timestamp,
                    use_chunking=True
                )
                from distillation import _deep_merge
                fixed_blueprint = _deep_merge(fixed_blueprint, result)
                print("  [OK] Problem statement re-extracted")
        except Exception as e:
            print(f"  [WARNING] Failed to re-extract problem statement: {e}")
    
    return fixed_blueprint


def _deduplicate_sections(sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Deduplicate sections by normalized title and numbering."""
    import unicodedata
    import re
    
    def normalize_title(title: str) -> str:
        if not title:
            return ""
        normalized = unicodedata.normalize('NFKD', str(title).lower())
        normalized = ''.join(c for c in normalized if not unicodedata.combining(c))
        normalized = ' '.join(normalized.split())
        normalized = re.sub(r'^\d+\.\s*', '', normalized)
        return normalized
    
    seen = set()
    deduplicated = []
    
    for section in sections:
        title = section.get('title', '')
        numbering = str(section.get('numbering', '')).strip().lower()
        
        # Normalize numbering
        if numbering and numbering not in ['arabic', 'roman', 'none', 'null', '']:
            num_match = re.search(r'(\d+)', numbering)
            if num_match:
                numbering = num_match.group(1)
        
        normalized_title = normalize_title(title)
        sig = f"{normalized_title}||{numbering}"
        
        if sig not in seen:
            seen.add(sig)
            deduplicated.append(section)
    
    return deduplicated


def print_fix_plan(fix_plan: Dict[str, Any]) -> None:
    """Print a human-readable fix plan."""
    print("\n" + "=" * 60)
    print("Blueprint Fix Plan")
    print("=" * 60)
    
    if not fix_plan["fixes_needed"]:
        print("\n✅ No fixes needed - blueprint looks good!")
        return
    
    print(f"\nFixes needed: {len(fix_plan['fixes_needed'])}")
    
    if fix_plan["missing_sections"]:
        print(f"\n  Missing sections ({len(fix_plan['missing_sections'])}):")
        for title in fix_plan["missing_sections"][:5]:
            print(f"    - {title}")
    
    if fix_plan["missing_references"]:
        print("\n  ⚠️  Missing references - will re-extract")
    
    if fix_plan["has_duplicates"]:
        print("\n  ⚠️  Duplicate sections found - will deduplicate")
    
    if fix_plan["incomplete_fields"]:
        print(f"\n  Incomplete fields ({len(fix_plan['incomplete_fields'])}):")
        for field in fix_plan["incomplete_fields"]:
            print(f"    - {field}")
    
    print("\n" + "=" * 60)



