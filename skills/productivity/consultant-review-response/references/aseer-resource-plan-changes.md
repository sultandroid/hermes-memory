# Aseer Museum Resource Mgmt Plan Rev C00 — CG Review Changes

## Context
Project Resource Management Plan for Aseer Museum. Initial version had a highlighted "Outsourced / Remote-Managed Specialists" box and "Remote" pill badges for ~7 roles. BIM Manager described as "remote-managed · F2F on request".

## Changes made

### 1. Deleted the "Outsourced / Remote-Managed Specialists" box
Entire standalone table (6 rows: BIM Manager, 4 BIM Coords, MEP Specialists, Sustainability, NRS, Lighting) removed. These staff still appear in their respective tiers — they're not hidden, just not grouped under a loaded heading.

### 2. Reframed BIM Manager subtitle
- **Before:** `FT · remote-managed · F2F on request`
- **After:** `Dubai-based · monthly site presence · full-time digital presence`

### 3. Added BIM Deputy / Arch. BIM Lead
Added a dashed-separator line under BIM Manager:
```
——————————————————
Arch. BIM Lead (on-site): Eng. Ali Abdelrahman Mostafa · Samaya Technical Office · Riyadh + site
```
This gives CG confidence there's local coverage.

### 4. Changed Tier 2 pill badges
All 7 `pill-slate` "Remote" badges changed to "Specialist". Legend updated:
- **Before:** `FT full-time · Remote remote-based · F2F on request · Stage stage-specific`
- **After:** `FT full-time · Specialist specialist staff (augmented team) · F2F on request · Stage stage-specific`

### 5. Location Matrix entries softened
| Role | Before | After |
|------|--------|-------|
| BIM Coords & Leads | `Overseas-based · remote · F2F at G2/G3/G4 gates` | `International specialists · F2F presence at G2/G3/G4 design review gates` |
| Sustainability Specialist | `Outsourced · remote review · F2F on request` | `Independent specialist · periodic review · F2F on request` |
| BIM Manager | — | Changed Site column from ○ to ● and back to ○ per user correction |

### 6. Risk register R4 softened
- **Before:** `Overseas BIM team continuity (remote-only engagement)`
- **After:** `International BIM team continuity`
- **Impact before:** `Delays if travel restrictions or connectivity issues occur`
- **Impact after:** `Delays if specialist availability affected by travel or connectivity constraints`

### Key lesson: User corrected twice
1. BIM Manager should be ○ (visits) not ● (primary) at Site — Dubai-based role.
2. Ali is formally onboarded as Architectural BIM key person, not a generic deputy.
→ Always verify role accuracy against actual assignments, not inferred.

---

## Session 2 — 18-Jun: Tier 2 & Location Matrix update with KPR data

### What triggered the update
CG review feedback on previous changes was accepted, but user noted the Tiers and Location Matrix still didn't reflect current KPR data: MEP Design was now AD Engineering Co. (Code B approved 15-Jun), and ZNA Studio was the approved Lighting Designer (Code B approved 11-Jun).

### Changes made

#### Tier 2 table — Discipline Leads & Coordinators
| Before | After |
|--------|-------|
| Mechanical Eng. — Moustafa (Dubai) · HVAC + plumbing | **MEP Design (AD Engineering Co.)** — Moustafa + Omar combined, Code B approved 15-Jun · HVAC + power/lighting design |
| Electrical Eng. — Omar (Dubai) · Power + lighting | *(merged into row above)* |
| *(missing)* | **Lighting Design** — Julie Riley (ZNA Studio) · Exhibition lighting design · Code B approved 11-Jun |
| Electrical Eng. (HO) — Hakami · Lighting design coordination / ZNA Studio interface | Updated: ZNA Studio interface (ZNA now formally onboarded) |

#### Location Matrix — new rows + status updates
| Before | After |
|--------|-------|
| *(missing)* | **MEP Design (AD Engineering Co.)** — Dubai-based · specialist |
| Lighting Design: London-based · scope under negotiation | ZNA Studio: Julie Riley · Code B approved 11-Jun · F2F for mock-up + scene setting |
| Sustainability: independent specialist · periodic review | Dr. Ehab Foda · Code C (revise & resubmit 11-Jun) |
| BIM Manager Site column: ● | Corrected back to ○ (visits) per user direction |

### Session workflow pattern
1. Received CG review + user direction to check new data sources
2. Delegate sub-agent: read Stakeholder Plan Rev 03 (org structure)
3. Delegate sub-agent: read Key Personnel Register Excel (vendor/individual details)
4. Discovered: AD Engineering approved in KPR but Stakeholder Plan still TBC
5. Update plan: Tier 2 table → Location Matrix → description/notes
6. Update Odoo task: reopen, document changes, log time
7. User corrected: BIM Manager column back to ○ (pitfall: don't overstate presence)

---

## Session 3 — 18-Jun: Revision C03 → C00 correction + document status cleanup

### What triggered the correction
The document was marked "REVISION C03" but the user caught it: this was the first time submitting to CG, so it should be C00, not C03. Additionally, the document said "Issued for CG Review" without email evidence — user enforced: **don't mark issued until you have proof**.

### User corrections (applied to document)
1. **Revision numbering**: First formal submission is C00. The user asked: "is this normal to make the revision C03 and this is the 1st time we submit?" — clear signal that C00 is expected.
2. **"Issued" status**: "we didnt issue please dont mark it as issue untile you found the email evidance for that" — strict rule: no "Issued" label without submission proof.
3. **Document code**: "remove any doc code or no dc will fill that" — DC fills doc codes. Use "[DC TO FILL]" placeholder.
4. **Filename must match revision**: The HTML filename contained `RevC03` even after the in-document text was fixed. User explicitly asked to "fix the name depend on its version" at the start of the session.

### All changes applied

| Location | Before | After |
|----------|--------|-------|
| Cover — project ref | `MOC-ASEER-SIC-1K0-PL-0024` | `[DC TO FILL]` |
| Cover — status line | `Issued for CG Review` | `For CG Review` |
| Cover — subtitle | `Updated with PMBOK...` | `PMBOK-compliant...` |
| Cover — bottom tag | `REV C00 · ISSUED FOR CG REVIEW` | `REV C00 · CG REVIEW` |
| Rev history header | `[ISSUED FOR CG REVIEW]` | `[DRAFT — FOR CG REVIEW]` |
| Rev history row desc | `First issue for CG Review` | `Draft: PMBOK-conforming...` |
| Rev history row status | `ISSUED FOR CG REVIEW` (green) | `Draft` |
| HTML title tag | `Rev C03` | `Rev C00` |
| Filename | `...RevC03_CG_REVIEW.html` | `...RevC00_CG_REVIEW.html` |
| All 13 page footers | `Rev C03 · CG REVIEW` | `Rev C00 · CG REVIEW` |
| Risk register header | `Expanded for C03` | `Expanded for C00` |
| §10.3 Compliance text | `This Plan Rev C03` | `This Plan Rev C00` |

### Renamed file
```bash
mv "aser_museum_resource_mgmt_plan_RevC03_CG_REVIEW.html" \
   "aser_museum_resource_mgmt_plan_RevC00_CG_REVIEW.html"
```

### Odoo task update
- Task PL-0021 (ID 3022): reopened from `1_done` → `01_in_progress`
- Description: replaced all C03 → C00 references
- Logged 0.5 hr for revision correction

### Key pitfall documented
When the user says "fix the name depend on its version", they mean the filename must match the document's internal revision letter. Don't just change text — update filename too.

---

## Session 4 — 19-Jun: KPR alignment + table widths + jargon removal

### KPR alignment corrections
User checked the plan against the live KPR (Rev C05, 2026-06-19) and corrected several issues:

1. **"Pending submission" ≠ vacant** — People listed as "Pending submission" in KPR (Eng. Mohamed Samir, Dr. Waleed, Eng. Mohamed Ahmed) ARE on board. Show their names with "On board" — do NOT blank them or write "pending MoC submission".
2. **"Code C" handling** — Dr. Ehab Foda (Sustainability) has Code C status. Keep the name, show "submission in progress" — NOT "Code C (revise & resubmit)".
3. **No "Overseas"** — Remove "Overseas" from all BIM coord/lead rows. Names only, no location qualifier.
4. **No non-project-site locations** — Remove Dubai, London, Egypt from all tables and location matrix. Only Riyadh and Abha are valid location references.
5. **BIM Manager = Dr. Waleed Salah** — Not Ali Abdelrahman Mostafa. Ali is a BIM Modeler in the Riyadh HO team, not a sub-line under BIM Manager.
6. **Riyadh HO BIM Modelers list** — Must include ALL team members: Eng. Ali A. Mostafa · Mohamed Mostafa · Toka Hesham · Mohamed Matrawy · Alaa Hissi.

### Table width fix (CSS)
Added `table-layout:fixed` to global `table` CSS rule + `word-wrap:break-word; overflow-wrap:break-word` to `td` and `th`. This forces browsers to respect `th style="width:X%"` percentages. Without it, auto-sizing by content causes A4 overflow. Also converted all pixel widths (60px, 70px, 30px, 22px) to percentages for consistent A4 rendering.

### Jargon removal
- Removed all "PMBOK" / "PMBOK-compliant" / "aligned to PMBOK practices" references
- Removed "WBS", "RBS" abbreviations from headers and body text
- Removed internal tool references: "QS_Template.xlsx" → "QS Template", "Primavera P6" removed
- Removed internal change notes: "added Interactive Design, Lighting, ICT Security", "aligned to SMP Rev 03"
- Removed "aligned to Master Programme Rev.03" from phase strip title

### Date correction
Revision history date changed from 2026-06-16 to 2026-06-19 (tomorrow's date for submission).
