from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from benchmark_parsers import build_benchmark_result, load_json_fixture


def parse_fixture(input_dir: Path, lab_id: str) -> Dict[str, Any]:
    fixture = input_dir / "metrics.json"
    data = load_json_fixture(fixture)
    return build_benchmark_result(
        platform="flutter",
        lab_id=lab_id,
        fixture_metrics=data,
        fixture_paths=[fixture],
        parser_name="flutter_parser",
    )

