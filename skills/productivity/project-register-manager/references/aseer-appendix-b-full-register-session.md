# Aseer Museum — Appendix B Full Register Creation Session (June 2026)

**Session scope:** Created SPEC.md + Submittal Registers for all 16 Appendix B subcontractor packages for Aseer Museum.

## Key Corrections & Lessons

### 1. Appendix B is the Authoritative Subcontractor List
- Use `Subcontractors/_assets/APPendix B.pdf` — NOT the README
- Appendix B lists: Model Maker, Lighting, Graphics, AV Hardware, Showcase, Rigging, FF&E, Exhibition Fit-Out (Mgmt), Interactives, M&E, FLS, Structural Engineering, H&S, IT/Data, Surveyor, Accessibility, Architect, Acoustic, M&E Contractor, Interior Design, Landscape
- **Do NOT create folders for packages not in Appendix B** — user said "keep folder only same link appendix B.pdf why you add more"

### 2. Folder Numbering Rules
- Renumber subcontractor folders to match Appendix B sequence (not README order)
- Use temp names during renumbering to avoid OneDrive sync conflicts:
  ```
  mv 03_AV_IT_Contractor zz_temp
  mv 08_Graphics_Contractor 03_Graphics_Contractor
  mv zz_temp 04_AV_IT_Contractor
  ```
- Related packages grouped: technology cluster (02-04), MEP cluster (10-13), fit-out cluster (06-09)
- Non-Appendix-B folders merged into related main packages (e.g., Oddy → Exhibition Fit-Out QA)

### 3. SPEC.md vs Register Location
- **SPEC.md** → `_MANAGER_DASHBOARD/SPEC.md` (management files)
- **Excel Register** → its own subfolder at subcontractor root: `Subcontractors/NN_xxx/Register_Name/Register_Name.xlsx`
- User explicitly corrected: "no i mean the md files not the registers itself"

### 4. 09_Registers Serialization
- `_Master_Register_Index/` and `_Master_Submittal_Register/` have NO serial numbers (`_` prefix sorts first)
- Real registers get `01_` to `NN_` serial prefixes
- No loose `.xlsx` files at root
- `Specialist/` kept as separate group

### 5. Long-Lead Items Drive 50% Package Thickness
- User corrected: "why you waite me to tell you" about Showcases long-lead
- Showcases (14wks) → 8 items at 50% (schedule, materials, environmental control, GA, structural, lighting, power, lock system)
- MEP (12-16wks) → 13 items at 50% (surveys, basis of design, preliminary loads/SLDs)
- Check README and SCOPE_REQUESTs for lead times BEFORE creating register

### 6. Draft Email Cleanup
- Remove ALL `_Email_to_*.md` and `draft_email_*.md` files from project
- Email drafts are conversation output, not project files

### 7. QC Gate Before Delivery
- Self-review 50% package thickness, stage assignments, SOW wording
- Delegate to Kimi for QC review before presenting
- Apply findings before reporting

### 8. Professional Master Register Format
- Cover sheet: doc control block, DMP gate reference table
- Dashboard: auto-filter, colour-coded status, alternating rows, totals
- DMP Reference sheet mapping all register items to DMP sections
- Legend sheet for column descriptions

### 9. Always Generate Design Schedule Programme
- After all registers → generate Design_Schedule_Programme.xlsx from DMP data
- DMP milestones: D0→D35→D65→D82→D88→D90→D300
- Gantt with 10-day columns, critical path flags, dependency matrix
- Mermaid .mmd export for Obsidian/GitHub rendering

## Complete Package List (Post-Renumbering)

| # | Package | Folder | Status |
|---|---------|--------|--------|
| 01 | Model Maker | 01_Replica_Model | RFQ Issued 🟡 |
| 02 | Lighting | 02_Lighting | Appointed ZNA 🟢 |
| 03 | Graphics | 03_Graphics | Pre-qual needed 🔴 |
| 04 | AV/IT | 04_AV_IT | Design coord active 🟡 |
| 05 | Showcases | 05_Showcases | Appointed 🟢 |
| 06 | Rigging | 06_Rigging | Pre-qual pending 🔴 |
| 07 | FF&E | 07_FFE | Pre-qual pending 🔴 |
| 08 | Exhibition Fit-Out | 08_Exhibition_FitOut | Pre-qual active 🟡 |
| 09 | Interactives | 09_Interactive | Nominated 🟡 |
| 10 | MEP | 10_MEP | Rev C02 🟡 |
| 11 | FLS | 11_FLS | MoC Approved 🟢 |
| 12 | Structural+Rigging | 12_Structural | Scope drafted 🔴 |
| 13 | MEP Designer | 13_MEP_Designer | ITC variation 🟡 |
| 14 | CITC/IT-Data | 14_CITC | SI active 🟡 |
| 18 | Acoustic | 18_Acoustic | Strategy issued 🟡 |
| 21 | Landscaping | 21_Landscaping | Not appointed 🔴 |
