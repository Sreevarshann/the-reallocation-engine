# CHANGE BRIEF — newgrad-de-ml-optwindow · 2026fa · Sreevarshann

## Executive summary

**What this is.** The plan, written before any code, for a small tool that helps a new-graduate international student on an F-1 visa decide where to spend scarce application effort when targeting Data Engineer and Machine Learning Engineer roles. It reuses the engine's existing company, sponsorship, wage, and scoring pieces rather than rebuilding them.

**Why read it.** The engine's scorer quietly treats missing evidence as either zero or as a pass. A student whose work permission carries a fixed 90-day unemployment clock cannot afford a recommendation built on evidence nobody checked. This brief commits in advance to what the tool will refuse to guess, what a human must check by hand, and what we expect it to get wrong — so the eventual results can be judged against a record written before them.

**What it decides.**
- Companies are narrowed first by real sponsorship history and job-title evidence, then by seniority; most of the "skipping" happens there, before anything is scored.
- No company reaches the scorer unless a human has checked a real posting by hand within the last week and recorded the link and date; everything else goes to a "verify posting or network first" list.
- A role with any missing input — fit, sponsorship, posting check, or timeline — is blocked with a stated reason, never filled with a default.
- Funding and wage data are shown as context but do not change any score, because the current scorer has no place for them.
- We predict the score itself will skip almost nothing among roles with an open posting, and say plainly why that is not being "fixed" by tuning thresholds.

## The funnel (record unless marked)

| Stage | Count | Source / label |
|---|---|---|
| Companies in the sponsorship dataset | 30,369 | record |
| …with any sponsored-job-title, approval, or salary data | 1,557 | record — the other 28,812 are blank on all of these together |
| …whose sponsored titles match the 8 role keywords | 114 | record (keywords: your-input) |
| …entry-eligible (≥1 non-senior matched title) | 64 → apply candidates | record (seniority rule: your-input) |
| …senior-only | 50 → networking list, never scored | record (seniority rule: your-input) |
| …with a current human posting check (≤ 7 days old) | N (planned 4–5) | your-input |

Breakdown of the 64 entry-eligible roles (one entry-level role type per company): Data Engineer 33, ML Engineer 31; sponsorship tier Proven 22, likely 25, possible 17.

## Career situation (fictional persona) and engine layers used

The persona and all dates are fictional; the situation type (F-1 new grad, OPT not started, Data/ML Engineer roles) is the one this recipe is designed for. Persona: **Meera Krishnan**, a new fictional persona at `search/examples/meera-krishnan/profile.yml` (declared exception — see below). Every value is your-input.

| Field | Value |
|---|---|
| Program | MS, Data Science (STEM), fictional university; graduating 2026-12-12 |
| Status | F-1; OPT not started; OPT start (EAD) 2027-01-15 |
| Unemployment window | 90 days from OPT start; ends 2027-04-15; 0 days used |
| OPT end date | not set — missing, not estimated |
| STEM extension | not set for this persona — missing |
| Target roles | Data Engineer (fit 0.7), ML Engineer (fit 0.5) — self-assessed |
| Company preference | any size, any industry, any US location |
| Hiring lag | 60 days — an **assumption**, not a record |

**Engine layers used:** Sponsorship (Ch.7) — scored vote from approval counts in the 80 Days dataset · Liveness (Ch.8) — gate, from human posting checks only · Role quality (Ch.9) — report-only (scorer weight is 0) · Timeline (Ch.10) — gate, from the persona's 90-day window · Funding — report-only context, proposed as a future vote · Composite (Ch.11) — the existing scorer, run as a command-line tool.

## Existing data and scripts reused (paths confirmed to exist 2026-10-02)

| Path | Use |
|---|---|
| `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` | companies, `top_job_titles_sponsored`, `Total Approvals`, `Total Denials`, `Approval_Rate`, `latest_funding_date`, `latest_funding_stage` |
| `data/bls/compact/soc_occupation_compact.csv` | national median wage for the mapped SOC codes (report-only) |
| `data/sec/form-d/processed/sample/*.sample.json` | Form D funding cross-check (sample only; zero matches today) |
| `scripts/score/role-scorer.mjs` | the composite — run via CLI with `--out-dir` inside my namespace; never re-implemented |
| `scripts/sec/sec-all-quarters.py` → `normalize_company_name` | company-name normalization for every name join |
| `course/2026fa/submissions/Sreevarshann/notes/candidate-analysis.py` | the keyword and seniority rules this brief freezes |
| `scripts/conformance.mjs`, `scripts/pii-scan.mjs`, `scripts/doctor.mjs` | machine checks before every commit |
| `search/examples/meera-krishnan/profile.yml` (new, declared exception) | the fictional persona |

**Field formats confirmed:** `Approval_Rate` is a **0–100 percentage**, not a fraction — for all 114 matched rows it equals approvals ÷ (approvals + denials) × 100 exactly; across the 114: min 75.00, median 100.00, 80 at exactly 100. It is **reported, not scored**. Approval counts are stored as decimals (`"38.0"`). Funding dates are ISO `YYYY-MM-DD`.

**Proposed additions:**
- `[TODO: DEV]` **Prototype entry script** in `scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/`: filter, seniority split, read persona + posting-check file, pre-score evidence check, write `roles.json` for the scorer, call the scorer CLI, write the report and the blocked / network / verify-posting lists. Reason: no stored script does the filter → gate → score chain for this situation.
- `[TODO: DEV]` **Harness + fixtures** in the same folder: one fixture per predicted failure case below, plus a `BROKEN-*` mutant that sends an unchecked role to the scorer, to prove the harness catches it. Reason: CONTRIBUTING requires break attempts; the guards are the point of this work.
- `[TODO: DATA SOURCE]` **Posting-check file** (your-input): `company, role_type, url, date_checked, status (open | closed | not found)`. Planned: 4–5 real companies checked by hand, at least one closed or missing. Reason: the dataset has no posting URLs; liveness may only come from a human check.
- `[TODO: DATA SOURCE]` **Full Form D quarters** (gitignored, not in a fresh clone). Reason: the shipped samples match none of the 114 companies, so funding cannot be cross-checked.
- `[TODO: DEV]` + `[TODO: DEFINE]` **A funding vote for the scorer.** Reason: funding is one of the engine's five evidence components but has no term in the composite; the weight and the date-to-vote mapping need a human-defined value with reasoning. Not implemented here; funding is never folded into fit or sponsorship.

**Sponsorship mapping** — approval counts: record; cut-offs and the resulting p: your-input. In `roles.json`, `sponsorship.source` is `your-input`, and the approval count travels separately as `record` evidence in `roles.json` and in the report.

| Total Approvals | p | tier |
|---|---|---|
| ≥ 50 | 0.8 | `Proven` |
| 10–49 | 0.6 | `likely` |
| 2–9 | 0.4 | `possible` |

`Proven` provenance: tier string from Ch.11 and data/examples fixtures; code only defines soft tiers at role-scorer.mjs:48. Fewer than 2 approvals does not occur among the 114; if it did, the role is blocked, not given a tier.

**BLS (report-only, record; SOC mapping is model-judgment; zero effect on score):**

| Role | SOC (model-judgment) | O*NET rows | Annual median wage (2024 national) |
|---|---|---|---|
| Data Engineer | 15-1243 | Database Architects; Data Warehousing Specialists | 135,980 |
| ML Engineer | 15-2051 | Data Scientists; Business Intelligence Analysts; Clinical Data Managers | 112,590 |

O*NET rows under one BLS code share one wage (the wage is published at the BLS level). BLS has no Data Engineer or ML Engineer occupation.

## Gates

| # | Gate | Testable condition | Who clears / what they must see |
|---|---|---|---|
| G1 | Persona input | Persona parses; graduation, OPT start, window end are valid dates; window end > OPT start; fit present for both role types | Machine. Failure → halt with the field name. |
| G2 | Timeline gate | Window end not already past (else **halt**: "unemployment window ended YYYY-MM-DD; timeline cannot be evaluated"). Factor = 1.0 if run date + 60 days ≤ 2027-04-15, else 0.0 | Machine computes; report shows run date, lag (labelled assumption), window end, and the comparison. Closes for any run after 2027-02-14. |
| G3 | Seniority classification review | Every matched title listed with its class; counts 64 / 50 reproduce | **Human (named, dated).** Must see the full title-class table and the known edge case ("Associate Manager – Data Engineering" → senior). |
| G4 | Liveness human gate | A role reaches the scorer only if the posting-check file has a row for that company + role type with URL, a valid status, and date_checked ≤ run date **and** run date − date_checked ≤ 7 days (the 7-day limit is your-input). open → 1.0; closed / not found → 0.0. A check older than 7 days is stale → role goes back to the verify-posting list | **Human (named, dated).** Must see each URL, check date, age in days, and status they recorded. |
| G5 | Pre-score evidence completeness | Every role sent to the scorer has explicit sponsorship.p + tier, fit.p, liveness.factor, timeline.factor, each with a source label; anything missing → blocked list with reason, never sent | Machine. Halts the run if a role in `roles.json` lacks any of the four (guards the scorer's silent defaults). |
| G6 | Output adequacy | Report renders funnel, scored table, blocked list, network list, verify-posting list, cannot-verify list | **Human (named, dated)** reads the report against the live postings. |

## Predicted failure cases

| Case | How the prototype detects it | What it outputs instead of an invented value |
|---|---|---|
| Company not in the CSV (e.g. a posting check for a company outside the 114) | Normalized-name lookup (reused normalizer) finds no matched row | Blocked: "not in matched sponsorship set". No sponsorship p, no score. |
| OPT start or 90-day window already past | G1/G2 date comparison against run date | Halt with a clear error naming the date. No timeline factor. |
| Posting liveness unchecked | No posting-check row for company + role type | "Verify posting / network first" list. Never scored. |
| Stale posting check (older than 7 days at run time) | G4 age = run date − date_checked > 7 | Back to the verify-posting list with the check date and age shown. Never scored on the old status. |
| Blank `latest_funding_date` (1 of 114) | Empty-string check | Funding context shows `missing (blank in source)` — not 0, not "old". Score unaffected (funding is not scored). |
| Senior-only company | Seniority split | Network list with its matched senior titles. Never scored, even if a posting check exists for it. |
| Keyword matches an irrelevant title | Cannot be auto-detected | G3 title-class table makes every matched title visible; human flags false matches; flags recorded, keywords changed only by a logged revision. |
| Role with no fit value | Persona has no `fit_self_assessment` entry for the role type | Blocked: "fit missing — not defaulted". Never sent to the scorer. |
| Approval count < 2 or non-numeric | Numeric parse + cut-off check | Blocked: "sponsorship evidence below tier floor / unparseable". |
| Human-typed company name differs from the CSV | Normalizer finds no match | Blocked as "not in matched set" with both names shown, so the human can fix the check file. |

## Known scorer behaviors this prototype must guard against (scripts/score/role-scorer.mjs)

- **A missing vote scores like 0.** `push()` returns without adding the vote when `p` is not a number (lines 71–75; the check is line 73), and `voteSum` (line 80) is not reweighted — so a role with no sponsorship evidence gets the same composite as `p = 0`, with no "missing" flag. **Guard:** G5 blocks before scoring.
- **A missing gate defaults to open and is still labelled.** Liveness and timeline default to 1.0 (lines 83–84) and to source `record` / `your-input` (lines 86–87). An unchecked posting would look like "live, per record". **Guard:** G4 + G5; every role sent carries an explicit factor and label.
- **No funding term.** Weights are only `sponsorship`, `fit`, `role_quality` (lines 34–43); only those three are read (lines 76–78). **Guard:** funding is report-only and labelled so; a future vote is `[TODO: DEV]`.
- **`role_quality` weight is 0.0** (line 37, `[VERIFY]`). **Guard:** BLS wages are report-only; the brief never implies a wage affects a decision.
- **Source labels are not validated** — any string in `source` passes through (line 74). **Guard:** the prototype emits only `record` / `model-judgment` / `your-input` and the harness asserts it.
- **Profile parsing treats "authorized" as no-sponsorship-needed** (line 60). **Guard:** no `--profile` is passed; with no profile the scorer assumes sponsorship is needed (line 59), which is correct for this persona.
- **No exports; `main()` runs on load** (line 185). **Guard:** CLI only; results read from `role-scores.json`.
- **The report's skip rate counts overrides** (lines 145–146). **Guard:** no overrides are used in this run.

## Skip-rate prediction (pre-run calculation, not a scorer result)

If all 64 entry-eligible roles had a current open posting check, the scorer's own arithmetic (weights at lines 35–36, threshold 44, floor 45, soft tiers 48) would give:

| Tier | Data Engineer (fit 0.7) | ML Engineer (fit 0.5) |
|---|---|---|
| Proven, p 0.8 | 0.49 → Apply | 0.43 → Apply |
| likely, p 0.6 | 0.42 → Consider (soft tier) | 0.36 → Consider (soft tier) |
| possible, p 0.4 | 0.35 → Consider (soft tier) | 0.29 → Consider (band) |

≈ **22 Apply / 42 Consider / 0 Skip** — a 0% skip rate among open postings, below DOMAIN.md's "a healthy run skips at least half". **This is expected and will not be tuned away.** This recipe skips at the filter stage (30,369 → 64 is a 99.8% reduction before any score); moving cut-offs to hit a skip target would be rigging the score.

Within the actually scored set, the skip rate will equal the share of current postings recorded as closed or not found, because the liveness gate zeroes them. With 4–5 checks including at least one closed or missing, we expect ≥ 20% — a measure of the human checks, not of the scorer's judgment.

## What we predict the prototype will get wrong on the first pass

1. **Missed titles, including the student's own field.** "Data Analytics Engineer" does not match `data engineer` (a word sits between); "Analytics Engineer" and "Data Platform Engineer" are missed too.
2. **Name joins between the posting-check file and the CSV will fail** on suffixes and punctuation the normalizer does not strip, so real companies will show up as "not in matched set".
3. **Sponsorship strength is company-wide, not role-specific.** A company with 800 approvals mostly for other roles still gets `Proven` for Data Engineer.
4. **"Top" titles only.** Companies that sponsor Data Engineers but whose top-five list does not include it are invisible.
5. **Funding context is stale.** Only 5 of the 64 have a funding date in the last 24 months.
6. **The 7-day staleness rule will push hand checks back to the verify list** if the worked run happens more than a week after the checks.

## Declared exceptions

- **New persona** at `search/examples/meera-krishnan/profile.yml` — an exception to my own path rule, required by DATA_CONTRACT §Zero-Conditions for profile-shaped files and allowed by CI's scope check. Declared in the PR body. Only `profile.yml` is added; no repo tool requires `resume.example.json` or `gaps.md`, and `search/examples/README.md` is left untouched.

## Revisions

Everything above this heading is the original record as of the first commit of this file. Later changes are appended below — dated, with a reason — never edited in place.

- **R0 (recorded at drafting, 2026-10-02):** SOC mapping changed from 15-1252 (the candidate-C decision in `notes/candidate-analysis.md`) to 15-1243 for Data Engineer and 15-2051 for ML Engineer, reported separately. Still model-judgment, still zero effect on the score. The committed note is left unedited.
- **R1 (2026-10-02): normalizer source switched from `scripts/sec/sec-all-quarters.py` to `scripts/sec/entity-resolution.py`.** Reason: `sec-all-quarters.py` imports pandas at line 1, so importing it fails on a clean stdlib-only Python (`ModuleNotFoundError: No module named 'pandas'`, Python 3.13.9 venv); CI installs only pyyaml; this was masked locally because the default interpreter was Anaconda, which ships pandas. `entity-resolution.py` imports only the standard library, has a `__main__` guard, and uses an identical suffix list. Equivalence check: 0 disagreements across 30,569 names (30,369 from the 80 Days CSV + 200 from the SEC samples); the only difference is an empty name → `None` (sec-all-quarters) vs `''` (entity-resolution), both treated as blocked. Every mention of `sec-all-quarters.py` as the normalizer source above now means `entity-resolution.py`. `notes/candidate-analysis.py` received the same switch as a dated fix; its rerun on the clean interpreter reproduced the committed output with 0 differing lines.
- **R2 (2026-10-02): timeline gate finding and G1/fit clarification.**
  - **Timeline gate is effectively a halt for this persona — a prediction miss.** The prototype implements both the G2 factor rule and the failure-case rule "OPT start already past → halt". Together they make factor 0.0 unreachable for this persona with a 60-day lag: any run after 2027-01-15 halts, and any run on or before 2027-01-15 lands by 2027-03-16 (+60 days), inside the window ending 2027-04-15. Factor 0.0 is reachable only with a lag > 90 days (covered by tests). This contradicts the original G2 prediction that the gate "closes for any run after 2027-02-14"; that prediction is recorded as missed, not edited. Decision (your-input): keep the OPT-start halt.
  - `[TODO: DEV]` After OPT start, require unemployment days used with an as-of date and recompute the window instead of halting.
  - **G1 does not halt on missing fit.** A persona missing fit for a role type passes G1; the role-level block in the failure-case table ("fit missing — not defaulted") governs. Decision (your-input): keep per-role blocking.
- **R3 (2026-10-02): AI-sourced posting checks are scored but do not clear G4; ats:liveness used as a recorded cross-check.**
  - **Why:** no human posting checks were done for this run. All five posting checks in `inputs/posting-checks.csv` come from Claude (chat) web search results on 2026-10-02, some from aggregator sites, and none was opened and verified by a human.
  - **Change:** the posting-check file gains a required `checked_by` column, plus optional `what_was_seen`, `tool_result`, `tool_reason`, `tool_run_date`. A check whose `checked_by` says "not human-verified" is labelled **model-judgment** and does **not** clear G4. The role **is still scored**, so the run is not empty. Every such role carries `g4_human_cleared: false`, the plan is marked provisional, and the report's first section must state that the G4 human liveness gate was NOT cleared for these roles and every decision is provisional. A check by a human stays **your-input** and clears G4 as before. A blank `checked_by` is rejected. The scorer receives the liveness label as given (`model-judgment`), not `your-input`. This supersedes, for this run, the earlier statement that no company reaches the scorer without a human posting check.
  - **Cross-check:** `npm run ats:liveness` was run once per URL. The full output is in `runs/ats-liveness-2026-10-02.txt`. `tool_result` and `tool_reason` are labelled **record**, source "npm run ats:liveness, 2026-10-02". The `status` column (model-judgment) still sets the liveness factor; the tool result is reported alongside and changes nothing.
  - **Observed:** the tool contradicts both AI "open" statuses: AMGEN → expired (HTTP 404), TWILIO → expired (insufficient content). The other three are inconclusive (`uncertain`: two pages started a file download; one URL is a company homepage, not a posting).
  - **Added to Cannot-verify:** (1) ats:liveness has no "not found" result, so removed and closed postings both report `expired` and only the reason text separates them; (2) ats:liveness classifies "insufficient content" as `expired`, so a slow or bot-blocked page can be reported expired while the posting is live.
- **R4 (2026-10-02): the record outranks a model-judgment posting status on conflicts.**
  - **Rule:** if a posting check's status is model-judgment and the ats:liveness `tool_result` (record) contradicts it (status `open` + tool `expired`, or status `not found`/`closed` + tool `active`), the role is **not scored**. It goes to the verify-posting list with reason "conflict: model-judgment status vs ats:liveness record", showing both values with their labels.
  - A **your-input (human) status is never overridden** by `tool_result`. A disagreement is flagged in the report, but the human status governs, because ats:liveness has known false-expired cases (bot-blocked pages read as "insufficient content").
  - `tool_result` **"uncertain" never overrides anything**; it is shown as context only.
  - **Reason:** the first AI-sourced check (AMGEN) said open, and ats:liveness returned HTTP 404. Under R3 it would have scored Apply on a dead link.
  - **Test change:** two R3 tests used exactly this conflict (AI `open` + tool `expired`) to show the status driving the factor. They now use a non-conflicting tool result (`active` / `uncertain`); the conflict case is covered by new R4 tests.
