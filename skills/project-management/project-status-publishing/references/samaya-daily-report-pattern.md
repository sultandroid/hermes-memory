# Samaya-Style Daily Progress Report — HTML + Surge Deploy

## When to Use

- User says "daily report" or "daily progress"
- User asks for a formatted project status update to share with the team
- User says "follow the Samaya style guide" for a report

## Pattern

1. **Read source data** — `00_Status/project_status.md`, `00_Status/action_items.md`, `08_Document_Index/00_plan_tracker.md`
2. **Build HTML** — 4-page A4 portrait, Samaya Formal Plan style:
   - **Cover** — navy full-bleed, project info, contract, handover countdown
   - **Page 1: Executive Summary** — KPI cards (submittals, plans, NCRs, milestones, actions), today's highlights table, risk summary
   - **Page 2: Submissions & Milestones** — new submissions to CG, Aconex transmittals, meetings held
   - **Page 3: Open Actions** — actions on the user (with due dates + priority badges), actions on the team
   - **Page 4: Plan Status & Forecast** — plan tracker summary, tomorrow's priorities, key contacts

3. **Deploy to Surge** — use a descriptive domain like `aseer-daily.surge.sh`

## Samaya Style Quick Reference

| Element | Rule |
|---------|------|
| Palette | Navy `#0F172A`, Sky `#0284C7`, Green `#16A34A`, Red `#B91C1C`, Brown `#92400E` |
| Font | Montserrat (headings), Inter (body), Menlo (metadata) |
| Page | A4 portrait, 210×297mm, 12mm/16mm padding |
| Cover | Full-bleed navy, white text, green accent keyline |
| Tables | `.eng-table` — navy header, hairline grid, zebra rows |
| Badges | `.badge-pass` (green), `.badge-critical` (red), `.badge-high` (brown), `.badge-low` (gray) |
| Footer | 3-col grid: doc-ref · section context · PAGE N / TOTAL |
| No emoji | Use text labels like "SUBMITTED", "DONE", "NCR", "ACTION" |

## Deploy Command

```bash
rm -rf /tmp/surge-deploy && mkdir -p /tmp/surge-deploy
cp report.html /tmp/surge-deploy/index.html
cp -r assets/ /tmp/surge-deploy/  # Samaya logo
npx surge /tmp/surge-deploy/ aseer-daily.surge.sh
```

## Pitfalls

- **Logo path** — Samaya logo must be copied from `_Style-Guides/logos archives/samaya-logo-trans.png`
- **File name** — rename to `index.html` before deploy so root URL resolves (not `daily-report-23-jul-2026.html`)
- **Page count** — update `/TOTAL` in every footer when pages change
- **Data freshness** — read `project_status.md` and `action_items.md` fresh each time; don't reuse cached values
- **Cover logo** — use `filter: brightness(0) invert(1)` for white logo on navy background
