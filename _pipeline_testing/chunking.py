"""Text chunking utilities for handling long documents."""

from typing import List, Tuple
import re


def chunk_text_by_sections(text: str, max_chunk_size: int = 100000, overlap: int = 1000) -> List[Tuple[str, int, int]]:
    """
    Chunk text intelligently by trying to break at section boundaries.
    
    Args:
        text: Full text to chunk
        max_chunk_size: Maximum characters per chunk
        overlap: Characters to overlap between chunks for context
    
    Returns:
        List of tuples: (chunk_text, start_index, end_index)
    """
    if len(text) <= max_chunk_size:
        return [(text, 0, len(text))]
    
    chunks = []
    current_pos = 0
    text_length = len(text)
    
    # Try to find section boundaries (headings, chapter markers, etc.)
    section_patterns = [
        r'\n#{1,6}\s+',  # Markdown headings
        r'\n\s*Chapter\s+\d+',  # Chapter markers
        r'\n\s*[IVX]+\.\s+',  # Roman numerals
        r'\n\s*\d+\.\s+[A-Z]',  # Numbered sections
        r'\n\n\n+',  # Multiple newlines (section breaks)
    ]
    
    while current_pos < text_length:
        end_pos = min(current_pos + max_chunk_size, text_length)
        
        # If not at the end, try to find a good break point
        if end_pos < text_length:
            # Look for section boundaries in the last 20% of the chunk
            search_start = max(current_pos, end_pos - int(max_chunk_size * 0.2))
            best_break = end_pos
            
            for pattern in section_patterns:
                matches = list(re.finditer(pattern, text[search_start:end_pos], re.IGNORECASE))
                if matches:
                    # Use the last match before the end
                    match = matches[-1]
                    best_break = search_start + match.end()
                    break
            
            # If we found a good break, use it
            if best_break > current_pos + max_chunk_size * 0.5:  # Don't make chunks too small
                end_pos = best_break
        
        chunk_text = text[current_pos:end_pos]
        chunks.append((chunk_text, current_pos, end_pos))
        
        # Move to next chunk with overlap
        # Ensure we make progress - move forward by at least 10% of chunk size
        min_progress = max_chunk_size // 10
        current_pos = max(current_pos + min_progress, end_pos - overlap)
        
        # Safety check: if we're not making progress, force a larger jump
        if current_pos <= chunks[-1][1] if chunks else 0:
            current_pos = end_pos - overlap
    
    return chunks


def chunk_text_simple(text: str, max_chunk_size: int = 100000, overlap: int = 1000) -> List[Tuple[str, int, int]]:
    """
    Simple chunking by character count with overlap.
    
    Args:
        text: Full text to chunk
        max_chunk_size: Maximum characters per chunk
        overlap: Characters to overlap between chunks
    
    Returns:
        List of tuples: (chunk_text, start_index, end_index)
    """
    if len(text) <= max_chunk_size:
        return [(text, 0, len(text))]
    
    chunks = []
    current_pos = 0
    text_length = len(text)
    
    while current_pos < text_length:
        end_pos = min(current_pos + max_chunk_size, text_length)
        chunk_text = text[current_pos:end_pos]
        chunks.append((chunk_text, current_pos, end_pos))
        current_pos = end_pos - overlap
    
    return chunks


def get_chunking_strategy(text: str, max_chunk_size: int = 100000) -> str:
    """
    Determine best chunking strategy based on text characteristics.
    
    Returns:
        'none' if text is short enough
        'sections' if text has clear section markers
        'simple' for plain text chunking
    """
    if len(text) <= max_chunk_size:
        return 'none'
    
    # Check for section markers
    section_markers = [
        r'#{1,6}\s+',  # Markdown headings
        r'Chapter\s+\d+',
        r'[IVX]+\.\s+',
    ]
    
    for pattern in section_markers:
        if re.search(pattern, text, re.IGNORECASE):
            return 'sections'
    
    return 'simple'

