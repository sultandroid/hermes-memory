# Appending Submission Plan Sheets to Existing Register

When the user asks for a "submission plan" and then "make Excel file" — check if a register already exists at the target path FIRST.

## Workflow

1. **Locate the file** — user may give a folder path (ending in `/`), not the file path. `ls -la` inside the folder to find `*.xlsx`.
2. **Copy to /tmp** — OneDrive paths may fail with `FileNotFoundError` from openpyxl due to sync stubs. Always `cp` to `/tmp/` first.
3. **Read existing structure** — load with openpyxl, dump sheet names, headers, row count.
4. **Preserve all original sheets** — never delete or modify existing data.
5. **Append new sheets** — add these 6 sheets matching the submission plan template:

| Sheet | Content |
|-------|---------|
| Submission Plan | 10 deliverables (G-D-L-001 through as-built docs) with ref, due stage, acceptance criteria, status |
| Schedule & Milestones | 6 milestones from PO to handover with color-coded risk (Critical=red, High=amber) |
| Dependencies & Risks | 6 dependencies with owners — MoC blocked in red |
| Approval Workflow | 4-stage chain (Graphit → NRS → CG → MoC) with durations |
| Procurement Status | 9 items — prequal, contract, RFIs, risk level |
| Coordination Interfaces | 8 trades with key coordination items |

6. **Copy back to OneDrive** — AppleScript `duplicate src to dest with replacing`.

## Styling (openpyxl)

```python
navy = "1E293B"
light_bg = "F1F5F9"
red = "B01E2F"
amber = "D97706"

hdr_font = Font(name="Calibri", size=10, bold=True, color=white)
hdr_fill = PatternFill(start_color=navy, end_color=navy, fill_type="solid")
body_font = Font(name="Calibri", size=10, color="000000")
alt_fill = PatternFill(start_color=light_bg, end_color=light_bg, fill_type="solid")
red_font = Font(name="Calibri", size=10, bold=True, color=red)
amber_font = Font(name="Calibri", size=10, bold=True, color=amber)
thin_border = Border(
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1"),
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="thin", color="CBD5E1"),
)
```

## Pitfalls

- **Do NOT create a standalone new file** when the user specifies an existing register path. They want the existing register updated with new sheets appended, not replaced.
- **OneDrive sync stubs** — openpyxl's `load_workbook` fails with `FileNotFoundError` on cloud-only files. Always `cp` to `/tmp/` first.
- **AppleScript for OneDrive writes** — direct writes produce zero-byte placeholders. Use `duplicate src to dest with replacing`.
- **Copy back to the folder path** (the directory containing the xlsx), not the file path itself. AppleScript `duplicate` replaces the file by name.
