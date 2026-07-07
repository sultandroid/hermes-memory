# Showcase Microclimate Control Report Pattern

Use when producing an action report for museum showcase environmental control systems.

## Key domain rules

- **Connected showcases share air volume.** If showcases are open to each other internally, one microclimate unit serves the entire cluster. Installing multiple units in the same air volume creates conflicting control loops.
- **Quantity = clusters, not individual showcases.** Count connected groups, not total showcase count.
- **One unit per cluster** regardless of cluster size (10 connected cases = 1 unit).

## Report structure — two variants

### Variant A: Full Action Report (internal / procurement use)

| Section | Content |
|---------|---------|
| 1.0 Introduction | Project context, showcase count, cluster arrangement |
| 2.0 Recommended Solution | Device type, components table (unit, sensor, data output) |
| 3.0 Methodology | Control cycle flowchart + installation methodology flowchart |
| 4.0 Distribution Plan | Table: cluster → showcases → air volume → units required |
| 5.0 Cost Estimate | Itemised table with unit price, qty, subtotal. Mark costs TBC. |
| 6.0 Comparison | Alternatives table (silica gel, data loggers, microclimate units) |
| 7.0 Recommendation | Summary + next steps |

### Variant B: Methodology Submittal (client submission — NO financial data)

Strip cost/comparison sections when the deliverable goes to the client:

| Section | Content |
|---------|---------|
| 1.0 Introduction | Project context, showcase count, cluster arrangement |
| 2.0 Recommended Solution | Device type, components table (unit, sensor, data output) |
| 3.0 Methodology | Control cycle flowchart + installation methodology flowchart |
| 4.0 Distribution Plan | Table: cluster → showcases → MCU → sensors → air volume |
| 5.0 [Optional] Recommended Device | Specific model specs table, manufacturer, note about TBC confirmation |
| 6.0 Showcase Layout Plans | Clean PDF-extracted plans with figure captions (see annotation workflow below) |
| 7.0 Recommendation | Summary + next steps |

**Rule:** Client submittals get methodology only. Financial data (cost tables, comparison rows, TBC notes, supplier quotation recommendations) stays in internal Action Reports.

### Variant C: Methodology with Device Specs (client submittal including equipment data)

Same as Variant B but insert a Section 5 with a technical specification table for the recommended device. This is appropriate when the user explicitly asks for or provides device specs. The section goes between Distribution Plan and Layout Plans:

```
5.0  RECOMMENDED DEVICE — FREEAIR FL-Z81

Body text explaining the recommendation context.

| Parameter | Value |
|-----------|-------|
| Model No. | FL-Z81 |
| Voltage | 220-240V / 50Hz / 1PH |
| Air Circulation | 90 m³/h |
| Power Input | 350 W |
| Operating Temperature | 5-38°C |
| Refrigerant | R410A / R407C / R134A |
| Air Inlet Diameter | 30 mm |
| Air Outlet Diameter | 30 mm |
| Dimensions | 500 × 480 × 250 mm |
| Weight | 30 kg |
| Suitable Space | ≤ 0.5-1 m³ |

Note: Specifications per manufacturer datasheet. Final selection to be confirmed against cluster's actual internal air volume. Supplier quotation required before procurement.
```

## Flowchart types

1. **Control Cycle Flowchart** — closed-loop: Showcase Air → Filter → Sensor → Controller Decision (Peltier for T, Humidifier/Dehumidifier for RH) → Fan → Return to Showcase, with continuous feedback loop
2. **Installation Methodology Flowchart** — 8 steps: Site Survey → Unit Selection → Mount → Power → Setpoint Config → Stabilization Test (48-72h) → Calibration Verify → Artifact Placement

## SVG design for DOCX flowcharts

- viewBox must be **cropped to content bounds**, not the full canvas. If content spans x=30 to x=1040, use `viewBox="0 0 1100 520"` not `viewBox="0 0 1740 520"` — otherwise the image appears off-center with empty space on the right.
- Colors: navy `#1E293B` boxes, dark gray `#334155` alternate, red `#B01E2F` diamonds/circles
- Font: Calibri 14-16px for titles, 12-13px for sub-text (larger than default for readability)
- Box sizes: 200x100px for main steps, with 8px border-radius
- Arrow markers: 14x10px with stroke-width 3
- Dashed feedback loop line in `#64748B`
- Export via cairosvg with `output_width=1740`, insert at `width=Cm(16.5)` (full A4 text width)
- Center images via `p.alignment = WD_ALIGN_PARAGRAPH.CENTER`

### Arrow routing for multi-row flowcharts

When creating 2-row flowcharts (Row 1: Steps 1-4, Row 2: Steps 5-8):

1. The down arrow from Row 1 must route to the **START** of Row 2 (Step 5), not drop straight down from Step 4
2. Use an L-shaped path: `M{x4},{y1_bottom} L{x4},{mid_y} L{x5},{mid_y} L{x5},{y2_top}`
3. The arrow endpoint (`y2`) must exactly equal the target box's `y` value — even a 10px gap means the arrowhead doesn't touch the box
4. Example: `path="M940,180 L940,210 L130,210 L130,250"` (from Step 4 at x=940 to Step 5 at x=130)

## Cost presentation

- Only branded option (CCI RH-33 class) in formal reports — no Alibaba/cheap alternatives
- Mark all prices as TBC with note: "Final pricing requires supplier quotation"
- Include installation, commissioning/calibration, and shipping as separate line items

## User prefers MANUAL annotations on plans — do NOT automate

When the user says "mark on the plans where we put the devices": **do NOT programmatically annotate the plans.** The user will correct you ("your annotation outside the showcase itself", "remove the annotations") and then do their own annotations manually in Word/PDF.

**Workflow instead:**
1. Extract clean pages from the PDF at full resolution via PyMuPDF
2. Resize to ~1500px for DOCX embedding
3. Embed with a descriptive italic caption (Figure 1, 2, 3) that mentions showcase clusters, MCU numbering, and what could be marked
4. Let the user annotate manually in their drawing software or by hand
5. After they save their annotated version, read the DOCX to confirm changes, then stop — do NOT regenerate

**Pitfall:** The user wants clean plans with just captions. Annotations (colored circles, callouts, legend boxes, boundary rectangles) placed by script are imprecise (you don't know the exact geometry of showcase positions in a PDF) and will be rejected. Embed clean, embed small, let the user mark up.

## After user annotates plans manually — add matching legend text

When the user says "I added points manually in the layout for the device locations" and provides their symbol list (e.g. `●  MCU-01  —  SHC-01 cluster (3 showcases)`):

1. **Read the existing DOCX** — NEVER regenerate. Find the Section 6 intro paragraph (just before "Figure 1")
2. **Remove any old legend** elements between intro and first figure caption
3. **Insert new legend** as `<w:p>` elements via lxml XML insertion into the body:
   - Bold title: "Legend — Device and Sensor Markings:"
   - One line per MCU: `●  MCU-NN  —  Description for cluster (X showcases)`
   - Logger line: `■  Logger  —  Data Logger / T/RH Sensor (1 per showcase)`
   - Gateway line: `◆  Gateway —  Gateway / Base Station`
   - "Figure 4:" caption in italic gray
4. **Verify** by re-reading and printing figure captions

**Key:** Match the user's exact symbols (`●`, `■`, `◆`) and exact cluster naming. Do NOT change cluster names or counts — the user's manual annotations on the plans are authoritative for the actual layout.

## DOCX patching workflow — preserve manual edits

**CRITICAL:** When the user has made manual edits in Word (annotations on plans, text changes, formatting), NEVER regenerate the entire DOCX from the gen script. Regeneration overwrites their work. Instead, patch the XML tree directly.

### Option A: Add new content before/after existing paragraphs (insert into XML tree)

Use `python-docx` + lxml to insert new paragraphs/tables at specific positions in the XML body:

```python
from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document(path)
body = doc.element.body

# Find the anchor paragraph
for elem in body:
    if elem.tag == qn('w:p'):
        texts = [t.text or '' for t in elem.iter(qn('w:t'))]
        if 'anchor text' in ''.join(texts):
            anchor = elem
            break

def insert_after(ref, el):
    parent = ref.getparent()
    parent.insert(list(parent).index(ref) + 1, el)

# Build new element (paragraph, table, etc.)
new_p = OxmlElement('w:p')
# ... construct content with runs, text, formatting ...
insert_after(anchor, new_p)
```

### Option B: Renumber sections inline

When inserting a new section (e.g. Section 5) before an existing one, renumber the displaced sections by modifying the text runs in-place:

```python
for p in doc.paragraphs:
    for run in p.runs:
        if '5.0' in run.text and 'SHOWCASE LAYOUT' in p.text:
            run.text = run.text.replace('5.0', '6.0', 1)
```

### Option C: Add legend after figure section intro

Common pattern: user annotates plans manually, then needs a matching legend in the document body. Insert the legend as a series of `<w:p>` elements between the section intro paragraph and the first figure caption:

```
Legend — Device and Sensor Markings:
●  MCU-01  —  Description for cluster 1
●  MCU-02  —  Description for cluster 2
...etc...

Figure 4: Legend for device and sensor locations shown on the layout plans.
```

Each legend line is a separate paragraph with `•` or symbol character at the start. Use bold for the legend title, normal weight for items, italic gray for the Figure 4 caption.

### Rules for patching existing DOCX

- Always read the existing DOCX first to understand the current structure before attempting any patch
- Use `python-docx` API for simple reads/renumbers (paragraphs, runs, tables); drop to lxml XML manipulation for insertions
- After patching, verify by re-reading the DOCX and printing section headings + figure captions
- If the patch script fails (AttributeError, missing method), fall back to lxml XML tree manipulation instead
- When inserting complex content (tables with formatting, colored header rows, alternating fills), build the XML directly — python-docx table creation methods may not place the table correctly in the body

When the user provides a PDF with showcase layout plans and asks to embed them, follow this pattern:

### 1. Extract pages from PDF using PyMuPDF

```python
import fitz, tempfile, os

def extract_pngs(pdf_path, scale=2):
    doc = fitz.open(pdf_path)
    paths = []
    for i in range(len(doc)):
        page = doc[i]
        pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale))
        path = os.path.join(tempfile.mkdtemp(), f'page_{i+1}.png')
        pix.save(path)
        paths.append(path)
    return paths
```

### 2. Resize for DOCX embedding

DOCX files bloat with full-resolution images (5MB+ per page). Resize to ~1500px wide before embedding:

```python
from PIL import Image

def resize_for_docx(src_path, target_width=1500):
    img = Image.open(src_path)
    w, h = img.size
    r = target_width / w
    img_resized = img.resize((target_width, int(h * r)), Image.LANCZOS)
    dst = src_path.replace('.png', '_resized.png')
    img_resized.save(dst, quality=88, optimize=True)
    return dst
```

### 3. Insert into SamayaDoc

```python
from docx.shared import Cm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_image(doc, img_path, width_cm=16.0, caption=""):
    if not os.path.exists(img_path):
        doc.add_body(f"[Image not found: {img_path}]")
        return
    p = doc.doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(img_path, width=Cm(width_cm))
    if caption:
        c = doc.doc.add_paragraph()
        c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = c.add_run(caption)
        r.font.size = Pt(9)
        r.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
        r.font.italic = True
```

**Labels:** Figures get numbered italic captions (Figure 1, Figure 2, etc.) in gray #64748B, 9pt.

### 4. Section placement

Add a dedicated "Showcase Layout Plans" section after the Distribution Plan table and before the Recommendation.

### SamayaDoc API quirk — adding raw paragraphs

SamayaDoc does NOT expose add_paragraph() directly. To insert raw paragraphs (images, non-standard formatting), use:

```python
p = doc.doc.add_paragraph()  # NOT doc.add_paragraph()
```

The `doc` attribute is the underlying python-docx Document() object.

## Annotating showcase plans with MCU / sensor locations

When the user provides PDF plan drawings and says "mark on the plans where the devices and sensors go":

### Workflow

1. **Extract pages** from PDF via PyMuPDF at 2x resolution (full-res for annotation, then resize)
2. **Annotate using Pillow** — draw colored markers, cluster boundary rectangles, legend boxes, callout arrows
3. **Resize** annotated images to ~1500px wide for DOCX embedding (keeps file size manageable)
4. **Embed into DOCX** after the Distribution Plan section, before Recommendation

### Color-coding convention per cluster

Use distinct colors per MCU so the reader can instantly map cluster | device:

| MCU | Cluster | Color | RGB |
|-----|---------|-------|-----|
| MCU-01 | SHC-01 (largest group) | Red | (200, 60, 80) |
| MCU-02 | SHC-02 (medium group) | Orange | (220, 120, 60) |
| MCU-03 | SHC-04 (corner/small) | Green | (60, 180, 100) |
| MCU-04 | SHC-05 (corner/small) | Brown | (180, 100, 60) |
| Data loggers | Per showcase | Blue | (50, 120, 200) |
| Gateway | Central | Green | (100, 180, 100) |

### Annotation elements

| Element | PIL method | Purpose |
|---------|-----------|---------|
| Filled circle | draw.ellipse() | MCU location marker |
| Color rectangle | draw.rectangle() | Cluster zone boundary |
| Legend box | draw.rectangle() + text | Color mapping key |
| Callout line | draw.line() | Connect marker to label |
| Title band | draw.rectangle() + text | Bottom-of-image figure title |

### Key PIL code patterns

**Rounded-rect helper** (Pillow lacks rounded_rectangle in older versions; use rectangle + corner fills):

```python
def draw_bg_box(draw, xy, fill):
    x1, y1, x2, y2 = xy
    draw.rectangle(xy, fill=fill)
    r = 20
    draw.rectangle((x1+r, y1, x2-r, y1+r), fill=fill)
    draw.rectangle((x1+r, y2-r, x2-r, y2), fill=fill)
    draw.rectangle((x1, y1+r, x1+r, y2-r), fill=fill)
    draw.rectangle((x2-r, y1+r, x2, y2-r), fill=fill)
```

**Font loading** (macOS paths vary):
```python
fnt_title = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 72)
fnt_label = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 56)
```

**Anchored text** (anchor="mm" for center alignment):
```python
draw.text((cx, cy), "TEXT", fill=(255,255,255), font=fnt_title, anchor="mm")
```

### Numbered integration callouts (showcase detail page)

For the construction detail page showing a single showcase, use numbered callouts (1-5) with leader lines to specific drawing parts:

1. MCU mount point inside base
2. T/RH sensor inside showcase
3. Low-voltage power supply connection
4. Air intake and return vent
5. Data cable route to gateway

### Figure captions

After each annotated image, add a numbered italic caption in gray that explains both what the original drawing shows and what the annotations added:

```python
caption = doc.doc.add_paragraph()
caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = caption.add_run("Figure 1: Master Layout Plan -- MCU locations per cluster...")
r.font.size = Pt(9)
r.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)
r.font.italic = True
```

## SVG pitfalls (cairosvg)

### Ampersand character breaks XML parsing

The `&` character is not valid in XML attribute values or SVG text content unless escaped. Cairosvg parses SVGs as XML and throws ParseError: not well-formed (invalid token) if an unescaped `&` appears in the SVG string:

```python
# WRONG -- ParseError
text = "Power and Data Connection"

# RIGHT
text = "Power and Data Connection"
```

Fix: Always scan SVG string constants for bare `&` characters. Use "and" instead. The `&amp;` entity works but is easy to forget; safest to just write "and".

### Other SVG-in-DOCX rules

- viewBox must be cropped to content bounds -- content at x=30 to x=1040 means viewBox="0 0 1100 520", not a full 1740 canvas
- Arrow endpoints must exactly equal the target box's y value -- even 10px gap means the arrowhead floats
- Always run with DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib
- Font in SVG: font-family="Calibri, Arial, sans-serif" so DOCX matches

## Pitfalls

- **Verify project before generating.** Do not assume which project a report belongs to based on session context alone. The user may be asking about Zamzam while the session is in Aseer context, or vice versa. Confirm the project explicitly before writing any project-specific content (showcase IDs, gallery names, cluster arrangements, doc ref prefix). Generating for the wrong project wastes time and requires deletion + re-generation.
- Do NOT assume one unit per showcase — always ask if they're connected internally
- Do NOT include Alibaba pricing in formal branded reports unless explicitly asked
- Do NOT include financial data in client-submittal methodology reports (Variant B). Cost tables, comparison rows, TBC notes, and supplier quotation recommendations belong only in internal Action Reports, not client-facing methodology submittals.
- Do NOT forget the stabilization period (48-72h) before artifact placement
- Always run cairosvg with `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib` on macOS
- DOCX file size grows significantly with embedded images (241KB without plans → 1.6MB with 3 plans). Resize to 1500px before embedding.
- PyMuPDF (fitz) is the reliable tool for PDF page extraction — read_file on a PDF gives raw text, not page images.
