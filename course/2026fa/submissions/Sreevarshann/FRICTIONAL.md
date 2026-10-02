# FRICTIONAL — 2026fa · Sreevarshann

## Executive summary

This is my honest log of attempts, checks, and human vs. AI contributions for this contribution.

## Entry template

### Entry —

- **Date/time:**
- **Step:**
- **What I tried:**
- **What I expected:**
- **What happened:**
- **What I checked or changed:**
- **Human vs AI (accepted / modified / rejected):**
- **Trace (commit SHA, file, test, command):**

### Entry 1
- **Date/time:** 2026-10-02, ~17:00
- **Step:** Setup — clone and session folder
- **What I tried:** Asked Claude Code to clone my fork and install.
- **What I expected:** Clone into my new Reallocation folder.
- **What happened:** Claude Code was started inside an unrelated project folder (Brut) and offered to clone there. After I restarted in Reallocation, the desktop session had two folders attached and used the parent as its working directory, so the repo's CLAUDE.md didn't auto-load (confirmed with pwd).
- **What I checked or changed:** Checked pwd and the session folder chip in a screenshot. Told Claude Code to treat the-reallocation-engine subfolder as the repo root and read CLAUDE.md, AGENTS.md, and SNICKERDOODLE.md explicitly.
- **Human vs AI:** Claude (chat) diagnosed the two-folder session from my screenshot and wrote the redirect prompt; I accepted it.
- **Trace:** none (environment setup, no commit).

### Entry 2
- **Date/time:** 2026-10-02, evening
- **Step:** Orientation and baseline
- **What I tried:** Had Claude Code read the governing docs and run doctor, verify, ats:scan --dry-run, and the baseline score.
- **What I expected:** Everything runs; the scorer can be imported as CONTRIBUTING.md says.
- **What happened:** doctor and verify passed. ats:scan failed (no portals.yml). role-scorer.mjs has no exports, so only the CLI route works. A missing sponsorship vote scores the same as p = 0, and a missing liveness or timeline gate defaults to 1.0 (open) while still being labeled record/your-input. 4 of 6 CI harness scripts don't exist. package-lock.json was already modified before any work, probably by my local npm install (not verified).
- **What I checked or changed:** Restored package-lock.json with git restore. Decided my prototype must block missing evidence before it reaches the scorer instead of trusting the scorer's defaults.
- **Human vs AI:** Claude Code found the scorer behaviors; Claude (chat) proposed the "block before scoring" design; I accepted it. Unresolved: whether a red CI harness job is acceptable for submission — asking a TA.
- **Trace:** /tmp/orientation-report.md (uncommitted), scripts/score/role-scorer.mjs.

### Entry 3
- **Date/time:** 2026-10-02, evening
- **Step:** Checking the assignment's "Facts that bite"
- **What I tried:** Gave Claude Code the eight facts to check against the repo.
- **What I expected:** All eight hold.
- **What happened:** Seven hold, three of those worse than stated. Fact 6 doesn't match: four recipes are RUNNABLE-SAMPLE, not all DRAFT. validate-h1b-join-sample.py would overwrite a tracked audit file if the full data were present.
- **What I checked or changed:** Noted not to run that script on my branch.
- **Human vs AI:** Claude Code ran the checks; I accepted the findings.
- **Trace:** /tmp/localwage-fresh.txt, /tmp/h1b-fresh.txt.

### Entry 4
- **Date/time:** 2026-10-02, evening
- **Step:** Choosing the role type
- **What I tried:** Defining the persona's target roles as AI Engineer and Data Engineer.
- **What I expected:** A SOC column to filter on, and Form D funding matches.
- **What happened:** The 80 Days CSV has no SOC column; only 1,557 of 30,369 rows have any sponsored titles. "AI Engineer" matched zero rows under the matching rule. Zero companies in any candidate matched a Form D sample company. Only 5 entry-eligible companies have a funding date in the last 24 months.
- **What I checked or changed:** Chose candidate C (Data Engineer + ML Engineer keywords, 114 companies). Added a seniority split. Classified "III", "IV", and "Founding" titles as senior, because for a new grad a false "entry-eligible" wastes an application, while a false "senior-only" only moves a company to the networking list. Result: 64 entry-eligible, 50 senior-only.
- **Human vs AI:** Claude Code computed all counts. Claude (chat) recommended candidate C, the seniority split, and the III/IV/Founding rule; I accepted all three. "Associate Manager – Data Engineering" stays senior as a known edge case.
- **Trace:** da4f71b, course/2026fa/submissions/Sreevarshann/notes/candidate-analysis.md.

### Entry 5
- **Date/time:** 2026-10-02, ~18:30
- **Step:** First commit — privacy check
- **What I tried:** Committing the candidate analysis.
- **What I expected:** A clean commit.
- **What happened:** Claude Code noticed the commit author email was my machine's .local address, which carries my name and machine and isn't caught by pii-scan (it doesn't check commit metadata). The working-tree pii-scan also flags an npm package author's email address in the tracked package-lock.json on main — not my file.
- **What I checked or changed:** Set my GitHub noreply address for this repo only, re-authored the commit (abc26d0 → da4f71b), and confirmed with git log that only the noreply address remains in branch history.
- **Human vs AI:** Claude Code caught the email issue; I chose the fix and provided the address.
- **Trace:** da4f71b, git log main..HEAD --format='%ae'.

### Note on authorship of this log
- Entries 1–5 were drafted by Claude (chat) from our conversation transcript at my request, then reviewed and confirmed by me for accuracy. Later entries are written by me unless marked otherwise.
