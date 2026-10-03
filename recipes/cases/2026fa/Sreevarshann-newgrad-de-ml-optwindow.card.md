# newgrad-de-ml-optwindow — human card

## Executive summary

**What this is.** The one-page guide for the person who has to decide whether to trust this tool's lists. **Why read it.** It says, in plain terms, what the tool can and cannot know before you spend an application hour on its advice. **What it found in run 1.** Of 64 entry-level candidate companies, 3 reached the scorer and all were skipped because their postings were reported gone; 61 need a posting checked first; 53 senior-only roles are networking targets. No posting was checked by a human, so nothing is final.

**Lifecycle status:** DRAFT (held). The tool runs end to end on shipped sample data (commit bc723e6, run 2026-10-02), but the recipe stays at DRAFT until its 5 proposed additions are closed with evidence, a run-log entry exists, and a named human has read an audit of the sample run — see the agent twin for the exact rule.

**Audience:** an F-1 new graduate, OPT not started, targeting Data Engineer or ML Engineer roles.
**Agent twin:** `recipes/cases/2026fa/Sreevarshann-newgrad-de-ml-optwindow.md`
**Chapters:** 7, 8, 10, 11 (Ch 9 report-only; Ch 2 for the 3-3-2 day).

## Purpose

Answer: of the companies with a record of sponsoring these roles, which deserve today's application hours, which need a posting checked first, and which are people to meet rather than places to apply? If the evidence does not support an answer, the tool must say so and why.

## What it can verify

- A company's recorded H-1B approval count and which of its sponsored titles match Data/ML Engineer keywords.
- Whether those titles are all senior (networking target) or include an entry-level one (apply candidate).
- Whether a role has every input the scorer needs before it is scored — and that nothing incomplete reaches the scorer.
- Whether a posting check exists, how old it is, whether a human or an AI made it, and whether the liveness tool's recorded result disagrees.
- The 90-day window arithmetic for the persona, shown step by step.

## What it cannot verify

- Whether any posting is live — no human checked one in run 1.
- Whether sponsorship counts apply to this role (they are company-wide) or to this company (HUMAN INC and the PATHAI / PATHRAI pair look like possible wrong matches — unverified).
- Companies outside the "top sponsored titles" field, titles like "Data Analytics Engineer", or anything labelled "AI Engineer" (zero matches).
- Funding: no shipped Form D sample matches, and most funding dates are years old.
- Pay for this employer: the BLS wage is a national occupation median, and the job-code mapping is a judgment.

## Dependencies

- Python 3 (standard library only) and Node (for the scorer).
- Playwright's Chromium, installed outside the repo, only for the optional liveness cross-check.
- `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv`, `data/bls/compact/soc_occupation_compact.csv`, `data/sec/form-d/processed/sample/*.sample.json`.
- `search/examples/meera-krishnan/profile.yml` (fictional persona) and `course/2026fa/submissions/Sreevarshann/inputs/posting-checks.csv`.

## Annotated commands

Full run (expected: a report and a run log in `course/2026fa/submissions/Sreevarshann/runs/<run-date>/`; the scorer runs only if a role passes every gate):

```bash
python3 scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/run.py
```

Offline tests (expected: all pass; no network):

```bash
python3 -m unittest discover -s scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/tests -v
```

Liveness cross-check on one posting (expected: `active`, `expired`, or `uncertain` — a hint, not a verdict):

```bash
npm run ats:liveness -- <posting-url>
```

## What it produces

- `report.md`: a warning first if no human checked the postings, then the funnel, the scored roles, the lists, what cannot be verified, and one next action per company.
- `run-log.json`: everything the agent needs to re-trace the run, including input hashes and the scorer's own output.

## Named failure modes

1. **Ghost "open"** — an AI search says a posting is open but the page is gone (AMGEN, HTTP 404). Mitigation: a recorded tool result that contradicts an AI status sends the role back to "verify posting".
2. **False "expired"** — the liveness tool reads a bot-blocked page as expired. Mitigation: a human's status always governs; the tool only flags.
3. **Wrong company** — a generic name joins to the wrong sponsorship record (HUMAN INC?). Mitigation: shown under Cannot verify; check the company before relying on its count.
4. **Silent default** — the scorer treats a missing vote as 0 and a missing gate as open. Mitigation: nothing incomplete is sent; a mutant test proves the guard holds.
5. **Clock passes** — after OPT start the run halts rather than guess the remaining days. Mitigation: re-enter days used (proposed addition).
