# TEST-REPORT — newgrad-de-ml-optwindow · 2026fa · Sreevarshann

Interpreter for every Python command in this report: `<scratchpad>/cleanvenv/bin/python` — Python 3.13.9, an isolated virtual environment with no site packages (pandas is not importable). The full path is shortened because it contains the local username.

## Executive summary

**What this is.** The test record for a small tool that sorts companies for a new-graduate F-1 student targeting Data Engineer and ML Engineer roles, and refuses to let the engine's scorer treat missing evidence as zero or as a pass.

**Why read it.** It shows what was actually run, what passed, what broke, and what a person still has to judge — so the tool's results can be trusted only as far as the evidence goes.

**What it found.**
- All 57 offline tests pass, and the repository's own checks pass before and after this work with no new warnings.
- The full run on the shipped data completes: 3 roles reached the scorer and all 3 were skipped because their postings were reported gone; 61 roles need a posting checked first; 53 are networking targets.
- Six deliberate break attempts were made. Five failed cleanly. One — pointing the tool at a posting-check file that does not exist — crashed with a raw error instead of a clean message. It invented nothing, but it is a defect to fix.
- The first committed run accidentally used a different Python installation than intended; a rerun with the intended clean one produced identical scorer outputs.
- Three problems in the shared repository make parts of the course's automatic checks fail for everyone; none is caused by this work.

## Toolchain baseline (before vs after)

| Check | Before (start of session, `/tmp/doctor-before.txt`, `/tmp/verify-before.txt`) | After (run now) |
|---|---|---|
| `npm run doctor` | exit 0; environment ✓ runnable; ✓ no private/PII paths are tracked; 33 recipes | exit 0; **identical output** to before (`diff` after the npm header lines: no differences) |
| `npm run verify` — conformance | `conformance: 158 files (85 md · 36 py · 30 js · 4 sh · 3 json)` ✓ | `conformance: 167 files (88 md · 41 py · 30 js · 4 json · 4 sh)` ✓ — the 9 extra files are this contribution's |
| `npm run verify` — manifest check | ✓ passed (3 warnings: `archive/`, `private/`, `data/ats/`) | ✓ passed (same 3 warnings) |

Doctor, last 3 lines (for the PR template):

```
  environment: ✓ runnable
  recipes: 33/33 carry lifecycle frontmatter — all tracked
  next: continue
```

The doctor counts only top-level `recipes/`; the new case recipe under `recipes/cases/2026fa/` is not in its count.

## Unit tests

```
$PY -W error::ResourceWarning -m unittest discover -s scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/tests -b
Ran 57 tests in 8.521s

OK
```

## Full sample run (real output, run now)

Run into `/tmp` so the committed run folder is not overwritten; the scorer outputs are then compared byte for byte with the committed ones.

```
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

Exit 0. `roles.json`, `role-scores.json`, `role-scores.md`: **identical** to `course/2026fa/submissions/Sreevarshann/runs/2026-10-02/`.

## Failure cases → tests

Every failure case predicted in CHANGE-BRIEF, with the test that covers it (all in `scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/tests/`) and the break attempt that exercised it on the real CLI, if any.

| Failure case (CHANGE-BRIEF) | Expected output | Test(s) | Break attempt |
|---|---|---|---|
| Company not in the CSV | blocked: "not in matched sponsorship set" | `test_company_not_in_csv_is_blocked` | — |
| Human-typed name differs from the CSV | blocked, both names shown | `test_typo_name_blocked_with_both_names_shown`, `test_suffix_and_punctuation_variants_still_match` | — |
| OPT start or 90-day window already past | halt naming the date | `test_g2_halts_when_window_already_past`, `test_g2_halts_when_opt_start_already_past`, `test_g2_halt_stops_the_whole_plan`, `test_halt_writes_run_log_and_no_report` | **a** |
| Posting liveness unchecked | verify-posting list | `test_unchecked_role_goes_to_verify_posting` | — |
| Stale posting check (> 7 days) | verify-posting with date and age | `test_stale_check_goes_back_to_verify_posting`, `test_seven_days_is_current_eight_is_stale`, `test_future_dated_check_is_not_trusted` | — |
| Blank `latest_funding_date` | `missing (blank in source)`, never 0 | `test_blank_funding_date_stays_missing_not_zero` | — |
| Senior-only company | network list, never scored | `test_senior_only_company_is_network_never_scored` | — |
| Keyword matches an irrelevant title | visible in the title table for human review | `test_irrelevant_title_match_is_visible_for_human_review` | — |
| Role with no fit value | blocked: "fit missing — not defaulted" | `test_role_without_fit_is_blocked_not_defaulted`, `test_out_of_range_fit_is_treated_as_missing` | — |
| Approval count < 2 or non-numeric | blocked with reason | `test_below_floor_and_unparseable_approvals_blocked`, `test_cutoff_boundaries` | — |
| Malformed posting-check row | row rejected with reason, never repaired | `test_malformed_check_rejected_and_role_stays_unchecked`, `test_blank_checked_by_is_rejected`, `test_tool_result_without_run_date_is_rejected` | **b** |
| Unknown posting-check column | halt naming the column | `test_unknown_column_halts` | **c** |
| AI check is not a human check (R3) | scored, G4 not cleared, run provisional | `test_ai_check_is_scored_but_g4_not_cleared_and_run_is_provisional`, `test_human_check_clears_g4`, `test_submission_input_file_loads_as_model_judgment` | — |
| Record contradicts an AI status (R4) | verify-posting with both values | `test_model_judgment_open_vs_record_expired_goes_to_verify_posting`, `test_model_judgment_not_found_vs_record_active_goes_to_verify_posting`, `test_human_open_vs_record_expired_human_governs_and_is_flagged`, `test_uncertain_never_overrides` | — |
| Same-date tie between checks (R5) | human check wins | `test_same_date_human_check_beats_ai_check_in_either_order`, `test_newer_ai_check_still_beats_older_human_check` | — |
| Incomplete role reaches the scorer (G5) | blocked or halt | `test_each_missing_input_is_caught`, `test_assert_scoreable_halts_on_incomplete_role`, `test_suite_catches_broken_mutant` | **f** |
| Zero scoreable roles | scorer skipped with a plain message | `test_zero_scoreable_skips_scorer_with_plain_message` | — |
| Rerun into an existing run folder | refused | `test_refuses_to_overwrite_existing_run` | **e** |

## Break attempts (real CLI runs)

Full commands and real output: `course/2026fa/submissions/Sreevarshann/runs/break-attempts-2026-10-02.txt`. Broken inputs lived in `/tmp/break-2026-10-02/`.

| id | Attempt | Exit | Outcome | Failed cleanly, no invented value? |
|---|---|---|---|---|
| a | persona whose 90-day window ended 2026-08-30 | 2 | HALT at G2; only `run-log.json` (status `halted`) | yes |
| b | posting check with `date_checked` 2026-13-45 | 0 | AMGEN row rejected; AMGEN → verify-posting "unchecked"; rest of run proceeds | yes — rejected, not repaired |
| c | posting-check file with an unknown column | 2 | HALT naming `vibe`; only `run-log.json` | yes |
| d | posting-check file path does not exist | 1 | unhandled `FileNotFoundError` traceback; no outputs at all | **no invented value, but not clean** |
| e | rerun into the existing `runs/2026-10-02` | 3 | "refusing to overwrite existing run outputs …"; committed folder untouched | yes |
| f | `BROKEN-g5-ignores-liveness` mutant test | 0 | test passes: the real G5 halts the unchecked role, the mutant lets it through | yes |

**Defect from attempt d (open):** `run.py` computes each input's SHA-256 before its `GateHalt` handling, so a missing input file raises a raw traceback instead of a clean "input not found" halt with a run log. No value is invented and no file is written, but the failure is not clean. Not fixed in this step.

## Diff scope: `git diff --stat main...HEAD`

23 files changed, 11,271 insertions, 0 deletions. Every path is in a namespaced location or the declared persona exception:

| Location | Files |
|---|---|
| `course/2026fa/submissions/Sreevarshann/` | 11 |
| `scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/` | 9 |
| `recipes/cases/2026fa/` | 2 |
| `search/examples/meera-krishnan/profile.yml` | 1 — **declared exception** (DATA_CONTRACT requires new fictional personas there) |

No protected path is touched (`logs/RUN_LOG.md`, `package.json`, `package-lock.json`, `CLAUDE.md`, `AGENTS.md`, `SNICKERDOODLE.md`, `DOMAIN.md`, `DATA_CONTRACT.md`, `.github/`). The largest file is the run's `run-log.json` (8,175 lines, ~311 KB), which holds the full labelled plan. This commit adds the break-attempt file, this report, WORKED-RUN, the justification outline, and `logs/runs/2026fa-Sreevarshann-1.md` (an allowed path).

## Interpreter correction

The committed run in `course/2026fa/submissions/Sreevarshann/runs/2026-10-02/` (commit `bc723e6`) was meant to use the clean interpreter. A symlink added inside the clean environment created a loop, and the shell fell through to the Anaconda `python3`, which does have pandas. The prototype imports only the standard library, so this did not change its behaviour, but the statement "ran with the clean interpreter" was wrong. The loop was fixed, and a rerun with the clean interpreter produced byte-identical `roles.json`, `role-scores.json`, and `role-scores.md`; `report.md` and `run-log.json` differ only in the command line and output paths, which record the temp folder. The 57-test run happened before the symlink change and was unaffected.

## What each gate requires a human to judge

| Gate | Machine checks | A human must judge |
|---|---|---|
| G1 persona input | dates parse, window after OPT start, integers valid | that the persona's dates and the 60-day hiring lag are realistic for the situation being modelled |
| G2 timeline | the arithmetic and the halt | whether halting after OPT start is acceptable (R2), and the lag assumption itself |
| G3 seniority review | the rule reproduces 114 / 64 / 50 | each title's senior/non-senior class — e.g. "Associate Manager – Data Engineering", "Data Engineer III" — by reading the title lists in `report.md` |
| G4 liveness | check exists, ≤ 7 days old, human vs AI, tool conflicts | the posting itself: open it, record URL, date, status. Not done in run 1 |
| G5 evidence completeness | every scorer input present and labelled | nothing — fully mechanical |
| G6 output adequacy | report sections and order | whether the report is right about the real companies, read against the live postings |

## Known repo-wide CI issues (not caused by this work)

1. **The `harness-regression` CI job fails for every PR.** It calls six harness scripts; four do not exist: `scripts/test/gate-behavior-harness.mjs`, `scripts/test/fuzz-invariants.mjs`, `scripts/gates/gate-behavior-harness.mjs`, `scripts/score/scorer-harness.mjs`.
2. **The working-tree PII scan fails on `main`.** `node scripts/pii-scan.mjs` flags an npm package author's email address in the tracked `package-lock.json`. The branch-history scan (`--diff main`) is clean for this contribution.
3. **`scripts/score/role-scorer.mjs` has no exports** and runs `main()` on load (line 185), so the import route CONTRIBUTING.md documents (`CONFIG`, `SRC`, `applyProfile`, `scoreRole`) cannot work; this contribution uses the CLI.
