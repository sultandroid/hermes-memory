# Standard/Regulatory PDF Extraction Pattern

When extracting content from European/British standards (BS EN, EN, ISO) or similar regulatory PDFs, these patterns recur.

## Detection: Is this a national adoption?

National adoptions (SIST, DIN, BSI, etc.) often differ from the full English original:

| Signal | What it means |
|--------|---------------|
| PDF is encrypted (128-bit RC4) | National adoption — decrypt with `pypdf.PdfReader(path).decrypt('')` |
| Page count is 15 but TOC says 42 | Only front matter + first few clauses are in the file |
| Last page ends mid-sentence | The file is truncated — the full standard is elsewhere |
| Slovenian/German/French title page | National adoption, not the original EN |
| `iTeh STANDARD PREVIEW` watermarks | Preview copy — may be incomplete |

## Extraction workflow

```python
# 1. Check encryption and page count
import pypdf
reader = pypdf.PdfReader(path)
print(f"Encrypted: {reader.is_encrypted}, Pages: {len(reader.pages)}")
if reader.is_encrypted:
    reader.decrypt('')
    print(f"Decrypted, pages: {len(reader.pages)}")

# 2. Get TOC from first few pages
import fitz
doc = fitz.open(path)
toc_text = ""
for i in range(min(6, len(doc))):
    toc_text += doc[i].get_text()
# Look for "Contents" section to find actual page count

# 3. Extract all available text
for i in range(len(doc)):
    text = doc[i].get_text()
    print(f"=== PAGE {i+1} ({len(text)} chars) ===")
    print(text)

# 4. Check if last page is complete
last_page = doc[-1].get_text()
if last_page.strip().endswith(('SIST', 'iTeh', 'https://')):
    print("WARNING: Last page appears to be a watermark/footer — file may be truncated")
```

## Supplementing missing sections

When the PDF is incomplete, use these sources:

1. **ANSI webstore previews** — `webstore.ansi.org/preview-pages/BSI/preview_*.pdf` — often have the TOC, scope, and first few clauses
2. **iTeh standards** — `cdn.standards.iteh.ai/samples/...` — same content as the national adoption
3. **Academic reviews** — MDPI, Elsevier papers that cite the standard often reproduce key tables (temperature bands, RH bands, light levels)
4. **Industry guidance** — English Heritage, Collections Trust, ICOM-CC papers that reference the standard
5. **Collections Trust** — `collectionstrust.org.uk` — concise summaries of what each standard covers

## What to expect from a standard PDF

| Section | Usually present? | Notes |
|---------|-----------------|-------|
| Title page + foreword | Yes | Always in national adoptions |
| Scope (Clause 1) | Yes | |
| Normative references (Clause 2) | Yes | |
| Terms and definitions (Clause 3) | Yes | |
| Principles (Clause 4) | Usually | May be truncated mid-clause |
| Technical specifications (Clauses 5-7) | Often missing | These are the contractor-relevant parts |
| Annexes (informative) | Often missing | Temperature/RH/light tables, pollutant lists, load tables |
| Bibliography | Often missing | |

## Worked example: BS EN 16893:2018

See `/Users/mohamedessa/BS_EN_16893_2018_Extraction.md` for the full extraction from this session.

Key findings:
- The SIST EN 16893:2018 PDF (15 pages, 578 KB) only contains Clauses 1-4.4.2
- Clauses 5 (Building specifications), 6 (Fire protection), 7 (Security), and all 6 annexes are listed in the TOC but absent from the file
- Supplemented with: English Heritage sustainable stores paper, MDPI critical review, ANSI preview, Collections Trust summary, ICON guidance
- The standard does NOT prescribe fixed numerical values — it requires per-collection specification
