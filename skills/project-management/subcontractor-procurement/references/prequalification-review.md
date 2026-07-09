# Prequalification Document Review Workflow

## When to Use
- User provides supplier/subcontractor prequalification documents (company profile, COO, product datasheets, scope of work)
- Need to check compliance against project design specs
- Need to prepare email to Document Controller + submittal statement

## Workflow

### Step 1: Inventory the Documents
List all files from the supplier package. Categorize into:
- **Company profile** — proves company exists, relevant experience
- **COO & Warranty** — Certificate of Origin, product warranty
- **Product datasheets** — technical specs of proposed equipment
- **Scope of Work / BOQ** — what they're quoting, quantities, locations

### Step 2: Check Against Project Design Specs
1. **Search project files** for the governing design document (e.g. AV_Deep_Research.md, DHD BoQ, NRS specs)
2. **Extract the specified equipment** — model numbers, quantities, locations
3. **Compare supplier's proposed equipment** against spec:
   - **Equipment type match** — same model number? (e.g. Q-Sys Core 510i ✓)
   - **Quantity match** — same count? Flag gaps (e.g. 5 quoted vs 8 specified)
   - **Location match** — same zones/galleries?
4. **Note the supplier relationship** — are they a direct sub to Samaya, or a sub-supplier to a main contractor (e.g. NMK → Rawasin)?

### Step 3: Document the Compliance Assessment
Create a compliance table:

| Spec Item | Specified Model | Proposed Model | Qty Spec | Qty Proposed | Status |
|-----------|----------------|----------------|:--------:|:------------:|--------|
| Master DSP | Q-Sys Core 510i | Core 510i | 1 | 1 | ✅ Match |
| Rack Touch | TSC-70-G3 | TSC-70-G3 | 1 | 1 | ✅ Match |
| Gallery Touch | TSC-50-G3 | TSC-50-G3 | 8 | 5 | ⚠️ Qty gap |

### Step 4: Draft Email to Document Controller
Subject: `{Supplier} {Product} Prequalification Documents — {Discipline}`

Structure:
1. **What's attached** — list of documents
2. **Compliance statement** — "Equipment type is correct per the approved {design ref}"
3. **Relationship note** — who the supplier is supplying to
4. **Gaps/notes** — any quantity or scope variances that need clarification
5. **Action requested** — PQ number assignment, formal submission to CG

### Step 5: Prepare Submittal Statement
Create a markdown file with YAML frontmatter:

```yaml
---
last_updated: YYYY-MM-DD
owner_agent: Hermes
status: active
source: {supplier} prequalification documents
---
```

Include:
- **Proposed Ref:** `MOC-MUS-ASE-1K0-PQ-XXXX` (next sequential number)
- **Discipline:** 1K0 (General) / {specific discipline}
- **Submitted by:** Samaya Technical Office
- **Date:** YYYY-MM-DD
- **Submittal Statement:** 2-3 sentence compliance summary
- **Documents Enclosed:** numbered table
- **Status table:** Prepared by | Reviewed by (NRS) | Approved by (CG)

### Step 6: File the Documents
Organize under `04_Submittals/{Discipline}/`:
```
04_Submittals/{Discipline}/
├── Prequalifications/          ← company profiles, COO, warranty
├── Product_Datasheets/         ← equipment spec sheets
├── Scope_of_Work/              ← BOQ, SOW Excel
├── email_draft_{supplier}_PQ.md
└── submittal_statement_{supplier}_PQ.md
```

## Pitfalls
- **Supplier relationship matters** — If the supplier is a sub-supplier to an already-contracted main contractor (e.g. NMK → Rawasin), the PQ may be handled internally by that contractor, not submitted directly to CG. Clarify before assigning a PQ number.
- **Quantity gaps are common** — Supplier BOQs often quote partial quantities. Flag them but don't reject the PQ for it. The gap may be covered by another supplier or a later phase.
- **Design docs may be concept-stage** — The governing design document (e.g. DHD BoQ v1.11) may be "CONCEPT" not "IFC". Note this in the compliance statement — the spec may change at IFC.
- **Check existing PQ numbers** — Look at existing files in `04_Submittals/{Discipline}/Prequalifications/` to find the next sequential number. Pattern: `MOC-MUS-ASE-1K0-PQ-XXXX`.
- **Email + submittal statement are separate files** — The email is for the DC's inbox. The submittal statement is the formal record. Both go in the same discipline folder.
