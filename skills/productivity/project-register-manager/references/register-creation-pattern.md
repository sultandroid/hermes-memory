# Register Creation Pattern (for projects with partial structure)

When a project has folders but **zero Excel registers** in `Docs/09_Registers/`, create the registers using this exact pattern.

## Python Script Pattern

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from datetime import datetime
import os

ROOT = '/path/to/project'
REG = f'{ROOT}/Docs/09_Registers'
os.makedirs(REG, exist_ok=True)

def make_cover(ws, title, subtitle, project, project_ar, contractor):
    ws.merge_cells('B2:E2')
    ws['B2'] = 'PROJECT REGISTER'
    ws['B2'].font = Font(bold=True, size=14)
    ws.merge_cells('B4:E4')
    ws['B4'] = title
    ws['B4'].font = Font(bold=True, size=18)
    ws.merge_cells('B5:E5')
    ws['B5'] = subtitle
    ws['B5'].font = Font(bold=True, size=14)
    ws['B7'] = 'Project:'
    ws['C7'] = project
    ws['B8'] = 'Project (AR):'
    ws['C8'] = project_ar
    ws['B9'] = 'Project Dir:'
    ws['C9'] = project
    ws['B10'] = 'Contractor:'
    ws['C10'] = contractor
    ws['B13'] = 'REVISION HISTORY'
    ws['B13'].font = Font(bold=True)
    for col, hdr in [('C', 'Rev'), ('D', 'Date'), ('E', 'Description'), ('F', 'Author')]:
        ws[f'{col}13'] = hdr
        ws[f'{col}13'].font = Font(bold=True)
    ws['C14'] = '00'
    ws['D14'] = datetime.now().strftime('%Y-%m-%d')
    ws['E14'] = 'Initial Register Creation'
    ws['F14'] = 'Hermes AI'
    ws['B17'] = 'NOTES'
    ws['B17'].font = Font(bold=True)
    ws['B18'] = 'This register is automatically generated and maintained by Hermes AI.'
    ws['B20'] = 'Last Updated:'
    ws['C20'] = datetime.now().strftime('%Y-%m-%d %H:%M')

def make_header(ws, headers, col_widths):
    ws.append(headers)
    for cell in ws[1]:
        cell.font = Font(bold=True, color='FFFFFF')
        cell.fill = PatternFill('solid', fgColor='2F5496')
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    for i, w in enumerate(col_widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(i)].width = w

# === DRAWING REGISTER ===
wb = openpyxl.Workbook()
ws_cover = wb.active
ws_cover.title = 'Cover'
make_cover(ws_cover, 'Drawing', 'Register', 'PROJECT_NAME', 'اسم المشروع', 'Samaya Investment')
ws = wb.create_sheet('Drawing')
make_header(ws, ['Date', 'Drawing #', 'Title', 'Discipline', 'Scale', 'Sheet Size', 'Rev', 'Status', 'File Path'],
            [12, 12, 45, 15, 10, 10, 6, 12, 60])
# Append drawing rows here...
wb.save(f'{REG}/Drawing_Register.xlsx')

# === SUBMITTAL REGISTER ===
wb = openpyxl.Workbook()
ws_cover = wb.active
ws_cover.title = 'Cover'
make_cover(ws_cover, 'Submittal', 'Register', 'PROJECT_NAME', 'اسم المشروع', 'Samaya Investment')
ws = wb.create_sheet('Submittal')
make_header(ws, ['Date', 'Submittal #', 'Title', 'Type', 'From', 'To', 'Status', 'Due Date', 'File Path', 'Remarks'],
            [12, 14, 45, 18, 20, 20, 12, 12, 55, 35])
# Append submittal rows here...
wb.save(f'{REG}/Submittal_Register.xlsx')

# === STUB REGISTERS (empty templates) ===
stub_registers = ['RFI_Register', 'SI_Register', 'NCR_Register', 'Change_Order_Register',
                  'Material_Register', 'Invoice_Register', 'Meeting_Minutes_Register',
                  'Transmittal_Register', 'Contract_Register', 'Risk_Register',
                  'Subcontractor_Register', 'HSE_Register']
for reg_name in stub_registers:
    path = f'{REG}/{reg_name}.xlsx'
    if os.path.exists(path):
        continue
    wb = openpyxl.Workbook()
    ws_cover = wb.active
    ws_cover.title = 'Cover'
    title = reg_name.replace('_Register', '').replace('_', ' ')
    make_cover(ws_cover, title, 'Register', 'PROJECT_NAME', 'اسم المشروع', 'Samaya Investment')
    short_name = title.replace(' ', '')
    ws = wb.create_sheet(short_name)
    ws.append([''] * 10)
    wb.save(path)
```

## Key Lessons Learned

1. **Deduplicate immediately** — check existing IDs before appending. Duplicate IDs (e.g., `DWG-005` twice) cause confusion and require manual cleanup.
2. **Path prefix must match existing entries** — if existing drawings use `04_Design_Files/...`, new entries must use the same prefix, not `Design Files/...` (different prefix = same file, duplicate entry).
3. **Cover sheet + data sheet** — registers have two sheets: `Cover` (metadata, revision history) and `Drawing`/`Submittal` (data).
4. **Auto-filter on data sheet** — add `ws.auto_filter.ref` for usability.
5. **Submittal's vs Submittals** — some projects use `Submittal's` (with apostrophe). Always use the exact subfolder name found in the project.
6. **Labor CLIs for file enumeration are SLOW** — use `os.walk` Python for scanning. Reserve Claude/Kimi for content analysis.