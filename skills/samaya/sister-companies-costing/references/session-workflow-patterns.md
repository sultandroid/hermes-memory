# Session Workflow Patterns (discovered 2026-07-19/20)

## Shorthand Commands

| Command | Meaning | Action |
|---------|---------|--------|
| `fix` | Exclude all flagged items, use verified-only data, build files immediately | No confirmation needed on individual flagged items |
| `next` | Move to next project in sequence | Immediately examine next project's data, present it |
| `2` (numeric) | Pick option 2 from presented choices | Used when user chose "leave as 0" for Jabal Omar |

## Parallel Dispatch Pattern

When processing projects sequentially:
1. Dispatch subagent to build files for current project
2. In the same turn, start examining the next project's data
3. Present the next project's data while subagent works
4. When subagent reports back, verify files exist, then user says "next"

This keeps the conversation moving without idle waiting.

## Data Presentation Pattern

For each new project, present:
1. **Existing analysis file** — what the FCA already has (labour breakdown, materials, other)
2. **Accounting file** — what the main costing file says for factory cost
3. **Flagged items** (if any) — items needing user decision, with amounts and flags
4. **Proposed 3-row breakdown** — Labour / Materials / Other with totals

Always translate Arabic category names to English before presenting.

## Projects with No Factory Cost Data

When accounting file says "No data" (0 SAR):
- Present the situation: accounting total vs 0 factory cost
- Offer 3 options: (1) classify manually, (2) leave as 0, (3) use full accounting total
- If option 2: create empty files with "No data" rows and 0 totals
- Document the gap in Gap_Analysis
