"""File I/O and text extraction utilities."""

import hashlib
from pathlib import Path
from typing import Optional
import PyPDF2


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extract text content from PDF file."""
    text_parts = []
    try:
        with open(pdf_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text_parts.append(page.extract_text())
        return "\n".join(text_parts)
    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {e}")


def extract_text_from_txt(txt_path: Path) -> str:
    """Extract text content from TXT file."""
    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            return f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        with open(txt_path, "r", encoding="latin-1") as f:
            return f.read()
    except Exception as e:
        raise ValueError(f"Failed to extract text from TXT: {e}")


def extract_text_from_file(file_path: Path) -> str:
    """Extract text from file based on extension."""
    ext = file_path.suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".txt":
        return extract_text_from_txt(file_path)
    elif ext == ".epub":
        raise ValueError(f"EPUB extraction not yet implemented. Please convert {file_path.name} to PDF or TXT.")
    elif ext == ".docx":
        raise ValueError(f"DOCX extraction not yet implemented. Please convert {file_path.name} to PDF or TXT.")
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def calculate_file_hash(file_path: Path, algorithm: str = "sha256") -> str:
    """Calculate hash of a file."""
    hash_obj = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_obj.update(chunk)
        return hash_obj.hexdigest()
    except Exception as e:
        raise ValueError(f"Failed to calculate hash: {e}")


def calculate_json_hash(data: dict, algorithm: str = "sha256") -> str:
    """Calculate hash of a JSON-serializable object."""
    import json
    # Serialize to JSON with sorted keys for deterministic hashing
    json_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
    hash_obj = hashlib.sha256()
    hash_obj.update(json_str.encode('utf-8'))
    return hash_obj.hexdigest()


