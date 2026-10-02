#!/usr/bin/env python3
# Revised 2026-10-02: normalizer import switched from sec-all-quarters.py to entity-resolution.py because the former requires pandas; output verified identical (see CHANGE-BRIEF R1).
"""Orientation analysis: candidate role-type definitions vs real repo data (2026fa, Sreevarshann).
Run from the repo root:  python3 course/2026fa/submissions/Sreevarshann/notes/candidate-analysis.py
Read-only: reads public repo data (80 Days CSV, BLS compact, SEC Form D samples); writes nothing.
Prints job-title strings and aggregate counts only, no company contact or person fields.
TODAY is pinned so the 24-month funding window is reproducible."""
import csv, glob, importlib.util, json, re, statistics
from datetime import date

TODAY = date(2026, 10, 2)
CUTOFF = date(TODAY.year - 2, TODAY.month, TODAY.day)  # last 24 months

CSV = 'data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv'
BLS = 'data/bls/compact/soc_occupation_compact.csv'
SEC = 'data/sec/form-d/processed/sample/*.sample.json'

CANDIDATES = {
    'A  Data Engineer': (['data engineer', 'data engineering'], '15-1243'),
    'B  ML/AI Engineer': (['machine learning engineer', 'ml engineer', 'ai engineer', 'ai/ml',
                           'deep learning engineer', 'mlops'], '15-2051'),
    'C  Data + AI Engineer (union)': (['data engineer', 'data engineering', 'machine learning engineer',
                                       'ml engineer', 'ai engineer', 'ai/ml', 'deep learning engineer',
                                       'mlops'], '15-1252'),
}
SCORER_FIELDS = ['Total Approvals', 'Total Denials', 'Approval_Rate', 'latest_funding_date', 'median_salary_offered']

# reuse the maintained SEC normalizer (guarded by __main__, safe to import)
spec = importlib.util.spec_from_file_location('entity_resolution', 'scripts/sec/entity-resolution.py')
er = importlib.util.module_from_spec(spec); spec.loader.exec_module(er)
norm = er.normalize_company_name

def kw_regex(kws):
    # case-insensitive; keyword must not be glued to other letters (so "ml engineer" != "html engineer")
    return re.compile('|'.join(rf'(?<![a-z]){re.escape(k)}(?![a-z])' for k in kws), re.I)

def num(v):
    try: return float(v)
    except (TypeError, ValueError): return None

def parse_date(v):
    try: return date.fromisoformat(v.strip())
    except (AttributeError, ValueError): return None

rows = list(csv.DictReader(open(CSV, newline='', encoding='utf-8')))
sec = {}
for f in sorted(glob.glob(SEC)):
    for c in json.load(open(f))['companies']:
        n = c['company']['company_name_normalized']
        if n: sec.setdefault(n, []).append((c['company']['name'], c['filing']['quarter']))
bls = list(csv.DictReader(open(BLS, newline='')))

print(f'source rows={len(rows)}  rows with any sponsored title={sum(1 for r in rows if r["top_job_titles_sponsored"].strip())}')
print(f'SEC sample normalized names={len(sec)}  24-month cutoff={CUTOFF} (today={TODAY})\n')

for name, (kws, soc) in CANDIDATES.items():
    rx = kw_regex(kws)
    m = [r for r in rows if rx.search(r['top_job_titles_sponsored'])]
    print('=' * 78); print(name); print(f'  keywords={kws}  SOC={soc}')
    print(f'  1. matched rows: {len(m)}')
    appr = [num(r['Total Approvals']) for r in m]
    pos = sorted(a for a in appr if a is not None and a > 0)
    dist = f'min={pos[0]:g} median={statistics.median(pos):g} max={pos[-1]:g}' if pos else 'n/a'
    print(f'  2. Total Approvals > 0: {len(pos)}  ({dist})')
    fd = [parse_date(r['latest_funding_date']) for r in m if r['latest_funding_date'].strip()]
    bad_fd = sum(1 for d in fd if d is None)
    recent = sum(1 for d in fd if d and CUTOFF <= d <= TODAY)
    future = sum(1 for d in fd if d and d > TODAY)
    print(f'  3. non-blank latest_funding_date: {len(fd)} (unparseable {bad_fd}, future {future}); within last 24 months: {recent}')
    hits = [(r['company_name'], norm(r['company_name'])) for r in m]
    hits = [(cn, n, sec[n]) for cn, n in hits if n and n in sec]
    print(f'  4. exact normalized-name matches to Form D sample: {len(hits)}')
    for cn, n, s in hits: print(f'       {cn!r} -> {n!r} -> {s}')
    print('  5. blank or non-numeric scorer fields among matched rows:')
    anybad = 0
    for r in m:
        if any((num(r[f]) is None) if f != 'latest_funding_date' else (parse_date(r[f]) is None) for f in SCORER_FIELDS): anybad += 1
    for f in SCORER_FIELDS:
        bad = sum(1 for r in m if ((num(r[f]) is None) if f != 'latest_funding_date' else (parse_date(r[f]) is None)))
        print(f'       {f}: {bad}')
    print(f'       rows with at least one: {anybad}')
    print(f'  6. BLS rows for {soc}:')
    for b in bls:
        if b['bls_soc_code'] == soc:
            print(f'       {b["onet_soc_code"]} {b["title"]}: annual_median_wage={b["annual_median_wage"] or "blank"} (oews_year {b["oews_year"] or "blank"})')
    titles = sorted({t for r in m for t in re.findall(r"'([^']*)'", r['top_job_titles_sponsored']) if rx.search(t)})
    print(f'  matched title strings ({len(titles)} distinct, check for false positives): {titles[:40]}{" …" if len(titles) > 40 else ""}')
    print()

# ── Seniority split for the chosen candidate (C). Decision by the user (your-input). ──
SENIOR_KWS = ['senior', 'sr', 'staff', 'principal', 'lead', 'manager', 'director', 'head', 'vp', 'iii', 'iv', 'founding']
# Known edge case (user decision 2026-10-02): 'Associate Manager – Data Engineering' stays senior via 'manager'.
senior_rx = kw_regex(SENIOR_KWS)  # same not-glued-to-letters rule: "sr" matches "Sr." not "isr"; "lead" not "leadership"
kws, soc = CANDIDATES['C  Data + AI Engineer (union)']
rx = kw_regex(kws)
m = [r for r in rows if rx.search(r['top_job_titles_sponsored'])]
print('=' * 78); print('SENIORITY SPLIT — candidate C'); print(f'  senior keywords={SENIOR_KWS}')
print(f'  matched rows={len(m)}  distinct company_name={len({r["company_name"] for r in m})}')
groups = {'entry-eligible': [], 'senior-only': []}
title_class = {}
for r in m:
    matched_titles = [t for t in re.findall(r"'([^']*)'", r['top_job_titles_sponsored']) if rx.search(t)]
    flags = [bool(senior_rx.search(t)) for t in matched_titles]
    for t, s in zip(matched_titles, flags): title_class[t.strip()] = 'senior' if s else 'non-senior'
    if not matched_titles:
        print(f'  ! no matched title extracted for {r["company_name"]!r} — check field format'); continue
    groups['senior-only' if all(flags) else 'entry-eligible'].append(r)
for g, rs in groups.items():
    pos = sorted(a for a in (num(r['Total Approvals']) for r in rs) if a is not None and a > 0)
    dist = f'min={pos[0]:g} median={statistics.median(pos):g} max={pos[-1]:g}' if pos else 'n/a'
    fd = [parse_date(r['latest_funding_date']) for r in rs]
    recent = sum(1 for d in fd if d and CUTOFF <= d <= TODAY)
    blank_fd = sum(1 for r in rs if not r['latest_funding_date'].strip())
    print(f'  {g}: {len(rs)} rows | Total Approvals > 0: {len(pos)} ({dist}) | funding date in last 24 months: {recent} (blank funding date: {blank_fd})')
print('  title classification (audit):')
for t in sorted(title_class): print(f'    {title_class[t]:<10} {t}')
