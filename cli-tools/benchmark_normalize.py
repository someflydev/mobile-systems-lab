#!/usr/bin/env python3
"""Wrapper around mobile_systems_lab benchmark normalization command."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lab_id")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    cmd = [sys.executable, str(root / "cli-tools" / "mobile_systems_lab.py"), "benchmark", args.lab_id]
    raise SystemExit(subprocess.call(cmd))
