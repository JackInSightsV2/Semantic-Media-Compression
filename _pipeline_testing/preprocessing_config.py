"""
Preprocessing configuration for different document types.
Defines which preprocessing models to use for each category.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class PreprocessingConfig:
    """Configuration for preprocessing models per document type."""
    use_grobid: bool = False  # Use GROBID for citation parsing
    use_ner: bool = True  # Use lightweight NER for entity extraction
    ner_focus: str = "citations"  # Focus: "citations", "entities", "general", "none"
    grobid_url: Optional[str] = None  # GROBID service URL (default: localhost:8070)


# Preprocessing configuration per category
PREPROCESSING_CONFIG: Dict[str, PreprocessingConfig] = {
    # Research papers: Use both GROBID and NER for citations
    "research": PreprocessingConfig(
        use_grobid=True,
        use_ner=True,
        ner_focus="citations",
        grobid_url="http://localhost:8070"  # Default local GROBID
    ),
    "research_paper": PreprocessingConfig(
        use_grobid=True,
        use_ner=True,
        ner_focus="citations",
        grobid_url="http://localhost:8070"
    ),
    "paper": PreprocessingConfig(
        use_grobid=True,
        use_ner=True,
        ner_focus="citations",
        grobid_url="http://localhost:8070"
    ),
    
    # Business plans: Use NER for entities (names, dates, organizations)
    "business": PreprocessingConfig(
        use_grobid=False,
        use_ner=True,
        ner_focus="entities"
    ),
    "business_plan": PreprocessingConfig(
        use_grobid=False,
        use_ner=True,
        ner_focus="entities"
    ),
    "plan": PreprocessingConfig(
        use_grobid=False,
        use_ner=True,
        ner_focus="entities"
    ),
    
    # Narrative fiction: Use NER for character names, locations, dates
    "fiction": PreprocessingConfig(
        use_grobid=False,
        use_ner=True,
        ner_focus="general"
    ),
    "narrative": PreprocessingConfig(
        use_grobid=False,
        use_ner=True,
        ner_focus="general"
    ),
    "story": PreprocessingConfig(
        use_grobid=False,
        use_ner=True,
        ner_focus="general"
    ),
    
    # Technical docs: Use NER for technical terms, APIs, entities
    "technical": PreprocessingConfig(
        use_grobid=False,
        use_ner=True,
        ner_focus="entities"
    ),
    "api": PreprocessingConfig(
        use_grobid=False,
        use_ner=True,
        ner_focus="entities"
    ),
    "docs": PreprocessingConfig(
        use_grobid=False,
        use_ner=True,
        ner_focus="entities"
    ),
    
    # Reports: Use NER for entities and dates
    "report": PreprocessingConfig(
        use_grobid=False,
        use_ner=True,
        ner_focus="entities"
    ),
    "reports": PreprocessingConfig(
        use_grobid=False,
        use_ner=True,
        ner_focus="entities"
    ),
}


def get_preprocessing_config(category: str) -> PreprocessingConfig:
    """
    Get preprocessing configuration for a category.
    
    Args:
        category: Document category name
        
    Returns:
        PreprocessingConfig for the category
    """
    category_key = category.lower().strip()
    return PREPROCESSING_CONFIG.get(category_key, PreprocessingConfig(
        use_grobid=False,
        use_ner=True,
        ner_focus="general"
    ))

