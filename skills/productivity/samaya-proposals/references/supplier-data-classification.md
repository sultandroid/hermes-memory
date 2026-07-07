# Supplier Data — Excel Classification & Multi-Store Proposal Workflow

> Session: 2026-06-27 | Saudi Coffee (مقهى القهوة السعودية) — 10 stores

## Excel Data Structure (from Supplier Ibrahim)

**Source file:** `مقهي القهوة السعودية (من ايميل ابراهيم 2026-06).xlsx`

### Sheets
| Sheet | Content |
|-------|---------|
| `مقهي القهوة السعودية` | Main costing — items with category, description, amount, item type |
| `معدات (Equipment)` | Equipment-only items (split from main) |
| `تشغيلية (Operations)` | Operations-only items (split from main) |

### Header row (Row 8 in main sheet)
| التصنيف | م | البيان | المبلغ | ملاحظات | نوع البند |
|---------|---|-------|--------|---------|----------|
| Category | # | Description (bilingual AR/EN) | Amount | Notes | Item Type |

### Category Groups in Main Sheet
1. **Factory Materials** — التصنيف = "Factory Materials" (raw material PO costs)
2. **Construction & Finishing** — construction/installation line items
3. **Equipment & Appliances** — equipment line items
4. **Furnishings & Decor** — furnishings line items

### Item Type Classification Keywords (Arabic)
| Type | Keywords |
|------|----------|
| **Construction** (إنشاءات) | خشب, نجارة, حديد, دهان, جبس, أرضيات, رخام, ميكانيكا, تكييف, سباكة, مكافحة حريق, عمال, توريد, تركيب, زجاج, اكريليك, بروفايل, صاج, سيراميك, موكيت, كنب, زراعه, ابواب, المونيوم, تعديل, تشطيب, مواد حداده, اصلاح |
| **Equipment** (معدات) | شاشة, كيبل, ليد, لمبة, جهاز, ماكينة, كمبيوتر, طابعة, كاميرا, بروجكتر, راوتر, مكيف, ثلاجة, خلاط, نظام, صوت, سماعات, ميزان, معدات, ستيل كيتشن, خلاط مطبخ |
| **Operations** (تشغيلية) | سفر, تذكرة, فندق, سكن, نقل, شحن, مواصلات, اكل, عشاء, طعام, ضيافة, قرطاسية, طباعة, بنك, تأمين, رسوم, صيانة, دومين, مصروفات, ماء, مبيد, تراخيص, ايجار, هاتف, انترنت, دعاية, اعلان, تصروح |

### Cost Summary (per store)
| Category | Calculation | Notes |
|----------|------------|-------|
| Accounting Total | SUM(Construction + Furnishings + Factory Materials) | From main sheet, excludes Equipment & Operations |
| Equipment Total | SUM from Equipment sheet | Separated for independent invoicing |
| Operations Total | SUM from Operations sheet | Separated for independent invoicing |
| Raw Materials (POs) | Hardcoded value (not formula) | Factory cost — material procurement |
| Factory Labor | Value or 0 | Factory cost — labor |
| Supervision | 10% × (Accounting + Raw Materials + Factory Labor) | Standard Samaya markup |
| **Grand Total** | Accounting + Equipment + Operations + Raw Materials + Factory Labor + Supervision | Final bid price |

## Store Structure (Saudi Coffee — 10 stores)

### 4 Companies, 10 Stores

| Company | Store Code | Store Name | Area | Location |
|---------|-----------|------------|------|----------|
| **Qahwitna comp.** | 03 | Qahwatna Cafe | TBD | TBD |
| | 04 | Hira Cafe | TBD | TBD |
| | 08 | Qahwatna Al Safiya Cafe | TBD | TBD |
| | 11 | **Najdi Coffee** | **173 m²** | **Makkah** |
| **Rateeb Trading Com.** | 10 | Rateeb Store | TBD | TBD |
| **Tezkarat Trading Com.** | 09 | Tzkarat Store | TBD | TBD |
| **Tiba Gift comp.** | 01 | Al Wahi Gift Shop | TBD | TBD |
| | 02 | Holy Quran Gift Shop | TBD | TBD |
| | 06 | As Safiyyah Giftshop | TBD | TBD |
| | 07 | Khair Al Khair Store | TBD | TBD |

### Proposal File Path Convention
```
~/_Final Folder/{Company}/{Store_Code}_{Store_Name}/index.html
~/projects/saudi-coffee/clients/{Company}/{Store_Code}_{Store_Name}/   (mirror)
```

When only Store 11 has data: create full proposal for Store 11, framework proposals (TBD pricing) for stores 01-10. Framework = all 12 sections present, BOQ rows empty with amber TBD badge.

## Framework Proposal Rules

1. **Cover page** — Store name, client company name, generic location placeholder
2. **Scope of Work** — 7 generic work packages (Civil, Architectural, MEP, Equipment, Landscaping, AV/IT, Signage) with note "detailed scope per store upon site survey"
3. **BOQ** — Empty table with headers and category subtotal rows; every cell shows `—` or `TBD`
4. **Pricing note** — Amber banner: "🔶 Pricing pending supplier confirmation"
5. **Schedule** — Uniform 12-week timeline regardless of store size
6. **Team structure** — Same Samaya org chart for all stores

## Excel Extraction Code Pattern

```python
import openpyxl
wb = openpyxl.load_workbook('/tmp/supplier_file.xlsx', data_only=True)
ws = wb['Main Sheet']

for row in ws.iter_rows(min_row=10, values_only=True):
    cat, num, desc, amount, notes, item_type = row
    if not cat or not amount: continue
    # Classify
    if 'Factory' in str(cat): category = 'Factory Materials'
    elif 'Construction' in str(cat): category = 'Construction'
    elif 'Equip' in str(cat): category = 'Equipment'
    elif 'Furnish' in str(cat): category = 'Furnishings'
    else: category = str(cat).strip()
    
    # Item type (Construction/Equipment/Operations)
    item_class = str(item_type).strip() if item_type else classify_from_keywords(desc, AR_KEYWORDS)
```

## Project Metadata
- **Brand:** Saudi Coffee (مقهى القهوة السعودية / Najdi Coffee — Al Kahwa Al Nagdia)
- **Supplier contact:** Ibrahim (email source)
- **Reference:** Session 2026-06-27
- **Workflow:** delegate_task → read Excel → classify → create PROPOSAL_STUDY_REPORT.md → build framework HTML proposals → save to _Final Folder
