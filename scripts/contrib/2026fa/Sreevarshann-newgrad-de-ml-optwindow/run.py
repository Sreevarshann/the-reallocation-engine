#!/usr/bin/env python3
"""newgrad-de-ml-optwindow: end-to-end run (2026fa, Sreevarshann).

One command from the repo root:
    python3 scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/run.py

Builds the gated plan (core.py), writes roles.json, calls the existing scorer through
its CLI (npm run score -- roles.json --out-dir <run folder>), then writes run-log.json
(for agents) and report.md (for the person). Stdlib only. Never re-implements the scorer.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import core  # noqa: E402

HERE = Path(__file__).resolve().parent
SUBMISSION = core.REPO / "course/2026fa/submissions/Sreevarshann"
DEFAULT_PERSONA = HERE / "fixtures/persona-meera-krishnan.json"
DEFAULT_CHECKS = SUBMISSION / "inputs/posting-checks.csv"
DEFAULT_OUT_ROOT = SUBMISSION / "runs"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def call_scorer(roles_path, out_dir):
    """Run the maintained scorer through its CLI. Returns (exit_code, stdout, stderr, command)."""
    cmd = ["npm", "run", "score", "--", core._rel(roles_path), "--out-dir", core._rel(out_dir)]
    p = subprocess.run(cmd, cwd=core.REPO, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr, " ".join(cmd)


def funnel(rows, plan, checks):
    with_titles = sum(1 for r in rows if r["top_job_titles_sponsored"].strip())
    cls_sources = {}
    for lst in ("scoreable", "verify_posting", "network", "blocked"):
        for r in plan[lst]:
            if isinstance(r.get("company"), dict) and r.get("company_class"):
                cls_sources.setdefault(r["company_class"]["value"], set()).add(r["company"]["source"])
    entry = len(cls_sources.get("entry-eligible", ()))
    senior = len(cls_sources.get("senior-only", ()))
    return [
        ("Companies in the sponsorship dataset", len(rows), "record"),
        ("…with any sponsored-job-title data", with_titles, "record"),
        ("…matching the 8 role keywords", entry + senior, "record (keywords: your-input)"),
        ("…entry-eligible (apply candidates)", entry, "record (seniority rule: your-input)"),
        ("…senior-only (networking list)", senior, "record (seniority rule: your-input)"),
        ("Posting checks loaded (valid rows)", len(checks), "label per row (see verify / scored tables)"),
        ("Roles sent to the scorer", len(plan["scoreable"]), "after gates G1–G5"),
    ]


def next_action(item, kind, scored=None):
    """Fixed rules (this report's logic, not a model judgment) for what the person does next."""
    if kind == "scored":
        live = item["liveness"]["factor"]
        reason = (scored or {}).get("reason", "")
        if reason.startswith("gated: liveness"):  # the scorer's own wording; no threshold copied here
            who = "a human" if live["g4_human_cleared"] else "an AI web search (not human-verified)"
            return (f"Posting reported '{live['status']}' by {who}. Check the company careers site yourself "
                    "before dropping it; record a human check with the URL and date.")
        rec = scored.get("recommendation") if scored else None
        if not live["g4_human_cleared"]:
            return f"Scorer says {rec}, provisionally. Open the posting yourself and record a human check first."
        return {"Apply": "Apply.", "Consider": "Consider: decide after reading the posting.",
                "Skip": "Skip."}.get(rec, "Read the scorer reason.")
    if kind == "verify":
        if item["reason"].startswith(core.CONFLICT_REASON):
            return "Open the posting yourself: the AI status and the liveness tool disagree. Record a human check."
        if item["reason"].startswith("stale"):
            return "Re-check the posting (the last check is older than 7 days) and record the new date."
        return "Find a current Data/ML Engineer posting on the company's careers site and record a human check."
    if kind == "network":
        return "Networking target: find a contact on the team; do not apply to the senior posting."
    return "Fix the input named in the reason, then re-run."


def num(x):
    return f"{x:g}" if isinstance(x, (int, float)) and not isinstance(x, bool) else "—"


def esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def render_report(plan, run_record, funnel_rows, scored_by_id, scorer_note, bls):
    o = []
    rd = run_record["run_date"]
    o.append(f"# Run report — newgrad-de-ml-optwindow · {rd}")
    o.append("")
    o.append("## Executive summary")
    o.append("")
    for w in plan["headline_warnings"]:  # headline warnings come first, before anything else
        o.append(f"> **Provisional — read first.** {w}")
        o.append("")
    o.append("**What this is.** The first end-to-end run of a tool that sorts companies for a new-graduate F-1 "
             "student targeting Data Engineer and ML Engineer roles: which to apply to, which to verify first, "
             "which are networking targets, and which are blocked — each with the evidence behind it.")
    o.append("")
    o.append("**Why read it.** It shows what the evidence actually supports today, and where it stops. Every "
             "value is labelled as a record, a model judgment, or the student's own input.")
    o.append("")
    c = plan["counts"]
    recs = {}
    for r in scored_by_id.values():
        recs[r["recommendation"]] = recs.get(r["recommendation"], 0) + 1
    rec_txt = ", ".join(f"{k} {v}" for k, v in sorted(recs.items())) or "none (scorer not run)"
    o.append("**What it found.**")
    o.append(f"- {c['scoreable']} role(s) reached the scorer; result: {rec_txt}.")
    o.append(f"- {c['verify_posting']} role(s) need a posting checked before they can be scored; "
             f"{sum(1 for v in plan['verify_posting'] if v['reason'].startswith(core.CONFLICT_REASON))} of them "
             "because an AI-reported status was contradicted by the liveness tool.")
    o.append(f"- {c['network']} role(s) at senior-only companies are networking targets, not applications.")
    o.append(f"- {c['blocked']} role(s) blocked for missing or unusable evidence.")
    o.append("- No posting in this run was checked by a human, so no decision here is final.")
    o.append("")

    o.append("## Run record")
    o.append("")
    o.append(f"- Run date: {rd} · persona: {run_record['persona_id']} (fictional)")
    o.append(f"- Command: `{run_record['command']}`")
    o.append(f"- Scorer: {scorer_note}")
    o.append(f"- Timeline gate: {plan['timeline']['arithmetic']} (lag is an assumption, not a record)")
    for name, info in run_record["inputs"].items():
        o.append(f"- Input `{info['path']}` sha256 `{info['sha256'][:12]}…`")
    o.append(f"- Outputs: `{run_record['outputs']['report']}`, `{run_record['outputs']['run_log']}`, "
             f"`{run_record['outputs']['roles']}`" + (", scorer `role-scores.json` / `role-scores.md`"
                                                      if run_record["scorer"]["ran"] else ""))
    o.append("")

    o.append("## Funnel")
    o.append("")
    o.append("| Stage | Count | Label |")
    o.append("|---|---|---|")
    for stage, n, label in funnel_rows:
        o.append(f"| {stage} | {n} | {label} |")
    o.append("")

    o.append("## Scored roles")
    o.append("")
    if not plan["scoreable"]:
        o.append("No role reached the scorer in this run.")
    else:
        o.append("| Company | Role | Approvals [record] | Tier / p [your-input] | Fit [your-input] | Liveness | "
                 "Timeline [your-input] | Composite | Scorer result | Scorer reason | G4 human-cleared |")
        o.append("|---|---|---|---|---|---|---|---|---|---|---|")
        for r in plan["scoreable"]:
            s, live, sc = r["sponsorship"], r["liveness"]["factor"], scored_by_id.get(r["role_id"], {})
            o.append(f"| {esc(r['company']['value'])} | {r['role_type']['value']} | {num(s['approvals']['value'])} | "
                     f"{s['tier']['value']} / {s['p']['value']} | {r['fit']['p']['value']} | "
                     f"{live['value']} [{live['label']}] ({live['status']}) | {r['timeline']['factor']['value']} | "
                     f"{sc.get('composite', '—')} | **{sc.get('recommendation', '—')}** | {esc(sc.get('reason', '—'))} | "
                     f"{'yes' if live['g4_human_cleared'] else '**no**'} |")
        o.append("")
        o.append("Liveness cross-check (ats:liveness, record) for scored roles:")
        o.append("")
        for r in plan["scoreable"]:
            live = r["liveness"]["factor"]
            tr = live.get("tool_result")
            o.append(f"- {esc(r['company']['value'])}: status `{live['status']}` [{live['label']}] · tool "
                     + (f"`{tr['value']}` — {esc(live['tool_reason']['value'])}" if tr else "not run"))
        if plan["tool_disagreements"]:
            o.append("")
            o.append("Human status vs tool disagreements (human governs):")
            for d in plan["tool_disagreements"]:
                o.append(f"- {d['role_id']}: {esc(d['note'])}")
    o.append("")

    o.append("## Verify-posting list")
    o.append("")
    o.append("| Company | Role | Tier | Approvals [record] | Reason |")
    o.append("|---|---|---|---|---|")
    for r in sorted(plan["verify_posting"], key=lambda x: (not x["reason"].startswith(core.CONFLICT_REASON),
                                                           x["company"]["value"])):
        s = r.get("sponsorship", {})
        o.append(f"| {esc(r['company']['value'])} | {r['role_type']['value']} | "
                 f"{s.get('tier', {}).get('value', '—')} | {num(s.get('approvals', {}).get('value'))} | "
                 f"{esc(r['reason'])} |")
    o.append("")

    o.append("## Network list (senior-only — networking targets, never scored)")
    o.append("")
    o.append("| Company | Role | Matched senior titles [record] | Note |")
    o.append("|---|---|---|---|")
    for r in sorted(plan["network"], key=lambda x: x["company"]["value"]):
        o.append(f"| {esc(r['company']['value'])} | {r['role_type']['value']} | "
                 f"{esc('; '.join(r['matched_titles']['value']))} | {esc(r.get('note', ''))} |")
    o.append("")

    o.append("## Blocked list")
    o.append("")
    if not plan["blocked"]:
        o.append("Nothing blocked in this run.")
    else:
        o.append("| Company | Role | Reason |")
        o.append("|---|---|---|")
        for r in plan["blocked"]:
            rt = r["role_type"]["value"] if isinstance(r.get("role_type"), dict) else r.get("role_type")
            o.append(f"| {esc(r['company']['value'])} | {rt} | {esc(r['reason'])} |")
    if plan["rejected_checks"]:
        o.append("")
        o.append("Rejected posting-check rows:")
        for r in plan["rejected_checks"]:
            o.append(f"- {r['source']}: {esc(r['reason'])}")
    o.append("")

    o.append("## Cannot verify")
    o.append("")
    tool_limits = [x for x in plan["cannot_verify"] if x["company_key"] is None]
    formd = sorted(x["company_key"] for x in plan["cannot_verify"] if x["company_key"] is not None)
    for x in tool_limits:
        o.append(f"- {x['reason']}")
    if formd:
        o.append(f"- Funding not cross-checkable for {len(formd)} companies: none appear in the shipped Form D "
                 "sample (full quarters are not in a fresh clone). Normalized names: " + ", ".join(formd) + ".")
    o.append("- Whether any posting is live: no human checked a posting in this run.")
    o.append("- Sponsorship strength is company-wide, not role-specific; 'top' titles only.")
    o.append("")

    o.append("## Report-only context (no effect on any score)")
    o.append("")
    o.append("| Role | SOC [model-judgment] | O*NET title [record] | National annual median wage, 2024 [record] |")
    o.append("|---|---|---|---|")
    for rt, b in bls.items():
        for row in b["rows"]:
            w = row["annual_median_wage"]["value"]
            o.append(f"| {rt} | {b['soc']['value']} | {esc(row['title']['value'])} | "
                     f"{f'{w:,.0f}' if w is not None else 'blank in source'} |")
    o.append("")
    if plan["scoreable"]:
        o.append("| Company | Latest funding date [record] | Stage [record] | Approval rate % [record, not scored] |")
        o.append("|---|---|---|---|")
        for r in plan["scoreable"]:
            f = r["funding_context"]
            o.append(f"| {esc(r['company']['value'])} | {f['latest_funding_date']['value'] or 'missing (blank in source)'} | "
                     f"{f['latest_funding_stage']['value'] or 'missing'} | {f['approval_rate_pct']['value']} |")
        o.append("")

    o.append("## Next action per company")
    o.append("")
    o.append("Fixed rules from this report's logic, not a model judgment.")
    o.append("")
    o.append("| Company | Role | List | Next action |")
    o.append("|---|---|---|---|")
    for r in plan["scoreable"]:
        o.append(f"| {esc(r['company']['value'])} | {r['role_type']['value']} | scored | "
                 f"{esc(next_action(r, 'scored', scored_by_id.get(r['role_id'])))} |")
    for r in sorted(plan["verify_posting"], key=lambda x: x["company"]["value"]):
        o.append(f"| {esc(r['company']['value'])} | {r['role_type']['value']} | verify-posting | "
                 f"{esc(next_action(r, 'verify'))} |")
    for r in sorted(plan["network"], key=lambda x: x["company"]["value"]):
        o.append(f"| {esc(r['company']['value'])} | {r['role_type']['value']} | network | "
                 f"{esc(next_action(r, 'network'))} |")
    for r in plan["blocked"]:
        rt = r["role_type"]["value"] if isinstance(r.get("role_type"), dict) else r.get("role_type")
        o.append(f"| {esc(r['company']['value'])} | {rt} | blocked | {esc(next_action(r, 'blocked'))} |")
    o.append("")
    return "\n".join(o) + "\n"


def main(argv=None, scorer=call_scorer):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--run-date", default=date.today().isoformat(), help="ISO date (default: today)")
    ap.add_argument("--persona", default=str(DEFAULT_PERSONA))
    ap.add_argument("--checks", default=str(DEFAULT_CHECKS))
    ap.add_argument("--out-root", default=str(DEFAULT_OUT_ROOT))
    ap.add_argument("--overwrite", action="store_true", help="replace an existing run folder's outputs")
    a = ap.parse_args(argv)

    run_date = date.fromisoformat(a.run_date)
    out_dir = Path(a.out_root) / run_date.isoformat()
    report_path, log_path, roles_path = out_dir / "report.md", out_dir / "run-log.json", out_dir / "roles.json"
    if report_path.exists() and not a.overwrite:
        print(f"refusing to overwrite existing run outputs in {core._rel(out_dir)} (use --overwrite)")
        return 3

    command = "python3 " + core._rel(Path(__file__)) + (f" {' '.join(argv)}" if argv else "")
    inputs = {"persona": a.persona, "posting_checks": a.checks, "companies": str(core.CSV_PATH),
              "bls": str(core.BLS_PATH)}
    run_record = {"run_date": run_date.isoformat(), "command": command,
                  "outputs": {"report": core._rel(report_path), "run_log": core._rel(log_path),
                              "roles": core._rel(roles_path)}}
    # Check every input exists before hashing it: a missing file is a clean halt, never a traceback.
    missing = [(k, p) for k, p in inputs.items() if not Path(p).is_file()]
    if missing:
        msg = "input file not found: " + "; ".join(f"{k} = {core._rel(p)}" for k, p in missing)
        print(f"HALT: {msg}")
        out_dir.mkdir(parents=True, exist_ok=True)
        run_record["inputs"] = {k: {"path": core._rel(p), "exists": Path(p).is_file()} for k, p in inputs.items()}
        log_path.write_text(json.dumps({**run_record, "status": "halted", "halt": msg}, indent=2) + "\n")
        print(f"run-log: {core._rel(log_path)}")
        return 2
    run_record["inputs"] = {k: {"path": core._rel(p), "sha256": sha256(p)} for k, p in inputs.items()}
    try:
        persona = core.load_persona(a.persona)
        run_record["persona_id"] = persona["persona_id"]
        checks, rejected = core.load_posting_checks(a.checks)
        rows = core.load_companies()
        plan = core.build_plan(rows, persona, checks, run_date, rejected_checks=rejected)
    except core.GateHalt as e:
        print(f"HALT: {e}")
        out_dir.mkdir(parents=True, exist_ok=True)
        log_path.write_text(json.dumps({**run_record, "status": "halted", "halt": str(e)}, indent=2) + "\n")
        print(f"run-log: {core._rel(log_path)}")
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)
    records = [core.to_scorer_record(r) for r in plan["scoreable"]]
    roles_path.write_text(json.dumps(records, indent=2) + "\n")
    print(f"plan: {plan['counts']}  provisional={plan['provisional']}")
    print(f"roles.json: {len(records)} role(s) -> {core._rel(roles_path)}")

    scored_by_id = {}
    if not records:
        scorer_note = "not run: zero scoreable roles"
        print("scorer: skipped — zero scoreable roles")
        run_record["scorer"] = {"ran": False, "reason": "zero scoreable roles"}
    else:
        code, out, err, cmd = scorer(roles_path, out_dir)
        print(f"scorer: $ {cmd}")
        print(out.rstrip())
        if err.strip():
            print(err.rstrip(), file=sys.stderr)
        run_record["scorer"] = {"ran": True, "command": cmd, "exit_code": code, "stdout": out, "stderr": err}
        if code != 0:
            print(f"HALT: scorer exited {code}")
            log_path.write_text(json.dumps({**run_record, "status": "scorer-failed", "plan": plan},
                                           indent=2, default=str) + "\n")
            return 1
        scores = json.loads((out_dir / "role-scores.json").read_text())
        scored_by_id = {s["role_id"]: s for s in scores["roles"]}
        missing = [r["role_id"] for r in records if r["role_id"] not in scored_by_id]
        if missing:
            print(f"HALT: scorer output lacks roles {missing}")
            return 1
        scorer_note = f"`{cmd}` → exit 0; results read from `role-scores.json`"
        run_record["scorer"]["outputs"] = [core._rel(out_dir / "role-scores.json"), core._rel(out_dir / "role-scores.md")]

    bls = core.bls_context()
    fun = funnel(rows, plan, checks)
    report_path.write_text(render_report(plan, run_record, fun, scored_by_id, scorer_note, bls))
    log = {**run_record, "status": "complete", "provisional": plan["provisional"], "counts": plan["counts"],
           "funnel": [{"stage": s, "count": n, "label": lbl} for s, n, lbl in fun],
           "scored": [{"role_id": r["role_id"], "scorer_input": rec, "scorer_output": scored_by_id.get(r["role_id"])}
                      for r, rec in zip(plan["scoreable"], records)],
           "plan": plan, "bls_context": bls}
    log_path.write_text(json.dumps(log, indent=2, default=str) + "\n")
    print(f"report: {core._rel(report_path)}")
    print(f"run-log: {core._rel(log_path)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
