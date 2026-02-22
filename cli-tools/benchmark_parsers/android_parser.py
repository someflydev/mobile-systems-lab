from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from benchmark_parsers import build_benchmark_result, load_kv_fixture


def parse_fixture(input_dir: Path, lab_id: str) -> Dict[str, Any]:
    fixture = input_dir / "metrics.txt"
    data = load_kv_fixture(fixture)
    return build_benchmark_result(
        platform="kotlin_android",
        lab_id=lab_id,
        fixture_metrics=data,
        fixture_paths=[fixture],
        parser_name="android_parser",
    )

