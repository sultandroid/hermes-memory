# June 18, 2026 Worked Example — Stale Registers, Zero 7-Day Entries

## Context

Both registers had **0 entries** in the 7-day window (June 11-18):
- Aseer CSV: newest entry May 25 (24 days stale)
- Zamzam CSV: locked by OneDrive (`Resource deadlock avoided`)
- Zamzam Email_Archive root: newest files June 4-5 (13-14 days old)
- Aseer Email_Archive: no files in last 7 days

This is a **zero-entry window** — the TODO generator had to construct items from older register data + watchdog `find` metadata.

## Data Sources Used

| Source | Status | How Used |
|--------|--------|----------|
| Aseer CSV register | ✅ Readable but stale | Extracted 20+ Active items from May 17-25 |
| Zamzam CSV | ❌ Locked | Skipped |
| Watchdog state | ✅ Readable | Found Aseer Graphic Schedule (Jun 17) — Zamzam recent = 0 |
| `find -newermt` Design Files | ✅ Works on stubs | Found Temp Power, CCTV, TQ PDFs modified Jun 11 |
| Zamzam Email_Archive root | ✅ `ls -lt` works | Found IR/MIR/WIR/DOC files from Jun 4-5 (beyond 7d window) |
| Aseer Email_Archive | ❌ No recent files | Skipped |

## Key Decisions

1. **Included items up to 30 days old** (May 17-25) because no newer data existed. Added note: `⚠️ السجلات لم تُحدّث منذ 25 مايو — تم تضمين البنود النشطة القديمة`
2. **Zamzam items from Jun 4** included despite being outside 7-day window — they were the most recent Zamzam activity
3. **Aseer Design Files find scan** yielded 4 new PDFs (Temp Power, CCTV, TQ, RFI) — added as HIGH priority design review items
4. **Output capped at 15 items** with overflow summarized: HIGH kept all 8, MEDIUM kept 5/9 (+4 summarized), LOW kept 2/7 (+5 summarized)

## Priority Distribution

| Priority | Kept | Summarized | Rationale |
|----------|------|------------|-----------|
| 🔴 HIGH | 8 | 0 | All critical — RFP, HSE, MEP design files |
| 🟡 MED | 5 | 4 | Collapsed BMS + Graphic Schedule + Zamzam DOC/MIR |
| 🟢 LOW | 2 | 5 | Routine reviews — collapsed 5 into one line |

## Output Format

Used text markers instead of emoji (`[HIGH]` etc.) because the first attempt with `🏗️`/`🕋` was blocked by the security scanner (variation selector characters). Output written to `/tmp/todo_report.md` first for verification, then printed to stdout.
