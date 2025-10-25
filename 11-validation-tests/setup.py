#!/usr/bin/env python3
"""Easy setup script for semantic compression testing framework"""

import os
import subprocess
import sys
from pathlib import Path

def setup_environment():
    """Set up virtual environment and install dependencies"""
    print("Setting up testing environment...")
    
    # Create virtual environment if it doesn't exist
    venv_path = Path("venv")
    if not venv_path.exists():
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
    else:
        print("Virtual environment already exists.")
    
    # Determine pip path based on OS
    if os.name == 'nt':  # Windows
        pip_path = "venv/Scripts/pip"
        python_path = "venv/Scripts/python"
    else:  # Unix/Linux/Mac
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    # Install dependencies
    requirements_file = Path("01-core-technical/requirements.txt")
    if requirements_file.exists():
        print("Installing dependencies...")
        subprocess.run([pip_path, "install", "-r", str(requirements_file)], check=True)
    else:
        print("Warning: requirements.txt not found. Please create it first.")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("Creating .env template...")
        create_env_template()
    else:
        print(".env file already exists.")
    
    print("\nSetup complete!")
    print("Next steps:")
    print("1. Update .env file with your actual API keys")
    print("2. Ensure video files are in the 'video' folder in project root")
    print("3. Run tests using: python run_tests.py")

def create_env_template():
    """Create .env template file"""
    template = """# API Keys - Replace with your actual keys
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here

# Budget Controls
TOTAL_BUDGET=200.0
PER_TEST_BUDGET=50.0
WARNING_THRESHOLD=0.8

# Video Settings
VIDEO_FOLDER=video
TEST_VIDEO_COUNT=5

# Model Settings
GPT4_MAX_REQUESTS_PER_MINUTE=10
CLAUDE_MAX_REQUESTS_PER_MINUTE=15
"""
    with open(".env", "w") as f:
        f.write(template)

def validate_setup():
    """Validate that setup was successful"""
    print("Validating setup...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("Warning: Python 3.8+ recommended")
    else:
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Check virtual environment
    venv_path = Path("venv")
    if venv_path.exists():
        print("✓ Virtual environment created")
    else:
        print("✗ Virtual environment not found")
    
    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print("✓ .env template created")
    else:
        print("✗ .env file not found")
    
    # Check requirements file
    requirements_file = Path("01-core-technical/requirements.txt")
    if requirements_file.exists():
        print("✓ requirements.txt found")
    else:
        print("✗ requirements.txt not found")
    
    # Check video folder
    video_folder = Path("../video")
    if video_folder.exists():
        print("✓ Video folder found")
    else:
        print("! Video folder not found - create 'video' folder in project root")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup semantic compression testing framework")
    parser.add_argument("--validate", action="store_true", help="Validate setup without installing")
    
    args = parser.parse_args()
    
    if args.validate:
        validate_setup()
    else:
        setup_environment()
        validate_setup()