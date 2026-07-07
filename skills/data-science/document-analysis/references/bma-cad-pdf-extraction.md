# BMA CAD PDF Extraction Reference

## Source Document Pattern
Boris Micka Associates (BMA) scenography PDFs — Detail Design stage, exported from AutoCAD/Vectorworks.

### Drawing Code System
```
GROUP.ZONE.PACKAGE.SEQUENCE
Example: S.CF.CS.01 = Supporting, Café, Current State, Sheet 01
```

### Zones Covered
| Code | Area | Typical Scale |
|------|------|---------------|
| CF | Café Area | A1 1:37.5 |
| FL | Female Lounge | A1 1:20 |
| SM | Studio/Meeting Area | A1 1:15 |
| LB | Library Area | A1 1:20 |
| MJ | Majlis Area | A1 1:20 |
| FY | Foyer Area | A1 1:20 |
| BR | Break Area | A1 1:20 |
| CA | Central Area | A1 1:75 |

### Package Types
| Code | Description |
|------|-------------|
| CS | Current State |
| CR | Construction Requirements |
| ID | Interior Design |
| DT | Details (joinery, cabinetry) |
| LI | Lighting |

---

## Critical Disclaimer Language

Search extracted text for these phrases — they limit MEP scope to "indicative" only:

1. "These drawings are for indicative and notional purposes only, showing hypothetical locations of MEP services"
2. "Refer to MEP documentation for final locations and routing of all MEP elements shown"
3. "This document section only includes remaining MEP elements and modifications proposed to the existing MEP equipment"
4. "Refer to Package Lighting for details on lighting power supply"
5. "Refer to Package Audiovisual Hardware for details on Audiovisual Hardware power supply"
6. "Refer to Power supply requirements for power supply needs of interior elements"

---

## MEP Fixture Legends (Extracted from BMA RCRC December 2025)

### LV Power (S.ZZ.CS.11)
- 13A, 230V, one gang wall mounted switched socket outlet
- 13A, 230V, two gang wall mounted switched socket outlet
- Modular flush floor service outlet box, 3 compartments equipped with:
  - 1NO. (13A, 2 gang socket outlet 230V for NORMAL)
  - 1NO. (13A, 2 gang socket outlet 230V for UPS)
  - 1NO. (RJ45 data socket outlets for IP telephony & data)
- Floor junction box for future use
- 25A wall mounted double pole switch, serving E.W.H.
- Hand dryer unit 2.25kVA, 230V, 60Hz with photo cell
- Three phase final distribution board
- Normal power conduit 25mmØ PVC & 3/4" EMT conduit
- UPS power conduit 25mmØ PVC & 3/4" EMT conduit
- 300mm WIDTH x 75mm DEPTH x 1.5mm THICKNESS, 3 compartment heavy duty galvanized trunking

### Construction Requirements LV Power (S.ZZ.CR.07) — additional:
- Insect killer
- Electric floor boxes
- Electric curtain
- Furniture-mounted power + USB

### IP Data & Telephony (S.ZZ.CS.12)
- RJ45 socket outlet which can be used as IP telephony or data
- Ceiling-mounted WAP (Wireless Access Point)
- 300×75mm 3-compartment trunking
- 25mmØ PVC & 3/4" EMT conduits

### Fire Alarm System (S.ZZ.CS.13)
- Addressable optical smoke detector (ceiling mounted)
- Addressable optical smoke detector (above false ceiling)
- Conventional flasher wall mounted, weatherproof
- Weatherproof conventional siren
- Control module
- PAD-4 auxiliary supply
- Pull station
- Fire telephone jack socket
- Isolator short circuit
- Beam type smoke detector (transmitter) to be installed in roof slab
- Fire-rated cabling: 2×1.5mm² / 2×2.5mm² in 25mmØ PVC & 3/4" EMT
- Demolition note: "Existing fire alarm devices are to be relocated to suit new ceiling height"

### Lighting (S.ZZ.CS.14)
- 27W LED recessed down lighting fixture (round shape) with heatsink, bracket, addressable DALI ballast, central battery system
- 48W LED recessed down lighting fixture (round shape) with IP44 protection glass, addressable DALI ballast
- 7W LED spot down light type, 220V main power, Ø11cm, IP20
- 2×36W surface mounted fluorescent lighting fixture, sheet steel base, opal polycarbonate diffuser
- Backlit panel ceiling
- AV Panel (symbol)
- Lighting distribution panel
- Grid switch panel
- 1 gang normal & emergency switch
- Exit signage
- Lighting conduit normal / emergency

### HVAC (S.ZZ.CS.15)
- VAV boxes
- Volume control dampers
- Thermostats
- Four diffuser types: LSCD (Linear Supply Ceiling Diffuser), LRCD (Linear Return Ceiling Diffuser), LSSD (Linear Supply Side Diffuser), LRSD (Linear Return Side Diffuser)

### Plumbing (S.CA.PL.01 — Planters)
- Drainage cells wrapped around with filter fabric
- Drainage outlet
- Water proofing membrane
- 50mm thick protection screed
- RCC structure
- FAUCET and SINK symbols in cafe/break areas

---

## RFI Cross-Reference Example (RCRC Exhibition, 26 June 2026)

### Source: `2025_12_21 RCRC EXPERIENCE SUPPORTING AREAS INTERIOR DESIGN.pdf`
### Target: `RFI_RCRC_Experience_Exhibition_001.docx` (4 RFIs, 27 questions)

| RFI | Total Qs | CONFIRMED | PARTIAL | NOT IN SCOPE |
|-----|----------|-----------|---------|--------------|
| RFI-01 Electrical | 8 | 2 (Q6, Q7) | 3 (Q3, Q5, Q8) | 3 (Q1, Q2, Q4) |
| RFI-02 Mechanical/MEP | 6 | 2 (Q2, Q6) | 2 (Q3, Q4) | 2 (Q1, Q5) |
| RFI-03 AV Headend | 6 | 0 | 1 (Q4) | 5 (Q1, Q2, Q3, Q5, Q6) |
| RFI-04 Site Logistics | 7 | 0 | 0 | 7 (all) |
| **TOTAL** | **27** | **4** | **6** | **17** |

**Key takeaway**: The BMA interior design document answered 4 of 27 RFI questions (15%) with confidence. It cannot answer ANY building infrastructure questions (electrical rooms, mechanical rooms, AV headend, site logistics). Those need MEP/ELV building drawings from the main contractor/PMC.

### Extraction Method
```
pdftotext -layout "input.pdf" /tmp/output.txt
wc -l /tmp/output.txt  # 8,705 lines (text), 15,492 lines (structured)
```
- Text extraction captured all fixture legends and notes
- Graphical element placement (actual fixture coordinates on plans) was NOT extractable
- Room dimensions appeared as scattered text fragments from CAD line artifacts

### Workflow Pattern
1. Extract PDF → text with `pdftotext -layout`
2. Search for disclaimer language FIRST → determine document scope limits
3. Extract fixture legends from drawing legend blocks
4. Cross-reference each RFI question against extracted content
5. Classify as CONFIRMED / PARTIAL / NOT IN SCOPE
6. For CONFIRMED answers: draft response with specific sheet references
7. For NOT IN SCOPE: list required source documents (MEP drawings, site logistics plan, etc.)