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
        
        if category == "research_paper":
            report = _check_research_paper_quality(blueprint, original_text)
        else:
            # Default report for other categories
            report["quality_score"] = 100
        
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
    
    # Problem & motivation
    if not blueprint.get('problem_and_motivation', {}).get('problem'):
        report["warnings"].append("Missing problem statement in blueprint")
    
    # Calculate overall quality score
    completeness_scores = [v for v in report["completeness"].values() if isinstance(v, (int, float))]
    if completeness_scores:
        # Cap scores at 100% (extra sections don't improve quality)
        capped_scores = [min(100, score) for score in completeness_scores]
        report["quality_score"] = sum(capped_scores) / len(capped_scores)
    else:
        report["quality_score"] = 100  # If no metrics, assume good
    
    return report


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

