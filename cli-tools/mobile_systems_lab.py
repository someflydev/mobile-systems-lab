#!/usr/bin/env python3
"""Minimal mobile-systems-lab CLI.

Commands:
  generate <spec.json> [--dry-run] [--force]
  compare <LAB_ID>
  benchmark <LAB_ID>
  mutate <LAB_ID> --spec <spec.json> [--sensor-add=<sensor>] [--sensor-remove=<sensor>]
"""

from __future__ import annotations

import argparse
import json
import os
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES_ROOT = REPO_ROOT / "templates"
CONTRACTS_ROOT = REPO_ROOT / "artifacts" / "contracts"
REPORTS_ROOT = REPO_ROOT / "artifacts" / "reports"
BENCH_RESULTS_ROOT = REPO_ROOT / "artifacts" / "benchmark" / "results"

PLATFORMS = {
    "kotlin": REPO_ROOT / "kotlin-android" / "labs",
    "swift": REPO_ROOT / "swift-ios" / "labs",
    "flutter": REPO_ROOT / "flutter" / "labs",
    "react-native": REPO_ROOT / "react-native" / "labs",
}


def load_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def percentile(values: List[float], p: float) -> float:
    if not values:
        return 0.0
    sorted_vals = sorted(values)
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])
    k = (len(sorted_vals) - 1) * p
    f = int(k)
    c = min(f + 1, len(sorted_vals) - 1)
    if f == c:
        return float(sorted_vals[f])
    return float(sorted_vals[f] + (k - f) * (sorted_vals[c] - sorted_vals[f]))


def ensure_v2_required(spec: Dict[str, Any]) -> None:
    required = [
        "schema_version",
        "lab_id",
        "title",
        "difficulty_level",
        "canonical_features_used",
        "sensors_used",
        "storage_used",
        "state_complexity_level",
        "state_model_type",
        "async_complexity",
        "expected_runtime_constraints",
        "config_schema_version",
        "ui_components_required",
        "background_processing_required",
        "performance_goal",
        "performance_budget",
        "expected_permissions",
        "device_constraints",
    ]
    missing = [k for k in required if k not in spec]
    if missing:
        raise ValueError(f"LAB_SPEC.v2 missing required keys: {', '.join(missing)}")


def render_template(content: str, replacements: Dict[str, str]) -> str:
    rendered = content
    for key, value in replacements.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def platform_specific_replacements(spec: Dict[str, Any], mapping: Dict[str, Any], platform: str) -> Dict[str, str]:
    platform_key_map = {
        "kotlin": "kotlin_android",
        "swift": "swift_ios",
        "flutter": "flutter",
        "react-native": "react_native",
    }
    map_key = platform_key_map[platform]

    state_type = spec["state_model_type"]
    state_map = mapping["state_model_type_mapping"][state_type][map_key]

    sensor_lines = []
    for sensor in spec.get("sensors_used", []):
        sensor_entry = mapping["sensor_subscription_mapping"].get(sensor)
        if sensor_entry:
            sensor_lines.append(f"- {sensor}: {sensor_entry[map_key]}")
    if not sensor_lines:
        sensor_lines = ["- no sensor subscriptions"]

    permission_lines = []
    for perm in spec.get("expected_permissions", []):
        perm_entry = mapping["permission_mapping"].get(perm)
        if perm_entry:
            permission_lines.append(f"- {perm}: {perm_entry[map_key]}")
    if not permission_lines:
        permission_lines = ["- no runtime permission requests"]

    ui_components = ", ".join(spec.get("ui_components_required", []))
    background_block = (
        "background behavior enabled and bounded by platform policy"
        if spec.get("background_processing_required")
        else "no background processing in this lab"
    )

    config_default = {
        "schema_version": spec.get("config_schema_version", "config.v1"),
        "lab_id": spec["lab_id"],
        "feature_flags": {
            "accelerometer_enabled": "accelerometer" in spec.get("sensors_used", []),
            "gps_enabled": "gps" in spec.get("sensors_used", []),
            "dark_mode": False,
            "log_sensor_data": True,
        },
    }

    return {
        "LAB_ID": spec["lab_id"],
        "APP_TITLE": spec["title"],
        "KOTLIN_PACKAGE": f"com.mobilelab.{spec['lab_id'].lower()}",
        "STATE_MODEL": state_map,
        "SENSOR_SUBSCRIPTION": "\\n".join(sensor_lines),
        "PERMISSION_REQUEST": "\\n".join(permission_lines),
        "CONFIG_LOAD": mapping["config_loader_snippet"][map_key],
        "CONFIG_SAVE": mapping["config_save_snippet"][map_key],
        "UI_COMPONENTS": ui_components,
        "BACKGROUND_BLOCK": background_block,
        "CONFIG_DEFAULT_JSON": json.dumps(config_default, indent=2),
    }


def command_generate(args: argparse.Namespace) -> int:
    spec_path = Path(args.spec).resolve()
    spec = load_json(spec_path)
    ensure_v2_required(spec)

    mapping = load_json(CONTRACTS_ROOT / "CANONICAL_MAPPING.json")
    lab_id = spec["lab_id"]

    for platform, out_root in PLATFORMS.items():
        template_root = TEMPLATES_ROOT / platform
        target_root = out_root / lab_id
        if target_root.exists() and not args.force:
            raise RuntimeError(
                f"Target exists: {target_root}. Use --force to overwrite templates in-place."
            )
        replacements = platform_specific_replacements(spec, mapping, platform)

        if args.dry_run:
            print(f"[dry-run] {platform}: would render templates -> {target_root}")
            continue

        target_root.mkdir(parents=True, exist_ok=True)
        for tpl in template_root.glob("*.tpl"):
            out_name = tpl.name[:-4]
            out_path = target_root / out_name
            rendered = render_template(tpl.read_text(encoding="utf-8"), replacements)
            out_path.write_text(rendered, encoding="utf-8")

        readme = target_root / "README.generated.md"
        readme.write_text(
            f"# {lab_id} ({platform}) generated scaffold\\n\\nGenerated from {spec_path} at {datetime.now().isoformat()}\\n",
            encoding="utf-8",
        )

    if not args.dry_run:
        REPORTS_ROOT.mkdir(parents=True, exist_ok=True)
        report_path = REPORTS_ROOT / f"{lab_id}-comparison.md"
        report_path.write_text(
            f"# {lab_id} Comparison Report (Generated Stub)\\n\\nGenerated at {datetime.now().isoformat()}\\n",
            encoding="utf-8",
        )
        print(f"Generated scaffold + report: {report_path}")
    return 0


def command_compare(args: argparse.Namespace) -> int:
    lab_id = args.lab_id
    print(f"LAB compare: {lab_id}")
    missing = []
    for platform, root in PLATFORMS.items():
        path = root / lab_id
        exists = path.exists()
        files = len(list(path.rglob("*"))) if exists else 0
        print(f"- {platform:12} exists={exists} files={files}")
        if not exists:
            missing.append(platform)

    if missing:
        print("Missing platforms:", ", ".join(missing))
        return 1
    return 0


def normalize_results(lab_id: str) -> Dict[str, Any]:
    platform_files: Dict[str, List[Path]] = {
        "kotlin_android": [],
        "swift_ios": [],
        "flutter": [],
        "react_native": [],
    }
    for platform in platform_files:
        platform_dir = BENCH_RESULTS_ROOT / platform / lab_id
        if platform_dir.exists():
            platform_files[platform] = sorted(platform_dir.glob("*.json"))

    platform_metrics = []
    for platform, files in platform_files.items():
        if not files:
            continue
        samples = [load_json(p) for p in files]

        cold = [float(s["summary"]["cold_start_ms_p95"]) for s in samples]
        warm = [float(s["summary"]["warm_start_ms_p50"]) for s in samples]
        mem_idle = [float(s["summary"]["memory_idle_mb_p50"]) for s in samples]
        mem_stream = [float(s["summary"]["memory_streaming_mb_p50"]) for s in samples]
        cpu_idle = [float(s["summary"]["cpu_idle_pct_p50"]) for s in samples]
        cpu_accel = [float(s["summary"]["cpu_accel_pct_p50"]) for s in samples]
        cpu_gps = [float(s["summary"]["cpu_gps_pct_p50"]) for s in samples]
        cfg = [float(s["summary"]["config_load_ms_p50"]) for s in samples]

        platform_metrics.append(
            {
                "platform": platform,
                "cold_start_ms_p95": percentile(cold, 0.95),
                "warm_start_ms_p95": percentile(warm, 0.95),
                "memory_idle_mb_p95": percentile(mem_idle, 0.95),
                "memory_streaming_mb_p95": percentile(mem_stream, 0.95),
                "cpu_idle_pct_p95": percentile(cpu_idle, 0.95),
                "cpu_accel_pct_p95": percentile(cpu_accel, 0.95),
                "cpu_gps_pct_p95": percentile(cpu_gps, 0.95),
                "jank_rate_pct": 0.0,
                "frame_time_p95_ms": 16.67,
                "accel_throughput_eps_p50": 0.0,
                "gps_throughput_epm_p50": 0.0,
                "battery_drain_pct_per_hour": 0.0,
                "background_reliability_pct": 100.0,
                "config_load_ms_p95": percentile(cfg, 0.95),
                "score": 0.0,
            }
        )

    def best(metric: str, lower_is_better: bool = True) -> Dict[str, Any]:
        if not platform_metrics:
            return {"platform": "kotlin_android", "value": 0.0}
        sorted_items = sorted(platform_metrics, key=lambda x: x[metric], reverse=not lower_is_better)
        return {"platform": sorted_items[0]["platform"], "value": sorted_items[0][metric]}

    ranked = sorted(platform_metrics, key=lambda x: x["cold_start_ms_p95"])

    return {
        "schema_version": "unified_metrics.v1",
        "benchmark_id": f"bench_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "lab_id": lab_id,
        "scenario": "combined_sensors",
        "normalization_context": {
            "device_class": "mid",
            "os_version_locked": True,
            "build_type": "debug",
            "sample_window_sec": 300,
            "winsorization_pct": 5,
            "unit_conventions": {
                "time": "ms",
                "memory": "MB",
                "cpu": "pct",
                "throughput_accel": "events_per_sec",
                "throughput_gps": "events_per_min",
                "battery": "pct_per_hour",
            },
        },
        "platform_metrics": platform_metrics,
        "comparative_summary": {
            "best_cold_start": best("cold_start_ms_p95", True),
            "best_memory_idle": best("memory_idle_mb_p95", True),
            "best_frame_stability": best("frame_time_p95_ms", True),
            "best_battery": best("battery_drain_pct_per_hour", True),
            "best_background_reliability": best("background_reliability_pct", False),
            "overall_rank": [
                {"platform": x["platform"], "value": x["cold_start_ms_p95"]} for x in ranked
            ],
        },
        "regression_alerts": [],
    }


def command_benchmark(args: argparse.Namespace) -> int:
    lab_id = args.lab_id
    unified = normalize_results(lab_id)
    out_path = BENCH_RESULTS_ROOT / "unified" / lab_id / f"{unified['benchmark_id']}.UNIFIED_METRICS.json"
    write_json(out_path, unified)
    print(f"Wrote unified metrics: {out_path}")
    if not unified["platform_metrics"]:
        print("No per-platform BENCHMARK_RESULT files found. Added empty unified shell.")
        return 1
    return 0


def command_mutate(args: argparse.Namespace) -> int:
    if not args.spec:
        raise RuntimeError("mutate requires --spec <path>")
    spec_path = Path(args.spec).resolve()
    spec = load_json(spec_path)
    if spec.get("lab_id") != args.lab_id:
        raise RuntimeError(f"spec lab_id ({spec.get('lab_id')}) does not match CLI lab_id ({args.lab_id})")

    sensors = list(spec.get("sensors_used", []))
    if args.sensor_add and args.sensor_add not in sensors:
        sensors.append(args.sensor_add)
    if args.sensor_remove and args.sensor_remove in sensors:
        sensors.remove(args.sensor_remove)
    spec["sensors_used"] = sensors or ["none"]

    out_path = spec_path.with_name(spec_path.stem + ".mutated.json")
    write_json(out_path, spec)
    print(f"Wrote mutated spec: {out_path}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mobile-systems-lab")
    sub = p.add_subparsers(dest="command", required=True)

    g = sub.add_parser("generate", help="Generate multi-platform scaffold from LAB_SPEC.v2")
    g.add_argument("spec")
    g.add_argument("--dry-run", action="store_true")
    g.add_argument("--force", action="store_true")
    g.set_defaults(func=command_generate)

    c = sub.add_parser("compare", help="Check whether a lab exists in all platform directories")
    c.add_argument("lab_id")
    c.set_defaults(func=command_compare)

    b = sub.add_parser("benchmark", help="Normalize benchmark results into UNIFIED_METRICS")
    b.add_argument("lab_id")
    b.set_defaults(func=command_benchmark)

    m = sub.add_parser("mutate", help="Mutate a LAB_SPEC with simple sensor add/remove operations")
    m.add_argument("lab_id")
    m.add_argument("--spec", required=False)
    m.add_argument("--sensor-add", dest="sensor_add")
    m.add_argument("--sensor-remove", dest="sensor_remove")
    m.set_defaults(func=command_mutate)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except Exception as exc:  # pragma: no cover
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
