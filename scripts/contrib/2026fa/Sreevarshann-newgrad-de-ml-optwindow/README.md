---
owner: Sreevarshann
term: 2026fa
component: newgrad-de-ml-optwindow
status: DRAFT
promoted_to: null
---

# newgrad-de-ml-optwindow

## Executive summary

**What this is.** A small tool that sorts companies for a new-graduate F-1 student targeting Data Engineer and ML Engineer roles into four lists: roles the existing scorer may judge, roles that need a job posting checked first, senior-only companies to network with, and roles blocked for missing evidence. Every value says whether it came from a record, a model judgment, or the student's own input.

**Why read it.** The engine's scorer silently treats missing evidence as zero or as a pass. This tool stops that before scoring, and refuses to guess: missing data stays missing, and an unchecked or contradicted posting is never scored.

**What it does today.** One command runs the whole chain on the real repository data, calls the existing scorer through its command line, and writes a machine log and a plain-language report. The plan it follows is `course/2026fa/submissions/Sreevarshann/CHANGE-BRIEF.md` (with revisions R1–R5).

## Run it

From the repo root (Python 3, standard library only; Node for the scorer):

    python3 scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/run.py

A run refuses to overwrite an existing run folder for the same date (exit 3, "refusing to overwrite existing run outputs"). The committed run for 2026-10-02 is already in `course/2026fa/submissions/Sreevarshann/runs/2026-10-02/`, so to rerun or demo it without touching that folder, write to a temp folder instead:

    python3 scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/run.py --run-date 2026-10-02 --out-root /tmp/reallocation-demo

Options: `--run-date YYYY-MM-DD` (default today), `--persona`, `--checks`, `--out-root`, `--overwrite` (an existing run folder is never replaced without it).

Environment: the prototype and its tests need only the Python 3 standard library (no pandas, no PyYAML). The repo-wide `npm run verify` needs **PyYAML** (`pip install pyyaml`), because `scripts/manifest-check.mjs` parses `.ai/manifest.yaml` with it; CI installs it the same way. That requirement belongs to `npm run verify` only, not to this prototype.

## Inputs

| Input | Default path | Label |
|---|---|---|
| Company sponsorship data (7 non-personal columns read) | `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` | record |
| BLS wages (report-only) | `data/bls/compact/soc_occupation_compact.csv` | record (SOC mapping: model-judgment) |
| Form D samples (funding cross-check) | `data/sec/form-d/processed/sample/*.sample.json` | record |
| Persona (fictional) | `fixtures/persona-meera-krishnan.json` — the fields this tool needs from `search/examples/meera-krishnan/profile.yml` | your-input |
| Posting checks | `course/2026fa/submissions/Sreevarshann/inputs/posting-checks.csv` | your-input if a human checked; model-judgment if `checked_by` says "not human-verified"; `tool_result` is record |

## Outputs

Written to `course/2026fa/submissions/Sreevarshann/runs/<run-date>/`:

| File | For | What it holds |
|---|---|---|
| `report.md` | the person | headline warnings first, then funnel, scored table, verify-posting list (with conflict reasons), network list, blocked list, cannot-verify list, report-only context, next action per company |
| `run-log.json` | agents | inputs with SHA-256, commands, scorer stdout/exit code, counts, the full labelled plan |
| `roles.json` | the scorer | only roles that passed every gate |
| `role-scores.json`, `role-scores.md` | written by the existing scorer | only when at least one role is scoreable; otherwise the scorer is skipped with a plain message |

## Tests

Offline, no network; outputs of the run tests go to a temp folder:

    python3 -m unittest discover -s scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/tests -v

## Layout

| Path | What it is |
|---|---|
| `core.py` | filter, seniority split, sponsorship mapping, gates G1/G2/G4/G5, conflict and tie-break rules, scorer-record shaping |
| `run.py` | the end-to-end run and report writer |
| `fixtures/` | fictional companies, fictional posting checks (example.com), persona fields, and the `BROKEN-*` mutant used only by the tests |
| `tests/` | `test_core.py`, `test_run.py` |

## Limitations

- **Liveness is the binding constraint.** Only roles with a posting check reach the scorer. In the first run no posting was checked by a human, so every scored decision is provisional (G4 not cleared).
- **ats:liveness is a cross-check, not a verdict.** It has no "not found" result, and it reports "insufficient content" (e.g. bot-blocked pages) as expired.
- **Matching is by job-title keywords** in the sponsorship data's "top titles" field; titles like "Data Analytics Engineer" are missed, and sponsorship counts are company-wide, not role-specific.
- **Funding and wages do not affect the score.** The scorer has no funding term and its role-quality weight is 0; both are shown as context only.
- **The timeline gate is effectively a halt for this persona** with a 60-day lag (CHANGE-BRIEF R2): runs after OPT start halt rather than recompute the window.
- **Form D samples match none of the target companies**; full quarters are not in a fresh clone.
