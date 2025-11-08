#!/usr/bin/env python3
"""Entrypoint for the modular semantic compression testing suite."""

from __future__ import annotations

import argparse
import json
import sys

from testing_suite import TestRunner, load_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Semantic Compression Testing Suite (mock-friendly)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--test",
        nargs="+",
        choices=["01", "02", "03", "04", "all"],
        default=["all"],
        help="Specific test IDs to run.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available tests and exit.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON summary.",
    )
    parser.add_argument(
        "--provider",
        help="Model provider to use (overrides TEST_SUITE_PROVIDER).",
    )
    parser.add_argument(
        "--prompt-set",
        dest="prompt_set",
        help="Prompt set to load (overrides TEST_SUITE_PROMPT_SET).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    config = load_config(
        provider_override=args.provider,
        prompt_set_override=args.prompt_set,
    )
    runner = TestRunner(config=config)

    if args.list:
        print("Available tests:", ", ".join(runner.available_tests()))
        return 0

    test_ids = args.test
    if "all" in test_ids:
        selected = runner.available_tests()
    else:
        selected = test_ids

    results = runner.run(selected)

    if args.json:
        serialisable = [
            {
                "test_id": result.test_id,
                "name": result.name,
                "status": result.status.value,
                "summary": result.summary,
                "metrics": result.metrics,
            }
            for result in results
        ]
        print(json.dumps(serialisable, indent=2))

    failures = [result for result in results if result.status.value == "failure"]
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())