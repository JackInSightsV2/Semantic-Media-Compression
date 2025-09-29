"""
Data management system for semantic compression testing framework.

This module handles loading test content (videos, code samples), ground truth data,
and provides metadata extraction capabilities for test content.
"""

import os
import json
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import subprocess
import mimetypes

# Optional OpenCV import for video metadata extraction
try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False
    print("Warning: OpenCV not available. Video metadata extraction will be limited.")

from . import (
    VideoTestContent, 
    CodeTestContent, 
    TestSummary,
    SemanticExtractionResult,
    JSONGenerationResult,
    ContentRegenerationResult,
    CodeExtractionResult
)


class DataLoadingError(Exception):
    """Raised when data loading fails."""
    pass


class DataManager:
    """
    Manages loading and organization of test data including videos, code samples,
    and ground truth annotations.
    """
    
    def __init__(self, tests_root: Optional[str] = None):
        """
        Initialize the data manager.
        
        Args:
            tests_root: Path to TESTS directory. If None, auto-detects.
        """
        if tests_root is None:
            # Auto-detect TESTS directory
            current_dir = Path(__file__).parent
            while current_dir.parent != current_dir:
                tests_dir = current_dir / "TESTS"
                if tests_dir.exists():
                    self.tests_root = tests_dir
                    break
                current_dir = current_dir.parent
            else:
                # Fallback: assume we're in TESTS/01-core-technical/framework/data
                self.tests_root = Path(__file__).parent.parent.parent.parent
        else:
            self.tests_root = Path(tests_root)
        
        self.core_technical_dir = self.tests_root / "01-core-technical"
        self.test_data_dir = self.core_technical_dir / "test-data"
        self.results_dir = self.core_technical_dir / "results"
        
        # Video folder is in project root (parent of TESTS)
        self.project_root = self.tests_root.parent
        self.video_folder = self.project_root / "video"
        
        # Ensure directories exist
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Ensure required directories exist."""
        directories = [
            self.test_data_dir / "ground-truth",
            self.test_data_dir / "code-samples",
            self.test_data_dir / "schemas",
            self.results_dir / "semantic-extraction",
            self.results_dir / "json-generation", 
            self.results_dir / "content-regeneration",
            self.results_dir / "code-extraction"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def load_test_content(self, test_type: str = "all") -> Dict[str, List[Any]]:
        """
        Load test content based on test type.
        
        Args:
            test_type: Type of test content to load ('video', 'code', 'all')
            
        Returns:
            Dictionary with 'videos' and 'code_samples' keys containing lists of test content
            
        Raises:
            DataLoadingError: If content loading fails
        """
        content = {
            'videos': [],
            'code_samples': []
        }
        
        if test_type in ('video', 'all'):
            content['videos'] = self._load_video_content()
        
        if test_type in ('code', 'all'):
            content['code_samples'] = self._load_code_content()
        
        return content
    
    def _load_video_content(self) -> List[VideoTestContent]:
        """
        Discover and load video content from the video folder with metadata extraction.
        
        Returns:
            List of VideoTestContent objects
            
        Raises:
            DataLoadingError: If video loading fails
        """
        if not self.video_folder.exists():
            raise DataLoadingError(f"Video folder not found: {self.video_folder}")
        
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.m4v'}
        video_files = [
            f for f in self.video_folder.iterdir()
            if f.is_file() and f.suffix.lower() in video_extensions
        ]
        
        if not video_files:
            raise DataLoadingError(f"No video files found in {self.video_folder}")
        
        video_content = []
        
        for video_file in video_files:
            try:
                # Extract metadata
                metadata = self._extract_video_metadata(video_file)
                
                # Determine genre and cultural context from filename
                genre, cultural_context = self._classify_video_content(video_file.name)
                
                # Load ground truth annotations if available
                ground_truth = self._load_video_ground_truth(video_file.stem)
                
                video_content.append(VideoTestContent(
                    file_path=str(video_file),
                    genre=genre,
                    duration=metadata['duration'],
                    cultural_context=cultural_context,
                    ground_truth_annotations=ground_truth
                ))
                
            except Exception as e:
                print(f"Warning: Failed to load video {video_file.name}: {e}")
                continue
        
        if not video_content:
            raise DataLoadingError("No valid video content could be loaded")
        
        return video_content
    
    def _extract_video_metadata(self, video_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from video file using OpenCV and ffprobe.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video metadata
        """
        metadata = {
            'duration': 0.0,
            'width': 0,
            'height': 0,
            'fps': 0.0,
            'has_audio': False,
            'file_size': 0,
            'estimated_cost': 0.0
        }
        
        try:
            # Get file size
            metadata['file_size'] = video_path.stat().st_size
            
            # Use OpenCV to get basic video properties if available
            if HAS_OPENCV:
                cap = cv2.VideoCapture(str(video_path))
                if cap.isOpened():
                    metadata['width'] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    metadata['height'] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    metadata['fps'] = cap.get(cv2.CAP_PROP_FPS)
                    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                    
                    if metadata['fps'] > 0:
                        metadata['duration'] = frame_count / metadata['fps']
                    
                    cap.release()
            else:
                # Fallback: estimate duration using ffprobe if available
                try:
                    result = subprocess.run([
                        'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', str(video_path)
                    ], capture_output=True, text=True, timeout=10)
                    
                    if result.stdout.strip():
                        metadata['duration'] = float(result.stdout.strip())
                except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
                    # Fallback: assume 2 minutes for cost estimation
                    metadata['duration'] = 120.0
            
            # Try to detect audio using ffprobe if available
            try:
                result = subprocess.run([
                    'ffprobe', '-v', 'quiet', '-show_streams', 
                    '-select_streams', 'a', '-of', 'csv=p=0', str(video_path)
                ], capture_output=True, text=True, timeout=10)
                
                metadata['has_audio'] = bool(result.stdout.strip())
            except (subprocess.TimeoutExpired, FileNotFoundError):
                # ffprobe not available or timeout, assume has audio
                metadata['has_audio'] = True
            
            # Estimate processing cost based on duration and resolution
            # Base cost: $0.04 per minute for GPT-4 Vision
            # Additional cost for high resolution
            base_cost_per_minute = 0.04
            duration_minutes = metadata['duration'] / 60.0
            resolution_multiplier = 1.0
            
            if metadata['width'] * metadata['height'] > 1920 * 1080:
                resolution_multiplier = 1.5  # 4K content costs more
            
            metadata['estimated_cost'] = duration_minutes * base_cost_per_minute * resolution_multiplier
            
        except Exception as e:
            print(f"Warning: Could not extract full metadata for {video_path.name}: {e}")
        
        return metadata
    
    def _classify_video_content(self, filename: str) -> Tuple[str, str]:
        """
        Classify video content based on filename to determine genre and cultural context.
        
        Args:
            filename: Video filename
            
        Returns:
            Tuple of (genre, cultural_context)
        """
        filename_lower = filename.lower()
        
        # Genre classification based on filename patterns
        if any(term in filename_lower for term in ['documentary', 'doc', 'educational']):
            genre = 'documentary'
        elif any(term in filename_lower for term in ['action', 'fight', 'battle', 'cyberpunk', 'hulk']):
            genre = 'action'
        elif any(term in filename_lower for term in ['comedy', 'funny', 'burnham', 'rant']):
            genre = 'comedy'
        elif any(term in filename_lower for term in ['drama', 'marty', 'heartache', 'breakup']):
            genre = 'drama'
        elif any(term in filename_lower for term in ['music', 'video', 'song', 'carpenter', 'wizzy']):
            genre = 'music_video'
        elif any(term in filename_lower for term in ['sci-fi', 'tron', 'legacy', 'grid']):
            genre = 'sci_fi'
        elif any(term in filename_lower for term in ['animation', 'animated', 'cartoon']):
            genre = 'animation'
        else:
            genre = 'general'
        
        # Cultural context classification
        if any(term in filename_lower for term in ['asian', 'mahjong', 'rich asians']):
            cultural_context = 'asian_american'
        elif any(term in filename_lower for term in ['american', 'netflix', 'burnham']):
            cultural_context = 'american'
        elif any(term in filename_lower for term in ['cyberpunk', 'futuristic']):
            cultural_context = 'futuristic'
        elif any(term in filename_lower for term in ['1955', 'classic', 'marty']):
            cultural_context = 'classic_american'
        elif any(term in filename_lower for term in ['tech', 'altman', 'ai']):
            cultural_context = 'tech_contemporary'
        else:
            cultural_context = 'contemporary'
        
        return genre, cultural_context
    
    def _load_video_ground_truth(self, video_stem: str) -> Dict[str, Any]:
        """
        Load ground truth annotations for a video if available.
        
        Args:
            video_stem: Video filename without extension
            
        Returns:
            Ground truth annotations dictionary
        """
        ground_truth_file = self.test_data_dir / "ground-truth" / f"{video_stem}.json"
        
        if ground_truth_file.exists():
            try:
                with open(ground_truth_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load ground truth for {video_stem}: {e}")
        
        # Return default structure if no ground truth available
        return {
            'micro_expressions': {},
            'body_language': {},
            'cultural_signals': {},
            'vocal_layers': {},
            'temporal_consistency': {},
            'character_descriptions': {},
            'scene_descriptions': {},
            'narrative_structure': {}
        }
    
    def _load_code_content(self) -> List[CodeTestContent]:
        """
        Discover and load code samples organized by language and complexity.
        
        Returns:
            List of CodeTestContent objects
            
        Raises:
            DataLoadingError: If code loading fails
        """
        code_samples_dir = self.test_data_dir / "code-samples"
        
        if not code_samples_dir.exists():
            print(f"Warning: Code samples directory not found: {code_samples_dir}")
            return []
        
        code_extensions = {
            '.py': 'python',
            '.js': 'javascript', 
            '.ts': 'typescript',
            '.java': 'java',
            '.go': 'go',
            '.cs': 'csharp',
            '.php': 'php',
            '.rb': 'ruby',
            '.cpp': 'cpp',
            '.c': 'c'
        }
        
        code_content = []
        
        # Walk through code samples directory
        for root, dirs, files in os.walk(code_samples_dir):
            root_path = Path(root)
            
            for file in files:
                file_path = root_path / file
                extension = file_path.suffix.lower()
                
                if extension in code_extensions:
                    try:
                        language = code_extensions[extension]
                        
                        # Determine complexity and business domain from path structure
                        relative_path = file_path.relative_to(code_samples_dir)
                        path_parts = relative_path.parts
                        
                        complexity_level = 'medium'  # default
                        business_domain = 'general'  # default
                        
                        # Extract complexity from path if structured as language/complexity/
                        if len(path_parts) >= 2:
                            if path_parts[1] in ['simple', 'medium', 'complex']:
                                complexity_level = path_parts[1]
                        
                        # Extract business domain from filename or path
                        filename_lower = file_path.stem.lower()
                        if any(term in filename_lower for term in ['ecommerce', 'shop', 'cart']):
                            business_domain = 'ecommerce'
                        elif any(term in filename_lower for term in ['finance', 'bank', 'payment']):
                            business_domain = 'finance'
                        elif any(term in filename_lower for term in ['user', 'auth', 'login']):
                            business_domain = 'authentication'
                        elif any(term in filename_lower for term in ['api', 'rest', 'service']):
                            business_domain = 'api'
                        elif any(term in filename_lower for term in ['data', 'database', 'model']):
                            business_domain = 'data_management'
                        
                        # Look for associated test suite
                        test_suite_path = self._find_test_suite(file_path, language)
                        
                        # Load ground truth semantics if available
                        ground_truth = self._load_code_ground_truth(file_path.stem, language)
                        
                        code_content.append(CodeTestContent(
                            file_path=str(file_path),
                            language=language,
                            complexity_level=complexity_level,
                            business_domain=business_domain,
                            test_suite_path=test_suite_path,
                            ground_truth_semantics=ground_truth
                        ))
                        
                    except Exception as e:
                        print(f"Warning: Failed to load code file {file_path}: {e}")
                        continue
        
        return code_content
    
    def _find_test_suite(self, code_file: Path, language: str) -> str:
        """
        Find associated test suite for a code file.
        
        Args:
            code_file: Path to code file
            language: Programming language
            
        Returns:
            Path to test suite file or empty string if not found
        """
        # Common test file patterns
        test_patterns = [
            f"test_{code_file.stem}",
            f"{code_file.stem}_test",
            f"{code_file.stem}.test",
            f"test{code_file.stem.capitalize()}"
        ]
        
        test_extensions = {
            'python': ['.py'],
            'javascript': ['.js', '.test.js', '.spec.js'],
            'typescript': ['.ts', '.test.ts', '.spec.ts'],
            'java': ['.java'],
            'go': ['_test.go'],
            'csharp': ['.cs'],
            'php': ['.php']
        }
        
        extensions = test_extensions.get(language, [code_file.suffix])
        
        # Look in same directory and test subdirectories
        search_dirs = [
            code_file.parent,
            code_file.parent / "test",
            code_file.parent / "tests",
            code_file.parent / "__tests__"
        ]
        
        for search_dir in search_dirs:
            if not search_dir.exists():
                continue
                
            for pattern in test_patterns:
                for ext in extensions:
                    test_file = search_dir / f"{pattern}{ext}"
                    if test_file.exists():
                        return str(test_file)
        
        return ""
    
    def _load_code_ground_truth(self, code_stem: str, language: str) -> Optional[Dict[str, Any]]:
        """
        Load ground truth semantic annotations for code if available.
        
        Args:
            code_stem: Code filename without extension
            language: Programming language
            
        Returns:
            Ground truth semantics dictionary or None
        """
        ground_truth_file = self.test_data_dir / "ground-truth" / f"{code_stem}_{language}.json"
        
        if ground_truth_file.exists():
            try:
                with open(ground_truth_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Warning: Could not load code ground truth for {code_stem}: {e}")
        
        return None
    
    def load_ground_truth_data(self, content_type: str = "all") -> Dict[str, Dict[str, Any]]:
        """
        Load reference annotations from test-data/ground-truth/ directory.
        
        Args:
            content_type: Type of ground truth to load ('video', 'code', 'all')
            
        Returns:
            Dictionary mapping content IDs to ground truth annotations
            
        Raises:
            DataLoadingError: If ground truth loading fails
        """
        ground_truth_dir = self.test_data_dir / "ground-truth"
        
        if not ground_truth_dir.exists():
            raise DataLoadingError(f"Ground truth directory not found: {ground_truth_dir}")
        
        ground_truth_data = {}
        
        for ground_truth_file in ground_truth_dir.iterdir():
            if not ground_truth_file.is_file() or ground_truth_file.suffix != '.json':
                continue
            
            try:
                # Determine content type from filename
                filename = ground_truth_file.stem
                is_code = any(lang in filename for lang in ['_python', '_javascript', '_java', '_go', '_csharp', '_php'])
                
                if content_type == 'video' and is_code:
                    continue
                elif content_type == 'code' and not is_code:
                    continue
                
                with open(ground_truth_file, 'r', encoding='utf-8') as f:
                    ground_truth_data[filename] = json.load(f)
                    
            except Exception as e:
                print(f"Warning: Could not load ground truth file {ground_truth_file.name}: {e}")
                continue
        
        return ground_truth_data
    
    def get_video_processing_cost_estimate(self, video_content: List[VideoTestContent]) -> float:
        """
        Calculate estimated processing cost for video content.
        
        Args:
            video_content: List of video test content
            
        Returns:
            Estimated total processing cost in USD
        """
        total_cost = 0.0
        
        for video in video_content:
            try:
                # Use duration from video object (already extracted)
                duration_minutes = video.duration / 60.0 if video.duration > 0 else 2.0
                
                # Base cost: $0.04 per minute for GPT-4 Vision
                # Additional models: Claude ($0.02/min), Whisper ($0.006/min)
                cost_per_minute = 0.04 + 0.02 + 0.006  # Total: $0.066/min
                video_cost = duration_minutes * cost_per_minute
                total_cost += video_cost
                    
            except Exception as e:
                print(f"Warning: Could not estimate cost for {video.file_path}: {e}")
                # Fallback: assume 2 minutes average
                total_cost += 2.0 * 0.066
        
        return total_cost
    
    def create_sample_ground_truth_files(self) -> None:
        """
        Create sample ground truth files for testing if they don't exist.
        This is useful for initial setup and testing.
        """
        ground_truth_dir = self.test_data_dir / "ground-truth"
        ground_truth_dir.mkdir(parents=True, exist_ok=True)
        
        # Sample video ground truth
        sample_video_gt = {
            "micro_expressions": {
                "timestamp_0_5": {
                    "facial_expressions": ["slight_smile", "raised_eyebrow"],
                    "confidence": 0.8
                }
            },
            "body_language": {
                "timestamp_0_5": {
                    "gestures": ["hand_wave", "open_posture"],
                    "confidence": 0.7
                }
            },
            "cultural_signals": {
                "cultural_markers": ["western_business_attire", "formal_setting"],
                "cultural_context": "professional_american"
            },
            "vocal_layers": {
                "tone": "confident",
                "pace": "moderate",
                "emotional_undertones": ["enthusiasm", "slight_nervousness"]
            },
            "temporal_consistency": {
                "character_appearance": 0.9,
                "scene_continuity": 0.85
            }
        }
        
        # Sample code ground truth
        sample_code_gt = {
            "algorithmic_intent": {
                "primary_algorithm": "user_authentication",
                "complexity": "medium",
                "business_rules": [
                    "password_must_be_8_chars_minimum",
                    "account_locks_after_3_failed_attempts"
                ]
            },
            "architectural_patterns": {
                "pattern_type": "mvc",
                "components": ["model", "view", "controller"],
                "dependencies": ["database", "session_manager"]
            },
            "functional_requirements": [
                "validate_user_credentials",
                "create_user_session",
                "handle_authentication_errors"
            ]
        }
        
        # Create sample files if they don't exist
        sample_video_file = ground_truth_dir / "sample_video.json"
        if not sample_video_file.exists():
            with open(sample_video_file, 'w', encoding='utf-8') as f:
                json.dump(sample_video_gt, f, indent=2)
        
        sample_code_file = ground_truth_dir / "sample_auth_python.json"
        if not sample_code_file.exists():
            with open(sample_code_file, 'w', encoding='utf-8') as f:
                json.dump(sample_code_gt, f, indent=2)
        
        print(f"Sample ground truth files created in {ground_truth_dir}")