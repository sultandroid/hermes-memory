# SOW §6.22 / §2.4 — Technical Design Deliverables Package Structure

> **Key rule:** DD submission is organized by **drawing package type** per SOW §6.22, NOT by floor. CG requests for "basement priority" or "staggered by floor" contradict the SOW structure.

## Source

- SOW document: `6380_KMS_RPT_PM_AS_00006_Aseer_Contractors_Scope of Work.pdf`
- Extracted text: `Docs/00_Project_Charter/extracted_text/scope_of_work.txt` (Pages 26–34 cover §6.22)
- ER document: `05_AS_Employer's Requirements Documents_250313/` (complements SOW)
- SOW §6.22 = "Technical Design Deliverables — Exhibition and Auxiliary Spaces"
- SOW §2.4 references "Combined Design Development (DD) and Construction Documentation (CD)" as deliverable packages

## SOW §6.22 Deliverables List (Pages 26–34)

### §6.22 — Technical Design Deliverables (Exhibition & Auxiliary Spaces)

Organized by deliverable TYPE, not by building level:

| SOW §6.22 Ref | Deliverable | Folder Code | Folder in DD Structure |
|---|---|---|---|
| (i) | Exhibition drawings (plans, sections, elevations & details) | Multiple codes | `Arch DD Drawing/` |
| General Arrangement plans | GA plans | 1200 | `1200_General_Arrangement/` |
| Walls and Floor finish plans and details | Walls & floor finishes | 1220/1920, 1230/1900 | `1220_Walls/`, `1230_Floor_Finishes/` |
| Interior elevations and details | Interior elevations | 1510 | `1510_Internal_Elevations/` |
| Reflected ceiling plans | RCP | 1250 | `1250_Ceiling_Details/` |
| Coordinated ceiling plans (MEP, Security, FLS, Data) | Coord. ceilings | 1250/1910 | Part of ceiling package |
| Showcase drawings + schedule | Showcases | 1800 | `Showcases Package/` |
| Graphic detailed design | Graphics | 1850/1860 | `1850_Graphics_Housing/` |
| §6.22.1 Graphic samples & production spec | Graphic specs | — | Within Graphic package |
| §6.22.2 AV hardware systems design | AV | 1930/1950 | Part of DD Drawing |
| §6.22.3 Exhibition lighting design | Lighting | 1250/1910 | Part of ceiling package + separate |
| (ii) | Detailed Specifications (all Fit-Out elements) | — | `Arch DD Specs/` (22 spec books K10E–Z31) |
| (v) | Final Showcase Schedule | — | `Showcases Package/` |
| (vi) | Detailed Showcase interior/object layout drawings | — | `Showcases Package/` |
| (viii) | Graphic Detailed Design | — | Within Graphic package |
| (x) | Graphics Schedule | — | Within Graphic package |
| (xiv) | Exhibition Lighting Design full package | — | Part of DD specs + drawings |
| (xv) | Horticulture / Landscape Design | 1570 | `1570_External_Details/` |
| Stairs | Stairs details | 1550 | `1550_Stairs_Details/` |
| External stramp & stairs | External details | 1570 | `1570_External_Details/` |
| Washrooms / VIP | Washrooms | 1600 | `1600_Washrooms_VIP/` |
| Setworks / Partitions | Setworks | 1711 | `1711_Setworks_Partitions/` |
| Furniture | FF&E | 1730 | `1730_Furnitures/` |
| Retails | Retail | 1760 | `1760_Retails/` |
| Freestanding walls | FWall | 1700 | `1700_Freestanding_Wall/` |
| Doors & Lift types | Doors | 1930/1950 | `1930_1950_Doors_Lifts/` |
| Lift lining | Lift | 1940 | `1940_Lift_Lining/` |
| Painted finishes | Finishes | 1890 | `1890_Painted_Finishes/` |
| Arch Visualization 3D Shots | 3D renders | — | `Arch Visualization 3D Shots/` |
| Terrace shading & balustrade | External | 1570 | `1570_External_Details/` |
| Library shelving & retail fit-out | Internal built-in | — | Within relevant drawing package |
| Demolition & site clearing | External | — | Within Sections/External |

### §6.22.4 — Technical Design Deliverables Summary Table

The SOW has a structured summary table (page 9 TOC reference, pages 26–34 content) that consolidates all the above by deliverable type. The table confirms:

1. **DD Drawing Packages** — organized by drawing type (GA, Sections, Elevations, Finishes, Showcases, etc.)
2. **DD Specifications** — 22 specification books covering all fit-out elements
3. **Showcases Package** — Glasbau Hahn showcase drawings, schedules, interior layouts
4. **3D Visualization** — rendered shots for design intent approval
5. **Material Submittals** — organized by CSI Division and specification section

**Crucially, the SOW does NOT organize DD by floor level.** The "basement priority" and "staggered floors" framing from CG is an organizational overlay that contradicts the contractual package structure.

## DD Folder Structure Confirmation

Actual DD folder at `02_Submittals/03_DD Documents/`:
```
Arch DD Drawing/
Arch DD Specs/
Arch Visualization 3D Shots/
Showcases Package/
audit/
Document_Issue_Register.xlsx
New Title Block/
```

Sub-folders under `Arch DD Drawing/` use 3/4-digit drawing-type codes (1200, 1220, 1230, 1250, 1350, 1500, 1510, 1550, 1570, 1600, 1700, 1711, 1730, 1760, 1800, 1850, 1860, 1890, 1930, 1940, 1950) — each a drawing TYPE, not a floor.

## Schedule Structure Implication

When building a Deliverables Submission Schedule for DD:
- **Rows = drawing packages** (GA, Walls, Floor Finishes, Ceilings, Sections, Elevations, Stairs, etc.)
- **NOT rows = building floors** (Basement, Ground, First Floor)
- DD dates should be per-package, confirmed by NRS
- IFC packages likewise per-drawing-type, produced by Samaya Tech Office
- Material Submittals are a separate phase per CSI section, not per floor
- CG review buffer (14 days) applies per submission package

## Related SOW Cross-References

| SOW Section | Topic | Relevance |
|---|---|---|
| §2.4 | DD and CD combined deliverables | Confirms package-based structure |
| §6.22 | Technical Design Deliverables — Exhibition | Full DD scope by deliverable type |
| §6.22.1 | Graphic Design | Separate spec package |
| §6.22.2 | AV Hardware Systems | Separate spec package |
| §6.22.3 | Exhibition Lighting | Separate spec package |
| §6.22.4 | DD Summary Table | Consolidated deliverables list |
| §7.0 | Site Assessment & Engineering | Part 2 — separate from DD Part 1 |
| §13 | Phase-Gate Matrix (Comm Plan) | Confirms G-1 Design Development submission routing |