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
    
    # Check content patterns
    if any(keyword in content_lower for keyword in ['business plan', 'executive summary', 'market analysis', 'financial projections']):
        return "business_plan"
    
    if any(keyword in content_lower for keyword in ['api', 'endpoint', 'request', 'response', 'authentication', 'documentation']):
        return "technical_documentation"
    
    if any(keyword in content_lower for keyword in ['chapter', 'novel', 'story', 'character', 'plot', 'the philosopher']):
        return "narrative_fiction"
    
    if any(keyword in content_lower for keyword in ['submission', 'report', 'recommendation', 'findings', 'conclusion']):
        return "report"
    
    if any(keyword in content_lower for keyword in ['abstract', 'introduction', 'methodology', 'results', 'conclusion', 'references']):
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


