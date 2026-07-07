# Tender Package Example: Khair El-Khalq Museum

## Project
Interior fit-out museum project with zones: Reception, Waiting Area & VIP, Hall 1, Pre-Hijra, Madinah, Death, Last Hall, General, Media.

## Source Data
- Items Status sheet (`Items Status.xlsx`) — 49 items with location, description, supplier, action status
- 20+ drawings in `Revit Files/Detail Drawings/` (PDF/DWG/RVT)
- 27 MasterFormat spec divisions in `Specs & Datasheet/GENERAL SPECIFICATIONS/`
- Revit model: `ASR-KHAIR_AL_KHALK.rvt` + 6 backup versions

## Tender Package Files Created

| File | Content |
|---|---|
| `BOQ.xlsx` | 49 items grouped by zone, navy/gold styling, Notes sheet |
| `Pricing_Schedule.xlsx` | Same items with VAT summary section |
| `Scope_of_Work.md` | 9 zones + exclusions + contractor responsibilities |
| `Tender_Drawings_List.md` | 20 drawings indexed (PDF/DWG/RVT) |
| `Technical_Specifications_Index.md` | 27 MasterFormat divisions, 6 key sections highlighted |
| `Tender_Conditions.md` | 6 sections: submission, pricing, qualifications, evaluation, general |
| `Tender_Form.md` | Letter of Tender with declarations + tenderer info table |

## BOQ Formatting
- Headers: Item #, Location, Description, Unit, Qty, Unit Rate (SAR), Total (SAR)
- Navy `#1F3864` header fill, white bold font
- Gold `#FFD700` grand total row
- Column widths: A=8, B=20, C=50, D=14, E=10, F=16, G=16
- Notes sheet: currency (SAR), VAT (15%), quantities verification

## Key Decisions
- Items grouped by physical zone (not trade) — matches how fit-out contractors price
- Unit rates left blank (TBD) for tenderer to fill
- Revit model included as reference for quantity take-off
- Spec index only lists divisions that actually exist in the project folder
- Files saved directly to OneDrive-synced `Tinder Doc/` folder
