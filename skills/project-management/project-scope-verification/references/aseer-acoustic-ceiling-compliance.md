# Aseer Museum Acoustic/Ceiling Compliance — Session Context

## Files Reviewed
- **TOS-ASEER-TP-003-Rev00-Consolidated.pdf**
  - Path: `/Users/mohamedessa/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/9FD3B2CD-F1D0-4906-AF84-63748DE961CA/TOS-ASEER-TP-003-Rev00-Consolidated.pdf`
  - Key sections:
    - **Section 2**: BOQ Scope Mapping
    - **Section 3**: Acoustic Targets & Spaces
    - **Section 6**: Proposed Products & Value-Engineering
      - Product Equivalency Matrix
      - D1 Acoustic Performance Comparison
      - BoSpray 25mm Acoustic Spray
      - BoCoustic 40mm Acoustic Plaster

- **Aseer Museum of Art-Ceiling Finishes Package.pdf**
  - Path: `/Users/mohamedessa/Library/Containers/net.whatsapp.WhatsApp/Data/tmp/documents/6000D89A-81FB-4F96-9414-31D960CB3F11/Aseer Museum of Art-Ceiling Finishes Package.pdf`
  - Content: Binary-encoded drawings + material schedules for ceiling finishes (acoustic sprays, plasters, panels).

## TOS Requirements (Acoustic)

| Requirement | Target | Notes |
|-------------|--------|-------|
| **NRC** | ≥0.80 | Noise Reduction Coefficient (ASTM C423) |
| **CAC** | ≥35 | Ceiling Attenuation Class (ASTM E1414) |
| **Fire rating** | Class A | EN 13501-1 or BS 476 |
| **VOC emissions** | LEED EQ C4.2 compliant | ≤5 g/L |
| **Thickness** | 25mm (spray), 40mm (plaster) | Application method: spray/trowel |
| **Application** | Spray (BoSpray), Trowel (BoCoustic) | Substrate prep: concrete/gypsum board |

## Proposed Products (TOS Section 6)

| Product | Type | NRC | CAC | Fire Rating | VOC | Thickness |
|---------|------|-----|-----|-------------|-----|-----------|
| **BoSpray 25mm** | Acoustic Spray | 0.85 | 35 | Class A | 4 g/L | 25mm |
| **BoCoustic 40mm** | Acoustic Plaster | 0.90 | 40 | Class A | 3 g/L | 40mm |

## Ceiling Package Quirks
- **Binary PDF**: Drawings are encoded; use `read_file` with `offset`/`limit` for text extraction.
- **Material schedules**: Embedded in drawings (plans, sections, details).
- **Acoustic zones**: Gallery vs. back-of-house require different NRC/CAC targets.

## Compliance Workflow
1. **Extract TOS requirements** (NRC, CAC, fire, VOC, thickness).
2. **Extract product data** from supplier submittal (test reports, certificates).
3. **Cross-reference** product data against TOS.
4. **Flag deviations** (e.g., NRC 0.75 vs. TOS ≥0.80).
5. **Report compliance status** with evidence (test report excerpts, certificate numbers).