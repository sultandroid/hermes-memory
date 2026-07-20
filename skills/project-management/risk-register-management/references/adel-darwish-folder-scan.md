# Adel Darwish Folder Scan — Aseer Museum

> Results of scanning all 20 folders in Adel Darwish's OneDrive execution documents.
> Scanned 2026-07-19. Use this to avoid re-scanning.

## Source Path

```
/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Adel  Darwish's files - 01- Execution Documents/
```

## Folder Assessment

| # | Folder | Content | Useful? | Action Taken |
|---|--------|---------|:-------:|-------------|
| 01 | Letters | 20 OUT letters (Samaya→CG) + 2 IN letters (CG→Samaya) — formal correspondence, RFIs, submissions | ✅ Yes | Created `letters_register.md` |
| 02 | DOC - Document Submittal | 93 GN document submittals (ZD series) | ❌ Already in submittal register | Skipped |
| 03 | SD - Shop Drawing | 5 shop drawing packages | ❌ Minimal, already tracked | Skipped |
| 04 | Daily Report | Daily reports by month | ⚠️ Low priority | Skipped |
| 05 | RFI | 23 RFI/TQ folders | ✅ Yes | Created `rfi_register.md` |
| 06 | Weekly Meeting MOM | 15 meeting minutes (MOM-02 to MOM-15) | ✅ Yes | Updated `meeting_minutes_register.md` |
| 07 | Pre-Qualification | 100+ PQ submissions | ❌ Already tracked | Skipped |
| 08 | Material Submittal MA | Material submittals | ❌ Already tracked | Skipped |
| 09 | Method Statement | 16 MS documents | ⚠️ Low priority | Skipped |
| 10 | CG Site Instruction SI | 20 SIs (SI-01 to SI-20) | ✅ Yes | Created `si_register.md` |
| 11 | IFC Drawing | 8 IFC packages | ❌ Already tracked | Skipped |
| 12 | NCR | 11 NCR folders | ✅ Yes | Updated `ncr_register.md` |
| 13 | Weekly Report | 18 weekly reports | ✅ Yes | Created `weekly_report_index.md` |
| 14 | Inspection Request (IR) | 3 IRs (safety handrail, temp fence, survey) | ❌ Site operational records | Skipped |
| 15 | Start New Activity (SNA) | 7 SNAs (glass dismantling, electrical/mechanical) | ❌ Operational notifications | Skipped |
| 16 | Safety Notices | 1 safety notice (building power use) | ❌ Covered by SI-09/SI-11 | Skipped |
| 17 | SOR | 9 HSE safety observation reports | ❌ HSE operational | Skipped |
| 18 | MIR | 1 material inspection request | ❌ Single record | Skipped |
| 19 | Weekly HSE Reports | Only Week 19 available | ❌ Too sparse | Skipped |
| 20 | DDD | 6 architecture DD gate submittals | ❌ Already in submittal register | Skipped |

## Registers Created/Updated

| Register | File | Content |
|----------|------|---------|
| Letters | `01_Registers/letters_register.md` | 20 OUT + 2 IN letters with dates, subjects, linked risks |
| RFI/TQ | `01_Registers/rfi_register.md` | 22 TQs with subjects, linked risks |
| MOM | `01_Registers/meeting_minutes_register.md` | 13 meetings (MOM-02 to MOM-15) |
| SI | `01_Registers/si_register.md` | 20 SIs with PRR cross-references |
| NCR | `01_Registers/ncr_register.md` | 14 NCRs with linked risks |
| Weekly Reports | `01_Registers/weekly_report_index.md` | 18 reports indexed |

## Key Evidence Found for Risk Register

| Risk | Evidence | Source |
|------|----------|--------|
| PRR-COM-05 | LT-0001 (21-Apr), LT-0002 (21-May) — CG warning letters | Letters folder |
| PRR-FLS-01 | NC-1F0-007 — NAFFCO absent, fire alarm not started | NCR folder |
| PRR-PRC-05 | TQ-022 — powder coating alternative proposed | RFI folder |
| PRR-SIT-01 | SI-10 — 3D point cloud survey not started | SI folder |
| PRR-MEP-02 | SI-12 — BMS engineer withdrawn | SI folder |
| PRR-HSE-01 | SI-16 (detector tape), SI-17 (FACP disconnected), NC-1KH-009 (debris chute) | SI + NCR folders |
| PRR-CON-01 | SI-18 (hoarding), NC-1M0-005 (plumbing), NC-1G0-006 (WIR) | SI + NCR folders |
| PRR-PRC-04 | SI-13 (ICT PQ), NC-1E0-0010 (ICT delay), NC-1L0-0011 (landscape) | SI + NCR folders |
| PRR-SEC-01 | SI-13, NC-1E0-0010 | SI + NCR folders |
| PRR-MEP-01 | SI-19 (EL assessment delayed) | SI folder |

## OneDrive Read Safety

Read PDFs one at a time using `pdftotext` (poppler). Do NOT batch-read or use `read_file` on PDFs — OneDrive sync hangs on bulk reads. Pattern:

```bash
pdftotext -layout "/path/to/file.pdf" - 2>/dev/null | head -40
```

For Arabic PDFs, use `-raw` instead of `-layout` to avoid encoding artifacts.
