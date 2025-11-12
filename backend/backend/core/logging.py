from __future__ import annotations

import logging
import sys
from typing import Any

import structlog

from .settings import AppSettings


def configure_logging(settings: AppSettings) -> None:
    """
    Configure structlog and standard logging according to settings.
    """

    shared_processors: list[structlog.types.Processor] = [
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    if settings.logging.json_logs:
        renderer: structlog.types.Processor = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            *shared_processors,
            renderer,
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, settings.logging.level)),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        level=getattr(logging, settings.logging.level),
        format="%(message)s",
        stream=sys.stdout,
    )


def get_logger(*args: Any, **kwargs: Any) -> structlog.BoundLogger:
    """
    Convenience wrapper to create a structlog logger.
    """

    return structlog.get_logger(*args, **kwargs)
