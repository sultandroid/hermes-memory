# Compliance Sheet Template — Supplier Product vs Project Requirements

When a supplier submits products/documents and you need to assess compliance against the project's contract requirements (spec list, PQ register, design research, scope docs), build a multi-sheet Excel compliance workbook.

## When to Use

- Supplier submits product datasheets, trade licenses, COO, warranty
- User asks for a "compliance sheet" or "complaince sheet" for a company
- Need to cross-reference supplier offering against project spec list, PQ register, AV deep research, scope docs
- Pre-award assessment before recommending approval

## Workflow

### Step 1: Extract Source Data

1. **Read the supplier's XLSX/PDF** — extract product codes, quantities, locations
2. **Unzip any accompanying ZIP** — datasheets, trade licenses, COO, warranty
3. **Read project requirements from the repo** — in this order:
   - `01_Registers/specification_list.md` — spec numbers, compliance types (Mandatory, Statutory, Oddy Test)
   - `Technical_Office/Specialist_Management/specialist_register.md` — specialist status, PQ refs
   - `99_Archive/02_Scope_Management/AV_IT/AV_Deep_Research.md` — AV concept design, quantities per zone
   - `01_Registers/prequalification_register.md` — PQ codes (A/B/C/D) for each vendor/product
   - `03_Scope/scope_summary.md` — project scope overview
   - `Technical_Office/deliverables_register.md` — deliverable status per discipline

### Step 2: Build 6-Sheet Compliance Workbook

Use openpyxl with Samaya standard styling (navy `#1F3864` headers, white text, thin borders, RAG fills).

| Sheet | Content | Columns |
|---|---|---|
| **Cover** | Summary table — 8-10 compliance items with RAG status | Section, Status, Notes |
| **Product Compliance** | Each product line mapped against concept design quantities | #, Product Code, Description, Qty (XLSX), Qty (Concept), Locations, AV Zone Ref, Compliance, Gap/Notes |
| **Project Requirements** | Each project requirement mapped to supplier offering | Ref, Project Requirement, Source, Audinate Offering, Compliance, Action Required |
| **Documentation** | Each document file checked | #, Document, File, Status, Notes |
| **Location Mapping** | Each location/zone with product assignment | Location Code, Location Name, Floor, Product, AV Zone (Concept), Gallery/Area |
| **Gap Analysis** | Identified gaps with mitigation | Gap ID, Description, Severity, Impact, Mitigation, Owner |

### Step 3: RAG Status Convention

- ✅ Green (`C6EFCE`) — compliant, no action needed
- ⚠️ Yellow (`FFEB9C`) — partial compliance, needs verification or minor action
- 🔴 Red (`FFC7CE`) — non-compliant, blocks approval

### Step 4: Key Sources to Cross-Reference

| Source File | What to Extract |
|---|---|
| `specification_list.md` | Spec numbers relevant to the supplier's discipline (e.g. AV-001 to AV-016 for AV equipment) |
| `AV_Deep_Research.md` | Concept design quantities per zone, product models specified |
| `prequalification_register.md` | PQ code status for the supplier's product category |
| `specialist_register.md` | Which specialist is responsible (e.g. Rawasin for AV) |
| `deliverables_register.md` | Current deliverable status for the discipline |
| `scope_summary.md` | In-scope/out-of-scope boundaries |
| ER/SoW extracts | Contractual requirements (Oddy testing, MOI compliance, etc.) |

### Step 5: Common Gap Types to Flag

1. **PQ status gap** — supplier's product category has Code C (Revise & Resubmit) — blocks approval
2. **Quantity discrepancy** — XLSX qty vs concept design qty — verify with specialist
3. **IFC specs not issued** — concept stage only — note as pending final sign-off
4. **Distributor vs manufacturer** — supplier is distributor, may need manufacturer authorization letter
5. **Documentation gaps** — missing datasheets, COO, warranty, trade license renewal

## Example Output

See the worked example at `Technical_Office/Specialist_Management/Audinate_ProLab_Compliance_Sheet.xlsx` for the Aseer Museum Audinate/ProLab assessment.

## Pitfalls

- Always check the PQ register first — a Code C or D blocks the whole assessment
- Quantity gaps in the XLSX vs concept design are the most common finding — flag but don't block on them (the specialist may have a separate PO)
- IFC specs may not be issued yet — note this as a limitation on final compliance sign-off
- Trade license renewal year matters — 2025 license alone is stale if the current year is 2026
- COO + Warranty are separate documents — check both exist
- The supplier's XLSX may have typos in location codes — cross-reference against the AV zone naming convention
