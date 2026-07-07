# HTML Print-Ready Proposal Workflow (Samaya Tenders)

## Overview

Build bilingual (Arabic/English) A4 print-ready HTML proposals for Samaya tenders. Deployed to Surge.sh.

## Design System

| Element | Value |
|---------|-------|
| Theme color | `#B01E2F` (red) |
| Arabic font | IBM Plex Sans Arabic |
| English font | Inter |
| Mono font | JetBrains Mono |
| Page | A4 portrait (794×1123px @96dpi) |
| Print @page | `size:A4 portrait; margin:10mm 0` |
| Screen | responsive with breakpoint at 830px |

## Structure Rules

- **Cover** → TOC → Executive Summary → Scope → Capabilities → Technical Specs → Datasheets → BOQ → Timeline → Lighting → Company → Payment → Terms → Sign-off
- **Technical Specs + all Material Datasheets = ONE section** — never split them
- Data sheets in order: Overview table → Banner TDS → Cement Board TDS → Jotun Epoxy TDS → LED Flood Light TDS
- All 4 datasheets sit consecutively (Banner, Cement Board, Jotun, LED)
- Each page is `<section class="page" id="page-N">`
- Footer: `Samaya Investment · سمايا الاستمارية` + `samaya-factory.com` (with QR) + `Page <b>NN</b> / TT`

## TOC Requirements

- 4 category groups with icons:
  - 📋📊 Project Introduction
  - 🔧📐📦 Technical Scope
  - 📅💡 Execution Plan
  - 🏢💰⚖️✍️ Company & Commercial
- Each item is clickable anchor link: `<a href="#page-N" style="text-decoration:none;color:inherit">`
- Never change the text style of TOC links
- Page numbers must match actual footer numbers

## Content Rules

- No galvanized steel references — always Epoxy paint (Jotun Epoxy Mastic)
- Steel profile is HSS without specific dimensions (per structural calculation)
- Cladding is Cement Board 12mm (not ACP or PVC-only)
- PVC Flex Banner is mounted ON the cement board surface (substrate)
- Gates: 1 vehicle gate (6m×8m) + 1 pedestrian gate (1.2m×2.1m)
- LED light count: based on net fence length minus gate openings (~118 for 1,426m minus 7.2m gates)
- Client: شركة الغربية للتطوير والاستثمار المحدودة (Al Gharbia Development & Investment Co. Ltd.)
- Location: مواقف الزايدي — مكة المكرمة
- SBC-Makkah code reference specific to Makkah region
- All tables use compact padding (spec-table: 2px 8px, ds-table: 4px 10px)

## Implementation

1. Build/update in Al_Zaidi_Technical_Proposal_Print_Ready.html (source)
2. Copy to index.html for deployment
3. Deploy from /tmp/ (not OneDrive path — causes Surge failures)
4. Always use patch() — never regenerate entire HTML

## Delegation

- Delegate design, restructure, and content changes to Claude Code via delegate_task
- Provide explicit file path, project context, and numbered change list
- Verify changes after Claude returns

## Casing

Cover → TABLE OF CONTENTS → EXECUTIVE SUMMARY → DEFINED SCOPE OF WORK → CAPABILITIES → TECHNICAL SPECIFICATIONS → DATA SHEET · BANNER & UV PRINTING → DATA SHEET · CEMENT BOARD 12MM → MATERIAL DATASHEET: JOTUN EPOXY MASTIC → BOQ PART 1 → BOQ PART 2 + PAYMENT TERMS → METHODOLOGY → PROJECT TIMELINE → DATA SHEET · LED FLOOD LIGHT → COMPANY DOCUMENTS & CERTIFICATIONS → BOQ PART 3 + PAYMENT + TERMS → TERMS + SIGN-OFF
