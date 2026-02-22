import json
import subprocess
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli-tools" / "mobile-systems-lab"
UNIFIED_DIR = ROOT / "artifacts" / "benchmark" / "results" / "unified" / "LAB_01_SENSOR_TOGGLE_APP"


class BenchmarkPipelineTest(unittest.TestCase):
    def test_benchmark_command_emits_unified_metrics_with_expected_keys(self):
        before = set(UNIFIED_DIR.glob("*.UNIFIED_METRICS.json")) if UNIFIED_DIR.exists() else set()
        created_target = None
        try:
            proc = subprocess.run(
                [str(CLI), "benchmark", "LAB_01_SENSOR_TOGGLE_APP"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr + proc.stdout)
            self.assertIn("Wrote unified metrics:", proc.stdout)

            after = set(UNIFIED_DIR.glob("*.UNIFIED_METRICS.json"))
            self.assertTrue(after, "expected unified metrics outputs to exist")

            new_files = sorted(after - before)
            target = new_files[-1] if new_files else sorted(after)[-1]
            if new_files:
                created_target = target
            payload = json.loads(target.read_text(encoding="utf-8"))

            for key in [
                "schema_version",
                "benchmark_id",
                "lab_id",
                "scenario",
                "normalization_context",
                "platform_metrics",
                "comparative_summary",
                "regression_alerts",
            ]:
                self.assertIn(key, payload)

            self.assertEqual(payload["schema_version"], "unified_metrics.v1")
            self.assertEqual(payload["lab_id"], "LAB_01_SENSOR_TOGGLE_APP")
            self.assertIsInstance(payload["platform_metrics"], list)
            self.assertGreaterEqual(len(payload["platform_metrics"]), 1)
        finally:
            if created_target and created_target.exists():
                created_target.unlink()


if __name__ == "__main__":
    unittest.main()
