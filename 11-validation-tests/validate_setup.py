#!/usr/bin/env python3
"""
Setup Validation Script for Core Technical Testing Framework
Validates configuration, dependencies, and test environment
"""

import os
import sys
import json
from pathlib import Path

# Add framework to path
sys.path.append(str(Path(__file__).parent / "01-core-technical"))

def validate_python_version():
    """Validate Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def validate_dependencies():
    """Validate required Python packages"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'openai',
        'anthropic', 
        'python-dotenv',
        'pyyaml',
        'jsonschema',
        'matplotlib',
        'pandas',
        'pytest'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True

def validate_configuration():
    """Validate configuration files"""
    print("\n⚙️  Checking configuration...")
    
    # Check .env file
    env_file = Path("TESTS/.env")
    if env_file.exists():
        print("✅ .env file found")
        
        # Check for required environment variables
        with open(env_file, 'r') as f:
            env_content = f.read()
        
        required_vars = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'VIDEO_FOLDER']
        missing_vars = []
        
        for var in required_vars:
            if var not in env_content or f"{var}=your_" in env_content:
                missing_vars.append(var)
        
        if missing_vars:
            print(f"⚠️  Missing or placeholder values: {', '.join(missing_vars)}")
        else:
            print("✅ Environment variables configured")
    else:
        print("❌ .env file not found")
        print("Create TESTS/.env with your API keys")
        return False
    
    return True

def validate_directory_structure():
    """Validate directory structure"""
    print("\n📁 Checking directory structure...")
    
    required_dirs = [
        "TESTS/01-core-technical",
        "TESTS/01-core-technical/framework",
        "TESTS/01-core-technical/scripts",
        "TESTS/01-core-technical/results",
        "TESTS/01-core-technical/test-data",
        "video"
    ]
    
    all_present = True
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"✅ {dir_path} - OK")
        else:
            print(f"❌ {dir_path} - MISSING")
            all_present = False
    
    return all_present

def validate_video_files():
    """Validate video files"""
    print("\n🎥 Checking video files...")
    
    video_folder = Path("video")
    if not video_folder.exists():
        print("❌ Video folder not found")
        return False
    
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(video_folder.glob(f"*{ext}"))
    
    if video_files:
        print(f"✅ Found {len(video_files)} video files")
        for video in video_files[:5]:  # Show first 5
            print(f"   - {video.name}")
        if len(video_files) > 5:
            print(f"   ... and {len(video_files) - 5} more")
        return True
    else:
        print("⚠️  No video files found")
        print("Add test videos to the 'video' folder")
        return False

def validate_test_scripts():
    """Validate test scripts"""
    print("\n🧪 Checking test scripts...")
    
    test_scripts = [
        "TESTS/01-core-technical/scripts/run_test_01.py",
        "TESTS/01-core-technical/scripts/run_test_02.py", 
        "TESTS/01-core-technical/scripts/run_test_03.py",
        "TESTS/01-core-technical/scripts/run_test_04.py",
        "TESTS/run_tests.py"
    ]
    
    all_present = True
    
    for script in test_scripts:
        path = Path(script)
        if path.exists():
            print(f"✅ {path.name} - OK")
        else:
            print(f"❌ {path.name} - MISSING")
            all_present = False
    
    return all_present

def estimate_costs():
    """Estimate test execution costs"""
    print("\n💰 Estimating test costs...")
    
    cost_estimates = {
        "Test 01 (Semantic Extraction)": 30.0,
        "Test 02 (JSON Generation)": 25.0,
        "Test 03 (Content Regeneration)": 50.0,
        "Test 04 (Code Extraction)": 40.0
    }
    
    total_cost = sum(cost_estimates.values())
    
    print("Estimated costs per test:")
    for test, cost in cost_estimates.items():
        print(f"  - {test}: £{cost:.2f}")
    
    print(f"\nTotal estimated cost: £{total_cost:.2f}")
    print("💡 Tip: Use --budget parameter to limit spending")
    
    return cost_estimates

def main():
    """Main validation function"""
    print("🔍 CORE TECHNICAL TESTING FRAMEWORK - SETUP VALIDATION")
    print("=" * 60)
    
    validations = [
        ("Python Version", validate_python_version),
        ("Dependencies", validate_dependencies),
        ("Configuration", validate_configuration),
        ("Directory Structure", validate_directory_structure),
        ("Video Files", validate_video_files),
        ("Test Scripts", validate_test_scripts)
    ]
    
    results = {}
    
    for name, validator in validations:
        results[name] = validator()
    
    # Cost estimation
    estimate_costs()
    
    # Summary
    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(results.values())
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {name}")
    
    print(f"\nOverall: {passed}/{total} validations passed")
    
    if passed == total:
        print("\n🎉 Setup validation PASSED - ready to run tests!")
        print("\nNext steps:")
        print("1. python TESTS/run_tests.py --dry-run")
        print("2. python TESTS/run_tests.py --test 01 --budget 30")
        return True
    else:
        print("\n⚠️  Setup validation FAILED - fix issues above")
        print("\nCommon fixes:")
        print("1. pip install -r TESTS/01-core-technical/requirements.txt")
        print("2. Copy TESTS/.env.example to TESTS/.env and add your API keys")
        print("3. Add test videos to the 'video' folder")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)