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

## Common Pitfalls

1. **`&` in SVG text:** Must be escaped as `&amp;` or cairosvg will fail with XML parse error. Check all SVG text content for `&` characters (e.g. `T&C` must be `T&amp;C`).

2. **`doc.paragraphs` vs `doc.doc.paragraphs`:** SamayaDoc wraps python-docx's `Document` as `self.doc`. To access paragraphs/tables for cleanup, use `doc.doc.paragraphs` and `doc.doc.tables`, not `doc.paragraphs`.

3. **Table column widths:** Sum must equal ~16.5cm for A4 portrait (21cm page - 2.5cm left - 2.0cm right). Wide tables (9+ columns) need narrow columns (0.6-1.5cm each).

4. **SVG viewBox cropping:** Crop to actual content bounds. If content spans x=30 to x=1040, use `viewBox="0 0 1100 620"` not `1740`.

5. **DYLD_FALLBACK_LIBRARY_PATH:** Always required for cairosvg on macOS with Homebrew cairo. Without it: `OSError: no library called "cairo-2"`.

6. **Symbol cleanup after generation:** Run `clean_symbols()` after all content is added to remove section symbols, em-dashes, smart quotes, accented characters, and bullet symbols.

7. **Gen script location:** Save alongside the output DOCX in `01_Source_Files/03_Word/` for reproducibility.

8. **Stakeholder names:** Use proper names (Samaya Investment, Ministry of Culture, Consultancy Group, ACE Moharram-Bakhoum, Nissen Richards Studio) not generic terms (the Contractor, the Client, the Consultant, the Designer).
