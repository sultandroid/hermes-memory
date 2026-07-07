# Prequalification Letter Pattern — Subcontractor → Samaya

Use when generating a prequalification letter **on behalf of a subcontractor** addressed to Samaya, confirming they understand the project, design, execution sequence, and comply with all requirements.

## When to use

- A subcontractor needs to submit a prequalification letter to Samaya
- The letter is written **as if from the subcontractor** (first-person "we")
- The letter confirms: project understanding, design understanding, execution sequence understanding, and compliance with all requirements

## Document structure (7-9 sections)

| # | Section | Content | Required? |
|---|---------|---------|-----------|
| 1 | Introduction | Company name, project name, contract number, interest in being considered | Yes |
| 2 | Project Understanding | Scope, design intent, specs, programme, CG supervision structure | Yes |
| 3 | Design Understanding | Design intent, coordination with NRS/BIM, material submittal process, shop drawings | Yes |
| 4 | Execution Sequence Understanding | Phased delivery, enabling works, service coordination, inspection hold points, handover | Yes |
| 5 | Compliance Statement | Commit to specs, QMS, HSE, programme, BEP, CG approval, SBC requirements | Yes |
| 6 | Company Capability | Experience, qualified team, equipment, supply chain | Yes |
| 7 | Declaration | Accuracy statement, readiness to proceed, signature block | Yes |
| 8 | RACI Matrix | 12-activity matrix across subcontractor, NRS, Samaya BIM, Samaya PM, CG | Recommended for complete package |
| 9 | Risk Register | 8 project-specific risks with likelihood/impact/severity/mitigation/owner | Recommended for complete package |

### RACI Matrix (§8) — when to include

Add when the subcontractor has no prior museum experience and needs to demonstrate they understand who does what. 12 rows covering: design development, shop drawings, material submittals, BIM coordination, underground services, MEP interface, QC/ITP, HSE, progress reporting, snagging, as-builts, commissioning/handover.

Columns: Activity | Subcontractor | NRS | Samaya BIM Unit | Samaya PM | CG

### Risk Register (§9) — when to include

Add when the subcontractor needs to show they've thought through project-specific risks. 8 rows minimum. Columns: # | Risk Description | Likelihood | Impact | Severity | Mitigation Measure | Owner

Common risks for landscaping: imported plant lead times, weather windows, underground services clashes, CG material rejection, coordination delays, site access, irrigation design changes, labour availability.

## Style rules

- **DO NOT use SamayaDoc** — this is the subcontractor's own document, not Samaya's
- Use standalone `python-docx` with the subcontractor's own branding/colors
- Cover says "Submitted to: Samaya Investment" and "Prepared by: [Subcontractor Name]"
- Navy `#1E293B` headings, 11pt Calibri body, A4 margins (2.5cm top/left, 2.0cm bottom/right)
- No Samaya logo — the subcontractor's own letterhead or name only

## Doc ref pattern

```
MOC-ASEER-SIC-1K0-PQ-00XX
```

Where `XX` = next available sequential number. Check existing PQs in the target folder first.

## File placement

```
.../02_Submittals/09_Prequalifications/Landscape_Evergreen_Prequalification_Letter.docx
```

Copy via AppleScript `duplicate` from `/tmp/` to the OneDrive path (never write directly to OneDrive).

## Gen script skeleton

```python
from docx import Document
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import nsdecls
from docx.oxml import parse_xml

NAVY = RGBColor(0x1E, 0x29, 0x3B)
DARK_GRAY = RGBColor(0x33, 0x41, 0x55)
MED_GRAY = RGBColor(0x64, 0x74, 0x8B)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x00, 0x00, 0x00)

doc = Document()
# A4 page setup
section = doc.sections[0]
section.page_width = Cm(21.0)
section.page_height = Cm(29.7)
section.top_margin = Cm(2.5)
section.bottom_margin = Cm(2.0)
section.left_margin = Cm(2.5)
section.right_margin = Cm(2.0)

# Cover: centered title + meta block
# Body: 7 sections with add_h1 / add_body helpers
# Signature block
doc.save("/tmp/CompanyName_Prequalification_Letter.docx")
```

## Pitfalls

- **Confirm the subcontractor's actual scope** before writing — don't assume from the company name. The user may say "router" meaning "route" (as in "route to models"). Ask for clarification when the scope is unclear.
- **Doc ref number** — check the existing PQs in `09_Prequalifications/` to find the next available number. Don't use a placeholder that conflicts.
- **OneDrive copy** — always stage to `/tmp/` and use AppleScript `duplicate` to copy to OneDrive. Verify with `ls -la` that the file has non-zero size.
- **No Samaya branding** — this is the subcontractor's document, not Samaya's. No SamayaDoc, no Samaya logo, no Samaya header/footer.
- **Email to procurement: clarify the action clearly.** When telling procurement to send the doc to the supplier for stamping, state explicitly: (1) send the doc to the supplier, (2) ask them to stamp + sign, (3) return to us. Don't say "review and stamp" — that sounds like procurement should stamp it themselves. The user corrected: "contact the supplier to stamp and resend."
- **Explain WHY the doc was prepared on their behalf.** If the supplier has no museum experience, say so explicitly in the email. The user said: "he hasent experiance in musuem before" — that's the reason we prepared the support doc for them. State it in the email so procurement understands the context.
- **Reference existing SOW doc.** The subcontractor folder already has a `SCOPE_REQUEST.docx` and `SCOPE_REQUEST.md`. Mention in the email that a separate SOW will follow (or already exists). Don't let procurement think the prequal letter is the full scope definition.
- **Include relevant drawings.** When sending the prequal package, also send reference drawings (site plans, sections, structural reports) so the supplier can properly understand the scope. Check the subcontractor's `02_Reference_Drawings/` folder and the project's Arch DD Package for relevant PDFs.
