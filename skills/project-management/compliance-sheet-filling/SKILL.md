---
name: compliance-sheet-filling
description: Fill Engineer-provided compliance sheets (Excel) with material data, achieved values, evidence references, and compliance status. Covers reading the Engineer's format, extracting values from datasheets, mapping spec requirements, and writing plain-language entries.
---

# Filling Engineer-Provided Compliance Sheets

## When to use
The Engineer has sent their own compliance sheet format (Excel) with spec clauses already written. They want it filled with actual achieved values from datasheets, not a new sheet you created.

## Steps

### 1. Read the Engineer's format
- Open the Excel file and understand the column structure
- Typical columns: No., Section, Specifications, Manufacturer/Supplier Statement, Compliance, Remarks
- Note merged cells — they affect which cells to write to
- Identify which rows have spec content (col E) vs headers/section titles

### 2. Gather all datasheets
- List all PDFs in the submission folder
- Extract text from PDFs using `pdftotext` or Python
- For image-based PDFs (no extractable text), delegate to a subagent with vision/OCR capability
- Build a table of: Manufacturer | Product | Parameter | Achieved Value | Test Standard | Source File

### 3. Map spec requirements to achieved values
- For each spec clause with a numerical requirement (density, MOR, MOE, thickness, fire rating, etc.)
- Find the matching achieved value from datasheets
- Compare: does the achieved value meet the spec requirement?

### 4. Fill ONLY substantive rows — NEVER fill headers, labels, or section titles
Engineers do not fill "Compliant" next to "PART 1 - GENERAL" or "2.5 MATERIALS" or "4. Properties". Before writing ANY value, decide: is this row a real spec clause that needs a response, or is it a heading/label? If heading/label — leave it EMPTY.

Rows that NEED filling: spec clauses with measurable requirements (density, MOR, fire rating, BHMA grade, EN classification, etc.) and submittal requirements (Product Data, Product Certificates, Shop Drawings).

Rows to LEAVE EMPTY: section headers (PART 1, PART 2, 2.5 MATERIALS, 3.2 INSTALLATION), clause headings (RELATED DOCUMENTS, SUMMARY, QUALITY ASSURANCE), property labels (Properties:, a. Scientific Name), and general administrative clauses (Delivery & Storage, Coordination, generic "noted" or "acknowledged" items).

- **Manufacturer/Supplier Statement** (col O): State the product name and achieved value with test standard. Example: "Verdo FR MDF: 800.80 kg/m3 per ASTM D1037-12(2020)."
- **Compliance** (col W): Use plain words only — "Compliant", "Partial", "Pending". No symbols (no ✓, △, —).
- **Remarks** (col Y): Reference the specific source file and value. Example: "TDS FR MDF E0 NAUF CARB P2 -B.pdf - Density 800.80 kg/m3"

### 4a. Data availability check before filling
Before writing any values: list every datasheet available, extract key values, compare against spec requirements, and report gaps to the user. Ask: "All data available? Do we have everything we need?" Do not start filling until the user confirms the data coverage is sufficient.

### 4b. Shop drawing rows
If a shop drawing has been submitted, mark it "Compliant" — not "Partial" or "to be reviewed by Engineer". The Engineer's review happens on the drawing itself, not on the compliance sheet. Just note where it is filed.

### 4c. File naming convention for datasheets
Rename all datasheets to clean English names before referencing in compliance sheets:
- `Verdo_FR_MDF_TDS.pdf` (not `TDS FR MDF E0 NAUF CARB P2 -B.pdf`)
- `Ritver_PB209IT_FR_PU_Sealer_TDS.pdf` (not Arabic or original long names)
- Pattern: `Manufacturer_Product_KeySpec_Type.pdf`
After renaming, run a find-replace across the compliance sheets to update all Remarks references to the new filenames. Use `openpyxl` to search col O and col Y for old names and replace them.

### 5. Language rules (strict)
- No symbols: use "Compliant" not "✓", "Partial" not "△", "Pending" not "—"
- No AI jargon: no "robust", "comprehensive", "streamlined", "leveraged", "well within limit", "exceeds minimum by X%"
- Plain engineer speak: "Exceeds minimum", "Within spec range", "To be confirmed"
- No AI fingerprints: no em-dashes, smart quotes, section symbols, accented characters
- User may ask to fill only material data, only company data, or all rows — confirm before filling. When they say \"all\", still skip section headers/labels as per rule 4 above

### 6. Evidence in Remarks
Every filled row must have a source file reference in Remarks:
- File name + specific value found
- Example: "VERDO FR CLASS B (1).pdf - FSI 35, SDI 20"
- For Partial items, state what is missing and what is needed to close the gap

### 7. Common pitfalls
- **Do not create a new compliance sheet** — fill the Engineer's existing format
- **Do not copy old data** from previous submissions without verifying against current datasheets
- **Do not use symbols** in Compliance column — the Engineer may use their own symbols in review
- **Do not fill company data** unless the Engineer's sheet explicitly has rows for it. Company data = fabricator qualifications, installer experience, warranty clauses, installation tolerances, submittal procedural items. Material data = MDF properties, fire test results, hardware specs, adhesive specs. When in doubt, confirm with the user. NOTE: the user may toggle between \"materials only\" and \"all substantive rows\" — if they say \"fill all\" or \"fill company data\", fill both material AND company rows but still skip section headers/labels. Do not assume the last instruction from a previous session still applies — ask if unclear.
- **Do not remove signature rows** at the bottom of the sheet
- **Do not delete supporting datasheets** — the Engineer may want to cross-reference
- **Do not fill every row when the user says "all"** — the user means "all SPEC CLAUSE rows", not section headers, labels, and administrative filler. "All" = all substantive rows, not literally every row with text. If you fill section headers with "Compliant", the sheet looks amateur. Filter: is this row a numbered spec requirement or a heading?
- **"Fill company data / no fill company data"** — the user may toggle this. Before clearing company rows in bulk, check: are you also clearing evidence in material rows? If using a batch clear, target only the company rows — do not iterate all filled rows with a single clear operation.
- **When clearing company rows, do not accidentally clear evidence from material rows** — if you batch-clear columns, only target the company-specific rows, not all rows
- **Fire test compliance**: If the product is Class B but spec requires Class A, check if the spec has an alternative acceptance clause (e.g., BS 476 Class 0). Document both the gap and the alternative path.
- **MAR review PDF is a goldmine**: The Engineer's Code C review often contains all the datasheets, certificates, and compliance sheets embedded as pages. Extract them before discarding the review file. Typical page ranges: pages 7-250 = datasheets and product catalogs, pages 279-298 = legal certificates (ISO, CR, VAT, GOSI, Saudization), page 310 = SASO compliance statement. Use `pymupdf` to extract pages as images or individual PDFs.
- **Timber spec values for Douglas Fir (061000 2.1.B.4)**: Density 512 kg/m³, Hardness 3,160 N, MOE 1,357 kg/mm². These are BS EN 942 structural grade values, not generic averages. The Wood Database (wood-database.com) has published averages that are close but lower — a proper supplier TDS is needed to confirm the specific grade. If no supplier TDS is available, reference the Wood Database and mark as Partial with a note.
- **Confirm before bulk-deleting**: When the user says "remove ola paper" or "remove what unneeded", list exactly which files/folders you will delete BEFORE executing. "Remove datasheets" and "remove the team's original submission folder" are different things. If the user corrects themselves later ("no we need ola paper also"), you can recover from the MAR PDF if available. When in doubt, move files to a temp location rather than deleting.
- **Shop drawing = Compliant**: If a shop drawing was submitted with the package, mark the shop drawing rows "Compliant" — not "Partial / to be reviewed by Engineer". The Engineer reviews the drawing itself. The compliance sheet just records that it was provided.

### 8. Rev02 folder organization
When preparing a revision submission (Rev02, Rev03, etc.):
```
Rev02/
├── 064023 - INTERIOR ARCHITECTURAL WOODWORK.xlsx   ← filled Engineer's format
├── 061000 - ROUGH CARPENTRY.xlsx                    ← filled Engineer's format
├── certificates/                                     ← ISO, CR, VAT, GOSI, Saudization
├── Data sheet/                                       ← all manufacturer TDS + test reports
│   ├── Verdo_FR_MDF_TDS.pdf
│   ├── Verdo_FR_MDF_Grade_130_Test_Report.pdf
│   ├── Ritver_PB209IT_FR_PU_Sealer_TDS.pdf
│   └── ... (all datasheets with clean English names)
└── Shop Drawing/
    └── Outline_Enterprise_KKIA_Shop_Drawing.pdf
```
- Keep compliance sheets at Rev02 root, not in subfolders
- Rename all datasheets to clean English names (no Arabic, no spaces)
- Category reference: MDF → `MDF FR/`, PU coatings → `Paint/Pu Painting/`, Hardware → `Hardware/`, SS → `Steel/`, Adhesives → `Adhesives/`, Plywood → `Plywood/`
- After finalizing, copy datasheets back to `Samaya/Assetes/Datasheets/` distributed into the correct category subfolder for future project reuse
- Update Remarks in compliance sheets to reference the new filenames after renaming

### 9. Parallel subagent for image-based PDFs
When multiple image-based PDFs cannot be read by pdftotext (scanned certificates, test reports):
- Delegate them to a subagent (Kimi) as a batch with `delegate_task(tasks=[...])`
- Subagent uses PyMuPDF + OCR to extract content
- Provide exact file paths and specific questions for each PDF
- Use returned values to fill compliance sheets

### 10. Generate partial items list for procurement
After filling, extract all Partial items into a simple numbered list for the procurement team to chase suppliers:
- Format: `1. [what is needed] - [from whom]`
- No headers, no descriptions, no "From:" lines — just the numbered items
- Save as `PARTIAL_ITEMS_SUPPLIER_DOCS_NEEDED.txt` in the Rev0X folder
- Open the file for the user

### 11. Verification
After filling, verify:
- Every material spec row has a Manufacturer Statement
- Every filled row has a Compliance status
- Every filled row has an Evidence reference in Remarks
- Signature rows at the bottom are intact
- No symbols in Compliance column
- No AI-sounding language
- Section headers and labels are EMPTY — not filled with "Compliant"
- File references in Remarks match the actual filenames in Data sheet/
