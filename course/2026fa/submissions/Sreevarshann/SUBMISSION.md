# SUBMISSION — newgrad-de-ml-optwindow · 2026fa · Sreevarshann

## Executive summary

A recipe and working prototype that sorts H-1B-sponsoring companies into apply, verify-the-posting-first, network, and blocked lists for an F-1 new graduate targeting entry-level Data/ML Engineer roles; it runs end to end on the repository's shipped sample data, and its lifecycle stage is honestly held at DRAFT.

## Submission fields

- **Assignment:** The Reallocation Engine — Recipe Design Assignment
- **Student:** Sreevarshan Sathiyamurthy
- **GitHub handle:** Sreevarshann
- **Domain / situation:** fictional persona — F-1 MS new grad (OPT not started, 90-day window) targeting entry-level Data Engineer / ML Engineer roles at H-1B sponsors
- **Recipe path:** recipes/cases/2026fa/Sreevarshann-newgrad-de-ml-optwindow.md
- **Prototype command:**

      python3 scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/run.py

  Rerun / demo without touching the committed run folder:

      python3 scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/run.py --run-date 2026-10-02 --out-root /tmp/reallocation-demo

- **GitHub repository / branch / PR URL:** https://github.com/Sreevarshann/the-reallocation-engine / contrib/2026fa-Sreevarshann-newgrad-de-ml-optwindow / PR: https://github.com/nikbearbrown/the-reallocation-engine/pull/32
- **Submitted commit SHA:** e187b2ddd3350f11d06ba1f4622867ccdc09415d (content under review; the only later commit updates SUBMISSION.md itself)
- **Lifecycle stage claimed:** DRAFT (prototype runs end to end on shipped sample data; held at DRAFT per SNICKERDOODLE lines 58–59)
- **Summary of my changes:**
  - A plan of record (`CHANGE-BRIEF.md`, revisions R1–R5) and a recipe + card pair under `recipes/cases/2026fa/`, held at DRAFT with 5 typed TODO items.
  - A stdlib-only prototype (`scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/`: `core.py`, `run.py`) that gates every role before the existing scorer sees it, labels every value record / model-judgment / your-input, and calls the scorer only through its CLI.
  - 58 offline tests, a `BROKEN-*` mutant, six break attempts (all now failing cleanly), and a fresh-clone check; one real run on 2026-10-02 with a run log in `logs/runs/2026fa-Sreevarshann-1.md`.
  - A new fictional persona (`search/examples/meera-krishnan/profile.yml`, declared exception) and AI-sourced posting checks labelled model-judgment, cross-checked with `npm run ats:liveness`.
  - TEST-REPORT, WORKED-RUN (with attestation draft), DOMAIN-JUSTIFICATION, FRICTIONAL, and SOURCES documenting what was run, what broke, and what was AI vs. my decision.
- **Known limitations:**
  - No human posting checks: G4 (human liveness gate) was never cleared, so every decision in the run is provisional; the run produced 3 Skips and nothing to apply to.
  - The AI-sourced AMGEN posting reported as "open" returned HTTP 404 under `ats:liveness`; it was sent back to verify-posting rather than scored.
  - Sponsorship approvals are company-wide, not role-specific, and only "top" sponsored titles are visible (28,812 of 30,369 rows carry no title data).
  - Possible wrong company matches (model-judgment, unverified): HUMAN INC's 1,382 approvals, and PATHAI INC / PATHRAI INC appearing as one company entered twice.
  - The timeline gate is effectively a halt for this persona with a 60-day lag (R2): any run after OPT start halts instead of recomputing the window.
  - Zero Form D sample matches for the 114 target companies, and funding dates are mostly stale, so funding is report-only.
  - `ats:liveness` has no "not found" result and reads bot-blocked pages as expired, so it is a cross-check, not a verdict.
  - The keyword rule misses "Data Analytics Engineer" titles and finds zero "AI Engineer" records; the SOC mapping is model-judgment.
