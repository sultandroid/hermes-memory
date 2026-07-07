# Week 24 (Jun 6-7, 2026) — Pipeline Findings

## Jun 7 Run — New Emails Downloaded & Filed

**32 files** downloaded from Outlook (Week 23 archive), **22 project-relevant files** filed to BIM Unit structure. Download script ran in background for ~5 min then killed (full inbox of 18,151 is too slow via AppleScript, but the most recent week was successfully captured).

### CG Verdicts Confirmed & Filed

| Doc Ref | Description | Status | File Path |
|---------|-------------|:------:|-----------|
| MOC-MUS-ASE-1KH-PL-0043 Rev.01 | Temporary Electrical Mgmt Plan | **✅ Code B** | `02_Correspondence_MOC/` |
| MOC-MUS-ASE-1KH-PL-0045 | Heat Stress Management Plan | **✅ Code B** | `02_Correspondence_MOC/` |
| MOC-MUS-ASE-1K0-PL-0018 Rev.01 | Project Communication Plan | **❌ Code C** (resubmit) | `02_Correspondence_MOC/` |
| MOC-MUS-CG-ASE-1KN-PQ-013 | ICT Security System Integrator PQ | Corresp. filed | `02_Correspondence_MOC/` |
| Site Instructions | ICT Security Integrator (updated 20/05) | SI filed | `02_Correspondence_MOC/` |

### New Proposals & Docs Filed to Design Files/00_Scope_and_Proposals/

| File | Description |
|------|-------------|
| Aseer 2026 FEE PROP_S4_S5_010626_StudioZNA.pdf | StudioZNA fee proposal (lighting design, RIBA Stage 4) |
| Aseer 2026 SCOPE of works 010625_StudioZNA.pdf | StudioZNA scope of works |
| 35-العرض الفني والمالي - Structural quotation | Heritage Sites (already on file, skipped) |

### Other Files Filed

| File | Destination | Notes |
|------|-------------|-------|
| CG RE MOC-MUS-ASE-1KH-PL-0043 Rev.01 - Reply.pdf | `02_Correspondence_MOC/` | 13.3 MB |

Extracted from this session's pipeline run. **No new emails downloaded** — inbox is current through Week 23. Findings below are from re-scanning existing `23.md` for CG verdicts not captured in the PENDING updates (which only tracked new submissions, not responses).

## New CG Verdicts Found in 23.md (Missing from PENDING Updates)

| Doc Ref | Description | Actual Status | PENDING Entry Had | Source |
|---------|-------------|:-------------:|-------------------|--------|
| MOC-MUS-ASE-1KH-PL-0043 Rev.01 | Temporary Electrical Mgmt Plan | **✅ B - Approved** | "under review" | CG/Mohammad Elbaz, 2 Jun |
| MOC-MUS-ASE-1E0-PQ-0056 Rev.01 | Panasonic Projector (resubmit) | **✅ B - Approved w/ Comments** | "product queries ongoing" | CG, 4 Jun |
| MOC-MUS-ASE-1KH-PL-0045 | Heat Stress Management Plan | 🔄 Under CG Review | (not mentioned) | CG, 1 Jun |
| MOC-ASEER-0PS-SH-006 Rev.03 | Master Schedule (resubmit) | **❌ C - Revise & Resubmit** | "resubmitted for approval" | CG, 4 Jun |
| ZAM-NWC-CTR-CLR-MEP-003 | MEP Site Clearance | **✅ Approved** | (not mentioned) | EGEC/Habib → Almakarem, 4 Jun |

## New Meeting Outcomes (from 23.md)

| Meeting | Date | Key Outcome |
|---------|:----:|-------------|
| **EV & Visualisation Progress Meeting** | 4 Jun @ 14:00 | 3D visualizations to be delivered WITH detailed-drawings submissions; programme extension impacting invoicing/resources |
| **Progress Meeting No. 12** | — | Postponed to after Eid Al-Adha holiday |
| **Structural Model meeting** | 1 Jun | Quotation from Heritage Sites consultancy (Ahmed Gad/A. Farag); doc: 35-العرض الفني والمالي |

## New Submissions (from 23.md, not in PENDING)

| Doc Ref | Description | Type |
|---------|-------------|:----:|
| MOC-MUS-ASE-1K0-ZD-0050 | MEP Design Team | General Doc |
| MOC-MUS-ASE-1M0-ZD-0051 | Mechanical Mobilization Layout | General Doc |
| MOC-MUS-ASE-1A0-TQ-0026 | Content Research Deliverables Formal Request | Technical Query |
| MOC-MUS-ASE-1C0-IR-0002 | Temporary Fence Installation | Inspection Request |

## Zamzam New (not in PENDING)

| Doc Ref | Description | Status |
|---------|-------------|:------:|
| ZAM-NWC-CTR-CLR-MEP-003 | MEP Site Clearance — Columns B:16-20, Walls A/C:14-20 | ✅ Approved |

## PROJECT_MEMORY.md Update Status

| Copy | Path | Status |
|------|------|:------:|
| **Canonical** | `Aseer-Museum/_Project_Memory/PROJECT_MEMORY.md` | Updated Jun 5 17:31 (51KB, OneDrive-locked). PENDING updates APPLIED. |
| **Scripts** | `Aseer-Museum/Scripts/PROJECT_MEMORY.md` | Updated Jun 6 by pipeline (23KB). Appended new CG verdicts from 23.md. |

## Pipeline Status

| Component | Status | Notes |
|-----------|:------:|-------|
| `download_mails.py` | ✅ Exited 0 | No new emails — inbox current through Week 23 |
| Attachments (`mails/attachments/`) | ✅ Empty | All prior files routed (238 filed, 491 skipped) |
| PENDING updates | ✅ Already applied | PENDING_PROJECT_MEMORY_UPDATES.md says "APPLIED on 2026-06-05" |
| Missing BIM folders | ⚠️ 2 missing | `14_MEP_Contractor` → use `12_MEP_Installation`; `99_Images` → needs `mkdir -p` |
