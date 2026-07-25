# Dual-Column Bilingual PDF Extraction

## Source Contract

Contract 0010003521 (Aseer Regional Museum) — bilingual PDF with English left column, Arabic right column.

## Extraction Script Pattern

```python
import re

def clean_ctrl(s):
    """Remove Unicode directional control characters."""
    return re.sub(r'[\u200B-\u200F\u202A-\u202E\u2066-\u2069\uFEFF]', '', s)

def has_arabic(s):
    return bool(re.search(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]', s))

def split_dual(line):
    line = clean_ctrl(line)
    if not line.strip():
        return ('', '')
    for i, ch in enumerate(line):
        if '\u0600' <= ch <= '\u06FF' or '\u0750' <= ch <= '\u077F' or '\uFB50' <= ch <= '\uFDFF' or '\uFE70' <= ch <= '\uFEFF':
            en = line[:i].rstrip()
            ar = line[i:].strip()
            ar = re.sub(r'\.+\s*$', '', ar).strip()
            en = re.sub(r'\s{3,}', '  ', en).strip()
            return (en, ar)
    return (line.strip(), '')
```

## Section Header Detection (Variable Spacing)

PDF headers like `SECTION         FOUR:        CONTRACTOR'S` have 9+ spaces between words.

```python
section_patterns = [
    (re.compile(r'SECTION\s+ONE'), 'Section One', 'القسم الأول'),
    (re.compile(r'SECTION\s+TWO'), 'Section Two', 'القسم الثاني'),
    (re.compile(r'SECTION\s+THREE'), 'Section Three', 'القسم الثالث'),
    (re.compile(r'SECTION\s+FOUR'), 'Section Four', 'القسم الرابع'),
    (re.compile(r'SECTION\s+FIVE'), 'Section Five', 'القسم الخامس'),
    (re.compile(r'SECTION\s+SIX'), 'Section Six', 'القسم السادس'),
    (re.compile(r'SECTION\s+SEVEN'), 'Section Seven', 'القسم السابع'),
    (re.compile(r'SECTION\s+EIGHT'), 'Section Eight', 'القسم الثامن'),
    (re.compile(r'SECTION\s+NINE'), 'Section Nine', 'القسم التاسع'),
]
article_re = re.compile(r'Article\s+(One|Two|Three|...|Forty)', re.IGNORECASE)
```

## Output Files

- `Contract_0010003521_Full_EN.md` — 130K chars, 9 sections, 94 articles
- `Contract_0010003521_Full_AR.md` — 102K chars, 9 sections, 94 articles

## Key Pitfalls

1. **RTL control characters** — `\u200B-\u202E` and `\u2066-\u2069` are invisible but corrupt English text. Always strip first.
2. **stdout cap** — `terminal("cat largefile")` truncates at ~50KB. Use Python `open()` for files >3000 lines.
3. **Variable spacing in headers** — use `\s+` not literal spaces.
4. **Trailing dots** — Arabic text often ends with `......` from PDF layout. Strip with regex.
5. **Page headers/footers** — "Kingdom of Saudi Arabia", "Ministry of Culture" appear on every page. Filter.
6. **Article title wrapping** — titles may span two lines. Detect on first line, skip continuation.
