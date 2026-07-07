# Samaya BIM Project Code Cross-Reference

When a file with an unfamiliar document code is found in one project's directory, it may belong to a different project. Use this to route it correctly.

## Code-to-Project Mapping

| Document Code / Pattern | Project | Notes |
|------------------------|---------|-------|
| `A2742`, `MOC-MUS-ASE`, `MOC-ASEER` | **Aseer Museum** | Main project codes for the Aseer Regional Museum of Art |
| `M2742-*` | **Aseer Museum** | NRS contract document series — *NOT* a different project. Same M2742 series found in Contracts/ and Docs/ |
| King Khaled Road refs (A-02, etc.) | **Aseer Museum** | The museum is on King Khaled Road in Abha. These are as-built reference drawings for the existing building |
| `MOC-Asser-SIC-*` | **Aseer Museum** (likely) | Consistent misspelling by NRS sender. An analysis note `MOC-ASSER-0PS-SH-006_Analysis.md` already exists in Aseer-Museum/Docs |
| `P083` | **Zamzam Museum / Zamzam Visitor Center** | Design development drawings and landscape plans. Multiple copies in Zamzam's Email_Archive and Design Files |
| `TF2438*` | **Zamzam Museum** | Drawing reference found in Zamzam Museum/Docs/ |
| `MVii` Madinah model refs | **El-Haramain Museum** | Physical scale model for Prophet's Mosque (Al-Masjid Al-Nabawi) |
| `MVii` Makkah model refs | **Zamzam Museum** | Physical scale model for Grand Mosque (Al-Masjid Al-Haram) |
| `MVii` company docs (licenses, bank, certs) | **El-Haramain Museum** | Support both mosque models — El-Haramain = The Two Holy Mosques |
| Haram / Haramain / `المسجد الحرام` / `المسجد النبوي` | **El-Haramain Museum** | About the Two Holy Mosques |
| `مسجد النور` / Al-Noor / Alnoor | **Masjid Alnoor** | Separate mosque project in Makkah |
| TP-09-2512-UTT-RP-R01 | **El-Haramain Museum** | Barriers report for Grand Mosque + Prophet's Mosque |

## Discovery Workflow

When a file doesn't match the project's expected codes:

1. **Search the full workspace** for context:
   ```bash
   find "Samaya/" -type f -iname "*CODE*" 2>/dev/null
   find "Samaya/Technical Office/Bim Unit" -type f -iname "*CODE*" 2>/dev/null
   ```

2. **Check other project folders** — search each project's Docs/, Design Files/, Contracts/ for matching codes

3. **Apply contextual rules** (not just code matching):
   - Same document number series → same project (e.g., M2742-1.00-004 matches M2742-1.00-003 in Contracts)
   - Same building/location name → same project (King Khaled Road → Aseer Museum address)
   - Same subcontractor → check which projects they're engaged on
   - Consistent misspelling of project code → likely same project (MOC-Asser-SIC → Aseer)

4. **Route directly** to the target project's canonical subfolder. Do NOT use a catch-all holding area.

5. **Create descriptive subfolders** as needed:
   - `Design Files/MVii_Models/` for model-related content
   - `Design Files/As-Built_References/` for reference drawings
   - `Docs/As-Built_References/` for as-built PDFs

## Common Pitfalls

| Assumption | Reality |
|-----------|---------|
| M2742 is a different project code | Actually same project (Aseer Museum) — NRS uses multiple document series |
| King Khaled Road files are for a road project | Actually as-built drawings for the Aseer Museum building (it's on that road) |
| MOC-Asser-SIC is a different project | Likely Aseer with a consistent typo — check for analysis notes before concluding |
| MVii docs all go to one project | Split by location: Madinah → El-Haramain, Makkah → Zamzam |
