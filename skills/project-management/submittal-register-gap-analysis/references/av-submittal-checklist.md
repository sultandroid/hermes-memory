# AV Submittal Register — Standard Checklist

## Gate 1 — Detailed Design (31 items)

### Design Philosophy & Criteria
- ASE-AV-REP-001 — AV Design Basis Report
- ASE-AV-SCH-001 — AV Equipment Schedule & Technical Specifications
- ASE-AV-REP-002 — AV Design Criteria (codes, standards, acoustics)
- ASE-AV-DWG-001 — AV System Architecture & Signal Flow Diagrams

### Coordination with MEP/Structural
- ASE-AV-CAL-001 — AV Rack Room Layouts, Power & Heat Load Calculations
- ASE-AV-DWG-002 — AV Containment & Infrastructure Layouts (conduits, floor boxes, cable trays)
- ASE-AV-DWG-003 — AV Mounting, Fixing & Support Details (weights, brackets, structural loads)

### Studies (after Arch 50%)
- ASE-AV-REP-003 — AV Sightline, LUX & Projection Study
- ASE-AV-REP-004 — AV Audio Coverage & Acoustic Integration Study

### System Designs (after Arch 50%)
- ASE-AV-SYS-001 — Display System Design (LCD/LED screens, monitors)
- ASE-AV-SYS-002 — Video Projection System Design (projectors, screens, lenses)
- ASE-AV-SYS-003 — Audio System Design (speaker coverage, zones, amplification)
- ASE-AV-SYS-004 — Show Control System Design (control logic, interfaces, scheduling)
- ASE-AV-SYS-005 — Video Distribution System Design (matrix, routing, switching)
- ASE-AV-SYS-006 — Digital Signage System Design (players, displays, CMS)
- ASE-AV-SYS-007 — Intercom & Communication System Design
- ASE-AV-SYS-008 — Assistive Listening & Accessibility Systems

### Content-Hardware Interface
- ASE-AV-REP-005 — AV Content-Hardware Interface Specification

### BIM Models
- ASE-AV-BIM-001 — AV BIM Model LOD 300 (coordination model)
- ASE-AV-BIM-002 — AV BIM Model LOD 350 (design model)

### Coordination Submittals (commonly missed)
- ASE-AV-REG-001 — AV Interface Register (NRS/MEP/Lighting/Showcase coordination)
- ASE-AV-SYS-006 — CCTV / ELV System Design
- ASE-AV-REP-004 — Wireless Coverage / Heat Map Study (43 WAPs)
- ASE-AV-CAL-004 — Structural Loading Calculations for AV Mounts
- ASE-AV-SPC-002 — DALI / BMS Interface Specification
- ASE-AV-COO-001 — Showcase AV Interface Submittal (GBH coordination)
- ASE-AV-DWG-005 — AV Setwork Housing Drawings (equipment in joinery)
- ASE-AV-REP-005 — Cybersecurity Hardening Report
- ASE-AV-REP-006 — Acoustic Integration Report (RT60, sound bleed)
- ASE-AV-REP-007 — AV Content-Hardware Interface Matrix

## Gate 2 — Material Approval (2 items)
- AV-MAT-001 — AV Material Submittals Register (Live-Sync)
- AV-MAT-002 — AV Equipment Submittals (displays, projectors, speakers, amps, cables)
- AV-MAT-003 — Pre-qualification Submittals (PQ-0056 Panasonic + others)

## Gate 3 — Coordinated IFC (10 items)
- AV-IFC-BF — Basement Floor IFC Package
- AV-IFC-LGF — Lower Ground Floor IFC Package
- AV-IFC-GF — Ground Floor IFC Package
- AV-IFC-1F — First Floor IFC Package
- AV-IFC-2F — Second Floor IFC Package
- AV-IFC-RF — Roof Floor IFC Package
- AV-IFC-SPEC — AV Technical Specifications
- ASE-AV-BIM-003 — AV BIM Model LOD 500 / As-Built
- AV-QA-001 — AV ITP — Inspection & Test Plan
- AV-HO-003 — AV Spares — 1-year period

## Gate 4 — Testing, Commissioning & Handover (8 items)
- AV-QA-002 — AV Commissioning Report
- AV-FAT-001 — FAT — Factory Acceptance Test Documentation
- AV-SAT-001 — SAT — Site Acceptance Test
- AV-CBL-001 — Cable Test Certification (Cat6A class EA, OS2 fibre)
- AV-NET-001 — Network Switch Configuration & VLAN Scheme
- AV-SEC-001 — Remote Access Policy (security · maintenance windows)
- AV-HO-001 — AV O&M Manual
- AV-HO-002 — AV Training for MoC — system operation & maintenance

## Common Gaps in Subcontractor Registers
1. **BIM models** — subcontractors almost never include LOD300/350/500
2. **Per-floor IFC** — they lump all floors into one package; split per floor with staggered dates
3. **Coordination submittals** — Interface Register, setwork housings, showcase AV interface, DALI/BMS
4. **Post-install deliverables** — FAT, SAT, cable test certs, network config, cybersecurity
5. **Already-submitted items** — register starts from scratch, omits items already submitted (e.g., IFC-0008)
6. **No drawing codes** — items lack proper ASE-AV-xxx codes
7. **No programme links** — Linked Activity ID column left empty
8. **All status = "Planned"** — no tracking of actual progress
9. **Unrealistic dates** — all IFC on same date, no time for CG review + procurement + install
