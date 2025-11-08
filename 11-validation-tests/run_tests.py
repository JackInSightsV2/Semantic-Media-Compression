#!/usr/bin/env python3
"""Entrypoint for the modular semantic compression testing suite."""

from __future__ import annotations

import argparse
import json
import sys
from typing import List

from testing_suite import TestRunner, load_config
from testing_suite.models import PROVIDERS
from testing_suite.prompts import PROMPT_SETS


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
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Choose provider, prompt set, and tests interactively.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.interactive:
        provider = _choose_option("provider", sorted(PROVIDERS.keys()), args.provider or "mock")
        prompt_set = _choose_option("prompt set", sorted(PROMPT_SETS.keys()), args.prompt_set or "default")
        test_ids = _choose_tests()
    else:
        provider = args.provider
        prompt_set = args.prompt_set
        test_ids = args.test

    config = load_config(
        provider_override=provider,
        prompt_set_override=prompt_set,
    )
    runner = TestRunner(config=config)

    if args.list and not args.interactive:
        print("Available tests:", ", ".join(runner.available_tests()))
        return 0

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


def _choose_option(label: str, options: List[str], default: str) -> str:
    print(f"Choose {label}:")
    for idx, option in enumerate(options, start=1):
        marker = " (default)" if option == default else ""
        print(f"  {idx}. {option}{marker}")
    while True:
        try:
            choice = input(f"Enter number [default {default}]: ").strip()
        except EOFError:
            print("\nNo input detected, using default.")
            return default
        if not choice:
            return default
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        print("Invalid selection, please try again.")


def _choose_tests() -> List[str]:
    print("Available tests: 01, 02, 03, 04, or 'all'.")
    while True:
        try:
            choice = input("Enter comma-separated test IDs [default all]: ").strip()
        except EOFError:
            print("\nNo input detected, running all tests.")
            return ["all"]
        if not choice or choice.lower() == "all":
            return ["all"]
        selected = [token.strip() for token in choice.split(",") if token.strip()]
        if selected:
            return selected
        print("Please enter at least one test ID or 'all'.")


if __name__ == "__main__":
    sys.exit(main())