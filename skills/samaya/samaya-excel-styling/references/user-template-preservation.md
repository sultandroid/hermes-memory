# User-Provided Risk Snapshot Template

## Inspection

Load the workbook twice when needed: once with formulas preserved and once with `data_only=True` for cached values. Record, per sheet:

- sheet names and dimensions
- header row and data start row
- merged-cell ranges
- freeze panes and autofilter
- charts and image anchors
- formula cells and hyperlinks
- owner, target, response/action, evidence, and action-plan columns

## Safe rebuild pattern

1. Copy the supplied workbook to a stable project template path.
2. Copy the template to a temporary output path before editing.
3. Do not rebuild the visual layout from scratch.
4. Do not blindly call `insert_rows()` on a formatted sheet with merged cells. It can leave merged ranges misaligned and cause `MergedCell` write errors.
5. If the template has a footer merge below the data region, expand the data region deliberately before writing, or rebuild a clean equivalent while copying styles. Verify the footer and merged ranges afterwards.
6. Populate existing columns by position only after inspecting the actual header row. In the DDR template inspected in July 2026, the Risk Register headers were on row 9 and included: ID, CAT, RATING, SCORE, STATUS, OWNER, TARGET, RISK EVENT / TITLE, CAUSE, CONSEQUENCE, RESPONSE / ACTION, EVIDENCE. The Action Plan headers were on row 9.
7. Use the source `response_action` as the Action Plan entry when the source has no structured `actions` array.
8. Preserve source gaps. If owner or target is `—`, blank, or TBC in the source, do not invent a person or date.
9. After saving, reopen the workbook and verify owner/action-plan cells, sheet names, merges, charts, images, and hyperlinks.
10. Test the published download URL with an actual HTTP request. If a newly uploaded file returns 403 while older files return 200, check file mode (644) and directory mode (755) on the server, then retest.

## Required verification

For each generated snapshot:

- `Risk Register` contains the expected number of populated risk rows.
- Owner, Target, Response / Action, and Evidence columns are retained.
- `Action Plan` has one populated row per source risk when structured actions are unavailable, or one row per structured action when available.
- Dashboard has the user's logo/QR/header arrangement and no chart overflow.
- Formula cells remain formulas after save; recalculate with LibreOffice before final delivery when available.
- Live-register link and QR target the correct register URL.
- The download URL returns HTTP 200 and the correct XLSX content type.
