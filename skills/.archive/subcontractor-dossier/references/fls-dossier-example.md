# Example: FLS (Fire Life Safety) Subcontractor Dossier

Real-world example from Aseer Regional Museum, executed 03 June 2026.

## Source discovery order

1. **SCOPE_REQUEST.md** — already existed at `13_FLS_Specialist_Contractor/SCOPE_REQUEST.md`
   - Contractor: Nama Consulting (MoC-approved 2026-02-08)
   - Register: MOC-ASEER-SIC-1K0-SC-0012
   - 13 deliverables defined

2. **PROJECT_MEMORY.md** → identified IFC-0004 Life Safety submittal, Fire Pump Room issue

3. **RFI_REGISTER.md** → identified RFI #16 (Fire Hose Locations), #38 (Fire Hose Cabinet), #39 (Escape Door Width)

4. **PROJECT_EMAILS.md** → identified 6 FLS-related emails referencing:
   - IFC-0004 Life Safety Drawings (22/26 Apr)
   - Fire Prevention Plan PL-0036 (19/24 May)
   - Namaa Site Survey IR-0001 (14/17 May)

5. **Email body extracts** in `Scripts/output/email_bodies/` and `Scripts/output/email_bodies/cg_responses/` → found full email chains with CG's exact Code C language including: "cannot be reviewed in isolation without reference to and approval of the Project Design Drawings and Fire & Life Safety Consultant approval"

6. **Docs/02_Plans/02.1_DMP/04_Discipline_Files/05_Fire_Life_Safety.md** → FLS discipline file with 197 lines defining scope, deliverables, RACI, risks

7. **Submittals/Life and Safety/** → Fire alarm packages, LSP floor plans

8. **Docs/03_Submittals/03.2_IFC_Packages/** → IFC-0004 submission + CG comments + NRS Fire Alarm Comments

9. **Docs/07_Reports/07.6_FLS_Studies/** → Fire Pump Room Compliance Study

10. **As-Built Docs/** → FIRE ALARM (RISER).dwg, as built fire system.dwg, FIRE PROTECTION.dwg, EL-FA layouts

11. **Completed Tender Package From NRS/02_Approved_Stamped_Packages/04_Life_Safety_Stamped/** → 25 stamped SLF drawings

12. **Specs & Datasheet/GENERAL SPECIFICATIONS/** → Division 21 Fire Suppression

13. **Design Files/** → Fire Strategy PDFs, Fire Escape Distances, Fire Fighting Layouts

## Key pitfalls discovered

- **Email .md files don't exist**: PROJECT_EMAILS.md lists 182 emails with paths like `Email_Archive/2026-05-20 - RE...FIRE PREVENTION PLAN.md` but NONE of these individual files exist on disk. Only summary files (`hesham_archive_may2026.md`, `CG_comprehensive_document_status_mapping.md`) exist.
- **Real email body text** is in `Scripts/output/email_bodies/` and `Scripts/output/email_bodies/cg_responses/` as `.txt` extracts
- **CG rejection language** often contains hidden process gates — read the full email chain, not just the code
- **IFC-0004 (Life Safety) had CG Code C for 2 reasons**: (1) Project Design Drawings not approved first, (2) FLS Consultant endorsement required before CG review
- **Nama had already done site work** (IR-0001) but no formal SoW contract existed — the sub-agent missed this important detail initially

## Final dossier stats

- 88 files, ~193MB
- 7 subfolders populated (2 remained empty: BOQ, Reference Imagery)
- STATUS_REGISTER.md created with 8 sections
- PROJECT_MEMORY.md updated (subcontractor count + IFC-0004 note)
