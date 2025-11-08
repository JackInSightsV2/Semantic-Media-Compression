#!/usr/bin/env python3
"""Wrapper that runs the modular JSON structure test."""

from __future__ import annotations

import argparse
import sys

from testing_suite import TestRunner, load_config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Test 02: JSON Structure Generation")
    parser.parse_args(argv)

    runner = TestRunner(config=load_config())
    results = runner.run(["01", "02"])

    result = results[-1]
    print(f"{result.test_id} :: {result.summary}")
    return 0 if result.status.value != "failure" else 1


if __name__ == "__main__":
    sys.exit(main())
