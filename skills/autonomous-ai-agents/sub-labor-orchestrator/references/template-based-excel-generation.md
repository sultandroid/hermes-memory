# Template-Based Excel Costing Workbook Generation

Proven pattern (2026-06-09) for creating costing/analysis Excel files across multiple projects following a reference template.

## Use Case

You have a reference Excel template (e.g. `Jabal_Omar_Stores_Costs.xlsx` with 2 sheets) and need to create similar files for N other projects, each with its own source data.

## The Pattern

### 1. Understand the Template Structure

Read the template with openpyxl to understand exact layout:

```python
import openpyxl
wb = openpyxl.load_workbook("template.xlsx", data_only=True)
for name in wb.sheetnames:
    ws = wb[name]
    print(f"Sheet: '{name}' ({ws.max_row}r x {ws.max_column}c)")
```

Key things to detect:
- **Title row** — may not be row 1. The template might have row 5 as title.
- **Header row** — scan for cells containing `البيان` and `المبلغ` to find the real header row.
- **Data starts** — usually 2 rows below headers.
- **Total row** — look for `الإجمالي` in the description column.

### 2. Source Data Types

Projects may have different source data formats:

| Type | Source | Reading Method |
|------|--------|---------------|
| `takaleef` (تكاليف) | `.xlsx` with same Sheet 1 structure | `openpyxl.load_workbook(path, data_only=True)` |
| `legacy_xls` | `.xls` (old Excel) | LibreOffice `soffice --headless --convert-to xlsx`, or `xlrd` |
| `jn_docx` | JN Word docs with factory item tables | `python-docx` — extract table rows with Description/Qty columns |
| `pdf_contracts_only` | PDF contracts/statements | Placeholder workbook only (amounts need PDF extraction) |
| `empty` | No source data | Placeholder workbook with "No source data" note |

### 3. Build the Script

Create a single Python script that:

1. **Defines a PROJECTS map** — `{name: {folder, source_type, source, output}}`
2. **Reads source data** per type
3. **Classifies items into categories** (أرضيات, إضاءة, خشب وأثاث, إلكترونيات, عمالة, etc.) using keyword matching on description
4. **Creates Workbook with 2 sheets**:
   - Sheet 1: Raw items (م | البيان | المبلغ | ملاحظات)
   - Sheet 2: Categorized quotation (م | البيان | وحدة | كمية | سعر الوحدة | الإجمالي | الفواتير الفعلية | أرقام الفواتير)
5. **Saves** beside source data

### 4. Categorization via Keyword Matching

```python
CATEGORIES = [
    ("أرضيات", ['بورسلين', 'سيراميك', 'رخام', 'ارضيات', 'بلاط']),
    ("إضاءة", ['اضاءة', 'لمبة', 'لمبات', 'ليد', 'ترالايت']),
    ("خشب وأثاث", ['خشب', 'اخشاب', 'ملامين', 'ام دي اف', 'mdf', 'رفوف', 'دولاب', 'وحدات عرض', 'shelves', 'display']),
    ("إلكترونيات وأنظمة", ['برنامج', 'جهاز بيع', 'كاشير', 'كاميرا', 'كمبيوتر', 'شاشة', 'انترنت']),
    ("أعمال حديد", ['حديد', 'زوايا حديد', 'استانلس', 'صاج']),
    ("زجاج", ['زجاج', 'قزاز', 'شوكيش', 'سكريت']),
    ("دهانات", ['دهان', 'دهانات', 'بوية', 'فينوماستك']),
    ("ميكانيكا وتكييف", ['مكيف', 'ميكانيكا', 'ستائر هوائية']),
    ("عمالة وتركيب", ['عمالة', 'اجور', 'نقل', 'تركيب', 'ايجار', 'شحن']),
    ("مصنعية", ['shelves', 'display unit', 'unit', 'صناعية']),
]
```

For each item, iterate categories in order — first match wins. Unmatched items go to "متنوعات".

### 5. LibreOffice Conversion for .xls Files

```python
def convert_xls_to_xlsx(path):
    soffice = shutil.which("libreoffice") or shutil.which("soffice") or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    subprocess.run([soffice, "--headless", "--convert-to", "xlsx", "--outdir", str(CONVERTED_DIR), str(path)], check=True)
    return CONVERTED_DIR / (Path(path).stem + ".xlsx")
```

### 6. Validation

After generation, validate each workbook:
- Check Sheet 1 total matches source total (within 1 SAR tolerance)
- Check Sheet 2 has category subtotals and grand total
- Verify all Arabic text renders correctly
- Verify RTL sheet direction

### 7. Known Pitfalls

- **.xls files** — openpyxl cannot read them. Must convert via LibreOffice or use xlrd.
- **OneDrive paths** — Arabic Unicode characters in paths need careful quoting in shell commands.
- **data_only=True** — Always use `data_only=True` when reading source files to get computed values, not formulas.
- **Header detection** — Don't assume headers are on row 1. Scan for `البيان` text.
- **Category collision** — An item matching both "دهانات" (paint) and "عمالة" (labor) keywords → first match wins. Order categories from most specific to most general.
- **Kimi QC timeout** — Kimi may time out on large validation tasks (>30KB files). Use Python validation scripts instead.
