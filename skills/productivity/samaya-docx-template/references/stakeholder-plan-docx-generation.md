# Stakeholder Management Plan DOCX Generation

## Overview

This reference documents the workflow for generating a Samaya-branded DOCX of the Stakeholder Management Plan (SMP) from the source HTML, including SVG chart embedding and personnel verification.

## Source HTML

The SMP HTML lives at:
```
/Users/mohamedessa/aseer-museum-pm/03_Plans/02_Stakeholder/MOC-ASEER-SIC-1K0-PL-0020_Rev03_Stakeholder_Management_Plan.html
```

### Content extraction

The HTML is ~293KB / 2511 lines. Use `html2text` via terminal to extract clean text:

```bash
cd /Users/mohamedessa/aseer-museum-pm/03_Plans/02_Stakeholder
python3 -c "
import html2text
with open('MOC-ASEER-SIC-1K0-PL-0020_Rev03_Stakeholder_Management_Plan.html', 'r') as f:
    html = f.read()
h = html2text.HTML2Text()
h.ignore_links = False
h.ignore_images = False
h.ignore_tables = False
h.body_width = 0
text = h.handle(html)
with open('/tmp/smp_text.txt', 'w') as f:
    f.write(text)
print(f'Extracted {len(text)} chars')
"
```

Then read in chunks via `read_file` with offset/limit.

## Section-to-SVG Chart Mapping

| Section | Content | Chart Type | SVG Required |
|---------|---------|------------|-------------|
| Sec 3.2 | Stakeholder Ecology Diagram | Hub-and-spoke with 4 spheres | YES - Ecology SVG |
| Sec 5.1 | Power-Interest Matrix | 2x2 table | Table (keep as table) |
| Sec 6 | Engagement Assessment Matrix | Table with C/D markers | Table (keep as table) |
| Sec 10 | Interface Coordination | Table with 16 interfaces | Table (keep as table) |
| Sec 11 | Escalation Procedure | 5-tier L1-L5 flowchart | YES - Escalation SVG |
| Sec 14.1 | Organisation Chart | Org chart: MoC > PMC > CG > Samaya PD > T1 + NRS > Specialists | YES - Org Chart SVG |

## SVG-to-PNG-to-DOCX Embedding Pattern

### Prerequisites

```bash
brew install cairo
pip3 install cairosvg
```

### Run command

```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 gen_script.py
```

### Helper function

```python
import tempfile, os, cairosvg
from docx.shared import Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_svg_to_doc(doc, svg_content, width_cm=16.5):
    """Render SVG string to PNG and insert into SamayaDoc document."""
    png_data = cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), output_width=1740)
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        f.write(png_data)
        temp_path = f.name
    p = doc.doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(temp_path, width=Cm(width_cm))
    os.unlink(temp_path)
    return p
```

**IMPORTANT:** Use `doc.doc.add_paragraph()` (accessing the underlying python-docx Document), NOT `doc.add_paragraph()` which does not exist on SamayaDoc.

### SVG design rules

- Use `font-family="Calibri,sans-serif"` to match DOCX body font
- Set explicit `viewBox` for aspect ratio
- Use Samaya palette: `#1E293B` (navy), `#0284C7` (blue), `#16A34A` (green), `#92400E` (amber), `#B91C1C` (red), `#64748B` (gray)
- Wrap in `<rect>` background `#F8FAFC` for clean look
- **Escape `&` as `&amp;`** in SVG text content (e.g. `T&amp;C Mgr` not `T&C Mgr`)
- Crop viewBox to actual content bounds (not full canvas width)

## SVG Chart Specifications

### 1. Stakeholder Ecology Diagram

- **Type:** Hub-and-spoke with 4 spheres
- **Center:** Samaya PMO (circle, navy `#1E293B`)
- **4 spheres connected by dashed lines:**
  - **Strategic Sphere** (top, navy `#0F172A`): MoC, ACE PMC, Samaya Board
  - **Delivery Sphere** (right, blue `#0284C7`): Samaya PD, NRS Lead, CG Engineer, T1 Management
  - **Execution Sphere** (bottom, green `#16A34A`): T2 Specialists, Suppliers, Subs
  - **Validation Sphere** (left, amber `#92400E`): 7 Authorities, ITCA, Operator, Public/Press
- **viewBox:** `0 0 1100 620`

### 2. Escalation Procedure Flowchart

- **Type:** 5-tier L1-L5 horizontal pipeline with triggers section below
- **L1** (navy): Discipline Lead, SLA 48h
- **L2** (blue): BIM Manager, SLA 7d
- **L3** (amber): Project Director (Eng. Waris Sultan), SLA 14d
- **L4** (red): PMC (ACE), SLA 21d
- **L5** (navy, below): Client/MoC, Per Contract
- **Down arrow** from L4 to L5 via L-shaped path
- **Triggers section:** 8 triggers (T-01 to T-08) in a white box
- **Concurrent escalation rule** in light gray box
- **Conflict resolution rules** (4 rules) in light gray box
- **viewBox:** `0 0 1100 520`

### 3. Organisation Chart

- **Type:** Top-down hierarchy
- **MoC** (navy) > **ACE PMC** (blue) > **CG** (amber) > **Samaya PD** (green, Eng. Waris Sultan)
- **T1 Management row** (dark gray): BIM (Dr. Waleed), HSSE (Eng. Mohamed), QA/QC (Vacant), Procurement (Hani), Tech Office (Eng. Sultan), Site Mgr (TBC)
- **NRS Design Lead** (navy, Eng. Jim) - dashed line from PD
- **Specialists row** (gray): AD Engineering, Rawasin, Studio ZNA, Glasbau Hahn, Interactive Specialist (TBC)
- **Additional roles row** (gray): Sustainability (M. Fida), IT/Security (TBC), IT/Data Liaison (Salah), DC (Hesham), T&C Mgr (TBC)
- **viewBox:** `0 0 1100 620`

## DOCX Structure (15 Sections)

| Section | Title | Content |
|---------|-------|---------|
| Cover | - | Project info, revision, status |
| 1.0 | Document Control | Revision history (4 revs), document ID table, QC sign-off |
| 2.0 | Purpose, Scope & Definitions | Lifecycle scope (7 phases), 6 objectives, acronyms table |
| 3.0 | Stakeholder Identification | 6 methods, Ecology SVG, snapshot counts |
| 4.0 | Stakeholder Register | T1 (15 roles), T2 (23 roles), T3 (12 roles), External (5), Ops (5) |
| 5.0 | Stakeholder Analysis | P/I matrix, Salience model (8 stakeholders), Influence/Impact (12) |
| 6.0 | Engagement Assessment Matrix | 5 levels, C/D states (12 stakeholders), gap analysis (9 actions) |
| 7.0 | Engagement Strategy | 4 quadrants, phase intensity (7 groups x 7 phases), cultural considerations |
| 8.0 | Communication Plan | 5 channels, 8 reports, 11 meetings, BIM cadence, 6 authority cycles |
| 9.0 | Roles & Responsibilities (RACI) | 10 deliverables x 7 roles, supplementary T&C RACI |
| 10.0 | Interface Coordination Matrix | 5 types (A-E), 16 interfaces with resolution logic |
| 11.0 | Escalation Procedure | Escalation SVG, 8 triggers, 4 conflict rules |
| 12.0 | Monitoring & KPIs | 11 KPIs, 7 dashboard panels |
| 13.0 | Change Management | 5 triggers, 6 onboarding steps, 6 off-boarding steps |
| 14.0 | Visual Tools & Schedules | Org chart SVG, engagement calendar, communication matrix |
| 15.0 | Compliance & Authorization | 8 CG comments, sign-off block, distribution list |

## Personnel Verification Protocol

**CRITICAL:** Verify all personnel names against the SMP HTML and Key Personnel Register before writing. The following are verified correct for Rev 03:

| Role | Name | Notes |
|------|------|-------|
| Project Director | Eng. Waris Sultan | NOT Adel Darwish |
| Sustainability Specialist | Muhammad Fida | NOT Sustainability Manager |
| QA/QC Manager | Vacant (Samir acting) | NO mention of Medhat |
| Procurement Manager | Hani Alghamdi | |
| IT/Security Specialist | TBC (T1-07) | |
| IT/Data Authority Liaison | Eng. Salah Eldin (T3-09) | |
| Technical Office Manager | Eng. Mohamed Sultan | |
| BIM Manager | Dr. Waleed Salah | |
| HSSE Manager | Eng. Mohamed Ahmed | |
| Document Controller | Eng. Hesham Abdelhamid | |
| Project Engineer | Eng. Ahmed Salah | |
| Architecture/BIM Lead | Eng. Ali Abdelrahman | |
| MEP Design Agency | AD Engineering | PO issued Jun 21 |
| Exhibition Lighting | Studio ZNA | Julie Riley |
| AV/IT Systems Integrator | Rawasin | Sister company |
| Interactive Specialist | TBC | Lumotion declined |

## Revision History Format

| Rev | Date | Description | Status |
|-----|------|-------------|--------|
| 00 | 01-MAR-26 | Initial Issue for CG Review | Code C |
| 01 | 21-MAY-26 | Resubmission - 19 CRS comments from CG | Code C |
| 02 | 05-JUN-26 | Resubmission - IT/Security reclassified, MEP design agency added | Approved |
| 03 | 03-JUL-26 | Personnel updates: AD Engineering, Waris Sultan, Rawasin, Sustainability Specialist, Studio ZNA, Interactive TBC | This submission |

## Personnel Verification Protocol (CRITICAL)

Every name must be cross-checked against the repo BEFORE writing. Authoritative sources (in order):

1. `Technical_Office/Specialist_Management/specialist_register.md` — live specialist register
2. `03_Plans/10_Resource/resource_management_plan.md` — full org chart
3. `99_Archive/00_Project_Overview/PROJECT_MEMORY.md` — latest project status

### Verified names for Aseer Museum (as of Jul 2026)

| Role | Name | Source |
|------|------|--------|
| Project Director | Eng. Waris Sultan | specialist_register.md |
| BIM Manager | Dr. Waleed Salah | specialist_register.md |
| Technical Office Manager | Eng. Mohamed Sultan | resource_plan.md |
| HSSE Manager | Eng. Mohamed Ahmed | specialist_register.md |
| QA/QC Manager | Vacant (Samir acting) | specialist_register.md |
| Procurement Manager | Hani Alghamdi | resource_plan.md |
| Site Manager / Construction Manager | Mohamed Samir | odoo_mapping + project_status |
| Document Controller | Eng. Hesham Abdelhamid | resource_plan.md |
| Project Engineer | Eng. Ahmed Salah | resource_plan.md |
| Architecture / BIM Lead (Interior Architect) | Eng. Ali Abdelrahman | resource_plan.md |
| Sustainability Specialist | Muhammad Fida | specialist_register.md |
| IT/Security Specialist | TBC | specialist_register.md |
| MEP Design | AD Engineering | specialist_register.md |
| Lighting | Studio ZNA | specialist_register.md |
| AV/IT Systems | Rawasin | specialist_register.md |
| Interactives | TBD | specialist_register.md (Lumotion declined) |
| Scenographer | NRS | specialist_register.md |
| Setworks/Joinery | NRS design + Samaya Factory fab | specialist_register.md |
| Graphics | Samaya-Graphic - Approved | specialist_register.md |
| Structural | Radiance / TBD | specialist_register.md |

## What NOT to Include in Stakeholder Descriptions

CG does NOT need internal notes or procurement details. Strip these:

| Remove | Reason |
|--------|--------|
| "CV submitted", "CV via DS" | Internal HR tracking |
| "PQD to be submitted", "PQD under submission" | Procurement status |
| "PO issued", "kick-off Jun" | Commercial detail |
| "Fee X approved", "SAR X/month" | Commercial — never disclose fees |
| "agreed DD-MMM-YY" | Internal agreement date |
| "Target: CP-X Decision/Mobilisation" | Internal milestones |
| "Per KP Register Rev CXX" | Internal reference |
| "pending CG/MoC approval" | Status note, not role description |
| "Sub-contracted" | Redundant — all T2 are subcontracted |
| "hard/softscape" | Detail belongs in scope doc |
| "Pre-qual pending" | Use "Approved" or "TBC" |
| "Appointed by Samaya - experienced" | Redundant — just state firm name |

Keep it minimal: `"AD Engineering"` not `"AD Engineering - PO issued Jun 21 - kick-off Jun 25"`. Stakeholder register shows WHO and scope, not procurement history.

## Page Balance and Compaction Strategy

Three levels of compaction by content density:

| Class | When | Effect |
|-------|------|--------|
| `compact tight` | All pages (except cover) | 0.46rem font, reasonable padding |
| `compact tight xtight` | Pages >75% full | 0.38rem font, 1px padding, tighter margins |
| Plain `page` | Cover only | Full spacing |

Check density before deciding:
```python
est_height = text_len * 0.03 + table_rows * 10 + svgs * 100
available = 1972
pct = est_height / available * 100
# >75% -> xtight, otherwise compact tight
```

## Image Rendering Fixes (Word on macOS)

Word on macOS fails to render python-docx images if:
1. **RGBA mode** — convert to RGB with white background via Pillow
2. **cNvPr name is temp filename** — must match docPr name by position
3. **noChangeAspect missing** on graphicFrameLocks — add it
4. **JPEG preferred** — if PNG fails, convert to JPEG (Word renders JPEG more reliably)

**Best approach:** Replace SVG charts with styled tables (tables always render in Word).

## AI Fingerprint Cleanup (MANDATORY)

Strip ALL of these after generation:

| Symbol/Phrase | Replace with |
|---------------|-------------|
| Section symbol (§), &sect; | "Sec." |
| Em-dash, en-dash, &mdash;, &ndash; | " - " |
| Middle dot (·), &middot; | " - " |
| Smart quotes ("") | Straight quotes |
| "systematic parse", "comprehensive" | "review", "full" |
| "utilize", "leverage", "robust" | "use", "use", "strong" |
| "seamless", "holistic", "innovative" | "smooth", "complete", "new" |
| "bespoke", "cutting-edge", "state-of-the-art", "synergistic" | Remove |
| "it should be noted", "as shown above", "the following sections" | Remove entirely |

Run this after EVERY generation. User rejects documents with AI fingerprints.

## CG Comments: External CR Sheet Only

CG comment disposition MUST NOT be in the plan. Keep only:
```
CG Comments: All closed in Rev 02. Full disposition per attached CR sheet.
```
The CR sheet is a separate Excel file in `02_CG_Responses/`. Do not include comment-by-comment tables in the plan.

## Common Pitfalls

1. **`&` in SVG text:** Must be escaped as `&amp;` or cairosvg fails with XML parse error.
2. **`doc.paragraphs` vs `doc.doc.paragraphs`:** SamayaDoc wraps Document as `self.doc`. Use `doc.doc.paragraphs`.
3. **Table column widths:** Sum ~16.5cm for A4. Use narrower columns for 9+ column tables.
4. **SVG viewBox cropping:** Crop to actual content bounds, not full canvas width.
5. **DYLD_FALLBACK_LIBRARY_PATH:** Required for cairosvg on macOS with Homebrew cairo.
6. **Symbol cleanup:** Run after EVERY generation — mandatory.
7. **Personnel names:** Verify every name against 3 repo sources before writing.
8. **Stakeholder names:** Use proper names (Samaya Investment, Ministry of Culture, Consultancy Group, ACE Moharram-Bakhoum, Nissen Richards Studio) not generic terms.
