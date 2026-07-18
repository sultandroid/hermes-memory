# Contract Clause Text Extraction — OneDrive PDFs

When the repo (`aseer-museum-pm/`) doesn't have the literal text of a contract/SoW clause, extract it from the source PDFs in OneDrive.

## Source PDFs

| Document | OneDrive Path | Notes |
|----------|--------------|-------|
| SoW (Scope of Works) | `04_Docs/00_Project_Charter/Contractors Scope of Works Document - Technical_250313/6380_KMS_RPT_PM_AS_00006_Aseer_Contractors_Scope of Work.pdf` | Main scope document, clause 6.22.x |
| ER (Employer's Requirements) | `04_Docs/00_Project_Charter/Contractors Employers Requirements - Engineering_250313/250313_ER Document - Aseer Museum of Arts_R02.pdf` | Engineering requirements |
| Contract | `04_Docs/00_Project_Charter/10003521- عقد.pdf` | Full contract (Arabic) |
| StudioZNA Scope | `04_Docs/00_Project_Charter/Aseer 2026 SCOPE of works 010625_StudioZNA.pdf` | ZNA-specific scope |

## Extraction Steps

```bash
# 0. Check PDF is real (not 0-byte OneDrive placeholder)
ls -la "<pdf_path>"

# 1. Check PDF page count first
pdfinfo "<pdf_path>" | grep -i "pages"

# 2. Extract full text with -layout for better formatting
pdftotext -layout "<pdf_path>" /tmp/sow_text.txt

# 3. Verify completeness — compare line count against page count
#    Rule of thumb: ~40-50 lines per page for text-heavy PDFs
wc -l /tmp/sow_text.txt
#    If line count is suspiciously low (e.g. 358 lines for 72 pages),
#    the extraction was truncated — re-extract with -layout flag

# 4. Search for the clause
grep -n "6\\.22\\.1" /tmp/sow_text.txt

# 5. Read the clause context (adjust offset as needed)
read_file /tmp/sow_text.txt offset=<line> limit=30
```

## Pitfalls

- **OneDrive path may have spaces** — quote the path or use tab-completion to verify
- **PDF may be 0-byte placeholder** — if pdftotext fails, check file size first with `ls -la`
- **Clause numbering in TOC vs body** — the TOC may list the clause at a different page than the body text. Search the full extracted text, not just the TOC section
- **Text may be truncated** — pdftotext can miss text in complex PDF layouts. If a clause seems incomplete, try `pdfminer` as fallback: `python3 -c "from pdfminer.high_level import extract_text; print(extract_text('path.pdf'))"`
- **The repo's `scope_of_work.txt` is a copy** — it may be outdated or OCR-imperfect. Always prefer the original PDF for verbatim text
