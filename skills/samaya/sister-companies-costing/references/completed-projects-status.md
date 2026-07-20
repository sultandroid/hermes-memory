# Sister Companies — Completed Factory Cost Details (as of 2026-07-20)

## Projects 01-11: Factory Cost Totals

| # | Project | Labour | Materials | Other | **Total** | Notes |
|---|---------|--------|-----------|-------|-----------|-------|
| 01 | Al Wahi Gift Shop | 157,143 | 110,328 | 61,577 | **329,048** | Full timesheet (664 rows), 9 POs, 3 expense items |
| 02 | Holy Quran Gift Shop | 51,856 | 8,972 | 11,429 | **72,257** | Trade-level summaries (12 trades), 3 POs, fleet + reallocation |
| 03 | Qahwatna Cafe | 1,579 | 124,010 | 154,022 | **279,611** | Verified-only items (excluded 216,935 SAR flagged items) |
| 04 | Hira Cafe | 23,897 | 61,265 | -29,549 | **55,613** | 8 trades, 7 POs, reallocation -29,549 to Ice Coffee |
| 05 | Jabal Omar VIP Stores | 0 | 0 | 0 | **0** | Accounting file: "No data" for factory cost |
| 06 | As Safiyyah Giftshop | 30,890 | 68,665 | 19,100 | **118,655** | 9 trades, 7 PO categories, fleet |
| 07 | Khair Al-Khalq Gift Shop | 14,492 | 200 | 20,826 | **35,518** | 7 trades, 1 PO, reallocation from Jabal Omar |
| 08 | Qahwatna Al Safiya Cafe | 31,064 | 25,939 | 2,900 | **59,903** | 10 trades, 4 POs, fleet |
| 09 | Tzkarat Store | 4,250 | 6,774 | 70,429 | **81,453** | 4 trades, 2 POs, 4 reallocations from Al Wahi + Rateeb |
| 10 | Rateeb Store | — | — | — | **—** | Not yet processed |
| 11 | Najdi Coffee | 0 | 42,383 | 0 | **42,383** | 2 POs (PO#554/664 Other: 34,470, PO#627 Wood: 7,913). No labour or other expenses. |
| 12 | Ice Coffee Shop | — | — | — | **—** | Not yet processed |
| 13 | Hera Visitor Center | — | — | — | **—** | Not yet processed |

## File Locations

All projects have both files (full + clean) in:
- `00_Organized_13_Project_Factory_Reconciliation/{Company}/{Project}/`
- `_Final/{Client_Folder}/{Project}/`

## Company Mapping (verified)

| Project | Company Folder (Organized) | Client Folder (_Final) |
|---------|---------------------------|----------------------|
| 01 Al Wahi | Tiba_Gift_Company | Tiba Gift comp_ |
| 02 Holy Quran | Tiba_Gift_Company | Tiba Gift comp_ |
| 03 Qahwatna Cafe | Tiba_Gift_Company | Tiba Gift comp_ |
| 04 Hira Cafe | Qahwatna_Company | Qahwitna comp_ |
| 05 Jabal Omar VIP | (standalone) | (standalone) |
| 06 As Safiyyah | Tiba_Gift_Company | Tiba Gift comp_ |
| 07 Khair Al-Khalq | Tiba_Gift_Company | Tiba Gift comp_ |
| 08 Qahwatna Al Safiya | Qahwatna_Company | Qahwitna comp_ |
| 09 Tzkarat | Tezkarat_Trading_Company | Tezkarat Trading Com_ |
| 10 Rateeb | Rateeb_Trading_Company | Rateeb Trading Com_ |
| 11 Najdi Coffee | **Tiba_Gift_Company** | **Tiba Gift comp_** |
| 12 Ice Coffee | Qahwatna_Company | Qahwitna comp_ |
| 13 Hera Visitor Center | (standalone) | (standalone) |

> **⚠️ Company mapping note for Project 11 (Najdi Coffee):** The project map in the main skill lists Project 11 under Qahwitna comp_ / Qahwatna_Company, but the user directed files to Tiba Gift comp_ / Tiba_Gift_Company in the 2026-07-20 session. Verify with the user before hardcoding paths in future scripts. The mapping above reflects what was actually done, not what the original project map says.
