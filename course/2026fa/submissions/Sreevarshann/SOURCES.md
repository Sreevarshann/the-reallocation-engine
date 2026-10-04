# SOURCES — newgrad-de-ml-optwindow · 2026fa · Sreevarshann

## Executive summary

**What this is.** The list of everything this contribution relied on: the repository and its rules, the data files, the existing code it reused, the one essay behind its time-allocation framing, and the tools used to build it.

**Why read it.** So a reviewer can trace any claim back to its source and see plainly which parts were done by AI tools and which were the student's own decisions.

**What it records.** All data came from files already in the repository; no outside dataset was added. The existing scorer and helper scripts were reused, never rewritten. Most of the code and writing was produced with AI assistance; the student made the scoping choices, kept personal details out of the repository, and rejected the over-claims.

## Repository and governing docs

- Repository: `nikbearbrown/the-reallocation-engine` (worked on in the fork `Sreevarshann/the-reallocation-engine`, branch `contrib/2026fa-Sreevarshann-newgrad-de-ml-optwindow`).
- `SNICKERDOODLE.md` — constitution: principles, verification stack, recipe lifecycle (lines 48–83 used to set the recipe's status).
- `DOMAIN.md` — domain map, runnable commands, known gaps.
- `CONTRIBUTING.md` — contribution paths, branch rule, run-log location, engine API.
- `DATA_CONTRACT.md` — data layers and §Zero-Conditions (fictional personas only).
- `AGENTS.md`, `CLAUDE.md` — generated agent instructions.
- `recipes/_shared.md` — shared recipe contract and run-log template.
- `recipes/scan.md`, `recipes/local-wage-adjustment.md`, `recipes/local-wage-adjustment.card.md` — style models for the recipe and card.

## Data used (exact paths)

- `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` — 7 non-personal columns read: `company_name`, `top_job_titles_sponsored`, `Total Approvals`, `Total Denials`, `Approval_Rate`, `latest_funding_date`, `latest_funding_stage`.
- `data/bls/compact/soc_occupation_compact.csv` — national median wages for SOC 15-1243 and 15-2051 (report-only).
- `data/sec/form-d/processed/sample/companies-sec-2025q2-d.sample.json`
- `data/sec/form-d/processed/sample/companies-sec-2025q3-d.sample.json`
- `data/sec/form-d/processed/sample/companies-sec-2025q4-d.sample.json`
- `data/sec/form-d/processed/sample/companies-sec-2026q1-d.sample.json`

## Repo code reused

- `scripts/score/role-scorer.mjs` — the composite scorer, called through its CLI (`npm run score -- <roles.json> --out-dir <dir>`); never imported or re-implemented.
- `scripts/sec/entity-resolution.py` — `normalize_company_name` for every company-name join.
- `scripts/ats/check-liveness.mjs` — `npm run ats:liveness`, the posting liveness cross-check.
- `scripts/conformance.mjs`, `scripts/pii-scan.mjs`, `scripts/doctor.mjs` — machine checks before every commit.

## Essay

- Nik Bear Brown, "The 3-3-2 Split" — the source of the 3-3-2 day (2 hours applying, 3 networking, 3 portfolio) used for next actions. No figures from it are cited as records. In-repo text of the 3-3-2 day: `book/chapters/02-the-reallocation-principle.md`, line 39.

## Tools

- Claude Code (Opus 5.5) in the Claude desktop app — repository work, code, tests, runs, drafts.
- Claude (chat) on claude.ai — planning, prompts, recommendations, web search for posting URLs, drafts of reflective writing.
- Playwright Chromium (Chrome Headless Shell 151.0.7922.34, Playwright 1.62.1) — used by `npm run ats:liveness`; installed outside the repository.

## AI contribution vs. my decisions

**What Claude (chat) did:** planned the step order and wrote the prompts I pasted into Claude Code; recommended candidate C, the seniority split, and treating III/IV/Founding as senior; recommended all six CHANGE-BRIEF decisions (sponsorship tiers, fit values, funding report-only, liveness handling, timeline dates, BLS report-only), which I adopted; found candidate posting URLs and statuses by web search — one of them (AMGEN) was a dead link it reported as open; advised holding the recipe at DRAFT; drafted FRICTIONAL entries 1–8, the Reflection, and the domain justification, which I reviewed.

**What Claude Code did:** read the repo and ran all baseline commands; computed every count; wrote all prototype code, tests, fixtures, the mutant, run.py, the recipe and card drafts, TEST-REPORT, WORKED-RUN, and the run log; caught my machine's local hostname email in commit metadata, the pandas dependency hidden by Anaconda, the persona being linkable to the author, the Approval_Rate format, the 0% skip-rate consequence, the timeline-gate contradiction, the tie-break bug, and an email it had itself put into TEST-REPORT; admitted and corrected its own interpreter mistake.

**What I decided, checked, or changed:** described the situation type the persona models (no personal details in the repo); chose candidate C and approved the slug; chose option (a) for the persona location and changed the persona's program and university so it isn't linkable to me; chose option A (stdlib normalizer) with a dated fix rather than a note; chose not to tune cut-offs to hit a skip-rate target; chose to commit AI-sourced posting checks labeled model-judgment instead of doing human checks, and accepted that G4 was never cleared; approved R4 and R5; refused the RUNNABLE-SAMPLE claim and held the recipe at DRAFT; ran the CSV check for AMGEN and HUMAN INC in my own terminal. Most technical recommendations came from the AI and were accepted by me; what I rejected were over-claims (RUNNABLE-SAMPLE, unverified human checks).
