# Comment Extraction & Mapping Technique

## PDF Extraction
- Use `pdftotext -layout` to extract text preserving table structure
- For large PDFs (>40k chars), read in chunks using offset/limit
- Identify the comment section: typically after "CG Response Date" or "Code C: Revise and Resubmit"
- Comments are often numbered (1, 2, 3...) with inline status markers

## Status Code Mapping
| PDF Marker | Meaning | Action |
|---|---|---|
| "OK" | Acknowledged, no further action | Closed |
| "OK - comply with Ad." | AD has taken action | Closed |
| "OK - confirm form Ad." | Awaiting AD confirmation | In Progress |
| "OK - Update in DL" | Drawing list needs updating | In Progress |
| "OK - Celerefication in RACI" | Clarified in RACI matrix | Closed |
| "Confirmation With Ad." | Awaiting AD confirmation | In Progress |
| "Same comment #N" | Duplicate of earlier comment | Same status as #N |
| "NP" | Noted, no problem | Closed |
| Blank / no status | Action still needed | In Progress |

## Party Assignment (from RACI)
- **AD Engineering Office** → MEP design (HVAC, plumbing, electrical, fire fighting)
- **RAWASIN** → AV systems design, installation, commissioning
- **ZNA** → Lighting design, LUX calculations, lighting control
- **BMS/ICT Specialist** → BMS controls, structured cabling, network
- **Namaa** → Existing systems survey
- **Samaya (Coordinator)** → Overall coordination, drawing list updates, RACI, timeline

## Comment Categorization
1. **Scope clarifications** — who is responsible for what
2. **Drawing list gaps** — missing submittals, missing disciplines
3. **Technical design issues** — conflicts, calculations, studies
4. **Process/compliance** — DMP adherence, LOD definitions, timelines
5. **Documentation** — missing deliverables, format issues
