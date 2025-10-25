"""
JSON schema validation and compression analysis for semantic blueprints.

This module provides validation methods for JSON schema compliance,
compression ratio calculation, and semantic completeness scoring.
"""

import json
import jsonschema
from jsonschema import validate, ValidationError
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import logging
from pathlib import Path
import os
import gzip
import sys

logger = logging.getLogger(__name__)

@dataclass
class JSONValidationResult:
    """Container for JSON validation results."""
    schema_compliance: bool
    compliance_score: float  # 0-100%
    validation_errors: List[str]
    schema_type: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'schema_compliance': self.schema_compliance,
            'compliance_score': self.compliance_score,
            'validation_errors': self.validation_errors,
            'schema_type': self.schema_type
        }

@dataclass
class CompressionAnalysisResult:
    """Container for compression analysis results."""
    original_size: int  # bytes
    compressed_size: int  # bytes
    compression_ratio: float  # ratio (e.g., 500:1 = 500.0)
    meets_target: bool  # True if >= 500:1
    size_reduction_percentage: float  # 0-100%
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'original_size': self.original_size,
            'compressed_size': self.compressed_size,
            'compression_ratio': self.compression_ratio,
            'meets_target': self.meets_target,
            'size_reduction_percentage': self.size_reduction_percentage
        }

@dataclass
class SemanticCompletenessResult:
    """Container for semantic completeness scoring results."""
    character_preservation: float  # 0-100%
    scene_detail_preservation: float  # 0-100%
    action_preservation: float  # 0-100%
    cultural_context_preservation: float  # 0-100%
    dialogue_meaning_preservation: float  # 0-100%
    overall_completeness: float  # 0-100%
    meets_target: bool  # True if >= 85%
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'character_preservation': self.character_preservation,
            'scene_detail_preservation': self.scene_detail_preservation,
            'action_preservation': self.action_preservation,
            'cultural_context_preservation': self.cultural_context_preservation,
            'dialogue_meaning_preservation': self.dialogue_meaning_preservation,
            'overall_completeness': self.overall_completeness,
            'meets_target': self.meets_target
        }

@dataclass
class CulturalAdaptationResult:
    """Container for cultural adaptation validation results."""
    adaptation_accuracy: float  # 0-100%
    cultural_sensitivity: float  # 0-100%
    context_preservation: float  # 0-100%
    localization_quality: float  # 0-100%
    overall_adaptation_score: float  # 0-100%
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'adaptation_accuracy': self.adaptation_accuracy,
            'cultural_sensitivity': self.cultural_sensitivity,
            'context_preservation': self.context_preservation,
            'localization_quality': self.localization_quality,
            'overall_adaptation_score': self.overall_adaptation_score
        }


class JSONValidator:
    """
    Validates JSON schema compliance and analyzes compression ratios.
    
    Provides methods for schema validation, compression analysis,
    semantic completeness scoring, and cultural adaptation validation.
    """
    
    def __init__(self, schema_directory: Optional[str] = None):
        """
        Initialize the JSON validator.
        
        Args:
            schema_directory: Path to directory containing JSON schemas
        """
        self.schema_directory = schema_directory or "TESTS/01-core-technical/test-data/schemas"
        self.compression_target = 500.0  # 500:1 minimum target
        self.completeness_target = 85.0  # 85% minimum target
        
        # Load predefined schemas
        self.schemas = self._load_schemas()
        
    def validate_schema_compliance(self, 
                                 json_data: Dict[str, Any], 
                                 schema_type: str) -> JSONValidationResult:
        """
        Validate JSON data against specified schema with 100% compliance requirement.
        
        Args:
            json_data: JSON data to validate
            schema_type: Type of schema to validate against
            
        Returns:
            JSONValidationResult with compliance details
        """
        logger.info(f"Validating JSON schema compliance for type: {schema_type}")
        
        schema = self.schemas.get(schema_type)
        if not schema:
            logger.error(f"Schema type '{schema_type}' not found")
            return JSONValidationResult(
                schema_compliance=False,
                compliance_score=0.0,
                validation_errors=[f"Schema type '{schema_type}' not found"],
                schema_type=schema_type
            )
        
        validation_errors = []
        compliance_score = 0.0
        
        try:
            # Validate against schema
            validate(instance=json_data, schema=schema)
            
            # If validation passes, check completeness
            compliance_score = self._calculate_schema_compliance_score(json_data, schema)
            schema_compliance = compliance_score >= 100.0  # 100% compliance requirement
            
            if not schema_compliance:
                validation_errors.append(f"Schema compliance score {compliance_score:.1f}% below 100% requirement")
            
        except ValidationError as e:
            schema_compliance = False
            validation_errors.append(f"Schema validation error: {e.message}")
            compliance_score = 0.0
            
        except Exception as e:
            schema_compliance = False
            validation_errors.append(f"Validation error: {str(e)}")
            compliance_score = 0.0
        
        return JSONValidationResult(
            schema_compliance=schema_compliance,
            compliance_score=compliance_score,
            validation_errors=validation_errors,
            schema_type=schema_type
        )
    
    def calculate_compression_ratio(self, 
                                  original_content_path: str, 
                                  json_blueprint: Dict[str, Any]) -> CompressionAnalysisResult:
        """
        Calculate compression ratio comparing original content to JSON blueprint.
        
        Args:
            original_content_path: Path to original video/content file
            json_blueprint: JSON semantic blueprint
            
        Returns:
            CompressionAnalysisResult with compression metrics
        """
        logger.info(f"Calculating compression ratio for: {original_content_path}")
        
        try:
            # Get original file size
            if not os.path.exists(original_content_path):
                logger.error(f"Original content file not found: {original_content_path}")
                return CompressionAnalysisResult(0, 0, 0.0, False, 0.0)
            
            original_size = os.path.getsize(original_content_path)
            
            # Calculate JSON blueprint size
            json_string = json.dumps(json_blueprint, separators=(',', ':'))
            compressed_size = len(json_string.encode('utf-8'))
            
            # Calculate compression ratio
            if compressed_size > 0:
                compression_ratio = original_size / compressed_size
            else:
                compression_ratio = 0.0
            
            # Check if meets target (500:1+)
            meets_target = compression_ratio >= self.compression_target
            
            # Calculate size reduction percentage
            size_reduction_percentage = ((original_size - compressed_size) / original_size * 100) if original_size > 0 else 0.0
            
            logger.info(f"Compression ratio: {compression_ratio:.1f}:1 (target: {self.compression_target}:1)")
            
            return CompressionAnalysisResult(
                original_size=original_size,
                compressed_size=compressed_size,
                compression_ratio=compression_ratio,
                meets_target=meets_target,
                size_reduction_percentage=size_reduction_percentage
            )
            
        except Exception as e:
            logger.error(f"Error calculating compression ratio: {e}")
            return CompressionAnalysisResult(0, 0, 0.0, False, 0.0)
    
    def semantic_completeness_score(self, 
                                  json_blueprint: Dict[str, Any],
                                  original_metadata: Dict[str, Any]) -> SemanticCompletenessResult:
        """
        Measure semantic completeness with 85%+ target.
        
        Args:
            json_blueprint: Generated JSON semantic blueprint
            original_metadata: Original content metadata for comparison
            
        Returns:
            SemanticCompletenessResult with completeness metrics
        """
        logger.info("Calculating semantic completeness score")
        
        # Score character preservation
        character_score = self._score_character_preservation(
            json_blueprint.get('characters', []),
            original_metadata.get('characters', [])
        )
        
        # Score scene detail preservation
        scene_score = self._score_scene_detail_preservation(
            json_blueprint.get('scenes', []),
            original_metadata.get('scenes', [])
        )
        
        # Score action preservation
        action_score = self._score_action_preservation(
            json_blueprint.get('actions', []),
            original_metadata.get('actions', [])
        )
        
        # Score cultural context preservation
        cultural_score = self._score_cultural_context_preservation(
            json_blueprint.get('cultural_elements', {}),
            original_metadata.get('cultural_elements', {})
        )
        
        # Score dialogue meaning preservation
        dialogue_score = self._score_dialogue_meaning_preservation(
            json_blueprint.get('dialogue', []),
            original_metadata.get('dialogue', [])
        )
        
        # Calculate overall completeness (weighted average)
        overall_completeness = (
            character_score * 0.25 +
            scene_score * 0.20 +
            action_score * 0.20 +
            cultural_score * 0.15 +
            dialogue_score * 0.20
        )
        
        # Check if meets target (85%+)
        meets_target = overall_completeness >= self.completeness_target
        
        return SemanticCompletenessResult(
            character_preservation=character_score,
            scene_detail_preservation=scene_score,
            action_preservation=action_score,
            cultural_context_preservation=cultural_score,
            dialogue_meaning_preservation=dialogue_score,
            overall_completeness=overall_completeness,
            meets_target=meets_target
        )
    
    def validate_cross_cultural_adaptation(self, 
                                         original_blueprint: Dict[str, Any],
                                         adapted_blueprint: Dict[str, Any],
                                         target_culture: str) -> CulturalAdaptationResult:
        """
        Validate cross-cultural adaptation while preserving narrative structure.
        
        Args:
            original_blueprint: Original JSON blueprint
            adapted_blueprint: Culturally adapted JSON blueprint
            target_culture: Target culture for adaptation
            
        Returns:
            CulturalAdaptationResult with adaptation metrics
        """
        logger.info(f"Validating cultural adaptation for target culture: {target_culture}")
        
        # Score adaptation accuracy
        adaptation_accuracy = self._score_adaptation_accuracy(
            original_blueprint, adapted_blueprint, target_culture
        )
        
        # Score cultural sensitivity
        cultural_sensitivity = self._score_cultural_sensitivity_adaptation(
            adapted_blueprint, target_culture
        )
        
        # Score context preservation
        context_preservation = self._score_context_preservation(
            original_blueprint, adapted_blueprint
        )
        
        # Score localization quality
        localization_quality = self._score_localization_quality(
            adapted_blueprint, target_culture
        )
        
        # Calculate overall adaptation score
        overall_score = (
            adaptation_accuracy * 0.30 +
            cultural_sensitivity * 0.25 +
            context_preservation * 0.25 +
            localization_quality * 0.20
        )
        
        return CulturalAdaptationResult(
            adaptation_accuracy=adaptation_accuracy,
            cultural_sensitivity=cultural_sensitivity,
            context_preservation=context_preservation,
            localization_quality=localization_quality,
            overall_adaptation_score=overall_score
        )
    
    def validate_hierarchical_schema(self, json_data: Dict[str, Any]) -> JSONValidationResult:
        """Validate against hierarchical scene-based schema."""
        return self.validate_schema_compliance(json_data, "hierarchical_scene_based")
    
    def validate_character_centric_schema(self, json_data: Dict[str, Any]) -> JSONValidationResult:
        """Validate against character-centric schema."""
        return self.validate_schema_compliance(json_data, "character_centric")
    
    def validate_temporal_schema(self, json_data: Dict[str, Any]) -> JSONValidationResult:
        """Validate against temporal schema."""
        return self.validate_schema_compliance(json_data, "temporal")
    
    def validate_cultural_schema(self, json_data: Dict[str, Any]) -> JSONValidationResult:
        """Validate against cultural schema."""
        return self.validate_schema_compliance(json_data, "cultural")
    
    # Private helper methods
    
    def _load_schemas(self) -> Dict[str, Dict[str, Any]]:
        """Load JSON schemas from schema directory."""
        schemas = {}
        
        # Define default schemas if directory doesn't exist
        default_schemas = {
            "hierarchical_scene_based": self._get_hierarchical_schema(),
            "character_centric": self._get_character_centric_schema(),
            "temporal": self._get_temporal_schema(),
            "cultural": self._get_cultural_schema()
        }
        
        schema_dir = Path(self.schema_directory)
        if schema_dir.exists():
            # Load schemas from files
            for schema_file in schema_dir.glob("*.json"):
                try:
                    with open(schema_file, 'r') as f:
                        schema_name = schema_file.stem
                        schemas[schema_name] = json.load(f)
                        logger.info(f"Loaded schema: {schema_name}")
                except Exception as e:
                    logger.error(f"Error loading schema {schema_file}: {e}")
        
        # Use default schemas for any missing ones
        for schema_name, schema_def in default_schemas.items():
            if schema_name not in schemas:
                schemas[schema_name] = schema_def
                logger.info(f"Using default schema: {schema_name}")
        
        return schemas
    
    def _get_hierarchical_schema(self) -> Dict[str, Any]:
        """Get hierarchical scene-based schema definition."""
        return {
            "type": "object",
            "required": ["video_metadata", "scenes"],
            "properties": {
                "video_metadata": {
                    "type": "object",
                    "required": ["title", "duration", "genre"],
                    "properties": {
                        "title": {"type": "string"},
                        "duration": {"type": "number"},
                        "genre": {"type": "string"},
                        "cultural_context": {"type": "string"}
                    }
                },
                "scenes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["scene_id", "timestamp", "setting", "characters", "actions"],
                        "properties": {
                            "scene_id": {"type": "string"},
                            "timestamp": {
                                "type": "object",
                                "required": ["start", "end"],
                                "properties": {
                                    "start": {"type": "number"},
                                    "end": {"type": "number"}
                                }
                            },
                            "setting": {"type": "string"},
                            "characters": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "actions": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "dialogue": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["character", "text"],
                                    "properties": {
                                        "character": {"type": "string"},
                                        "text": {"type": "string"},
                                        "emotion": {"type": "string"}
                                    }
                                }
                            },
                            "cultural_elements": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    
    def _get_character_centric_schema(self) -> Dict[str, Any]:
        """Get character-centric schema definition."""
        return {
            "type": "object",
            "required": ["characters", "narrative_structure"],
            "properties": {
                "characters": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name", "role", "appearances"],
                        "properties": {
                            "name": {"type": "string"},
                            "role": {"type": "string"},
                            "personality_traits": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "appearances": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "required": ["scene_id", "actions", "dialogue"],
                                    "properties": {
                                        "scene_id": {"type": "string"},
                                        "actions": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        },
                                        "dialogue": {
                                            "type": "array",
                                            "items": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "narrative_structure": {
                    "type": "object",
                    "required": ["acts", "themes"],
                    "properties": {
                        "acts": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "themes": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            }
        }
    
    def _get_temporal_schema(self) -> Dict[str, Any]:
        """Get temporal schema definition."""
        return {
            "type": "object",
            "required": ["timeline", "temporal_relationships"],
            "properties": {
                "timeline": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["timestamp", "event_type", "description"],
                        "properties": {
                            "timestamp": {"type": "number"},
                            "event_type": {"type": "string"},
                            "description": {"type": "string"},
                            "participants": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    }
                },
                "temporal_relationships": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["event1", "event2", "relationship"],
                        "properties": {
                            "event1": {"type": "string"},
                            "event2": {"type": "string"},
                            "relationship": {"type": "string"}
                        }
                    }
                }
            }
        }
    
    def _get_cultural_schema(self) -> Dict[str, Any]:
        """Get cultural schema definition."""
        return {
            "type": "object",
            "required": ["cultural_context", "cultural_elements"],
            "properties": {
                "cultural_context": {
                    "type": "object",
                    "required": ["primary_culture", "cultural_setting"],
                    "properties": {
                        "primary_culture": {"type": "string"},
                        "cultural_setting": {"type": "string"},
                        "time_period": {"type": "string"},
                        "geographic_location": {"type": "string"}
                    }
                },
                "cultural_elements": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["element_type", "description", "cultural_significance"],
                        "properties": {
                            "element_type": {"type": "string"},
                            "description": {"type": "string"},
                            "cultural_significance": {"type": "string"},
                            "sensitivity_level": {"type": "string"}
                        }
                    }
                }
            }
        }
    
    def _calculate_schema_compliance_score(self, json_data: Dict[str, Any], schema: Dict[str, Any]) -> float:
        """Calculate detailed schema compliance score."""
        # This is a simplified implementation
        # In practice, this would do detailed field-by-field analysis
        
        required_fields = schema.get("required", [])
        present_fields = [field for field in required_fields if field in json_data]
        
        if not required_fields:
            return 100.0
        
        compliance_percentage = (len(present_fields) / len(required_fields)) * 100
        return compliance_percentage
    
    def _score_character_preservation(self, blueprint_characters: List[Dict[str, Any]], 
                                    original_characters: List[Dict[str, Any]]) -> float:
        """Score character preservation in JSON blueprint."""
        if not original_characters:
            return 100.0
        
        if not blueprint_characters:
            return 0.0
        
        # Compare character names and key attributes
        original_names = {char.get('name', '') for char in original_characters}
        blueprint_names = {char.get('name', '') for char in blueprint_characters}
        
        name_preservation = len(original_names.intersection(blueprint_names)) / len(original_names) * 100
        
        # Score attribute preservation for matching characters
        attribute_scores = []
        for orig_char in original_characters:
            orig_name = orig_char.get('name', '')
            matching_char = next((char for char in blueprint_characters if char.get('name') == orig_name), None)
            
            if matching_char:
                # Compare key attributes
                attributes = ['role', 'personality_traits', 'appearance']
                matches = sum(1 for attr in attributes if orig_char.get(attr) == matching_char.get(attr))
                attribute_score = (matches / len(attributes)) * 100 if attributes else 0
                attribute_scores.append(attribute_score)
        
        avg_attribute_score = sum(attribute_scores) / len(attribute_scores) if attribute_scores else 0
        
        # Weighted combination
        return (name_preservation * 0.6 + avg_attribute_score * 0.4)
    
    def _score_scene_detail_preservation(self, blueprint_scenes: List[Dict[str, Any]], 
                                       original_scenes: List[Dict[str, Any]]) -> float:
        """Score scene detail preservation in JSON blueprint."""
        if not original_scenes:
            return 100.0
        
        if not blueprint_scenes:
            return 0.0
        
        # Compare scene count and details
        scene_count_ratio = min(len(blueprint_scenes) / len(original_scenes), 1.0)
        
        # Score detail preservation for matching scenes
        detail_scores = []
        for i, orig_scene in enumerate(original_scenes):
            if i < len(blueprint_scenes):
                blueprint_scene = blueprint_scenes[i]
                
                # Compare scene attributes
                attributes = ['setting', 'characters', 'actions', 'dialogue']
                matches = sum(1 for attr in attributes if attr in blueprint_scene and attr in orig_scene)
                detail_score = (matches / len(attributes)) * 100
                detail_scores.append(detail_score)
        
        avg_detail_score = sum(detail_scores) / len(detail_scores) if detail_scores else 0
        
        return (scene_count_ratio * 50 + avg_detail_score * 0.5)
    
    def _score_action_preservation(self, blueprint_actions: List[str], 
                                 original_actions: List[str]) -> float:
        """Score action preservation in JSON blueprint."""
        if not original_actions:
            return 100.0
        
        if not blueprint_actions:
            return 0.0
        
        # Calculate action overlap
        original_set = set(original_actions)
        blueprint_set = set(blueprint_actions)
        
        intersection = original_set.intersection(blueprint_set)
        preservation_ratio = len(intersection) / len(original_set)
        
        return preservation_ratio * 100
    
    def _score_cultural_context_preservation(self, blueprint_cultural: Dict[str, Any], 
                                           original_cultural: Dict[str, Any]) -> float:
        """Score cultural context preservation in JSON blueprint."""
        if not original_cultural:
            return 100.0
        
        if not blueprint_cultural:
            return 0.0
        
        # Compare cultural elements
        cultural_attributes = ['cultural_context', 'cultural_elements', 'cultural_references']
        matches = sum(1 for attr in cultural_attributes if attr in blueprint_cultural and attr in original_cultural)
        
        return (matches / len(cultural_attributes)) * 100 if cultural_attributes else 0
    
    def _score_dialogue_meaning_preservation(self, blueprint_dialogue: List[Dict[str, Any]], 
                                           original_dialogue: List[Dict[str, Any]]) -> float:
        """Score dialogue meaning preservation in JSON blueprint."""
        if not original_dialogue:
            return 100.0
        
        if not blueprint_dialogue:
            return 0.0
        
        # Compare dialogue count and content
        dialogue_count_ratio = min(len(blueprint_dialogue) / len(original_dialogue), 1.0)
        
        # Score meaning preservation (simplified)
        meaning_scores = []
        for i, orig_line in enumerate(original_dialogue):
            if i < len(blueprint_dialogue):
                blueprint_line = blueprint_dialogue[i]
                
                # Compare key elements
                character_match = orig_line.get('character') == blueprint_line.get('character')
                has_text = 'text' in blueprint_line and blueprint_line['text']
                has_emotion = 'emotion' in blueprint_line or 'tone' in blueprint_line
                
                meaning_score = (int(character_match) + int(has_text) + int(has_emotion)) / 3 * 100
                meaning_scores.append(meaning_score)
        
        avg_meaning_score = sum(meaning_scores) / len(meaning_scores) if meaning_scores else 0
        
        return (dialogue_count_ratio * 50 + avg_meaning_score * 0.5)
    
    def _score_adaptation_accuracy(self, original: Dict[str, Any], 
                                 adapted: Dict[str, Any], 
                                 target_culture: str) -> float:
        """Score cultural adaptation accuracy."""
        # Simplified adaptation scoring
        # Check if cultural elements have been appropriately modified
        
        original_cultural = original.get('cultural_elements', [])
        adapted_cultural = adapted.get('cultural_elements', [])
        
        # Score based on presence of target culture elements
        target_elements = [elem for elem in adapted_cultural if target_culture.lower() in str(elem).lower()]
        adaptation_ratio = len(target_elements) / max(len(adapted_cultural), 1)
        
        return adaptation_ratio * 100
    
    def _score_cultural_sensitivity_adaptation(self, adapted: Dict[str, Any], target_culture: str) -> float:
        """Score cultural sensitivity in adaptation."""
        # Simplified sensitivity scoring
        cultural_elements = adapted.get('cultural_elements', [])
        
        # Check for sensitivity markers
        sensitivity_indicators = ['respectful', 'authentic', 'appropriate', 'traditional']
        sensitive_elements = sum(1 for elem in cultural_elements 
                               if any(indicator in str(elem).lower() for indicator in sensitivity_indicators))
        
        if not cultural_elements:
            return 100.0
        
        return (sensitive_elements / len(cultural_elements)) * 100
    
    def _score_context_preservation(self, original: Dict[str, Any], adapted: Dict[str, Any]) -> float:
        """Score narrative context preservation during adaptation."""
        # Compare narrative structure preservation
        original_structure = original.get('narrative_structure', {})
        adapted_structure = adapted.get('narrative_structure', {})
        
        if not original_structure:
            return 100.0
        
        # Compare key structural elements
        structure_elements = ['acts', 'themes', 'character_arcs']
        preserved_elements = sum(1 for elem in structure_elements 
                               if elem in adapted_structure and elem in original_structure)
        
        return (preserved_elements / len(structure_elements)) * 100 if structure_elements else 0
    
    def _score_localization_quality(self, adapted: Dict[str, Any], target_culture: str) -> float:
        """Score localization quality for target culture."""
        # Simplified localization scoring
        # Check for appropriate cultural adaptations
        
        localization_indicators = [
            'language_adaptation',
            'cultural_references',
            'local_customs',
            'appropriate_imagery'
        ]
        
        present_indicators = sum(1 for indicator in localization_indicators 
                               if indicator in adapted or any(indicator in str(v) for v in adapted.values()))
        
        return (present_indicators / len(localization_indicators)) * 100