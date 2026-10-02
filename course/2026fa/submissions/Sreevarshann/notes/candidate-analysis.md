# Role-type candidate analysis — 2026fa · Sreevarshann

## Executive summary

**What this is.** A record of how the target role type for this contribution was chosen: three candidate definitions of "the jobs this student is after," each measured against the repository's real company-sponsorship, funding, and wage data before any choice was made.

**Why read it.** Every later number in this contribution depends on which companies count as a match. This file shows the exact rule, the counts it produced, and the decisions the student made after seeing them, so the selection can be checked and rerun rather than taken on trust.

**What it found and decided.**
- Only about 1 in 20 companies in the source list (1,557 of 30,369) carries any sponsored-job-title, approval, or salary data; the rest are blank, so role matching can only work inside that minority.
- The student chose the combined Data Engineer + Machine Learning Engineer definition: 114 companies, every one with at least one past sponsorship approval.
- Split by seniority of the matched titles: **64 companies are entry-eligible** (at least one non-senior matching title) and **50 are senior-only**. Senior-only companies are kept as networking targets, not application targets.
- Funding evidence is thin: only 5 entry-eligible and 2 senior-only companies show a funding round in the last 24 months, and none of the 114 appear in the shipped sample of SEC funding filings.
- The literal title "AI Engineer" effectively does not occur in the data; the AI side of the search is represented by Machine Learning Engineer titles.

## Decisions recorded (your-input — the student's, 2026-10-02)

| Decision | Value |
|---|---|
| Role definition | Candidate C — keywords `data engineer`, `data engineering`, `machine learning engineer`, `ml engineer`, `ai engineer`, `ai/ml`, `deep learning engineer`, `mlops`; case-insensitive, keyword not glued to other letters |
| Senior title keywords | `senior`, `sr`, `staff`, `principal`, `lead`, `manager`, `director`, `head`, `vp`, `iii`, `iv`, `founding` |
| Company classes | entry-eligible = at least one matched title is non-senior; senior-only = every matched title is senior |
| Known edge case | "Associate Manager – Data Engineering" is classified senior (via `manager`) — kept deliberately |
| SOC mapping | 15-1252 Software Developers — **model-judgment, report-only**; BLS has no Data Engineer or ML Engineer occupation, and the scorer's role-quality weight is 0 |

## Run record

- **Command (from repo root):** `python3 course/2026fa/submissions/Sreevarshann/notes/candidate-analysis.py`
- **Inputs (public repo data, read-only):** `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv`, `data/bls/compact/soc_occupation_compact.csv`, `data/sec/form-d/processed/sample/*.sample.json`
- **Name normalizer reused, not re-implemented:** `normalize_company_name` from `scripts/sec/sec-all-quarters.py`
- **Date pinned:** today = 2026-10-02; 24-month funding window = 2024-10-02 to 2026-10-02
- **Exit status:** 0
- **Privacy check before saving:** output contains no phone numbers, email addresses, executive/board/person fields, or company names — only job-title strings and aggregate counts.
- **Label key:** counts and wages below are `record` (computed from the files above); the SOC choice is `model-judgment`; keyword lists and seniority rules are `your-input`.

## Full output (verbatim)

```text
source rows=30369  rows with any sponsored title=1557
SEC sample normalized names=196  24-month cutoff=2024-10-02 (today=2026-10-02)

==============================================================================
A  Data Engineer
  keywords=['data engineer', 'data engineering']  SOC=15-1243
  1. matched rows: 64
  2. Total Approvals > 0: 64  (min=2 median=38 max=1882)
  3. non-blank latest_funding_date: 63 (unparseable 0, future 0); within last 24 months: 2
  4. exact normalized-name matches to Form D sample: 0
  5. blank or non-numeric scorer fields among matched rows:
       Total Approvals: 0
       Total Denials: 0
       Approval_Rate: 0
       latest_funding_date: 1
       median_salary_offered: 0
       rows with at least one: 1
  6. BLS rows for 15-1243:
       15-1243.00 Database Architects: annual_median_wage=135980.0 (oews_year 2024)
       15-1243.01 Data Warehousing Specialists: annual_median_wage=135980.0 (oews_year 2024)
  matched title strings (29 distinct, check for false positives): [' Data Engineer', 'Associate Manager – Data Engineering', 'Backend Data Engineer', 'Clinical Data Engineer', 'DATA ENGINEER', 'Data Engineer', 'Data Engineer 2', 'Data Engineer 20516.3745', 'Data Engineer II', 'Data Engineer II (00049724)', 'Data Engineer III', 'Data Engineer III ', 'Data Engineer, Professional Services', 'Data Engineering Lead', 'Manager, Data Engineering', 'Manager, Data Engineering (20639.22.16)', 'Principal Data Engineer', 'Principal Data Engineer, Lead', 'SENIOR DATA ENGINEER', 'Senior Data Engineer', 'Senior Data Engineer ', 'Senior Director, Data Engineering ', 'Senior Engineering Manager, Data Engineering', 'Senior Manager, Data Engineering', 'Software Data Engineer ', 'Sr. Data Engineer', 'Staff AI/ML Data Engineer', 'Staff Data Engineer', 'Staff Data Engineer ']

==============================================================================
B  ML/AI Engineer
  keywords=['machine learning engineer', 'ml engineer', 'ai engineer', 'ai/ml', 'deep learning engineer', 'mlops']  SOC=15-2051
  1. matched rows: 53
  2. Total Approvals > 0: 53  (min=2 median=16 max=856)
  3. non-blank latest_funding_date: 53 (unparseable 0, future 0); within last 24 months: 5
  4. exact normalized-name matches to Form D sample: 0
  5. blank or non-numeric scorer fields among matched rows:
       Total Approvals: 0
       Total Denials: 0
       Approval_Rate: 0
       latest_funding_date: 0
       median_salary_offered: 0
       rows with at least one: 0
  6. BLS rows for 15-2051:
       15-2051.00 Data Scientists: annual_median_wage=112590.0 (oews_year 2024)
       15-2051.01 Business Intelligence Analysts: annual_median_wage=112590.0 (oews_year 2024)
       15-2051.02 Clinical Data Managers: annual_median_wage=112590.0 (oews_year 2024)
  matched title strings (18 distinct, check for false positives): ['Deep Learning Engineer', 'Founding ML Engineer', 'Lead Machine Learning Engineer', 'Machine Learning Engineer', 'Machine Learning Engineer ', 'Machine Learning Engineer (L2)', 'Machine Learning Engineer / AI Scientist ', 'Machine Learning Engineer II', 'Machine Learning Engineer III', 'Principal Machine Learning Engineer - Personalization', 'Robotics and Machine Learning Engineer', 'SENIOR MACHINE LEARNING ENGINEER', 'Senior Machine Learning Engineer', 'Senior Machine Learning Engineer ', 'Senior Machine Learning Engineer I', 'Sr. Machine Learning Engineer', 'Staff AI/ML Data Engineer', 'Staff Machine Learning Engineer']

==============================================================================
C  Data + AI Engineer (union)
  keywords=['data engineer', 'data engineering', 'machine learning engineer', 'ml engineer', 'ai engineer', 'ai/ml', 'deep learning engineer', 'mlops']  SOC=15-1252
  1. matched rows: 114
  2. Total Approvals > 0: 114  (min=2 median=22 max=1882)
  3. non-blank latest_funding_date: 113 (unparseable 0, future 0); within last 24 months: 7
  4. exact normalized-name matches to Form D sample: 0
  5. blank or non-numeric scorer fields among matched rows:
       Total Approvals: 0
       Total Denials: 0
       Approval_Rate: 0
       latest_funding_date: 1
       median_salary_offered: 0
       rows with at least one: 1
  6. BLS rows for 15-1252:
       15-1252.00 Software Developers: annual_median_wage=133080.0 (oews_year 2024)
  matched title strings (46 distinct, check for false positives): [' Data Engineer', 'Associate Manager – Data Engineering', 'Backend Data Engineer', 'Clinical Data Engineer', 'DATA ENGINEER', 'Data Engineer', 'Data Engineer 2', 'Data Engineer 20516.3745', 'Data Engineer II', 'Data Engineer II (00049724)', 'Data Engineer III', 'Data Engineer III ', 'Data Engineer, Professional Services', 'Data Engineering Lead', 'Deep Learning Engineer', 'Founding ML Engineer', 'Lead Machine Learning Engineer', 'Machine Learning Engineer', 'Machine Learning Engineer ', 'Machine Learning Engineer (L2)', 'Machine Learning Engineer / AI Scientist ', 'Machine Learning Engineer II', 'Machine Learning Engineer III', 'Manager, Data Engineering', 'Manager, Data Engineering (20639.22.16)', 'Principal Data Engineer', 'Principal Data Engineer, Lead', 'Principal Machine Learning Engineer - Personalization', 'Robotics and Machine Learning Engineer', 'SENIOR DATA ENGINEER', 'SENIOR MACHINE LEARNING ENGINEER', 'Senior Data Engineer', 'Senior Data Engineer ', 'Senior Director, Data Engineering ', 'Senior Engineering Manager, Data Engineering', 'Senior Machine Learning Engineer', 'Senior Machine Learning Engineer ', 'Senior Machine Learning Engineer I', 'Senior Manager, Data Engineering', 'Software Data Engineer '] …

==============================================================================
SENIORITY SPLIT — candidate C
  senior keywords=['senior', 'sr', 'staff', 'principal', 'lead', 'manager', 'director', 'head', 'vp', 'iii', 'iv', 'founding']
  matched rows=114  distinct company_name=114
  entry-eligible: 64 rows | Total Approvals > 0: 64 (min=2 median=22 max=1882) | funding date in last 24 months: 5 (blank funding date: 1)
  senior-only: 50 rows | Total Approvals > 0: 50 (min=2 median=22 max=856) | funding date in last 24 months: 2 (blank funding date: 0)
  title classification (audit):
    senior     Associate Manager – Data Engineering
    non-senior Backend Data Engineer
    non-senior Clinical Data Engineer
    non-senior DATA ENGINEER
    non-senior Data Engineer
    non-senior Data Engineer 2
    non-senior Data Engineer 20516.3745
    non-senior Data Engineer II
    non-senior Data Engineer II (00049724)
    senior     Data Engineer III
    non-senior Data Engineer, Professional Services
    senior     Data Engineering Lead
    non-senior Deep Learning Engineer
    senior     Founding ML Engineer
    senior     Lead Machine Learning Engineer
    non-senior Machine Learning Engineer
    non-senior Machine Learning Engineer (L2)
    non-senior Machine Learning Engineer / AI Scientist
    non-senior Machine Learning Engineer II
    senior     Machine Learning Engineer III
    senior     Manager, Data Engineering
    senior     Manager, Data Engineering (20639.22.16)
    senior     Principal Data Engineer
    senior     Principal Data Engineer, Lead
    senior     Principal Machine Learning Engineer - Personalization
    non-senior Robotics and Machine Learning Engineer
    senior     SENIOR DATA ENGINEER
    senior     SENIOR MACHINE LEARNING ENGINEER
    senior     Senior Data Engineer
    senior     Senior Director, Data Engineering
    senior     Senior Engineering Manager, Data Engineering
    senior     Senior Machine Learning Engineer
    senior     Senior Machine Learning Engineer I
    senior     Senior Manager, Data Engineering
    non-senior Software Data Engineer
    senior     Sr. Data Engineer
    senior     Sr. Machine Learning Engineer
    senior     Staff AI/ML Data Engineer
    senior     Staff Data Engineer
    senior     Staff Machine Learning Engineer
```
