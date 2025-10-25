"""
Data models for semantic compression testing framework.

This module contains all the dataclasses and data structures used throughout
the testing framework for semantic media compression validation.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


@dataclass
class VideoTestContent:
    """
    Represents video content used for semantic compression testing.
    
    Attributes:
        file_path: Path to the video file
        genre: Genre classification (e.g., 'documentary', 'action', 'educational')
        duration: Video duration in seconds
        cultural_context: Cultural context description
        ground_truth_annotations: Reference annotations for validation
    """
    file_path: str
    genre: str
    duration: float
    cultural_context: str
    ground_truth_annotations: Dict[str, Any]


@dataclass
class SemanticExtractionResult:
    """
    Results from semantic extraction testing on video content.
    
    Attributes:
        test_id: Unique identifier for the test run
        model_name: Name of the AI model used (e.g., 'gpt4_vision', 'claude_sonnet')
        extraction_data: Extracted semantic information containing:
            - micro_expressions: Facial micro-expression analysis
            - body_language: Body language and gesture analysis
            - cultural_signals: Cultural context and signals
            - vocal_layers: Audio semantic analysis
            - temporal_consistency: Consistency across time
        accuracy_score: Accuracy score from 0-10 scale
        processing_time: Time taken for processing in seconds
        cost: API cost for this extraction
        timestamp: When the extraction was performed
    """
    test_id: str
    model_name: str
    extraction_data: Dict[str, Any]
    accuracy_score: float  # 0-10 scale
    processing_time: float
    cost: float
    timestamp: datetime


@dataclass
class JSONGenerationResult:
    """
    Results from JSON structure generation testing.
    
    Attributes:
        test_id: Unique identifier for the test run
        model_name: Name of the AI model used
        schema_type: Type of JSON schema used (e.g., 'hierarchical', 'character_centric')
        json_data: Generated JSON structure
        schema_compliance: Whether JSON complies with schema (boolean)
        semantic_completeness: Completeness percentage (0-100%)
        compression_ratio: Achieved compression ratio (target 500:1+)
        timestamp: When the generation was performed
    """
    test_id: str
    model_name: str
    schema_type: str
    json_data: Dict[str, Any]
    schema_compliance: bool
    semantic_completeness: float  # 0-100%
    compression_ratio: float  # Target 500:1+
    timestamp: datetime


@dataclass
class QualityMetrics:
    """
    Quality metrics for content regeneration and validation.
    
    Attributes:
        character_consistency: Character consistency across scenes (target 80%+)
        scene_coherence: Scene coherence and narrative flow (target 75%+)
        cultural_accuracy: Cultural representation accuracy (target 70%+)
        overall_score: Overall quality score calculated from individual metrics
    """
    character_consistency: float  # Target 80%+
    scene_coherence: float  # Target 75%+
    cultural_accuracy: float  # Target 70%+
    overall_score: float


@dataclass
class CodeTestContent:
    """
    Represents code content used for semantic extraction testing.
    
    Attributes:
        file_path: Path to the code file
        language: Programming language (e.g., 'python', 'javascript', 'java')
        complexity_level: Code complexity level ('simple', 'medium', 'complex')
        business_domain: Business domain context
        test_suite_path: Path to associated test suite for validation
        ground_truth_semantics: Reference semantic extraction for validation
    """
    file_path: str
    language: str
    complexity_level: str
    business_domain: str
    test_suite_path: str
    ground_truth_semantics: Optional[Dict[str, Any]] = None


@dataclass
class TestSummary:
    """
    Summary of test execution results across all test cases.
    
    Attributes:
        test_id: Unique identifier for the test run
        test_type: Type of test ('semantic_extraction', 'json_generation', etc.)
        total_test_cases: Total number of test cases executed
        passed_cases: Number of test cases that passed
        failed_cases: Number of test cases that failed
        average_scores: Average quality metrics across all test cases
        cost_summary: Total cost breakdown
        execution_time: Total execution time in seconds
        timestamp: When the test summary was generated
        detailed_results: List of individual test results
    """
    test_id: str
    test_type: str
    total_test_cases: int
    passed_cases: int
    failed_cases: int
    average_scores: QualityMetrics
    cost_summary: Dict[str, float]
    execution_time: float
    timestamp: datetime
    detailed_results: List[Any] = field(default_factory=list)


@dataclass
class ContentRegenerationResult:
    """
    Results from content regeneration testing.
    
    Attributes:
        test_id: Unique identifier for the test run
        model_name: Name of the generation model used
        original_content_id: ID of the original content
        regenerated_content_path: Path to regenerated content
        quality_metrics: Quality assessment metrics
        generation_time: Time taken for generation
        cost: Cost of generation
        cycle_number: Regeneration cycle number (for multi-cycle testing)
        timestamp: When regeneration was performed
    """
    test_id: str
    model_name: str
    original_content_id: str
    regenerated_content_path: str
    quality_metrics: QualityMetrics
    generation_time: float
    cost: float
    cycle_number: int
    timestamp: datetime


@dataclass
class CodeExtractionResult:
    """
    Results from code semantic extraction testing.
    
    Attributes:
        test_id: Unique identifier for the test run
        model_name: Name of the AI model used
        source_code_path: Path to original source code
        extracted_semantics: Extracted semantic blueprint
        regenerated_code_paths: Paths to regenerated code in different languages
        functional_equivalence_scores: Equivalence scores by language
        business_logic_preservation: Business logic preservation score (target 98%+)
        architectural_pattern_fidelity: Pattern fidelity score (target 90%+)
        processing_time: Time taken for extraction and regeneration
        cost: Total cost for extraction and regeneration
        timestamp: When the extraction was performed
    """
    test_id: str
    model_name: str
    source_code_path: str
    extracted_semantics: Dict[str, Any]
    regenerated_code_paths: Dict[str, str]  # language -> file_path
    functional_equivalence_scores: Dict[str, float]  # language -> score (target 95%+)
    business_logic_preservation: float  # Target 98%+
    architectural_pattern_fidelity: float  # Target 90%+
    processing_time: float
    cost: float
    timestamp: datetime


# Export all dataclasses for easy importing
__all__ = [
    'VideoTestContent',
    'SemanticExtractionResult', 
    'JSONGenerationResult',
    'QualityMetrics',
    'CodeTestContent',
    'TestSummary',
    'ContentRegenerationResult',
    'CodeExtractionResult'
]
