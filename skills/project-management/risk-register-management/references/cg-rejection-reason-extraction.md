# CG Rejection Reason Extraction — From Approval PDF to Risk Register

## When to Use

- A risk register entry says "Code D" or "Code C" without the CG rejection reason
- A material submittal (MA) or prequalification (PQ) has a status code but no verbatim CG comment recorded
- You need to populate the risk's `cause` and `evidence` columns with the actual CG feedback

## The Pattern

CG rejection reasons live in the **Approval PDF** inside the submittal's folder in Adel Darwish's OneDrive bank. The submittal form itself (the MS/MA cover sheet) only shows the code — the CG Comments section at the bottom has the verbatim reason.

### Step 1: Find the Approval PDF

```
Adel Darwish's files - 01- Execution Documents/08- Material Submittal MA/
  Architectural/01-MOC-Asser-SIC-1A0-MA-0001/
    Approval/001.pdf          ← CG response with comments
```

The Approval subfolder contains the CG-signed PDF with the actual rejection reason. The top-level PDF in the MA folder is the submission form (Samaya's cover sheet) — it shows the code but not the reason.

### Step 2: Extract Text

```bash
cp "/path/to/Approval/001.pdf" /tmp/ma-xxxx-approval.pdf
pdftotext /tmp/ma-xxxx-approval.pdf -
```

### Step 3: Find the CG Comments Section

In the extracted text, look for:

- `CG Comments:` — the section header
- `Rejected` or `Disapproved` — the status keyword
- The actual reason text, typically in garbled encoding after the header

The CG Comments section is usually at the bottom of the first page, after the Contractor's signature block. The text may be garbled by pdftotext (Arabic/English mixed encoding) but the English reason is readable.

### Step 4: Cross-Reference with Underlying PQ

If the MA was rejected, check the **underlying supplier prequalification (PQ)** — it was likely rejected for the same reason. The PQ approval PDF is in the same bank structure:

```
Adel Darwish's files - 01- Execution Documents/08- Material Submittal MA/
  Architectural/01-MOC-Asser-SIC-1A0-MA-0001/
    MOC-Asser-SIM-1A0-PQ-0026/   ← embedded PQ folder
```

The PQ rejection reason often mirrors the MA rejection. In the Aseer Museum case:
- PQ-0026 (EXA supplier): "Rejected — submit 3 options"
- MA-0001 (Porcelain Tiles): "Rejected — submit 3 options for porcelain"

Same root cause: only 1 supplier submitted instead of the required 3.

### Step 5: Update the Risk Register

| Field | What to Write |
|-------|---------------|
| `cause` | "CG rejected R0 (DD-MMM-YYYY, Signatory Name): \"Verbatim CG comment\". Underlying PQ-XXXX also rejected same reason." |
| `evidence` | "MA-XXXX Code D; PQ-XXXX Code D; CG comment: \"Verbatim CG comment\"" |
| `response_action` | Must address the CG's specific requirement (e.g., "Source minimum 3 suppliers" not just "resubmit") |

## Common CG Rejection Reasons (Aseer Museum)

| Reason | Frequency | Typical Fix |
|--------|-----------|-------------|
| "Rejected — submit 3 options" | Common (porcelain, showcases) | Source 3 suppliers, not 1 |
| "Submission found incomplete" | Common | Attach missing docs (NRS review, certificates, MSDS, test reports) |
| "Materials do not comply with specifications" | Common | Verify spec compliance before submission |
| "Anti-reflective glass not in compliance" | Specific to showcases | Provide manufacturer compliance datasheet |
| "Provide three alternative suppliers" | CG standard requirement | Always submit 3 options per material |

## Pitfalls

- **The top-level PDF is the submission form, not the response.** The Approval subfolder has the CG-signed response. Don't waste time extracting the wrong file.
- **pdftotext garbles Arabic/English mixed text.** The CG Comments section may look like random characters. Look for English keywords like "Rejected", "submit", "options", "incomplete" — they survive the encoding.
- **The PQ folder may be embedded inside the MA folder** (not in the PQ section of the bank). Check the MA folder's contents for PQ subfolders.
- **Date on the PDF may be wrong** (off-by-100 year, wrong month). Cross-check against the register log date.
- **Not all MA rejections have a verbatim CG comment** — some only have the code (D) on the cover sheet. In that case, the CG Comments section may be blank. Record what you can and flag the gap.
