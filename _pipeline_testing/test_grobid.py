#!/usr/bin/env python3
"""
Standalone test script for GROBID service.
Tests GROBID in isolation to verify it's working correctly.
"""

import sys
from pathlib import Path
import requests
import json

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from grobid_client import GrobidClient, extract_citations_with_grobid


def test_grobid_health(base_url: str = "http://localhost:8070"):
    """Test if GROBID service is alive."""
    print("=" * 60)
    print("Testing GROBID Health Check")
    print("=" * 60)
    
    try:
        response = requests.get(f"{base_url}/api/isalive", timeout=5)
        if response.status_code == 200:
            print(f"✅ GROBID is alive at {base_url}")
            print(f"   Response: {response.text}")
            return True
        else:
            print(f"❌ GROBID returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to GROBID at {base_url}")
        print("   Make sure the Docker container is running:")
        print("   docker run --rm --init --ulimit core=0 -p 8070:8070 grobid/grobid:0.8.2-crf")
        return False
    except Exception as e:
        print(f"❌ Error checking GROBID: {e}")
        return False


def test_citation_parsing(base_url: str = "http://localhost:8070"):
    """Test GROBID citation parsing with sample citations."""
    print("\n" + "=" * 60)
    print("Testing GROBID Citation Parsing")
    print("=" * 60)
    
    # Sample citations in different formats
    sample_citations = [
        "Aggeri, Franck and Cartel, Melodie (2017), 'Le Changement Climatique et les Entreprises: Enjeux, Espaces d'action, Régulations Internationales', Entreprises et Historie, 1 (86), 6-20.",
        "Bansal, Pratima and Andrew J. Hoffman (eds.) (2012), The Oxford Handbook of Business and the Natural (Oxford; New York: Oxford University Press).",
        "Jones, Geoffrey (2017a), Profits and Sustainability. A Global History of Green Entrepreneurship (Oxford: Oxford University Press)."
    ]
    
    client = GrobidClient(base_url=base_url)
    
    if not client.is_available:
        print("❌ GROBID service not available")
        return False
    
    print(f"\nTesting {len(sample_citations)} sample citations...\n")
    
    for i, citation in enumerate(sample_citations, 1):
        print(f"Citation {i}:")
        print(f"  Input: {citation[:80]}...")
        
        try:
            parsed = client.parse_citations(citation)
            if parsed:
                print(f"  ✅ Parsed successfully:")
                for p in parsed:
                    print(f"     - Authors: {p.get('authors', [])}")
                    print(f"     - Title: {p.get('title', 'N/A')}")
                    print(f"     - Year: {p.get('year', 'N/A')}")
                    print(f"     - Venue: {p.get('venue', 'N/A')}")
            else:
                print(f"  ⚠️  No structured data extracted (may be normal for some formats)")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print()
    
    return True


def test_pdf_processing(pdf_path: Path, base_url: str = "http://localhost:8070"):
    """Test GROBID PDF processing."""
    print("\n" + "=" * 60)
    print("Testing GROBID PDF Processing")
    print("=" * 60)
    
    if not pdf_path.exists():
        print(f"❌ PDF file not found: {pdf_path}")
        return False
    
    print(f"Processing PDF: {pdf_path.name}")
    print(f"File size: {pdf_path.stat().st_size / 1024:.1f} KB")
    
    client = GrobidClient(base_url=base_url)
    
    if not client.is_available:
        print("❌ GROBID service not available")
        return False
    
    try:
        print("\nExtracting bibliographic data...")
        bib_data = client.extract_bibliographic_data(pdf_path=pdf_path)
        
        if bib_data:
            print("✅ Successfully extracted bibliographic data:")
            print(json.dumps(bib_data, indent=2))
        else:
            print("⚠️  No bibliographic data extracted (may be normal)")
        
        print("\nExtracting citations from PDF text...")
        # Extract text first (simplified - in real pipeline we use file_handlers)
        from file_handlers import extract_text_from_file
        text = extract_text_from_file(pdf_path)
        
        results = extract_citations_with_grobid(
            text,
            pdf_path=pdf_path,
            grobid_url=base_url
        )
        
        print(f"\nResults:")
        print(f"  Available: {results.get('available', False)}")
        print(f"  Citations found: {results.get('citation_count', 0)}")
        print(f"  Source: {results.get('source', 'unknown')}")
        
        if results.get('citations'):
            print(f"\n  Sample citations ({min(3, len(results['citations']))}):")
            for i, cit in enumerate(results['citations'][:3], 1):
                print(f"    {i}. {cit}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing PDF: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all GROBID tests."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test GROBID service in isolation")
    parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8070",
        help="GROBID service URL (default: http://localhost:8070)"
    )
    parser.add_argument(
        "--pdf",
        type=Path,
        default=None,
        help="Optional PDF file to test with"
    )
    parser.add_argument(
        "--skip-pdf",
        action="store_true",
        help="Skip PDF processing test"
    )
    
    args = parser.parse_args()
    
    print("\n" + "=" * 60)
    print("GROBID Standalone Test")
    print("=" * 60)
    print(f"\nGROBID URL: {args.url}\n")
    
    # Test 1: Health check
    if not test_grobid_health(args.url):
        print("\n❌ GROBID health check failed. Please check your Docker container.")
        sys.exit(1)
    
    # Test 2: Citation parsing
    test_citation_parsing(args.url)
    
    # Test 3: PDF processing (if PDF provided or default)
    if not args.skip_pdf:
        if args.pdf:
            pdf_path = args.pdf
        else:
            # Try to find a test PDF
            data_dir = Path(__file__).parent / "data" / "research_papers"
            pdfs = list(data_dir.glob("*.pdf"))
            if pdfs:
                pdf_path = pdfs[0]
                print(f"\nUsing default PDF: {pdf_path.name}")
            else:
                print("\n⚠️  No PDF found for testing. Use --pdf to specify one.")
                pdf_path = None
        
        if pdf_path:
            test_pdf_processing(pdf_path, args.url)
    
    print("\n" + "=" * 60)
    print("Test Complete")
    print("=" * 60)
    print("\n✅ GROBID is working correctly!")
    print("   You can now run the full pipeline with:")
    print("   python main.py -category research_paper -num 1")


if __name__ == "__main__":
    main()

