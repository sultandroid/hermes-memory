# Source Folder → FCA File Mapping

Source folders under `Reports/Sister_Companies/` use the pattern `{NN}_{Project_Name}_XX`.
The FCA (Factory Cost Analysis) files within them drop the leading `NN_` prefix.

| Code | Source Folder | FCA File | Costing File |
|------|--------------|----------|-------------|
| 01 | `01_Al_Wahi_GiftSHop_01` | `Al_Wahi_GiftSHop_01_Factory_Cost_Analysis.xlsx` | (FCA Cost_Register has it) |
| 02 | `02_Holy_Quran_GIFTSHOP_02` | `Holy_Quran_GIFTSHOP_02_Factory_Cost_Analysis.xlsx` | (FCA has it) |
| 03 | `03_Qahwatna _Caffee_02` | `Qahwatna _Caffee_02_Factory_Cost_Analysis.xlsx` | `Qahwatna_Costing.xlsx` |
| 04 | `04_Hira_Cafee_02` | `Hira_Cafee_02_Factory_Cost_Analysis.xlsx` | `Hira_Cafee_02_Restructured_Costing.xlsx` |
| 05 | `05_Jabal_Omar_Vip_Stores_03` | `Jabal_Omar_Vip_Stores_03_Factory_Cost_Analysis.xlsx` | (none — empty project) |
| 06 | `06_As_Safiyyah_Giftshop_04` | `As_Safiyyah_Giftshop_04_Factory_Cost_Analysis.xlsx` | (FCA has it) |
| 07 | `07_Khair_Al_Khalq_Museum_GiftShop_05` | `Khair_Al_Khalq_Museum_GiftShop_05_Factory_Cost_Analysis.xlsx` | `Khair_Al_Khalq_Museum_Store_Costing.xlsx` |
| 08 | `08_Qahwatna_Al_Safiya_Cafee_03` | `Qahwatna_Al_Safiya_Cafee_03_Factory_Cost_Analysis.xlsx` | `Qahwatna_Al_Safiya_Costing.xlsx` |
| 09 | `09_Tzkarat_Store_06` | `Tzkarat_Store_06_Factory_Cost_Analysis.xlsx` | `Tzkarat_Costing.xlsx` |
| 10 | `10_Rateeb_Store_07` | `Rateeb_Store_07_Factory_Cost_Analysis.xlsx` | `Rateeb_Costing.xlsx` |
| 11 | `11_Cafe_4_Najdi_Coffee_04` | `Cafe_4_Najdi_Coffee_04_Factory_Cost_Analysis.xlsx` | (none — sparse data) |
| 12 | `12_Ice_Coffee_05` | `Ice_Coffee_05_Factory_Cost_Analysis.xlsx` | `Ice_Coffee_Store_Costing.xlsx` |
| 13 | `13_Hera_Visitor_Center` | `Hera_Visitor_Center_Factory_Cost_Analysis.xlsx` | `Hera_Visitor_Center_Costing.xlsx` |

**Safe glob pattern** to find FCA in any source folder:
```python
import glob, os
folder = os.path.join(BASE, source_folder)
matches = glob.glob(os.path.join(folder, "*Factory_Cost_Analysis*.xlsx"))
# Filter out backups:
matches = [m for m in matches if "backup" not in m.lower() and "~" not in m]
fca_path = sorted(matches)[-1] if matches else None
```

## FCA Labor Data Availability

Not all projects have per-trade breakdowns in the FCA. Projects 01, 03, 05, 11, 13 have either aggregate-only data or no labor data at all. For these, use the `_Final` project file as fallback:

| Project | FCA Labor Detail | Fallback Source |
|---------|-----------------|-----------------|
| 01 Al Wahi | Aggregate only (853 rec, 6,635 hrs, 72,143 SAR) | _Final says 157,143 total |
| 03 Qahwatna | 1 trade only (Faom Technision, 119 SAR) | _Final says 59,467 total |
| 05 Jabal Omar | Empty FCA | No data — reallocation-only |
| 11 Najdi Coffee | No labor | _Final says 0 |
| 13 Hera VC | No labor | Reallocation-only |

## FCA PO Data Patterns

The PO data appears in FCA files in two places:
1. **Cost_Register sheet**: Lines like `PO - Wood | Factory Materials | 40920 | PO#525, PO#540`
2. **Factory_Work sheet**: Lines like `PO - Paint | PO#416 | 25000`

When programmatic parsing fails, the manual read-and-embed approach always works.
