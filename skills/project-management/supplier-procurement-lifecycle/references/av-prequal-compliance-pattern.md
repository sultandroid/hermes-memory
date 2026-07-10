# AV Prequalification Compliance Check & Submittal Statement Pattern

Used when processing AV equipment prequalification packages (supplier to Rawasin or other AV contractor).

## Workflow

### 1. Identify the Equipment

From the supplier's scope of work / BOQ, extract:
- Equipment models and quantities
- Locations/zones
- Supplier name and relationship (distributor, manufacturer, sub-supplier)

### 2. Check Against Approved Design

Compare against the project's approved AV design (typically DHD Services Ltd design concept for Aseer Museum):

| Check | What to verify |
|-------|---------------|
| **Equipment type** | Does the model number match the design spec? |
| **Technical specs** | Power, connectivity, form factor, environmental rating |
| **Compliance verdict** | ✅ Match / ⚠️ Minor variance / ❌ Mismatch |

### 3. Note Quantity Variances

If the supplier's BOQ qty differs from the design BoQ, flag it but do NOT block on it — quantities are often revised between concept and IFC. State: "X quoted vs Y per design — to be reconciled with contractor."

### 4. Draft Submittal Statement

Keep it short. Pattern:

> **Submittal Statement — [Supplier] [Equipment] Prequalification Package**
>
> This prequalification is for the **[equipment purpose — e.g., Yamaha audio equipment supply]** to the Aseer Museum AV system, in compliance with the approved project specifications. Equipment types and technical specs ([list key models]) match the approved DHD AV design.
>
> **Details:**
> - Supplier: [Name] ([role — e.g., Yamaha authorized distributor — KSA])
> - Contractor: Rawasin Media Production (AV contractor)
> - Proposed Ref: MOC-MUS-ASE-1K0-PQ-NNNN
>
> **Provided files:**
> [numbered list of documents]

### 5. File Under AV Submittals

```
04_Submittals/AV/
├── Prequalifications/     — company profiles, certs, COO, warranty
├── Product_Datasheets/    — equipment spec sheets
├── Scope_of_Work/         — BOQ / SOW Excel
├── submittal_statement_[Supplier]_PQ.md
└── email_draft_[Supplier]_PQ.md
```

### 6. Update Submittal Register

Add to the "In Preparation" section:

```
| MOC-MUS-ASE-1K0-PQ-NNNN | [Supplier] [Equipment] Prequalification — [Category] | AV | **In Preparation** | Supplier to Rawasin. Equipment: [models]. Complies with DHD AV design. |
```

## Examples

| Supplier | Equipment | Design Match | Qty Variance |
|----------|-----------|-------------|-------------|
| NMK (Q-Sys) | Core 510i, TSC-50-G3, TSC-70-G3 | ✅ | 5 vs 8 TSC-50-G3 |
| Adawliah (Yamaha) | VXC6, VXS8, XMV8140-D | ✅ | 43 vs 51 VXC6, 5 vs 6 amps |
