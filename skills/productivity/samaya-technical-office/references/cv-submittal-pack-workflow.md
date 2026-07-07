# CV Submittal Pack Workflow — Key Personnel CV Submission

## When to Use

Creating CV submittal packs for project team members (Sustainability, BIM, MEP, Site) following the Key Personnel Register format. Packs are submitted to CG for review and onward MoC approval per SoW §5.5.

## Template Format

Existing packs live under:
```
Docs/09_Registers/Key_Personnel_Register/CVs/{Team_Name}/
_assets/logos/  ← 4 logos: moc.png, pmc_ace.png, cg.png, samaya.png
```

HTML source files in `_archive/HTML/` serve as templates. The format uses:
- **Font:** Carlito/Calibri from Google Fonts
- **Page:** A4 portrait (210mm × 297mm)
- **Logos:** 4-column strip (MoC Employer · ACE PMC · CG Consultant · Samaya Main Contractor)
- **doc-strip:** Header on every page with team name + page info
- **Meta-grid:** 6 cells (Project/Contract, Submitted to, Issued by, Reference, Doc No, Status)
- **DC block:** Document Control grid + QC Sign-Off grid
- **Summary table:** Personnel listing with Name, Role, Page

## Document Numbering — DC-Managed

All document-control metadata fields belong to the Document Controller (DC).

### What To Remove
- **Meta-grid:** Remove the entire `Doc No.` label + value cell from the grid
- **DC block:** Remove `Document No.`, `Revision`, and `Issue Date` cells entirely (label + value)
- **Doc-strip headers:** Remove `· Rev XX · YYYY-MM-DD` suffix from all page headers

### What NOT To Add
- Never add `[TBD]`, `[TBD by DC]`, `---`, or any placeholder text
- Never add revision, date, or document number strings anywhere
- The DC fills these at submission time; pre-populating creates extra work for them to undo

## Team Naming

- Use **"Samaya {Discipline}"** as the uniform team name across all packs (e.g. `Samaya Sustainability`)
- All packs in the same discipline use the identical team name in title, h1, doc-strip, ToC
- **Do NOT** use sub-team names like "Aseer Sustainability Consultancy" or "SAS Framework"

### Package A / Package B (Options for CG)

When the submittal presents options for CG to choose between:

- **Cover h1:** `Samaya Sustainability — Package A` / `Samaya Sustainability — Package B`
- **Cover subtitle:** Add an option label below the CV Submission Pack header:
  `Option A — Sustainability Consultancy (Design & Construction)`
  `Option B — Sustainability Advisory & Reporting`
- **Title tag:** `Package A · Sustainability Consultancy · Key Personnel CV Submittal Pack`
- **Doc-strip:** `Package A · Sustainability Consultancy · Key Personnel CV Submittal Pack · Page 01 of N`
- **ToC section header:** Always uses the uniform team name: `Samaya Sustainability — Aseer Regional Museum`

### File Naming
```
Package A · Sustainability Consultancy · Key Personnel CV Submittal Pack.html
Package B · Sustainability Advisory & Reporting · Key Personnel CV Submittal Pack.html
```
No document numbers in filenames.

## Mission Brief Content

### Must Match Actual Proposal Scope
- Read the person's actual proposal/scope document before writing — do NOT infer scope from CV content alone
- The CV lists skills they HAVE; the proposal defines what they'll DO on this project
- Check the proposal for exclusions (e.g., advisory role "does not include engineering calculations")

### Per-Person, Not Generic
- Each person gets a mission brief describing THEIR specific deliverables
- **Do NOT** use a generic team-wide mission brief shared across multiple persons
- Design-phase expert: envelope, energy modeling, passive retrofit, water strategy, thermal comfort, materials
- Construction-phase expert: site audits, environmental monitoring, waste diversion, material compliance, IAQ, commissioning support
- Advisory/reporting: sustainability reports, compliance tracking, coordination with project team for inputs

### Existing Building Retrofit (Not New Build)
- Remove references to early-stage design tools (Autodesk Forma Cloud, etc.)
- Frame passive design as "retrofit optimisation" not "orientation advice"
- Avoid "from concept through IFC" — use "from assessment through IFC"
- Reference SoW §13.9 and Employer's Requirements Mostadam / SBC 1001 compliance

### Subcontractor References
- **Do NOT** reference subcontractor names (SG Group, etc.)
- Submit individuals directly under Samaya Sustainability
- The person IS the sustainability team for their scope
- They coordinate with the **project team** (Samaya TO, BIM Unit, NRS), not another consultancy

## LEED vs Mostadam

- **Mostadam** is the project's rating system — reference Mostadam / SBC 1001 in all scope items
- **LEED** references: keep only in personal certifications (the person holds a LEED credential as qualification)
- **Remove LEED from**:
  - Core competencies: `LEED / Mostadam Compliance` → `Mostadam Compliance`
  - Scope/coordination bullets: `LEED documentation` → `sustainability documentation`
  - Technical skills lists: remove standalone LEED, keep only if it's their certification
- Personal certs (education/certification section) can stay — those are the person's credentials

## Mostadam Credit Language

- **Do NOT** use "credit pursuit," "credit scoring," or "Mostadam credits" in scope text
- Credit scoring and pursuit is the **Sustainability Lead's (Dr. Ehab Foda)** role, not these team members'
- These team members support **compliance evidence and documentation**:
  - `Mostadam credit support` → `Mostadam compliance documentation`
  - `Mostadam envelope credits` → `Mostadam compliance evidence`
  - `credit tracking with project teams` → `compliance tracking with project teams`
- The project uses reference forms: F-16 / F-19 / F-34 / F-35 / F-36 for evidence

## SOW Companion Document

When submitting CV packs to CG, create a companion **Scope of Services** document:

- **Location:** `Docs/02_Plans_and_Procedures/02.12_Sustainability_Strategy/04_Consultants/SOW_Sustainability_Team.html`
- **Format:** Same A4 portrait template as CV packs (logo strip, meta-grid, DC block, QC sign-off)
- **Content:**
  - Team structure (referenced as Package A / Package B, not individual names)
  - Scope of services per package (design-phase, construction-phase, advisory/reporting)
  - Deliverables schedule with responsible package and frequency
  - Reporting & governance, scope exclusions
- **No individual names** — CG chooses between packages, not between people
- **No Mostadam credit language** — use compliance evidence terminology
- Keep it concise — the SOW serves as a compact overview/annex to the Sustainability Plan

## Verification Checklist

- [ ] All Doc No / Revision / Issue Date cells **removed** (meta-grid + DC block — labels AND values)
- [ ] No `[TBD]`, `---`, or placeholder text anywhere
- [ ] Rev/date removed from all doc-strip headers
- [ ] Team name consistent across title, h1, doc-strip, ToC
- [ ] Mission brief matches actual proposal scope (read the proposal, not just the CV)
- [ ] No new-build tools listed (Autodesk Forma, etc.) for retrofit projects
- [ ] No subcontractor references in team names or affiliations
- [ ] LEED removed from all scope sections (keep only in personal certs)
- [ ] Mostadam credit → compliance evidence language throughout
- [ ] HTML source only — no PDF generated
- [ ] SOW companion doc created if needed
- [ ] Codex audit passed (run Codex on both HTML files before delivery)
