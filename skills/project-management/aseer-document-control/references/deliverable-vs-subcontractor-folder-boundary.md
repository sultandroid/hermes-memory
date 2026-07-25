# Deliverable Folder vs Subcontractor Folder — Boundary Pattern

When the same subcontractor/specialist produces a plan or deliverable, you end up with two locations. This is correct — keep both but enforce a clear boundary.

## Two-Location Rule

| Role | Plans Folder (`04_Docs/02_Plans_and_Procedures/`) | Subcontractor Folder (`24_Subcontractors/<N>_<name>/`) |
|------|--------------------------------------------------|--------------------------------------------------------|
| Purpose | Technical deliverable archive + project reference library | Subcontractor/consultant relationship management |
| Content | Formal revision history, codes/standards, CG responses, internal analysis | Subcontractor contract, invoices, correspondence, delivered files |
| Audience | Internal team + CG review | Contract management with the subcontractor |

## Standard Subcontractor Subfolder Structure

Every subcontractor folder under `24_Subcontractors/` should follow this pattern:

```
24_Subcontractors/20_Sustainability/
├── 01_Contract/          ← Contract/PO, engagement letter
├── 02_Invoices/          ← Payment docs, invoices
├── 03_Correspondence/    ← Emails, meeting notes, image attachments
├── 04_Deliverables/      ← Subcontractor's delivered files (PDFs, DOCXs)
└── 05_CR_Sheets/         ← CR sheets sent back-and-forth
```

Create with:
```bash
BASE="/path/to/24_Subcontractors/<N>_<name>"
for d in 01_Contract 02_Invoices 03_Correspondence 04_Deliverables 05_CR_Sheets; do
  mkdir -p "$BASE/$d"
done
```

## OneDrive File Handling

- **Do NOT `mv` on OneDrive** — it can corrupt sync propagation. Use `cp` instead; originals can be deleted via the web UI.
- **Write /tmp first, then `cp`** to the OneDrive path if the file is generated.
- **Micro volume sync**: After updating OneDrive, copy the same changes to `/Volumes/MIcro/Work/Aseer-Museum/` if that volume is in use.

## Checking If CR Sheet Comments Were Actually Addressed

When a subcontractor returns a CR sheet claiming all comments are closed, verify by checking the actual DOCX content — not just the CR sheet.

### Procedure

```python
from docx import Document

doc = Document('path/to/submission.docx')
text = '\n'.join([p.text for p in doc.paragraphs])
lower = text.lower()

# Check tables too — many additions are in tables, not paragraphs
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            lower += cell.text.lower() + '\n'

# Verify each CR item
checks = {
    'Example comment': ['keyword1', 'keyword2', 'phrase'],
}
for label, keywords in checks.items():
    found = all(kw.lower() in lower for kw in keywords)
    missing = [k for k in keywords if k.lower() not in lower]
    print(f'{"CLOSED" if found else f"MISSING: {missing}"} | {label}')
```

### Common Pitfalls

- **Table content is NOT in `doc.paragraphs`** — always scan tables too. "Selection Criteria / Rationale" columns often live only in table headers.
- **Search for partial forms** — "3.7.VIII" might be written as "Section 3.7.VIII" or "ER 3.7.VIII". Search for the core reference.
- **Formatting differences** — the CR sheet response says "Appendix-O" but the document has "Appendix O" (without hyphen). Search for the base word.
- **Push-back items should be absent** — if you told the subcontractor NOT to include something (e.g. exhibition strategy), its absence is correct. Don't flag as missing.
