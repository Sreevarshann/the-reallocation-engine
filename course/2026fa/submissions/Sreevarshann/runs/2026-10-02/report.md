# Run report — newgrad-de-ml-optwindow · 2026-10-02

## Executive summary

> **Provisional — read first.** G4 human liveness gate NOT cleared for 3 scored role(s) (femtosense:ml_engineer, human:data_engineer, overjet:ml_engineer): their posting status comes from a check marked 'not human-verified' (labelled model-judgment), not from a human. Every decision for these roles is provisional.

**What this is.** The first end-to-end run of a tool that sorts companies for a new-graduate F-1 student targeting Data Engineer and ML Engineer roles: which to apply to, which to verify first, which are networking targets, and which are blocked — each with the evidence behind it.

**Why read it.** It shows what the evidence actually supports today, and where it stops. Every value is labelled as a record, a model judgment, or the student's own input.

**What it found.**
- 3 role(s) reached the scorer; result: Skip 3.
- 61 role(s) need a posting checked before they can be scored; 2 of them because an AI-reported status was contradicted by the liveness tool.
- 53 role(s) at senior-only companies are networking targets, not applications.
- 0 role(s) blocked for missing or unusable evidence.
- No posting in this run was checked by a human, so no decision here is final.

## Run record

- Run date: 2026-10-02 · persona: meera-krishnan (fictional)
- Command: `python3 scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/run.py`
- Scorer: `npm run score -- course/2026fa/submissions/Sreevarshann/runs/2026-10-02/roles.json --out-dir course/2026fa/submissions/Sreevarshann/runs/2026-10-02` → exit 0; results read from `role-scores.json`
- Timeline gate: 2026-10-02 + 60 days = 2026-12-01 <= window end 2027-04-15 -> 1.0 (lag is an assumption, not a record)
- Input `scripts/contrib/2026fa/Sreevarshann-newgrad-de-ml-optwindow/fixtures/persona-meera-krishnan.json` sha256 `b87c445a25df…`
- Input `course/2026fa/submissions/Sreevarshann/inputs/posting-checks.csv` sha256 `a3656719d1ea…`
- Input `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv` sha256 `eccdee2addf4…`
- Input `data/bls/compact/soc_occupation_compact.csv` sha256 `bac5acf77ca2…`
- Outputs: `course/2026fa/submissions/Sreevarshann/runs/2026-10-02/report.md`, `course/2026fa/submissions/Sreevarshann/runs/2026-10-02/run-log.json`, `course/2026fa/submissions/Sreevarshann/runs/2026-10-02/roles.json`, scorer `role-scores.json` / `role-scores.md`

## Funnel

| Stage | Count | Label |
|---|---|---|
| Companies in the sponsorship dataset | 30369 | record |
| …with any sponsored-job-title data | 1557 | record |
| …matching the 8 role keywords | 114 | record (keywords: your-input) |
| …entry-eligible (apply candidates) | 64 | record (seniority rule: your-input) |
| …senior-only (networking list) | 50 | record (seniority rule: your-input) |
| Posting checks loaded (valid rows) | 5 | label per row (see verify / scored tables) |
| Roles sent to the scorer | 3 | after gates G1–G5 |

## Scored roles

| Company | Role | Approvals [record] | Tier / p [your-input] | Fit [your-input] | Liveness | Timeline [your-input] | Composite | Scorer result | Scorer reason | G4 human-cleared |
|---|---|---|---|---|---|---|---|---|---|---|
| FEMTOSENSE INC | ml_engineer | 6 | possible / 0.4 | 0.5 | 0.0 [model-judgment] (not found) | 1.0 | 0 | **Skip** | gated: liveness ≈ 0.000 (a closed gate zeroes the composite regardless of votes) | **no** |
| HUMAN INC | data_engineer | 1382 | Proven / 0.8 | 0.7 | 0.0 [model-judgment] (not found) | 1.0 | 0 | **Skip** | gated: liveness ≈ 0.000 (a closed gate zeroes the composite regardless of votes) | **no** |
| OVERJET INC | ml_engineer | 48 | likely / 0.6 | 0.5 | 0.0 [model-judgment] (not found) | 1.0 | 0 | **Skip** | gated: liveness ≈ 0.000 (a closed gate zeroes the composite regardless of votes) | **no** |

Liveness cross-check (ats:liveness, record) for scored roles:

- FEMTOSENSE INC: status `not found` [model-judgment] · tool `uncertain` — content present but no visible apply control found
- HUMAN INC: status `not found` [model-judgment] · tool `uncertain` — navigation error: page.goto: Download is starting
- OVERJET INC: status `not found` [model-judgment] · tool `uncertain` — navigation error: page.goto: Download is starting

## Verify-posting list

| Company | Role | Tier | Approvals [record] | Reason |
|---|---|---|---|---|
| AMGEN INC | data_engineer | Proven | 1882 | conflict: model-judgment status vs ats:liveness record (status=open [model-judgment], tool_result=expired [record]: HTTP 404) |
| TWILIO INC | ml_engineer | Proven | 802 | conflict: model-judgment status vs ats:liveness record (status=open [model-judgment], tool_result=expired [record]: insufficient content — likely nav/footer only) |
| AGENT TECHNOLOGIES INC | ml_engineer | Proven | 216 | unchecked: no posting check recorded |
| AIM INTELLIGENT MACHINES INC | ml_engineer | likely | 10 | unchecked: no posting check recorded |
| ANDIUM INC | ml_engineer | possible | 4 | unchecked: no posting check recorded |
| APPLOVIN CORP | ml_engineer | Proven | 130 | unchecked: no posting check recorded |
| AVALANCHE BIOTECHNOLOGIES INC | data_engineer | Proven | 60 | unchecked: no posting check recorded |
| BENEFITS SCIENCE LLC | data_engineer | likely | 18 | unchecked: no posting check recorded |
| BIOME ANALYTICS INC | data_engineer | possible | 2 | unchecked: no posting check recorded |
| BLUE RIVER TECHNOLOGY INC | ml_engineer | possible | 2 | unchecked: no posting check recorded |
| CARGO CHIEF ACQUISITION INC | ml_engineer | possible | 2 | unchecked: no posting check recorded |
| CELESTIAL AI INC | ml_engineer | Proven | 56 | unchecked: no posting check recorded |
| CENTIFIC GLOBAL SOLUTIONS INC | data_engineer | likely | 22 | unchecked: no posting check recorded |
| COHERE HEALTH INC | ml_engineer | Proven | 104 | unchecked: no posting check recorded |
| COURSERA INC | data_engineer | Proven | 88 | unchecked: no posting check recorded |
| CPACKET NETWORKS INC | ml_engineer | likely | 16 | unchecked: no posting check recorded |
| DEAKO INC | data_engineer | possible | 8 | unchecked: no posting check recorded |
| DOCUSIGN INC | data_engineer | Proven | 1082 | unchecked: no posting check recorded |
| DV01 INC | data_engineer | likely | 16 | unchecked: no posting check recorded |
| ECLINICAL SOLUTIONS LLC | data_engineer | likely | 40 | unchecked: no posting check recorded |
| ENTRUPY INC | data_engineer | likely | 10 | unchecked: no posting check recorded |
| EXABEAM INC | data_engineer | Proven | 68 | unchecked: no posting check recorded |
| FORMATION DATA SYSTEMS INC | data_engineer | Proven | 130 | unchecked: no posting check recorded |
| GENIES INC | ml_engineer | likely | 22 | unchecked: no posting check recorded |
| GEOPIPE INC | ml_engineer | possible | 4 | unchecked: no posting check recorded |
| GORGIAS INC | ml_engineer | likely | 22 | unchecked: no posting check recorded |
| HAPPY MONEY INC | data_engineer | possible | 2 | unchecked: no posting check recorded |
| HAYDEN AI TECHNOLOGIES INC | ml_engineer | Proven | 52 | unchecked: no posting check recorded |
| IMMUNEID INC | data_engineer | possible | 2 | unchecked: no posting check recorded |
| INMARKET MEDIA LLC | data_engineer | likely | 46 | unchecked: no posting check recorded |
| KENSHO TECHNOLOGIES INC | ml_engineer | likely | 40 | unchecked: no posting check recorded |
| KINETIC AUTOMATION INC | ml_engineer | likely | 16 | unchecked: no posting check recorded |
| LENDBUZZ INC | ml_engineer | Proven | 60 | unchecked: no posting check recorded |
| LOOKING GLASS PRODUCTIONS LLC | data_engineer | likely | 22 | unchecked: no posting check recorded |
| MANGO TECHNOLOGIES INC | data_engineer | likely | 38 | unchecked: no posting check recorded |
| MOLOCO INC | ml_engineer | Proven | 200 | unchecked: no posting check recorded |
| NATRON ENERGY INC | data_engineer | likely | 40 | unchecked: no posting check recorded |
| NERDWALLET INC | data_engineer | Proven | 88 | unchecked: no posting check recorded |
| NEXTDOOR INC | ml_engineer | Proven | 222 | unchecked: no posting check recorded |
| PATHAI INC | ml_engineer | Proven | 78 | unchecked: no posting check recorded |
| PATHRAI INC | ml_engineer | Proven | 78 | unchecked: no posting check recorded |
| PERSIVIA INC | data_engineer | likely | 14 | unchecked: no posting check recorded |
| PLUS ONE ROBOTICS INC | ml_engineer | likely | 10 | unchecked: no posting check recorded |
| PRESTO AUTOMATION INC | ml_engineer | possible | 2 | unchecked: no posting check recorded |
| PRM SOLUTIONS INC | data_engineer | possible | 2 | unchecked: no posting check recorded |
| RAIN NEUROMORPHICS INC | ml_engineer | likely | 14 | unchecked: no posting check recorded |
| ROOTS AUTOMATION INC | ml_engineer | likely | 12 | unchecked: no posting check recorded |
| SPACECRAFT INC | ml_engineer | possible | 2 | unchecked: no posting check recorded |
| T-REX GROUP INC | data_engineer | possible | 4 | unchecked: no posting check recorded |
| TREASURE DATA INC | data_engineer | likely | 40 | unchecked: no posting check recorded |
| ULTRASENSE SYSTEMS INC | ml_engineer | possible | 2 | unchecked: no posting check recorded |
| UPSTART NETWORK INC | data_engineer | Proven | 316 | unchecked: no posting check recorded |
| VANTA INC | ml_engineer | likely | 10 | unchecked: no posting check recorded |
| VERACYTE INC | data_engineer | likely | 48 | unchecked: no posting check recorded |
| VISICON TECHNOLOGIES INC | data_engineer | Proven | 330 | unchecked: no posting check recorded |
| WELBE HEALTH LLC | data_engineer | likely | 18 | unchecked: no posting check recorded |
| WHEELS UP PARTNERS HOLDINGS LLC | data_engineer | likely | 38 | unchecked: no posting check recorded |
| WIREWHEEL INC | data_engineer | possible | 2 | unchecked: no posting check recorded |
| ZANBATO INC | data_engineer | possible | 4 | unchecked: no posting check recorded |
| ZOOM VIDEO COMMUNICATIONS INC | ml_engineer | possible | 2 | unchecked: no posting check recorded |
| ZOOX INC | data_engineer | Proven | 1364 | unchecked: no posting check recorded |

## Network list (senior-only — networking targets, never scored)

| Company | Role | Matched senior titles [record] | Note |
|---|---|---|---|
| 1LIFE HEALTHCARE INC | data_engineer | Senior Data Engineer |  |
| ACV AUCTIONS INC | ml_engineer | Machine Learning Engineer III |  |
| AKTANA INC | ml_engineer | Senior Machine Learning Engineer |  |
| ANOKIWAVE INC | data_engineer | Senior Data Engineer |  |
| ATTENTIVE MOBILE INC | ml_engineer | Senior Machine Learning Engineer I |  |
| CAPTION HEALTH INC | ml_engineer | Senior Machine Learning Engineer |  |
| CLARIFY HEALTH SOLUTIONS INC | data_engineer | Senior Director, Data Engineering |  |
| COGNIAC CORP | ml_engineer | Sr. Machine Learning Engineer |  |
| DATAMINR INC | data_engineer | Data Engineer III |  |
| DEEPFRAUD TECHNOLOGIES INC | data_engineer | Manager, Data Engineering |  |
| DEXCARE INC | data_engineer | Staff AI/ML Data Engineer |  |
| DEXCARE INC | ml_engineer | Staff AI/ML Data Engineer |  |
| EVOLUS INC | data_engineer | Sr. Data Engineer |  |
| GINGERIO INC | data_engineer | Staff Data Engineer |  |
| GINGERIO INC | ml_engineer | Lead Machine Learning Engineer |  |
| GLASSDOOR INC | data_engineer | Manager, Data Engineering (20639.22.16) |  |
| GUARDANT HEALTH INC | data_engineer | Manager, Data Engineering |  |
| HEADSPACE INC | ml_engineer | Senior Machine Learning Engineer |  |
| HINGE HEALTH INC | data_engineer | Senior Engineering Manager, Data Engineering |  |
| HYPER LABS INC | ml_engineer | Senior Machine Learning Engineer |  |
| IMPERATIVE CARE INC | ml_engineer | Senior Machine Learning Engineer |  |
| INTEGRAL AD SCIENCE INC | data_engineer | Staff Data Engineer |  |
| JUVO PLUS INC | data_engineer | Senior Manager, Data Engineering |  |
| LUA TECHNOLOGIES INC | data_engineer | Senior Data Engineer; Senior Data Engineer |  |
| MAPLEBEAR INC | ml_engineer | Senior Machine Learning Engineer |  |
| MUTINY HQ CORP | data_engineer | Data Engineering Lead |  |
| NUMERADE LABS INC | ml_engineer | SENIOR MACHINE LEARNING ENGINEER |  |
| OCROLUS INC | ml_engineer | Senior Machine Learning Engineer |  |
| OUTSET MEDICAL INC | data_engineer | Staff Data Engineer |  |
| PERSONALIZED BEAUTY DISCOVERY INC | ml_engineer | Senior Machine Learning Engineer; Staff Machine Learning Engineer |  |
| PLUME DESIGN INC | data_engineer | SENIOR DATA ENGINEER |  |
| PROCORE TECHNOLOGIES INC | data_engineer | Senior Data Engineer |  |
| PROVE IDENTITY INC | data_engineer | Data Engineer III |  |
| QUANTIPHI INC | data_engineer | Senior Data Engineer |  |
| QUANTIPHI INC | ml_engineer | Senior Machine Learning Engineer |  |
| REFUELAI INC | ml_engineer | Founding ML Engineer |  |
| REVIVEMED INC | data_engineer | Senior Data Engineer |  |
| RISE INTERACTIVE MEDIA & ANALYTICS LLC | data_engineer | Manager, Data Engineering |  |
| ROBLOX CORP | ml_engineer | Principal Machine Learning Engineer - Personalization |  |
| ROKU INC | data_engineer | Senior Data Engineer |  |
| SILA NANOTECHNOLOGIES INC | data_engineer | Senior Data Engineer |  |
| SOCURE INC | data_engineer | Sr. Data Engineer |  |
| THEREALREAL INC | ml_engineer | Senior Machine Learning Engineer |  |
| THIRTY MADISON INC | data_engineer | Senior Data Engineer |  |
| TREAT TECHNOLOGIES INC | ml_engineer | Senior Machine Learning Engineer |  |
| TREDENCE INC | data_engineer | Associate Manager – Data Engineering |  |
| TYPEFACE INC | ml_engineer | Staff Machine Learning Engineer |  |
| UNDERDOG SPORTS HOLDINGS INC | ml_engineer | Senior Machine Learning Engineer |  |
| UNITE USA INC | data_engineer | Senior Data Engineer; Staff Data Engineer |  |
| VILLAGE PRACTICE MANAGEMENT COMPANY LLC | data_engineer | Principal Data Engineer |  |
| YEXT INC | data_engineer | Senior Data Engineer |  |
| YIELDMO INC | data_engineer | Principal Data Engineer, Lead |  |
| ZENLEADS INC | ml_engineer | Senior Machine Learning Engineer |  |

## Blocked list

Nothing blocked in this run.

## Cannot verify

- ats:liveness has no 'not found' result: removed and closed postings both report 'expired'; only the reason text tells them apart
- ats:liveness classifies 'insufficient content' as expired: a slow or bot-blocked page can be reported expired while the posting is live
- Funding not cross-checkable for 64 companies: none appear in the shipped Form D sample (full quarters are not in a fresh clone). Normalized names: agenttechnologies, aimintelligentmachines, amgen, andium, applovin, avalanchebiotechnologies, benefitsscience, biomeanalytics, bluerivertechnology, cargochiefacquisition, celestialai, centificglobalsolutions, coherehealth, coursera, cpacketnetworks, deako, docusign, dv01, eclinicalsolutions, entrupy, exabeam, femtosense, formationdatasystems, genies, geopipe, gorgias, happymoney, haydenaitechnologies, human, immuneid, inmarketmedia, kenshotechnologies, kineticautomation, lendbuzz, lookingglassproductions, mangotechnologies, moloco, natronenergy, nerdwallet, nextdoor, overjet, pathai, pathrai, persivia, plusonerobotics, prestoautomation, prmsolutions, rainneuromorphics, rootsautomation, spacecraft, treasuredata, trexgroup, twilio, ultrasensesystems, upstartnetwork, vanta, veracyte, visicontechnologies, welbehealth, wheelsuppartnersholdings, wirewheel, zanbato, zoomvideocommunications, zoox.
- Whether any posting is live: no human checked a posting in this run.
- Sponsorship strength is company-wide, not role-specific; 'top' titles only.

## Report-only context (no effect on any score)

| Role | SOC [model-judgment] | O*NET title [record] | National annual median wage, 2024 [record] |
|---|---|---|---|
| data_engineer | 15-1243 | Database Architects | 135,980 |
| data_engineer | 15-1243 | Data Warehousing Specialists | 135,980 |
| ml_engineer | 15-2051 | Data Scientists | 112,590 |
| ml_engineer | 15-2051 | Business Intelligence Analysts | 112,590 |
| ml_engineer | 15-2051 | Clinical Data Managers | 112,590 |

| Company | Latest funding date [record] | Stage [record] | Approval rate % [record, not scored] |
|---|---|---|---|
| FEMTOSENSE INC | 2024-11-26 | Seed | 75.0 |
| HUMAN INC | 2018-09-13 | Series B | 99.13916786226686 |
| OVERJET INC | 2024-02-16 | Series C | 96.0 |

## Next action per company

Fixed rules from this report's logic, not a model judgment.

| Company | Role | List | Next action |
|---|---|---|---|
| FEMTOSENSE INC | ml_engineer | scored | Posting reported 'not found' by an AI web search (not human-verified). Check the company careers site yourself before dropping it; record a human check with the URL and date. |
| HUMAN INC | data_engineer | scored | Posting reported 'not found' by an AI web search (not human-verified). Check the company careers site yourself before dropping it; record a human check with the URL and date. |
| OVERJET INC | ml_engineer | scored | Posting reported 'not found' by an AI web search (not human-verified). Check the company careers site yourself before dropping it; record a human check with the URL and date. |
| AGENT TECHNOLOGIES INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| AIM INTELLIGENT MACHINES INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| AMGEN INC | data_engineer | verify-posting | Open the posting yourself: the AI status and the liveness tool disagree. Record a human check. |
| ANDIUM INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| APPLOVIN CORP | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| AVALANCHE BIOTECHNOLOGIES INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| BENEFITS SCIENCE LLC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| BIOME ANALYTICS INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| BLUE RIVER TECHNOLOGY INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| CARGO CHIEF ACQUISITION INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| CELESTIAL AI INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| CENTIFIC GLOBAL SOLUTIONS INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| COHERE HEALTH INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| COURSERA INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| CPACKET NETWORKS INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| DEAKO INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| DOCUSIGN INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| DV01 INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| ECLINICAL SOLUTIONS LLC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| ENTRUPY INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| EXABEAM INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| FORMATION DATA SYSTEMS INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| GENIES INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| GEOPIPE INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| GORGIAS INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| HAPPY MONEY INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| HAYDEN AI TECHNOLOGIES INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| IMMUNEID INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| INMARKET MEDIA LLC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| KENSHO TECHNOLOGIES INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| KINETIC AUTOMATION INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| LENDBUZZ INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| LOOKING GLASS PRODUCTIONS LLC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| MANGO TECHNOLOGIES INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| MOLOCO INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| NATRON ENERGY INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| NERDWALLET INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| NEXTDOOR INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| PATHAI INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| PATHRAI INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| PERSIVIA INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| PLUS ONE ROBOTICS INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| PRESTO AUTOMATION INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| PRM SOLUTIONS INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| RAIN NEUROMORPHICS INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| ROOTS AUTOMATION INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| SPACECRAFT INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| T-REX GROUP INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| TREASURE DATA INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| TWILIO INC | ml_engineer | verify-posting | Open the posting yourself: the AI status and the liveness tool disagree. Record a human check. |
| ULTRASENSE SYSTEMS INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| UPSTART NETWORK INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| VANTA INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| VERACYTE INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| VISICON TECHNOLOGIES INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| WELBE HEALTH LLC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| WHEELS UP PARTNERS HOLDINGS LLC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| WIREWHEEL INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| ZANBATO INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| ZOOM VIDEO COMMUNICATIONS INC | ml_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| ZOOX INC | data_engineer | verify-posting | Find a current Data/ML Engineer posting on the company's careers site and record a human check. |
| 1LIFE HEALTHCARE INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| ACV AUCTIONS INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| AKTANA INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| ANOKIWAVE INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| ATTENTIVE MOBILE INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| CAPTION HEALTH INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| CLARIFY HEALTH SOLUTIONS INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| COGNIAC CORP | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| DATAMINR INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| DEEPFRAUD TECHNOLOGIES INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| DEXCARE INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| DEXCARE INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| EVOLUS INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| GINGERIO INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| GINGERIO INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| GLASSDOOR INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| GUARDANT HEALTH INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| HEADSPACE INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| HINGE HEALTH INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| HYPER LABS INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| IMPERATIVE CARE INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| INTEGRAL AD SCIENCE INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| JUVO PLUS INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| LUA TECHNOLOGIES INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| MAPLEBEAR INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| MUTINY HQ CORP | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| NUMERADE LABS INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| OCROLUS INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| OUTSET MEDICAL INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| PERSONALIZED BEAUTY DISCOVERY INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| PLUME DESIGN INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| PROCORE TECHNOLOGIES INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| PROVE IDENTITY INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| QUANTIPHI INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| QUANTIPHI INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| REFUELAI INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| REVIVEMED INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| RISE INTERACTIVE MEDIA & ANALYTICS LLC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| ROBLOX CORP | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| ROKU INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| SILA NANOTECHNOLOGIES INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| SOCURE INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| THEREALREAL INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| THIRTY MADISON INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| TREAT TECHNOLOGIES INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| TREDENCE INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| TYPEFACE INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| UNDERDOG SPORTS HOLDINGS INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| UNITE USA INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| VILLAGE PRACTICE MANAGEMENT COMPANY LLC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| YEXT INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| YIELDMO INC | data_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |
| ZENLEADS INC | ml_engineer | network | Networking target: find a contact on the team; do not apply to the senior posting. |

