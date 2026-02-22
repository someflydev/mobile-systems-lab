"""Fixture parsers for benchmark result generation.

These parsers intentionally stay simple and pure:
- input fixture files (text/json) -> schema-shaped BENCHMARK_RESULT dict
"""

from __future__ import annotations

import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List


def now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def benchmark_id() -> str:
    return f"bench_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"


def percentile(values: List[float], p: float) -> float:
    if not values:
        return 0.0
    vals = sorted(values)
    if len(vals) == 1:
        return float(vals[0])
    k = (len(vals) - 1) * p
    f = int(k)
    c = min(f + 1, len(vals) - 1)
    if f == c:
        return float(vals[f])
    return float(vals[f] + (k - f) * (vals[c] - vals[f]))


def median(values: Iterable[float]) -> float:
    seq = list(values)
    return float(statistics.median(seq)) if seq else 0.0


def load_json_fixture(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_kv_fixture(path: Path) -> Dict[str, Any]:
    data: Dict[str, Any] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = _coerce_value(value.strip())
    return data


def _coerce_value(value: str) -> Any:
    if "," in value:
        return [_coerce_scalar(v.strip()) for v in value.split(",")]
    return _coerce_scalar(value)


def _coerce_scalar(value: str) -> Any:
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def ensure_list_floats(value: Any) -> List[float]:
    if isinstance(value, list):
        return [float(v) for v in value]
    return [float(value)]


def build_benchmark_result(
    *,
    platform: str,
    lab_id: str,
    fixture_metrics: Dict[str, Any],
    fixture_paths: List[Path],
    parser_name: str,
    provenance: str = "parsed_fixture",
) -> Dict[str, Any]:
    cold = ensure_list_floats(fixture_metrics["cold_start_ms_samples"])
    warm = ensure_list_floats(fixture_metrics["warm_start_ms_samples"])
    mem_idle = ensure_list_floats(fixture_metrics["memory_idle_mb_samples"])
    mem_stream = ensure_list_floats(fixture_metrics["memory_sensor_stream_mb_samples"])
    cpu_idle = ensure_list_floats(fixture_metrics["cpu_idle_pct_samples"])
    cpu_accel = ensure_list_floats(fixture_metrics["cpu_accel_pct_samples"])
    cpu_gps = ensure_list_floats(fixture_metrics["cpu_gps_pct_samples"])
    cfg = ensure_list_floats(fixture_metrics["config_load_latency_ms_samples"])
    accel_eps = ensure_list_floats(fixture_metrics["accelerometer_events_per_sec"])
    gps_epm = ensure_list_floats(fixture_metrics["gps_events_per_min"])

    frame_total = int(fixture_metrics["frame_total"])
    frame_jank = int(fixture_metrics["frame_jank"])
    attempts = int(fixture_metrics["background_attempts"])
    resumes = int(fixture_metrics["background_successful_resumes"])

    os_name = "ios" if platform == "swift_ios" else "android"
    payload = {
        "schema_version": "benchmark_result.v1",
        "benchmark_id": benchmark_id(),
        "lab_id": lab_id,
        "platform": platform,
        "timestamp_utc": now_utc(),
        "run_context": {
            "device_id": str(fixture_metrics.get("device_id", "fixture-device")),
            "device_model": str(fixture_metrics.get("device_model", "fixture-model")),
            "device_class": str(fixture_metrics.get("device_class", "mid")),
            "os_name": os_name,
            "os_version": str(fixture_metrics.get("os_version", "fixture-os")),
            "build_type": str(fixture_metrics.get("build_type", "debug")),
            "thermal_state": str(fixture_metrics.get("thermal_state", "nominal")),
            "battery_pct_start": int(fixture_metrics.get("battery_pct_start", 80)),
            "battery_pct_end": int(fixture_metrics.get("battery_pct_end", 79)),
        },
        "protocol": {
            "cold_start_runs": int(fixture_metrics.get("cold_start_runs", len(cold))),
            "warm_start_runs": int(fixture_metrics.get("warm_start_runs", len(warm))),
            "sensor_stream_duration_sec": int(fixture_metrics.get("sensor_stream_duration_sec", 300)),
            "idle_window_sec": int(fixture_metrics.get("idle_window_sec", 120)),
            "sample_interval_ms": int(fixture_metrics.get("sample_interval_ms", 1000)),
            "gps_enabled": bool(fixture_metrics.get("gps_enabled", True)),
            "accelerometer_enabled": bool(fixture_metrics.get("accelerometer_enabled", True)),
            "background_window_sec": int(fixture_metrics.get("background_window_sec", 120)),
        },
        "metrics": {
            "cold_start_ms_samples": cold,
            "warm_start_ms_samples": warm,
            "memory_idle_mb_samples": mem_idle,
            "memory_sensor_stream_mb_samples": mem_stream,
            "cpu_idle_pct_samples": cpu_idle,
            "cpu_accel_pct_samples": cpu_accel,
            "cpu_gps_pct_samples": cpu_gps,
            "frame_jank": {
                "total_frames": frame_total,
                "jank_frames": frame_jank,
                "jank_rate_pct": (frame_jank / frame_total * 100.0) if frame_total else 0.0,
                "frame_time_p95_ms": float(fixture_metrics["frame_time_p95_ms"]),
            },
            "sensor_throughput": {
                "accelerometer_events_per_sec": accel_eps,
                "gps_events_per_min": gps_epm,
            },
            "battery": {
                "estimated_drain_pct_per_hour": float(fixture_metrics["estimated_drain_pct_per_hour"]),
                "delta_pct_during_run": int(fixture_metrics["battery_delta_pct_during_run"]),
            },
            "background_execution": {
                "attempts": attempts,
                "successful_resumes": resumes,
                "reliability_pct": (resumes / attempts * 100.0) if attempts else 0.0,
            },
            "config_load_latency_ms_samples": cfg,
        },
        "tooling": {
            "collector_version": f"{provenance}.v1",
            "commands_executed": [f"provenance:{provenance}", f"fixture_parser:{parser_name}"],
            "log_artifacts": [str(p) for p in fixture_paths],
        },
        "summary": {
            "cold_start_ms_p50": median(cold),
            "cold_start_ms_p95": percentile(cold, 0.95),
            "warm_start_ms_p50": median(warm),
            "memory_idle_mb_p50": median(mem_idle),
            "memory_streaming_mb_p50": median(mem_stream),
            "cpu_idle_pct_p50": median(cpu_idle),
            "cpu_accel_pct_p50": median(cpu_accel),
            "cpu_gps_pct_p50": median(cpu_gps),
            "config_load_ms_p50": median(cfg),
        },
    }
    return payload

