---
title: Aseer Register Scope Validation & Reorganization (June 2026)
---

# Register Scope Validation & Reorganization

## Core Principle: Verify Against BOQ Before Creating Registers

Never create a submittal register based on assumptions. Verify against:
1. **BOQ** (`05_BOQ/` — sheets like `004. Furniture`, `05. Display Cases`, `009. Graphics`)
2. **Actual subcontractor registers** (in `24_Subcontractors/`) 
3. **Who actually delivers** the item (NRS design vs external vendor vs joinery subcon)

## Scope Mapping by BOQ Sheet

| BOQ Sheet | What's in it | Register | Notes |
|-----------|-------------|----------|-------|
| 001-003 (Design, Enabling, Finishes) | Exhibition design deliverables per floor | **Architecture** | NRS scope — drawings, specs, sections, details |
| **004. Furniture** | Loose furniture only — lobby, VIP, cafe, terrace, circulation, library | **FFE** | NO fixed/bespoke items. Procurement tracking only (catalog, TDS, sample, compliance) |
| **05. Display Cases** | Display case schedule by type | **Showcase** | Separate register exists |
| 006 (Lighting & Power) | Lighting fixtures, power, data | **Lighting** | Design by ZNA, installation by MEP |
| 007 (Security, Data, Life Safety) | Security, CCTV, access control, FLS | **FLS** + separate disciplines |
| 008 (Plumbing & Mechanical) | HVAC, plumbing, BMS | **MEP** |
| **009. Graphics** | Graphic artwork, production, installation | **Graphics** | 🔴 **NO dates — RFI pending client research/data** |
| **010. Models and Replicas** | Physical models, replicas, object mounts | **Model Maker** | 🔴 **NO dates — RFI pending client research/data** |
| 011-012 (AV Hardware + AVS) | AV equipment, software, content | **AV/IT** |
| 013 (Setworks) | Scenography, setworks | **Setworks/Rigging** |

## Three Register Types (Critical Distinction)

| Type | What it tracks | Example | Format |
|------|---------------|---------|--------|
| **Design register** | Drawings, specs, schedules — what the designer produces | Architecture (NRS) | By floor/level, dates in stage columns |
| **Procurement register** | Vendor submittals — catalogs, TDS, samples, compliance | FFE (loose furniture) | By BOQ zone, dates in stage columns |
| **QA/Handover register** | Close-out items across ALL packages | QA_Commissioning_Handover | Consolidated, IFC-stage only |

## FFE Register: Design → Procurement rewrite

FFE was initially created with NRS design items (FF&E schedule, layouts, design intent). **Wrong.**

| Item | Who delivers | In FFE? |
|------|-------------|---------|
| FF&E schedule, layouts, design intent | NRS (Architecture register) | ❌ |
| Fixed/bespoke furniture (reception, shelving, counters, railings) | NRS designs → Joinery sub fabricates | ❌ |
| Display cases | Showcase subcontractor | ❌ |
| **Loose furniture** (sofas, chairs, tables, cafe, outdoor, rugs) | External vendors | ✅ **Yes — procurement only** |

## Exhibition Fit-Out: Deleted

Confirmed redundant. Items were either:
- NRS design (covered by Architecture register per floor)
- Generic subcontractor management (ITP, AFC, O&M — now in QA/Handover consolidated register)

## Graphics & Model Maker: No Dates

**RFI raised to client** for research and data. Stage columns use blank/— markers only, NOT dates. Legend notes "Dates TBC — RFI raised to client for research/data."

## OneDrive Folder Naming

On this project, the scripts folder is `_scripts` (underscore prefix sorts first), NOT `scripts`. Always check the actual folder name before running batch operations.

## QA/Commissioning/Handover: Consolidated Register

Single register tracking close-out across all 16 packages:
- Material Submittals, ITP, AFC, Commissioning, Record Drawings
- O&M, Training, Spares
- Package-specific items (Civil Defense for FLS, BMS Integration for MEP, etc.)

All IFC-stage only. One view for Technical Office to track handover readiness.
