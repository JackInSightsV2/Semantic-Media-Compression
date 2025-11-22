"""File service for categorization and storage."""

import shutil
from pathlib import Path
from typing import Tuple, Optional
from datetime import datetime

from config import DATA_DIR, CATEGORY_MAP
from categorize_files import categorize_file, extract_pdf_text


class FileService:
    """Service for file categorization and storage."""
    
    def __init__(self):
        DATA_DIR.mkdir(exist_ok=True)
    
    def categorize_and_save_file(
        self,
        file_path: Path,
        filename: Optional[str] = None
    ) -> Tuple[str, Path, str]:
        """
        Categorize a file and save it to the appropriate data directory.
        
        Args:
            file_path: Path to the uploaded file
            filename: Optional custom filename (uses original if not provided)
        
        Returns:
            Tuple of (category, saved_file_path, category_folder)
        """
        if filename is None:
            filename = file_path.name
        
        # Extract sample content for categorization
        content_sample = ""
        if file_path.suffix.lower() == '.pdf':
            try:
                content_sample = extract_pdf_text(str(file_path), max_pages=3)
            except Exception:
                content_sample = ""
        elif file_path.suffix.lower() == '.txt':
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content_sample = f.read(2000)
            except Exception:
                content_sample = ""
        
        # Categorize the file
        category = categorize_file(filename, content_sample)
        
        # Map category to category_key and folder name
        category_mapping = {
            "research_paper": ("research", "research_papers"),
            "business_plan": ("business", "business_plans"),
            "narrative_fiction": ("fiction", "narrative_fiction"),
            "technical_documentation": ("technical", "technical_documentation"),
            "report": ("report", "reports"),
            "unknown": ("research", "research_papers")  # Default to research if unknown
        }
        
        category_key, category_folder = category_mapping.get(category, ("research", "research_papers"))
        
        # Create category directory
        category_dir = DATA_DIR / category_folder
        category_dir.mkdir(exist_ok=True)
        
        # Generate unique filename if file already exists
        dest_path = category_dir / filename
        if dest_path.exists():
            # Add timestamp to filename
            stem = dest_path.stem
            suffix = dest_path.suffix
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest_path = category_dir / f"{stem}_{timestamp}{suffix}"
        
        # Copy file to destination
        shutil.copy2(file_path, dest_path)
        
        return category_key, dest_path, category_folder

