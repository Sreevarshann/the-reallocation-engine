#!/usr/bin/env python3
"""newgrad-de-ml-optwindow: prototype core (2026fa, Sreevarshann).

Implements the filter, sponsorship mapping and gates G1, G2, G4, G5 from
course/2026fa/submissions/Sreevarshann/CHANGE-BRIEF.md. Python 3 stdlib only.
This module does not call the scorer and writes no files.

Every emitted value is {"value", "label", "source"} with label exactly one of
record / model-judgment / your-input. Missing data stays None with a reason;
it is never turned into 0.
"""
from __future__ import annotations

import csv
import glob
import importlib.util
import json
import re
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]

# Reused, not re-implemented: the maintained stdlib-only normalizer (CHANGE-BRIEF R1).
_spec = importlib.util.spec_from_file_location("entity_resolution", REPO / "scripts/sec/entity-resolution.py")
_er = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_er)
normalize_company_name = _er.normalize_company_name

# ── labels ────────────────────────────────────────────────────────────────
RECORD, MODEL, INPUT = "record", "model-judgment", "your-input"
LABELS = frozenset({RECORD, MODEL, INPUT})


def v(value, label, source, **extra):
    """One emitted value: {value, label, source} plus optional detail (e.g. missing reason)."""
    if label not in LABELS:
        raise ValueError(f"label must be one of {sorted(LABELS)}, got {label!r}")
    out = {"value": value, "label": label, "source": source}
    out.update(extra)
    return out


# ── frozen rules (notes/candidate-analysis.py; decisions are your-input) ──
CSV_PATH = REPO / "data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv"
BLS_PATH = REPO / "data/bls/compact/soc_occupation_compact.csv"
SEC_SAMPLE_GLOB = str(REPO / "data/sec/form-d/processed/sample/*.sample.json")

ROLE_KEYWORDS = {
    "data_engineer": ["data engineer", "data engineering"],
    "ml_engineer": ["machine learning engineer", "ml engineer", "ai engineer", "ai/ml",
                    "deep learning engineer", "mlops"],
}
SENIOR_KEYWORDS = ["senior", "sr", "staff", "principal", "lead", "manager", "director", "head", "vp",
                   "iii", "iv", "founding"]
RULE_SOURCE = "CHANGE-BRIEF.md / notes/candidate-analysis.py (keyword + seniority rules)"

# Only these columns are kept; personal and contact columns (phone, executive_officers,
# board_directors, website, address fields) are never retained.
NEEDED_COLUMNS = ["company_name", "top_job_titles_sponsored", "Total Approvals", "Total Denials",
                  "Approval_Rate", "latest_funding_date", "latest_funding_stage"]

TIER_SOURCE = "tier cut-offs: CHANGE-BRIEF.md (your-input)"
PROVEN_SOURCE = ("tier string from Ch.11 and data/examples fixtures; "
                 "code only defines soft tiers at role-scorer.mjs:48")
POSTING_COLUMNS = ["company", "role_type", "url", "date_checked", "status"]
POSTING_STATUSES = {"open": 1.0, "closed": 0.0, "not found": 0.0}
MAX_CHECK_AGE_DAYS = 7  # your-input (CHANGE-BRIEF G4)
SOC_MAP = {"data_engineer": "15-1243", "ml_engineer": "15-2051"}  # model-judgment, report-only


class GateHalt(Exception):
    """A gate that stops the whole run (G1 persona input, G2 timeline, G5 final check)."""


def kw_regex(keywords):
    # case-insensitive; a keyword must not be glued to other letters ("ml engineer" != "html engineer")
    return re.compile("|".join(rf"(?<![a-z]){re.escape(k)}(?![a-z])" for k in keywords), re.I)


ROLE_RX = {rt: kw_regex(kws) for rt, kws in ROLE_KEYWORDS.items()}
ANY_ROLE_RX = kw_regex([k for kws in ROLE_KEYWORDS.values() for k in kws])
SENIOR_RX = kw_regex(SENIOR_KEYWORDS)
TITLE_RX = re.compile(r"'([^']*)'")  # same title extraction as the frozen analysis


def _num(raw):
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _date(raw):
    try:
        return date.fromisoformat(str(raw).strip())
    except ValueError:
        return None


# ── data loading ──────────────────────────────────────────────────────────
def load_companies(path=CSV_PATH):
    """Read the 80 Days CSV keeping only NEEDED_COLUMNS, each row tagged with its source line."""
    path = Path(path)
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        missing = [c for c in NEEDED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise GateHalt(f"source CSV {path.name} lacks required columns: {missing}")
        rows = []
        for i, row in enumerate(reader, start=2):  # line 1 is the header
            kept = {c: row[c] for c in NEEDED_COLUMNS}
            kept["_source"] = f"{_rel(path)}#L{i}"
            rows.append(kept)
    return rows


def _rel(path):
    try:
        return str(Path(path).resolve().relative_to(REPO))
    except ValueError:
        return str(path)


# ── keyword match + seniority split ──────────────────────────────────────
def classify_companies(rows):
    """Keyword-match each company, then split matched companies by seniority of their matched titles.

    Returns {"candidates": [...], "network": [...], "blocked": [...]}. A candidate is one
    (company, role type) pair with at least one non-senior matched title at an
    entry-eligible company.
    """
    out = {"candidates": [], "network": [], "blocked": []}
    for row in rows:
        field = row["top_job_titles_sponsored"]
        if not ANY_ROLE_RX.search(field):
            continue
        src = row["_source"]
        name = row["company_name"]
        key = normalize_company_name(name)
        titles = TITLE_RX.findall(field)
        by_role = {rt: [t.strip() for t in titles if rx.search(t)] for rt, rx in ROLE_RX.items()}
        matched = [t for ts in by_role.values() for t in ts]
        if not key:
            out["blocked"].append(_blocked(name, None, src, "company name empty after normalization"))
            continue
        if not matched:
            out["blocked"].append(_blocked(name, None, src, "title field matched but no titles could be extracted"))
            continue
        seniority = {t: ("senior" if SENIOR_RX.search(t) else "non-senior") for t in matched}
        entry_eligible = any(s == "non-senior" for s in seniority.values())
        for rt, ts in by_role.items():
            if not ts:
                continue
            item = {
                "role_id": f"{key}:{rt}",
                "company": v(name, RECORD, src),
                "company_key": key,
                "role_type": v(rt, INPUT, RULE_SOURCE),
                "matched_titles": v(ts, RECORD, src),
                "title_seniority": v({t: seniority[t] for t in ts}, INPUT, RULE_SOURCE),
                "company_class": v("entry-eligible" if entry_eligible else "senior-only", INPUT, RULE_SOURCE),
                "_row": row,
            }
            if entry_eligible and any(seniority[t] == "non-senior" for t in ts):
                out["candidates"].append(item)
            else:
                item["reason"] = ("senior-only company: networking target, never scored" if not entry_eligible
                                  else "role type senior-only at this company: networking target, never scored")
                out["network"].append(item)
    return out


def _blocked(company, role_type, src, reason, **extra):
    d = {"company": v(company, RECORD, src), "role_type": role_type, "reason": reason}
    d.update(extra)
    return d


# ── sponsorship mapping ───────────────────────────────────────────────────
def map_sponsorship(raw_approvals, src):
    """Map a recorded approval count to the scorer's p and tier, or block it.

    Returns (evidence, None) on success or (evidence, reason) when blocked.
    The count is record; p and tier come from your-input cut-offs.
    """
    n = _num(raw_approvals)
    if n is None:
        return {"approvals": v(None, RECORD, src, missing="unparseable in source", raw=raw_approvals)}, \
            "sponsorship evidence unparseable (Total Approvals is not a number)"
    approvals = v(n, RECORD, src)
    if n >= 50:
        p, tier, tier_src = 0.8, "Proven", PROVEN_SOURCE
    elif n >= 10:
        p, tier, tier_src = 0.6, "likely", TIER_SOURCE
    elif n >= 2:
        p, tier, tier_src = 0.4, "possible", TIER_SOURCE
    else:
        return {"approvals": approvals}, f"sponsorship evidence below tier floor ({n:g} approvals < 2)"
    return {"approvals": approvals, "p": v(p, INPUT, TIER_SOURCE), "tier": v(tier, INPUT, tier_src)}, None


# ── report-only context ───────────────────────────────────────────────────
def funding_context(row):
    """Funding date and stage from the CSV, labelled record; blank stays missing, never 0."""
    src = row["_source"]
    out = {}
    raw = row["latest_funding_date"].strip()
    if not raw:
        out["latest_funding_date"] = v(None, RECORD, src, missing="blank in source")
    elif _date(raw) is None:
        out["latest_funding_date"] = v(None, RECORD, src, missing="unparseable in source", raw=raw)
    else:
        out["latest_funding_date"] = v(raw, RECORD, src)
    stage = row["latest_funding_stage"].strip()
    out["latest_funding_stage"] = v(stage or None, RECORD, src, **({} if stage else {"missing": "blank in source"}))
    rate = _num(row["Approval_Rate"])
    out["approval_rate_pct"] = v(rate, RECORD, src, note="0-100 percentage; reported, not scored",
                                 **({} if rate is not None else {"missing": "blank or unparseable in source"}))
    out["scored"] = False
    return out


def bls_context(path=BLS_PATH):
    """National median wage rows for the mapped SOC codes. Wages are record; the mapping is model-judgment."""
    path = Path(path)
    out = {}
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    for rt, soc in SOC_MAP.items():
        items = []
        for i, r in enumerate(rows, start=2):
            if r["bls_soc_code"] != soc:
                continue
            src = f"{_rel(path)}#L{i}"
            wage = _num(r["annual_median_wage"])
            items.append({
                "onet_soc_code": v(r["onet_soc_code"], RECORD, src),
                "title": v(r["title"], RECORD, src),
                "annual_median_wage": v(wage, RECORD, src, **({} if wage is not None else {"missing": "blank in source"})),
            })
        out[rt] = {"soc": v(soc, MODEL, "SOC mapping is model-judgment (CHANGE-BRIEF); report-only, zero effect on score"),
                   "rows": items}
    return out


def formd_crosscheck(company_keys, sample_glob=SEC_SAMPLE_GLOB):
    """Which companies appear in the shipped Form D samples (exact normalized name). Misses go to cannot-verify."""
    names = set()
    for f in sorted(glob.glob(sample_glob)):
        with open(f, encoding="utf-8") as fh:
            companies = json.load(fh)["companies"]
        for c in companies:
            n = c["company"].get("company_name_normalized")
            if n:
                names.add(n)
    matched = sorted(k for k in set(company_keys) if k in names)
    missing = sorted(k for k in set(company_keys) if k not in names)
    return {"matched": matched, "cannot_verify": [
        {"company_key": k, "reason": "funding not cross-checkable: company not in the shipped Form D sample"}
        for k in missing]}


# ── G1 persona input ──────────────────────────────────────────────────────
PERSONA_DATES = ["graduation_date", "opt_start_date", "unemployment_window_end"]


def load_persona(path):
    """G1: read the persona JSON; halt on a missing or invalid date or an impossible window."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return validate_persona(data, source=_rel(path))


def validate_persona(data, source="persona"):
    out = {"persona_id": data.get("persona_id"), "_source": source}
    for k in PERSONA_DATES:
        d = _date(data.get(k)) if data.get(k) is not None else None
        if d is None:
            raise GateHalt(f"G1 persona input: {k} missing or not an ISO date ({data.get(k)!r})")
        out[k] = d
    if out["unemployment_window_end"] <= out["opt_start_date"]:
        raise GateHalt("G1 persona input: unemployment_window_end must be after opt_start_date")
    lag = data.get("hiring_lag_days")
    if not isinstance(lag, int) or isinstance(lag, bool) or lag < 0:
        raise GateHalt(f"G1 persona input: hiring_lag_days must be a non-negative integer ({lag!r})")
    out["hiring_lag_days"] = lag
    used = data.get("unemployment_days_used")
    if not isinstance(used, int) or isinstance(used, bool) or used < 0:
        raise GateHalt(f"G1 persona input: unemployment_days_used must be a non-negative integer ({used!r})")
    out["unemployment_days_used"] = used
    # Fit may be partial: a role type without fit is blocked per role, not a whole-run halt.
    fit = data.get("fit") or {}
    out["fit"] = {rt: fit[rt] for rt in ROLE_KEYWORDS if isinstance(fit.get(rt), (int, float))
                  and not isinstance(fit.get(rt), bool) and 0 <= fit[rt] <= 1}
    return out


# ── G2 timeline gate ──────────────────────────────────────────────────────
def timeline_gate(persona, run_date):
    """G2: halt if the window (or OPT start) is already past; else factor 1.0 if run date + lag <= window end."""
    end, start, lag = persona["unemployment_window_end"], persona["opt_start_date"], persona["hiring_lag_days"]
    if run_date > end:
        raise GateHalt(f"G2 timeline: unemployment window ended {end.isoformat()}; timeline cannot be evaluated")
    if run_date > start:
        raise GateHalt(f"G2 timeline: OPT start {start.isoformat()} has passed; unemployment_days_used "
                       f"({persona['unemployment_days_used']}) must be re-entered by a human before the "
                       "timeline can be evaluated")
    ready = run_date + timedelta(days=lag)
    factor = 1.0 if ready <= end else 0.0
    return v(factor, INPUT, f"{persona['_source']} dates + hiring-lag assumption",
             arithmetic=f"{run_date.isoformat()} + {lag} days = {ready.isoformat()} "
                        f"{'<=' if factor else '>'} window end {end.isoformat()} -> {factor}",
             assumption=f"hiring_lag_days={lag} is an assumption, not a record")


# ── G4 posting checks + liveness ─────────────────────────────────────────
def load_posting_checks(path):
    """Read the human posting-check CSV; malformed rows are rejected with a reason, never repaired."""
    path = Path(path)
    valid, rejected = [], []
    with path.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != POSTING_COLUMNS:
            raise GateHalt(f"posting-check file must have columns exactly {POSTING_COLUMNS}, got {reader.fieldnames}")
        for i, row in enumerate(reader, start=2):
            src = f"{_rel(path)}#L{i}"
            row = {k: (row[k] or "").strip() for k in POSTING_COLUMNS}
            problems = []
            if not row["company"]:
                problems.append("company blank")
            if row["role_type"] not in ROLE_KEYWORDS:
                problems.append(f"role_type must be one of {sorted(ROLE_KEYWORDS)}")
            if not re.match(r"^https?://\S+$", row["url"]):
                problems.append("url missing or not http(s)")
            if _date(row["date_checked"]) is None:
                problems.append("date_checked not an ISO date")
            if row["status"] not in POSTING_STATUSES:
                problems.append(f"status must be one of {sorted(POSTING_STATUSES)}")
            if problems:
                rejected.append({"row": row, "source": src, "reason": "; ".join(problems)})
            else:
                row["date_checked"] = _date(row["date_checked"])
                row["company_key"] = normalize_company_name(row["company"])
                row["_source"] = src
                valid.append(row)
    return valid, rejected


def liveness_gate(role, checks, run_date, max_age_days=MAX_CHECK_AGE_DAYS):
    """G4: return (factor_value, None) from a current human check, or (None, reason) -> verify-posting list."""
    mine = [c for c in checks if c["company_key"] == role["company_key"] and c["role_type"] == role["role_type"]["value"]]
    if not mine:
        return None, "unchecked: no human posting check recorded"
    latest = max(mine, key=lambda c: c["date_checked"])
    d = latest["date_checked"]
    if d > run_date:
        return None, f"check dated {d.isoformat()}, after the run date {run_date.isoformat()}"
    age = (run_date - d).days
    if age > max_age_days:
        return None, (f"stale: checked {d.isoformat()}, {age} days before run "
                      f"(limit {max_age_days} days, your-input)")
    factor = POSTING_STATUSES[latest["status"]]
    return v(factor, INPUT, f"human posting check {latest['_source']}", url=latest["url"],
             date_checked=d.isoformat(), age_days=age, status=latest["status"]), None


# ── G5 pre-score evidence completeness ───────────────────────────────────
REQUIRED_EVIDENCE = [("sponsorship", "p"), ("sponsorship", "tier"), ("fit", "p"),
                     ("liveness", "factor"), ("timeline", "factor")]


def evidence_problems(role, required=REQUIRED_EVIDENCE):
    """G5: list every missing or malformed scorer input on a role; empty list means scoreable."""
    problems = []
    for block, field in required:
        item = (role.get(block) or {}).get(field)
        if not isinstance(item, dict) or item.get("value") is None:
            problems.append(f"{block}.{field} missing")
            continue
        if item.get("label") not in LABELS:
            problems.append(f"{block}.{field} label {item.get('label')!r} not one of {sorted(LABELS)}")
        if field == "tier":
            if not isinstance(item["value"], str) or not item["value"]:
                problems.append(f"{block}.{field} must be a non-empty string")
        elif not isinstance(item["value"], (int, float)) or isinstance(item["value"], bool) \
                or not 0 <= item["value"] <= 1:
            problems.append(f"{block}.{field} must be a number in [0, 1]")
    return problems


def assert_scoreable(roles, check=evidence_problems):
    """G5 final: halt the run if any role about to go to the scorer fails the evidence check."""
    bad = {r.get("role_id"): p for r in roles if (p := check(r))}
    if bad:
        raise GateHalt(f"G5 evidence completeness: {len(bad)} role(s) not scoreable: {bad}")
    return True


# ── assembly ──────────────────────────────────────────────────────────────
def build_plan(rows, persona, checks, run_date, rejected_checks=(), sample_glob=SEC_SAMPLE_GLOB):
    """Run every gate and sort each role into scoreable / blocked / network / verify-posting lists."""
    timeline = timeline_gate(persona, run_date)  # halts the run if the window is past
    cls = classify_companies(rows)
    plan = {"run_date": v(run_date.isoformat(), INPUT, "run parameter"), "timeline": timeline,
            "scoreable": [], "blocked": list(cls["blocked"]), "network": [], "verify_posting": [],
            "rejected_checks": list(rejected_checks)}
    entry_keys = {(c["company_key"], c["role_type"]["value"]) for c in cls["candidates"]}
    entry_companies = {c["company_key"] for c in cls["candidates"]}
    network_companies = {n["company_key"] for n in cls["network"]}

    for role in cls["candidates"]:
        row = role.pop("_row")
        rt = role["role_type"]["value"]
        role["funding_context"] = funding_context(row)
        spon, reason = map_sponsorship(row["Total Approvals"], row["_source"])
        role["sponsorship"] = spon
        if reason:
            plan["blocked"].append({**role, "reason": reason})
            continue
        if rt not in persona["fit"]:
            plan["blocked"].append({**role, "reason": f"fit missing for {rt}: not defaulted"})
            continue
        role["fit"] = {"p": v(persona["fit"][rt], INPUT, f"{persona['_source']} fit.{rt}")}
        role["timeline"] = {"factor": timeline}
        live, reason = liveness_gate(role, checks, run_date)
        if reason:
            plan["verify_posting"].append({**role, "reason": reason})
            continue
        role["liveness"] = {"factor": live}
        problems = evidence_problems(role)
        if problems:
            plan["blocked"].append({**role, "reason": "G5: " + "; ".join(problems)})
            continue
        plan["scoreable"].append(role)

    for n in cls["network"]:
        n.pop("_row", None)
        if any(c["company_key"] == n["company_key"] and c["role_type"] == n["role_type"]["value"] for c in checks):
            n["note"] = "posting check ignored: networking target, not an application"
        plan["network"].append(n)

    for c in checks:  # checks that point at nothing scoreable
        if (c["company_key"], c["role_type"]) in entry_keys or c["company_key"] in network_companies:
            continue
        if c["company_key"] in entry_companies:
            reason = f"role type {c['role_type']} is not an entry role at this company"
        else:
            reason = "not in matched sponsorship set (check the company name against the source CSV)"
        plan["blocked"].append(_blocked(c["company"], c["role_type"], c["_source"], reason,
                                        normalized_name=c["company_key"]))

    plan["cannot_verify"] = formd_crosscheck(
        [r["company_key"] for r in plan["scoreable"] + plan["verify_posting"]], sample_glob)["cannot_verify"]
    assert_scoreable(plan["scoreable"])
    plan["counts"] = {k: len(plan[k]) for k in ("scoreable", "blocked", "network", "verify_posting",
                                                 "rejected_checks", "cannot_verify")}
    return plan


def to_scorer_record(role):
    """Shape one scoreable role for scripts/score/role-scorer.mjs; evidence carries the record count."""
    s = role["sponsorship"]
    return {
        "role_id": role["role_id"],
        "company": role["company"]["value"],
        "title": role["role_type"]["value"],
        "sponsorship": {"p": s["p"]["value"], "tier": s["tier"]["value"], "source": INPUT},
        "fit": {"p": role["fit"]["p"]["value"], "source": INPUT},
        "liveness": {"factor": role["liveness"]["factor"]["value"], "source": INPUT},
        "timeline": {"factor": role["timeline"]["factor"]["value"], "source": INPUT},
        "evidence": {"total_approvals": s["approvals"]},
    }
