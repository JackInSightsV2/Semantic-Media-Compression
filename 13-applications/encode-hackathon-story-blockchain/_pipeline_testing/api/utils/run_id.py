"""Run ID generation and validation utilities."""

import uuid
from typing import Optional


def generate_run_id() -> str:
    """Generate a UUID-based run ID."""
    return str(uuid.uuid4())


def validate_run_id(run_id: str) -> bool:
    """Validate that a run ID is a valid UUID."""
    try:
        uuid.UUID(run_id)
        return True
    except (ValueError, TypeError):
        return False

