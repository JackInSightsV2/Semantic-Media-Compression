"""
GROBID client for citation parsing and bibliographic data extraction.
Modular integration that can be enabled/disabled per document type.
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any
from pathlib import Path


class GrobidClient:
    """
    Client for GROBID REST API.
    Handles citation parsing and bibliographic data extraction.
    """
    
    def __init__(self, base_url: str = "http://localhost:8070", timeout: int = 30):
        """
        Initialize GROBID client.
        
        Args:
            base_url: GROBID service URL (default: http://localhost:8070)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.is_available = False
        self._check_availability()
    
    def _check_availability(self) -> bool:
        """Check if GROBID service is available."""
        try:
            response = requests.get(f"{self.base_url}/api/isalive", timeout=5)
            self.is_available = response.status_code == 200
            return self.is_available
        except Exception:
            self.is_available = False
            return False
    
    def parse_citations(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse citations from text using GROBID.
        
        Args:
            text: Text containing citations
            
        Returns:
            List of parsed citation dictionaries
        """
        if not self.is_available:
            return []
        
        try:
            # GROBID citation parsing endpoint
            response = requests.post(
                f"{self.base_url}/api/processCitation",
                data={"citations": text},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                # Parse TEI XML response (simplified - would need proper XML parsing)
                # For now, return structured data
                return self._parse_grobid_response(response.text)
            else:
                return []
        except Exception as e:
            print(f"  [WARNING] GROBID citation parsing failed: {e}")
            return []
    
    def parse_references_section(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse references section from text.
        
        Args:
            text: References section text
            
        Returns:
            List of parsed reference dictionaries
        """
        if not self.is_available:
            return []
        
        try:
            # Extract references section
            ref_section = self._extract_references_section(text)
            if not ref_section:
                return []
            
            # Process each citation
            citations = []
            # Split by common citation separators
            citation_lines = ref_section.split('\n')
            current_citation = []
            
            for line in citation_lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if line looks like start of new citation
                if self._is_citation_start(line):
                    if current_citation:
                        citation_text = ' '.join(current_citation)
                        parsed = self.parse_citations(citation_text)
                        if parsed:
                            citations.extend(parsed)
                        current_citation = [line]
                    else:
                        current_citation = [line]
                else:
                    current_citation.append(line)
            
            # Process last citation
            if current_citation:
                citation_text = ' '.join(current_citation)
                parsed = self.parse_citations(citation_text)
                if parsed:
                    citations.extend(parsed)
            
            return citations
        except Exception as e:
            print(f"  [WARNING] GROBID references parsing failed: {e}")
            return []
    
    def _extract_references_section(self, text: str) -> str:
        """Extract references section from text."""
        import re
        patterns = [
            r'(?i)(?:^|\n)(?:references|bibliography|works\s+cited)(?:\s*:)?\s*\n',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return text[match.end():].strip()
        
        return ""
    
    def _is_citation_start(self, line: str) -> bool:
        """Check if line looks like start of a citation."""
        import re
        patterns = [
            r'^\s*(\[\d+\]|\d+\.|\([A-Z]+\d+\))',  # Numbered citations
            r'^[A-Z][a-z]+,\s+[A-Z]',  # Author, First format
            r'^[A-Z][a-z]+\s+\(?\d{4}\)?',  # Author (Year) format
        ]
        
        for pattern in patterns:
            if re.match(pattern, line):
                return True
        return False
    
    def _parse_grobid_response(self, xml_text: str) -> List[Dict[str, Any]]:
        """
        Parse GROBID TEI XML response.
        Simplified parser - full implementation would use proper XML parsing.
        
        Args:
            xml_text: GROBID TEI XML response
            
        Returns:
            List of citation dictionaries
        """
        # Simplified parsing - in production, use proper XML parser
        citations = []
        
        # Try to extract structured data from XML
        # This is a simplified version - full implementation would parse TEI XML properly
        import re
        
        # Extract author names
        authors_pattern = r'<author><persName[^>]*>(.*?)</persName></author>'
        authors = re.findall(authors_pattern, xml_text, re.DOTALL)
        
        # Extract title
        title_pattern = r'<title[^>]*>(.*?)</title>'
        titles = re.findall(title_pattern, xml_text, re.DOTALL)
        
        # Extract year
        year_pattern = r'<date[^>]*>(\d{4})</date>'
        years = re.findall(year_pattern, xml_text)
        
        # Extract venue/journal
        venue_pattern = r'<biblScope[^>]*unit="journal"[^>]*>(.*?)</biblScope>'
        venues = re.findall(venue_pattern, xml_text, re.DOTALL)
        
        # Build citation objects
        if authors or titles or years:
            citations.append({
                'authors': [a.strip() for a in authors] if authors else [],
                'title': titles[0].strip() if titles else None,
                'year': int(years[0]) if years else None,
                'venue': venues[0].strip() if venues else None,
                'source': 'grobid'
            })
        
        return citations
    
    def extract_bibliographic_data(self, pdf_path: Optional[Path] = None, text: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract bibliographic data from PDF or text.
        
        Args:
            pdf_path: Path to PDF file (preferred)
            text: Text content (fallback)
            
        Returns:
            Dictionary with bibliographic data
        """
        if not self.is_available:
            return {}
        
        if pdf_path and pdf_path.exists():
            try:
                # Process PDF file
                with open(pdf_path, 'rb') as f:
                    files = {'input': f}
                    data = {'generateIDs': '1', 'consolidateCitations': '1'}
                    response = requests.post(
                        f"{self.base_url}/api/processFulltextDocument",
                        files=files,
                        data=data,
                        timeout=self.timeout * 2  # PDF processing takes longer
                    )
                    
                    if response.status_code == 200:
                        # Parse TEI XML response (simplified)
                        return self._parse_grobid_response(response.text)
            except Exception as e:
                print(f"  [WARNING] GROBID PDF processing failed: {e}")
        
        return {}


def extract_citations_with_grobid(
    text: str,
    pdf_path: Optional[Path] = None,
    grobid_url: str = "http://localhost:8070"
) -> Dict[str, Any]:
    """
    Extract citations using GROBID.
    
    Args:
        text: Document text
        pdf_path: Optional PDF file path (better accuracy)
        grobid_url: GROBID service URL
        
    Returns:
        Dictionary with GROBID extraction results
    """
    client = GrobidClient(base_url=grobid_url)
    
    if not client.is_available:
        return {
            'citations': [],
            'entities': {},
            'citation_count': 0,
            'source': 'grobid',
            'available': False
        }
    
    # Try to parse references section
    citations = client.parse_references_section(text)
    
    # If PDF available, try full document processing
    bibliographic_data = {}
    if pdf_path:
        bibliographic_data = client.extract_bibliographic_data(pdf_path=pdf_path)
    
    return {
        'citations': citations,
        'entities': {
            'potential_authors': [c.get('authors', []) for c in citations if c.get('authors')],
            'potential_years': [str(c.get('year')) for c in citations if c.get('year')],
            'potential_venues': [c.get('venue') for c in citations if c.get('venue')],
        },
        'citation_count': len(citations),
        'source': 'grobid',
        'available': True,
        'bibliographic_data': bibliographic_data
    }

