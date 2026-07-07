# Construction Submittal Register Pattern

Session: 2026-06-10 — Aseer Museum subcontractor registers (16 packages, 648 items)

## When to use

Creating Excel submittal registers for construction subcontractor packages from SOW/ER contract documents. Typically a multi-day workflow covering all Appendix B subcontractors.

## Workflow

1. **Write SPEC.md** in `_MANAGER_DASHBOARD/` — defines scope, SOW refs, deliverables by stage, standards, coordination, lead-time flags
2. **Write Python generator script** at `02_Submittals/<Register>.py` — produces .xlsx from hardcoded data
3. **Generate Excel** — saved to 3 locations: `02_Submittals/<Register>/`, `Docs/09_Registers/<Register>/`, `Subcontractors/<NN_Discipline>/<Register>/`
4. **Run QC** — KIMI or delegate_task reviews the script and/or output BEFORE delivery
5. **Fix** — apply QC findings, regenerate
6. **Deploy Master** — regenerate the Master Submittal Register to incorporate all updates, deploy to all _MANAGER_DASHBOARD folders

## File location rules

| File type | Location |
|-----------|----------|
| **SPEC.md** (scope definition) | `Subcontractors/<NN_Discipline>/_MANAGER_DASHBOARD/` |
| **.xlsx register** | Own subfolder: `Subcontractors/<NN_Discipline>/<Register>/<Register>.xlsx` |
| **Generator .py** | `02_Submittals/<Register>.py` |
| **Master copy** | `Docs/09_Registers/<Register>/<Register>.xlsx` |
| **Draft emails** | ❌ NEVER save — the user considers these clutter. Deliver in chat or send directly. |

## Subcontractor numbering rule

Folders MUST be numbered to match **Appendix B order** (the SOW's Appendix B.pdf), NOT the project README. Related packages adjacent (e.g. M&E next to FLS). Do NOT create folders for packages that don't already exist in the project — only work within existing structure.

`09_Registers` folder should also be serialized with `NN_` prefix. Index and Master files get `_` underscore prefix (sort first, no serial number).

## Item data structure

```python
(ref, description, sow_section, er_section, discipline, [50%, 90%, 100%, IFC], sub_package, remarks)
```

Stage mask: `[1,0,0,0]` = due at 50% only, `[1,1,1,0]` = due at all DD stages, `[0,0,0,1]` = construction only.

**Mapping to DMP gates (use in Programme sheet):**
- 50% = G2 gate (D35)
- 90% = G3 gate (D65)  
- 100% = G4 gate (D82 IFC)
- IFC/AFC = G5 gate (D88)

## Category header system

```python
cat_names = {1:'A — CATEGORY NAME', 8:'B — NEXT CATEGORY', ...}
```

Category header prints when ANY item in that range filters into the current package sheet.

**Pitfall:** Header ranges must not overlap. When using `rn + N` as upper bound, verify N doesn't reach the next category's start. Set N carefully per category.

## Stage columns display (proven pattern)

```python
'' if mask[0] else '—',   # mask[0]=1 → blank = due at this stage
'' if mask[1] else '—',   # mask[1]=0 → em-dash = not due
```

## Cross-package scope rule (🔥 NEW — Jun 2026)

When a subcontractor's scope overlaps with another (e.g. rigging is structurally related to structural steel), **add the shared items to BOTH registers**. The structural designer's register must include the rigging items even if rigging has its own Appendix B package folder. Keep both:
- The **separate folder for tracking** (Rigging has its own register)
- The **merged items in the designer's register** (Structural includes rigging items)

This ensures the trade responsible for design coordination has the complete picture.

## Long-lead rule

Check README.md in the subcontractor folder for lead times. When a package is long-lead (e.g. "14 weeks" = showcases), push procurement-related items to 50%: materials selection, lighting specs, lock systems, structural anchoring, environmental control spec. Do NOT wait for the user to flag this — verify proactively against the README.

**50% package minimum:** 5-8 items for a credible gate review. If only 1-3, re-evaluate what design-decisions need to happen early.

## DMP Alignment (NEW — required from Jun 2026)

Every Master Submittal Register must include:

1. **Cover sheet** with document control block (ref, revision, date, prepared by, DMP reference, project name)
2. **DMP Reference sheet** mapping register items to DMP sections
3. **Legend & User Guide** explaining columns, colour codes, and usage
4. **Dashboard** with auto-filter, freeze panes, status colour-coding

**Document control fields:** Document Ref (e.g. SAM-MSR-001), Revision, Date, DMP Reference (MOC-MUS-ASE-1K0-PL-0029 Rev.02), Prepared by.

**DMP gate reference per package:** G1→G5 applicable gates. Doc types: ZD=Design Doc, SH=Schedule, DWG=Drawing.

**Stage date mapping from DMP Rev C04:**
| Gate | Day | Stage |
|------|-----|-------|
| G1 Kick-Off | D0 | LOA |
| G2 50% DD | D35 | Interim design |
| G3 90% DD | D65 | Draft final |
| G4 IFC NOC | D82 | Final approval |
| G5 AFC NOC | D88 | Construction docs |
| Site start | D90 | Construction |
| TOC | D300 | Handover |

## Professional Excel formatting standards

**Required for Master Submittal Register (not strictly necessary for individual package registers, but follow when consolidating):**

- Cover sheet: title block, doc control, DMP gate reference table
- Dashboard: auto-filter on ALL columns, freeze panes below headers, status colour-coding (green/amber/red)
- DMP Reference sheet: section-by-section mapping
- Legend: column descriptions, colour key, user guide
- Alternating row shading for readability
- Consistent column widths and borders throughout
- Tab colours: Navy for reference sheets, Blue for data sheets

## Generator script structure pattern

```python
wb = openpyxl.Workbook()

# 1. Define styles (fonts, fills, borders, alignments)
# 2. Define items list (tuples with stage masks)
# 3. Define package definitions [50%, 90%, 100%, IFC] with filter functions
# 4. Define category names dict {start_ref: 'CATEGORY NAME'}
# 5. Loop through packages → create sheet → write header → write items with category headers
# 6. Save to 3 locations
# 7. Print summary (total items, per-package counts)
```

**Pitfall:** When copying cells between workbooks (e.g. package registers into Master), copy only `.value` — do NOT copy `.font`, `.fill`, `.border`, `.alignment` directly as `StyleProxy` objects crash cross-workbook copy. Strip formatting on import.

## QC checklist for registers (run BEFORE delivery — do NOT wait for user to ask)

- [ ] Stage masks match lead-time logic from README (long-lead = earlier stages)
- [ ] Descriptions use exact SOW/ER wording, not paraphrased
- [ ] 50% package not critically thin (<3 items triggers review; minimum 5-8)
- [ ] Category header ranges don't overlap (check with `next cat key - 1` as upper bound)
- [ ] References only cite SOW § or ER § — no external sources
- [ ] All 3 save locations updated (02_Submittals, 09_Registers, Subcontractor folder)
- [ ] Cross-package scope checked — shared items in BOTH registers where scope overlaps
- [ ] DMP alignment verified (gate mapping, section references)
- [ ] No draft email .md files left in project
- [ ] If any folder was renumbered: update ALL generator script save paths to match

## Common pitfalls

- **Category header overlap** — bound calculation reaches into next category. Always verify with the next cn key.
- **50% too thin** — minimum 5-8 items for a credible gate review. If only 1-3, re-evaluate what needs early approval.
- **Source wording** — use exact SOW language, not paraphrased. User says "list same as SOW Listed".
- **References** — only SOW § and ER §. No external specs, interface matrices, or vendor docs.
- **Path corruption after renumbering** — when subcontractor folders are renumbered, ALL generator scripts' save paths break. Fix ALL of them before regenerating.
- **StyleProxy crash** — don't copy font/fill/border objects cross-workbook. Copy `.value` only.
- **Emails saved as project files** — NEVER save draft emails as .md files. The user will find and delete them.
