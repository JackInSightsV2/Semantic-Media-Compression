"""
Quality checks for distilled blueprints before reinflation.
Compares blueprint content with original document to catch extraction issues.
"""

from typing import Dict, Any, List, Tuple
import re
from collections import Counter


def check_blueprint_quality(blueprint: Dict[str, Any], original_text: str, category: str = "research_paper") -> Dict[str, Any]:
    """
    Check quality of distilled blueprint against original document.
    
    Returns a quality report with:
    - Completeness scores
    - Missing elements warnings
    - Extraction quality metrics
    """
    try:
        report = {
            "completeness": {},
            "warnings": [],
            "metrics": {},
            "quality_score": 0
        }
        
        # Normalize category for matching
        category_lower = category.lower() if category else ""
        
        if category_lower in ["research_paper", "research", "paper"]:
            report = _check_research_paper_quality(blueprint, original_text)
        elif category_lower in ["technical_documentation", "technical"]:
            report = _check_technical_documentation_quality(blueprint, original_text)
        elif category_lower == "report":
            report = _check_report_quality(blueprint, original_text)
        elif category_lower in ["business_plan", "business", "plan"]:
            report = _check_business_plan_quality(blueprint, original_text)
        elif category_lower in ["narrative_fiction", "fiction", "narrative", "story"]:
            report = _check_narrative_fiction_quality(blueprint, original_text)
        else:
            # Default report for unknown categories - still try to extract basic metrics
            report["warnings"].append(f"Unknown category '{category}' - using generic quality check")
            # Try to extract at least some basic metrics
            blueprint_sections = blueprint.get('document_structure', {}).get('sections', [])
            original_sections = _extract_sections_from_text(original_text)
            report["metrics"]["original_sections"] = len(original_sections)
            report["metrics"]["blueprint_sections"] = len(blueprint_sections)
            if len(original_sections) > 0:
                report["completeness"]["sections"] = (len(blueprint_sections) / len(original_sections) * 100)
            else:
                report["completeness"]["sections"] = 100 if len(blueprint_sections) > 0 else 0
            report["quality_score"] = report["completeness"].get("sections", 100)
        
        return report
    except Exception as e:
        # Return error report instead of failing silently
        import traceback
        print(f"  [ERROR] Quality check exception: {e}")
        traceback.print_exc()
        return {
            "completeness": {},
            "warnings": [f"Quality check failed: {str(e)}"],
            "metrics": {},
            "quality_score": 0,
            "error": str(e)
        }


def _check_research_paper_quality(blueprint: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """Check quality for research paper blueprints."""
    report = {
        "completeness": {},
        "warnings": [],
        "metrics": {},
        "quality_score": 0
    }
    
    # Extract sections from original document
    original_sections = _extract_sections_from_text(original_text)
    blueprint_sections = blueprint.get('document_structure', {}).get('sections', [])
    
    # Compare section counts
    original_section_count = len(original_sections)
    blueprint_section_count = len(blueprint_sections)
    
    report["metrics"]["original_sections"] = original_section_count
    report["metrics"]["blueprint_sections"] = blueprint_section_count
    
    # Only calculate completeness if we found sections
    if original_section_count > 0:
        report["completeness"]["sections"] = min(100, (blueprint_section_count / original_section_count * 100))
        
        # Check for missing sections
        original_titles = {_normalize_title(s['title']) for s in original_sections}
        blueprint_titles = {_normalize_title(s.get('title', '')) for s in blueprint_sections}
        
        missing_titles = original_titles - blueprint_titles
        if missing_titles:
            report["warnings"].append(f"Missing {len(missing_titles)} sections from blueprint: {list(missing_titles)[:5]}")
        
        # Check for extra sections in blueprint (might indicate duplicates)
        extra_titles = blueprint_titles - original_titles
        if extra_titles and len(extra_titles) > len(blueprint_titles) * 0.1:  # More than 10% extra
            report["warnings"].append(f"Extra sections in blueprint (possible duplicates): {len(extra_titles)}")
    else:
        # If we couldn't extract sections, still report counts and calculate based on blueprint
        if blueprint_section_count > 0:
            report["completeness"]["sections"] = 100  # Assume complete if we can't verify original
            report["warnings"].append("Could not extract sections from original text - assuming blueprint is complete")
        else:
            report["completeness"]["sections"] = 0
            report["warnings"].append("Could not extract sections from original text and blueprint has no sections")
    
    # Check references
    original_ref_count = _count_references_in_text(original_text)
    blueprint_refs = blueprint.get('document_structure', {}).get('references', [])
    blueprint_ref_count = len(blueprint_refs)
    
    report["metrics"]["original_references"] = original_ref_count
    report["metrics"]["blueprint_references"] = blueprint_ref_count
    if original_ref_count > 0:
        report["completeness"]["references"] = (blueprint_ref_count / original_ref_count * 100)
        if blueprint_ref_count < original_ref_count * 0.8:  # Less than 80%
            report["warnings"].append(f"Missing references: {original_ref_count} in original, {blueprint_ref_count} in blueprint")
    
    # Check for key elements
    structure = blueprint.get('document_structure', {})
    
    # Title page
    title_page = structure.get('title_page', {})
    if not title_page.get('title'):
        report["warnings"].append("Missing title in blueprint")
    
    # Problem & motivation
    if not blueprint.get('problem_and_motivation', {}).get('problem'):
        report["warnings"].append("Missing problem statement in blueprint")
    
    # Calculate overall quality score
    completeness_scores = [v for v in report["completeness"].values() if isinstance(v, (int, float))]
    if completeness_scores:
        # Cap scores at 100% (extra sections don't improve quality)
        capped_scores = [min(100, score) for score in completeness_scores]
        base_score = sum(capped_scores) / len(capped_scores)
    else:
        # If no completeness metrics, check if we have basic structure
        if blueprint_section_count > 0 or blueprint_ref_count > 0:
            base_score = 75  # Partial credit if we have some structure
        else:
            base_score = 50  # Lower score if no structure found
    
    # Penalize for warnings - each warning reduces score by 5% (less harsh)
    warning_penalty = min(len(report["warnings"]) * 5, 30)  # Max 30% penalty
    report["quality_score"] = max(0, round(base_score - warning_penalty, 1))
    
    return report


def _check_technical_documentation_quality(blueprint: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """Check quality for technical documentation blueprints."""
    report = {
        "completeness": {},
        "warnings": [],
        "metrics": {},
        "quality_score": 0
    }
    
    # Extract sections from original document
    original_sections = _extract_sections_from_text(original_text)
    blueprint_sections = blueprint.get('document_structure', {}).get('sections', [])
    
    # Compare section counts
    original_section_count = len(original_sections)
    blueprint_section_count = len(blueprint_sections)
    
    report["metrics"]["original_sections"] = original_section_count
    report["metrics"]["blueprint_sections"] = blueprint_section_count
    
    # Only calculate completeness if we found sections
    if original_section_count > 0:
        report["completeness"]["sections"] = (blueprint_section_count / original_section_count * 100)
        
        # Check for missing sections
        original_titles = {_normalize_title(s['title']) for s in original_sections}
        blueprint_titles = {_normalize_title(s.get('title', '')) for s in blueprint_sections}
        
        missing_titles = original_titles - blueprint_titles
        if missing_titles:
            report["warnings"].append(f"Missing {len(missing_titles)} sections from blueprint: {list(missing_titles)[:5]}")
        
        # Check for extra sections in blueprint (might indicate duplicates)
        extra_titles = blueprint_titles - original_titles
        if extra_titles and len(extra_titles) > len(blueprint_titles) * 0.1:  # More than 10% extra
            report["warnings"].append(f"Extra sections in blueprint (possible duplicates): {len(extra_titles)}")
    else:
        # If we couldn't extract sections, still report counts
        report["warnings"].append("Could not extract sections from original text (check extraction pattern)")
        if blueprint_section_count > 0:
            report["completeness"]["sections"] = 100  # Assume complete if we can't verify
    
    # Check references
    original_ref_count = _count_references_in_text(original_text)
    blueprint_refs = blueprint.get('document_structure', {}).get('references', [])
    blueprint_ref_count = len(blueprint_refs)
    
    report["metrics"]["original_references"] = original_ref_count
    report["metrics"]["blueprint_references"] = blueprint_ref_count
    if original_ref_count > 0:
        report["completeness"]["references"] = (blueprint_ref_count / original_ref_count * 100)
        if blueprint_ref_count < original_ref_count * 0.8:  # Less than 80%
            report["warnings"].append(f"Missing references: {original_ref_count} in original, {blueprint_ref_count} in blueprint")
    
    # Check for key elements
    structure = blueprint.get('document_structure', {})
    
    # Title page
    title_page = structure.get('title_page', {})
    if not title_page.get('title'):
        report["warnings"].append("Missing title in blueprint")
    
    # Problem & motivation (for technical docs, this might be "overview" or "purpose")
    problem = blueprint.get('problem_and_motivation', {})
    if not problem.get('problem') and not problem.get('why_it_matters'):
        report["warnings"].append("Missing problem statement or purpose in blueprint")
    
    # Check for examples/case studies (important for technical docs)
    examples = blueprint.get('examples_and_case_studies', [])
    report["metrics"]["examples_count"] = len(examples)
    if len(examples) == 0:
        report["warnings"].append("No examples or case studies found in blueprint")
    
    # Calculate overall quality score
    completeness_scores = [v for v in report["completeness"].values() if isinstance(v, (int, float))]
    if completeness_scores:
        # Cap scores at 100% (extra sections don't improve quality)
        capped_scores = [min(100, score) for score in completeness_scores]
        base_score = sum(capped_scores) / len(capped_scores)
    else:
        base_score = 100  # If no metrics, assume good
    
    # Penalize for warnings - each warning reduces score by 10%
    warning_penalty = min(len(report["warnings"]) * 10, 50)  # Max 50% penalty
    report["quality_score"] = max(0, base_score - warning_penalty)
    
    return report


def _check_report_quality(blueprint: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """Check quality for report blueprints."""
    report = {
        "completeness": {},
        "warnings": [],
        "metrics": {},
        "quality_score": 0
    }
    
    # Extract sections from original document
    original_sections = _extract_sections_from_text(original_text)
    blueprint_sections = blueprint.get('document_structure', {}).get('sections', [])
    
    # Compare section counts
    original_section_count = len(original_sections)
    blueprint_section_count = len(blueprint_sections)
    
    report["metrics"]["original_sections"] = original_section_count
    report["metrics"]["blueprint_sections"] = blueprint_section_count
    
    # Only calculate completeness if we found sections
    if original_section_count > 0:
        report["completeness"]["sections"] = (blueprint_section_count / original_section_count * 100)
        
        # Check for missing sections
        original_titles = {_normalize_title(s['title']) for s in original_sections}
        blueprint_titles = {_normalize_title(s.get('title', '')) for s in blueprint_sections}
        
        missing_titles = original_titles - blueprint_titles
        if missing_titles:
            report["warnings"].append(f"Missing {len(missing_titles)} sections from blueprint: {list(missing_titles)[:5]}")
        
        # Check for extra sections in blueprint (might indicate duplicates)
        extra_titles = blueprint_titles - original_titles
        if extra_titles and len(extra_titles) > len(blueprint_titles) * 0.1:  # More than 10% extra
            report["warnings"].append(f"Extra sections in blueprint (possible duplicates): {len(extra_titles)}")
    else:
        # If we couldn't extract sections, still report counts
        report["warnings"].append("Could not extract sections from original text (check extraction pattern)")
        if blueprint_section_count > 0:
            report["completeness"]["sections"] = 100  # Assume complete if we can't verify
    
    # Check references
    original_ref_count = _count_references_in_text(original_text)
    blueprint_refs = blueprint.get('document_structure', {}).get('references', [])
    blueprint_ref_count = len(blueprint_refs)
    
    report["metrics"]["original_references"] = original_ref_count
    report["metrics"]["blueprint_references"] = blueprint_ref_count
    if original_ref_count > 0:
        report["completeness"]["references"] = (blueprint_ref_count / original_ref_count * 100)
        if blueprint_ref_count < original_ref_count * 0.8:  # Less than 80%
            report["warnings"].append(f"Missing references: {original_ref_count} in original, {blueprint_ref_count} in blueprint")
    
    # Check for key elements
    structure = blueprint.get('document_structure', {})
    
    # Title page
    title_page = structure.get('title_page', {})
    if not title_page.get('title'):
        report["warnings"].append("Missing title in blueprint")
    
    # Problem & motivation (for reports, this might be "purpose" or "scope")
    problem = blueprint.get('problem_and_motivation', {})
    if not problem.get('problem') and not problem.get('why_it_matters'):
        report["warnings"].append("Missing problem statement or purpose in blueprint")
    
    # Check for findings/recommendations (important for reports)
    findings = blueprint.get('results', {})
    recommendations = blueprint.get('implications', {}).get('recommended_uses', [])
    report["metrics"]["recommendations_count"] = len(recommendations)
    if len(recommendations) == 0:
        report["warnings"].append("No recommendations found in blueprint")
    
    # Calculate overall quality score
    completeness_scores = [v for v in report["completeness"].values() if isinstance(v, (int, float))]
    if completeness_scores:
        # Cap scores at 100% (extra sections don't improve quality)
        capped_scores = [min(100, score) for score in completeness_scores]
        base_score = sum(capped_scores) / len(capped_scores)
    else:
        base_score = 100  # If no metrics, assume good
    
    # Penalize for warnings - each warning reduces score by 10%
    warning_penalty = min(len(report["warnings"]) * 10, 50)  # Max 50% penalty
    report["quality_score"] = max(0, base_score - warning_penalty)
    
    return report


def _check_business_plan_quality(blueprint: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """Check quality for business plan blueprints."""
    report = {
        "completeness": {},
        "warnings": [],
        "metrics": {},
        "quality_score": 0
    }
    
    # Extract sections from original document
    original_sections = _extract_sections_from_text(original_text)
    blueprint_sections = blueprint.get('document_structure', {}).get('sections', [])
    
    # Compare section counts
    original_section_count = len(original_sections)
    blueprint_section_count = len(blueprint_sections)
    
    report["metrics"]["original_sections"] = original_section_count
    report["metrics"]["blueprint_sections"] = blueprint_section_count
    
    # Only calculate completeness if we found sections
    if original_section_count > 0:
        report["completeness"]["sections"] = (blueprint_section_count / original_section_count * 100)
        
        # Check for missing sections
        original_titles = {_normalize_title(s['title']) for s in original_sections}
        blueprint_titles = {_normalize_title(s.get('title', '')) for s in blueprint_sections}
        
        missing_titles = original_titles - blueprint_titles
        if missing_titles:
            report["warnings"].append(f"Missing {len(missing_titles)} sections from blueprint: {list(missing_titles)[:5]}")
        
        # Check for extra sections in blueprint (might indicate duplicates)
        extra_titles = blueprint_titles - original_titles
        if extra_titles and len(extra_titles) > len(blueprint_titles) * 0.1:  # More than 10% extra
            report["warnings"].append(f"Extra sections in blueprint (possible duplicates): {len(extra_titles)}")
    else:
        # If we couldn't extract sections, still report counts
        report["warnings"].append("Could not extract sections from original text (check extraction pattern)")
        if blueprint_section_count > 0:
            report["completeness"]["sections"] = 100  # Assume complete if we can't verify
    
    # Check references
    original_ref_count = _count_references_in_text(original_text)
    blueprint_refs = blueprint.get('document_structure', {}).get('references', [])
    blueprint_ref_count = len(blueprint_refs)
    
    report["metrics"]["original_references"] = original_ref_count
    report["metrics"]["blueprint_references"] = blueprint_ref_count
    if original_ref_count > 0:
        report["completeness"]["references"] = (blueprint_ref_count / original_ref_count * 100)
        if blueprint_ref_count < original_ref_count * 0.8:  # Less than 80%
            report["warnings"].append(f"Missing references: {original_ref_count} in original, {blueprint_ref_count} in blueprint")
    
    # Check for key business plan elements
    structure = blueprint.get('document_structure', {})
    
    # Title page
    title_page = structure.get('title_page', {})
    if not title_page.get('title'):
        report["warnings"].append("Missing title in blueprint")
    
    # Executive summary
    exec_summary = blueprint.get('executive_summary', {})
    if not exec_summary.get('overview') or not exec_summary.get('mission'):
        report["warnings"].append("Missing executive summary overview or mission in blueprint")
    
    # Company description
    company = blueprint.get('company_description', {})
    if not company.get('company_name') or not company.get('legal_structure'):
        report["warnings"].append("Missing company name or legal structure in blueprint")
    
    # Financial projections (critical for business plans)
    financials = blueprint.get('financial_projections', {})
    projections = financials.get('projections', [])
    report["metrics"]["financial_projections_count"] = len(projections)
    if len(projections) == 0:
        report["warnings"].append("No financial projections found in blueprint")
    
    # Funding requirements (critical for business plans)
    funding = blueprint.get('funding_requirements', {})
    if not funding.get('amount_needed'):
        report["warnings"].append("Missing funding amount in blueprint")
    
    # Examples/case studies
    examples = blueprint.get('examples_and_case_studies', [])
    report["metrics"]["examples_count"] = len(examples)
    
    # Calculate overall quality score
    completeness_scores = [v for v in report["completeness"].values() if isinstance(v, (int, float))]
    if completeness_scores:
        # Cap scores at 100% (extra sections don't improve quality)
        capped_scores = [min(100, score) for score in completeness_scores]
        base_score = sum(capped_scores) / len(capped_scores)
    else:
        base_score = 100  # If no metrics, assume good
    
    # Penalize for warnings - each warning reduces score by 10%
    warning_penalty = min(len(report["warnings"]) * 10, 50)  # Max 50% penalty
    report["quality_score"] = max(0, base_score - warning_penalty)
    
    return report


def _check_narrative_fiction_quality(blueprint: Dict[str, Any], original_text: str) -> Dict[str, Any]:
    """Check quality for narrative fiction blueprints."""
    report = {
        "completeness": {},
        "warnings": [],
        "metrics": {},
        "quality_score": 0
    }
    
    # Extract sections/chapters from original document (narrative fiction specific)
    original_sections = _extract_narrative_fiction_sections(original_text)
    blueprint_sections = blueprint.get('document_structure', {}).get('sections', [])
    
    # Compare section counts
    original_section_count = len(original_sections)
    blueprint_section_count = len(blueprint_sections)
    
    report["metrics"]["original_sections"] = original_section_count
    report["metrics"]["blueprint_sections"] = blueprint_section_count
    
    # Only calculate completeness if we found sections
    if original_section_count > 0:
        report["completeness"]["sections"] = (blueprint_section_count / original_section_count * 100)
        
        # Check for missing sections
        original_titles = {_normalize_title(s['title']) for s in original_sections}
        blueprint_titles = {_normalize_title(s.get('title', '')) for s in blueprint_sections}
        
        missing_titles = original_titles - blueprint_titles
        if missing_titles:
            report["warnings"].append(f"Missing {len(missing_titles)} sections from blueprint: {list(missing_titles)[:5]}")
        
        # Check for extra sections in blueprint (might indicate duplicates)
        extra_titles = blueprint_titles - original_titles
        if extra_titles and len(extra_titles) > len(blueprint_titles) * 0.1:  # More than 10% extra
            report["warnings"].append(f"Extra sections in blueprint (possible duplicates): {len(extra_titles)}")
    else:
        # If we couldn't extract sections, still report counts
        report["warnings"].append("Could not extract sections from original text (check extraction pattern)")
        if blueprint_section_count > 0:
            report["completeness"]["sections"] = 100  # Assume complete if we can't verify
    
    # Check story overview
    story_overview = blueprint.get('story_overview', {})
    if not story_overview.get('title'):
        report["warnings"].append("Missing title in blueprint")
    if not story_overview.get('summary'):
        report["warnings"].append("Missing story summary in blueprint")
    
    # Check characters
    characters = blueprint.get('characters', [])
    report["metrics"]["characters_count"] = len(characters)
    if len(characters) == 0:
        report["warnings"].append("No characters found in blueprint")
    
    # Check plot structure
    plot_structure = blueprint.get('plot_structure', {})
    acts_or_chapters = plot_structure.get('acts_or_chapters', [])
    report["metrics"]["acts_or_chapters_count"] = len(acts_or_chapters)
    if len(acts_or_chapters) == 0:
        report["warnings"].append("No acts or chapters found in plot structure")
    
    # Check scenes
    scenes = blueprint.get('scenes', [])
    report["metrics"]["scenes_count"] = len(scenes)
    if len(scenes) == 0:
        report["warnings"].append("No scenes found in blueprint")
    
    # Check quotes and dialogue
    quotes = blueprint.get('quotes_and_dialogue', [])
    report["metrics"]["quotes_count"] = len(quotes)
    if len(quotes) == 0:
        report["warnings"].append("No quotes or dialogue found in blueprint")
    
    # Check setting
    setting = blueprint.get('setting', {})
    if not setting.get('primary_setting'):
        report["warnings"].append("Missing primary setting in blueprint")
    
    # Check themes
    themes = blueprint.get('themes', {})
    primary_themes = themes.get('primary_themes', [])
    report["metrics"]["primary_themes_count"] = len(primary_themes)
    if len(primary_themes) == 0:
        report["warnings"].append("No primary themes found in blueprint")
    
    # Calculate overall quality score
    completeness_scores = [v for v in report["completeness"].values() if isinstance(v, (int, float))]
    if completeness_scores:
        # Cap scores at 100% (extra sections don't improve quality)
        capped_scores = [min(100, score) for score in completeness_scores]
        base_score = sum(capped_scores) / len(capped_scores)
    else:
        base_score = 100  # If no metrics, assume good
    
    # Penalize for warnings - each warning reduces score by 10%
    warning_penalty = min(len(report["warnings"]) * 10, 50)  # Max 50% penalty
    report["quality_score"] = max(0, base_score - warning_penalty)
    
    return report


def _extract_narrative_fiction_sections(text: str) -> List[Dict[str, str]]:
    """Extract section/chapter headings from narrative fiction text."""
    sections = []
    seen = set()
    
    # Pattern 1: All-caps titles (e.g., "THE PHILOSOPHER'S JOKE")
    # Must be all caps, on its own line, followed by blank line or content
    all_caps_pattern = r'^([A-Z][A-Z\s\']{3,50})$'
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # Check for all-caps title
        if re.match(all_caps_pattern, line_stripped):
            # Must be followed by blank line or content (not another all-caps)
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                # Skip if next line is also all-caps (likely not a section break)
                if next_line and not re.match(all_caps_pattern, next_line):
                    # This looks like a section title
                    title = line_stripped
                    # Filter out common false positives
                    if title in ['THE PROJECT GUTENBERG', 'START OF THE PROJECT', 'END OF THE PROJECT', 
                                 'COPYRIGHT', 'PUBLISHED', 'CREDITS', 'LANGUAGE', 'RELEASE DATE']:
                        continue
                    if len(title) < 5 or len(title) > 100:
                        continue
                    # Skip if it looks like a copyright notice
                    if 'copyright' in title.lower() or 'gutenberg' in title.lower():
                        continue
                    
                    sig = f"title.{_normalize_title(title)}"
                    if sig not in seen:
                        seen.add(sig)
                        sections.append({
                            'number': str(len(sections) + 1),
                            'title': title
                        })
    
    # Pattern 2: Asterisk breaks (***) followed by title
    asterisk_pattern = r'^\*{3,}\s*\n\s*([A-Z][^\n]{5,80})$'
    matches = re.finditer(asterisk_pattern, text, re.MULTILINE)
    for match in matches:
        title = match.group(1).strip()
        if len(title) < 5 or len(title) > 100:
            continue
        sig = f"asterisk.{_normalize_title(title)}"
        if sig not in seen:
            seen.add(sig)
            sections.append({
                'number': str(len(sections) + 1),
                'title': title
            })
    
    # Pattern 3: Numbered sections (fallback to original pattern)
    numbered_sections = _extract_sections_from_text(text)
    for section in numbered_sections:
        sig = f"numbered.{_normalize_title(section['title'])}"
        if sig not in seen:
            seen.add(sig)
            sections.append(section)
    
    # Sort by order found in text
    return sections


def _extract_sections_from_text(text: str) -> List[Dict[str, str]]:
    """Extract section headings from original text."""
    sections = []
    
    # Pattern for numbered sections: "1. Title" or "1. Title 2" (with page numbers)
    # Must start with capital letter (actual section headings)
    pattern = r'^(\d+)\.\s+([A-Z][^\n]+?)(?:\s+\d+)?$'
    
    seen = set()  # Avoid duplicates
    matches = re.finditer(pattern, text, re.MULTILINE)
    
    for match in matches:
        number = match.group(1)
        title = match.group(2).strip()
        # Remove page numbers if present
        title = re.sub(r'\s+\d+$', '', title).strip()
        
        # Filter out false positives:
        # - References (usually have author names, years, etc.)
        # - Very short titles (likely not sections)
        # - Titles that look like citations
        # - Sentences (section headings are usually short, not full sentences)
        if len(title) < 5:
            continue
        if re.search(r'^\w+\.\s+\w+', title):  # Looks like "Author. Title" (citation)
            continue
        if re.search(r'\d{4}', title):  # Has year (likely citation)
            continue
        # Section headings are usually 2-8 words, not full sentences
        # Filter out very long titles (likely sentences)
        word_count = len(title.split())
        if word_count > 12:  # Too long for a section heading
            continue
        # Filter out sentences that start with "The" and are too long
        if title.startswith('The ') and word_count > 8:
            continue
        
        # Create signature to avoid duplicates
        sig = f"{number}.{_normalize_title(title)}"
        if sig not in seen:
            seen.add(sig)
            sections.append({
                'number': number,
                'title': title
            })
    
    # Sort by section number and filter to main sections (1-20 typically)
    sections.sort(key=lambda x: int(x['number']) if x['number'].isdigit() else 999)
    # Only keep sections numbered 1-20 (main document sections, not references)
    sections = [s for s in sections if s['number'].isdigit() and 1 <= int(s['number']) <= 20]
    
    return sections


def _normalize_title(title: str) -> str:
    """Normalize section title for comparison."""
    import unicodedata
    normalized = unicodedata.normalize('NFKD', title.lower())
    normalized = ''.join(c for c in normalized if not unicodedata.combining(c))
    normalized = ' '.join(normalized.split())
    # Remove numbering prefix
    normalized = re.sub(r'^\d+\.\s*', '', normalized)
    return normalized


def _count_references_in_text(text: str) -> int:
    """Count references in original text."""
    # Look for references section
    ref_pattern = r'(?:^|\n)\s*(?:References?|Bibliography|Works\s+Cited)\s*(?:\n|$)'
    ref_match = re.search(ref_pattern, text, re.IGNORECASE | re.MULTILINE)
    
    if not ref_match:
        return 0
    
    # Count numbered references after the heading
    ref_section = text[ref_match.end():]
    # Look for numbered references: "1. ", "2. ", etc. or "[1]", "[2]", etc.
    numbered_refs = len(re.findall(r'^\s*\d+[\.\)]\s+', ref_section, re.MULTILINE))
    bracket_refs = len(re.findall(r'\[\d+\]', ref_section))
    
    return max(numbered_refs, bracket_refs // 2)  # Use the higher count


def print_quality_report(report: Dict[str, Any]) -> None:
    """Print a human-readable quality report."""
    print("\n" + "=" * 60)
    print("Blueprint Quality Check")
    print("=" * 60)
    
    print(f"\nQuality Score: {report.get('quality_score', 0):.1f}%")
    
    if report.get('completeness'):
        print("\nCompleteness:")
        for key, value in report['completeness'].items():
            print(f"  {key.capitalize()}: {value:.1f}%")
    
    if report.get('metrics'):
        print("\nMetrics:")
        for key, value in report['metrics'].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
    
    if report.get('warnings'):
        print(f"\n⚠️  Warnings ({len(report['warnings'])}):")
        for warning in report['warnings']:
            print(f"  - {warning}")
    else:
        print("\n✅ No warnings - blueprint looks complete!")
    
    print("=" * 60)

