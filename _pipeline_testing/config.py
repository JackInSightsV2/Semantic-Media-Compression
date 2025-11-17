"""Configuration and constants for the semantic distillation pipeline."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_KEY not found in .env file")

MODEL = "x-ai/grok-4-fast"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Directory paths
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
RESPONSES_DIR = SCRIPT_DIR / "responses"
OUTPUT_DIR = SCRIPT_DIR / "output"
SCHEMAS_DIR = SCRIPT_DIR / "schemas"

# Create directories
DATA_DIR.mkdir(exist_ok=True)
RESPONSES_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Category mapping: category_name -> (data_folder, schema_folder, schema_id)
CATEGORY_MAP = {
    "research": ("research_papers", "research_paper", "research_paper_distillation"),
    "research_paper": ("research_papers", "research_paper", "research_paper_distillation"),
    "paper": ("research_papers", "research_paper", "research_paper_distillation"),
    "business": ("business_plans", "business_plan", "business_plan_distillation"),
    "business_plan": ("business_plans", "business_plan", "business_plan_distillation"),
    "plan": ("business_plans", "business_plan", "business_plan_distillation"),
    "fiction": ("narrative_fiction", "narrative_fiction", "narrative_fiction_distillation"),
    "narrative": ("narrative_fiction", "narrative_fiction", "narrative_fiction_distillation"),
    "story": ("narrative_fiction", "narrative_fiction", "narrative_fiction_distillation"),
    "technical": ("technical_documentation", "technical_documentation", "technical_documentation_distillation"),
    "technical_documentation": ("technical_documentation", "technical_documentation", "technical_documentation_distillation"),
    "api": ("technical_documentation", "technical_documentation", "technical_documentation_distillation"),
    "docs": ("technical_documentation", "technical_documentation", "technical_documentation_distillation"),
    "report": ("reports", "report", "report_distillation"),
    "reports": ("reports", "report", "report_distillation"),
}


