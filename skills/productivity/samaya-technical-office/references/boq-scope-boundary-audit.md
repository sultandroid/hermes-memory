# BOQ Scope Boundary Audit — Cross-Referencing ER + SOW + BOQ

## When to Use This Workflow

When you need to determine the **actual contractual scope** of a Design & Build project. The ER (Employer's Requirements) and SOW (Scope of Work) define what should be delivered. The BOQ/Pricing Schedule confirms what was **priced** — and therefore what is contractually committed.

## Workflow

### Step 1: Gather the Three Documents
1. **ER** — Search for `ER*`, `Employer*Requirement*`, usually a PDF in the tender pack
2. **SOW** — Search for `*Scope of Work*`, `*SOW*`, `*Contractors Scope*` in the tender pack
3. **BOQ/Pricing Schedule** — Search for `Pricing Schedule`, `BOQ`, `*Pricing*` in the commercial docs folder

### Step 2: Extract BOQ Structure
Read the BOQ Excel file to understand its pricing sections:

```python
import openpyxl
wb = openpyxl.load_workbook("Pricing_Schedule.xlsx", data_only=True, read_only=True)
for sname in wb.sheetnames:
    ws = wb[sname]
    print(f"Sheet: {sname} (rows: {ws.max_row}, cols: {ws.max_column})")
    # Read first 10 rows for headers
    for i, row in enumerate(ws.iter_rows(max_row=10, values_only=True)):
        vals = [str(v)[:60] if v else "" for v in row[:6]]
        print(f"  Row {i+1}: {' | '.join(vals)}")
```

### Step 3: Identify Scope Boundaries
For each BOQ section, determine:

| BOQ Ref | Section Name | In Scope? | Evidence |
|---------|-------------|-----------|----------|
| §001 | Design Development | Yes — lump sum | Priced line items |
| §012 | AV Software/Content | **By MoC — excluded** | All lines marked "By MoC" |
| §011 | AV Hardware | Yes — in scope | Priced line items |
| §014 | Mock-ups/Samples | Yes — SAR 120K + 250K | Explicit allowance amounts |
| §009 | Graphics production | Yes (production) | Priced; content/text = MoC |

### Step 4: Mark Exclusions Clearly
Every BOQ section with lines marked "By MoC" means the Contractor is **not** responsible for those items. Flag them:
- `[MoC]` — Employer supplies
- `[EXCLUDED]` — Explicitly excluded per SOW
- `[DEFERRED]` — Deferred to later stage

### Step 5: Cross-Check Against ER Handover Requirements
The ER often lists specific handover items (e.g., ER §2.7 has 17 items). Verify the BOQ has allowances for:
- O&M Manuals compilation
- As-Built documentation
- Training
- Spares
- Building Manual
- ITCA/commissioning

If these are **not** in the BOQ as separate items, they may be deemed included in the lump sum design fee. Flag as risk.

### Aseer Museum Example (May 2026)

**Documents:**
- ER: `250313_ER Document - Aseer Museum of Arts_R02.pdf` (170pp, Bluehaus MEP)
- SOW: `6380_KMS_RPT_PM_AS_00006_Aseer_Contractors_Scope of Work.md` (46pp)
- BOQ: `Pricing Schedule for the Aseer Museum for Ministry of C.xlsx` (16 sheets)

**BOQ Sections Found:**
| Sheet | Section | Scope |
|-------|---------|-------|
| 001 | Detail Design | In scope — lump sum |
| 002 | Enabling/Demolition | In scope — per gallery |
| 003 | Internal Partitions & Finishes | In scope — per gallery |
| 004 | Furniture | In scope — per item |
| 005 | Display Cases | In scope — museum grade |
| 006 | Lighting & Power | In scope — per gallery |
| 007 | Security, Data, Life Safety | In scope — per gallery |
| 008 | Plumbing & Mechanical | In scope — per gallery |
| 009 | Graphics Production | In scope — CONTENT excluded |
| 010 | Models & Replicas | In scope — per item |
| 011 | AV Hardware | In scope — priced lines |
| 012 | AV Software/Content | **By MoC — EXCLUDED** |
| 013 | Setworks & Scenography | In scope |
| 014 | Mock-ups, Samples & Prototypes | SAR 120K + SAR 250K allowances |
| 015 | GF Entrance Enhancement | In scope — additional |

**Key finding (all confirmed):**
- AV software (BOQ §012) ALL marked "By MoC" → confirmed exclusion
- Mock-ups (BOQ §014) have explicit allowances → in scope
- Design development (BOQ §001) is lump sum covering ALL compliance/approvals
- Graphics production (BOQ §009) covers physical install; content/labels = MoC
