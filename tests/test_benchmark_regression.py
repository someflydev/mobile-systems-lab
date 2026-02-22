import json
import subprocess
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli-tools" / "mobile-systems-lab"
BASELINE = ROOT / "artifacts/benchmark/baselines/LAB_01_SENSOR_TOGGLE_APP.UNIFIED_METRICS.baseline.json"


class BenchmarkRegressionTest(unittest.TestCase):
    def test_benchmark_regress_no_alerts_when_current_equals_baseline(self):
        proc = subprocess.run(
            [
                str(CLI),
                "benchmark-regress",
                "LAB_01_SENSOR_TOGGLE_APP",
                "--current",
                str(BASELINE),
                "--baseline",
                str(BASELINE),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr + proc.stdout)
        self.assertIn("No regression alerts", proc.stdout)

    def test_benchmark_regress_detects_required_metric_increases(self):
        baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
        current = json.loads(BASELINE.read_text(encoding="utf-8"))

        target = next(p for p in current["platform_metrics"] if p["platform"] == "kotlin_android")
        target["cold_start_ms_p95"] = float(target["cold_start_ms_p95"]) + 200.0
        target["memory_idle_mb_p95"] = float(target["memory_idle_mb_p95"]) + 20.0
        target["cpu_gps_pct_p95"] = float(target["cpu_gps_pct_p95"]) + 4.0

        with tempfile.TemporaryDirectory() as td:
            current_path = Path(td) / "current.UNIFIED_METRICS.json"
            current_path.write_text(json.dumps(current), encoding="utf-8")
            proc = subprocess.run(
                [
                    str(CLI),
                    "benchmark-regress",
                    "LAB_01_SENSOR_TOGGLE_APP",
                    "--current",
                    str(current_path),
                    "--baseline",
                    str(BASELINE),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 1, msg=proc.stderr + proc.stdout)
            out = proc.stdout + proc.stderr
            self.assertIn("cold_start_ms_p95", out)
            self.assertIn("memory_idle_mb_p95", out)
            self.assertIn("cpu_gps_pct_p95", out)


if __name__ == "__main__":
    unittest.main()
