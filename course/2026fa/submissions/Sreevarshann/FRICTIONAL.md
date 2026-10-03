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

### Entry 6
- **Date/time:** 2026-10-02, evening
- **Step:** Prototype core — normalizer import
- **What I tried:** Reusing normalize_company_name from scripts/sec/sec-all-quarters.py, as the brief committed to.
- **What I expected:** A clean import.
- **What happened:** The file imports pandas at line 1. It only worked locally because my python3 is Anaconda; in a clean stdlib-only environment it fails. CI installs only pyyaml. My committed candidate-analysis.py had the same hidden dependency.
- **What I checked or changed:** Switched to the stdlib-only normalize_company_name in scripts/sec/entity-resolution.py after Claude Code showed 0 disagreements across 30,569 names; made a dated fix to candidate-analysis.py; recorded as CHANGE-BRIEF R1.
- **Human vs AI:** Claude Code found the dependency and ran the equivalence check; I chose option A and a dated fix over a note-only correction.
- **Trace:** 01d07f1, CHANGE-BRIEF R1.

### Entry 7
- **Date/time:** 2026-10-02, evening
- **Step:** Posting checks
- **What I tried:** I did not do human posting checks. Claude (chat) found candidate URLs and statuses via web search; I committed them labeled model-judgment, checked_by "not human-verified".
- **What I expected:** The AI's "open" statuses to hold up.
- **What happened:** ats:liveness returned HTTP 404 for the AMGEN URL the AI reported as open, and "insufficient content" for Twilio. Under R3, AMGEN would have scored Apply on a dead link.
- **What I checked or changed:** Added R4 — a record outranks a model-judgment on posting status, so contradicted AI checks go to verify-posting. Added R5 so a human check wins same-date ties. Chose not to add a human check for this run; G4 was never cleared and the whole run is provisional.
- **Human vs AI:** The stale URL came from Claude (chat). Claude Code ran the tool and implemented R4/R5. I chose the rules and chose to skip the human check. Unresolved: no role in this run reached a real decision.
- **Trace:** 8cde854, 6202dc8, 806ce8a, runs/ats-liveness-2026-10-02.txt.

### Entry 8
- **Date/time:** 2026-10-02, late evening
- **Step:** End-to-end run and recipe status
- **What I tried:** Running run.py through the real scorer and marking the recipe RUNNABLE-SAMPLE.
- **What I expected:** RUNNABLE-SAMPLE to be justified because the prototype runs end to end.
- **What happened:** Claude Code later admitted the committed run used Anaconda, not the clean environment, because of a symlink loop it created; a clean rerun reproduced identical scorer outputs. SNICKERDOODLE lines 58–59 require zero open TODOs and a read audit before RUNNABLE-SAMPLE; I have 5 TODOs.
- **What I checked or changed:** Held the recipe at DRAFT with a sentence explaining why. Break attempt (d) exposed a crash on a missing input file, which I then had fixed.
- **Human vs AI:** Claude Code caught and corrected its own interpreter error. Claude (chat) advised holding at DRAFT; I accepted. The scorer's own role-scores.md calls the 100% skip "healthy", which my report contradicts.
- **Trace:** bf8b65d, d32daa0, c9344b0, 2cb57e8 (fix), a56845e (docs).

### Note on authorship of entries 6–8
- Drafted by Claude (chat) from our conversation at my request, then reviewed and confirmed by me.

### Entry 9
- **Date/time:** 2026-10-02, late night
- **Step:** Final validation — fresh clone and audit
- **What I tried:** Running the prototype and repo checks from a fresh clone of my branch, then a requirements audit against the assignment.
- **What I expected:** Everything to pass as it did in my working copy.
- **What happened:** npm run verify failed in the fresh clone with the clean interpreter: the repo's manifest check needs PyYAML, which CI installs but my earlier "passes" had silently used Anaconda for — the same hidden-dependency pattern as pandas. The README command also refused to run on a date that already had a run folder. Claude Code nearly committed the npm author's email again in pasted pii-scan output; the working-tree scan caught it before commit this time. The audit found five partial items: a stale lifecycle sentence, facts 6–8 not named, a stale diff stat, and the justification slightly over one page.
- **What I checked or changed:** Mirrored CI with a PyYAML-only environment (verify passed); documented the --out-root rerun command in the README; fixed all four partial items.
- **Human vs AI:** Claude Code ran the clone, found the PyYAML issue, and did the audit; Claude (chat) recommended mirroring CI and fixing the README; I approved both. This entry was drafted by Claude (chat) and reviewed by me.
- **Trace:** 93bb449, and this commit.
