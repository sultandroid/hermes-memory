# Aseer Museum — 3D Scanner Procurement (Replica Package SC-01)

> Reference file for the Artec Space Spider II tender and scanner cost comparison.
> Updated: May 29, 2026

## Tender Folder Location

```
Samaya/Tenders/2026/Aseer Museum - Artec Space Spider Replica/01 RFQ/
├── RFQ-01.txt to RFQ-04.txt          (RFQ email texts — OneDrive locked)
├── Technical Proposal (SPIDER II).pdf
├── Artec Spider II.pdf               (10.7 MB — quotation PDF)
├── 00556 SAMAYA Investment spider 2.pdf
├── Spider-II-demo-VDI-VDE-certificate.pdf
├── RAK 2025.pdf
└── Sample stone photos (5 JPGs + 3 3D model renders)
```

Also accessible at:
- `_Unsorted_Emails/Email_Archive/Artec Spider II.pdf` (10.7 MB)

## Scanner Cost Comparison Workbook

**File:** `Aseer-Museum/Subcontractors/01_Replica_Model_Contractor/01_Schedule_and_BOQ/3D_Scanner_Cost_Comparison.xlsx`

**5 sheets:**
1. **Project Requirements** — BOQ line scanning needs (G5/G9/G12), technical constraints
2. **Scanner Selection** — 8 scanners ranked (Artec Spider II, Creaform HandySCAN 307, EinScan HX2, SIMSCAN, MetroX, ATOS Q, GOM Scan 1, Artec Eva)
3. **Cost Breakdown** — Option A (full pro, SAR 147k–221k) vs Option B (budget, SAR 108k–165k) incl. 15% VAT
4. **Distributors** — 16 contacts across KSA → Gulf → China → Europe priority tiers
5. **Action Plan** — 9 steps rebased to May 29, 2026

## Cost Summary (Final — May 29, 2026)

| Option | Description | USD | SAR (incl. 15% VAT) |
|--------|-------------|-----|---------------------|
| **A** | Artec Spider II + EinScan HX2 + full workstation + training | $39,215–$58,880 | SAR 147,056–220,800 |
| **B** | Artec Spider II only + budget PC | $28,865–$43,930 | SAR 108,244–164,738 |

## Recommended Strategy

| Priority | Galleries | Recommended Scanner | Distributor |
|----------|-----------|-------------------|-------------|
| PRIMARY | G12 Touch (Lines 4–5) | Artec Space Spider II or Creaform HandySCAN 307 | 3D Middle East / GDS Middle East |
| SECONDARY | G5 + G9 Visual (Lines 1–3) | Shining3D EinScan HX2 | MAPTEC (Riyadh/Dubai) |
| BUDGET PILOT | Internal workflow validation | Revopoint MetroX (~$999) | revopoint3d.com |

## Common Audit Issues (Cost Comparison Workbooks)

When auditing cost comparison xlsx files, check for these patterns:

1. **SAR columns zero** — USD figures present but SAR columns blank (rate not applied). Fix: multiply USD by 3.75.
2. **Totals blank** — No sum formula applied to Option A/B rows. Fix: sum line items, apply 15% VAT, compute grand total.
3. **Stale action plan dates** — Timelines anchored to past LOA dates without rebasing. Fix: determine current date, rewrite action plan with Week 1–8 windows.
4. **Missing specs in scanner table** — Resolution/accuracy columns blank for some models. Check manufacturer specs.
5. **Missing distributor contact details** — Some entries have company name only. Add email/phone.
6. **Duplicate vendor entries** — Same distributor appearing in multiple priority tiers. Clarify primary location.
7. **VAT not applied** — Warning note present but totals exclude 15% Saudi VAT.
8. **Revopoint MetroX resolution blank** — Known gap: should be 0.03mm accuracy, 0.02mm resolution.
