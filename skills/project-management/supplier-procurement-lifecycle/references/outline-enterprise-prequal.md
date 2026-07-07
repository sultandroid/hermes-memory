# Example: Outline Enterprise Prequalification (Jun 3, 2026)

## Entity
- Company: Outline Enterprise (أوتلاين للمشاريع)
- Group: Mazeed Investment Group
- Sector: Furniture manufacturing + interior fit-out
- 3 Saudi factories, 8 specialized companies, 25+ years
- CR: 1010642176, Factory: Second Industrial City Riyadh 5000+m²
- ISO 9001:2015 (TCI/EGAC)
- Website: ole.sa | LinkedIn: /company/oleenterprises

## Source Data
- Corporate Profile PDF extracted via pdfplumber (~12K chars)
- Google Drive portfolio: 28+ project folders (NHC, hospitality, govt, healthcare, commercial)
- LinkedIn meta description (most reliable single source)
- Website (ole.sa/ar/)

## Documents Created

| Document | Format | Contents |
|----------|--------|----------|
| PREQUALIFICATION_SUBMISSION_DOCUMENT | MD + DOCX | 8 sections, full submission package |
| FACTORY_PREQUALIFICATION_CHECKLIST | MD + DOCX | 93 items across 11 sections (A-K) |
| COMPANY_CAPABILITY_STATEMENT | MD + DOCX | Profile + stats + projects + services |
| COMPLIANCE_MATRIX_TEMPLATE | MD + DOCX | 104 items across 10 sections |
| preq_overview.html | HTML | Browser dashboard with 8 sections |
| outline_profile_a4_landscape.html | HTML | 7-page A4 landscape print-ready profile |

## Key Design Decisions
- Checklist tailored for MANUFACTURER not subcontractor — includes industrial license, SASO/SABER, production capacity, factory zones, equipment
- HTML profile uses brand colors: Navy #1a3a5c, Gold #c9a84c, Beige #f8f6f2
- A4 landscape @page size: 297mm 210mm for print
- Bilingual Arabic primary + English secondary
- Entity isolation note: "NOT Samaya project"

## Saudi Compliance Items Covered
- CR 1010642176 with industrial classification
- GOSI certificate 6863819
- Factory location + 5000+m² area
- ISO 9001:2015
- Production capacity (200 wardrobes/day, 100 beds/day, 50 living sets/day, 10 kitchens/day)
- 24 reference projects across 6 sectors

## Pitfalls Encountered
- DO NOT use generic subcontractor checklist — reviewers expect factory-specific items
- Corporate profile PDF was image-based in places — needed OCR fallback
- Google Drive without login shows limited data — document what's visible
- LinkedIn meta description is the most reliable single source for company facts
