# PROJECT_MEMORY.md Update — Example from Week 23 (June 2026)

## Source File
`23.md` — 5,025 lines, email archive for June 1-5, 2026.

## Existing Project Memory
`Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md` — 934 lines, last updated 07 Jun 2026.

## Delta Identification

### Lines of Inquiry
1. Scan email subjects for `MOC-MUS-ASE-` doc ref numbers
2. Look for CG response emails (from `@cg.com.sa` — especially `melbaz`, `hmabrouk`, `salfeer`)
3. Look for PMC communications from `mohamed.elmahlawy@ace-mb.com`
4. Look for subcontractor activity (Studio ZNA, SITML, Artec 3D, Heritage Sites)
5. Look for structural/technical developments
6. Cross-reference all findings against existing section 0 entries

### New Items Found (not in existing section 0)

| # | Item | Source Email |
|---|------|-------------|
| 1 | PL-0046 Rev.01 — Code C (2 Jun) | melbaz@cg.com.sa, Outlook ID 34748 |
| 2 | PL-0045 Heat Stress — Code B (1 Jun) | Implied from CG HSE approvals thread |
| 3 | Progress Meeting No.12 — After Eid | mohamed.elmahlawy@ace-mb.com, ID 34710 |
| 4 | MOM No.10 (14 May) + No.11 (19 May) distributed | mohamed.elmahlawy@ace-mb.com, IDs 34712, 34711 |
| 5 | 3D Scanning Evaluation — Leica demo 2 Jun | Ahmed Ali (aali@sitml.com), ID 34755 |
| 6 | 3D Scanning Evaluation — Artec meeting 3 Jun | Fahad Hassan, ID 34737 |
| 7 | Structural Design — Core test (ACES) report for 5-point floors | Abdelmohaymen Farag, ID 34692 |
| 8 | Structural Design — As-Built dwgs from Namaa Office | Same thread |
| 9 | Structural Design — Heritage Sites quotation | Ahmed Jad (a.jad@heritagesites.sa), ID 34692 |
| 10 | Studio ZNA — Dogan Kozan CV, 5-week delivery timeline | Julie Riley, ID 34725 |
| 11 | ICT Security SI (MOC-MUS-CG-ASE-1KN-PQ-013) | Mohammed Hakami, ID 34699 |

### Enhanced Existing Items
- PL-0043 Rev.01 — Added "Originally submitted 25-May (Code C), resubmitted 31-May, approved Code B 2-Jun"
- Studio ZNA — Added "RFP sent 13-Apr-2026", "Scope: Concept Design → IFC Lighting Package", "5-week delivery"

## Patch Strategy

### Section 0 Additions (7 new rows)
Used patch with surrounding context to ensure uniqueness:
```
old_string: Full table row from line 33 to line 34 including the `|---` separator
new_string: Same rows + 7 new entries + `|---`
```

Key: The `|---` separator appears 12+ times in the file. Always include the preceding table row as context.

### Session Update Section
Appended after section 12's "Key Updates" bullet list:
```
## Session Update — 07 Jun 2026 (Week 23 Detailed — CG Codes & Project Updates)
```
Subsections: CG Consultant Responses (table), Progress Meetings (bullets), Lighting Design — Studio ZNA, 3D Scanning Evaluation, Structural Design, ICT Security, Core Test Data.

## CG Code Progression Tracking

| Doc | Initial | Final | Progression |
|-----|---------|-------|-------------|
| PL-0043 Temp Electrical | Code C (25-May) | Code B (2-Jun) | 🟢 Resolved |
| PL-0046 Lifting Ops | Code C (2-Jun) | Code B (later) | 🟢 Resolved |
| PL-0018 Comm Plan | Code C (25-May) | — | 🔴 Open |
| PL-0020 Stakeholder | — (ICT comments) | — | 🟡 In review |
| PL-0045 Heat Stress | Code B (1-Jun) | — | ✅ Approved |
