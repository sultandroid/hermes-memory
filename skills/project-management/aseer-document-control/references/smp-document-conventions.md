# SMP Document Conventions — CG-Facing Plan Structure

Document governance rules learned from Stakeholder Management Plan Rev 04 updates.

## 1. Revision History — Only Formal Submissions

The revision history table must contain **only versions formally submitted to CG**. Internal iterative drafts (QC blocks, intermediate formatting passes) do NOT belong. Rule: if there's no submission email, transmittal document, or CG response for a revision, it was internal.

| Element | Rule |
|---------|------|
| Rev 00 | Initial submission to CG |
| Rev 01+ | Every resubmission with a transmittal |
| Internal versions | Never listed — irrelevant to CG audit trail |
| Rev number | Sequential integers, renumber if internal revs are removed |

## 2. QC Sign-Off — Real Names Always

The QC Sign-Off table (typically §1.3) must have **actual names**, not "Per live KPR". This table records who prepared, reviewed, and approved the document — it is an audit record, not a role register.

| QC Row | Field Pattern |
|--------|---------------|
| QC-01 (Prepare) | Department or role that prepared (e.g. "Technical Office") |
| QC-02 (Register) | Document Controller name |
| QC-03 (Review) | QA/QC reviewer name (use "on behalf" if signing for absent manager) |
| QC-04 (Approve) | Signing authority name |

## 3. CG Comments Are Sacred

In disposition matrices, the **CG Comment column must contain the EXACT text from the CG response PDF**. Every typo, grammar error, and awkward phrasing is preserved exactly as written by CG.

- Never summarize, rewrite, paraphrase, or "clean up" CG text
- Never rephrase "Structrual" → even if clearly a typo, it stays
- Our response goes in the **Disposition / Action column** — that's where we write
- If a CG comment references another document by name, keep that reference verbatim

## 4. Disposition Statuses — Covered vs Closed

| Status | Badge | When to Use |
|--------|-------|-------------|
| **COVERED** | `badge badge-low` | SMP-scope item we addressed in this revision, but CG hasn't reviewed/confirmed yet |
| **CLOSED** | `badge badge-pass` | CG explicitly confirmed resolution in a prior review round |
| **SUBMITTAL-PENDING** | `badge badge-high` | Resolution depends on external submittal (CV, PQD, prequal) — not resolved by plan content alone |
| **IN-PROGRESS** | `badge badge-low` | Action underway, not yet complete |
| **RE-OPENED** | `badge badge-critical` | CG-03 or similar — closure was withdrawn due to missing supporting submittals |

**Legends and status key blocks** are unnecessary in the disposition section — the badges are self-explanatory. Remove them to save space.

## 5. Table of Contents — Minimal Data

The TOC snapshot chip shows only document-level stats: sections, pages, roles. Do NOT include CG comment counts, approval statuses, or other operational indicators — those belong in the disposition matrix.

**Correct:** `15 SECTIONS · 24 PAGES · 56 ROLES`
**Wrong:** `15 SECTIONS · 24 PAGES · 25 CG COMMENTS (R1+R2) · 56 ROLES`

## 6. Document Number — From CG Response Folder

The formal document number comes from the **CG response PDF filename**, not internally generated. Compare:

| Internal (wrong) | Formal CG (correct) |
|------------------|---------------------|
| MOC-ASEER-SIC-1K0-PL-0020 | MOC-MUS-ASE-1K0-PL-0020 |

The CG-facing number uses the MoC project code (`MUS` = Museum, `ASE` = Aseer), not Samaya's internal project code (`SIC` = Samaya Investment Company). Always check `02_CG_Responses/` for the actual CG filename.

## 7. Table Column Widths — Standardise Across All Tables

All tables in an SMP must use consistent column widths for the same column types:

| Column Type | Standard Width |
|-------------|---------------|
| # (ID/Ref) | 40px |
| Date | 80px |
| Status | 90px |
| Prepared/Approved | 90px |
| Round | 65px |
| CG Comment | 250px |
| Disposition | 120px |
| Ref | 50px |
| Route / Scope | 90px |

Total per row: ~684px (fits A4 content area). Adjust as needed but keep consistent across tables of the same type.

## 8. Plan Names → Role-Based, Register Names → Individuals

| Document | Names Policy | Exception |
|----------|-------------|-----------|
| Plan body (SMP, PEP, DMP) | Role titles only | None — reference "Per live KPR" |
| Register (KPR, Stakeholder Register) | Individual names + approval dates | None |
| Revision History (§1.1) | Real names | Who prepared, who approved each revision |
| QC Sign-Off (§1.3) | Real names | Who prepared, reviewed, approved this document |
| CG Disposition (§1.4) | CG comment text preserved as-is | Never write our names into CG's comments |

## 9. Only Contractual Roles — No Non-Contractual Tiers

Every role in the plan and register must trace to a **contractual source**: ER, SOW, Appendix B, or a CG directive. Before adding any role, verify it exists in at least one of these. If not found, remove it.

**Examples from this project:**
| Role | Source | Verdict |
|------|--------|---------|
| Conservation Consultancy (T2-20) | Not in ER, SOW, or Appendix B | ❌ Removed |
| Café Sunshade (T2-12) | CG CRS-13 directive | ✅ Kept (CG-mandated) |
| MEP Coordinator | Internal Samaya role, not contractual | ✅ Keep but NOT in KPR |

**Checklist before adding any new role to a plan or register:**
- Is it in Appendix B (either column)?
- Is it in the ER or SOW?
- Is it a CG directive?
- If none of the above → it's non-contractual. Remove it.

## 10. In-Plan Name Reference Pattern

When a role has an approved name in the live register, reference it in the plan as:

```
{Name} · Per live KPR
```

**Examples:**
- `Eng. Mohamed Ahmed · Per live KPR` (HSSE Manager)
- `Dr. Waleed · Per live KPR` (BIM Manager)
- `Hani Alghamdi · Per live KPR` (Procurement Manager)

**Rules:**
- Known/approved → Name + "· Per live KPR"
- Vacant/TBC → status description only (no register reference)
- Pending → "TBC — hiring in progress" or similar (no name, just status)
- Never embed names in plan role descriptions — reference the live KPR
