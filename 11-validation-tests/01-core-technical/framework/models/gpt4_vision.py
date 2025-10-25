"""
GPT-4 Vision model integration for semantic extraction from video content.

This module implements the GPT-4 Vision API integration for extracting semantic
information from video content as part of the semantic compression testing framework.
"""

import os
import time
import base64
import cv2
import tempfile
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import json

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("OpenAI package not installed. Run: pip install openai>=1.0.0")

from .base_model import BaseModel, ModelResponse, CostEstimate


class GPT4VisionModel(BaseModel):
    """
    GPT-4 Vision model implementation for semantic extraction.
    
    This class handles video analysis using GPT-4 Vision API, extracting semantic
    information including micro-expressions, body language, cultural signals,
    and temporal consistency for semantic compression testing.
    """
    
    # Cost per image analysis (approximate)
    COST_PER_IMAGE = 0.01  # $0.01 per image
    COST_PER_VIDEO_BASE = 0.04  # Base cost for video processing
    
    def __init__(self, api_key: Optional[str] = None, rate_limit: int = 10, max_retries: int = 3):
        """
        Initialize GPT-4 Vision model.
        
        Args:
            api_key: OpenAI API key (if None, will use OPENAI_API_KEY env var)
            rate_limit: Maximum requests per minute
            max_retries: Maximum retry attempts for failed requests
        """
        if api_key is None:
            api_key = os.getenv("OPENAI_API_KEY")
        
        super().__init__("gpt4_vision", api_key, rate_limit)
        self.max_retries = max_retries
        
        if not self.validate_api_key():
            raise ValueError("OpenAI API key not provided or invalid")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def extract_semantics(self, content: Union[str, Path], **kwargs) -> ModelResponse:
        """
        Extract semantic information from video content using GPT-4 Vision.
        
        Args:
            content: Path to video file
            **kwargs: Additional parameters:
                - frames_to_analyze: Number of frames to extract (default: 5)
                - analysis_depth: Level of analysis detail (default: "comprehensive")
                
        Returns:
            ModelResponse containing semantic extraction results
        """
        start_time = time.time()
        
        try:
            # Handle rate limiting
            self._handle_rate_limiting()
            
            # Extract frames from video
            video_path = Path(content)
            if not video_path.exists():
                return self._create_error_response(f"Video file not found: {video_path}")
            
            frames_to_analyze = kwargs.get("frames_to_analyze", 5)
            analysis_depth = kwargs.get("analysis_depth", "comprehensive")
            
            # Extract frames
            frames = self._extract_video_frames(video_path, frames_to_analyze)
            if not frames:
                return self._create_error_response("Failed to extract frames from video")
            
            # Analyze frames with GPT-4 Vision
            semantic_data = self._analyze_frames_with_gpt4v(frames, analysis_depth)
            
            processing_time = time.time() - start_time
            estimated_cost = self.COST_PER_VIDEO_BASE + (len(frames) * self.COST_PER_IMAGE)
            
            # Track cost
            self.track_cost(estimated_cost)
            
            return ModelResponse(
                success=True,
                data=semantic_data,
                confidence_scores=semantic_data.get("confidence_scores", {}),
                processing_time=processing_time,
                actual_cost=estimated_cost,
                model_name=self.model_name
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return self._create_error_response(f"Error in semantic extraction: {str(e)}", processing_time)
    
    def generate_content(self, blueprint: Dict[str, Any], **kwargs) -> ModelResponse:
        """
        Generate content descriptions from semantic blueprint.
        
        Note: GPT-4 Vision is primarily for analysis, not content generation.
        This method provides detailed descriptions that could guide other generation models.
        
        Args:
            blueprint: Semantic blueprint containing generation instructions
            **kwargs: Additional parameters
            
        Returns:
            ModelResponse containing generation guidance
        """
        start_time = time.time()
        
        try:
            self._handle_rate_limiting()
            
            # Create generation prompt from blueprint
            prompt = self._create_generation_prompt(blueprint)
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in visual content generation guidance. Provide detailed instructions for recreating visual content based on semantic blueprints."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=2000,
                temperature=0.3
            )
            
            processing_time = time.time() - start_time
            estimated_cost = 0.02  # Approximate cost for text generation
            
            self.track_cost(estimated_cost)
            
            generation_data = {
                "generation_guidance": response.choices[0].message.content,
                "blueprint_processed": blueprint,
                "generation_type": "visual_guidance"
            }
            
            return ModelResponse(
                success=True,
                data=generation_data,
                confidence_scores={"generation_quality": 8.0},
                processing_time=processing_time,
                actual_cost=estimated_cost,
                model_name=self.model_name
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return self._create_error_response(f"Error in content generation: {str(e)}", processing_time)
    
    def get_cost_estimate(self, content_size: int, operation_type: str = "extract") -> CostEstimate:
        """
        Estimate cost for GPT-4 Vision operations.
        
        Args:
            content_size: Size of content (for videos, this is duration in seconds)
            operation_type: Type of operation ("extract" or "generate")
            
        Returns:
            CostEstimate with estimated cost
        """
        if operation_type == "extract":
            # Estimate frames based on video duration (1 frame per 10 seconds)
            estimated_frames = max(1, content_size // 10)
            estimated_cost = self.COST_PER_VIDEO_BASE + (estimated_frames * self.COST_PER_IMAGE)
        else:  # generate
            estimated_cost = 0.02
        
        return CostEstimate(
            estimated_cost=estimated_cost,
            operation_type=operation_type,
            content_size=content_size
        )
    
    def _extract_video_frames(self, video_path: Path, num_frames: int = 5) -> List[str]:
        """
        Extract frames from video and encode as base64.
        
        Args:
            video_path: Path to video file
            num_frames: Number of frames to extract
            
        Returns:
            List of base64-encoded frame images
        """
        try:
            cap = cv2.VideoCapture(str(video_path))
            if not cap.isOpened():
                return []
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            if total_frames == 0:
                return []
            
            # Calculate frame indices to extract evenly distributed frames
            frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]
            
            frames = []
            for frame_idx in frame_indices:
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if ret:
                    # Encode frame as base64
                    _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    frame_b64 = base64.b64encode(buffer).decode('utf-8')
                    frames.append(frame_b64)
            
            cap.release()
            return frames
            
        except Exception as e:
            print(f"Error extracting frames: {e}")
            return []
    
    def _analyze_frames_with_gpt4v(self, frames: List[str], analysis_depth: str = "comprehensive") -> Dict[str, Any]:
        """
        Analyze video frames using GPT-4 Vision with semantic extraction prompt.
        
        Args:
            frames: List of base64-encoded frame images
            analysis_depth: Level of analysis detail
            
        Returns:
            Dictionary containing semantic analysis results
        """
        # Create the comprehensive semantic extraction prompt
        system_prompt = """You are an expert in semantic video analysis for content compression and regeneration. 
        Your task is to extract ALL semantic information needed to recreate this video with complete authenticity. 
        This is not description - this is semantic blueprinting for regeneration."""
        
        user_prompt = self._create_semantic_extraction_prompt()
        
        # Prepare messages with images
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": user_prompt}
                ] + [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{frame}",
                            "detail": "high"
                        }
                    } for frame in frames
                ]
            }
        ]
        
        # Make API call with retry logic
        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4-vision-preview",
                    messages=messages,
                    max_tokens=3000,
                    temperature=0.2
                )
                
                # Parse response into structured format
                analysis_text = response.choices[0].message.content
                return self._parse_semantic_analysis(analysis_text)
                
            except Exception as e:
                if attempt == self.max_retries - 1:
                    raise e
                time.sleep(2 ** attempt)  # Exponential backoff
        
        return {}
    
    def _create_semantic_extraction_prompt(self) -> str:
        """Create the detailed semantic extraction prompt based on Test 01 specification."""
        return """
MICRO-EXPRESSION ANALYSIS (Critical for Authenticity):
- Facial muscle movements: eyebrow micro-raises, lip compressions, nostril flares
- Eye movement patterns: saccades, fixation points, blink timing and meaning
- Micro-expressions <0.5 seconds that convey subtext or internal conflict
- Asymmetrical facial expressions indicating mixed emotions
- Confidence level (1-10) for detecting these subtle human cues

BODY LANGUAGE SEMANTICS (Essential for Character Consistency):
- Posture shifts and weight distribution changes with emotional meaning
- Hand gesture timing, amplitude, and cultural significance
- Proxemics: interpersonal distance and cultural appropriateness
- Unconscious mirroring or rejection behaviors between characters
- Breathing patterns visible in chest/shoulder movement

VOCAL SEMANTIC LAYERS (if audio cues visible):
- Mouth movements indicating vocal fry, uptalk patterns
- Facial expressions showing pace changes and hesitation
- Visual cues of volume modulation and emotional state
- Lip-sync patterns and speech rhythm indicators

CULTURAL MICRO-SIGNALS (Critical for Cross-Cultural Adaptation):
- Eye contact patterns specific to cultural context
- Touch boundaries and cultural appropriateness
- Status indicators in clothing, posture, spatial positioning
- Cultural communication styles (direct vs indirect visual cues)
- Generational markers in behavior and expression

TEMPORAL SEMANTIC CONSISTENCY (For Multi-Scene Regeneration):
- Character emotional arc progression across frames
- Relationship dynamic evolution (trust, tension, intimacy changes)
- Environmental mood shifts (lighting, atmosphere, energy)
- Narrative momentum and pacing semantic markers

REGENERATION-CRITICAL ASSESSMENT:
- What specific micro-details would a human notice if missing?
- Which facial expressions carry the most semantic weight?
- What cultural elements would feel "off" if regenerated incorrectly?
- Which temporal inconsistencies would break immersion?
- What cannot current AI reliably detect or recreate?

For each category, provide:
1. Detailed observations
2. Confidence rating (1-10)
3. Specific regeneration requirements
4. Potential failure points

Format your response as structured JSON with clear categories and confidence scores.
"""
    
    def _parse_semantic_analysis(self, analysis_text: str) -> Dict[str, Any]:
        """
        Parse the semantic analysis response into structured format.
        
        Args:
            analysis_text: Raw analysis text from GPT-4 Vision
            
        Returns:
            Structured semantic analysis data
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
            "micro_expressions": {
                "analysis": self._extract_section(analysis_text, "MICRO-EXPRESSION"),
                "confidence": self._extract_confidence(analysis_text, "micro-expression")
            },
            "body_language": {
                "analysis": self._extract_section(analysis_text, "BODY LANGUAGE"),
                "confidence": self._extract_confidence(analysis_text, "body language")
            },
            "cultural_signals": {
                "analysis": self._extract_section(analysis_text, "CULTURAL"),
                "confidence": self._extract_confidence(analysis_text, "cultural")
            },
            "temporal_consistency": {
                "analysis": self._extract_section(analysis_text, "TEMPORAL"),
                "confidence": self._extract_confidence(analysis_text, "temporal")
            },
            "regeneration_assessment": {
                "analysis": self._extract_section(analysis_text, "REGENERATION"),
                "confidence": self._extract_confidence(analysis_text, "regeneration")
            },
            "raw_analysis": analysis_text,
            "confidence_scores": {
                "overall_analysis": 7.5,
                "micro_expressions": self._extract_confidence(analysis_text, "micro-expression"),
                "body_language": self._extract_confidence(analysis_text, "body language"),
                "cultural_signals": self._extract_confidence(analysis_text, "cultural"),
                "temporal_consistency": self._extract_confidence(analysis_text, "temporal")
            }
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
            elif in_section and line.strip() and not any(keyword in line.upper() for keyword in ["MICRO-EXPRESSION", "BODY LANGUAGE", "CULTURAL", "TEMPORAL", "REGENERATION"]):
                section_lines.append(line)
            elif in_section and any(keyword in line.upper() for keyword in ["MICRO-EXPRESSION", "BODY LANGUAGE", "CULTURAL", "TEMPORAL", "REGENERATION"]):
                break
        
        return '\n'.join(section_lines)
    
    def _extract_confidence(self, text: str, category: str) -> float:
        """Extract confidence score for a category from the analysis text."""
        # Look for patterns like "confidence: 7/10" or "confidence level: 8"
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
        
        return 6.0  # Default confidence score
    
    def _create_generation_prompt(self, blueprint: Dict[str, Any]) -> str:
        """Create generation guidance prompt from semantic blueprint."""
        return f"""
Based on this semantic blueprint, provide detailed visual generation instructions:

Blueprint: {json.dumps(blueprint, indent=2)}

Please provide:
1. Detailed visual composition requirements
2. Character appearance and expression specifications
3. Lighting and atmosphere requirements
4. Cultural authenticity guidelines
5. Temporal consistency requirements
6. Specific technical parameters for generation models

Format as detailed generation instructions that could guide DALL-E, Midjourney, or video generation models.
"""