#!/usr/bin/env python3
"""
Analyze files in the data folder and categorize them for schema/prompt generation.
"""

import os
import re
from pathlib import Path
import PyPDF2
from typing import Dict, List, Tuple

def extract_pdf_text(pdf_path: str, max_pages: int = 3) -> str:
    """Extract text from first few pages of PDF."""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for i, page in enumerate(reader.pages[:max_pages]):
                try:
                    text += page.extract_text() + "\n"
                except:
                    pass
            return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def categorize_file(filename: str, content_sample: str) -> str:
    """Categorize a file based on filename and content."""
    filename_lower = filename.lower()
    content_lower = content_sample.lower()
    
    # Check filename patterns first
    if re.match(r'\d{4}\.\d{5}v\d+\.pdf', filename):
        return "research_paper"
    
    # Check content patterns - prioritize more specific categories first
    
    # Research papers - check first as they're common and have specific patterns
    research_keywords = ['abstract', 'introduction', 'methodology', 'results', 'conclusion', 'references', 
                         'related work', 'background', 'experimental setup', 'evaluation', 'discussion']
    research_count = sum(1 for keyword in research_keywords if keyword in content_lower)
    if research_count >= 3:  # Need multiple research paper indicators
        return "research_paper"
    
    # Business plans - specific business terms
    if any(keyword in content_lower for keyword in ['business plan', 'executive summary', 'market analysis', 
                                                     'financial projections', 'revenue model', 'go-to-market']):
        return "business_plan"
    
    # Technical documentation - API/technical terms
    if any(keyword in content_lower for keyword in ['api endpoint', 'request/response', 'authentication', 
                                                     'technical documentation', 'api documentation', 'endpoint']):
        return "technical_documentation"
    
    # Reports - policy/report specific terms
    if any(keyword in content_lower for keyword in ['policy report', 'submission', 'recommendation', 
                                                     'findings and recommendations', 'executive report']):
        return "report"
    
    # Narrative fiction - more specific fiction indicators (check last to avoid false positives)
    # Need multiple fiction indicators to avoid matching research papers that mention "character" or "plot"
    fiction_keywords = ['chapter one', 'chapter two', 'novel', 'fiction', 'protagonist', 'antagonist',
                        'narrative arc', 'story arc', 'the philosopher', 'dialogue', 'scene']
    fiction_count = sum(1 for keyword in fiction_keywords if keyword in content_lower)
    if fiction_count >= 2:  # Need multiple fiction indicators
        return "narrative_fiction"
    
    # If we found some research indicators but not enough, still default to research
    if research_count >= 1:
        return "research_paper"
    
    # Default fallback
    return "unknown"

def analyze_data_folder(data_folder: str = "data") -> Dict[str, List[Tuple[str, str]]]:
    """Analyze all files in data folder and categorize them."""
    data_path = Path(data_folder)
    categories = {}
    
    for file_path in sorted(data_path.iterdir()):
        if file_path.is_file():
            filename = file_path.name
            ext = file_path.suffix.lower()
            
            content_sample = ""
            if ext == '.pdf':
                content_sample = extract_pdf_text(str(file_path))
            elif ext == '.txt':
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content_sample = f.read(2000)
                except:
                    pass
            elif ext in ['.docx', '.epub']:
                content_sample = f"[{ext.upper()} file - content extraction not implemented]"
            
            category = categorize_file(filename, content_sample)
            
            if category not in categories:
                categories[category] = []
            categories[category].append((filename, content_sample[:200]))
    
    return categories

if __name__ == "__main__":
    categories = analyze_data_folder()
    
    print("=" * 80)
    print("FILE CATEGORIZATION RESULTS")
    print("=" * 80)
    print()
    
    for category, files in sorted(categories.items()):
        print(f"\n{category.upper().replace('_', ' ')} ({len(files)} files):")
        print("-" * 80)
        for filename, sample in files:
            print(f"  • {filename}")
            if sample and len(sample) > 50:
                print(f"    Preview: {sample[:100]}...")
        print()


