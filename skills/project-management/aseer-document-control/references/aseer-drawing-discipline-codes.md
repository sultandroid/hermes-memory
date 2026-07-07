# Aseer Museum — Drawing & Discipline Code Conventions

> Source: Extracted from project files (BEP §8.5, actual DWG filenames, Submittal Registers, IFC package names). Use as reference when coding drawings, filling TIDP/MIDP, or setting up BEP forms.

---

## 1. Document Numbering (ISO 19650 style)

```
MOC-MUS-ASE-[LEVEL][DISC]-[DOCTYPE]-[SEQ]
```
Example: `MOC-MUS-ASE-1A0-IFC-0005`

| Segment | Meaning | Examples |
|---------|---------|----------|
| MOC | Client: Ministry of Culture | Fixed |
| MUS | Client Division: Museums Commission | Fixed |
| ASE | Project: Aseer (أثير) | Fixed |
| `[LEVEL][DISC]` | Phase level + Discipline code | `1A0`, `1E0`, `1K0`, `1KH` |
| `[DOCTYPE]` | Document type | `PL` (Plan), `IFC` (Issue for Construction), `SR` (Submittal Register), `ZD` (General/Methodology), `MS` (Method Statement), `IR` (Inspection Request), `SI` (Site Instruction), `TQ` (Technical Query), `RP` (Report) |
| `[SEQ]` | Sequential number, 4-digit | `0001`, `0005`, `0015` |

### Discipline Level Codes (in document numbering)

| Code | Discipline | Example |
|------|-----------|---------|
| `1A0` | Architecture | `MOC-MUS-ASE-1A0-IFC-0005` |
| `1E0` | Electrical / AV | `MOC-MUS-ASE-1E0-SR-0001` |
| `1K0` | Coordination / General / Multi | `MOC-MUS-ASE-1K0-PL-0015` (BEP) |
| `1KH` | HSE | `MOC-MUS-ASE-1KH-PL-0001` |
| `1C0` | Civil | per routing table |
| `1M0` | Mechanical | per routing table |
| `1KN` | Security / ICT | per routing table |
| `1A0-ZD-` | Architecture Design / General | `MOC-MUS-ASE-1A0-ZD-0060` (Arch Viz submittal) |

### MOC-MUS-ASE vs MOC-ASEER-SIC prefix

Two document-level prefixes exist:

| Prefix | Source | Usage |
|--------|--------|-------|
| `MOC-MUS-ASE-` | Ministry of Culture — Museums Division — Aseer | Documents issued by the Museums client team (CG responses, PMO directives, submittals managed through the Museums document control system) |
| `MOC-ASEER-SIC-` | Ministry of Culture — Aseer project — Supervision/Implementation Contractor | Contractor-issued documents (shop drawings, RFIs, method statements, correspondence) |

The `MOC-MUS-ASE-` prefix is used for client-side document control and CG review responses. The `MOC-ASEER-SIC-` prefix is used for Samaya's (contractor's) deliverables.

---

## 2. Drawing Numbering (Shop Drawings)

Actual convention used in DWG files:

```
MOC-ASEER-SIC-SDW-[DISC]-[TYPE]-[LEVEL]-[SEQ]
```
Example: `MOC-ASEER-SIC-SDW-AR-GA-BF-0001`

| Segment | Meaning | Examples |
|---------|---------|----------|
| MOC | Client | Fixed |
| ASEER | Project name | Fixed |
| SIC | Contractor: Samaya Investment Co. | Fixed |
| SDW | Shop Drawing | Fixed for SDW phase |
| `[DISC]` | Discipline | `AR` (Architecture), `ST` (Structure) |
| `[TYPE]` | Drawing type | `GA` (General Arrangement) |
| `[LEVEL]` | Level/Zone | `BF` (Basement Floor), `LGF` (Lower Ground Floor), `GF` (Ground Floor), `1F` (First Floor), `2F` (Second Floor) |
| `[SEQ]` | Sequential number | `0001` |

### Alternative — NRS/Consultant style (older files)

```
041-SIC-ZZ-ZZ-M3-Arch-01.rvt        (Revit model)
322062-N3-ABD-H-P3-1003.dwg          (NRS drawing code)
```

---

## 3. Submittal Register Reference Codes

Used in the actual submittal registers (not document numbers — these are deliverable references within registers):

| Code | Discipline | Example | Source File |
|------|-----------|---------|-------------|
| `AV-NNN` | Audio Visual | `AV-001` — Complete AV plans & elevations | AV Submittal Register |
| `LG-NNN` | Lighting | `LG-001` — Lighting design concept | Lighting Submittal Register |
| `LS-NNN` | Landscaping | `LS-001` — Landscape design concept | Landscaping Submittal Register |

---

## 4. BEP Internal Discipline Codes — Table 30 (Sheet Naming)

From the BEP §E.5 Naming Convention, Table 30 — these are the **approved discipline codes** for the Aseer Museum BEP. Any sheet numbering proposal MUST use these codes, not single-letter US NCS codes:

| Code | Discipline | Primary Keywords |
|------|-----------|-----------------|
| `AR` | Architecture | façade, walls, finishes, layouts |
| `ST` | Structure | concrete, rebar, columns, slabs |
| `ID` | Interior Design | public areas, ceiling, finishes |
| `HV` | HVAC | HVAC, ducts, air handling |
| `EL` | Electrical | power, lighting, panels |
| `PL` | Drainage / Plumbing | drainage, water, piping |
| `FF` | Fire Fighting | sprinklers, hydrants, pumps |
| `LS` | Landscape | planting, irrigation, paving |
| `IT` | ICT / ELV | CCTV, data, BMS, access control |
| `INF` | Infrastructure | utilities, roads, site works |
| `LC` | Low Current | Low Current System, ICT Systems |
| `GAS` | Gas | Gas System, LPG System |
| `FA` | Fire Alarm | Fire Alarm |

The BEP also defines a **Type** suffix for models: `M` (Model), `DRW` (Drawing), `R` (Report), `D` (Data).
Example: `AR-M-03` = Architecture Model, Detailed Design phase.

## 5. BEP Sheet Naming Convention — Table 24 (Title Block)

From BEP §E.5, Table 24 — the ISO 19650-style sheet name (used at container/CDE level):

```
[Project Number]-[Originator]-[Volume Code]-[Level Code]-[Doc Type]-[Discipline]-[Drawing Number]
```

Example: `223032-SAM-XX-XX-RVT-AR-001`

| Segment | Value | Notes |
|---------|-------|-------|
| Project Number | `223032` | Project code |
| Originator | `SAM` | Samaya |
| Volume Code | `XX` | All zones (wildcard) |
| Level Code | `XX` | All levels (wildcard) |
| Document Type | `RVT` | Revit (or `3DM`, `DWG`, `PDF`) |
| Discipline | `AR` | Per Table 30 above |
| Drawing Number | `001` | 3-digit sequential |

### ⚠️ BEP Table 31 Inconsistency

BEP Table 31 (worked example) shows `A001` as the Drawing Number with `Arch` as a separate Discipline field — using the single-letter `A` code and `Arch` label instead of the Table 30 code `AR`. This suggests the BEP drafters mixed US NCS single-letter codes into the drawing number field. The approved Appendix 223032-SAM-XX-XX-BEP-B-XX-Appendix-05_Naming_Convention should resolve this. Until confirmed, **use Table 30 codes** for all new work.

## 6. Checking a Proposed Naming Convention Against BEP (Workflow)

When asked to verify whether a proposed sheet/document numbering system complies with the project BEP and ISO 19650:

### Workflow

1. **Extract the proposed system** from the submitted file (DOCX paragraph/tables):
   ```python
   from docx import Document
   doc = Document(path)
   for para in doc.paragraphs: ...
   for table in doc.tables: ...
   ```

2. **Find the BEP** in the project's document control folder — search for `*BIM_Execution_Plan*` or `*BEP*` under `06_PDFs/`. Extract key tables:
   - Table 24 — Sheet Naming Convention (container code format)
   - Table 30 — Discipline Codes (authoritative code list)
   - Table 31 — Worked example (may have inconsistencies — flag them)

3. **Build a comparison matrix:**

   | Attribute | Proposed System | BEP Requirement | Compliant? |
   |-----------|----------------|-----------------|------------|
   | Discipline codes | Single-letter (A, S, M, E) | Two-letter (AR, ST, HV, EL) | NO — critical |
   | Format structure | Disc+Type+Seq (A-102) | Container code per ISO 19650 | OK for title block only |
   | Sequential digits | 2-digit (01) | 3-digit (001) | NO — minor |
   | Missing disciplines | (check BEP codes not covered) | ID, INF, GAS, LS | NO — moderate |

4. **Flag critical vs minor issues:**
   - **Critical**: discipline codes don't match BEP Table 30
   - **Moderate**: missing disciplines the BEP covers
   - **Minor**: digit length, separator conventions

5. **Check ISO 19650 compliance separately:**
   - The full container code (Project-Originator-Volume-Level-Type-Discipline-Number) at CDE level must be distinct from the simplified title-block code
   - The simplified code is acceptable if the container code is maintained separately
   - The document itself should acknowledge this distinction

6. **Report with table** — discipline codes mismatch, missing disciplines, digit length, and any BEP internal inconsistencies (like Table 31 contradicting Table 30).

---

## 5. Requisite Specialist Codes (For BEP Form / TIDP / MIDP)

When you need codes for specialist packages that aren't in the BEP's base list (e.g. for a BEP Form or drawing register), use these based on the project's subcontractor structure:

| Package | Recommended Code | Logic |
|---------|-----------------|-------|
| **Interior Design** | `ID` | Separate discipline from Architecture contract |
| **Landscape** | `LS` | Already used in Landscape register (LS-001) |
| **AV (Audio Visual)** | `AV` | Already used in AV register (AV-001) |
| **3D Visualization** | `VIZ` | Not a separate sub — falls under AR or Exhibition Designer |
| **Lighting** | `LG` | Already used in Lighting register (LG-001) |
| **General Arrangement** | `GA` | Under Architecture as TYPE (AR-GA) |
| **Showcases** | `SC` | Subcontractor 05_Showcases_Contractor |
| **Exhibition Fit-Out** | `EFO` | Subcontractor 08_Exhibition_FitOut_Contractor |
| **Graphics** | `GR` | Subcontractor 03_Graphics_Contractor |
| **FFE** | `FFE` | Subcontractor 07_FFE_Contractor |
| **Fire Life Safety** | `FLS` | Subcontractor 11_FLS_Specialist_Contractor |
| **Rigging** | `RG` | Subcontractor 06_Rigging_Contractor |

---

## 6. How to Organize in BEP Form (TIDP/MIDP)

### In the MIDP (Master Information Delivery Plan)

| WBS | Deliverable | Discipline Code | LOD | Format |
|-----|------------|----------------|-----|--------|
| 4.1 | General Arrangement Drawings | AR (GA) | 350-400 | PDF, DWG |
| 4.2 | Interior Design Layouts | ID | 400 | PDF, DWG |
| 5.1 | Landscape Plans | LS | 350-400 | PDF, DWG |
| 6.1 | AV System Layouts | AV | 400 | PDF, DWG |
| 7.1 | Lighting Plans & Details | LG | 400 | PDF, DWG |
| 8.1 | 3D Visualization Views | VIZ | N/A | Image, PDF |

### In the Drawing Register (if separate codes per specialist)

Two options:

**Option A — Extended DISC field:** Add new discipline rows to the BEP's discipline code table:

| DISC Code | Discipline |
|-----------|-----------|
| AR | Architecture (incl. GA) |
| ID | Interior Design |
| LS | Landscape |
| AV | Audio Visual |
| LG | Lighting Design |
| VIZ | 3D Visualization |
| SC | Showcases |
| EFO | Exhibition Fit-Out |
| GR | Graphics |
| FFE | Furniture, Fixtures & Equipment |
| FLS | Fire Life Safety |
| RG | Rigging |
| ST | Structure |
| ME | Mechanical |
| EL | Electrical |
| PL | Plumbing |
| FP | Fire Protection |
| IT | IT / Networks / Security |

**Option B — Keep AR master, extend TYPE field:**

```
DISC = AR (Architecture)
TYPE = GA (General Arrangement)
TYPE = ID  (Interior Design drawings)
TYPE = LS  (Landscape drawings)
TYPE = AV  (AV drawings)
TYPE = LG  (Lighting drawings)
TYPE = VIZ (3D Views/Renders)
```

---

## 7. Subcontractor Numbering

The project uses `NN_Discipline_Contractor` for folders:

| # | Contractor | Code |
|---|-----------|------|
| 01 | Replica Model Contractor | Replica Model |
| 02 | Lighting Designer | Lighting |
| 03 | Graphics Contractor | Graphics |
| 04 | AV IT Contractor | AV/IT |
| 05 | Showcases Contractor | Showcases |
| 06 | Rigging Contractor | Rigging |
| 07 | FFE Contractor | FFE |
| 08 | Exhibition Fit-Out Contractor | Fit-Out |
| 09 | Interactive Design Contractor | Interactive |
| 10 | MEP Contractor / Oddy Testing | MEP |
| 11 | FLS Specialist / Structural | FLS / ST |
| 12 | Structural Contractor | ST |
| 13 | MEP Designer | MEP |
| 14 | CITC Telecom Engineer / MEP Contractor | Telecom |
| 18 | Acoustic Specialist | Acoustic |
| 21 | Landscaping Specialist | LS |
