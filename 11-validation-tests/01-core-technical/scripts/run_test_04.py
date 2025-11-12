#!/usr/bin/env python3
"""Wrapper that runs the modular code semantics test."""

from __future__ import annotations

import argparse
import sys

from testing_suite import TestRunner, load_config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run Test 04: Code Semantic Extraction")
    parser.parse_args(argv)

    runner = TestRunner(config=load_config())
    results = runner.run(["01", "02", "03", "04"])

    result = results[-1]
    print(f"{result.test_id} :: {result.summary}")
    return 0 if result.status.value != "failure" else 1


if __name__ == "__main__":
    sys.exit(main())
