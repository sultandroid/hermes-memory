# Moqtana Odoo Project Codes Register

Codes derived from existing document references (RFP, ER, SOW filenames) in each project's folder.

## Active Projects (as of 2026-06-01)

| Code | Odoo ID | Project Name | Source Reference |
|------|---------|-------------|------------------|
| **URP-VC** | 13 | Urwa Palace Visitor Center | — (created for this project) |
| **DAR-VIC** | 14 | Darin Visitor Center (قلعة دارين) | `DAR-VIC-BIM-RFP-001` (RFP filename) |
| **SHO-VIC** | 15 | Shobra Palace Visitor Center | `SHO-VIC-BIM-RFP-001` (RFP filename) |
| **ALB-VC** | 16 | Al Bay'ah Mosque Visitor Center (مسجد البيعة) | — (created based on convention) |
| **ALF-VC** | 17 | Al Faw Visitor Center (قرية الفاو) | `ALF-PEP-006` (PEP document ref) |
| **ARA-ARC** | 18 | Al-Raka Archaeological Center (الراكة) | `AR-ER-2026-001` (ER document ref) |
| **ANT-VC** | 19 | Antara Rock Visitor Center (صخرة عنترة) | — (created based on convention) |
| **SAH-SQ** | 20 | Said Alshohadaa Square Hoarding (سيد الشهداء) | — (created — SQ = Square) |
| **TAB-VC** | 21 | Tabuk Castle Visitor Center (قلعة تبوك) | `TAB-VC-DSN-RFP-001` (RFP filename) |

## Code Convention Rules

### Suffix patterns

| Suffix | Meaning | Used for |
|--------|---------|---------|
| `-VC` | Visitor Center | Museum/heritage visitor center projects |
| `-VIC` | Visitor Center | Alternate form used in some RFP refs (Darin, Shobra) |
| `-ARC` | Archaeological Center | Archaeological/cultural center projects |
| `-SQ` | Square | Open square / plaza / hoarding projects |

### Prefix patterns

- First 3 letters of the project location/name, uppercase
- If the existing project documents already use a specific abbreviation (e.g. `DAR`, `SHO`, `ALF`, `TAB`), use that
- Otherwise, derive from the English project name (e.g. `ANT` for Antara, `SAH` for Said Alshohadaa)

## Template Projects

| Code | Odoo ID | Name |
|------|---------|------|
| — | 1 | Internal (Odoo system default) |
| TEMPLATE-FITOUT | 2 | [TEMPLATE] Design & Build Fit-out |
