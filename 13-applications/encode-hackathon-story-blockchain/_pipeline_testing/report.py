#!/usr/bin/env python3
"""
Standalone similarity report script.
Compares an original document with a reinflated document and generates a similarity report.
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

from config import OUTPUT_DIR
from file_handlers import extract_text_from_file
from similarity import compare_similarity


def main():
    """Main report generation workflow."""
    parser = argparse.ArgumentParser(
        description="Generate similarity report comparing original and reinflated documents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python report.py original.pdf reinflated.md
  python report.py -o output_dir original.txt reinflated.md
  python report.py --output-dir custom_output original.docx reinflated.md
        """
    )
    parser.add_argument(
        "original_file",
        type=str,
        help="Path to original document (PDF, TXT, DOCX, EPUB)"
    )
    parser.add_argument(
        "reinflated_file",
        type=str,
        help="Path to reinflated document (usually .md)"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default=None,
        help="Output directory for report (default: same directory as reinflated file, or OUTPUT_DIR)"
    )
    
    args = parser.parse_args()
    
    # Load original file
    original_path = Path(args.original_file)
    if not original_path.exists():
        print(f"\n[ERROR] Original file not found: {original_path}")
        sys.exit(1)
    
    # Load reinflated file
    reinflated_path = Path(args.reinflated_file)
    if not reinflated_path.exists():
        print(f"\n[ERROR] Reinflated file not found: {reinflated_path}")
        sys.exit(1)
    
    print("=" * 60)
    print("Generating Similarity Report")
    print("=" * 60)
    
    print(f"\n[INFO] Loading original document: {original_path.name}")
    try:
        original_text = extract_text_from_file(original_path)
        print(f"  [OK] Extracted {len(original_text)} characters")
    except Exception as e:
        print(f"  [ERROR] Failed to extract text: {e}")
        sys.exit(1)
    
    print(f"\n[INFO] Loading reinflated document: {reinflated_path.name}")
    try:
        with open(reinflated_path, "r", encoding="utf-8") as f:
            reinflated_text = f.read()
        print(f"  [OK] Loaded {len(reinflated_text)} characters")
    except Exception as e:
        print(f"  [ERROR] Failed to load reinflated file: {e}")
        sys.exit(1)
    
    # Determine output directory
    if args.output_dir:
        run_output_dir = Path(args.output_dir)
    else:
        # Use same directory as reinflated file, or OUTPUT_DIR
        run_output_dir = reinflated_path.parent
        if not run_output_dir.exists():
            run_output_dir = OUTPUT_DIR
    
    run_output_dir.mkdir(exist_ok=True)
    
    # Create run timestamp
    run_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    print(f"\n[INFO] Output directory: {run_output_dir}")
    print(f"  Run timestamp: {run_timestamp}")
    
    # Generate similarity report
    try:
        report_path = compare_similarity(
            original_text,
            reinflated_text,
            run_timestamp,
            run_output_dir
        )
        
        print("\n" + "=" * 60)
        print("Report Generation Complete")
        print("=" * 60)
        print(f"\n[OK] Similarity report saved to: {report_path}")
        print(f"  - Original: {original_path.name}")
        print(f"  - Reinflated: {reinflated_path.name}")
        print(f"  - Report: {report_path.name}")
        
    except Exception as e:
        print(f"\n[ERROR] Report generation failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

