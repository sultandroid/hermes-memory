# Aseer Museum — Document Filing Conventions

## Document Code Parsing

Format: `MOC-MUS-ASE-{originator}-{doc-type}-{number}`

| Segment | Meaning | Examples |
|---------|---------|----------|
| MOC | Ministry of Culture (client) | — |
| MUS | Museum | — |
| ASE | Aseer region | — |
| **Originator** | Who created it | 1KH = Samaya HSE/contractor · 1K0 = Samaya general · 1A0 = NRS (arch) · 1E0 = Electrical · 1M0 = Mechanical · 1C0 = Civil · 1V0 = AV |
| **Doc Type** | Category | PL = Plan · ZD = General design/development document · SC = HSE Submittal · IR = Inspection Request · TQ = Technical Query · RP = Report · SH = Schedule · PQ = Prequalification · MS = Method Statement |
| **Number** | Sequential per type | 0053, 0054 |

Example: `MOC-MUS-ASE-1KH-PL-0054` = Samaya HSE, Plan, #54

## Filing Rules by Document Type

### PL (Plan) documents — HSE-related
- Primary archive: `Docs/02_Plans_and_Procedures/02.5_HSE_Plan/01_Source_Files/`
- Transmitted copy: `Correspondence/`
- CG response copies: `02.5_HSE_Plan/02_CG_Responses/` (use `CG RE <code> - Reply.pdf` naming)
- Register: `CG_Response_Register.md` at `02.5_HSE_Plan/04_Registers/CG_Response_Register.md`

### ZD (Design/Development documents)
- **HSE-related ZD** (1KH originator, HSE discipline): `02.5_HSE_Plan/01_Source_Files/` + `Correspondence/`
- **Design-related ZD** (1K0/1A0 originators): `Docs/03_Submittals/03.1_Design_Submittals/` + `Correspondence/`
- CG Reply naming: `<doc-code> - CG Reply.pdf`

### CG Reply / Response documents
- Name pattern: `<doc-code> - CG Reply.pdf` or `CG RE <doc-code> - Reply.pdf`
- File alongside the original submittal + in `Correspondence/`

## Filing Workflow

1. **Identify** the document from its code (originator + type)
2. **Read** the cover page for: submittal date, rev, description, approval status, CG comments
3. **Check** if already filed (`find` / `grep` for the doc code in project tree)
4. **Copy** to proper folder(s) — always include `Correspondence/`
5. **Update registers**:
   - `PROJECT_MEMORY.md` — add to Latest Status Updates table
   - `CG_Response_Register.md` — add row + update stats + possibly Critical Actions
   - Analysis files in `_Analysis/` — correct if existing analysis is wrong
6. **Note approval status** — CG codes: A=Approved, B=Approved w/ comments, C=Revise & Resubmit, D=Disapproved. Code D and C go into Critical Actions section.

## Key Register Locations

| Register | Path |
|----------|------|
| Project Memory | `/Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md` |
| CG Response Register | `/Aseer-Museum/Docs/02_Plans_and_Procedures/02.5_HSE_Plan/04_Registers/CG_Response_Register.md` |
| Analysis files | `/Aseer-Museum/Docs/03_Submittals/_Analysis/` |
| Transmittal Register (xlsx) | `/Aseer-Museum/Docs/09_Registers/Transmittal_Register/` |

## Common Pitfalls
- The cover sheet may show a checkbox for Code B but the attached CG response pages may say Code D — always read the CG response pages, not just the cover
- ZD-0050 type documents (personnel CV submissions) often have a delayed CG response separate from the submission date
- Same-day CG responses are common (submitted and reviewed on the same day)
