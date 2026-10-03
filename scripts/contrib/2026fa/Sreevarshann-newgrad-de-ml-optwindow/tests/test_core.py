"""Offline tests for the newgrad-de-ml-optwindow prototype core (2026fa, Sreevarshann).

Run from the repo root:
    python3 -m unittest discover -s scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/tests -v

No network. Fixtures are fictional companies with example.com URLs; the persona is the
fictional search/examples/meera-krishnan. Two tests read the real (public) 80 Days CSV
to prove the frozen rules still reproduce the recorded counts.
"""
import copy
import csv
import importlib.util
import re
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
PKG = HERE.parent
sys.path.insert(0, str(PKG))
import core  # noqa: E402

FIX = PKG / "fixtures"
RUN = date(2026, 10, 2)


def load_mutant():
    spec = importlib.util.spec_from_file_location("broken_g5", FIX / "BROKEN-g5-ignores-liveness.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fixture_plan(run_date=RUN, persona_overrides=None):
    rows = core.load_companies(FIX / "companies-slice.csv")
    persona = core.load_persona(FIX / "persona-meera-krishnan.json")
    if persona_overrides:
        persona.update(persona_overrides)
    checks, rejected = core.load_posting_checks(FIX / "posting-checks.csv")
    return core.build_plan(rows, persona, checks, run_date, rejected_checks=rejected)


def by_company(items, name):
    return [i for i in items if i["company"]["value"] == name]


def labelled_values(obj):
    """Yield every {value, label, source} dict anywhere inside obj."""
    if isinstance(obj, dict):
        if {"value", "label", "source"} <= obj.keys():
            yield obj
        for x in obj.values():
            yield from labelled_values(x)
    elif isinstance(obj, (list, tuple)):
        for x in obj:
            yield from labelled_values(x)


def scoreable_role():
    """A fully evidenced role, built by the real pipeline, for G5 tests."""
    plan = fixture_plan()
    return copy.deepcopy([r for r in plan["scoreable"] if r["role_id"] == "alphadataexample:data_engineer"][0])


class FixturePlanTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = fixture_plan()

    def test_counts(self):
        self.assertEqual(self.plan["counts"], {"scoreable": 2, "blocked": 4, "network": 2, "verify_posting": 3,
                                               "rejected_checks": 1, "cannot_verify": 4})

    # failure case: company not in the CSV
    def test_company_not_in_csv_is_blocked(self):
        b = by_company(self.plan["blocked"], "Kappa Missing Example")
        self.assertEqual(len(b), 1)
        self.assertIn("not in matched sponsorship set", b[0]["reason"])
        self.assertNotIn("sponsorship", b[0])

    # failure case: human-typed name differs from the CSV
    def test_typo_name_blocked_with_both_names_shown(self):
        b = by_company(self.plan["blocked"], "Alpha Data Examples")
        self.assertEqual(len(b), 1)
        self.assertIn("not in matched sponsorship set", b[0]["reason"])
        self.assertEqual(b[0]["normalized_name"], "alphadataexamples")

    def test_suffix_and_punctuation_variants_still_match(self):
        # "Alpha Data Example" (check) vs "Alpha Data Example, Inc." (CSV) via the reused normalizer
        self.assertEqual([r["role_id"] for r in by_company(self.plan["scoreable"], "Alpha Data Example, Inc.")],
                         ["alphadataexample:data_engineer"])

    # failure case: posting liveness unchecked
    def test_unchecked_role_goes_to_verify_posting(self):
        v = [r for r in self.plan["verify_posting"] if r["role_id"] == "etabothexample:ml_engineer"]
        self.assertEqual(len(v), 1)
        self.assertTrue(v[0]["reason"].startswith("unchecked"))
        self.assertNotIn("liveness", v[0])

    # failure case: stale posting check
    def test_stale_check_goes_back_to_verify_posting(self):
        v = by_company(self.plan["verify_posting"], "Beta ML Example LLC")
        self.assertEqual(len(v), 1)
        self.assertIn("stale: checked 2026-09-20, 12 days before run (limit 7 days, your-input)", v[0]["reason"])

    def test_malformed_check_rejected_and_role_stays_unchecked(self):
        self.assertEqual(len(self.plan["rejected_checks"]), 1)
        self.assertIn("status must be one of", self.plan["rejected_checks"][0]["reason"])
        z = by_company(self.plan["verify_posting"], "Zeta Recruiting Example")
        self.assertTrue(z and z[0]["reason"].startswith("unchecked"))

    # failure case: blank latest_funding_date
    def test_blank_funding_date_stays_missing_not_zero(self):
        beta = by_company(self.plan["verify_posting"], "Beta ML Example LLC")[0]
        fd = beta["funding_context"]["latest_funding_date"]
        self.assertIsNone(fd["value"])
        self.assertEqual(fd["missing"], "blank in source")
        self.assertEqual(fd["label"], "record")
        self.assertFalse(beta["funding_context"]["scored"])

    # failure case: senior-only company
    def test_senior_only_company_is_network_never_scored(self):
        net = by_company(self.plan["network"], "Gamma Network Example Corp")
        self.assertEqual(len(net), 2)
        self.assertTrue(all("never scored" in n["reason"] for n in net))
        de = [n for n in net if n["role_type"]["value"] == "data_engineer"][0]
        self.assertIn("posting check ignored", de["note"])
        for lst in ("scoreable", "verify_posting", "blocked"):
            self.assertFalse(by_company(self.plan[lst], "Gamma Network Example Corp"), lst)

    # failure case: a keyword matching an irrelevant title (cannot be auto-detected)
    def test_irrelevant_title_match_is_visible_for_human_review(self):
        z = by_company(self.plan["verify_posting"], "Zeta Recruiting Example")[0]
        self.assertEqual(z["matched_titles"]["value"], ["Data Engineering Recruiter"])
        self.assertEqual(z["title_seniority"]["value"], {"Data Engineering Recruiter": "non-senior"})

    # failure case: approval count < 2 or non-numeric
    def test_below_floor_and_unparseable_approvals_blocked(self):
        delta = by_company(self.plan["blocked"], "Delta Thin Example")[0]
        self.assertIn("below tier floor (1 approvals < 2)", delta["reason"])
        eps = by_company(self.plan["blocked"], "Epsilon Garbled Example")[0]
        self.assertIn("unparseable", eps["reason"])
        self.assertIsNone(eps["sponsorship"]["approvals"]["value"])
        self.assertNotIn("p", eps["sponsorship"])

    def test_closed_posting_is_scored_with_gate_zero(self):
        eta = [r for r in self.plan["scoreable"] if r["role_id"] == "etabothexample:data_engineer"][0]
        self.assertEqual(eta["liveness"]["factor"]["value"], 0.0)
        self.assertEqual(eta["liveness"]["factor"]["status"], "closed")

    def test_unmatched_companies_are_ignored(self):
        for name in ("Theta Unrelated Example", "Iota No Titles Example"):
            for lst in ("scoreable", "blocked", "network", "verify_posting"):
                self.assertFalse(by_company(self.plan[lst], name))

    def test_form_d_misses_go_to_cannot_verify(self):
        keys = {c["company_key"] for c in self.plan["cannot_verify"]}
        self.assertEqual(keys, {"alphadataexample", "betamlexample", "etabothexample", "zetarecruitingexample"})


class FitTest(unittest.TestCase):
    # failure case: a role with no fit value
    def test_role_without_fit_is_blocked_not_defaulted(self):
        plan = fixture_plan(persona_overrides={"fit": {"data_engineer": 0.7}})
        ml = [b for b in plan["blocked"] if b.get("role_id") == "etabothexample:ml_engineer"]
        self.assertEqual(len(ml), 1)
        self.assertEqual(ml[0]["reason"], "fit missing for ml_engineer: not defaulted")
        self.assertNotIn("fit", ml[0])
        self.assertFalse([r for r in plan["scoreable"] + plan["verify_posting"]
                          if r["role_type"]["value"] == "ml_engineer"])

    def test_out_of_range_fit_is_treated_as_missing(self):
        p = core.validate_persona({"graduation_date": "2026-12-12", "opt_start_date": "2027-01-15",
                                   "unemployment_window_end": "2027-04-15", "unemployment_days_used": 0,
                                   "hiring_lag_days": 60, "fit": {"data_engineer": 1.7, "ml_engineer": "high"}})
        self.assertEqual(p["fit"], {})


class PersonaAndTimelineTest(unittest.TestCase):
    def setUp(self):
        self.persona = core.load_persona(FIX / "persona-meera-krishnan.json")

    def test_g1_halts_on_bad_date(self):
        with self.assertRaisesRegex(core.GateHalt, "G1 persona input: opt_start_date"):
            core.validate_persona({"graduation_date": "2026-12-12", "opt_start_date": "soon",
                                   "unemployment_window_end": "2027-04-15", "unemployment_days_used": 0,
                                   "hiring_lag_days": 60})

    def test_g1_halts_when_window_ends_before_opt_start(self):
        with self.assertRaisesRegex(core.GateHalt, "must be after opt_start_date"):
            core.validate_persona({"graduation_date": "2026-12-12", "opt_start_date": "2027-04-15",
                                   "unemployment_window_end": "2027-01-15", "unemployment_days_used": 0,
                                   "hiring_lag_days": 60})

    # failure case: 90-day window already past
    def test_g2_halts_when_window_already_past(self):
        with self.assertRaisesRegex(core.GateHalt, "unemployment window ended 2027-04-15"):
            core.timeline_gate(self.persona, date(2027, 4, 16))

    # failure case: OPT start already past
    def test_g2_halts_when_opt_start_already_past(self):
        with self.assertRaisesRegex(core.GateHalt, "OPT start 2027-01-15 has passed"):
            core.timeline_gate(self.persona, date(2027, 1, 16))

    def test_g2_halt_stops_the_whole_plan(self):
        with self.assertRaises(core.GateHalt):
            fixture_plan(run_date=date(2027, 4, 16))

    def test_g2_factor_boundary(self):
        # Any run on or before OPT start passes with the persona's 60-day lag (2027-01-15 + 60 = 2027-03-16);
        # runs after OPT start halt instead. So factor 0.0 is only reachable with a lag > 90 days.
        open_ = core.timeline_gate(self.persona, RUN)
        self.assertEqual(open_["value"], 1.0)
        self.assertIn("assumption, not a record", open_["assumption"])
        p = dict(self.persona, hiring_lag_days=90)
        self.assertEqual(core.timeline_gate(p, date(2027, 1, 15))["value"], 1.0)   # +90 = 2027-04-15
        self.assertEqual(core.timeline_gate(p, date(2027, 1, 14))["value"], 1.0)
        p = dict(self.persona, hiring_lag_days=91)
        self.assertEqual(core.timeline_gate(p, date(2027, 1, 15))["value"], 0.0)   # +91 = 2027-04-16

    def test_fixture_persona_matches_profile_yml(self):
        text = (core.REPO / "search/examples/meera-krishnan/profile.yml").read_text(encoding="utf-8")

        def scalar(key):
            m = re.search(rf"^\s*{key}:\s*([^\s#]+)", text, re.M)
            return m.group(1) if m else None
        self.assertEqual(scalar("graduation_date"), "2026-12-12")
        self.assertEqual(scalar("ead_start_date"), self.persona["opt_start_date"].isoformat())
        self.assertEqual(scalar("unemployment_window_end"), self.persona["unemployment_window_end"].isoformat())
        self.assertEqual(int(scalar("unemployment_days_used")), self.persona["unemployment_days_used"])
        self.assertEqual(int(scalar("hiring_lag_days")), self.persona["hiring_lag_days"])
        self.assertEqual(float(scalar("data_engineer")), self.persona["fit"]["data_engineer"])
        self.assertEqual(float(scalar("ml_engineer")), self.persona["fit"]["ml_engineer"])


class LivenessTest(unittest.TestCase):
    def setUp(self):
        self.role = {"company_key": "alphadataexample", "role_type": {"value": "data_engineer"}}

    def check(self, d, status="open"):
        return [{"company_key": "alphadataexample", "role_type": "data_engineer", "url": "https://example.com/j",
                 "date_checked": d, "status": status, "_source": "test", "checked_by": "test human",
                 "human_checked": True, "label": "your-input"}]

    def test_seven_days_is_current_eight_is_stale(self):
        live, reason = core.liveness_gate(self.role, self.check(date(2026, 9, 25)), RUN)
        self.assertIsNone(reason)
        self.assertEqual(live["age_days"], 7)
        live, reason = core.liveness_gate(self.role, self.check(date(2026, 9, 24)), RUN)
        self.assertIsNone(live)
        self.assertIn("stale", reason)

    def test_future_dated_check_is_not_trusted(self):
        live, reason = core.liveness_gate(self.role, self.check(date(2026, 10, 3)), RUN)
        self.assertIsNone(live)
        self.assertIn("after the run date", reason)

    def test_status_mapping(self):
        for status, factor in (("open", 1.0), ("closed", 0.0), ("not found", 0.0)):
            live, _ = core.liveness_gate(self.role, self.check(date(2026, 10, 1), status), RUN)
            self.assertEqual(live["value"], factor)
            self.assertEqual(live["label"], "your-input")


AI_BY = "Claude (chat) web search, not human-verified"


def write_checks(rows, header=None):
    """Write a temporary posting-check CSV (outside the repo) and return its path."""
    # column order: company, role_type, url, date_checked, status, checked_by,
    #               what_was_seen, tool_result, tool_reason, tool_run_date
    header = header or core.POSTING_COLUMNS + core.POSTING_OPTIONAL
    fh = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="", encoding="utf-8")
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(header)
    w.writerows(rows)
    fh.close()
    return Path(fh.name)


class CheckedByTest(unittest.TestCase):
    """CHANGE-BRIEF R3: who did the posting check decides whether G4 is cleared."""

    def plan_with(self, rows):
        checks, rejected = core.load_posting_checks(write_checks(rows))
        persona = core.load_persona(FIX / "persona-meera-krishnan.json")
        return core.build_plan(core.load_companies(FIX / "companies-slice.csv"), persona, checks, RUN,
                               rejected_checks=rejected)

    def test_ai_check_is_scored_but_g4_not_cleared_and_run_is_provisional(self):
        plan = self.plan_with([["Alpha Data Example", "data_engineer", "https://example.com/a", "2026-10-02", "open",
                                AI_BY, "snapshot", "active", "visible apply control detected", "2026-10-02"]])
        # R4: tool result chosen to agree with the status; the conflict case is covered by ConflictTest.
        role = [r for r in plan["scoreable"] if r["role_id"] == "alphadataexample:data_engineer"][0]
        live = role["liveness"]["factor"]
        self.assertEqual(live["label"], "model-judgment")
        self.assertFalse(live["g4_human_cleared"])
        self.assertEqual(live["what_was_seen"]["label"], "model-judgment")
        self.assertTrue(plan["provisional"])
        self.assertEqual(plan["g4_human_gate"]["not_cleared_role_ids"], ["alphadataexample:data_engineer"])
        self.assertTrue(plan["headline_warnings"][0].startswith("G4 human liveness gate NOT cleared"))
        self.assertIn("provisional", plan["headline_warnings"][0])
        self.assertEqual(core.to_scorer_record(role)["liveness"]["source"], "model-judgment")

    def test_tool_result_is_record_with_run_source(self):
        plan = self.plan_with([["Alpha Data Example", "data_engineer", "https://example.com/a", "2026-10-02", "open",
                                AI_BY, "snapshot", "uncertain", "navigation error: page.goto: Download is starting",
                                "2026-10-02"]])
        # R4: a non-conflicting result ("uncertain"); a contradicting one is covered by ConflictTest.
        live = plan["scoreable"][0]["liveness"]["factor"]
        self.assertEqual(live["tool_result"], {"value": "uncertain", "label": "record",
                                               "source": "npm run ats:liveness, 2026-10-02"})
        self.assertEqual(live["tool_reason"]["value"], "navigation error: page.goto: Download is starting")
        self.assertEqual(live["value"], 1.0, "without a contradiction the status drives the factor")
        reasons = [c["reason"] for c in plan["cannot_verify"]]
        self.assertTrue(any("no 'not found' result" in r for r in reasons))
        self.assertTrue(any("'insufficient content' as expired" in r for r in reasons))

    def test_human_check_clears_g4(self):
        plan = fixture_plan()
        self.assertFalse(plan["provisional"])
        self.assertEqual(plan["headline_warnings"], [])
        self.assertTrue(all(r["liveness"]["factor"]["g4_human_cleared"] for r in plan["scoreable"]))
        self.assertTrue(all(r["liveness"]["factor"]["label"] == "your-input" for r in plan["scoreable"]))
        self.assertFalse(any(c["company_key"] is None for c in plan["cannot_verify"]),
                         "tool limits only apply when ats:liveness results are used")

    def test_blank_checked_by_is_rejected(self):
        checks, rejected = core.load_posting_checks(write_checks(
            [["Alpha Data Example", "data_engineer", "https://example.com/a", "2026-10-02", "open", "", "", "", "", ""]]))
        self.assertEqual(checks, [])
        self.assertIn("checked_by blank", rejected[0]["reason"])

    def test_tool_result_without_run_date_is_rejected(self):
        _, rejected = core.load_posting_checks(write_checks(
            [["Alpha Data Example", "data_engineer", "https://example.com/a", "2026-10-02", "open", AI_BY, "",
              "expired", "HTTP 404", ""]]))
        self.assertIn("tool_run_date required", rejected[0]["reason"])

    def test_unknown_column_halts(self):
        with self.assertRaisesRegex(core.GateHalt, "unknown \\['vibe'\\]"):
            core.load_posting_checks(write_checks([], header=core.POSTING_COLUMNS + ["vibe"]))

    def test_submission_input_file_loads_as_model_judgment(self):
        path = core.REPO / "course/2026fa/submissions/Sreevarshann/inputs/posting-checks.csv"
        checks, rejected = core.load_posting_checks(path)
        self.assertEqual(rejected, [])
        self.assertEqual(len(checks), 5)
        self.assertTrue(all(c["label"] == "model-judgment" and not c["human_checked"] for c in checks))


class ConflictTest(unittest.TestCase):
    """CHANGE-BRIEF R4: a record outranks a model-judgment posting status; a human status is never overridden."""

    def plan_with(self, checked_by, status, tool_result, tool_reason):
        checks, rejected = core.load_posting_checks(write_checks(
            [["Alpha Data Example", "data_engineer", "https://example.com/a", "2026-10-02", status, checked_by,
              "snapshot", tool_result, tool_reason, "2026-10-02" if tool_result else ""]]))
        self.assertEqual(rejected, [])
        persona = core.load_persona(FIX / "persona-meera-krishnan.json")
        return core.build_plan(core.load_companies(FIX / "companies-slice.csv"), persona, checks, RUN)

    def alpha(self, plan, lst):
        return [r for r in plan[lst] if r.get("role_id") == "alphadataexample:data_engineer"]

    def test_model_judgment_open_vs_record_expired_goes_to_verify_posting(self):
        plan = self.plan_with(AI_BY, "open", "expired", "HTTP 404")
        self.assertFalse(self.alpha(plan, "scoreable"))
        v = self.alpha(plan, "verify_posting")[0]
        self.assertTrue(v["reason"].startswith("conflict: model-judgment status vs ats:liveness record"))
        self.assertIn("status=open [model-judgment]", v["reason"])
        self.assertIn("tool_result=expired [record]: HTTP 404", v["reason"])
        self.assertEqual(v["posting_conflict"]["status"]["label"], "model-judgment")
        self.assertEqual(v["posting_conflict"]["tool_result"]["label"], "record")
        self.assertNotIn("liveness", v)

    def test_model_judgment_not_found_vs_record_active_goes_to_verify_posting(self):
        plan = self.plan_with(AI_BY, "not found", "active", "visible apply control detected")
        self.assertFalse(self.alpha(plan, "scoreable"))
        self.assertTrue(self.alpha(plan, "verify_posting")[0]["reason"].startswith("conflict:"))

    def test_human_open_vs_record_expired_human_governs_and_is_flagged(self):
        plan = self.plan_with("test human", "open", "expired", "insufficient content — likely nav/footer only")
        role = self.alpha(plan, "scoreable")[0]
        live = role["liveness"]["factor"]
        self.assertEqual((live["value"], live["label"]), (1.0, "your-input"))
        self.assertIn("human status governs", live["tool_disagreement"])
        self.assertEqual([d["role_id"] for d in plan["tool_disagreements"]], ["alphadataexample:data_engineer"])
        self.assertNotIn("posting_conflict", role)

    def test_uncertain_never_overrides(self):
        for status, factor in (("open", 1.0), ("not found", 0.0)):
            plan = self.plan_with(AI_BY, status, "uncertain", "navigation error: page.goto: Download is starting")
            role = self.alpha(plan, "scoreable")[0]
            self.assertEqual(role["liveness"]["factor"]["value"], factor, status)
            self.assertEqual(role["liveness"]["factor"]["tool_result"]["value"], "uncertain")
            self.assertNotIn("tool_disagreement", role["liveness"]["factor"])
            self.assertEqual(plan["tool_disagreements"], [])

    def test_agreement_is_not_a_conflict(self):
        for status, tool in (("open", "active"), ("closed", "expired"), ("not found", "expired")):
            self.assertFalse(core.status_conflict(status, tool), (status, tool))


class SponsorshipTest(unittest.TestCase):
    def test_cutoff_boundaries(self):
        cases = {"50.0": (0.8, "Proven"), "49": (0.6, "likely"), "10": (0.6, "likely"),
                 "9.0": (0.4, "possible"), "2": (0.4, "possible")}
        for raw, (p, tier) in cases.items():
            ev, reason = core.map_sponsorship(raw, "test")
            self.assertIsNone(reason, raw)
            self.assertEqual((ev["p"]["value"], ev["tier"]["value"]), (p, tier), raw)
            self.assertEqual(ev["approvals"]["label"], "record")
            self.assertEqual(ev["p"]["label"], "your-input")
        for raw in ("1.9", "0", "", "n/a"):
            ev, reason = core.map_sponsorship(raw, "test")
            self.assertIsNotNone(reason, raw)
            self.assertNotIn("p", ev)

    def test_proven_provenance_string(self):
        ev, _ = core.map_sponsorship("120", "test")
        self.assertIn("role-scorer.mjs:48", ev["tier"]["source"])


class G5Test(unittest.TestCase):
    def test_complete_role_passes(self):
        self.assertEqual(core.evidence_problems(scoreable_role()), [])

    def test_each_missing_input_is_caught(self):
        for block, field in core.REQUIRED_EVIDENCE:
            role = scoreable_role()
            del role[block][field]
            self.assertIn(f"{block}.{field} missing", core.evidence_problems(role), (block, field))

    def test_bad_label_and_range_are_caught(self):
        role = scoreable_role()
        role["fit"]["p"]["label"] = "vibes"
        role["liveness"]["factor"]["value"] = 1.5
        problems = core.evidence_problems(role)
        self.assertTrue(any("label 'vibes'" in p for p in problems))
        self.assertTrue(any("liveness.factor must be a number in [0, 1]" in p for p in problems))

    def test_assert_scoreable_halts_on_incomplete_role(self):
        role = scoreable_role()
        del role["liveness"]
        with self.assertRaisesRegex(core.GateHalt, "G5 evidence completeness"):
            core.assert_scoreable([role])

    def test_suite_catches_broken_mutant(self):
        """The BROKEN mutant lets a role with no liveness through; this suite's check must expose it."""
        mutant = load_mutant()

        def catches_missing_liveness(check):
            role = scoreable_role()
            del role["liveness"]
            try:
                core.assert_scoreable([role], check=check)
            except core.GateHalt:
                return True
            return False
        self.assertTrue(catches_missing_liveness(core.evidence_problems))
        self.assertFalse(catches_missing_liveness(mutant.evidence_problems),
                         "mutant should let the unchecked role through; if it doesn't, the mutant is not a real break")


class LabelTest(unittest.TestCase):
    def test_every_emitted_value_has_an_allowed_label(self):
        plan = fixture_plan()
        found = list(labelled_values(plan))
        self.assertGreater(len(found), 50)
        for item in found:
            self.assertIn(item["label"], core.LABELS, item)
            self.assertTrue(item["source"], item)

    def test_v_rejects_unknown_label(self):
        with self.assertRaises(ValueError):
            core.v(1, "record-ish", "x")

    def test_soc_mapping_is_model_judgment_and_wage_is_record(self):
        bls = core.bls_context()
        self.assertEqual(bls["data_engineer"]["soc"]["value"], "15-1243")
        self.assertEqual(bls["ml_engineer"]["soc"]["value"], "15-2051")
        for rt in ("data_engineer", "ml_engineer"):
            self.assertEqual(bls[rt]["soc"]["label"], "model-judgment")
            self.assertTrue(bls[rt]["rows"])
            for row in bls[rt]["rows"]:
                self.assertEqual(row["annual_median_wage"]["label"], "record")

    def test_scorer_record_shape(self):
        rec = core.to_scorer_record(scoreable_role())
        self.assertEqual(rec["sponsorship"], {"p": 0.8, "tier": "Proven", "source": "your-input"})
        self.assertEqual(rec["evidence"]["total_approvals"]["label"], "record")
        self.assertEqual(rec["evidence"]["total_approvals"]["value"], 120.0)
        for block in ("fit", "liveness", "timeline"):
            self.assertEqual(rec[block]["source"], "your-input")


class RealDataTest(unittest.TestCase):
    """Reads the public 80 Days CSV (offline) to prove the frozen rules reproduce the recorded counts."""

    @classmethod
    def setUpClass(cls):
        cls.rows = core.load_companies()
        cls.cls = core.classify_companies(cls.rows)

    def test_loader_keeps_only_non_personal_columns(self):
        self.assertEqual(len(self.rows), 30369)
        self.assertEqual(set(self.rows[0]), set(core.NEEDED_COLUMNS) | {"_source"})
        for col in ("phone", "executive_officers", "board_directors", "website", "city", "zip_code"):
            self.assertNotIn(col, self.rows[0])

    def test_reproduces_recorded_funnel(self):
        entry = {c["company"]["source"] for c in self.cls["candidates"]}
        senior_only = {n["company"]["source"] for n in self.cls["network"]
                       if n["company_class"]["value"] == "senior-only"}
        self.assertEqual((len(entry), len(senior_only), len(entry | senior_only)), (64, 50, 114))
        self.assertEqual(self.cls["blocked"], [])
        by_type = {}
        for c in self.cls["candidates"]:
            by_type[c["role_type"]["value"]] = by_type.get(c["role_type"]["value"], 0) + 1
        self.assertEqual(by_type, {"data_engineer": 33, "ml_engineer": 31})
        tiers = {}
        for c in self.cls["candidates"]:
            ev, reason = core.map_sponsorship(c["_row"]["Total Approvals"], c["_row"]["_source"])
            self.assertIsNone(reason)
            tiers[ev["tier"]["value"]] = tiers.get(ev["tier"]["value"], 0) + 1
        self.assertEqual(tiers, {"Proven": 22, "likely": 25, "possible": 17})


if __name__ == "__main__":
    unittest.main()
