"""
Claude 3.5 Sonnet model integration for narrative understanding and JSON generation.

This module implements the Claude 3.5 Sonnet API integration for narrative analysis
and structured JSON generation from semantic data as part of the semantic compression
testing framework.
"""

import os
import time
import json
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    raise ImportError("Anthropic package not installed. Run: pip install anthropic>=0.8.0")

from .base_model import BaseModel, ModelResponse, CostEstimate


class ClaudeSonnetModel(BaseModel):
    """
    Claude 3.5 Sonnet model implementation for narrative understanding and JSON generation.
    
    This class handles narrative analysis and structured JSON generation using Claude 3.5 Sonnet,
    focusing on narrative structure, contextual understanding, relationship dynamics,
    and hierarchical scene-based JSON schema generation.
    """
    
    # Cost per analysis (approximate)
    COST_PER_ANALYSIS = 0.02  # $0.02 per analysis
    COST_PER_JSON_GENERATION = 0.03  # $0.03 per JSON generation
    
    def __init__(self, api_key: Optional[str] = None, rate_limit: int = 15, max_retries: int = 3):
        """
        Initialize Claude 3.5 Sonnet model.
        
        Args:
            api_key: Anthropic API key (if None, will use ANTHROPIC_API_KEY env var)
            rate_limit: Maximum requests per minute
            max_retries: Maximum retry attempts for failed requests
        """
        if api_key is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
        
        super().__init__("claude_sonnet", api_key, rate_limit)
        self.max_retries = max_retries
        
        if not self.validate_api_key():
            raise ValueError("Anthropic API key not provided or invalid")
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
    
    def extract_semantics(self, content: Union[str, Dict[str, Any]], **kwargs) -> ModelResponse:
        """
        Extract narrative understanding from content using Claude 3.5 Sonnet.
        
        Args:
            content: Either text content or semantic data from previous analysis
            **kwargs: Additional parameters:
                - analysis_type: Type of analysis ("narrative", "json_generation")
                - schema_type: JSON schema type for generation
                
        Returns:
            ModelResponse containing narrative analysis results
        """
        start_time = time.time()
        
        try:
            # Handle rate limiting
            self._handle_rate_limiting()
            
            analysis_type = kwargs.get("analysis_type", "narrative")
            
            if analysis_type == "narrative":
                result = self._perform_narrative_analysis(content)
            elif analysis_type == "json_generation":
                schema_type = kwargs.get("schema_type", "hierarchical")
                result = self._generate_json_structure(content, schema_type)
            else:
                return self._create_error_response(f"Unknown analysis type: {analysis_type}")
            
            processing_time = time.time() - start_time
            estimated_cost = self.COST_PER_ANALYSIS
            
            # Track cost
            self.track_cost(estimated_cost)
            
            return ModelResponse(
                success=True,
                data=result,
                confidence_scores=result.get("confidence_scores", {}),
                processing_time=processing_time,
                actual_cost=estimated_cost,
                model_name=self.model_name
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return self._create_error_response(f"Error in semantic extraction: {str(e)}", processing_time)
    
    def generate_content(self, blueprint: Dict[str, Any], **kwargs) -> ModelResponse:
        """
        Generate JSON structures from semantic blueprint.
        
        Args:
            blueprint: Semantic blueprint containing generation instructions
            **kwargs: Additional parameters:
                - schema_type: Type of JSON schema to generate
                - cultural_adaptation: Target culture for adaptation
                
        Returns:
            ModelResponse containing generated JSON structure
        """
        start_time = time.time()
        
        try:
            self._handle_rate_limiting()
            
            schema_type = kwargs.get("schema_type", "hierarchical")
            cultural_adaptation = kwargs.get("cultural_adaptation", None)
            
            # Generate JSON structure
            json_result = self._generate_json_structure(blueprint, schema_type, cultural_adaptation)
            
            processing_time = time.time() - start_time
            estimated_cost = self.COST_PER_JSON_GENERATION
            
            self.track_cost(estimated_cost)
            
            return ModelResponse(
                success=True,
                data=json_result,
                confidence_scores=json_result.get("confidence_scores", {}),
                processing_time=processing_time,
                actual_cost=estimated_cost,
                model_name=self.model_name
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return self._create_error_response(f"Error in content generation: {str(e)}", processing_time)
    
    def get_cost_estimate(self, content_size: int, operation_type: str = "extract") -> CostEstimate:
        """
        Estimate cost for Claude 3.5 Sonnet operations.
        
        Args:
            content_size: Size of content (in characters or tokens)
            operation_type: Type of operation ("extract" or "generate")
            
        Returns:
            CostEstimate with estimated cost
        """
        if operation_type == "extract":
            estimated_cost = self.COST_PER_ANALYSIS
        else:  # generate
            estimated_cost = self.COST_PER_JSON_GENERATION
        
        return CostEstimate(
            estimated_cost=estimated_cost,
            operation_type=operation_type,
            content_size=content_size
        )
    
    def _perform_narrative_analysis(self, content: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
        """
        Perform comprehensive narrative understanding analysis.
        
        Args:
            content: Content to analyze (text or semantic data)
            
        Returns:
            Dictionary containing narrative analysis results
        """
        # Create narrative analysis prompt
        prompt = self._create_narrative_analysis_prompt(content)
        
        # Make API call with retry logic
        for attempt in range(self.max_retries):
            try:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=3000,
                    temperature=0.3,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                
                # Parse response
                analysis_text = response.content[0].text
                return self._parse_narrative_analysis(analysis_text)
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return {}
    
    def _generate_json_structure(self, content: Union[str, Dict[str, Any]], 
                                schema_type: str = "hierarchical", 
                                cultural_adaptation: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate structured JSON representation from semantic data.
        
        Args:
            content: Semantic data to convert to JSON
            schema_type: Type of JSON schema ("hierarchical", "character_centric", "temporal")
            cultural_adaptation: Target culture for adaptation
            
        Returns:
            Dictionary containing JSON structure and metadata
        """
        # Create JSON generation prompt
        prompt = self._create_json_generation_prompt(content, schema_type, cultural_adaptation)
        
        # Make API call with retry logic
        for attempt in range(self.max_retries):
            try:
                response = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=4000,
                    temperature=0.2,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )
                
                # Parse response
                response_text = response.content[0].text
                return self._parse_json_generation(response_text, schema_type)
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return {}
    
    def _create_narrative_analysis_prompt(self, content: Union[str, Dict[str, Any]]) -> str:
        """Create comprehensive narrative analysis prompt."""
        content_str = json.dumps(content, indent=2) if isinstance(content, dict) else str(content)
        
        return f"""
I need you to perform comprehensive narrative understanding analysis on this content. Please analyze and extract:

CONTENT TO ANALYZE:
{content_str}

NARRATIVE STRUCTURE:
- Beginning, middle, end identification with specific timestamps/markers
- Plot points and story progression with narrative beats
- Character development arcs and transformation moments
- Conflict introduction, escalation, and resolution patterns
- Pacing analysis and narrative momentum shifts

CONTEXTUAL UNDERSTANDING:
- Implicit meanings and subtext that aren't explicitly stated
- Cultural references and their significance to the narrative
- Historical or social context that informs character behavior
- Symbolic elements and their deeper meanings
- Metaphorical language and visual metaphors

RELATIONSHIP DYNAMICS:
- Character interactions and relationship evolution
- Power dynamics and social hierarchies within scenes
- Communication patterns and styles between characters
- Trust, conflict, and intimacy progression
- Group dynamics and social positioning

THEMATIC ELEMENTS:
- Main themes and messages conveyed
- Underlying philosophical or moral questions
- Social commentary and cultural critique
- Universal human experiences represented
- Emotional themes and psychological depth

CULTURAL AND TEMPORAL CONTEXT:
- Time period indicators and historical markers
- Cultural norms and expectations reflected
- Generational differences in behavior and values
- Regional or ethnic cultural elements
- Social class and economic status indicators

For each category, provide:
1. Detailed analysis with specific examples
2. Confidence rating (1-10) for your analysis
3. Key narrative elements that must be preserved in any adaptation
4. Potential cultural adaptation considerations

Format your response as structured analysis with clear categories and confidence scores.
Rate your overall confidence (1-10) for each analysis point and note any ambiguities or uncertainties.
"""
    
    def _create_json_generation_prompt(self, content: Union[str, Dict[str, Any]], 
                                     schema_type: str, cultural_adaptation: Optional[str] = None) -> str:
        """Create JSON structure generation prompt."""
        content_str = json.dumps(content, indent=2) if isinstance(content, dict) else str(content)
        
        cultural_note = ""
        if cultural_adaptation:
            cultural_note = f"\nCULTURAL ADAPTATION: Adapt the content for {cultural_adaptation} culture while preserving core narrative structure."
        
        schema_instructions = self._get_schema_instructions(schema_type)
        
        return f"""
Generate a comprehensive JSON structure from this semantic content for video regeneration purposes.

CONTENT TO PROCESS:
{content_str}

SCHEMA TYPE: {schema_type}
{schema_instructions}

{cultural_note}

REQUIREMENTS:
1. Create a hierarchical JSON structure that captures ALL semantic information
2. Include video_metadata with technical and contextual information
3. Structure scenes as an array with detailed scene information
4. For each scene include: scene_id, timestamps, setting, characters, actions, dialogue, cultural_elements
5. Preserve implicit relationships and cultural context
6. Include confidence scores for each major element
7. Ensure the JSON could theoretically regenerate the original content with high fidelity

JSON STRUCTURE REQUIREMENTS:
- video_metadata: duration, genre, cultural_context, technical_specs
- scenes: array of scene objects with comprehensive details
- characters: detailed character profiles with consistency markers
- cultural_elements: specific cultural signals and context
- temporal_consistency: markers for maintaining continuity
- regeneration_notes: specific requirements for accurate recreation

Provide the JSON structure along with:
1. Schema compliance assessment
2. Semantic completeness score (0-100%)
3. Compression ratio estimate
4. Cultural adaptation notes (if applicable)
5. Confidence scores for major elements

Format as valid JSON followed by analysis metadata.
"""
    
    def _get_schema_instructions(self, schema_type: str) -> str:
        """Get specific instructions for different schema types."""
        if schema_type == "hierarchical":
            return """
HIERARCHICAL SCHEMA: Organize content in nested hierarchies from video -> scenes -> moments -> details.
Focus on temporal progression and nested relationships between elements.
"""
        elif schema_type == "character_centric":
            return """
CHARACTER-CENTRIC SCHEMA: Organize content around character perspectives and interactions.
Each character should have detailed profiles, arcs, and relationship mappings.
"""
        elif schema_type == "temporal":
            return """
TEMPORAL SCHEMA: Organize content strictly by time progression with detailed timestamps.
Focus on temporal consistency and chronological narrative flow.
"""
        else:
            return """
STANDARD SCHEMA: Use a balanced approach combining hierarchical, character, and temporal elements.
"""
    
    def _parse_narrative_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """
        Parse narrative analysis response into structured format.
        
        Args:
            analysis_text: Raw analysis text from Claude
            
        Returns:
            Structured narrative analysis data
        """
        try:
            # Try to extract JSON if present
            if "```json" in analysis_text:
                json_start = analysis_text.find("```json") + 7
                json_end = analysis_text.find("```", json_start)
                json_text = analysis_text[json_start:json_end].strip()
                return json.loads(json_text)
        except:
            pass
        
        # Fallback: create structured format from text analysis
        return {
            "narrative_structure": {
                "analysis": self._extract_section(analysis_text, "NARRATIVE STRUCTURE"),
                "confidence": self._extract_confidence(analysis_text, "narrative structure")
            },
            "contextual_understanding": {
                "analysis": self._extract_section(analysis_text, "CONTEXTUAL UNDERSTANDING"),
                "confidence": self._extract_confidence(analysis_text, "contextual understanding")
            },
            "relationship_dynamics": {
                "analysis": self._extract_section(analysis_text, "RELATIONSHIP DYNAMICS"),
                "confidence": self._extract_confidence(analysis_text, "relationship dynamics")
            },
            "thematic_elements": {
                "analysis": self._extract_section(analysis_text, "THEMATIC ELEMENTS"),
                "confidence": self._extract_confidence(analysis_text, "thematic elements")
            },
            "cultural_temporal_context": {
                "analysis": self._extract_section(analysis_text, "CULTURAL AND TEMPORAL"),
                "confidence": self._extract_confidence(analysis_text, "cultural")
            },
            "raw_analysis": analysis_text,
            "confidence_scores": {
                "overall_analysis": 8.0,
                "narrative_structure": self._extract_confidence(analysis_text, "narrative"),
                "contextual_understanding": self._extract_confidence(analysis_text, "contextual"),
                "relationship_dynamics": self._extract_confidence(analysis_text, "relationship"),
                "thematic_elements": self._extract_confidence(analysis_text, "thematic"),
                "cultural_context": self._extract_confidence(analysis_text, "cultural")
            }
        }
    
    def _parse_json_generation(self, response_text: str, schema_type: str) -> Dict[str, Any]:
        """
        Parse JSON generation response.
        
        Args:
            response_text: Raw response text from Claude
            schema_type: Type of schema generated
            
        Returns:
            Dictionary containing JSON structure and metadata
        """
        try:
            # Extract JSON structure
            json_structure = None
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_text = response_text[json_start:json_end].strip()
                json_structure = json.loads(json_text)
            
            # Extract metadata
            metadata = self._extract_json_metadata(response_text)
            
            return {
                "json_structure": json_structure or {},
                "schema_type": schema_type,
                "schema_compliance": metadata.get("schema_compliance", True),
                "semantic_completeness": metadata.get("semantic_completeness", 85.0),
                "compression_ratio": metadata.get("compression_ratio", 500.0),
                "cultural_adaptation_notes": metadata.get("cultural_adaptation", ""),
                "confidence_scores": {
                    "json_quality": metadata.get("json_quality", 8.5),
                    "schema_compliance": 9.0 if metadata.get("schema_compliance", True) else 6.0,
                    "semantic_completeness": metadata.get("semantic_completeness", 85.0) / 10.0,
                    "regeneration_potential": metadata.get("regeneration_potential", 7.5)
                },
                "raw_response": response_text,
                "generation_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "json_structure": {},
                "schema_type": schema_type,
                "error": f"Failed to parse JSON generation: {str(e)}",
                "raw_response": response_text,
                "confidence_scores": {"json_quality": 3.0}
            }
    
    def _extract_section(self, text: str, section_keyword: str) -> str:
        """Extract a specific section from the analysis text."""
        lines = text.split('\n')
        section_lines = []
        in_section = False
        
        for line in lines:
            if section_keyword.upper() in line.upper():
                in_section = True
                section_lines.append(line)
            elif in_section and line.strip() and not any(keyword in line.upper() for keyword in ["NARRATIVE", "CONTEXTUAL", "RELATIONSHIP", "THEMATIC", "CULTURAL"]):
                section_lines.append(line)
            elif in_section and any(keyword in line.upper() for keyword in ["NARRATIVE", "CONTEXTUAL", "RELATIONSHIP", "THEMATIC", "CULTURAL"]):
                break
        
        return '\n'.join(section_lines)
    
    def _extract_confidence(self, text: str, category: str) -> float:
        """Extract confidence score for a category from the analysis text."""
        import re
        patterns = [
            rf"{category}.*?confidence.*?(\d+(?:\.\d+)?)",
            rf"confidence.*?{category}.*?(\d+(?:\.\d+)?)",
            rf"(\d+(?:\.\d+)?)/10.*?{category}",
            rf"{category}.*?(\d+(?:\.\d+)?)/10"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                try:
                    score = float(matches[0])
                    return min(10.0, max(1.0, score))
                except:
                    continue
        
        return 7.5  # Default confidence score for Claude
    
    def _extract_json_metadata(self, response_text: str) -> Dict[str, Any]:
        """Extract metadata from JSON generation response."""
        import re
        
        metadata = {}
        
        # Extract semantic completeness
        completeness_match = re.search(r"semantic completeness.*?(\d+(?:\.\d+)?)%?", response_text.lower())
        if completeness_match:
            metadata["semantic_completeness"] = float(completeness_match.group(1))
        
        # Extract compression ratio
        compression_match = re.search(r"compression ratio.*?(\d+(?:\.\d+)?):1", response_text.lower())
        if compression_match:
            metadata["compression_ratio"] = float(compression_match.group(1))
        
        # Extract schema compliance
        if "schema compliance" in response_text.lower():
            if "100%" in response_text or "compliant" in response_text.lower():
                metadata["schema_compliance"] = True
            else:
                metadata["schema_compliance"] = False
        
        return metadata