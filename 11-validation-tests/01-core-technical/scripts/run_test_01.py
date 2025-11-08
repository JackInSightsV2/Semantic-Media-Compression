#!/usr/bin/env python3
"""Wrapper that runs the modular semantic extraction test."""

from __future__ import annotations

import argparse
import sys

from testing_suite import TestRunner, load_config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Test 01: Semantic Extraction")
    args = parser.parse_args(argv)

    runner = TestRunner(config=load_config())
    results = runner.run(["01"])

    result = results[0]
    print(f"{result.test_id} :: {result.summary}")
    return 0 if result.status.value != "failure" else 1


if __name__ == "__main__":
    sys.exit(main())