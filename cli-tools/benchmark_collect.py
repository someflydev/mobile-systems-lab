#!/usr/bin/env python3
"""Collect parsed fixture logs into BENCHMARK_RESULT JSON.

This is a CI-safe collector that parses representative fixture exports instead of
requiring attached devices.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from benchmark_parsers import android_parser, flutter_parser, ios_parser, react_native_parser


PARSER_MAP = {
    "kotlin_android": android_parser.parse_fixture,
    "swift_ios": ios_parser.parse_fixture,
    "flutter": flutter_parser.parse_fixture,
    "react_native": react_native_parser.parse_fixture,
}


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab-id", required=True)
    parser.add_argument(
        "--platform", required=True, choices=["kotlin_android", "swift_ios", "flutter", "react_native"]
    )
    parser.add_argument("--input", required=True, help="Fixture directory for the selected platform")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    input_dir = Path(args.input)
    if not input_dir.exists():
        raise SystemExit(f"input fixture path does not exist: {input_dir}")

    payload = PARSER_MAP[args.platform](input_dir, args.lab_id)
    write_json(Path(args.out), payload)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
