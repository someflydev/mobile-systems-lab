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


if __name__ == "__main__":
    unittest.main()
