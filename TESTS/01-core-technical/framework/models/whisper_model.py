"""
Whisper model integration for audio transcription and semantic analysis.

This module implements local Whisper integration for extracting audio semantic
information from video content as part of the semantic compression testing framework.
"""

import os
import time
import tempfile
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import json

try:
    import whisper
    import torch
except ImportError:
    raise ImportError("Whisper and torch packages not installed. Run: pip install openai-whisper torch")

try:
    import ffmpeg
except ImportError:
    raise ImportError("ffmpeg-python package not installed. Run: pip install ffmpeg-python")

from .base_model import BaseModel, ModelResponse, CostEstimate


class WhisperModel(BaseModel):
    """
    Whisper model implementation for audio transcription and semantic analysis.
    
    This class handles local audio transcription using OpenAI Whisper, extracting
    vocal semantic layers, speech patterns, and audio-based cultural signals
    for semantic compression testing.
    """
    
    # Cost is essentially free for local processing (only compute time)
    COST_PER_MINUTE = 0.001  # Minimal cost for local processing
    
    def __init__(self, model_size: str = "base", device: Optional[str] = None):
        """
        Initialize Whisper model.
        
        Args:
            model_size: Whisper model size ("tiny", "base", "small", "medium", "large")
            device: Device to run on ("cpu", "cuda", or None for auto-detection)
        """
        super().__init__("whisper_local", "", 60)  # No API key needed, high rate limit
        
        self.model_size = model_size
        
        # Auto-detect device if not specified
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device
        
        # Load Whisper model
        try:
            self.model = whisper.load_model(model_size, device=device)
        except Exception as e:
            raise RuntimeError(f"Failed to load Whisper model: {e}")
    
    def extract_semantics(self, content: Union[str, Path], **kwargs) -> ModelResponse:
        """
        Extract audio semantic information from video content using Whisper.
        
        Args:
            content: Path to video or audio file
            **kwargs: Additional parameters:
                - language: Expected language (None for auto-detection)
                - task: "transcribe" or "translate"
                - analyze_prosody: Whether to analyze prosodic features
                
        Returns:
            ModelResponse containing audio semantic analysis results
        """
        start_time = time.time()
        
        try:
            # Extract audio from video if needed
            audio_path = self._extract_audio_from_video(content)
            if not audio_path:
                return self._create_error_response("Failed to extract audio from video")
            
            language = kwargs.get("language", None)
            task = kwargs.get("task", "transcribe")
            analyze_prosody = kwargs.get("analyze_prosody", True)
            
            # Transcribe audio
            transcription_result = self.model.transcribe(
                str(audio_path),
                language=language,
                task=task,
                word_timestamps=True,
                verbose=False
            )
            
            # Analyze semantic layers
            semantic_data = self._analyze_vocal_semantics(transcription_result, analyze_prosody)
            
            # Clean up temporary audio file if created
            if str(audio_path) != str(content):
                try:
                    os.unlink(audio_path)
                except:
                    pass
            
            processing_time = time.time() - start_time
            estimated_cost = processing_time * self.COST_PER_MINUTE / 60  # Cost based on processing time
            
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
            return self._create_error_response(f"Error in audio semantic extraction: {str(e)}", processing_time)
    
    def generate_content(self, blueprint: Dict[str, Any], **kwargs) -> ModelResponse:
        """
        Generate audio guidance from semantic blueprint.
        
        Note: Whisper is for transcription, not audio generation.
        This method provides detailed audio specifications for generation models.
        
        Args:
            blueprint: Semantic blueprint containing audio generation instructions
            **kwargs: Additional parameters
            
        Returns:
            ModelResponse containing audio generation guidance
        """
        start_time = time.time()
        
        try:
            # Create audio generation guidance from blueprint
            audio_guidance = self._create_audio_generation_guidance(blueprint)
            
            processing_time = time.time() - start_time
            estimated_cost = 0.001  # Minimal cost for guidance generation
            
            self.track_cost(estimated_cost)
            
            return ModelResponse(
                success=True,
                data=audio_guidance,
                confidence_scores={"guidance_quality": 8.0},
                processing_time=processing_time,
                actual_cost=estimated_cost,
                model_name=self.model_name
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return self._create_error_response(f"Error in audio guidance generation: {str(e)}", processing_time)
    
    def get_cost_estimate(self, content_size: int, operation_type: str = "extract") -> CostEstimate:
        """
        Estimate cost for Whisper operations (essentially free for local processing).
        
        Args:
            content_size: Duration in seconds
            operation_type: Type of operation
            
        Returns:
            CostEstimate with estimated cost
        """
        # Estimate processing time (roughly real-time for base model)
        estimated_processing_time = content_size * 1.2  # 20% overhead
        estimated_cost = estimated_processing_time * self.COST_PER_MINUTE / 60
        
        return CostEstimate(
            estimated_cost=estimated_cost,
            operation_type=operation_type,
            content_size=content_size
        )
    
    def _extract_audio_from_video(self, video_path: Union[str, Path]) -> Optional[Path]:
        """
        Extract audio from video file using ffmpeg.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Path to extracted audio file or None if failed
        """
        try:
            video_path = Path(video_path)
            
            # If it's already an audio file, return as-is
            if video_path.suffix.lower() in ['.wav', '.mp3', '.m4a', '.flac']:
                return video_path
            
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_audio:
                temp_audio_path = Path(temp_audio.name)
            
            # Extract audio using ffmpeg
            (
                ffmpeg
                .input(str(video_path))
                .output(str(temp_audio_path), acodec='pcm_s16le', ac=1, ar='16000')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True)
            )
            
            return temp_audio_path
            
        except Exception as e:
            print(f"Error extracting audio: {e}")
            return None
    
    def _analyze_vocal_semantics(self, transcription_result: Dict[str, Any], analyze_prosody: bool = True) -> Dict[str, Any]:
        """
        Analyze vocal semantic layers from transcription results.
        
        Args:
            transcription_result: Whisper transcription result
            analyze_prosody: Whether to analyze prosodic features
            
        Returns:
            Dictionary containing vocal semantic analysis
        """
        # Extract basic transcription data
        text = transcription_result.get("text", "")
        segments = transcription_result.get("segments", [])
        language = transcription_result.get("language", "unknown")
        
        # Analyze speech patterns
        speech_patterns = self._analyze_speech_patterns(segments)
        
        # Analyze prosodic features if requested
        prosodic_features = {}
        if analyze_prosody:
            prosodic_features = self._analyze_prosodic_features(segments)
        
        # Analyze cultural and linguistic markers
        cultural_markers = self._analyze_cultural_markers(text, language, segments)
        
        # Calculate confidence scores
        confidence_scores = self._calculate_audio_confidence_scores(transcription_result, segments)
        
        return {
            "transcription": {
                "text": text,
                "language": language,
                "segments": segments
            },
            "vocal_semantic_layers": {
                "speech_patterns": speech_patterns,
                "prosodic_features": prosodic_features,
                "cultural_markers": cultural_markers,
                "confidence": confidence_scores.get("vocal_layers", 7.0)
            },
            "temporal_audio_consistency": {
                "speech_rhythm": self._analyze_speech_rhythm(segments),
                "pace_variations": self._analyze_pace_variations(segments),
                "confidence": confidence_scores.get("temporal_consistency", 6.5)
            },
            "regeneration_requirements": {
                "voice_characteristics": self._extract_voice_characteristics(segments),
                "emotional_markers": self._extract_emotional_markers(segments),
                "cultural_authenticity": cultural_markers,
                "confidence": confidence_scores.get("regeneration_potential", 6.0)
            },
            "confidence_scores": confidence_scores,
            "raw_transcription": transcription_result
        }
    
    def _analyze_speech_patterns(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze speech patterns from transcription segments."""
        if not segments:
            return {}
        
        # Calculate speaking rate (words per minute)
        total_words = sum(len(segment.get("text", "").split()) for segment in segments)
        total_duration = segments[-1].get("end", 0) - segments[0].get("start", 0)
        speaking_rate = (total_words / max(total_duration / 60, 0.1)) if total_duration > 0 else 0
        
        # Analyze pauses
        pauses = []
        for i in range(1, len(segments)):
            pause_duration = segments[i].get("start", 0) - segments[i-1].get("end", 0)
            if pause_duration > 0.1:  # Significant pause
                pauses.append(pause_duration)
        
        avg_pause_duration = sum(pauses) / len(pauses) if pauses else 0
        
        return {
            "speaking_rate_wpm": speaking_rate,
            "average_pause_duration": avg_pause_duration,
            "total_pauses": len(pauses),
            "speech_continuity": 1.0 - (len(pauses) / max(len(segments), 1))
        }
    
    def _analyze_prosodic_features(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze prosodic features from speech segments."""
        # Note: Whisper doesn't provide direct prosodic information,
        # so we infer from available data
        
        prosodic_markers = []
        
        for segment in segments:
            text = segment.get("text", "").strip()
            
            # Detect potential prosodic markers from text
            if text.endswith("?"):
                prosodic_markers.append("rising_intonation")
            elif text.endswith("!"):
                prosodic_markers.append("emphatic_stress")
            elif "..." in text or text.endswith("..."):
                prosodic_markers.append("hesitation_pause")
            
            # Analyze word-level timing if available
            words = segment.get("words", [])
            if words:
                word_durations = []
                for word in words:
                    duration = word.get("end", 0) - word.get("start", 0)
                    word_durations.append(duration)
                
                if word_durations:
                    avg_word_duration = sum(word_durations) / len(word_durations)
                    # Detect potential emphasis (unusually long words)
                    for i, duration in enumerate(word_durations):
                        if duration > avg_word_duration * 1.5:
                            prosodic_markers.append("word_emphasis")
        
        return {
            "prosodic_markers": prosodic_markers,
            "intonation_patterns": self._detect_intonation_patterns(segments),
            "stress_patterns": self._detect_stress_patterns(segments),
            "rhythm_analysis": self._analyze_rhythm(segments)
        }
    
    def _analyze_cultural_markers(self, text: str, language: str, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cultural and linguistic markers in speech."""
        cultural_indicators = {
            "language": language,
            "formality_level": self._detect_formality_level(text),
            "cultural_expressions": self._detect_cultural_expressions(text, language),
            "regional_markers": self._detect_regional_markers(text, language)
        }
        
        return cultural_indicators
    
    def _calculate_audio_confidence_scores(self, transcription_result: Dict[str, Any], segments: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate confidence scores for audio analysis."""
        # Use Whisper's internal confidence if available
        base_confidence = 7.0  # Default confidence for Whisper
        
        # Adjust based on transcription quality indicators
        text_length = len(transcription_result.get("text", ""))
        segment_count = len(segments)
        
        # Higher confidence for longer, more structured transcriptions
        length_factor = min(1.0, text_length / 500)  # Normalize to 500 characters
        structure_factor = min(1.0, segment_count / 10)  # Normalize to 10 segments
        
        adjusted_confidence = base_confidence * (0.7 + 0.15 * length_factor + 0.15 * structure_factor)
        
        return {
            "overall_transcription": min(10.0, adjusted_confidence),
            "vocal_layers": min(10.0, adjusted_confidence * 0.8),  # Slightly lower for semantic analysis
            "temporal_consistency": min(10.0, adjusted_confidence * 0.7),
            "regeneration_potential": min(10.0, adjusted_confidence * 0.6),  # Lowest for regeneration
            "cultural_accuracy": min(10.0, adjusted_confidence * 0.75)
        }
    
    def _analyze_speech_rhythm(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze speech rhythm patterns."""
        if not segments:
            return {}
        
        segment_durations = []
        for segment in segments:
            duration = segment.get("end", 0) - segment.get("start", 0)
            segment_durations.append(duration)
        
        if not segment_durations:
            return {}
        
        avg_duration = sum(segment_durations) / len(segment_durations)
        rhythm_variance = sum((d - avg_duration) ** 2 for d in segment_durations) / len(segment_durations)
        
        return {
            "average_segment_duration": avg_duration,
            "rhythm_variance": rhythm_variance,
            "rhythm_regularity": 1.0 / (1.0 + rhythm_variance)  # Higher = more regular
        }
    
    def _analyze_pace_variations(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze pace variations throughout the speech."""
        pace_variations = []
        
        for i, segment in enumerate(segments):
            duration = segment.get("end", 0) - segment.get("start", 0)
            word_count = len(segment.get("text", "").split())
            
            if duration > 0:
                pace = word_count / duration  # Words per second
                pace_variations.append({
                    "segment_index": i,
                    "pace_wps": pace,
                    "timestamp": segment.get("start", 0)
                })
        
        return pace_variations
    
    def _extract_voice_characteristics(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract voice characteristics for regeneration."""
        # Note: Limited information available from Whisper transcription
        return {
            "estimated_speaker_count": 1,  # Whisper doesn't do speaker diarization by default
            "speech_clarity": "high" if segments else "unknown",
            "background_noise": "low",  # Inferred from successful transcription
            "voice_consistency": "maintained"
        }
    
    def _extract_emotional_markers(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract emotional markers from speech patterns."""
        emotional_markers = []
        
        for segment in segments:
            text = segment.get("text", "").strip()
            
            # Simple emotional marker detection based on text patterns
            if any(word in text.lower() for word in ["!", "wow", "oh", "ah"]):
                emotional_markers.append({
                    "timestamp": segment.get("start", 0),
                    "marker_type": "exclamation",
                    "text": text
                })
            
            if "..." in text:
                emotional_markers.append({
                    "timestamp": segment.get("start", 0),
                    "marker_type": "hesitation",
                    "text": text
                })
        
        return emotional_markers
    
    def _detect_intonation_patterns(self, segments: List[Dict[str, Any]]) -> List[str]:
        """Detect intonation patterns from text cues."""
        patterns = []
        for segment in segments:
            text = segment.get("text", "")
            if text.endswith("?"):
                patterns.append("rising")
            elif text.endswith("!"):
                patterns.append("emphatic")
            else:
                patterns.append("neutral")
        return patterns
    
    def _detect_stress_patterns(self, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Detect stress patterns in speech."""
        stress_patterns = []
        
        for segment in segments:
            words = segment.get("words", [])
            for word in words:
                # Simple heuristic: longer duration might indicate stress
                duration = word.get("end", 0) - word.get("start", 0)
                if duration > 0.5:  # Arbitrary threshold
                    stress_patterns.append({
                        "word": word.get("word", ""),
                        "timestamp": word.get("start", 0),
                        "duration": duration,
                        "stress_level": "high" if duration > 1.0 else "medium"
                    })
        
        return stress_patterns
    
    def _analyze_rhythm(self, segments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze overall speech rhythm."""
        if not segments:
            return {}
        
        # Calculate inter-segment intervals
        intervals = []
        for i in range(1, len(segments)):
            interval = segments[i].get("start", 0) - segments[i-1].get("end", 0)
            intervals.append(interval)
        
        if not intervals:
            return {}
        
        avg_interval = sum(intervals) / len(intervals)
        rhythm_regularity = 1.0 - (max(intervals) - min(intervals)) / max(avg_interval, 0.1)
        
        return {
            "average_interval": avg_interval,
            "rhythm_regularity": max(0.0, rhythm_regularity),
            "total_intervals": len(intervals)
        }
    
    def _detect_formality_level(self, text: str) -> str:
        """Detect formality level of speech."""
        formal_indicators = ["please", "thank you", "sir", "madam", "would you", "could you"]
        informal_indicators = ["yeah", "ok", "gonna", "wanna", "hey", "cool"]
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in text.lower())
        informal_count = sum(1 for indicator in informal_indicators if indicator in text.lower())
        
        if formal_count > informal_count:
            return "formal"
        elif informal_count > formal_count:
            return "informal"
        else:
            return "neutral"
    
    def _detect_cultural_expressions(self, text: str, language: str) -> List[str]:
        """Detect cultural expressions in speech."""
        # This is a simplified implementation
        cultural_expressions = []
        
        # Language-specific cultural markers
        if language == "en":
            english_expressions = ["you know", "like", "actually", "basically", "literally"]
            for expr in english_expressions:
                if expr in text.lower():
                    cultural_expressions.append(expr)
        
        return cultural_expressions
    
    def _detect_regional_markers(self, text: str, language: str) -> List[str]:
        """Detect regional linguistic markers."""
        # Simplified implementation
        regional_markers = []
        
        # This would need much more sophisticated analysis in practice
        if "y'all" in text.lower():
            regional_markers.append("southern_us")
        if "eh" in text.lower():
            regional_markers.append("canadian")
        
        return regional_markers
    
    def _create_audio_generation_guidance(self, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """Create audio generation guidance from semantic blueprint."""
        return {
            "audio_generation_guidance": {
                "voice_characteristics": blueprint.get("voice_characteristics", {}),
                "speech_patterns": blueprint.get("speech_patterns", {}),
                "emotional_delivery": blueprint.get("emotional_markers", []),
                "cultural_authenticity": blueprint.get("cultural_markers", {}),
                "temporal_requirements": blueprint.get("temporal_consistency", {})
            },
            "technical_specifications": {
                "sample_rate": "44100 Hz",
                "bit_depth": "16-bit",
                "channels": "mono or stereo",
                "format": "WAV or MP3"
            },
            "generation_notes": "Audio generation guidance based on semantic analysis. Requires specialized TTS or voice cloning models for implementation.",
            "confidence_scores": {
                "guidance_completeness": 8.0,
                "technical_accuracy": 9.0,
                "regeneration_feasibility": 6.5
            }
        }