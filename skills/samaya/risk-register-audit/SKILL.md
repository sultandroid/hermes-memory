---
name: risk-register-audit
description: "Audit Aseer Museum risk register entries against real evidence from repo + Adel Darwish bank. Verify owners, dates, evidence, status, PxS, and factual claims before updating."
---

# Risk Register Audit Workflow

## Purpose
Verify all risk register entries against real evidence before updating. Every claim must be traceable to a real file or record.

## Evidence Sources (in priority order)

| Source | Path | What to Check |
|--------|------|---------------|
| Submittal register | `01_Registers/submittal_register.md` | Real submission/approval dates, CG codes |
| NCR register | `01_Registers/ncr_register.md` | Open NCR count, specific NCR references |
| RFI register | `01_Registers/rfi_register.md` | TQ/RFI status |
| Drawing register | `01_Registers/drawing_register.md` | Drawing status, phase |
| Prequalification log | `Technical_Office/Specialist_Management/prequalification_log.md` | PQ status, CG codes |
| Master programme | `02_Schedule/master_programme.md` | Schedule dates, milestones |
| Submission plan | `02_Schedule/submission_plan_risk_assessment.md` | Submission forecast dates |
| Treatment files | `03_Plans/08_Risk/treatment/` | Risk-specific response plans |
| Adel Darwish bank | `OneDrive/Adel Darwish's files - 01- Execution Documents/` | Physical file existence |

## Adel Darwish Bank Structure

```
Adel Darwish's files - 01- Execution Documents/
├── 01- Letters/           (LT-0027 EOT, etc.)
├── 02. DOC/               (Document submittals)
├── 03. SD/                (Shop drawings — SDW prefix)
├── 04- Daily Report/
├── 05- RFI/               (TQ-001 through TQ-022+)
├── 06- MOM/               (MoM-14, MoM-15, etc.)
├── 07- PQ/                (PQ-0007 through PQ-0125+)
├── 08- Material Submittal MA/  (MA-0001 through MA-0007)
├── 09- MS/                (Method statements)
├── 10- SI/                (SI-01 through SI-20)
├── 11- IFC/               (IFC-0003, IFC-0004, etc.)
├── 12- NCR/               (NC-001 through NC-1KN-SE-021)
├── 13- Weekly Report/
├── 14- IR/
├── 15- SNA/
├── 16- Safety/
├── 17- SOR/
├── 18- MIR/
├── 19- HSE/
├── 20- DDD/
```

## Audit Checklist (per risk)

| Check | What to Verify | Source |
|-------|---------------|--------|
| Owner | Site/construction risks -> Construction Manager, not Technical Office Mgr | Risk register + treatment file |
| Dates | target_close must be realistic, not past due without status update | Submittal register |
| Evidence | References must point to real files in repo or Adel bank | search_files + ls on OneDrive |
| Status | Open/Watch/Mitigated/Closed must match current reality | NCR register, submittal register |
| PxS | Must be consistent with actual severity (>=12=Critical, 8-11=High, 4-7=Medium, <=3=Low) | Calculate from P and S |
| Factual claims | Every claim (e.g. "IFC-0004 Rev.01 Code C") must be traceable | Cross-reference submittal register |

## Common Discrepancies Found

| Issue | Frequency | Fix |
|-------|-----------|-----|
| Owner = Technical Office Mgr for site risks | 2 instances (PRR-FLS-01, PRR-DES-07) | Change to Construction Manager |
| Evidence references to non-existent files (DDR-*, GAP-*) | 12+ instances | These exist in OneDrive/Aconex, not repo |
| NCR count understated | 2 instances (PRR-QLT-01, PRR-STK-02) | Update to actual count from ncr_register.md |
| SI count understated | 1 instance (PRR-QLT-01: "15 SIs" -> 20) | Update to actual count from Adel bank |
| Unverifiable evidence references (ZD-0076, ZD-0082) | 2 instances | Add to submittal register or correct reference |
| Blank target_close on High/Critical risks | 9 instances | Add realistic target dates |
| Target_close = today with Open status | 3 instances | Review for closure or extension |

## Deploy After Fixes

```bash
cd /Users/mohamedessa/aseer-museum-pm/06_Risk_System/webapp
bash deploy.sh
# Publishes to https://samaya-factory.com/aseer/registers/Risk/
```

The deploy script:
1. Reads `../risks.json` (source of truth)
2. Builds `src/index.html` (self-contained, 163KB)
3. Copies master Excel workbook to `src/`
4. Rsyncs to Hostinger `/build/aseer/registers/Risk/`

## OneDrive Deadlock Workaround

When reading files from Adel Darwish's bank, OneDrive may return "Resource deadlock avoided":
1. Quit OneDrive: `osascript -e 'tell application "Microsoft OneDrive" to quit'`
2. Wait 3-5 seconds
3. Retry the read
4. If still failing, use `strings` command instead of `pdftotext` for PDFs
5. Restart OneDrive after done
