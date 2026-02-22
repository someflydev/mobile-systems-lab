import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ContractFilesTest(unittest.TestCase):
    def test_contract_json_files_parse(self):
        contract_files = [
            ROOT / "artifacts/contracts/LAB_SPEC.v1.json",
            ROOT / "artifacts/contracts/LAB_SPEC.v2.json",
            ROOT / "artifacts/contracts/config.schema.v1.json",
            ROOT / "artifacts/contracts/CANONICAL_MAPPING.json",
            ROOT / "artifacts/contracts/BENCHMARK_RESULT.schema.json",
            ROOT / "artifacts/contracts/UNIFIED_METRICS.schema.json",
            ROOT / "artifacts/contracts/north-star-config.schema.v1.json",
        ]
        for path in contract_files:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), f"missing {path}")
                json.loads(path.read_text(encoding="utf-8"))

    def test_v2_schema_has_required_core_keys(self):
        schema = json.loads((ROOT / "artifacts/contracts/LAB_SPEC.v2.json").read_text(encoding="utf-8"))
        required = set(schema.get("required", []))
        for key in ["lab_id", "difficulty_level", "state_model_type", "performance_budget", "expected_permissions"]:
            self.assertIn(key, required)


if __name__ == "__main__":
    unittest.main()
