import shutil
import subprocess
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts" / "dev"
TMP_ROOT = ROOT / ".tmp" / "stage2"


def run_script(name: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["bash", str(SCRIPTS / name)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


class DevWorkflowScriptsTest(unittest.TestCase):
    def tearDown(self):
        shutil.rmtree(ROOT / ".tmp", ignore_errors=True)

    def test_doctor_script(self):
        proc = run_script("doctor.sh")
        self.assertEqual(proc.returncode, 0, msg=proc.stderr + proc.stdout)
        self.assertIn("doctor ok", proc.stdout)

    def test_bringup_is_idempotent_and_teardown_is_safe(self):
        proc1 = run_script("bringup_lab01.sh")
        self.assertEqual(proc1.returncode, 0, msg=proc1.stderr + proc1.stdout)
        self.assertTrue(TMP_ROOT.exists())

        proc2 = run_script("bringup_lab01.sh")
        self.assertEqual(proc2.returncode, 0, msg=proc2.stderr + proc2.stdout)
        self.assertTrue(TMP_ROOT.exists())

        # Do not invoke check_lab01.sh from unit tests because it runs `make validate`,
        # which would recursively invoke this test suite.
        proc3 = run_script("teardown_lab01.sh")
        self.assertEqual(proc3.returncode, 0, msg=proc3.stderr + proc3.stdout)
        self.assertFalse(TMP_ROOT.exists())


if __name__ == "__main__":
    unittest.main()
