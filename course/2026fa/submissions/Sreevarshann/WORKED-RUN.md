# WORKED RUN — newgrad-de-ml-optwindow · 2026-10-02 · 2026fa · Sreevarshann

Interpreter for every Python command below: `<scratchpad>/cleanvenv/bin/python` (`$PY`) — Python 3.13.9, an isolated virtual environment with no site packages (pandas is not importable). The full path is shortened because it contains the local username.

## Executive summary

**What this is.** A step-by-step record of one complete run of a tool that helps a new-graduate F-1 student (fictional persona) decide where to spend scarce application hours on Data Engineer and ML Engineer roles.

**Why read it.** Every number below can be traced to a file line or a command you can rerun, and every value says whether it is a record, a model judgment, or the student's own input — so you can check the tool's conclusions instead of trusting them.

**What it found.**
- Of 64 entry-level candidate companies, 5 had a posting check — all from an AI web search, none from a human.
- Two AI checks said "open" but the liveness tool contradicted them (Amgen's link returned "page not found"; Twilio's page read as empty), so both were sent back to "check the posting first" rather than scored.
- The other three were reported "not found", so the scorer skipped all three. Nothing reached "apply".
- Because no human checked a posting, every decision here is provisional.

## Inputs

| Input | Path | Label |
|---|---|---|
| Persona (fictional) | `search/examples/meera-krishnan/profile.yml`; fields used: `scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/fixtures/persona-meera-krishnan.json` | your-input |
| Posting checks | `course/2026fa/submissions/Sreevarshann/inputs/posting-checks.csv` — 5 rows, every `checked_by` = "Claude (chat) web search, not human-verified" | model-judgment (status), record (`tool_result`) |
| Company sponsorship data | `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` (7 non-personal columns read) | record |
| BLS wages (report-only) | `data/bls/compact/soc_occupation_compact.csv` | record (SOC mapping: model-judgment) |
| Form D samples (cross-check) | `data/sec/form-d/processed/sample/*.sample.json` (4 files) | record |

Persona values (your-input): OPT start 2027-01-15; 90-day window ends 2027-04-15; 0 unemployment days used; hiring lag 60 days (**assumption**); fit Data Engineer 0.7, ML Engineer 0.5.

Posting checks (all dated 2026-10-02, all "Claude (chat) web search, not human-verified"):

| Company | Role | status (model-judgment) | tool_result (record) |
|---|---|---|---|
| AMGEN INC | data_engineer | open | expired — HTTP 404 |
| HUMAN INC | data_engineer | not found | uncertain — navigation error: page.goto: Download is starting |
| TWILIO INC | ml_engineer | open | expired — insufficient content — likely nav/footer only |
| OVERJET INC | ml_engineer | not found | uncertain — navigation error: page.goto: Download is starting |
| FEMTOSENSE INC | ml_engineer | not found | uncertain — content present but no visible apply control found |

## Commands and real output

### 1. Liveness cross-check (`npm run ats:liveness`, one call per URL)

Run earlier the same day (21:17 local, 2026-10-03T01:17Z) and saved verbatim to `course/2026fa/submissions/Sreevarshann/runs/ats-liveness-2026-10-02.txt`; not re-run for this document, because the posting-check file's `tool_result` columns were filled from exactly this output.

```text
# npm run ats:liveness — one invocation per URL — run 2026-10-03T01:17:56Z (UTC)
# Playwright 1.62.1 · Chrome Headless Shell 151.0.7922.34

$ npm run ats:liveness -- https://careers.amgen.com/en/job/tampa/data-engineer/87/90666283952

> the-reallocation-engine@1.0.0 ats:liveness
> node scripts/ats/check-liveness.mjs https://careers.amgen.com/en/job/tampa/data-engineer/87/90666283952

Checking 1 URL(s)...

❌ expired    https://careers.amgen.com/en/job/tampa/data-engineer/87/90666283952
           HTTP 404

Results: 0 active  1 expired  0 uncertain
[exit 1]

$ npm run ats:liveness -- https://jobs.vertexventures.com/companies/human/jobs/63629925-senior-data-engineer

> the-reallocation-engine@1.0.0 ats:liveness
> node scripts/ats/check-liveness.mjs https://jobs.vertexventures.com/companies/human/jobs/63629925-senior-data-engineer

Checking 1 URL(s)...

⚠️ uncertain  https://jobs.vertexventures.com/companies/human/jobs/63629925-senior-data-engineer
           navigation error: page.goto: Download is starting

Results: 0 active  0 expired  1 uncertain
[exit 1]

$ npm run ats:liveness -- https://weworkremotely.com/remote-jobs/twilio-machine-learning-engineer

> the-reallocation-engine@1.0.0 ats:liveness
> node scripts/ats/check-liveness.mjs https://weworkremotely.com/remote-jobs/twilio-machine-learning-engineer

Checking 1 URL(s)...

❌ expired    https://weworkremotely.com/remote-jobs/twilio-machine-learning-engineer
           insufficient content — likely nav/footer only

Results: 0 active  1 expired  0 uncertain
[exit 1]

$ npm run ats:liveness -- https://jobs.generalcatalyst.com/companies/overjet/jobs/40776919-senior-machine-learning-engineer

> the-reallocation-engine@1.0.0 ats:liveness
> node scripts/ats/check-liveness.mjs https://jobs.generalcatalyst.com/companies/overjet/jobs/40776919-senior-machine-learning-engineer

Checking 1 URL(s)...

⚠️ uncertain  https://jobs.generalcatalyst.com/companies/overjet/jobs/40776919-senior-machine-learning-engineer
           navigation error: page.goto: Download is starting

Results: 0 active  0 expired  1 uncertain
[exit 1]

$ npm run ats:liveness -- https://www.femtosense.ai

> the-reallocation-engine@1.0.0 ats:liveness
> node scripts/ats/check-liveness.mjs https://www.femtosense.ai

Checking 1 URL(s)...

⚠️ uncertain  https://www.femtosense.ai
           content present but no visible apply control found

Results: 0 active  0 expired  1 uncertain
[exit 1]
```

### 2. Offline tests (run now)

```text
$PY -W error::ResourceWarning -m unittest discover -s scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/tests -b
Ran 57 tests in 8.521s

OK
```

### 3. End-to-end run (run now, into /tmp so the committed folder is untouched)

```text
$PY scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/run.py --run-date 2026-10-02 --out-root /tmp/worked-2026-10-02/out
plan: {'scoreable': 3, 'blocked': 0, 'network': 53, 'verify_posting': 61, 'rejected_checks': 0, 'cannot_verify': 66}  provisional=True
roles.json: 3 role(s) -> /tmp/worked-2026-10-02/out/2026-10-02/roles.json
scorer: $ npm run score -- /tmp/worked-2026-10-02/out/2026-10-02/roles.json --out-dir /tmp/worked-2026-10-02/out/2026-10-02

> the-reallocation-engine@1.0.0 score
> node scripts/score/role-scorer.mjs /tmp/worked-2026-10-02/out/2026-10-02/roles.json --out-dir /tmp/worked-2026-10-02/out/2026-10-02

✓ scored 3 roles → Apply 0 · Consider 0 · Skip 3 (skip 100%)
  ../../../../../tmp/worked-2026-10-02/out/2026-10-02/role-scores.json  +  ../../../../../tmp/worked-2026-10-02/out/2026-10-02/role-scores.md
report: /tmp/worked-2026-10-02/out/2026-10-02/report.md
run-log: /tmp/worked-2026-10-02/out/2026-10-02/run-log.json
```

Exit 0. `roles.json`, `role-scores.json`, and `role-scores.md` are byte-identical to the committed `course/2026fa/submissions/Sreevarshann/runs/2026-10-02/`. The committed folder's own report and run log are the files of record.

## Verified vs inferred, line by line

Source abbreviations: **CSV** = `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv`; **CHK** = `course/2026fa/submissions/Sreevarshann/inputs/posting-checks.csv`; **PER** = `scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/fixtures/persona-meera-krishnan.json`; **LIV** = `npm run ats:liveness, 2026-10-02`; **SC** = scorer output `role-scores.json`. "Verified" means the value matches its source file or command; "inferred" means it is a judgment or an assumption, not a fact checked against the world.

### Scored roles

| Field | HUMAN INC · data_engineer | OVERJET INC · ml_engineer | FEMTOSENSE INC · ml_engineer | Label | Verified / inferred |
|---|---|---|---|---|---|
| Company + source line | CSV#L12630 | CSV#L19395 | CSV#L9574 | record | verified (line exists, name matches) |
| Matched title(s) | Data Engineer 2 | Machine Learning Engineer II | Deep Learning Engineer | record | verified |
| Seniority class | non-senior | non-senior | non-senior | your-input (rule) | rule applied mechanically; class itself is a judgment |
| Total Approvals | 1382 | 48 | 6 | record | verified against CSV — **but see Verification: HUMAN INC may be a wrong company match** |
| Tier / p | Proven / 0.8 | likely / 0.6 | possible / 0.4 | your-input (cut-offs) | inferred |
| Fit p | 0.7 | 0.5 | 0.5 | your-input (PER) | inferred (self-assessment) |
| Posting status | not found | not found | not found | model-judgment (CHK#L3 / L5 / L6) | **inferred — no human checked** |
| Liveness factor | 0.0 | 0.0 | 0.0 | model-judgment | inferred (from the status above) |
| G4 human-cleared | no | no | no | — | verified (checked_by says "not human-verified") |
| ats:liveness result | uncertain — Download is starting | uncertain — Download is starting | uncertain — no visible apply control (company homepage, not a posting) | record (LIV) | verified as tool output; tells nothing either way |
| Timeline factor | 1.0 | 1.0 | 1.0 | your-input (PER dates + 60-day lag assumption) | arithmetic verified: 2026-10-02 + 60 days = 2026-12-01 ≤ 2027-04-15; lag is an assumption |
| Scorer arithmetic | (0.8·0.35 + 0.7·0.3) × 0 × 1 = 0.000 | (0.6·0.35 + 0.5·0.3) × 0 × 1 = 0.000 | (0.4·0.35 + 0.5·0.3) × 0 × 1 = 0.000 | derived (SC) | verified: scorer output |
| Recommendation | Skip — gated: liveness ≈ 0.000 | Skip — gated: liveness ≈ 0.000 | Skip — gated: liveness ≈ 0.000 | derived (SC) | verified as scorer output; **provisional** because the liveness input is model-judgment |
| Latest funding date / stage | 2018-09-13 / Series B | 2024-02-16 / Series C | 2024-11-26 / Seed | record (report-only) | verified against CSV; not scored |
| Approval rate % | 99.14 | 96.0 | 75.0 | record (report-only, 0–100 %) | verified; not scored |

### Verify-posting roles with a conflict (not scored)

| Field | AMGEN INC · data_engineer | TWILIO INC · ml_engineer | Label | Verified / inferred |
|---|---|---|---|---|
| Company + source line | CSV#L1567 | CSV#L27766 | record | verified |
| Matched title | Data Engineer 20516.3745 | Machine Learning Engineer (L2) | record | verified |
| Total Approvals | 1882 | 802 | record | verified against CSV |
| Tier / p | Proven / 0.8 | Proven / 0.8 | your-input (cut-offs) | inferred |
| Fit p | 0.7 | 0.5 | your-input (PER) | inferred |
| Posting status | open | open | model-judgment (CHK#L2 / L4) | inferred — no human checked |
| ats:liveness result | expired — HTTP 404 | expired — insufficient content | record (LIV) | verified as tool output |
| Placement | verify-posting: "conflict: model-judgment status vs ats:liveness record" | same | — | rule R4 applied |
| Latest funding date / stage | missing (blank in source) / missing (blank in source) | 2021-07-14 / Series D+ | record (report-only) | verified; Amgen's blank stays blank, never 0 |

## Verification

The exact source lines from the sponsorship CSV, showing only company name, approvals, and sponsored titles (no personal columns). Rerun with `sed -n '12630p;1567p'` on the CSV if you want to see them yourself, or open it in a spreadsheet at those rows.

**HUMAN INC — `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` line 12630**
- company_name: `HUMAN INC`
- Total Approvals: `1382.0`
- top_job_titles_sponsored: `['Senior Emerging Technology Engineer', 'Process Improvement Lead', 'Senior Software Engineer', 'Senior Full Stack Engineer', 'Software Engineer 2', 'Lead Technology Leadership Professional', 'Senior Application Architect', 'Senior Software Engineer', 'Senior Full Stack Engineer', 'Senior Cloud Services Engineer', 'Data Engineer 2', 'Lead Application Architect', 'Senior Software Engineer']`
- Note (model-judgment, unverified): the title mix reads like a large enterprise IT organisation, which does not fit a bot-fraud security firm of HUMAN's profile; this record may belong to a different employer.

My check:

**AMGEN INC — `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` line 1567**
- company_name: `AMGEN INC`
- Total Approvals: `1882.0`
- top_job_titles_sponsored: `['Data Engineer 20516.3745', 'Strategy Sr. Manager 20516.2439', 'Commercial Leadership Program 20516.4093', 'Principal IS Architect 20516.1936.14 ', 'Sr. Associate IS Engineer 20516.3864.5']`
- `latest_funding_date` and `latest_funding_stage` are blank on this line; the report shows them as missing.

My check:

## Reflection

<!-- Sreevarshann: write your reflection here. -->

## Attestation

> Drafted by Claude Code from the real runs listed here. It becomes Sreevarshann's attestation only after Sreevarshann reviews and confirms it. It does not promote the recipe: the recipe stays at DRAFT and its `attestation` field stays `null`.

- Recipe: newgrad-de-ml-optwindow v0.1.0
- By: Sreevarshann · 2026-10-02

### Tested
| Ran | Saw | Expected |
|---|---|---|
| `$PY -W error::ResourceWarning -m unittest discover -s scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/tests -b` | `Ran 57 tests … OK` | all tests pass, no resource warnings |
| `$PY scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/run.py --run-date 2026-10-02 --out-root /tmp/worked-2026-10-02/out` | exit 0; plan 3 scoreable / 61 verify / 53 network / 0 blocked; scorer Skip 3; `provisional=True` | a full run with every role on one list and the G4 warning first |
| byte compare of the clean rerun vs the committed run folder | `roles.json`, `role-scores.json`, `role-scores.md` identical | identical scorer inputs/outputs |
| `npm run ats:liveness -- <url>` on the 5 posting URLs | 2 expired (HTTP 404; insufficient content), 3 uncertain | a recorded result per URL |
| **Break a:** persona whose window ended 2026-08-30 | exit 2; `HALT: G2 timeline: unemployment window ended 2026-08-30 …`; only run-log.json | halt, no invented timeline |
| **Break b:** posting check dated 2026-13-45 | exit 0; row rejected "date_checked not an ISO date"; AMGEN → verify-posting "unchecked" | row rejected, not repaired |
| **Break c:** unknown column `vibe` | exit 2; HALT naming the column | halt |
| **Break d:** posting-check path does not exist | exit 1; raw `FileNotFoundError` traceback; no outputs | **clean halt with a run log — not met** |
| **Break e:** rerun into existing `runs/2026-10-02` | exit 3; "refusing to overwrite existing run outputs …"; no tracked changes | refusal |
| **Break f:** `-k suite_catches_broken_mutant` | `Ran 1 test … OK` — real G5 halts the unchecked role, the mutant does not | suite catches the mutant |
| `npm run doctor`, `npm run verify` (after) | both exit 0; doctor identical to before; conformance 167 files ✓; manifest ✓ (3 pre-existing warnings) | no regression |

### Did not test
- No human posting check: every posting status in this run is an AI web-search result (model-judgment).
- No run after OPT start (2027-01-15); the timeline factor 0.0 branch is reachable only with a lag over 90 days (unit-tested, not run on real data).
- No full Form D quarters; only the shipped samples (zero matches).
- `ats:liveness` on only 5 URLs, once, from one machine; no repeat to see whether results are stable.
- No check that HUMAN INC's or the PATHAI / PATHRAI records belong to the companies they are named for.
- No live run with a human clearing every gate; no RUNNABLE-LIVE run.
- No test of the report's adequacy against the real postings (G6) — needs a human.
- No run with a different persona or a different hiring-lag assumption.

### Broke during testing, fixed
- **Normalizer import needed pandas** — `scripts/sec/sec-all-quarters.py` imports pandas at line 1; switched to the stdlib-only `scripts/sec/entity-resolution.py` (CHANGE-BRIEF R1, commit `14411d3`); outputs verified identical across 30,569 names.
- **Unclosed-file warnings** in the Form D cross-check — fixed with a context manager before commit `2079aa6`.
- **Scorer record mislabelled liveness** as `your-input` regardless of who checked — now passes the real label (commit `c1771bb`).
- **Test-data column swap** — two R3 test rows had `checked_by` and `what_was_seen` in the wrong order, so an AI check read as human; test data fixed (commit `c1771bb`), no code changed to pass.
- **An AI "open" status would have scored Apply on a dead link** (AMGEN, HTTP 404) — rule added: a contradicting record outranks a model-judgment status (CHANGE-BRIEF R4, commit `0c6c941`); two R3 tests that relied on the old behaviour were updated.
- **Same-date tie took the first row in file order**, letting an AI check beat a human one — tie-break added (CHANGE-BRIEF R5, commit `4b08d46`).
- **Timeline gate effectively a halt for this persona** — found, recorded as a prediction miss, kept by decision (CHANGE-BRIEF R2, commit `01cde15`); recompute proposed.
- **Interpreter symlink loop** — the committed run fell through to Anaconda's Python; link restored, clean rerun reproduced identical scorer outputs.
- **Commit author email** was a machine `.local` address — re-authored to the GitHub noreply address before any push.
- **PII-scan finding introduced in FRICTIONAL.md** (a quoted npm author email) — amended before any push; branch-history scan clean.

### Broke during testing, not yet fixed
- **Break d** — a missing input file raises a raw traceback instead of a clean halt with a run log.
