"""Custom exceptions for the semantic distillation pipeline."""

from typing import Dict, Any, Optional


class PipelineError(Exception):
    """Base exception for pipeline errors."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize pipeline error.
        
        Args:
            message: Error message
            context: Additional context dictionary
        """
        self.message = message
        self.context = context or {}
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """String representation with context."""
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.message} (Context: {context_str})"
        return self.message


class LLMAPIError(PipelineError):
    """LLM API related errors."""
    pass


class ValidationError(PipelineError):
    """Schema validation errors."""
    pass


class FileProcessingError(PipelineError):
    """File I/O and processing errors."""
    pass


class ConfigurationError(PipelineError):
    """Configuration and setup errors."""
    pass


class SchemaError(PipelineError):
    """Schema loading and parsing errors."""
    pass


class ChunkingError(PipelineError):
    """Text chunking errors."""
    pass

