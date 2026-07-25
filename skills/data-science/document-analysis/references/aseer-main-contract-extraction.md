# Contract 0010003521 — KSA Government Construction Contract Extraction

## File Locations

| File | Path | Notes |
|------|------|-------|
| Source PDF | `Aseer-Museum/04_Docs/00_Project_Charter/10003521- عقد.pdf` | Primary location |
| Source PDF (copy) | `Aseer-Museum/01_Contracts/01_Main_Contract/10003521- عقد.pdf` | Same file, different folder |
| **Full EN extract** | `Aseer-Museum/01_Contracts/01_Main_Contract/Contract_0010003521_Full_EN.md` | **Complete English extraction (all 9 sections)** |
| **Full AR extract** | `Aseer-Museum/01_Contracts/01_Main_Contract/Contract_0010003521_Full_AR.md` | **Complete Arabic extraction (all 9 sections)** |
| DMP extract (partial) | `Aseer-Museum/04_Docs/02_Plans_and_Procedures/02.1_DMP/02_DMP_Chapters/02_Contractual_Framework.md` | Obligations matrix updated with all 13 articles of §4 |
| Odoo stub (metadata only) | `Aseer-Museum/25_odoo/01_Initiation/عقد مشروع تأهيل وتجهيز العروض المتحفية للمتحف الاقليمي الثالث(عسير).md` | 8 lines, metadata only — NOT a contract extract |

## Contract Structure (9 Sections)

| Section | Arabic | English | Line Start | Line End | Articles |
|---------|--------|---------|-----------|----------|----------|
| 1 | القسم الأول | General Provisions | 582 | 1434 | Definitions, scope, language, force majeure, IP |
| 2 | القسم الثاني | The Site | 1435 | 1744 | Site conditions, access, existing services |
| 3 | القسم الثالث | Government Representative | 1745 | 1828 | PMC role, authority, instructions |
| 4 | القسم الرابع | Contractor's Liabilities | 1829 | 2425 | 13 articles: obligations, liability, HSE, QA, transport, utilities, properties, site, insurance |
| 5 | القسم الخامس | Work Implementation | 2426 | 3524 | Commencement, duration, programme, delays, variations, payment |
| 6 | القسم السادس | Guarantees | 3525 | 3604 | Defects liability period |
| 7 | القسم السابع | Contract Termination | 3605 | 3830 | Termination by employer/mutual, settlement |
| 8 | القسم الثامن | Financial Conditions | 3831 | 4209 | Payment, advances, retention, claims |
| 9 | القسم التاسع | Specifications | 4210 | ~4400+ | Technical specifications, special conditions |

## Section 4 Article Map (Contractor's Responsibilities)

| Art | Arabic | English | Key Content |
|-----|--------|---------|-------------|
| 1 | الالتزامات العامة | General Obligations | 15 sub-clauses (a-o): diligence, Saudization, info sharing, skills, permits, IP, quality/safety |
| 2 | مسؤولية المتعاقد | Contractor's Liability | 3 parts: liability to Government, acknowledgments (15 items), liability to third parties |
| 3 | ممثل المتعاقد في الموقع | Site Representative | Appointment, MoC consent, 15-day replacement, Arabic interpreter |
| 4 | التعاون مع المتعاقدين الآخرين | Cooperation with other Contractors | Coordinate with Government Entity appointees |
| 5 | السلامة والصحة المهنية | Occupational Safety & Health | 3 parts: compliance, compensation, hazard notification |
| 6 | إجراءات السلامة | Safety Measures | 6 sub-clauses (a-f): instructions, person/property safety, lighting/guarding |
| 7 | حماية البيئة | Environmental Protection | Environmental compliance, pollution/noise limits |
| 8 | ضمان الجودة | Quality Assurance | QA plan submission, review, approval |
| 9 | نقل المعدات والمواد | Equipment & Materials Transport | 4 parts: dedicated equipment, national carriers, Saudi ships |
| 10 | الكهرباء والماء والغاز | Utilities | Contractor provides at own expense |
| 11 | ممتلكات الجهة الحكومية | Government Entity Properties | 3 parts: ownership, no replacement, maintenance |
| 12 | موقع العمل | Worksite | 3 parts: boundary limits, site clearance, vacation |
| 13 | التأمين | Insurance | Obtain/maintain insurance, Government verification right |

## Extraction Pattern — Full Contract to Bilingual EN/AR

**User preference: always split bilingual KSA government contracts into separate EN and AR MD files.** Do NOT produce merged bilingual files — the mixed columns are unreadable.

```python
import re

# 1. Extract full text
# pdftotext -layout preserves dual-column format
terminal("pdftotext -layout '/path/to/عقد.pdf' /tmp/contract_full.txt")

# 2. Read in Python (NOT via terminal — stdout cap truncates at ~40KB)
with open('/tmp/contract_full.txt', 'r') as f:
    lines = f.readlines()

# 3. Split each line into EN and AR using Unicode ranges
def split_dual(line):
    """Split dual-column line. Arabic starts where Unicode block \u0600-\u06FF begins."""
    for i, ch in enumerate(line):
        if '\u0600' <= ch <= '\u06FF' or '\u0750' <= ch <= '\u077F' or '\uFB50' <= ch <= '\uFDFF':
            return (line[:i].rstrip(), line[i:].strip())
    return (line.strip(), '')

# 4. Detect sections with regex (flexible spacing)
# Headers have variable spacing: "SECTION         FOUR:        CONTRACTOR'S"
section_re = re.compile(r'SECTION\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE)')

# 5. Detect articles
article_re = re.compile(r'Article\s+(One|Two|Three|...|Forty)', re.IGNORECASE)

# 6. Skip page headers/footers
skip_pats = [
    r'Kingdom of Saudi Arabia', r'Ministry of Culture',
    r'General Construction Contract', r'Restricted\s*-',
    r'اململكة العربية السعودية', r'وزارة الثقافة', r'عقد إنشاءات العامة',
]

# 7. Clean RTL control characters
def clean_ctrl(s):
    return re.sub(r'[\u200B-\u200F\u202A-\u202E\u2066-\u2069\uFEFF]', '', s)
```

## Key Pitfalls

1. **stdout cap truncates large files.** `terminal("cat file")` returns only ~40KB. For 6927-line PDFs, read the file directly with Python `open()`, not via terminal piping. The `execute_code` tool is the right approach.

2. **Variable spacing in section headers.** PDF layout mode inserts variable spaces: `SECTION         FOUR:        CONTRACTOR'S`. Use regex `SECTION\s+FOUR` not exact string match.

3. **RTL control characters bleed into English text.** Arabic bidirectional markers (U+202B RIGHT-TO-LEFT EMBEDDING, etc.) persist after splitting. Always run `clean_ctrl()` to strip `\u200B-\u200F`, `\u202A-\u202E`, `\u2066-\u2069`, `\uFEFF`.

4. **Arabic diacritics/dots missing.** `pdftotext` drops some Arabic dots/diacritics. This is normal — the text is still readable. Do not attempt OCR to "fix" this.

5. **Page breaks as form feeds.** `\f` characters appear at page boundaries in pdftotext output. Filter with `grep -v '^\f'` or strip in Python.

6. **Dual-column split point detection.** The split between English and Arabic columns is at the first Arabic Unicode character. This works reliably for KSA government contracts where English is always on the left.

## DMP Obligations Matrix Update

When full contract text is extracted, update the DMP Chapter 02 obligations matrix (`02_Contractual_Framework.md` section 2.6) with article-level detail. Current state: 13 rows for §4 (Arts 1-13) + 3 rows for key §5 obligations. Each row includes: Art number, Area, Key Requirements (detailed), Source reference.
