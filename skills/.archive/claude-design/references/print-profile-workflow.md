# Print-Ready Corporate Profile / Technical Proposal Workflow

Use when the user asks for a **print-ready corporate profile, capability statement, or technical proposal** in A4 landscape format with embedded images, bilingual text, and professional branding.

## Typical Trigger Phrases
- "design profile ready to print in A4"
- "technical proposal for prequalification"
- "corporate capability brochure"
- "make it like a printed document"

## Workflow

### 1. Research & Gather Assets
- Search the web for the company (LinkedIn, website, project directories)
- Extract real data: CR number, factory location, certifications, project references
- Locate corporate profile PDF or company logo

### 2. Extract Visual Assets
```python
# Extract images from PDF
import fitz
doc = fitz.open('corporate_profile.pdf')
for i, page in enumerate(doc):
    images = page.get_images()
    for j, img in enumerate(images):
        xref = img[0]
        base = doc.extract_image(xref)
        with open(f'page{i+1}_img{j+1}.{base["ext"]}', 'wb') as f:
            f.write(base['image'])

# Also render pages for reference
pix = page.get_pixmap(dpi=150)
pix.save(f'page{i+1}_render.jpg')
```

### 3. Prepare Embedded Images
Convert selected images to base64 data URIs for self-contained HTML:
```python
import base64
with open('image.jpg', 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()
    data_uri = f'data:image/jpeg;base64,{b64}'
```

### 4. HTML Design Specs
- **Page size**: A4 Landscape — `@page { size: 297mm 210mm landscape; margin: 0; }`
- **Fonts**: Google Fonts via `@import` — Inter for headings, Plus Jakarta Sans for body
- **Colorscheme**: Typically Navy (#1a3a5c) + Gold (#c9a84c) + Warm beige (#f8f6f2)
- **Structure**:
  - 7 pages minimum: Cover, About, Manufacturing, Products, Portfolio, Quality, Why Us
  - Each page: `page-break-after: always`
  - Footer with page number and document title
- **Print button**: Fixed position `onclick="window.print()"` with `.np` (no-print) class
- **Print CSS**: `-webkit-print-color-adjust: exact; print-color-adjust: exact;`

### 5. Image Embedding Strategy
- Build a Python script (`build_profile.py`) with the HTML template
- Load base64 data from a separate `img_data.py` module
- Use string placeholders (`__LOGO__`, `__HERO__`, etc.) and `.replace()` at runtime
- This avoids hitting message size limits and keeps the template editable

### 6. Bilingual Layout (English-Led)
```css
.sec-title { font-size: 28px; font-weight: 800; color: var(--navy); }  /* English */
.sec-title-ar { font-size: 13px; color: var(--gray); margin-bottom: 10px; }  /* Arabic below */
```

### 7. Generating the File
```python
# build_profile.py pattern
import img_data, base64
def uri(name, mime='image/jpeg'):
    return 'data:{};base64,'.format(mime) + base64.b64encode(getattr(img_data, name)).decode()

TM = r'''<html>...__LOGO__...__HERO__...</html>'''
for k, v in {'__LOGO__': LOGO, '__HERO__': HERO}.items():
    TM = TM.replace(k, v)
with open('output.html', 'w') as f:
    f.write(TM)
```

### 8. Verification
- Open in browser and check console for errors (file:// protocol)
- Verify all images load and pages render at correct size
- Print preview to check page breaks and margins

## Content Sections (Technical Proposal variant)

| Section | Content |
|---------|---------|
| 01 — Executive Summary | Company overview, scope of work, differentiators |
| 02 — Company & Legal | CR, factory location, certifications, license checklist |
| 03 — Technical Approach | Methodology phases, production capacity, equipment, zones |
| 04 — Quality & Compliance | ISO certs, SASO/SABER, SBC, material compliance standards |
| 05 — Project Experience | Sector-tagged project table, client logos, key references |
| 06 — HSE & Resources | Safety plan, team structure, full submission checklist |

## Content Sections (Corporate Profile variant)

| Page | Content |
|------|---------|
| 1 — Cover | Logo, company name, tagline, key stats |
| 2 — About | Company overview, vision/mission, data grid |
| 3 — Manufacturing | Production capacity, equipment, factory zones |
| 4 — Products & Services | Product categories, service flow diagram |
| 5 — Portfolio | Project table, sector tags, key clients |
| 6 — Quality | Certifications, compliance, QC flow |
| 7 — Why Us | Differentiators, contact, CTA |

## Pitfalls

- **Surrogate pairs in raw strings**: When using `r'''...'''` in Python, emoji characters like 🏭 generate surrogate pair escape sequences (`\ud83c\udfed`) that cannot be written as UTF-8. Replace all emoji with text alternatives (`[Factory]`) or use proper Unicode escapes (`\U0001F3ED`).
- **Large HTML files**: Embedded base64 images can create 2-3MB files. This is expected and fine for print, but may be slow in browser preview.
- **File:// protocol restrictions**: Google Fonts `@import` works from `file://` in most browsers, but check before delivery.
- **Page overflow**: A4 landscape at 297mm×210mm with `max-height:210mm; overflow:hidden` prevents content spill. Test each page's content fit.
