"""Logging service for tracking token usage and response times."""

import time
from typing import Dict, Any, Optional, List
from datetime import datetime


class LoggingService:
    """Service for tracking API metrics and LLM usage."""
    
    def __init__(self):
        self.metrics: Dict[str, Any] = {
            "total_tokens": 0,
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_cost": 0.0,
            "response_times": [],
            "llm_calls": []
        }
    
    def start_timer(self) -> float:
        """Start a timer and return the start time."""
        return time.time()
    
    def record_response_time(self, start_time: float) -> float:
        """Record response time and return elapsed time in milliseconds."""
        elapsed = (time.time() - start_time) * 1000  # Convert to milliseconds
        self.metrics["response_times"].append(elapsed)
        return elapsed
    
    def record_llm_call(
        self,
        response: Dict[str, Any],
        response_time_ms: float,
        cost_per_1k_tokens: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Record an LLM API call with token usage and timing.
        
        Args:
            response: The API response dictionary
            response_time_ms: Response time in milliseconds
            cost_per_1k_tokens: Optional cost per 1K tokens for cost calculation
        
        Returns:
            Dictionary with extracted metrics
        """
        usage = response.get("usage", {})
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        total_tokens = usage.get("total_tokens", prompt_tokens + completion_tokens)
        
        # Calculate cost if rate provided
        cost = 0.0
        if cost_per_1k_tokens and total_tokens > 0:
            cost = (total_tokens / 1000.0) * cost_per_1k_tokens
        
        call_metrics = {
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost": cost,
            "response_time_ms": response_time_ms,
            "timestamp": datetime.now().isoformat()
        }
        
        # Update totals
        self.metrics["total_tokens"] += total_tokens
        self.metrics["total_prompt_tokens"] += prompt_tokens
        self.metrics["total_completion_tokens"] += completion_tokens
        self.metrics["total_cost"] += cost
        self.metrics["llm_calls"].append(call_metrics)
        
        return call_metrics
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics summary."""
        response_times = self.metrics["response_times"]
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        return {
            "total_tokens": self.metrics["total_tokens"],
            "total_prompt_tokens": self.metrics["total_prompt_tokens"],
            "total_completion_tokens": self.metrics["total_completion_tokens"],
            "total_cost": round(self.metrics["total_cost"], 4),
            "total_llm_calls": len(self.metrics["llm_calls"]),
            "average_response_time_ms": round(avg_response_time, 2),
            "min_response_time_ms": round(min(response_times), 2) if response_times else 0,
            "max_response_time_ms": round(max(response_times), 2) if response_times else 0,
            "response_times": response_times.copy()  # Include full list of response times
        }
    
    def reset(self):
        """Reset all metrics."""
        self.metrics = {
            "total_tokens": 0,
            "total_prompt_tokens": 0,
            "total_completion_tokens": 0,
            "total_cost": 0.0,
            "response_times": [],
            "llm_calls": []
        }

