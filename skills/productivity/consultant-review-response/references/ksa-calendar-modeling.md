# KSA Calendar Modeling — Workday Formulas and Holiday Handling

## 1. Workweek

| Day | Status | Notes |
|-----|--------|-------|
| Sunday | Working | |
| Monday | Working | |
| Tuesday | Working | |
| Wednesday | Working | |
| Thursday | Working | |
| Friday | **Weekend** | |
| Saturday | **Weekend** | |

**WORKDAY.INTL code**: 7 (Fri+Sat weekend) in Excel.

## 2. Public Holidays (2025-2026, Hijri estimates)

| Holiday | 2026 Date | Duration |
|---------|-----------|----------|
| Founding Day | 22-Feb | 1 day |
| Ramadan window (est.) | 18-Feb to 19-Mar | ~30 days; production factor 1.4x |
| Eid al-Fitr (est.) | 19-Mar to 23-Mar | 5 days |
| Eid al-Adha (est.) | 26-May to 28-May | 3 days |
| National Day | 23-Sep | 1 day |

**Note**: Hijri dates shift ~11 days earlier each Gregorian year. Confirm against Umm al-Qura calendar.

## 3. Calendar-Day to Working-Day Conversion

All contract durations are specified in calendar days. CPM models compute in working days.

| Calendar Days Specified | Working Days (Sun-Thu) | Use Case |
|------------------------|----------------------|----------|
| 7 cd | 5 wd | CG review (SMP/Comm Plan SLA) |
| 14 cd (ER §2.4.A) | 10 wd | CG conformance review |
| 14 wd (SoW §6.5) | 14 wd | Stage-end gate review (NO conversion — already working days) |
| 30 cd (statutory) | 22 wd | SCD Civil Defense review |
| 5 cd | 4 wd | Expedited closure / consultant internal |

**Formula**: `working_days = ceil(calendar_days × 5/7)` for Sun-Thu calendar.

## 4. Ramadan Factor — Only Apply When Activity Overlaps Ramadan

**Wrong**: Flagging `ram=True` on all activities inflates pre-Ramadan work.

**Right**: Only apply 1.4x factor if activity finish date > Ramadan start date AND activity start date < Ramadan end date.

Simpler approach: skip per-activity Ramadan factors in the DMP-compliant baseline. Add a Ramadan delay buffer row in the EOT tracker instead.

## 5. Model Fingerprint Check

| Metric | Rule of Thumb |
|--------|--------------|
| Calendar:Working-day ratio | Should be ~1.4x (weekends + holidays add ~40% overhead) |
| If ratio < 1.25x | Likely no weekend/holiday logic applied |
| If ratio > 1.6x | Likely workdays inflated or wrong duration conversion |

A 101-calendar-day design phase should have ~72 working days of actual productive time.
