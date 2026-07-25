# Dashboard layout and language QA

## Formula and layout checks

1. Load the saved workbook with `data_only=False` and inspect formula strings on Dashboard. Check KPI, rating, status, category, owner, and matrix cells reference `Risk Register` ranges.
2. Load a second copy with `data_only=True`. If all formula results are empty, the workbook has no cached values. Preserve formulas and add cached values through an XLSX XML post-process, or recalculate with a spreadsheet engine.
3. Clear stale dashboard rows before writing new categories and statuses. Stale labels beside current codes are a common template failure.
4. Split long category data into two side-by-side tables. Use columns Category, Code, Count, and % of total in both tables. Place Top Owners below the taller table and move the footer when necessary.
5. Add one `id="schedule"` to the detailed web table. Make Risk Matrix, Exposure by Category, By Status, and Top Owners headings use a direct smooth-scroll handler to `#schedule`; verify the live HTML contains the click handler, not only the href.
6. Do not expose internal-only source names in public HTML or XLSX evidence fields. Remove references to internal consolidated risk registers or documents not issued to CG; replace with an approved external source or neutral project-review wording only when appropriate.
7. Show Probability, Severity, Score, and Rating in the downloaded Risk Register. Score must remain a formula (`=Probability*Severity`) and Rating must derive from the score bands, not be a static copied value.
6. Inspect drawing XML or a rendered workbook for chart and image extents. The logo and QR belong in the header; charts must stay inside the intended page width.

## Source and language checks

- Scan JSON, HTML, JavaScript, Markdown, and generated workbook text for `§`, `·`, `—`, `–`, arrows, decorative bullets, check marks, and cross marks.
- Replace symbols with plain words or standard punctuation. Keep technical notation only when it carries engineering meaning.
- Use direct engineering wording: identify the condition, consequence, owner, target, and action. Avoid promotional or AI-style terms such as seamless, robust, cutting-edge, leverage, and utilize.
- Do not invent owner names or dates. If the source is incomplete, assign only where the discipline responsibility is defensible and mark the assignment for review.

## Final verification

- Test all register pages for the schedule anchor and jump links.
- Test every workbook href with HTTP 200 and confirm it is a valid XLSX.
- Check the Owner and Target columns in both Risk Register and Action Plan.
- Confirm the source template used for all registers is the latest user-supplied workbook, not an earlier generic template.
