# Al Wahi Gift Shop — Cost Classification Worked Example

## Session Context (2026-06-15)

Full cross-project cost reallocation across 13 sister company stores + Hera Visitor Center. Scanned all .xlsx + .xls accounting statements, classified 500+ line items, created 2 new project folders.

## Project Basics

| Field | Value |
|-------|-------|
| Project | Al Wahi Gift Shop (01_Al_Wahi_GiftSHop_01) |
| JN IDs | 367+255 |
| Location | Makkah |
| Area | 240 m² |
| Source folder | `~/OneDrive - SAMAYA INVESTMENT/Reports/Sister_Companies/01_Al_Wahi_GiftSHop_01/` |

## Files in Project Folder

| File | Role |
|------|------|
| `Al_Wahi_GiftSHop_01_Factory_Cost_Analysis.xlsx` | Master analysis: Cost_Register, Dashboard, Factory_Work, Supervision, Audit_Log |
| `تكاليف متجر هدايا طيبة جبل النور (من ايميل ابراهيم 2026-06).xlsx` | Raw accounting source — 61 rows, SAR 253,557.62 |
| `تكاليف متجر هدايا طيبة جبل النور.xlsx` | Same with audit notes column |
| `Al_Wahi_Store_Costing.xlsx` | Empty template (no factory data entered) |
| `_Docs/` | Empty |

## Store Areas (from Management Reference)

| Store | Area (m²) | Code |
|-------|:---------:|:----:|
| Al Wahi | 240 | 01 |
| Holy Quran Gift Shop | 194 | 02 |
| Qahwatna Cafe (Hira) | 77.5 | 03 |
| Hira Cafe | 398 | 04 |
| Jabal Omar VIP Stores | 67 | 05 |
| As Safiyyah Giftshop | 445 | 06 |
| Khair Al-Khalq Store | 173 | 07 |
| Qahwatna Al-Safiya | 26 | 08 |
| Tzkarat Store | 51 | 09 |
| Rateeb Store | 42 | 10 |
| Al Kahwa Al Nagdia | 173 | 11 |
| Ice Coffee Shop | — | 12 |

## Complete Cross-Project Reallocation Table

All items flagged across ALL stores during the session scan:

| # | From Store | SAR | Description | Involves | Split Rule | Resolution |
|:-:|:----------:|----:|-------------|:---------|:----------|:-----------|
| 1 | 01 Al Wahi | 82,437.50 | MEP 50% | Tzkarat + Rateeb | Area 51:42 | ✅ 45,175.75 + 37,261.75 |
| 2 | 01 Al Wahi | 36,468.00 | MEP 30% | Rateeb + VC | Equal | ✅ 18,234 + 18,234 |
| 3 | 01 Al Wahi | 29,563.00 | Signage lettering | 2 shops no signage | Equal | ✅ Tzkarat + Rateeb |
| 4 | 01 Al Wahi | 3,696.50 | Fire protection | Al Wahi + Tzkarat | Area 240:51 | ✅ 3,049.61 + 646.89 |
| 5 | 04 Hira Cafe | 29,549.00 | Billboard for Ice Coffee | → 12 Ice Coffee | Full move | ✅ |
| 6 | 05 Jabal Omar | 20,826.00 | Mentions Khair Al-Khalq | → 07 | Full move | ✅ |
| 7 | 05 Jabal Omar | 1,583.00 | Mentions Jabal Alnour (01) | → 01 Al Wahi | Full move | ✅ |
| 8 | 05 Jabal Omar | 429.00 | Mentions Quran Exhibit | → 02 Holy Quran | Full move | ✅ |
| 9 | 10 Rateeb | 22,796.00 | Gypsum works | Rateeb + Maska + VC | Area TBD | ⏳ awaiting Maska area |
| 10 | 10 Rateeb | 19,649.57 | Cashier devices (Inv#794) | Rateeb + Tzkarat | Equal | ✅ 9,824.79 each |

## Bank Statement Analysis Pattern (.xls files)

The Quran Museum/Gift Shop folder (02) contained `.xls` bank statements that revealed:

| File | Account | Total (SAR) | Lines |
|------|---------|:-----------:|:-----:|
| متحف القرآن الكريم 2023.xls | معرض القران - جبل النور (Museum) | ~varies | 541 |
| متحف القرآن 2024.xls | معرض القران - جبل النور (Museum) | 205,756.65 | 608 |
| متجر متحف القرآن 2024.xls | متجر معرض القرآن الكريم (Gift Shop) | 23,934.78 | 24 |

Pattern: `.xls` files are bank account statements from SAMAYA INVESTMENT account (Saudi bank, account ending in various suffixes). Each has:
- Account name = project name (e.g., "المشاريع / معرض القران - جبل النور")
- Date range in header (من تاريخ / إلى تاريخ)
- Running balance in left column
- Credit entries in مدين column
- Statement total at the bottom of each section, with Arabic text amount

## New Project Creation Pattern

When a new project is discovered in shared cost lines:

1. Create folder under `Sister_Companies/` with sequential number (13_ for VC, 14_ for Maska when found)
2. Copy any existing source docs into the folder
3. Create `Factory_Cost_Analysis.xlsx` with:
   - **Cost_Register** sheet — classified lines with source project note
   - **Dashboard** sheet — project info, cost summary, notes on shared origins

## Translation Reference

| Arabic | English | Notes |
|--------|---------|-------|
| متجر هدايا طيبة جبل النور | Tayyiba Gifts / Al Wahi Gift Shop | Same store |
| متجر تذكارات | Tzkarat (Souvenirs) Store | Store 09 |
| متجر رطيب / التمور | Rateeb / Dates Store | Same store |
| مركز الزوار جبل النور | Jabal Alnour / Hera Visitor Center | Standalone project |
| مسكا | Maska | Unknown project — awaiting info |
| عهدة [اسم] | Custody advance [employee name] | Petty cash — stays in current project |
| كبار الزوار | VIP Visitors | Not the same as Visitor Center — usually references Jabal Omar VIP Store (05) |
