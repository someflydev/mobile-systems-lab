import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cli-tools"))

from benchmark_parsers import android_parser, ios_parser, flutter_parser, react_native_parser  # noqa: E402


class BenchmarkParsersTest(unittest.TestCase):
    def _assert_payload(self, payload, platform):
        self.assertEqual(payload["schema_version"], "benchmark_result.v1")
        self.assertEqual(payload["lab_id"], "LAB_01_SENSOR_TOGGLE_APP")
        self.assertEqual(payload["platform"], platform)
        self.assertIn("tooling", payload)
        self.assertIn("summary", payload)
        self.assertIn("metrics", payload)
        commands = payload["tooling"]["commands_executed"]
        self.assertIn("provenance:parsed_fixture", commands)
        self.assertTrue(any(cmd.startswith("fixture_parser:") for cmd in commands))

    def test_android_parser(self):
        payload = android_parser.parse_fixture(
            ROOT / "artifacts/benchmark/fixtures/android",
            "LAB_01_SENSOR_TOGGLE_APP",
        )
        self._assert_payload(payload, "kotlin_android")

    def test_ios_parser(self):
        payload = ios_parser.parse_fixture(
            ROOT / "artifacts/benchmark/fixtures/ios",
            "LAB_01_SENSOR_TOGGLE_APP",
        )
        self._assert_payload(payload, "swift_ios")

    def test_flutter_parser(self):
        payload = flutter_parser.parse_fixture(
            ROOT / "artifacts/benchmark/fixtures/flutter",
            "LAB_01_SENSOR_TOGGLE_APP",
        )
        self._assert_payload(payload, "flutter")

    def test_react_native_parser(self):
        payload = react_native_parser.parse_fixture(
            ROOT / "artifacts/benchmark/fixtures/react_native",
            "LAB_01_SENSOR_TOGGLE_APP",
        )
        self._assert_payload(payload, "react_native")


if __name__ == "__main__":
    unittest.main()
