"""
Configuration loading system for semantic compression testing framework.

This module handles loading configuration from environment variables (.env file)
and YAML configuration files with validation and environment variable substitution.
"""

import os
import yaml
from dataclasses import dataclass
from typing import Dict, List, Any, Optional
from pathlib import Path
from dotenv import load_dotenv


@dataclass
class TestConfig:
    """
    Configuration for test execution.
    
    Attributes:
        test_id: Unique identifier for the test run
        models_to_test: List of AI models to test
        budget_limit: Maximum budget for test execution (from TOTAL_BUDGET)
        quality_thresholds: Dictionary of quality thresholds for validation
        video_folder: Path to video files folder
        api_keys: Dictionary of API keys
        rate_limits: Dictionary of rate limits per model
    """
    test_id: str
    models_to_test: List[str]
    budget_limit: float
    quality_thresholds: Dict[str, float]
    video_folder: str
    api_keys: Dict[str, str]
    rate_limits: Dict[str, int]


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing."""
    pass


class ConfigLoader:
    """
    Loads and validates configuration from environment and YAML files.
    """
    
    def __init__(self, tests_root: Optional[str] = None):
        """
        Initialize the configuration loader.
        
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
        
        self.env_file = self.tests_root / ".env"
        self.config_dir = self.tests_root / "01-core-technical" / "config"
        
        # Load environment variables
        self._load_environment()
    
    def _load_environment(self) -> None:
        """Load environment variables from .env file."""
        if self.env_file.exists():
            load_dotenv(self.env_file)
        else:
            print(f"Warning: .env file not found at {self.env_file}")
    
    def _substitute_env_vars(self, value: Any) -> Any:
        """
        Recursively substitute environment variables in configuration values.
        
        Args:
            value: Configuration value that may contain ${VAR_NAME} patterns
            
        Returns:
            Value with environment variables substituted
        """
        if isinstance(value, str):
            # Replace ${VAR_NAME} patterns with environment variable values
            import re
            pattern = r'\$\{([^}]+)\}'
            
            def replace_var(match):
                var_name = match.group(1)
                return os.getenv(var_name, match.group(0))  # Keep original if not found
            
            return re.sub(pattern, replace_var, value)
        elif isinstance(value, dict):
            return {k: self._substitute_env_vars(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._substitute_env_vars(item) for item in value]
        else:
            return value
    
    def load_yaml_config(self, config_file: str) -> Dict[str, Any]:
        """
        Load and parse YAML configuration file with environment variable substitution.
        
        Args:
            config_file: Name of the configuration file (e.g., 'test_config.yaml')
            
        Returns:
            Parsed configuration dictionary
            
        Raises:
            ConfigurationError: If file doesn't exist or is invalid
        """
        config_path = self.config_dir / config_file
        
        if not config_path.exists():
            raise ConfigurationError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Substitute environment variables
            config = self._substitute_env_vars(config)
            
            return config
        except yaml.YAMLError as e:
            raise ConfigurationError(f"Invalid YAML in {config_file}: {e}")
        except Exception as e:
            raise ConfigurationError(f"Error loading {config_file}: {e}")
    
    def get_api_keys(self) -> Dict[str, str]:
        """
        Get API keys from environment variables.
        
        Returns:
            Dictionary of API keys
            
        Raises:
            ConfigurationError: If required API keys are missing
        """
        api_keys = {
            'openai': os.getenv('OPENAI_API_KEY'),
            'anthropic': os.getenv('ANTHROPIC_API_KEY'),
            'elevenlabs': os.getenv('ELEVENLABS_API_KEY')
        }
        
        # Check for missing keys
        missing_keys = [key for key, value in api_keys.items() if not value]
        if missing_keys:
            raise ConfigurationError(
                f"Missing required API keys: {', '.join(missing_keys)}. "
                f"Please set them in {self.env_file}"
            )
        
        return api_keys
    
    def get_budget_config(self) -> Dict[str, float]:
        """
        Get budget configuration from environment variables.
        
        Returns:
            Dictionary with budget limits
            
        Raises:
            ConfigurationError: If budget configuration is invalid
        """
        try:
            total_budget = float(os.getenv('TOTAL_BUDGET', '200.0'))
            per_test_budget = float(os.getenv('PER_TEST_BUDGET', '50.0'))
            warning_threshold = float(os.getenv('WARNING_THRESHOLD', '0.8'))
            
            if total_budget <= 0 or per_test_budget <= 0:
                raise ValueError("Budget values must be positive")
            
            if warning_threshold <= 0 or warning_threshold > 1:
                raise ValueError("Warning threshold must be between 0 and 1")
            
            return {
                'total_budget': total_budget,
                'per_test_budget': per_test_budget,
                'warning_threshold': warning_threshold
            }
        except ValueError as e:
            raise ConfigurationError(f"Invalid budget configuration: {e}")
    
    def validate_video_folder(self) -> str:
        """
        Validate that the video folder exists and contains expected files.
        
        Returns:
            Path to video folder
            
        Raises:
            ConfigurationError: If video folder is invalid
        """
        video_folder = os.getenv('VIDEO_FOLDER', 'video')
        
        # Convert to absolute path relative to project root
        if not os.path.isabs(video_folder):
            # Assume video folder is relative to project root (parent of TESTS)
            project_root = self.tests_root.parent
            video_path = project_root / video_folder
        else:
            video_path = Path(video_folder)
        
        if not video_path.exists():
            raise ConfigurationError(f"Video folder not found: {video_path}")
        
        if not video_path.is_dir():
            raise ConfigurationError(f"Video folder is not a directory: {video_path}")
        
        # Check for video files
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
        video_files = [
            f for f in video_path.iterdir() 
            if f.is_file() and f.suffix.lower() in video_extensions
        ]
        
        if not video_files:
            raise ConfigurationError(f"No video files found in {video_path}")
        
        return str(video_path)
    
    def create_test_config(self, test_id: str, test_type: str = "all") -> TestConfig:
        """
        Create a complete test configuration.
        
        Args:
            test_id: Unique identifier for the test run
            test_type: Type of test to configure
            
        Returns:
            Complete test configuration
            
        Raises:
            ConfigurationError: If configuration is invalid
        """
        # Load YAML configuration
        try:
            yaml_config = self.load_yaml_config('test_config.yaml')
        except ConfigurationError:
            # Use default configuration if file doesn't exist
            yaml_config = self._get_default_config()
        
        # Get environment-based configuration
        api_keys = self.get_api_keys()
        budget_config = self.get_budget_config()
        video_folder = self.validate_video_folder()
        
        # Extract test-specific configuration
        test_suites = yaml_config.get('test_suites', {})
        
        # Determine models to test based on test type
        models_to_test = []
        if test_type == "all" or test_type == "01":
            models_to_test.extend(test_suites.get('semantic_extraction', {}).get('models', ['gpt4_vision', 'claude_sonnet']))
        if test_type == "all" or test_type == "02":
            models_to_test.extend(test_suites.get('json_generation', {}).get('models', ['claude_sonnet']))
        if test_type == "all" or test_type == "03":
            models_to_test.extend(test_suites.get('content_regeneration', {}).get('models', ['dalle3']))
        if test_type == "all" or test_type == "04":
            models_to_test.extend(test_suites.get('code_extraction', {}).get('models', ['gpt4', 'claude_sonnet']))
        
        # Remove duplicates while preserving order
        models_to_test = list(dict.fromkeys(models_to_test))
        
        # Build quality thresholds
        quality_thresholds = {
            'accuracy_threshold': 0.75,
            'completeness_threshold': 0.85,
            'consistency_threshold': 0.80,
            'equivalence_threshold': 0.95
        }
        
        # Override with YAML configuration if available
        for suite_name, suite_config in test_suites.items():
            if 'accuracy_threshold' in suite_config:
                quality_thresholds['accuracy_threshold'] = suite_config['accuracy_threshold']
            if 'completeness_threshold' in suite_config:
                quality_thresholds['completeness_threshold'] = suite_config['completeness_threshold']
            if 'consistency_threshold' in suite_config:
                quality_thresholds['consistency_threshold'] = suite_config['consistency_threshold']
            if 'equivalence_threshold' in suite_config:
                quality_thresholds['equivalence_threshold'] = suite_config['equivalence_threshold']
        
        # Build rate limits
        rate_limits = {
            'gpt4_max_requests_per_minute': int(os.getenv('GPT4_MAX_REQUESTS_PER_MINUTE', '10')),
            'claude_max_requests_per_minute': int(os.getenv('CLAUDE_MAX_REQUESTS_PER_MINUTE', '15'))
        }
        
        return TestConfig(
            test_id=test_id,
            models_to_test=models_to_test,
            budget_limit=budget_config['per_test_budget'],
            quality_thresholds=quality_thresholds,
            video_folder=video_folder,
            api_keys=api_keys,
            rate_limits=rate_limits
        )
    
    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration when YAML file is not available.
        
        Returns:
            Default configuration dictionary
        """
        return {
            'test_suites': {
                'semantic_extraction': {
                    'enabled': True,
                    'models': ['gpt4_vision', 'claude_sonnet'],
                    'accuracy_threshold': 0.75
                },
                'json_generation': {
                    'enabled': True,
                    'models': ['claude_sonnet'],
                    'completeness_threshold': 0.85,
                    'compression_ratio_target': 500
                },
                'content_regeneration': {
                    'enabled': True,
                    'models': ['dalle3'],
                    'consistency_threshold': 0.80
                },
                'code_extraction': {
                    'enabled': True,
                    'models': ['gpt4', 'claude_sonnet'],
                    'equivalence_threshold': 0.95
                }
            }
        }
    
    def validate_configuration(self, config: TestConfig) -> List[str]:
        """
        Validate a test configuration and return any issues found.
        
        Args:
            config: Test configuration to validate
            
        Returns:
            List of validation issues (empty if valid)
        """
        issues = []
        
        # Validate test_id
        if not config.test_id or not isinstance(config.test_id, str):
            issues.append("test_id must be a non-empty string")
        
        # Validate models
        if not config.models_to_test:
            issues.append("models_to_test cannot be empty")
        
        valid_models = {'gpt4_vision', 'claude_sonnet', 'gpt4', 'dalle3', 'whisper', 'midjourney', 'stable_diffusion'}
        invalid_models = set(config.models_to_test) - valid_models
        if invalid_models:
            issues.append(f"Invalid models: {', '.join(invalid_models)}")
        
        # Validate budget
        if config.budget_limit <= 0:
            issues.append("budget_limit must be positive")
        
        # Validate thresholds
        for threshold_name, threshold_value in config.quality_thresholds.items():
            if not isinstance(threshold_value, (int, float)) or threshold_value < 0 or threshold_value > 1:
                issues.append(f"{threshold_name} must be a number between 0 and 1")
        
        # Validate video folder
        if not Path(config.video_folder).exists():
            issues.append(f"Video folder does not exist: {config.video_folder}")
        
        # Validate API keys
        required_keys = {'openai', 'anthropic'}
        missing_keys = required_keys - set(config.api_keys.keys())
        if missing_keys:
            issues.append(f"Missing API keys: {', '.join(missing_keys)}")
        
        return issues


def load_test_config(test_id: str, test_type: str = "all", tests_root: Optional[str] = None) -> TestConfig:
    """
    Convenience function to load a complete test configuration.
    
    Args:
        test_id: Unique identifier for the test run
        test_type: Type of test to configure
        tests_root: Path to TESTS directory (auto-detected if None)
        
    Returns:
        Complete test configuration
        
    Raises:
        ConfigurationError: If configuration is invalid
    """
    loader = ConfigLoader(tests_root)
    config = loader.create_test_config(test_id, test_type)
    
    # Validate configuration
    issues = loader.validate_configuration(config)
    if issues:
        raise ConfigurationError(f"Configuration validation failed:\n" + "\n".join(f"- {issue}" for issue in issues))
    
    return config