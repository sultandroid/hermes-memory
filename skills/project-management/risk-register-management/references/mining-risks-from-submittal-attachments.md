# Mining submittal attachments for NEW risks

Some email attachments are not mere submittals — they carry risk-relevant
findings that belong in the live risk register. **Compliance & Understanding
Reports, Assessment Reports, and Audit Reports are prime candidates.**

## Worked example (Aseer, 06-Aug-2026)

`MOC-MUS-ASE-1E0-ZD-0103 Rev.01` (Compliance & Understanding Report,
Engr. BMR/AEC) arrived as an email attachment. The PDF's first page was a
Document Submittal (DS) cover form; the actual report content followed it.
Reading the full body (not just the DS cover) surfaced:

- **8 electrical assessment reports not yet received** (Substation TR, Gen/ATS,
  LV cables, MCC, MDB/SMDB, UPS, Wiring devices, Panelboards)
- **5 systems still Code C** (PAVA, CCTV, Telecom, Lighting, Distribution Boards)
- **FAS non-compliant** with AHU/elevator/escalator/fire-suppression interfaces
- **10-yr-old Master Clock** with no final engineering recommendation

These gaps gate the electrical redesign (DD Gate 1) and as-built revision →
a genuine NEW High risk (`PRR-MEP-03`).

## Steps

1. Extract the attachment; read the FULL body — the report follows the DS cover.
2. Scan for structural gaps: missing deliverables ("N reports not yet
   received"), systems at Code C, non-compliant interfaces, aged equipment
   without final recommendations.
3. Create the new risk in BOTH places (dual-write):
   - `01_Registers/risk_register.md` — new table row + bump revision + Total
     Risks + Summary counts.
   - `06_Risk_System/risks.json` (the SoT) — full JSON entry
     (id/category/title/cause/event/consequence/probability/severity/score/
     rating/status/owner/evidence/response_action/actions/history/diagram/
     action_due).
4. **Verify the Summary counts by regex, do NOT hand-adjust.**
   After editing the md, recompute from the table rows:
   ```python
   import re
   ratings = re.findall(r'^\| \w+-\w+-\d+ \| [A-Z]+ \| .*? \| \d+ \| \d+ \| \d+ \| (\w+) \|', txt, re.M)
   statuses = re.findall(r'^\| \w+-\w+-\d+ \| [A-Z]+ \| .*? \| \d+ \| \d+ \| \d+ \| \w+ \| (\w+) \|', txt, re.M)
   ```
   The stored Summary counts can drift from the actual rows (pre-existing bug);
   fix both the ratings and statuses tables to match reality.
5. Update `01_Registers/assessment_evaluation_register.md` with the submittal's
   rev + status (e.g. `Submitted`, `SIC.-WTRAN-0001NN`).
6. Add chase/follow-up action items to `00_Status/action_items.md` with
   owners + due dates + source ref.
7. Optionally rebuild the webapp (see `register-webapp-operations`):
   `python3 webapp/build_risk.py` + `python3 webapp/build_snapshots.py --bump`.

## Pitfalls

- **"Attached" in the email body ≠ real attachment.** AppleScript may return 0
  attachments because the document was filed via Aconex/SharePoint. Check
  `Message_HasAttachment` and the `Mail_OwnedBlocks`→`Blocks` join. If
  `HasAttachment=0`, log the submittal and move on — do NOT loop-retry
  AppleScript.
- **DS cover page only** — `pdftotext` of the first page shows the submittal
  form; scroll past it to the report body (executive summary, per-system
  sections, conclusions).
- **Multiple attachments may be the same file** — verify with `md5sum` before
  treating two block rows as two documents.
