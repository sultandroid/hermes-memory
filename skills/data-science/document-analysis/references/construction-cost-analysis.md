# Construction Cost Analysis — Worked Example

**Context:** Sultan House (Building 210, Al-Firdous) finishing works project.
**Goal:** Extract all financial data from web app + scanned documents, compare estimate vs actual, produce HTML report with interactive charts.

## Pipeline

```
Web App (land210.vercel.app) ──→ Raw Text Dumps
                                       │
Supabase Storage (15 files) ──→ Bulk Download ──→ Scanned PDFs/Images
                                                         │
                                          pdftoppm + tesseract (ara)
                                                         │
                                    Categorized MD Summaries (per doc type)
                                                         │
                                    Cross-Document Reconciliation
                                                         │
                                    Comprehensive HTML Report (Chart.js)
```

## Step 1: Web App Data Extraction

Login to the project tracking app, navigate each section via browser JS console (not snapshot clicks — SPA routing often doesn't respond to accessibility tree clicks):

```javascript
// Navigate sections programmatically
document.querySelectorAll('button').forEach(b => {
  if (b.textContent.trim() === 'SECTION_NAME') b.click();
});

// Extract all visible text
document.body.innerText
```

Save each section as a raw `.txt` file on the Micro volume.

## Step 2: Discover & Download Supabase Files

Find download URLs via browser console — look for `<a>` tags with `href` containing the Supabase storage URL pattern:

```javascript
// Find all download links
document.querySelectorAll('a[href*="supabase.co/storage"]').forEach(a => {
  console.log(a.textContent.trim(), a.href);
});
```

Batch download with curl:

```bash
curl -sL -o "filename.pdf" "https://supabase-url" -w "%{http_code}"
```

Verify all 200s.

## Step 3: OCR Scanned Arabic Documents

Use `pdftoppm` for PDFs (handles scanned/image-based docs better than PyMuPDF for this use case):

```bash
# Convert PDF pages to images
pdftoppm -jpeg -r 300 "document.pdf" /tmp/pages/prefix

# Resize for faster OCR (large images slow tesseract)
convert page.jpg -resize 1200x -quality 75 small.jpg

# OCR with Arabic language pack
tesseract small.jpg stdout -l ara
```

**Key macOS quirk:** `cd /tmp` before running tesseract on files in `/tmp` to avoid `fopenReadStream` errors. Or use Python + pytesseract.

**Multi-pass cross-reference** for difficult scans — run OCR at different contrast levels and intersect results to find consensus text.

## Step 4: Categorize & Structure Output

Group documents by functional type (not file extension):

| Category | Output File |
|----------|-------------|
| Contracts | `contract_summary.md` |
| BOQ/Estimates | `boq_estimate.md` |
| Bank/Account Statements | `account_statements.md` |
| Payment Receipts | `payment_receipts.md` |
| Contractor Quotes | `contractor_quotations.md` |

Each file uses a consistent table format:

```markdown
## Document Title
| Field | Details |
|-------|---------|
| **File** | filename.pdf |
| Size | 147 KB |
| Method | pdftotext / OCR |

### Content
[structured data — tables for financials, bullets for scope, paragraphs for notes]

### Key Values
| Item | Amount |
|------|--------|
| Total | 366,894 EGP |
```

## Step 5: Cross-Document Reconciliation

Compare operational records (web app data) vs formal financial documents (account statements):

| Source | Client Payments | Total Spent | Balance |
|--------|:--------------:|:----------:|:-------:|
| **App records** | 550,000 EGP | 414,585 EGP | +93,957 EGP |
| **Account statements** | 366,894 EGP | 337,305 EGP | -4,142 EGP |

**Reconciliation approach:**
- Identify timing gaps (payments after last statement cutoff)
- Identify scope gaps (items not in original BOQ)
- Flag discrepancies transparently — don't pick one source as "truth"

## Step 6: Estimate vs Actual Comparison

Compare each BOQ line item category against actual spend:

| Category | BOQ Est. | Actual | Variance |
|----------|:--------:|:------:|:--------:|
| Electrical | 109,739 | 131,980 | +20% |
| Internal Plastering | 330,930 | 171,525 | -48% (only 4 of 6 zones done) |

**Critical OCR verification lesson:** Always cross-reference OCR-extracted BOQ totals against the known contract value. In this session, OCR misread Arabic-Indic digits and reported internal plastering as ~52K EGP when the real figure was 331K EGP (6x error). The contract value (632K EGP) should approximately match the sum of all Phase 1 BOQ categories — if it doesn't, the OCR is wrong. Get a clean digital copy (MD, XLSX) as primary source whenever available.

**Key insight:** The BOQ was marked as "minimum cost" — actuals will always exceed it. The value is in identifying **which categories** deviated most and **why** (materials vs labor).

## Step 7: HTML Report with Charts

Build a single-file HTML report with:
- **Cover** — navy/gold, project info, KPIs
- **KPI strip** — contract value, BOQ, actual, paid, balance, completion
- **Bar chart** — estimate vs actual per category (Chart.js)
- **Doughnut chart** — cost distribution
- **Tables** — category comparison with variance bars, payment schedule, contractor breakdown, per-floor plastering
- **Key findings cards** — 5-6 actionable insights
- **Print styles** — `@media print` with `print-color-adjust: exact`

Chart.js CDN: `https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js`

## Common Pitfalls

1. **Vision API not available** — Don't depend on vision_analyze for document reading. Model providers often don't support image input. Fallback: `pdftoppm` + `tesseract` OCR pipeline.
2. **Arabic-Indic digit confusion** — Tesseract frequently confuses ٠١٢٣٤٥٦٧٨٩ with Latin digits. Cross-reference multiple OCR passes. Flag exact figures as "~approximate."
3. **One source of truth doesn't exist** — App data and formal accounting records will disagree. Document both, explain the gap, don't fabricate reconciliation.
4. **Scanned handwriting** — Contractor names, handwritten signatures, and hand-entered amounts are unreliable via OCR. Flag them explicitly.
5. **Multi-page scanned contracts** — Process page by page. Don't batch-OCR 10 pages at once — you lose per-page context.
