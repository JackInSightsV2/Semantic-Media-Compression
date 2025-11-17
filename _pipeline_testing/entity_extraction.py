"""
Entity extraction module using lightweight ML models for preprocessing.
Extracts entities before LLM passes to reduce cost and improve accuracy.
Generalized to handle multiple document types: research papers, business plans, fiction, etc.
"""

import re
from typing import Dict, List, Optional, Tuple
from pathlib import Path


def extract_references_section(text: str) -> str:
    """
    Extract the references/bibliography section from document text.
    
    Args:
        text: Full document text
        
    Returns:
        References section text, or empty string if not found
    """
    # Common patterns for references section
    patterns = [
        r'(?i)(?:^|\n)(?:references|bibliography|works\s+cited|literature\s+cited)(?:\s*:)?\s*\n',
        r'(?i)(?:^|\n)(?:references|bibliography)\s*\n',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            # Extract from match to end of document
            start = match.end()
            return text[start:].strip()
    
    # Fallback: look for numbered citations at end
    # Pattern: lines starting with numbers or brackets
    lines = text.split('\n')
    ref_start = None
    for i, line in enumerate(lines):
        if re.match(r'^\s*(\[\d+\]|\d+\.|\([A-Z]+\d+\))\s+', line):
            ref_start = i
            break
    
    if ref_start:
        return '\n'.join(lines[ref_start:])
    
    return ""


def extract_citation_patterns(text: str) -> List[Dict[str, str]]:
    """
    Extract citation patterns using regex.
    Handles common citation formats: APA, IEEE, MLA, Chicago, etc.
    
    Args:
        text: References section text
        
    Returns:
        List of citation dictionaries with raw text
    """
    citations = []
    
    # Pattern 1: Numbered citations [1], [2], etc.
    pattern1 = r'\[\s*(\d+)\s*\]\s+(.+?)(?=\n\s*\[\s*\d+\s*\]|$)'
    matches = re.finditer(pattern1, text, re.MULTILINE | re.DOTALL)
    for match in matches:
        citations.append({
            'id': match.group(1),
            'raw_text': match.group(2).strip()
        })
    
    # Pattern 2: Numbered citations 1., 2., etc.
    if not citations:
        pattern2 = r'^\s*(\d+)\.\s+(.+?)(?=\n\s*\d+\.|$)'
        matches = re.finditer(pattern2, text, re.MULTILINE | re.DOTALL)
        for match in matches:
            citations.append({
                'id': match.group(1),
                'raw_text': match.group(2).strip()
            })
    
    # Pattern 3: Author-year citations (Author, Year) or Author (Year)
    if not citations:
        pattern3 = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*[,\s]+(\d{4})[^.]*\.\s*(.+?)(?=\n[A-Z]|$)'
        matches = re.finditer(pattern3, text, re.MULTILINE)
        for i, match in enumerate(matches, 1):
            citations.append({
                'id': str(i),
                'raw_text': match.group(0).strip()
            })
    
    return citations


def extract_entities_simple(text: str) -> Dict[str, List[str]]:
    """
    Extract entities using simple regex patterns (no external dependencies).
    Lightweight alternative to full NER models.
    
    Args:
        text: Text to extract entities from
        
    Returns:
        Dictionary with entity types and lists of extracted entities
    """
    entities = {
        'potential_authors': [],
        'potential_years': [],
        'potential_venues': [],
        'potential_locations': []
    }
    
    # Extract years (4-digit years, typically 1900-2099)
    year_pattern = r'\b(19\d{2}|20\d{2})\b'
    full_years = re.findall(year_pattern, text)
    entities['potential_years'] = list(set(full_years))
    
    # Extract potential author names (Capitalized words, often at start of lines)
    # Pattern: "Last, First" or "First Last" at start of citation
    author_patterns = [
        r'^([A-Z][a-z]+(?:\s+[A-Z]\.?\s*)?[A-Z][a-z]+)',  # First Last or First M. Last
        r'([A-Z][a-z]+,\s+[A-Z][a-z]+(?:\s+[A-Z]\.?)?)',  # Last, First
    ]
    authors = set()
    for pattern in author_patterns:
        matches = re.findall(pattern, text, re.MULTILINE)
        for match in matches:
            if isinstance(match, tuple):
                authors.add(' '.join(match))
            else:
                authors.add(match)
    entities['potential_authors'] = list(authors)[:50]  # Limit to 50
    
    # Extract potential venues (common journal/conference patterns)
    venue_keywords = ['Journal', 'Conference', 'Proceedings', 'Review', 'Transactions', 
                     'Workshop', 'Symposium', 'Magazine', 'Letters', 'Bulletin']
    venues = []
    for keyword in venue_keywords:
        pattern = rf'\b{keyword}\s+[A-Z][A-Za-z\s]+'
        matches = re.findall(pattern, text)
        venues.extend(matches)
    entities['potential_venues'] = list(set(venues))[:30]  # Limit to 30
    
    # Extract potential locations (common patterns)
    location_patterns = [
        r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s+([A-Z]{2})\b',  # City, State
        r'\b([A-Z][a-z]+)\s+University\b',  # University names
    ]
    locations = []
    for pattern in location_patterns:
        matches = re.findall(pattern, text)
        locations.extend([m if isinstance(m, str) else ' '.join(m) for m in matches])
    entities['potential_locations'] = list(set(locations))[:20]  # Limit to 20
    
    return entities


def extract_entities_general(text: str, focus: str = "general") -> Dict[str, List[str]]:
    """
    Extract general entities from any document type.
    
    Args:
        text: Document text
        focus: Focus area - "citations", "entities", "general", "none"
        
    Returns:
        Dictionary with extracted entities
    """
    entities = {
        'potential_authors': [],
        'potential_years': [],
        'potential_venues': [],
        'potential_locations': [],
        'potential_organizations': [],
        'potential_people': [],
        'potential_dates': [],
        'potential_titles': []  # For narrative fiction
    }
    
    # Always extract years and dates
    year_pattern = r'\b(19\d{2}|20\d{2})\b'
    full_years = re.findall(year_pattern, text)
    entities['potential_years'] = list(set(full_years))
    
    # Extract dates (various formats)
    date_patterns = [
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
    ]
    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, text, re.IGNORECASE))
    entities['potential_dates'] = list(set(dates))
    
    if focus in ["citations", "entities", "general"]:
        # Extract potential person names (capitalized words, often proper nouns)
        # Pattern: "First Last" or "Last, First"
        person_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z]\.?\s*)?[A-Z][a-z]+)\b',  # First Last or First M. Last
            r'\b([A-Z][a-z]+,\s+[A-Z][a-z]+(?:\s+[A-Z]\.?)?)\b',  # Last, First
        ]
        people = set()
        for pattern in person_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if isinstance(match, tuple):
                    people.add(' '.join(match))
                else:
                    people.add(match)
        entities['potential_people'] = list(people)[:50]
        entities['potential_authors'] = list(people)[:50]  # Authors are a subset of people
    
    if focus in ["citations", "entities"]:
        # Extract organizations (common patterns)
        org_patterns = [
            r'\b([A-Z][A-Za-z\s&]+(?:Inc\.|LLC|Corp\.|Ltd\.|Company|Corporation))\b',
            r'\b([A-Z][A-Za-z\s]+(?:University|College|Institute|School|Hospital))\b',
            r'\b([A-Z][A-Za-z\s]+(?:Journal|Review|Transactions|Proceedings|Conference))\b',
        ]
        orgs = set()
        for pattern in org_patterns:
            matches = re.findall(pattern, text)
            orgs.update(matches)
        entities['potential_organizations'] = list(orgs)[:30]
        
        # Extract venues (for citations)
        venue_keywords = ['Journal', 'Conference', 'Proceedings', 'Review', 'Transactions', 
                         'Workshop', 'Symposium', 'Magazine', 'Letters', 'Bulletin']
        venues = []
        for keyword in venue_keywords:
            pattern = rf'\b{keyword}\s+[A-Z][A-Za-z\s]+'
            matches = re.findall(pattern, text)
            venues.extend(matches)
        entities['potential_venues'] = list(set(venues))[:30]
    
    if focus in ["citations"]:
        # Extract locations (for citations - cities, countries)
        location_patterns = [
            r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*),\s+([A-Z]{2})\b',  # City, State
            r'\b([A-Z][a-z]+)\s+University\b',  # University names
        ]
        locations = []
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            locations.extend([m if isinstance(m, str) else ' '.join(m) for m in matches])
        entities['potential_locations'] = list(set(locations))[:20]
    
    # Extract titles for narrative fiction (focus="general")
    if focus == "general":
        # Look for titles in common patterns:
        # 1. Lines that are all caps or title case at the start of document
        # 2. Lines with quotes around them (e.g., "The Philosopher's Joke")
        # 3. Lines after "Title:" or "Title Page"
        # 4. Standalone lines with title case (often titles)
        title_patterns = [
            r'^"([^"]{5,100})"$',  # Quoted titles on their own line
            r'^([A-Z][A-Za-z\s\']{5,100})$',  # Title case on its own line (start of doc)
            r'(?:^Title[:\s]+)([A-Z][A-Za-z\s\']{5,100})$',  # After "Title:"
            r'(?:^The\s+)([A-Z][a-z]+(?:\'s)?\s+[A-Z][a-z]+)',  # "The [Title]"
        ]
        titles = set()
        lines = text.split('\n')[:50]  # Check first 50 lines for titles
        for i, line in enumerate(lines):
            line = line.strip()
            if not line or len(line) < 5:
                continue
            for pattern in title_patterns:
                matches = re.findall(pattern, line, re.MULTILINE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = ' '.join(match)
                    # Filter out common false positives
                    if match and not any(word in match.lower() for word in ['copyright', 'project gutenberg', 'ebook', 'license']):
                        titles.add(match)
        entities['potential_titles'] = list(titles)[:10]  # Limit to 10
    
    return entities


def extract_citation_entities(text: str, focus: str = "citations") -> Dict[str, any]:
    """
    Main function: Extract citation-related entities from document.
    Uses lightweight regex-based extraction (no external ML dependencies).
    Generalized to handle multiple document types.
    
    Args:
        text: Full document text
        focus: Focus area - "citations", "entities", "general", "none"
        
    Returns:
        Dictionary with:
        - citations: List of raw citation texts with IDs
        - entities: Dictionary of potential authors, years, venues, locations
        - citation_count: Number of citations found
    """
    if focus == "none":
        return {
            'citations': [],
            'entities': {},
            'citation_count': 0
        }
    
    # Extract references section (for citations focus)
    citations = []
    if focus == "citations":
        ref_section = extract_references_section(text)
        if ref_section:
            citations = extract_citation_patterns(ref_section)
            # Extract entities from references section
            entities = extract_entities_simple(ref_section)
        else:
            entities = extract_entities_general(text, focus="citations")
    else:
        # For non-citation focus, extract general entities from full text
        entities = extract_entities_general(text, focus=focus)
    
    return {
        'citations': citations,
        'entities': entities,
        'citation_count': len(citations)
    }


def format_ner_hints_for_prompt(ner_results: Dict[str, any], focus: str = "citations") -> str:
    """
    Format NER results as hints for LLM prompt.
    Generalized to handle different document types.
    
    Args:
        ner_results: Output from extract_citation_entities() or extract_entities_general()
        focus: Focus area - "citations", "entities", "general"
        
    Returns:
        Formatted string to include in prompt
    """
    if not ner_results:
        return "No pre-extracted entity hints available."
    
    hints = ["PRE-EXTRACTION HINTS (use as guidance, validate and structure):"]
    
    if focus == "citations":
        citation_count = ner_results.get('citation_count', 0)
        if citation_count > 0:
            hints.append(f"\nFound {citation_count} potential citations.")
        
        entities = ner_results.get('entities', {})
        
        if entities.get('potential_authors'):
            hints.append(f"\nPotential Authors ({len(entities['potential_authors'][:10])}):")
            hints.append(", ".join(entities['potential_authors'][:10]))
            if len(entities['potential_authors']) > 10:
                hints.append(f" (and {len(entities['potential_authors']) - 10} more)")
        
        if entities.get('potential_years'):
            hints.append(f"\nPotential Years ({len(entities['potential_years'])}):")
            hints.append(", ".join(sorted(entities['potential_years'], reverse=True)[:20]))
        
        if entities.get('potential_venues'):
            hints.append(f"\nPotential Venues ({len(entities['potential_venues'][:10])}):")
            hints.append(", ".join(entities['potential_venues'][:10]))
        
        if ner_results.get('citations'):
            hints.append(f"\n\nSample Citation Patterns (first 3):")
            for i, cit in enumerate(ner_results['citations'][:3], 1):
                hints.append(f"\n[{cit.get('id', i)}] {cit.get('raw_text', '')[:100]}...")
    
    elif focus in ["entities", "general"]:
        entities = ner_results.get('entities', {})
        
        if entities.get('potential_people'):
            hints.append(f"\nPotential People/Names ({len(entities['potential_people'][:15])}):")
            hints.append(", ".join(entities['potential_people'][:15]))
        
        if entities.get('potential_organizations'):
            hints.append(f"\nPotential Organizations ({len(entities['potential_organizations'][:10])}):")
            hints.append(", ".join(entities['potential_organizations'][:10]))
        
        if entities.get('potential_years'):
            hints.append(f"\nPotential Years ({len(entities['potential_years'])}):")
            hints.append(", ".join(sorted(entities['potential_years'], reverse=True)[:15]))
        
        if entities.get('potential_dates'):
            hints.append(f"\nPotential Dates ({len(entities['potential_dates'][:10])}):")
            hints.append(", ".join(entities['potential_dates'][:10]))
        
        if entities.get('potential_locations'):
            hints.append(f"\nPotential Locations ({len(entities['potential_locations'][:10])}):")
            hints.append(", ".join(entities['potential_locations'][:10]))
        
        # Add titles for narrative fiction
        if entities.get('potential_titles'):
            hints.append(f"\n\nPotential Titles ({len(entities['potential_titles'])}):")
            for title in entities['potential_titles']:
                hints.append(f"  - \"{title}\"")
            hints.append("\n⚠️ IMPORTANT: Verify the title matches the document EXACTLY. Use the exact title as it appears in the document, not these suggestions.")
    
    if len(hints) == 1:  # Only header was added
        return "No pre-extracted entity hints available."
    
    return "\n".join(hints)

