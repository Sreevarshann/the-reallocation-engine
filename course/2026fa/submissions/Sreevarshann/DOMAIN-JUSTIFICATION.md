# Domain Justification — newgrad-de-ml-optwindow

## Executive summary
*(Drafted by Claude (chat) from my decisions during the session; reviewed and confirmed by me.)* This recipe is for an F-1 master's new graduate (fictional persona) whose OPT has not started, targeting entry-level Data Engineer and ML Engineer roles. It makes two things visible a new grad can't easily see: which companies have sponsored H-1Bs for these titles *at a non-senior level*, and whether a posting that looks open is actually live.

## Who and what situation
An international MS student in data science (STEM) on F-1, graduating 2026-12-12, OPT starting 2027-01-15, with a 90-day unemployment window ending 2027-04-15. Targets: Data Engineer and ML Engineer, any company size or industry. The persona and all dates are fictional; the situation type (F-1 new grad, OPT not started, Data/ML Engineer roles) is the one this recipe is designed for.

## The information asymmetry
A new grad can't easily tell (1) whether a company's sponsorship history includes roles at their level or only senior ones — 50 of the 114 matching sponsors sponsored only senior titles for these roles; and (2) whether a posting is real — in this run, an AI search reported an AMGEN Data Engineer role as open, and the engine's liveness tool found the page returned HTTP 404. Both errors cost a student with a 90-day clock real application time.

## Engine layers
80 Days to Stay (sponsorship approvals and sponsored titles, as a scored vote); Job-Ops (ATS liveness, Ch.8): ats:liveness as a record-level cross-check on posting status, inside the liveness gate; the Cognitive Pivot (BLS/O*NET role quality, Ch.9): BLS wages for the mapped SOC codes, report-only because role_quality carries 0 weight; and the existing composite scorer via its CLI. Funding is shown as context only — the scorer has no funding term; a funding vote is proposed as [TODO: DEV] in the recipe.

## Where it fits the 3-3-2 day
It takes over the research half of the two applying hours: building a shortlist of sponsors for these exact titles and checking whether postings are live before tailoring anything. Its senior-only list (53 company-role pairs) feeds the three networking hours — companies worth an informational conversation, not an application. **Estimate, not a measurement:** if a student researches about 20 companies a week and checking sponsorship history plus posting status by hand takes roughly 15 minutes per company versus about 5 minutes reviewing this tool's report, that's about 20 × 10 min ≈ 3.3 hours saved per week. The per-company times are my assumptions, not timed observations.

## Domain-specific failure modes and who would struggle to catch them
1. **Senior-only sponsorship read as entry-level.** A company with hundreds of approvals looks like a strong sponsor, but if every matched title is Senior, Staff, or Principal, a new grad's application is likely screened out. New grads are least able to tell, because the headline number looks authoritative. The seniority split exists for this; titles like "III" or "Founding" are judgment calls in the rule.
2. **Wrong company match inflating sponsorship.** HUMAN INC carries 1,382 approvals, but its sponsored titles read like a large enterprise IT organization, not the bot-fraud security firm of that name — the record may belong to a different employer (model-judgment, unverified). A student would trust the number and apply; only checking the titles against the actual company reveals it.
