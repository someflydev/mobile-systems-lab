#!/usr/bin/env python3
"""Create a schema-shaped BENCHMARK_RESULT stub for manual or scripted filling."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lab-id", required=True)
    parser.add_argument("--platform", required=True, choices=["kotlin_android", "swift_ios", "flutter", "react_native"])
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = {
        "schema_version": "benchmark_result.v1",
        "benchmark_id": f"bench_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}",
        "lab_id": args.lab_id,
        "platform": args.platform,
        "timestamp_utc": now,
        "run_context": {
            "device_id": "unknown",
            "device_model": "unknown",
            "device_class": "mid",
            "os_name": "android" if args.platform in {"kotlin_android", "flutter", "react_native"} else "ios",
            "os_version": "unknown",
            "build_type": "debug",
            "thermal_state": "unknown",
            "battery_pct_start": 80,
            "battery_pct_end": 79,
        },
        "protocol": {
            "cold_start_runs": 7,
            "warm_start_runs": 7,
            "sensor_stream_duration_sec": 300,
            "idle_window_sec": 120,
            "sample_interval_ms": 1000,
            "gps_enabled": True,
            "accelerometer_enabled": True,
            "background_window_sec": 120,
        },
        "metrics": {
            "cold_start_ms_samples": [1400, 1500],
            "warm_start_ms_samples": [550, 600],
            "memory_idle_mb_samples": [150, 152],
            "memory_sensor_stream_mb_samples": [175, 180],
            "cpu_idle_pct_samples": [5, 6],
            "cpu_accel_pct_samples": [8, 9],
            "cpu_gps_pct_samples": [12, 13],
            "frame_jank": {
                "total_frames": 5000,
                "jank_frames": 50,
                "jank_rate_pct": 1,
                "frame_time_p95_ms": 16.67,
            },
            "sensor_throughput": {
                "accelerometer_events_per_sec": [5, 5],
                "gps_events_per_min": [12, 12],
            },
            "battery": {
                "estimated_drain_pct_per_hour": 24,
                "delta_pct_during_run": 1,
            },
            "background_execution": {
                "attempts": 10,
                "successful_resumes": 10,
                "reliability_pct": 100,
            },
            "config_load_latency_ms_samples": [12, 15],
        },
        "tooling": {
            "collector_version": "stub.v1",
            "commands_executed": ["manual_capture"],
            "log_artifacts": [],
        },
        "summary": {
            "cold_start_ms_p50": 1450,
            "cold_start_ms_p95": 1500,
            "warm_start_ms_p50": 575,
            "memory_idle_mb_p50": 151,
            "memory_streaming_mb_p50": 177.5,
            "cpu_idle_pct_p50": 5.5,
            "cpu_accel_pct_p50": 8.5,
            "cpu_gps_pct_p50": 12.5,
            "config_load_ms_p50": 13.5,
        },
    }
    write(Path(args.out), payload)
    print(args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
