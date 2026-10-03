"""Offline tests for run.py (2026fa, Sreevarshann). Outputs go to a temp folder, never the repo.

The section-order test uses STUB_SCORER, a canned stand-in that only echoes role ids so the
report can be rendered without npm. It is not the scorer and tests nothing about scoring.
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PKG))
sys.path.insert(0, str(Path(__file__).resolve().parent))
import core  # noqa: E402
import run  # noqa: E402
from test_core import AI_BY, write_checks  # noqa: E402


def STUB_SCORER(roles_path, out_dir):
    roles = json.loads(Path(roles_path).read_text())
    Path(out_dir, "role-scores.json").write_text(json.dumps({"roles": [
        {"role_id": r["role_id"], "composite": 0.0, "recommendation": "Skip",
         "reason": "gated: liveness ≈ 0.000 (stub)"} for r in roles]}))
    return 0, "stub scorer", "", "STUB_SCORER (not the real scorer)"


def NEVER_CALLED(*_):
    raise AssertionError("scorer must not be called when zero roles are scoreable")


class RunTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def args(self, checks, run_date="2026-10-02", *extra):
        return ["--run-date", run_date, "--checks", str(checks), "--out-root", self.tmp, *extra]

    def test_zero_scoreable_skips_scorer_with_plain_message(self):
        code = run.main(self.args(write_checks([])), scorer=NEVER_CALLED)
        self.assertEqual(code, 0)
        out = Path(self.tmp, "2026-10-02")
        self.assertEqual(json.loads((out / "roles.json").read_text()), [])
        report = (out / "report.md").read_text()
        self.assertIn("No role reached the scorer in this run.", report)
        log = json.loads((out / "run-log.json").read_text())
        self.assertEqual(log["scorer"], {"ran": False, "reason": "zero scoreable roles"})
        self.assertFalse((out / "role-scores.json").exists())

    def test_halt_writes_run_log_and_no_report(self):
        code = run.main(self.args(write_checks([]), "2027-04-16"), scorer=NEVER_CALLED)
        self.assertEqual(code, 2)
        out = Path(self.tmp, "2027-04-16")
        log = json.loads((out / "run-log.json").read_text())
        self.assertEqual(log["status"], "halted")
        self.assertIn("unemployment window ended 2027-04-15", log["halt"])
        self.assertFalse((out / "report.md").exists())

    def test_missing_input_file_halts_cleanly(self):
        """Break attempt (d): a missing input file is a clean halt with a run log, not a traceback."""
        missing = Path(self.tmp, "does-not-exist.csv")
        code = run.main(self.args(missing), scorer=NEVER_CALLED)
        self.assertEqual(code, 2)
        out = Path(self.tmp, "2026-10-02")
        log = json.loads((out / "run-log.json").read_text())
        self.assertEqual(log["status"], "halted")
        self.assertIn("input file not found: posting_checks = ", log["halt"])
        self.assertIn("does-not-exist.csv", log["halt"])
        self.assertFalse(log["inputs"]["posting_checks"]["exists"])
        self.assertTrue(log["inputs"]["persona"]["exists"])
        self.assertFalse((out / "report.md").exists())
        self.assertFalse((out / "roles.json").exists())

    def test_refuses_to_overwrite_existing_run(self):
        checks = write_checks([])
        self.assertEqual(run.main(self.args(checks), scorer=NEVER_CALLED), 0)
        self.assertEqual(run.main(self.args(checks), scorer=NEVER_CALLED), 3)
        self.assertEqual(run.main(self.args(checks, "2026-10-02", "--overwrite"), scorer=NEVER_CALLED), 0)

    def test_report_opens_with_summary_and_g4_warning_then_sections_in_order(self):
        checks = write_checks([["HUMAN INC", "data_engineer", "https://example.com/h", "2026-10-02", "not found",
                                AI_BY, "snapshot", "uncertain", "navigation error", "2026-10-02"]])
        self.assertEqual(run.main(self.args(checks), scorer=STUB_SCORER), 0)
        report = Path(self.tmp, "2026-10-02", "report.md").read_text()
        heads = [line for line in report.splitlines() if line.startswith("## ")]
        self.assertEqual(heads, ["## Executive summary", "## Run record", "## Funnel", "## Scored roles",
                                 "## Verify-posting list", "## Network list (senior-only — networking targets, never scored)",
                                 "## Blocked list", "## Cannot verify", "## Report-only context (no effect on any score)",
                                 "## Next action per company"])
        summary = report.split("## Executive summary", 1)[1].split("## Run record", 1)[0]
        self.assertTrue(summary.strip().startswith("> **Provisional — read first.** G4 human liveness gate NOT cleared"))
        self.assertLess(summary.index("Provisional"), summary.index("**What this is.**"))
        self.assertNotIn("/Users/", report, "no absolute local paths in outputs")
        log = Path(self.tmp, "2026-10-02", "run-log.json").read_text()
        self.assertNotIn("/Users/", log)
        for item in json.loads(log)["inputs"].values():
            self.assertEqual(len(item["sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
