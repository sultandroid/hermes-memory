# June 10, 2026 Daily TODO — Full Worked Example

This is the complete output and methodology from the June 10, 2026 cron run, ~8:00 AM Riyadh.

## Output

📋 *DAILY TODO — 2026-06-10*
Total: *26 items*

🔴 *HIGH PRIORITY (8)*
1. [Aseer] MOC-MUS-ASE-1K0-ZD-0050 - MEP Design Team — murajaa wa tahliil / Review & coordinate | MEP | 2026-06-03
2. [Aseer] Request for Review and Approval of Aseer Mobilization Plan — murajaa wa ietimad / Review & approve | MOB | 2026-06-03
3. [Aseer] MOC-MUS-ASE-1KH-PL-0049 - HSE TRAINING MATRIX, RECORDS AND TRAINING PLAN — murajaa wa ietimad / Review & approve (HSE) | HSE | 2026-06-03
4. [Aseer] MEP Design Services – Asir Regional Museum Project طلب عرض سعر تصميم متحف عسير — murajaa wa tahliil / Review & coordinate | MEP | 2026-06-03
5. [Aseer] MOC-MUS-ASE-1C0-IR-0002 - Installation of Project Temporary Fence — qarar / Decision required | IR | 2026-06-04
6. [Aseer] MOC-MUS-ASE-1M0-ZD-0051 - MECHANICAL MOBILIZATION LAYOUT PLAN — murajaa wa tahliil / Review & coordinate | MEP | 2026-06-04
7. [Zamzam] CCTV Drawings — murajaa wa tahliil / Review & coordinate | MEP | 2026-06-04
8. [Zamzam] HVAC Design Package — murajaa wa tahliil / Review & coordinate | MEP | 2026-06-04

🟡 *MEDIUM PRIORITY (7)* — showing top 7 of 14
1. [Aseer] MOC-MUS-ASE-1KH-PL-0048 - Mobile Equipment Personnel Interface Management Plan — murajaa / Review | DOC | 2026-06-03
2. [Aseer] MOC-MUS-ASE-1KH-PL-0047 - Reward and Recognition Scheme Plan — murajaa / Review | DOC | 2026-06-03
3. [Aseer] MOC-ASEER-0PS-SH-006 Rev.03 - الجدول الزمني — murajaa wa ietimad / Review schedule | SCH | 2026-06-04
4. [Aseer] MOC-MUS-ASE-1KH-PL-0046 Rev.01 - Lifting Operation Management Plan — murajaa / Review | DOC | 2026-06-04
5. [Aseer] MOC-MUS-ASE-1E0-PQ-0056 Rev-01 - Projector Vendor - Panasonic updated — taqyiim / Evaluate vendor | PQ | 2026-06-04
6. [Zamzam] El-Hramein Architectural Package (3 files) — murajaa / Review | DOC | 2026-06-04
7. [Zamzam] Landscape Design Development (2 files) — murajaa / Review | DOC | 2026-06-04

🔄 Plus 7 medium-priority items (design reviews, material submittals) and 4 low-priority items (reports, vehicle requests).

## Data Sources Used

| Source | Status | Items contributed |
|--------|--------|-----------------|
| Aseer Email_Archive/ *.md | ✅ 16 files, Jun 3-4 | 14 Aseer items (all) |
| Aseer CSV Register | ✅ Readable (46KB) but stale (latest entries May 28, outside 7d window) | 0 |
| Aseer Summary .md files | ✅ Readable but stale (May 28 data) | 0 |
| Zamzam Watchdog state | ✅ 19 files, Jun 4-9 | ~5 Zamzam groups |
| Zamzam CSV Register | ❌ Errno 11 (OneDrive locked) | 0 |

## Key Filenames Parsed (Email_Archive)

Files in 7-day window (Jun 3-Jun 10):

```
2026-06-03 - MEP Design Services – Asir Regional Museum Project طلب عرض سعر تصميم متحف عسير.md
2026-06-03 - MOC-MUS-ASE-1K0-RP-0003 Rev.02 - Structural and Architectural Assessment Report.md
2026-06-03 - MOC-MUS-ASE-1K0-ZD-0050 - MEP Design Team.md
2026-06-03 - MOC-MUS-ASE-1KH-PL-0047 - Reward and Recognition Scheme Plan.md
2026-06-03 - MOC-MUS-ASE-1KH-PL-0048 - Mobile Equipment Personnel Interface Management Plan.md
2026-06-03 - MOC-MUS-ASE-1KH-PL-0049 - HSE TRAINING MATRIX, RECORDS AND TRAINING PLAN.md
2026-06-03 - Request for Review and Approval of Aseer Mobilization Plan.md
2026-06-04 - MOC-ASEER-0PS-SH-006 Rev.03 - الجدول الزمني.md
2026-06-04 - MOC-MUS-ASE-1C0-IR-0002 - Installation of Project Temporary Fence.md
2026-06-04 - MOC-MUS-ASE-1E0-PQ-0056 Rev-01 - Projector Vendor - Panasonic updated.md
2026-06-04 - MOC-MUS-ASE-1E0-PQ-0056 Rev-01 - Projector Vendor - Panasonic.md
2026-06-04 - MOC-MUS-ASE-1KH-PL-0046 Rev.01 - Lifting Operation Management Plan.md
2026-06-04 - MOC-MUS-ASE-1M0-ZD-0051 - MECHANICAL MOBILIZATION LAYOUT PLAN.md
2026-06-04 - Request for Review and Approval of Aseer Mobilization Plan.md
2026-06-04 - إعادة توجيه طلب سيارة.md
2026-06-04 - طلب سيارة لنقل مواد وفنيين.md
```

## Dedup Behaviour

- "MOC-MUS-ASE-1E0-PQ-0056 Rev-01 - Projector Vendor - Panasonic" appeared twice (Jun 4, both "updated" and original) → deduped to 1 item
- "Request for Review and Approval of Aseer Mobilization Plan" appeared twice (Jun 3 and Jun 4) → deduped to 1 item (Jun 3 kept as earliest)
- Dedup key: `project + first 50 chars of task.lower()`

## Zamzam Watchdog Groups

19 files → 8 groups, most notably:

| Group | Files | Category | Priority |
|-------|-------|----------|----------|
| HVAC Design Package | 1 (El-Hramein HVAC dwg.zip) | MEP | HIGH |
| CCTV Drawings | 1 | MEP | HIGH |
| El-Hramein Architectural Package | 3 (FA-101 sheets) | DOC | MEDIUM |
| Landscape Design Development | 2 (P083 comments) | DOC | MEDIUM |
| Architectural Final Design (P083) | 2 | DOC | MEDIUM |
| Material Proposals | 3 (ZAM-SAM WhatsApp images) | MAR | MEDIUM |
| SDR-AR-033 | 1 | SDR | MEDIUM |
| External Wall Tiles | 1 | MAR | MEDIUM |

## Bug Fixed: HVAC vs El-Hramein Matching Order

A file named `El-Hramein Musuem - Final HVAC dwg.zip` was matching `'el-hramein' in nl` before reaching the `'hvac' in nl` check. Fix: reorder the elif chain to check `hvac` and `cctv` BEFORE `el-hramein` and `fa-`.

## Cap Strategy Used

Total: 26 items. Show all 8 HIGH + top 7 MEDIUM = 15 items. Remaining: "Plus 7 medium-priority items (design reviews, material submittals) and 4 low-priority items (reports, vehicle requests)."
