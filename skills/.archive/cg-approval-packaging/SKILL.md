---
name: cg-approval-packaging
title: CG Approval Packaging
description: Review and reframe project plans/documents to maximize CG (Consultant/Govt) approval likelihood. Identify loaded language that triggers scrutiny and replace it with approval-friendly framing while maintaining factual accuracy.
---

# CG Approval Packaging

## When to use

The user asks you to make a plan, procedure, or project document **CG-ready** or **approval-friendly** — not just technically correct but framed to pass external review with minimal pushback.

## Core technique

1. **Audit for loaded labels** — search for "remote", "outsourced", "offshore", "F2F on request" as standalone weakness signals. Replace with positively-framed equivalents like "specialist", "augmented", "dedicated support".
2. **Reframe location → coverage** — instead of "remote-managed · F2F on request" use "monthly site presence · full-time digital presence". **Do NOT mention non-project-site cities** (Dubai, London, Egypt, "Overseas"). Only Riyadh and Abha are location references in plan documents. The location matrix columns (HO Riyadh / Site Abha / Remote) are sufficient — don't add city names inline next to names or firms.
3. **Position local deputies** — every off-site senior role should show on-site backup. Use CV evidence to prove the deputy's qualifications.
4. **Change pill/label taxonomy** — "Remote" → "Specialist", "Overseas-based" → "International specialist". Update legends consistently.
5. **Soften risk register entries** — rephrase risks that name the staffing model as the vulnerability (e.g. "Overseas BIM team continuity (remote-only engagement)" → "International BIM team continuity").
6. **Remove standalone "outsourced" boxes** — don't group all remote staff in a highlighted section. Distribute them naturally into tiers.
7. **Emphasize F2F presence frequency** — "on request" → "monthly site presence" or "at design review gates". Be specific about schedule, not conditional.

## Cross-reference multiple data sources

**The Key Personnel Register (KPR) may contain approved vendors not yet reflected in other plans.** Example from session: AD Engineering Co. appeared in the KPR as "Code B approved 15-Jun" while the Stakeholder Plan Rev 03 still listed MEP Design Agency as "TBC". Always check BOTH:

- **Stakeholder Plan** — shows the org hierarchy, roles, power/interest matrix
- **Key Personnel Register** — shows actual approved companies, individuals, CV statuses, approval dates

Cross-reference them. The KPR wins on factual accuracy; the Stakeholder Plan may be stale on specific vendor names.

### KPR Name Verification Workflow — Org Charts, Resource Plans, Team Sections

Before submitting ANY document that names personnel (org chart, resource plan, stakeholder plan, responsibility matrix, team structure section), every name must be verified against the KPR Excel file. This is a mandatory gate, not optional.

**Step 1 — Load the KPR**
Parse the KPR Excel file (typically `KPR_Register.xlsx` or similar in the project's registers folder) with openpyxl. Extract all rows — columns typically: Role, Company/Entity, Individual Name, CV Status, Approval Status, Approval Date.

**Step 2 — Cross-reference every named person**
For each individual or entity appearing in the document, check the KPR:

| KPR Status | Action |
|-----------|--------|
| `Approved` / `Code A` / `Code B` / `Approved with Comments` | Keep the name. Use the KPR's entity/individual name, NOT the document's version if they differ. |
| `Pending` / `Under Review` / `Submitted` | **Keep the name** — the person IS on board and working, their CV just hasn't been formally submitted to MoC yet. Show name with "On board" or no status label at all. Do NOT blank the name. Do NOT write "pending MoC submission". |
| `Code C` / `Revise and Resubmit` | **Keep the name** — show "submission in progress". Do NOT blank the name. Do NOT write "Code C (revise & resubmit)" in the plan — that's KPR-level detail. |
| `Vacant` / `TBC` / not in KPR at all | Show `—` or "Vacant" / "TBC". Do not guess or carry forward from previous revisions. |
| Entity name mismatch | Use the KPR's entity name. E.g., document says "Nama Al Amal" → KPR says "Nama Consulting" → use "Nama Consulting". Document says "Glassbühne" → KPR says "Glasbau Hahn" → use "Glasbau Hahn". |

**Step 3 — Handle document metadata separately**
Document metadata fields (Prepared By, Issued By, Checked By — found in revision history blocks) are **operational facts** about who drafted the document, not personnel claims. These are NOT KPR-verified. Leave them as-is even if those individuals aren't in the KPR. Only the org chart / role-assignment sections need KPR clearance.

**Step 4 — Document the KPR source**
Add a footnote in the document e.g.: "Personnel names verified against KPR Rev XX dated YYYY-MM-DD."

**Step 5 — Warn about stale org charts**
If the KPR shows approved entities that the plan doesn't list at all (e.g., AD Engineering Co. approved for MEP Design but the plan still says "TBC"), flag this to the user — the plan may need new rows added.

## Remove internal jargon and methodology references

Client-facing plan documents must not contain:

| Remove | Reason |
|--------|--------|
| `PMBOK` / `PMBOK practices` / `PMBOK-compliant` | Client doesn't care about the methodology framework — only the results |
| `WBS` / `RBS` abbreviations | Internal project management jargon — use full terms or remove |
| `QS_Template.xlsx` / `Primavera P6` / internal tool names | Internal tool references are irrelevant to the consultant/client |
| Internal change notes (e.g., "added Interactive Design, Lighting, ICT Security") | Version-control detail, not client-facing info |
- `aligned to SMP Rev 03` / `aligned to Master Programme Rev.03` | Internal cross-reference — the Master Programme is already cited in the references section |
| `[DRAFT — FOR CG REVIEW]` status badge | CG sees "Draft" as not ready for review — change to `[ISSUED FOR CG REVIEW]` |
| `Updated per PD recommendations` (cover or revision history) | Rewrite as `Updated: [what changed]` — CG doesn't need to know internal review triggered the update |
| KPR Action Note (amber callout box listing PD/HR tasks) | Remove entirely — PD/HR housekeeping is not client-facing content |

**Rule**: If a phrase or note is not useful to the consultant (CG) or client (MoC), remove it. The plan is a deliverable, not an internal working document.

## Additional content rules (learned from CG-review sessions)

### Personnel labels
- **"on-site" → "appointed"**: When a person is assigned to the project but not physically at site, use "appointed" — not "on-site". The user will flag "on-site" as misleading.
- **Don't omit team members from location-group lists**: If listing BIM Modelers at Riyadh HO, include everyone assigned there (e.g. Ali A. Mostafa, Mohamed Mostafa, Toka Hesham, Mohamed Matrawy, Alaa Hissi) — even if someone also appears elsewhere in the document. Omitting them is an incomplete-data failure.

### Equipment and materials — detail from project data
- **Equipment specifics come from project memory, not generic placeholders.** Example: "Laser scanner" → "FARO Focus Premium 200 laser scanner". Always check what the project actually uses.
- **Materials lists must be detailed from project schedule JSONs**, not generic. Pull actual material descriptions, suppliers, and specs from:
  - `finishes_schedule.json` — floor/wall finishes, suppliers (Ceramiche Piemme, Concept Tiles, Clay-works, Corian, Kvadrat, GF Smith, etc.)
  - `showcase_schedule.json` — glass thickness, AR coating, climate control specs, case ratings
  - `av_equipment_schedule.json` — manufacturers (Yamaha, iGuzzini), product models, quantities
  - `lighting_schedule.json` — fixture types, manufacturers, wattage, CRI, CCT, dimming
- Generic "Concrete, rebar, blockwork, steel, finishes" is insufficient. Name actual products, suppliers, and specifications from the schedules.

### Revision history dates
- **Set the revision date to the intended submission date**, not the draft date. If submitting tomorrow, use tomorrow's date.

### Exhibition Matrix — Status display per role type

In the CG Approval Status column of the Exhibition Team Matrix (§7.3):

| Situation | Display | Example |
|-----------|---------|---------|
| Firm assigned, pending CG approval | `Firm — pending approval` | `Rawasen — pending approval` |
| Firm assigned, CG approved | `Approved` (no firm name repeated) | `Approved` |
| Firm assigned, Code B | `Code B approved [date]` | `Code B approved 11-Jun` |
| No firm assigned (TBC) | `TBC` — no qualifying commentary | `TBC` |
| No role assigned | `—` | `—` |

**Do NOT** append internal status notes to TBC entries: `TBC — pending submission`, `TBC — Code C`, `TBC — prequal in progress` are all inappropriate for a CG document. Only qualified firms get status qualifiers; unassigned roles just show `TBC`.

## HTML table layout fix for A4 documents

When tables overflow or columns don't respect width percentages:

```css
table { width:100%; border-collapse:collapse; table-layout:fixed; }
td { word-wrap:break-word; overflow-wrap:break-word; }
th { word-wrap:break-word; overflow-wrap:break-word; }
```

- `table-layout:fixed` forces the browser to respect `th` width percentages instead of auto-sizing by content.
- `word-wrap:break-word` ensures long text wraps within fixed columns instead of overflowing.
- Convert all pixel widths (`60px`, `70px`, `22px`) to percentages for consistent A4 rendering.
- Ensure every column has an explicit width — with `table-layout:fixed`, unwidthed columns split equally which may not be ideal.
- This is a global CSS fix — one change fixes all tables in the document.

## Pitfalls

- **Do NOT overstate on-site presence (○ vs ●).** The location matrix distinction between "primary base" (●) and "visits" (○) matters. Reframe the description, not the column. Changing ○ → ● without hard evidence (role is site-based) triggers CG scrutiny. The user will catch this.
- **Confirm deputy is actually onboarded.** When adding a local deputy, verify in the KPR whether they are formally assigned to the project. Don't assume "CV exists = not onboarded" or vice versa — read the KPR status column.
- **Changes ripple through multiple locations.** A single change (e.g. adding AD Engineering) affects: org chart box → Tier 2 table → Location Matrix row → legend → description/notes text. Check all five.
- **Never mark a document "Issued" without email evidence.** The user will flag this. Use "Draft — For CG Review" or "For CG Review" on the cover, revision history status, and page footers. Change "Issued for CG Review" → "For CG Review" and "ISSUED FOR CG REVIEW" (revision status) → "Draft" or "For Review". Only mark as "Issued" after you have proof of actual submission (email timestamp, transmittal).
- **Don't fill document codes.** The Document Controller (DC) assigns the formal document number. Use "[DC TO FILL]" as a placeholder or leave the field blank. Do not insert provisional document codes — they may conflict with the DC's numbering scheme.
- **First formal submission is always C00.** Internal draft iterations (C01, C02, C03) do not map to formal revision letters. The revision history should show a single C00 row for the first CG submission, not a chain of internal drafts that never left the Tech Office. If the source file says "Rev C03", the user will correct it.
- **Filename must match the revision letter.** When changing a revision (e.g. C03 → C00), update ALL locations: HTML title tag, cover page body text, revision history table, every page footer, and the actual filename on disk. Missing even one is a consistency error.

## End-to-end workflow

1. Load CG comments (email thread, review document)
2. Audit the plan for loaded language, red-flag labels, outsourcing groupings
3. Cross-reference Stakeholder Plan + KPR for current vendor/role data
4. **Check Register Log (.xlsb) for current status of every document referenced in the plan** — use `pyxlsb` library, search ALL sheets for each doc number. Never assume doc status from memory. See `samaya-technical-office` skill's `references/register-log-reading.md` for the full pattern.
5. Apply reframing changes across all document sections
6. Verify: re-scan for remaining "remote", "outsourc", "offshore" instances (body + pills + legends)
7. Update the Odoo task:
   - Change state from `1_done` back to `01_in_progress`
   - Update deadline date
   - Add assignees involved
   - Document all CG changes in the description
   - Log session time via `account.analytic.line`

## Key red flags to search for

| Red flag | Replace with |
|----------|-------------|
| `outsourced / remote-managed` | Remove standalone box; merge into org tiers |
| `remote` (pill badge) | `specialist` or `augmented` |
| `F2F on request` | `monthly site presence` or `F2F at design review gates` |
| `remote-only engagement` (risk register) | `specialist availability constraints` |
| `Overseas-based · remote` | Remove "Overseas" and city names — use role description only |

## Evidence-based staffing

When a deputy or local lead is mentioned, pull their CV if available. Use specific qualifications (years experience, relevant project type, certifications) in the plan to justify the coverage model. For CG, **showing someone is qualified on-site beats arguing someone can work remotely**.

## Verification

After changes, re-scan for remaining "remote", "outsourc", "offshore" instances. Check both the document body and any pill labels/legends.

## Files

- `references/aseer-resource-plan-changes.md` — before/after of the Aseer Museum Resource Mgmt Plan Rev C00 changes
- `references/aseer-resource-plan-c00-kpr-sync.md` — KPR Rev C05 sync session (2026-06-19): name restoration, content cleanup, table layout fix, materials detail expansion
