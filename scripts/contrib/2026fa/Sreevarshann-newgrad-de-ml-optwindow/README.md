---
owner: Sreevarshann
term: 2026fa
component: newgrad-de-ml-optwindow
status: DRAFT
promoted_to: null
---

# newgrad-de-ml-optwindow — prototype core

## Executive summary

**What this is.** The working core of a small tool that sorts companies for a new-graduate F-1 student targeting Data Engineer and ML Engineer roles into four lists: ready to score, blocked (with the reason), networking targets, and "check the posting first".

**Why read it.** It exists to stop the engine's scorer from treating missing evidence as zero or as a pass. Every value it emits says whether it came from a record, a model judgment, or the student's own input.

**What it does today.** The filters and gates are built and covered by offline tests. It does not yet call the scorer or produce a report; that is the next step. The plan it follows is `course/2026fa/submissions/Sreevarshann/CHANGE-BRIEF.md`.

## Run the tests

Python 3 standard library only, no network:

    python3 -m unittest discover -s scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/tests -v

## Layout

| Path | What it is |
|---|---|
| `core.py` | filter, seniority split, sponsorship mapping, gates G1/G2/G4/G5, scorer-record shaping |
| `fixtures/companies-slice.csv` | fictional companies, non-personal columns only |
| `fixtures/posting-checks.csv` | fictional posting checks, example.com URLs |
| `fixtures/persona-meera-krishnan.json` | the fields this tool needs from the fictional persona |
| `fixtures/BROKEN-g5-ignores-liveness.py` | mutant used only to prove the tests catch a broken G5 |
| `tests/test_core.py` | unittest suite |
