# Material Compliance Check — Worked Example

## Scenario
User sent 4 Ritver/RAR Holding documents and asked "do these materials comply with our project?" Context was ambiguous between Moqtana and Aseer Museum.

## Documents Provided

| Doc | Type | Key Data |
|-----|------|----------|
| Company Profile -A.pdf | Company profile | Ritver = paints/coatings mfr under RAR Holding, 60+ yr, international, LEED-certified products |
| RITVER WB711 - Wood Preservative Sealer | Tech datasheet | Water-based wood sealer for softwood, low VOC, UV/water/microbe protection |
| RITVER WT73X0 - Wood Preservative Topcoat | Tech datasheet | Water-based matt topcoat for exterior wood, LEED EQ C4.2, Catas certified, EN 927-3 passed |
| LEED204 --VOC Test | Test report | PU Sanding Sealer, 216 g/L VOC, tested by Al Futtaim Exova (Dubai), ASTM D 3960 / SCAQMD Rule 1113 |

## Process Applied

### Step 1: Confirm project (FAILED initially — assumed Moqtana from conversation history)
**Correction received:** "Not moqtana i mean aseer project"
**Lesson:** Always confirm project when user has multiple active contexts.

### Step 2: Search project specs
- Found Aseer Museum tender pack under OneDrive
- ER (Bluehaus MEP Engineering, 170pp) — MEP focused, no paint/finish specs
- SoW (46pp exhibition fit-out) — references §8.7 joinery, §13.13 mock-ups/samples, §13.9 sustainability
- BOQ xlsx — **locked** (open in Excel → Resource deadlock avoided)
- BOQ PDF mirror — **corrupt** (bad zip / no objects)
- No extractable paint/wood specification found in accessible documents

### Step 3: Map materials to project requirements

| Ritver Material | Project Requirement Match | Verdict |
|----------------|--------------------------|---------|
| Company profile | ISO-grade mfr, LEED-certified → aligns with §13.9 sustainability | ✅ No red flags |
| WB711 Wood Sealer | Water-based, low VOC → good for museum IAQ. Need to confirm if wood sealing is in BOQ/finish schedule | ⚠️ Conditionally OK |
| WT73X0 Topcoat | LEED EQ C4.2 + Catas + EN 927-3 → strong certs for museum exterior wood | ✅ Likely compliant |
| PU Sanding Sealer (216 g/L) | Under SCAQMD Rule 1113 limit (275 g/L for clear wood coatings). SASO limit unknown | ⚠️ Need SASO check |

### Step 4: Report with evidence gap
Could not definitively answer because:
- Finish schedule / paint spec not accessible from locked/corrupt files
- SASO VOC limits not confirmed
- Whether wood finishes are in scope (joinery mentioned but no material schedule found)

## Lessons Learned
1. **Always confirm project** before material compliance search — don't assume from conversation context.
2. **Two-file BOQ pattern** (xlsx + PDF mirror) — both may fail; ask user for the spec section directly.
3. **ER may not contain paint specs** — MEP-focused ERs won't cover architectural finishes. Check Room Data Sheets and finish schedules instead.
4. **Museum IAQ sensitivity** — water-based, low-VOC products are preferred. This is a general museum best practice, not a project-specific requirement.
5. **Certificate age matters** — 2017 VOC test report (LEED204) may be considered stale for a 2026 project.
