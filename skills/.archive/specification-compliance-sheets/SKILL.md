---
name: specification-compliance-sheets
description: Fill Engineer-provided compliance sheets for construction material submittals. Map spec clauses to achieved values from manufacturer datasheets, mark compliance status, and reference source documents.
tags: [compliance, submittal, material-approval, specification, construction]
---

# Specification Compliance Sheets

Fill Engineer-provided Excel compliance sheets for material submittals (woodwork, finishes, joinery, etc.).

## Workflow

0. **Check if Engineer provided their own format**
   - Look for Excel files named like `064023 - INTERIOR ARCHITECTURAL WOODWORK.xlsx` or `061000 - ROUGH CARPENTRY.xlsx` in the submission folder
   - If the Engineer provided their own format, FILL THAT ONE — do not create a new compliance sheet
   - The Engineer's format already has the spec text embedded; only fill the response columns (Manufacturer Statement, Compliance, Remarks)

1. **Read the Engineer's format first**
   - Open the Engineer's Excel file
   - Identify columns: Spec clause, Manufacturer Statement, Compliance, Remarks
   - Note merged cells — write to the correct merged range, not individual cells
   - Preserve header rows, signature rows, and formatting

2. **Inventory available evidence**
   - List all datasheets, test reports, certificates in the submission folder
   - For each spec clause, find the matching evidence
   - If a PDF is image-based (no extractable text), use pdftotext first, then PyMuPDF + OCR

3. **Fill Manufacturer/Supplier Statement with actual values**
   - Write the achieved value, test standard, and source file
   - Example: "Verdo FR MDF: 800.80 kg/m3 per ASTM D1037-12(2020)."
   - Never write "Compliant" without the actual number

4. **Mark Compliance using plain words only**
   - Use: `Compliant`, `Partial`, `Pending`
   - NEVER use symbols: no ✓, △, —, ✗, ✔
   - NEVER use AI jargon: no "exceeds minimum by 20%", "well within limit", "standard industry practice"
   - Write plain engineer language: "Exceeds minimum of 0.55 N/mm2", "Within spec range"

5. **Add Remarks with source reference**
   - Reference the exact file path or folder
   - Explain why Partial or Pending — what is missing and how to close it

6. **Preserve the original file**
   - Do not delete or modify spec text already in the Engineer's sheet
   - Do not overwrite signature rows, header info, or formatting
   - Only fill the empty columns (Manufacturer Statement, Compliance, Remarks)

## Common Gaps to Flag

| Gap Type | How to Document |
|----------|----------------|
| Fire test standard mismatch (ASTM vs EN) | Note the alternative acceptance clause in the spec (e.g. 2.6.C.1 accepts BS 476 Class 0) |
| Manufacturer declaration needed | Mark Partial and state: "Manufacturer declaration to be obtained from [supplier]" |
| TBC at shop drawing stage | Mark Pending and state: "To be confirmed per approved shop drawings" |
| Product not relevant to scope | Exclude from the sheet entirely |

## Pitfalls

- Merged cells in Engineer's Excel — writing to a merged cell's top-left corner fills the whole range, but writing to a different cell in the range may not work. Always write to the top-left cell of the merged range.
- Image-based PDFs (scanned documents) — use pdftotext first, then PyMuPDF to extract images, then tesseract OCR. Some PDFs have hidden text layers that pdftotext can extract even when the visual is image-based.
- Signature rows at the bottom of the sheet — do not overwrite them. Check the last rows before writing.
- The Engineer's format may have the full spec text already embedded. Do not add or change it — only fill the response columns.
