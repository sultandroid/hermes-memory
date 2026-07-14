# CG Submission Letter Pattern — Multi-Input Response Package

## When to use

When CG sends comments/requests from multiple sources (Architecture review, Structural review, Scenography request, etc.) and you need one formal submission letter consolidating the response package.

## Typical inputs

| Source | Format | Example |
|--------|--------|---------|
| CG Architecture comment sheet | Excel/PDF | CG Comment Sheet — Architecture DD (27 Jun 2026) |
| CG Structural comment sheet | Excel/PDF | CG Comment Sheet — Structural (27 Jun 2026) |
| CG email request | Email | Maged Zamzam — Scenography Drawings (16 Jun 2026) |
| CG reminder | Email | "Kind Reminder" follow-up |

## Document structure

| Section | Content |
|---------|---------|
| 1.0 Subject | List all 3 CG inputs with dates |
| 2.0 Introduction | Context — this package addresses all comments |
| 3.1 CR Sheet | Status summary table (Closed / In Progress / Open / Noted) |
| 3.2 NRS Draft Drawings | Table of draft PDFs mapped to their CRs |
| 3.3 Updated Registers | Table of revised submission plans and registers |
| 4.0 Scenography Status | 10-item table from Maged's request with status per item |
| 5.0 Request | CG to review and approve; open items to follow |
| 6.0 Attachments | List of all files in the package |
| 7.0 Sign-off | Prepared by / Reviewed by / Approved by |

## CR status summary table

4-column table: Status | Count | Remarks

Standard statuses: Closed (addressed), In Progress (partial), Open (needs specialist), Noted (acknowledged)

## Scenography 10-item table

From Maged Zamzam's request (16 Jun 2026):

| # | Drawing Type | Status | Remarks |
|---|-------------|--------|---------|
| 1 | Scenography Master Plan | Covered | CR-01 / Draft 1820 |
| 2 | Showcase Layout Plan | Covered | CR-08 / On GA drawings |
| 3 | Showcase Detail Drawings | Covered | CR-09 / In Arch packages |
| 4 | Scenography Lighting Plan | Open | CR-10 / ZNA scope |
| 5 | Signage & Graphics Plan | Covered | CR-05 / Draft 1260 |
| 6 | Multimedia & Interactive Plan | Open | CR-11 / AV specialist |
| 7 | Circulation & Flow Plan | Covered | CR-01 / Master Plan |
| 8 | Finishes & Materials Plan | In Progress | CR-12 / 90%+IFC |
| 9 | Maintenance Access Plan | Covered | CR-06 / Draft 1270 |
| 10 | Environmental / Microclimate | Open | CR-13 / MEP scope |

## Doc ref pattern

`MOC-MUS-ASE-1K0-COR-001` — COR series for correspondence. Increment per submission.

## File placement

```
04_Correspondence/
  MOC-MUS-ASE-1K0-COR-001_CG_Comments_Response_Submission_Letter.docx
```

## Pitfalls

- Do NOT repeat CG comments in the letter body — reference the CR sheet only
- Keep the cover brief — CG reviewers don't need verbose change logs
- Use `add_body()` for all text (no `add_remark()` — that method doesn't exist on SamayaDoc)
- Sign-off: Prepared by (Tech Office Mgr), Reviewed by (PD), Approved by (PM)
- Always check the CR sheet first to know which items are Closed vs Open before writing
