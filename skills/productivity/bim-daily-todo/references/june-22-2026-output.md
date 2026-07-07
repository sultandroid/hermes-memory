# June 22, 2026 — Extreme Zero-Data Scenario Worked Example

## Situation

- **Aseer register**: 284 entries, last entry May 28 (25 days stale). 0 entries in last 7 or 14 days.
- **Zamzam register**: CSV locked by OneDrive (`Resource deadlock avoided`, `kMDItemDownloadedDate = null`). All subdirectory files also stale (RFP from Sept-Oct 2025, SCH from Dec 2025).
- **Watchdog**: 2 files modified in last 3 days (Meged.pdf + FF&E Schedule.xlsx from June 18 — both design docs, not actionable).
- **Zamzam Design Files**: 0 files modified in last 7 days.
- **Aseer Design Files `find -newermt`**: 0 results in last 3 days.
- **Email_Archive/*.md filenames**: none within 7-day window.
- **Open/Active items in Aseer CSV**: 82 items, oldest going back to Sep 2025.

## Approach

1. All data sources (CSV, markdown, watchdog, find) produced zero new entries
2. Extracted 82 Open/Active items from Aseer CSV (the only non-locked source)
3. Selected top 15 by priority model:
   - RFP needing decision → 2 items (Artec Space Spider × 1 deduplicated, Bluehaus MEP × 1)
   - HSE/FIRE/EMERGENCY/SECURITY SDR → 4 items
   - Other HIGH (SDR with critical scope) → supplemented
   - MEDIUM → Submittal reviews, SI, SCH, design drops
   - LOW → GEN items only to fill to 15
4. Included caveat header about register staleness + 82 total open count
5. No Zamzam items at all — noted in caveat

## Output

```
📋 *DAILY TODO — 22 June 2026*

📌 Last register update: 28 May 2026 (25 days ago). No new entries in last 7 days. No new files in last 3 days from watchdog.

Total: *15 items*

🔴 *HIGH PRIORITY (6)*
1. [Aseer] RFP — Artec Space Spider quotation (RFQ) | Awaiting decision | May 25
2. [Aseer] IR — MEP Design Services – Bluehaus proposal | Review & decide | May 19
3. [Aseer] SDR — MOC-MUS-ASE-1KH-ZD-0044 HSE Notice Board Report | Active | May 25
4. [Aseer] SDR — MOC-MUS-ASE-1KH-PL-0041 Emergency Preparedness Response Plan | Active | May 24
5. [Aseer] SDR — MOC-MUS-ASE-1KH-PL-0036 Rev.01 FIRE PREVENTION PLAN | Active | May 24
6. [Aseer] SDR — MOC-MUS-ASE-1KH-PL-0040 SITE SECURITY MANAGEMENT PLAN | Active | May 23

🟡 *MEDIUM PRIORITY (6)*
7. [Aseer] SDR — Submittal 11 Showcase Shop Drawings (Wall Case-Type 1 & Freestanding Type 2) | Review | May 25
8. [Aseer] SDR — MOC-MUS-ASE-1E0-ZD-0042 Temporary Power Distribution | Active | May 24
9. [Aseer] SDR — MOC-MUS-ASE-1KH-PL-0043 Temporary Electrical Management Plan | Active | May 25
10. [Aseer] SI — SI-CG-ASEER-007 Rev.02 Site Instruction | Follow up | May 21
11. [Aseer] SCH — GBH Updated Time Schedule | Review | May 13
12. [Aseer] Design — FF&E Schedule / Meged Showcase Types (Modified June 18) | New files

🟢 *LOW PRIORITY (3)*
13. [Aseer] GEN — Lighting, AV & M&E within G11/G13 | Review | May 28
14. [Aseer] GEN — Invoice NRS-SAM-2026-004 Payment Processing | May 28
15. [Aseer] GEN — MOC-MUS-ASE-1K0-PL-0018 Rev.01 Project Communication Plan | Active | May 18

⚠️ *Note: Zamzam CSV locked (OneDrive sync). 82 open/active Aseer items total. Plus 80+ routine reviews not listed.*
```

## Key Decisions

- Used **single-line format** (not 2-line bilingual) since all descriptions were English document codes
- Placed caveat at **top** (not bottom) so reader immediately understands why items are old
- Included the 82-item total so reader knows the register is backlogged
- Omitted the SILENT option — even with zero new data, the user expected a daily status
- Deduplicated the 3+ Artec RFP thread variants into 1 item
