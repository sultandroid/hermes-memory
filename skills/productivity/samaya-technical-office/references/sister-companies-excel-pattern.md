# Sister Companies Excel Build Pattern (openpyxl)

## Critical: Column Header Helper

**NEVER do this** (scatters headers across rows):
```python
for ci, h in enumerate(headers, 1):
    ws.cell(row=r, column=ci, value=h).font = wf
    ws.cell(row=r, column=ci).fill = navy
    r += 1  # BUG! Each column on new row
```

**ALWAYS do this** (all headers on ONE row):
```python
def hdr(ws, r, cols):
    """Write all column headers on row r. Returns nothing — caller does r+=1."""
    for ci, h in enumerate(cols, 1):
        c = ws.cell(row=r, column=ci, value=h)
        c.font = wf
        c.fill = navy
        c.alignment = Alignment(horizontal="center", wrap_text=True)

# Usage:
r += 1  # section header
hdr(ws, r, ["#", "", "", "النوع", "المبلغ", "التصنيف", "البيان"])
r += 1  # ONE increment AFTER the call
```

## Complete Build Template

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

# Constants
TARGET = 600674; AREA = 173
navy = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
wf = Font(bold=True, color="FFFFFF", size=10)
sub = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")

# Helper
def hdr(ws, r, cols):
    for ci, h in enumerate(cols, 1):
        c = ws.cell(row=r, column=ci, value=h)
        c.font = wf; c.fill = navy; c.alignment = Alignment(horizontal="center", wrap_text=True)

# Workbook
wb = openpyxl.Workbook(); ws = wb.active; ws.title = "Project Name"
ws.sheet_view.rightToLeft = True

# Header
ws.merge_cells('A1:G1'); ws['A1'] = "Title"; ws['A1'].font = Font(bold=True, size=14, color="1E293B")
ws.merge_cells('A2:G2'); ws['A2'] = "Subtitle"; ws['A2'].font = Font(italic=True, size=10, color="666666")

r = 4

# === SECTION 1: ACCOUNTING ===
ws.cell(row=r, column=1, value="1 — كشف الحساب المحاسبي").font = Font(bold=True, size=12, color="1E293B")
r += 1
hdr(ws, r, ["#", "الرقم", "", "النوع", "المبلغ", "التصنيف", "البيان"])
r += 1
ds = r  # data start
for i, (num, desc, cat, amt, typ) in enumerate(items):
    ws.cell(row=r, column=1, value=i+1).alignment = Alignment(horizontal="center")
    ws.cell(row=r, column=2, value=num)
    ws.cell(row=r, column=4, value=typ)
    ws.cell(row=r, column=5, value=amt).number_format = '#,##0.00'
    ws.cell(row=r, column=6, value=cat)
    ws.cell(row=r, column=7, value=desc)
    r += 1

ws.cell(row=r, column=5, value=f"=SUM(E{ds}:E{r-1})").font = Font(bold=True)
ws.cell(row=r, column=5).number_format = '#,##0.00'
gt_r = r; r += 1

# === SECTIONS 2 & 3: MOVED/RECEIVED ===
ws.cell(row=r, column=1, value="2 — بنود محولة: لا توجد").font = Font(bold=True, size=11, color="1E293B")
ws.cell(row=r, column=4, value=0).number_format = '#,##0.00'
out_r = r; r += 1

ws.cell(row=r, column=1, value=f"3 — بنود مستلمة: من ... {incoming:,}").font = Font(bold=True, size=11, color="1E293B")
ws.cell(row=r, column=4, value=incoming).number_format = '#,##0.00'
in_r = r; r += 1

# === ACCT TOTAL ===
ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4)
ws.cell(row=r, column=1, value="الاجمالي المحاسبي").font = Font(bold=True, size=14, color="1E293B")
ws.cell(row=r, column=5, value=f"=E{gt_r}-D{out_r}+D{in_r}").font = Font(bold=True, size=14, color="1E293B")
ws.cell(row=r, column=5).number_format = '#,##0.00'
ws.cell(row=r, column=1).fill = navy; ws.cell(row=r, column=5).fill = navy
ws.cell(row=r, column=1).font = Font(bold=True, color="FFFFFF", size=13)
ws.cell(row=r, column=5).font = Font(bold=True, color="FFFFFF", size=14)
acct_r = r; r += 1

# === SECTION 4: TYPES ===
ws.cell(row=r, column=1, value=f"4 — انشاءات").font = Font(size=10)
ws.cell(row=r, column=5, value=f"=E{acct_r}").number_format = '#,##0.00'
r += 1

# === SECTION 5: FACTORY ===
ws.cell(row=r, column=1, value="5 — تكاليف المصنع").font = Font(bold=True, size=12, color="1E293B")
r += 1
hdr(ws, r, ["", "", "", "المبلغ", "", "", "البيان"])
r += 1
fs = r
ws.cell(row=r, column=1, value=1); ws.cell(row=r, column=4, value=labor).number_format = '#,##0.00'
ws.cell(row=r, column=7, value="عمالة المصنع"); r += 1
ws.cell(row=r, column=1, value=2); ws.cell(row=r, column=4, value=materials).number_format = '#,##0.00'
ws.cell(row=r, column=7, value="مواد خام المصنع"); r += 1
ws.cell(row=r, column=1, value=3); ws.cell(row=r, column=4, value=others).number_format = '#,##0.00'
ws.cell(row=r, column=7, value="اخرى - لوجستيك/نقل/تعهيد"); r += 1
ws.cell(row=r, column=1, value="اجمالي المصنع").font = Font(bold=True)
ws.cell(row=r, column=4, value=f"=SUM(D{fs}:D{r-1})").font = Font(bold=True)
ws.cell(row=r, column=4).number_format = '#,##0.00'
fc_r = r; r += 1

# === SECTION 6: FINAL ===
ws.cell(row=r, column=1, value="6 — الاجمالي النهائي").font = Font(bold=True, size=12, color="1E293B")
r += 1
hdr(ws, r, ["", "", "", "المبلغ", "نسبة", "", "البيان"])
r += 1
ws.cell(row=r, column=1, value=1); ws.cell(row=r, column=4, value=f"=E{acct_r}").number_format = '#,##0.00'
ws.cell(row=r, column=7, value="الاجمالي المحاسبي"); s1 = r; r += 1
ws.cell(row=r, column=1, value=2); ws.cell(row=r, column=4, value=f"=D{fc_r}").number_format = '#,##0.00'
ws.cell(row=r, column=7, value="تكاليف المصنع"); s2 = r; r += 1
ws.cell(row=r, column=1, value=3); ws.cell(row=r, column=4, value=f"=D{s1}+D{s2}").font = Font(bold=True)
ws.cell(row=r, column=4).number_format = '#,##0.00'
ws.cell(row=r, column=7, value="المجموع قبل الاشراف")
ws.cell(row=r, column=1).fill = sub; ws.cell(row=r, column=4).fill = sub; st = r; r += 1
ws.cell(row=r, column=1, value=4); ws.cell(row=r, column=4, value=f"=D{st}*0.1").number_format = '#,##0.00'
ws.cell(row=r, column=5, value="10%"); ws.cell(row=r, column=7, value="الاشراف الهندسي"); sr = r; r += 1

ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=3)
ws.cell(row=r, column=1, value="FINAL GRAND TOTAL")
ws.cell(row=r, column=1).font = Font(bold=True, size=13, color="FFFFFF")
ws.cell(row=r, column=4, value=f"=D{st}+D{sr}").font = Font(bold=True, size=15, color="FFFFFF")
ws.cell(row=r, column=4).number_format = '#,##0.00'
ws.cell(row=r, column=1).fill = navy; ws.cell(row=r, column=4).fill = navy
ft = r

# SAR/m² header row
ws.cell(row=3, column=2, value='محاسبي/m2').font = Font(bold=True, size=9, color='666666')
ws.cell(row=3, column=3, value=f'=E{acct_r}/{AREA}').number_format = '#,##0.00'
ws.cell(row=3, column=4, value='مصنع/m2').font = Font(bold=True, size=9, color='666666')
ws.cell(row=3, column=5, value=f'=D{fc_r}/{AREA}').number_format = '#,##0.00'
ws.cell(row=3, column=6, value='النهائي/m2').font = Font(bold=True, size=11)
ws.cell(row=3, column=7, value=f'=D{ft}/{AREA}').number_format = '#,##0.00'
ws.cell(row=3, column=7).font = Font(bold=True, size=14, color='1E293B')

# Column widths
for i, w in enumerate([6, 10, 14, 22, 14, 24, 55], 1):
    ws.column_dimensions[get_column_letter(i)].width = w

wb.save(path); wb.close()
```

## Target Formula

```
factory_needed = round(TARGET / 1.1 - acct_net, 2)
labor = round(factory_needed * 0.35, 0)  # 35%
materials = round(factory_needed * 0.45, 0)  # 45%
others = round(factory_needed - labor - materials, 2)  # remainder
```

Verify: `(acct_net + factory_needed) * 1.1 == TARGET`

## Pitfalls

1. **Never `delete_rows()` on formula sheets** — corrupts all =REF references silently
2. **Never `insert_rows()` on formula sheets** — same corruption
3. **Never put `r += 1` inside header loop** — scatters across rows
4. **Always rebuild from scratch** rather than patching
5. **Close file before opening with openpyxl** — `AttributeError: MergedCell` means cell is merged
6. **Use `hdr()` function** for all column headers — consistency
7. **Never find factory rows by matching "1"/"2"/"3" in column A globally** — accounting items ALSO start with 1,2,3. Match against section context (check column G for "عمالة المصنع" or find rows relative to "تكاليف المصنع" section header). When updating existing files, rebuild from scratch instead of patching.
8. **No duplicate items across projects**: Equipment items (#74,#8,#9,#77 in Qahwatna) must NOT be repeated in Hira's construction at any share. Each item# appears in exactly one project's construction/main sheet. Shared items split by area (16.3% + 83.7% = 100%). Equipment tab items belong to ONE project.
9. **Compact sections**: Sections with "لا توجد" = ONE row: `"2 — بنود محولة: لا توجد | 0"`. No separate column header row, no blank rows.
10. **Source files**: Always read from the original Ibrahim email files (`.xls` with xlrd, specific sheets like Sheet2), never from previously restructured `.xlsx` copies. User may delete intermediate files.
11. **"مهمل" → "محول من"**: Never write "مهمل" (neglected). Use "محول من (source)" (transferred from) for items moved between projects.
12. **Row 3 SAR/m²**: Do NOT merge cells for row 3. Write labels and formula references directly into individual cells (columns 2-7). Merging row 3 blocks later writes.
13. **Area-split shared museum+store**: When a store is inside a museum (e.g., 173 m² store inside 1,325 m² museum), items mentioning both \"معرض ومتجر\" are shared and split by area percentage. Items mentioning only \"متجر\" stay at 100%. Add a merged-row note below accounting explaining the split.
