---
status: DRAFT
todos_open: 5
last_gate: null
attestation: null
recipe_version: 0.1.0
---

# newgrad-de-ml-optwindow — Data/ML Engineer triage inside the OPT unemployment window

## Executive summary

**What it does.** Takes the engine's company sponsorship data and sorts every company that has sponsored Data Engineer or Machine Learning Engineer roles into four lists: roles the existing scorer may judge, roles whose job posting must be checked first, senior-only companies to network with, and roles blocked for missing evidence. It then runs the existing scorer on the first list only.

**Who it is for.** A new graduate on an F-1 visa whose OPT has not started yet, targeting Data Engineer or ML Engineer roles at any company size, industry, or US location — someone for whom the 90-day unemployment clock after OPT starts is the binding constraint.

**What it decides.** Which companies deserve the scarce daily application hours, which need a posting checked before any time is spent, and which are networking targets instead. It refuses to guess: a missing value stays missing, a posting nobody checked is never scored, and an AI-reported posting status that a recorded tool check contradicts is sent back for checking. In its first run on shipped data, no posting had been checked by a human, so every scored decision is provisional.

**Lifecycle status.** The prototype runs end to end on shipped sample data (commit bc723e6, run 2026-10-02), but the lifecycle stage is held at DRAFT because SNICKERDOODLE requires zero open TODO items before SPECIFIED (SNICKERDOODLE.md line 58; 5 are open) and, before RUNNABLE-SAMPLE, a run-log entry plus audit files that have been generated and read (line 59; neither exists yet). To advance: close each of the 5 proposed-addition TODO items with the closure evidence its type requires (lines 79 and 81: a DEV item needs the script, passing conformance, and its handoff condition met; a DATA SOURCE item needs the file at the named path plus a one-line provenance note, closed by a human) to reach SPECIFIED; then add the run-log entry `logs/runs/2026fa-Sreevarshann-1.md` (CONTRIBUTING.md puts student run logs there instead of `logs/RUN_LOG.md`) and an audit of the sample run that a named human has read, to reach RUNNABLE-SAMPLE.

Two customers: this file is for the agent; `recipes/cases/2026fa/Sreevarshann-newgrad-de-ml-optwindow.card.md` is for the human.

**Handoff condition (done when):** a run writes `report.md` and `run-log.json` under `course/2026fa/submissions/Sreevarshann/runs/<run-date>/`; every role appears on exactly one list; every emitted value carries a `record` / `model-judgment` / `your-input` label; the scorer received only roles that passed G1–G5; and the report's first section states whether the G4 human liveness gate was cleared. "Looks right" is not the condition.

Chapters claimed: Ch 7 (sponsorship), Ch 8 (liveness), Ch 10 (timeline), Ch 11 (composite), with the 3-3-2 day from Ch 2 for next actions. Ch 9 role quality is shown report-only.

## Purpose and source inventory

| Source | Path | Use | Label |
|---|---|---|---|
| Company sponsorship data | `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` | 7 non-personal columns: `company_name`, `top_job_titles_sponsored`, `Total Approvals`, `Total Denials`, `Approval_Rate` (0–100 %), `latest_funding_date`, `latest_funding_stage` | record |
| BLS wages | `data/bls/compact/soc_occupation_compact.csv` | national median for SOC 15-1243 / 15-2051, report-only | record (SOC mapping: model-judgment) |
| Form D samples | `data/sec/form-d/processed/sample/*.sample.json` | funding cross-check by normalized name | record |
| Name normalizer | `scripts/sec/entity-resolution.py` → `normalize_company_name` | every company-name join (stdlib-only; see CHANGE-BRIEF R1) | — |
| Scorer | `scripts/score/role-scorer.mjs` | the Ch.11 composite, CLI only | — |
| Liveness tool | `scripts/ats/check-liveness.mjs` (+ `liveness-browser.mjs`, `liveness-core.mjs`) | recorded cross-check of posting URLs | record |
| Persona (fictional) | `search/examples/meera-krishnan/profile.yml`; fields used: `scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/fixtures/persona-meera-krishnan.json` | dates, 60-day hiring-lag assumption, fit per role | your-input |
| Posting checks | `course/2026fa/submissions/Sreevarshann/inputs/posting-checks.csv` | status per company + role type; `checked_by` decides the label | your-input (human) / model-judgment (AI); `tool_result` record |
| Plan of record | `course/2026fa/submissions/Sreevarshann/CHANGE-BRIEF.md` (revisions R1–R5) | the rules this recipe runs | — |
| Prototype | `scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/` (`core.py`, `run.py`) | gates, plan, report | — |

**Commands** (from the repo root):

```bash
python3 scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/run.py
python3 -m unittest discover -s scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/tests -v
npm run score -- course/2026fa/submissions/Sreevarshann/runs/<run-date>/roles.json --out-dir course/2026fa/submissions/Sreevarshann/runs/<run-date>
npm run ats:liveness -- <posting-url>
```

`run.py` calls the scorer itself (third command) only when at least one role is scoreable; the scorer is never imported or re-implemented. `run.py` options: `--run-date`, `--persona`, `--checks`, `--out-root`, `--overwrite`.

**Network.** `run.py`, `core.py`, and the tests make **no network calls**. `npm run ats:liveness` contacts **only the posting URLs in the check file**, plus whatever those pages load (it drives a headless Chromium); it needs Playwright's Chromium installed outside the repo and writes nothing to disk.

## Proposed additions

1. **Funding vote for the scorer** — [TODO: DEV] The engine treats funding as one of five evidence components, but `role-scorer.mjs` has no funding term (weights at lines 34–43). Adding one needs a maintainer change to the scorer and a human-defined weight and date-to-vote mapping, with reasoning; until then funding stays report-only and is never folded into fit or sponsorship.
2. **Recompute the window after OPT start** — [TODO: DEV] Today any run after OPT start halts (CHANGE-BRIEF R2). Instead, require unemployment days used with an as-of date and recompute the remaining window, so the timeline gate can actually close rather than halt.
3. **Full Form D quarters** — [TODO: DATA SOURCE] The shipped samples (first 50 companies per quarter) match none of the 114 target companies, so funding cannot be cross-checked. The full quarters are gitignored and fetched via `scripts/sec/`; a run with them would turn "cannot verify" into a record.
4. **Human posting checks for every scored role** — [TODO: DATA SOURCE] Run 1 had none; all five checks came from an AI web search. Each role the scorer judges needs a human-recorded URL, date, and status (≤ 7 days old) before its decision stops being provisional.
5. **Scorer exports** — [TODO: DEV] `role-scorer.mjs` exports nothing and runs `main()` on load (line 185), so the documented import route (`CONFIG`, `SRC`, `applyProfile`, `scoreRole`) is impossible. Exporting them is a maintained-file change for a maintainer; this recipe uses the CLI meanwhile.

## Phase gates

Each gate is a hard stop. Liveness and timeline are **gates, not votes**: they multiply the composite or stop the run; they never add to it. Gate tests run offline:

```bash
python3 -m unittest discover -s scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/tests -k <filter>
```

| Gate | Testable condition | Fail → | Test filter | Who clears |
|---|---|---|---|---|
| G1 persona input | persona dates parse; window end after OPT start; hiring lag and days used are non-negative integers. Missing fit does **not** halt (R2) — that role is blocked | halt naming the field | `test_g1`, `fixture_persona` | machine |
| G2 timeline gate | halt if the window end or OPT start is past; else factor 1.0 if run date + 60 days ≤ window end, else 0.0. For this persona it is effectively a halt (R2) | halt | `test_g2` | machine |
| G3 seniority review | every matched title listed with its class; counts reproduce 114 / 64 / 50 | stop: fix rule by logged revision only | `reproduces_recorded_funnel` | **named human** reads the title lists in `report.md` |
| G4 liveness | a role is scored only with a check for its company + role type, dated ≤ run date and ≤ 7 days old. `open` → 1.0; `closed` / `not found` → 0.0. A check is human (your-input, clears G4) unless `checked_by` says "not human-verified" (model-judgment, scored but G4 **not** cleared, run provisional) — R3 | verify-posting list | `LivenessTest`, `CheckedByTest` | **named human** for clearance |
| R4 conflict rule | a model-judgment status contradicted by `tool_result` (open vs expired; closed/not found vs active) is not scored; a human status is never overridden (flagged instead); `uncertain` never overrides | verify-posting list with both values | `ConflictTest` | machine |
| R5 tie-break | newest check wins; on a same-date tie a human check beats an AI check | — | `ConflictTest` | machine |
| G5 evidence completeness | every role sent to the scorer has sponsorship p + tier, fit p, liveness factor, timeline factor, each labelled; the run halts if one slips through | blocked list, or halt | `G5Test` (incl. the `BROKEN-*` mutant test) | machine |
| G6 output adequacy | `report.md` opens with the executive summary carrying any G4 warning, then the sections in the output contract | stop before use | `report_opens_with_summary` | **named human** reads the report against live postings |

## Can verify / Cannot verify

**Can verify**
- Which companies in the 80 Days data have sponsored titles matching the 8 role keywords, and how they split by seniority (114 → 64 entry-eligible / 50 senior-only), each traced to a CSV line.
- The recorded H-1B approval count per company, and the tier and p this recipe's cut-offs assign (≥ 50 → 0.8 Proven; 10–49 → 0.6 likely; 2–9 → 0.4 possible; < 2 or unparseable → blocked).
- Whether a role has every input the scorer needs, before the scorer sees it — and that the scorer received only such roles.
- Whether a posting check exists, how old it is, who did it (human vs AI), and whether the liveness tool's recorded result contradicts it.
- The timeline arithmetic for the persona's 90-day window, shown in the report.
- That missing values stay missing: a blank funding date is reported as "blank in source", never 0.

**Cannot verify**
- **No human posting checks in run 1.** All five checks came from an AI web search; no scored decision is final.
- **AMGEN's AI "open" was contradicted** by ats:liveness returning HTTP 404; TWILIO's "open" was contradicted by "insufficient content". Both went back to verify-posting (R4).
- **ats:liveness has no "not found" result** (removed and closed postings both read `expired`), and it **reads bot-blocked or slow pages as expired** ("insufficient content").
- **Sponsorship approvals are company-wide, not role-specific**: a company with 800 approvals mostly for other roles still reads Proven for Data Engineer.
- **Only "top" sponsored titles are visible**: companies that sponsor these roles outside their top-titles list are invisible, and 28,812 of 30,369 rows carry no title data at all.
- **"AI Engineer" has zero matched records**: the one "AI Engineering Lead" string is excluded by the keyword rule; the AI side of the search is ML Engineer titles.
- **Zero Form D sample matches** for the 114 target companies; funding cannot be cross-checked with shipped data.
- **Funding dates are mostly stale**: 5 of 64 entry-eligible companies (7 of 114) have a funding date in the last 24 months.
- **Possible wrong company matches** (model-judgment, unverified): HUMAN INC's 1,382 approvals look high for that company; PATHAI INC and PATHRAI INC both show ML Engineer, Proven, 78 approvals — likely one company entered twice.
- **The SOC mapping is model-judgment** (15-1243 Data Engineer, 15-2051 ML Engineer); BLS has no occupation for either role.
- **"Data Analytics Engineer" titles are missed**: the keyword `data engineer` does not match when a word sits between.
- **The timeline gate is effectively a halt for this persona** (R2): with a 60-day lag, factor 0.0 is unreachable; any run after OPT start halts.

## How the Facts that bite apply

- **Role quality weight 0.0** (`role-scorer.mjs` line 37): BLS wages are shown report-only and change no decision.
- **`bls:local-wage` feeds nothing**: this recipe does not use it.
- **Only SEC samples ship**: Form D is used only as a cross-check against the samples; zero matches are listed under Cannot verify.
- **Planned directories and the `snickerdoodle` CLI do not exist**: this recipe references neither; every path above exists today.
- **Funding:** the assignment lists funding as a vote, but this recipe keeps it report-only because the scorer has no funding term; adding one is proposed addition 1.

## Output contract

### Agent output
File: `course/2026fa/submissions/Sreevarshann/runs/<run-date>/run-log.json`
Contains: run date and command; each input's path and SHA-256; status (`complete` / `halted` / `scorer-failed`) and any halt reason; scorer command, exit code, stdout/stderr; counts; the funnel; each scored role's scorer input and output; the full labelled plan (scoreable, blocked, network, verify-posting, rejected checks, cannot-verify); BLS context. Also `roles.json` (scorer input) and, when the scorer ran, its own `role-scores.json` / `role-scores.md`.

### Human report
File: `course/2026fa/submissions/Sreevarshann/runs/<run-date>/report.md`
Reader: the student deciding where to spend tomorrow's hours.
Decision enabled: apply, verify a posting, network, or drop — per company.
Sections, in order: Executive summary (headline warnings first), Run record, Funnel, Scored roles (with the liveness cross-check), Verify-posting list (conflict reasons first), Network list, Blocked list, Cannot verify, Report-only context, Next action per company.

## Stop conditions

- Stop if the persona fails G1, the window or OPT start is past (G2), or the posting-check file has missing/unknown columns — the run halts and writes only `run-log.json`.
- Stop if a role about to be scored lacks any required input (G5) — never let the scorer default it.
- Stop if the scorer exits nonzero or omits a role it was sent.
- Stop if asked to record a human check without a real URL and observation — never fill one in.
- Stop if asked to change cut-offs or keywords to hit a skip-rate target — that is rigging; skipping happens at the filter stage.
- Stop before overwriting an existing run folder unless `--overwrite` is given.

## Next action per result (the 3-3-2 day)

The Ch.2 3-3-2 day: 2 hours targeted applying, 3 hours networking, 3 hours portfolio.

| Result | Next action |
|---|---|
| Scored **Apply** (G4 human-cleared) | Tailor an application — this is what the 2 applying hours are for. If G4 was not cleared, check the posting first. |
| **Verify-posting** | Check the posting first (find it, open it, record URL, date, status); no application time until then. |
| **Senior-only** (network list) | Networking target — the 3 networking hours: find a contact on the team; do not apply to the senior posting. |
| Scored **Skip** | Stop spending time on it. If the skip came from an AI-reported "not found", one quick human check first. |
| Scored **Consider** | Read the posting; decide inside the 2 applying hours or drop. |
| **Blocked** | Fix the input named in the reason, then re-run. |

## Run-log template (`logs/runs/2026fa-Sreevarshann-<n>.md`)

Follows `recipes/_shared.md`; never edit `logs/RUN_LOG.md`. A log longer than a screen opens with an executive summary.

```markdown
## YYYY-MM-DD — newgrad-de-ml-optwindow run <n>

- **Recipe:** recipes/cases/2026fa/Sreevarshann-newgrad-de-ml-optwindow.md v0.1.0
- **Inputs:** persona fixture, posting-checks.csv (rows: N; human: N; AI: N), 80 Days CSV, BLS compact CSV — SHA-256 in run-log.json
- **Command:** python3 scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/run.py --run-date YYYY-MM-DD
- **Outputs:** course/2026fa/submissions/Sreevarshann/runs/YYYY-MM-DD/{report.md, run-log.json, roles.json, role-scores.json, role-scores.md}
- **Result:** counts (scoreable / verify-posting / network / blocked), scorer result (Apply / Consider / Skip), G4 cleared yes/no
- **Gate decisions:** G3 and G6 — cleared by <name>, <date>, or not cleared and why
- **Open issues:** what did not work or is still missing
```
