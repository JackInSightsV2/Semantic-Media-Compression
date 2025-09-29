"""
Base model abstract class for AI model integrations in semantic compression testing.

This module defines the abstract interface that all AI model implementations must follow,
ensuring consistent behavior across different model providers and types.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import time


@dataclass
class CostEstimate:
    """Cost estimation for model operations"""
    estimated_cost: float
    currency: str = "USD"
    operation_type: str = ""
    content_size: int = 0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


@dataclass
class ModelResponse:
    """Standard response format for all model operations"""
    success: bool
    data: Dict[str, Any]
    confidence_scores: Dict[str, float]
    processing_time: float
    actual_cost: float
    error_message: Optional[str] = None
    model_name: str = ""
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_requests_per_minute: int):
        self.max_requests = max_requests_per_minute
        self.requests = []
    
    def wait_if_needed(self):
        """Wait if rate limit would be exceeded"""
        now = time.time()
        # Remove requests older than 1 minute
        self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        if len(self.requests) >= self.max_requests:
            # Wait until the oldest request is more than 1 minute old
            sleep_time = 60 - (now - self.requests[0]) + 1
            if sleep_time > 0:
                time.sleep(sleep_time)
                # Clean up old requests after waiting
                now = time.time()
                self.requests = [req_time for req_time in self.requests if now - req_time < 60]
        
        self.requests.append(now)


class BaseModel(ABC):
    """
    Abstract base class for all AI model integrations.
    
    This class defines the standard interface that all model implementations must follow,
    including semantic extraction, content generation, and cost estimation capabilities.
    """
    
    def __init__(self, model_name: str, api_key: str, rate_limit: int = 10):
        """
        Initialize the base model.
        
        Args:
            model_name: Name identifier for the model
            api_key: API key for authentication
            rate_limit: Maximum requests per minute
        """
        self.model_name = model_name
        self.api_key = api_key
        self.rate_limiter = RateLimiter(rate_limit)
        self.total_cost = 0.0
        self.request_count = 0
    
    @abstractmethod
    def extract_semantics(self, content: Union[str, bytes, Any], **kwargs) -> ModelResponse:
        """
        Extract semantic information from content.
        
        This method should analyze the provided content and extract semantic information
        relevant to the semantic compression testing framework.
        
        Args:
            content: The content to analyze (video file path, image data, text, etc.)
            **kwargs: Additional parameters specific to the model
            
        Returns:
            ModelResponse containing extracted semantic data and metadata
        """
        pass
    
    @abstractmethod
    def generate_content(self, blueprint: Dict[str, Any], **kwargs) -> ModelResponse:
        """
        Generate content from semantic blueprint.
        
        This method should create new content based on semantic information,
        used for testing content regeneration capabilities.
        
        Args:
            blueprint: Semantic blueprint containing generation instructions
            **kwargs: Additional parameters specific to the model
            
        Returns:
            ModelResponse containing generated content and metadata
        """
        pass
    
    @abstractmethod
    def get_cost_estimate(self, content_size: int, operation_type: str = "extract") -> CostEstimate:
        """
        Estimate the cost of processing content.
        
        Args:
            content_size: Size of content to process (in bytes, tokens, etc.)
            operation_type: Type of operation ("extract", "generate", etc.)
            
        Returns:
            CostEstimate with estimated cost and details
        """
        pass
    
    def validate_api_key(self) -> bool:
        """
        Validate that the API key is properly configured.
        
        Returns:
            True if API key is valid, False otherwise
        """
        return bool(self.api_key and self.api_key.strip())
    
    def track_cost(self, actual_cost: float):
        """
        Track actual costs for budget monitoring.
        
        Args:
            actual_cost: The actual cost incurred for the operation
        """
        self.total_cost += actual_cost
        self.request_count += 1
    
    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics for the model.
        
        Returns:
            Dictionary containing usage statistics
        """
        return {
            "model_name": self.model_name,
            "total_cost": self.total_cost,
            "request_count": self.request_count,
            "average_cost_per_request": self.total_cost / max(1, self.request_count)
        }
    
    def reset_usage_stats(self):
        """Reset usage statistics."""
        self.total_cost = 0.0
        self.request_count = 0
    
    def _handle_rate_limiting(self):
        """Handle rate limiting before making API calls."""
        self.rate_limiter.wait_if_needed()
    
    def _create_error_response(self, error_message: str, processing_time: float = 0.0) -> ModelResponse:
        """
        Create a standardized error response.
        
        Args:
            error_message: Description of the error
            processing_time: Time spent processing before error
            
        Returns:
            ModelResponse indicating failure
        """
        return ModelResponse(
            success=False,
            data={},
            confidence_scores={},
            processing_time=processing_time,
            actual_cost=0.0,
            error_message=error_message,
            model_name=self.model_name
        )