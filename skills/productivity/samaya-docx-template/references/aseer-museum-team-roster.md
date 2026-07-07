# Aseer Museum — Project Team Roster

**Source:** MOC-ASEER-SIC-1K0-PL-0020 Rev.03 (05-JUN-26) Stakeholder Management Plan
**Cross-ref:** Stakeholder_Register_Update_Findings.md (16-JUN-26) + Email Archive

## Samaya Management (Tier 1 — QC / Key Personnel)

| SMP Code | Role | Name | Status |
|----------|------|------|--------|
| QC-01 | Project Manager | Eng. Adel Darwish | Active |
| QC-04 | Project Director | Eng. Adel Darwish (Interim) | Interim |
| QC-02 | Document Controller | Eng. Hesham Abdelhamid | Active |
| QC-03 | QA/QC Manager | Eng. Abdelmohaimen Medhat | Active |
| T1-01 | Project Director | Adel Darwish (Interim) | Active |
| T1-02 | BIM Manager | Dr. Waleed Salah | Active |
| T1-03 | T&C Manager | TBC | Target: CP-2 Decision |
| T1-04 | QA/QC Manager | Abdelmohaimen Medhat | Active |
| T1-05 | HSSE Manager | Eng. Mohamed Ahmed | Active |
| T1-06 | Site Manager | TBC | Target: CP-1 Mobilisation |
| T1-07 | IT/Security Specialist | TBC | CV via DS to be submitted |
| T1-08 | Procurement Manager | Samaya Procurement team | Active |

## Samaya Extended Team (from email findings)

| Name | Role | Email |
|------|------|-------|
| Eng. Mohamed Sultan | Tech Office Manager | sultan@samayainvest.com |
| Eng. Ahmed Salah | Project Engineer | Ahmed.salah@samayainvest.com |
| Eng. Ali Abdelrahman | BIM / Documentation | ali.abdelrahman@samayainvest.com |
| Mr. Hani Alghamdi | Procurement / Supply Chain | H.Alghamdi@samayainvest.com |
| Mr. Mohammed Hakami | Procurement / Contracts | m.hakami@samayainvest.com |
| Mr. Mohammed Al-Zeeny | Technical Director (AV/Interactive) | alzeeny@samayainvest.com |
| Eng. Mohamed Samir | Project Construction Mgr | m.samir@samayainvest.com |
| Mr. Kareem Hussain | Technical | Kareem.Hussain@samayainvest.com |
| Mr. Talha Yousaf | BIM | Talha.Yousaf@samayainvest.com |

## CG Consultant Team

| Name | Role | Email |
|------|------|-------|
| Eng. Mohammad Elbaz | CG Acting PM | melbaz@cg.com.sa |
| Eng. Hossam Mabrouk | CG Reviewer | hmabrouk@cg.com.sa |
| Eng. Maged Zamzam | Sr Architect / QC (drawing reviews) | mzamzam@cg.com.sa |
| Ms. Sundus Alfeer | CG Coordinator | salfeer@cg.com.sa |
| Eng. Abdrabo Shahin | CG Sr Structure/Reviewer | — |

## How to verify before writing

When generating any document that references project personnel:

```bash
# 1. Extract QC and T1 roles from SMP Rev03 HTML
grep -A2 'QC-0[1-4]' "/path/to/PL-0020_Rev03.html"
grep -A2 'T1-0[1-8]' "/path/to/PL-0020_Rev03.html"

# 2. Check Stakeholder_Register_Update_Findings for recent changes
grep -i "departure\|appointed\|new\|TBC\|KPR" ~/Stakeholder_Register_Update_Findings.md

# 3. Check UNIFIED_MEMORY for verified role assignments
egrep "PD|BIM Manager|QA/QC" ~/hermes-memory/unified/UNIFIED_MEMORY.md
```
