Interpreter: `<scratchpad>/cleanvenv/bin/python` (Python 3.13.9, isolated venv, no site packages). The committed run outputs were first produced with Anaconda's Python by mistake; a clean-interpreter rerun reproduced identical scorer outputs.

## 2026-10-02 — newgrad-de-ml-optwindow run 1 (sample mode, shipped data)

- **Recipe:** recipes/cases/2026fa/Sreevarshann-newgrad-de-ml-optwindow.md v0.1.0 (status DRAFT)
- **Inputs:** persona fixture `scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/fixtures/persona-meera-krishnan.json` (fictional); `course/2026fa/submissions/Sreevarshann/inputs/posting-checks.csv` (rows: 5; human: 0; AI: 5, "Claude (chat) web search, not human-verified"); `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv`; `data/bls/compact/soc_occupation_compact.csv`; Form D samples — SHA-256 of each in run-log.json
- **Command:** python3 scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/run.py (run date 2026-10-02; commit bf8b65d)
- **Outputs:** course/2026fa/submissions/Sreevarshann/runs/2026-10-02/{report.md, run-log.json, roles.json, role-scores.json, role-scores.md}; break attempts in course/2026fa/submissions/Sreevarshann/runs/break-attempts-2026-10-02.txt
- **Result:** 3 scoreable / 61 verify-posting / 53 network / 0 blocked / 0 rejected checks; scorer Apply 0 · Consider 0 · Skip 3 (all gated: liveness 0.0 from AI "not found"); AMGEN and TWILIO sent to verify-posting on R4 conflicts (AI "open" vs ats:liveness expired); G4 human liveness gate NOT cleared — run provisional; 57/57 offline tests pass
- **Gate decisions:** G3 (seniority review) and G6 (output adequacy) — not cleared; no named human has read and signed the report yet
- **Open issues:** no human posting checks; 5 open TODO items in the recipe (funding vote, after-OPT-start recompute, full Form D quarters, human posting checks, scorer exports); possible wrong company matches (HUMAN INC; PATHAI / PATHRAI) unverified
- **Update 2026-10-02:** break attempt d (missing input file raised a raw traceback) fixed in commit 2cb57e8; run.py now halts cleanly with a run log (exit 2); 58/58 offline tests pass.
