import json
import subprocess
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "cli-tools/mobile-systems-lab"


class CliSmokeTest(unittest.TestCase):
    def test_cli_help(self):
        proc = subprocess.run([str(CLI), "--help"], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0)
        self.assertIn("generate", proc.stdout)

    def test_generate_dry_run_from_v2_example(self):
        schema = json.loads((ROOT / "artifacts/contracts/LAB_SPEC.v2.json").read_text(encoding="utf-8"))
        example = schema.get("examples", [])[0]
        self.assertTrue(example)

        with tempfile.TemporaryDirectory() as td:
            spec_path = Path(td) / "spec.json"
            spec_path.write_text(json.dumps(example), encoding="utf-8")
            proc = subprocess.run(
                [str(CLI), "generate", str(spec_path), "--dry-run"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr + proc.stdout)
            self.assertIn("dry-run", proc.stdout)

    def test_generate_dry_run_from_repo_spec_example(self):
        spec_path = ROOT / "artifacts/spec-examples/LAB_01_SENSOR_TOGGLE_APP.spec.v2.json"
        proc = subprocess.run(
            [str(CLI), "generate", str(spec_path), "--dry-run"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr + proc.stdout)
        self.assertIn("dry-run", proc.stdout)

    def test_generate_rejects_schema_file_with_actionable_hint(self):
        schema_path = ROOT / "artifacts/contracts/LAB_SPEC.v2.json"
        proc = subprocess.run(
            [str(CLI), "generate", str(schema_path), "--dry-run"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertNotEqual(proc.returncode, 0)
        combined = proc.stdout + proc.stderr
        self.assertIn("artifacts/spec-examples", combined)
        self.assertIn("schema", combined.lower())

    def test_compare_existing_lab(self):
        proc = subprocess.run(
            [str(CLI), "compare", "LAB_01_SENSOR_TOGGLE_APP"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(proc.returncode, 0, msg=proc.stderr + proc.stdout)

    def test_mutate_produces_deterministic_output_changes(self):
        spec_example = ROOT / "artifacts/spec-examples/LAB_01_SENSOR_TOGGLE_APP.spec.v2.json"
        source = json.loads(spec_example.read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory() as td:
            spec_path = Path(td) / "lab01.spec.v2.json"
            spec_path.write_text(json.dumps(source), encoding="utf-8")

            proc1 = subprocess.run(
                [str(CLI), "mutate", "LAB_01_SENSOR_TOGGLE_APP", "--spec", str(spec_path), "--sensor-add=gyroscope"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc1.returncode, 0, msg=proc1.stderr + proc1.stdout)
            mutated_path = spec_path.with_name("lab01.spec.v2.mutated.json")
            self.assertTrue(mutated_path.exists())
            mutated1 = json.loads(mutated_path.read_text(encoding="utf-8"))
            self.assertIn("gyroscope", mutated1.get("sensors_used", []))

            # Re-run from the original input and verify stable output.
            proc2 = subprocess.run(
                [str(CLI), "mutate", "LAB_01_SENSOR_TOGGLE_APP", "--spec", str(spec_path), "--sensor-add=gyroscope"],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(proc2.returncode, 0, msg=proc2.stderr + proc2.stdout)
            mutated2 = json.loads(mutated_path.read_text(encoding="utf-8"))
            self.assertEqual(mutated1, mutated2)


if __name__ == "__main__":
    unittest.main()
