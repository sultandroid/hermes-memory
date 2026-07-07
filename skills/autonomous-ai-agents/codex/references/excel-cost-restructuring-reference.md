# Excel Cost Data Restructuring — Complete Workflow Reference

## Overview

Restructuring raw accounting/costing Excel files into standardized, classified, formula-based workbooks. Used for Samaya sister companies' cost data from accounting invoices (Ibrahim Shaban files) and factory cost records (FCA).

## Phase 0: Audit & Plan

1. List all project folders under the Sister_Companies directory
2. For each folder, identify: raw costing files (.xlsx), Factory_Cost_Analysis files, bank statements (.xls)
3. Check the _Management/Sister_Companies_Management_Reference.xlsx for: project names, locations, areas, budgets, JN numbers
4. Create a task plan with phases: Item Types → Restructure Raw Files → Formula Cleanup → Equipment Separation → Dashboard

## Phase 1: Read & Extract Raw Data

For .xlsx files: use `openpyxl.load_workbook(path, data_only=False)`
For .xls files: use `xlrd.open_workbook(path)` (old Excel format)

Extract: item #, description, amount, existing category/notes
Identify the total row (الإجمالي, TOTAL, Grand Total)

## Phase 2: Classify & Group

### Add Category Column
Map items to categories via Arabic keyword matching:

```python
categories = {
    'خشب|نجارة|اخشاب': 'أخشاب ونجارة (Wood & Carpentry)',
    'دهان|بوية|رستيك|دهانات': 'دهانات وتشطيبات (Paint & Finishing)',
    'حديد|ستيل|زاوية|صاج|حدادة': 'أعمال معدنية وحدادة (Metal Works)',
    'كهرباء|لمبة|ليد|كيبل|قاطع': 'كهرباء وإضاءة (Electrical & Lighting)',
    'زجاج|اكريليك': 'زجاج وأكريليك (Glass & Acrylic)',
    'شحن|نقل|مواصلات|توصيل': 'نقل ولوجستيك (Transport & Logistics)',
    'عمال|اجور|عمالة': 'عمالة (Labor)',
    'ميكانيكا|تكييف|مكافحة حريق|سباكة': 'ميكانيكا وتكييف (MEP / Mechanical)',
    'سفر|تذكرة|فندق|سكن': 'سفر وإقامة (Travel & Accommodation)',
    'قرطاسية|طباعة|ورق': 'قرطاطية ومطبوعات (Office Supplies)',
    'مواد|مستلزمات': 'مواد ومستلزمات (Materials & Supplies)',
    'معدات|جهاز|ماكينة|شاشة|كاميرا': 'معدات وتجهيزات (Equipment)',
}
```

### Group by Category
- Sort items by category
- Add bold category header row before each group
- Add `▶` prefix to category headers
- Add subtotal row after each group with `=SUM(range)` formula
- Renumber items sequentially within each group

## Phase 3: Add Item Types

Add column with header `نوع البند (Item Type)`.

Classification keywords (see SKILL.md for full table):
- **Construction**: مواد بناء, عمالة, تركيب, خشب, حديد, دهان, جبس, ميكانيكا, كهرباء (wiring), سباكة
- **Equipment**: جهاز, شاشة, كاميرا, كمبيوتر, طابعة, ماكينة, ليد, كيبل (cable supply), مكيف
- **Operations**: سفر, تذكرة, اكل, عشاء, قرطاسية, بنك, تأمين, رسوم, صيانة, ايجار

### Item Type Subtotals
Add section after all items:
```
إجمالي الإنشاءات (Total Construction): =SUMIF(item_type_range,"*Construction*",amount_range)
إجمالي المعدات (Total Equipment):     =SUMIF(item_type_range,"*Equipment*",amount_range)
إجمالي التشغيلية (Total Operations):  =SUMIF(item_type_range,"*Operations*",amount_range)
```

## Phase 4: Cross-Project Reallocation

### Identify Misclassified Items
Search descriptions for other store names:
- تذكارات → Tzkarat Store (09)
- رطيب / تمور → Rateeb Store (10)
- مركز الزوار → Hera Visitor Center (13)
- هدايا طيبة → Al Wahi Gift Shop (01)
- خير الخلق / الخلق العظيم → Khair Al-Khalq Museum (07)
- القران الكريم → Holy Quran Museum (02)
- جبل النور → Al Wahi area
- كبار الزوار → Jabal Omar VIP Stores (05)
- قهوتنا / قهوة → Coffee shops (03, 08, 11)

### Split Methods
- **Area-based**: cost × (store_area / total_area_of_involved_stores)
- **Equal**: cost / number_of_stores
- **Full transfer**: entire amount to one store

### Document in BOTH Source and Target Files
- Source file: mark item as outgoing with destination
- Target file: add incoming item with origin
- Add `Reallocation_Log` sheet to each Factory_Cost_Analysis.xlsx

## Phase 5: Add Factory Cost + Supervision

### Read from Factory_Cost_Analysis.xlsx
- Open the store's FCA file
- From `Factory_Work` sheet: get Factory Labor + Factory Materials (POs)
- From `Cost_Register`: get reallocated costs if applicable

### Append to Restructured File
```
=== FACTORY COST ===
Raw Materials (POs):     [amount or =cell_ref]
Factory Labor:          [amount or =cell_ref]
Subtotal Factory:       =SUM(raw_materials, factory_labor) [FORMULA]

=== GRAND TOTAL SUMMARY ===
Accounting Total (after reallocations):  [cell_ref to accounting total]
Factory Cost:                            [cell_ref to factory subtotal]
Subtotal:                                =accounting + factory [FORMULA]
Supervision (10%):                       =subtotal * 0.1 [FORMULA — ON FULL TOTAL]
Grand Total:                             =subtotal + supervision [FORMULA]
```

## Phase 6: Equipment/Operations Separation

After all items are classified with item types:

1. Filter items where Item Type = Equipment or Operations
2. Create new sheet `معدات (Equipment)` with these items + header + SUM total
3. Create new sheet `تشغيلية (Operations)` with these items + header + SUM total
4. Remove Equipment/Operations rows from the main sheet
5. Recalculate main sheet totals as Construction-only
6. Add note: "Non-construction items moved to separate sheets for independent invoicing"
7. If no items of a type exist, create sheet with note "لا توجد عناصر (No items)"

## Phase 7: Build Master Dashboard

Create `_Management/Stores_Coffee_Shops_Dashboard.xlsx` with:

**Sheet 1: Construction Costs Summary**
| Code | Project | Location | Area | Const. Accounting | Factory Cost | Subtotal | Supervision 10% | Grand Total | SAR/m² |

**Sheet 2: Non-Construction (Future Invoicing)**
| Project | Equipment SAR | Operations SAR | Non-Const. Total | Sheets Ready | Status |

## File Naming Convention
- Main costing file: keeps original Arabic name
- Factory Cost Analysis: `{Store_Code}_{Store_Name}_Factory_Cost_Analysis.xlsx`
- Backups: save as `- Original.xlsx` or in `_Backups/` folder

## Common Pitfalls
1. **Tilde expansion**: Use full path `/Users/...` not `~/...` in openpyxl
2. **data_only=True vs data_only=False**: When reading programmatically-created files, `data_only=True` shows blank cached values for formulas. Use `data_only=False` to see the formulas themselves.
3. **Merged cells**: `delete_rows()` in openpyxl doesn't auto-shift merged cell ranges. Unmerge before deletion and re-merge after.
4. **SUMIF text matching**: `*Labor*` pattern needs the wildcards in the string itself: `"*Labor*"` not just `"Labor"`.
5. **.xls files**: Use `xlrd` library (not openpyxl) for old Excel format.
6. **Decimal precision**: Accounting files often have floating-point artifacts (e.g., 104.347826086957). Round to 2 decimal places in display.
7. **Item type column location**: Some files have it in column E, some in column F or G. Check the actual header/column before writing code.
8. **Subtotals vs data rows**: Category subtotal rows have amounts too. Only classify actual item rows, not subtotal or total rows.
9. **RTL (Right-to-Left) sheet direction**: Set `ws.sheet_view.rightToLeft = True` for Arabic documents. Open the file and verify — Arabic documents expect columns to flow right-to-left in Excel.
10. **Openpyxl file locking**: If a workbook was previously loaded and is still in memory, save errors may occur or data may not persist. Always use the pattern: `load → modify → save → close`. Do not hold references to an old workbook object after saving.
11. **Invoice/document numbers**: Extract invoice numbers from Arabic descriptions (فاتورة/رقم followed by digits) and display in a dedicated column. This is critical for auditability — every line must be traceable to its source document.
12. **Reallocation descriptions**: When documenting moved items, use the FULL original Arabic description from the accounting statement, not a translated summary. The original description is the legal reference.
13. **Preserve original item numbers**: Add a column showing the original item number (e.g., `#39`) from the source accounting statement. This enables cross-referencing back to the original document.

## 6-Section Reference Document Template

The target output is a single comprehensive reference document per project with exactly these sections:

| # | Section | Content |
|---|---------|---------|
| 1 | Accounting Statement | All items grouped by category, each with: seq#, original#desc, invoice/doc#, category, amount, item type. Subtotals per category. Grand total. |
| 2 | Moved Out | Items transferred to other projects — original #, full description, invoice#, amount, destination, split method, amount kept (if partial) |
| 3 | Received From | Items received from other projects — description, source project, amount, reason for transfer |
| 4 | Item Type Summary | SUMIF breakdown: Construction / Equipment / Operations totals and percentages |
| 5 | Factory Cost | Raw Materials + Factory Labor (each merged to ONE line per type from the FCA; details in Remarks column) |
| 6 | Final Total | Accounting Total + Factory Cost + Supervision 10% = Grand Total. ALL values are FORMULAS referencing cells above. |
