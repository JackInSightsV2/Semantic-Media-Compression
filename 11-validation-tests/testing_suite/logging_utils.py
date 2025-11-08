"""Utility helpers for establishing verbose logging."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from .config import TestConfig


def configure_logging(config: TestConfig, run_name: str = "test_run") -> logging.Logger:
    """Configure and return a logger according to the suite configuration."""

    logger = logging.getLogger(f"testing_suite.{run_name}")
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, config.log_level, logging.INFO))

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    log_file = _prepare_log_file(config.output_dir, run_name)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False
    logger.debug("Logger configured (level=%s, log_file=%s)", config.log_level, log_file)
    return logger


def _prepare_log_file(output_dir: Path, run_name: str) -> Optional[Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    log_path = output_dir / f"{run_name}.log"
    try:
        log_path.touch(exist_ok=True)
    except OSError:
        return None
    return log_path
