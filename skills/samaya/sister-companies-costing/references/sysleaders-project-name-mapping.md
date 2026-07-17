# SysLeaders Project Name Mapping — 13 Sister Companies

The SysLeaders database uses different project names than the Sister Companies folder structure. When querying POs, cost analysis, or labor records, match by the SysLeaders name, not the folder name.

## Mapping table

| # | Folder Name | SysLeaders Project Name | Entity ID | POs Found |
|---|---|---|---|---|
| 1 | 01_Al_Wahi_Gift_Shop | Jabal Alnoor Gift Shop | — | 9 |
| 2 | 02_Holy_Quran_Gift_Shop | JN- Quaran Kareem's Shop | — | 0 |
| 3 | 03_Qahwatna_Cafe | Kahwatna Cafee | — | 9 |
| 4 | 04_Hira_Cafe | Hera Cafe | — | 11 |
| 5 | 05_Jabal_Omar_VIP_Stores | JN- Quaran Kareem's Museum | — | 62 |
| 6 | 06_As_Safiyyah_Giftshop | As Safiyyah Giftshop | — | 24 |
| 7 | 07_Khair_Al_Khalq_Store | Khair Al-Khalq Store | — | 0 |
| 8 | 08_Al_Safiya_Cafe | Kahwatna Cafee -alsafya Almadina | — | 8 |
| 9 | 09_Tzkarat_Store | JN- Tzkarat shop | — | 3 |
| 10 | 10_Rateeb_Store | JN-Rateeb-Shop متجر التمور | 282 | 3 |
| 11 | 11_Najdi_Coffee | Al kahwa alnagdia | — | 3 |
| 12 | 12_Ice_Coffee_Shop | JN- ICE coffee shop | — | 1 |
| 13 | 13_Hera_Visitor_Center | JN- Visitors Center | — | 1 |

## Query pattern

When filtering the `purchasing_orders_20260716_081602.json` records, use case-insensitive substring matching on field `637` (project name):

```python
matches = [r for r in all_pos if sl_name.lower() in r.get('637','').lower()]
```

## Notes

- Projects 02 (Holy Quran) and 07 (Khair Al-Khalq) have zero POs in the backup. Their costs may be under different SysLeaders names or may not use the PO system.
- Project 05 (Jabal Omar VIP Stores) has 62 POs (351,878.98 SAR) but a Section 5 target of 0 — this is a major allocation gap.
- Project 06 (As Safiyyah) has 24 POs (260,939.92 SAR) but a Section 5 target of 100,000 — gross POs exceed target by 161%.
- The `cost_analysis_20260716_081602.json` uses `parent_item_id` (project entity ID) rather than project name. Entity IDs are not consistently mapped in the backup.
