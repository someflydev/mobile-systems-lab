from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROMPTS_DIR = ROOT / ".prompts"
MANIFEST = PROMPTS_DIR / "PROMPT_MANIFEST.md"


class PromptManifestTest(unittest.TestCase):
    def test_manifest_exists_and_lists_prompt_files(self):
        self.assertTrue(MANIFEST.exists(), f"missing {MANIFEST}")
        text = MANIFEST.read_text(encoding="utf-8")
        rows = [line for line in text.splitlines() if line.startswith("| ")]
        self.assertGreater(len(rows), 0)

        listed_files = []
        for row in rows:
            parts = [p.strip() for p in row.strip("|").split("|")]
            if len(parts) < 3 or parts[0] in {"Order", "---"}:
                continue
            path_text = parts[2].strip("`")
            if path_text.startswith(".prompts/"):
                listed_files.append(ROOT / path_text)

        self.assertGreaterEqual(len(listed_files), 12)
        for path in listed_files:
            with self.subTest(path=path):
                self.assertTrue(path.exists(), f"manifest references missing file: {path}")

    def test_stage2_prompt_order_is_monotonic_and_explicit(self):
        text = MANIFEST.read_text(encoding="utf-8")
        in_stage2 = False
        stage2_rows = []

        for line in text.splitlines():
            if line.startswith("## Stage-2"):
                in_stage2 = True
                continue
            if in_stage2 and line.startswith("## "):
                break
            if in_stage2 and line.startswith("| "):
                stage2_rows.append(line)

        parsed = []
        for row in stage2_rows:
            parts = [p.strip() for p in row.strip("|").split("|")]
            if len(parts) < 5 or parts[0] in {"Order", "---"}:
                continue
            order = int(parts[0])
            prompt_id = parts[1]
            file_path = parts[2].strip("`")
            depends_on = parts[3]
            parsed.append((order, prompt_id, file_path, depends_on))

        self.assertEqual([p[0] for p in parsed], sorted(p[0] for p in parsed))
        self.assertEqual([p[0] for p in parsed], [8, 9, 10, 11, 12])

        expected_ids = [f"PROMPT_{n:02d}" for n in range(8, 13)]
        self.assertEqual([p[1] for p in parsed], expected_ids)
        for _, prompt_id, file_path, depends_on in parsed:
            self.assertTrue(file_path.endswith(f"{prompt_id}.txt"))
            self.assertTrue(depends_on, f"{prompt_id} missing dependency description")


if __name__ == "__main__":
    unittest.main()
