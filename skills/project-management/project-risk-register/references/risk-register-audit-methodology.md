# Risk Register Audit Methodology

Audit an existing Excel risk register for completeness, consistency, scoring integrity, structural issues, and governance gaps. This is NOT about building a new register — it's about QA-checking one that already exists.

## When to Use

- User sends you a risk register XLSX and says "check this", "audit this", "review this", "validate this"
- You need to assess the quality of a received risk register before accepting it into governance
- Preparing a review comment for a subcontractor's or consultant's submitted risk register

## Audit Scope

| Dimension | What to Check |
|-----------|---------------|
| **Structure** | Sheet count, naming, navigation (Dashboard → Detail → Methodology) |
| **Completeness** | Every risk has: ID, category, description, P×S score, rating, owner, status, mitigation |
| **Scoring Integrity** | P×S calculation matches the stated scale, ratings are correctly applied |
| **Cross-Referencing** | DRR → Master links, discipline-specific sheets → dashboard summary |
| **Lifecycle** | Date raised, last review, target close date, trigger/early warning indicators |
| **Residual Risk** | Whether post-mitigation scores exist (or only inherent) |
| **Dashboard Accuracy** | Counts match underlying data, live status reflects actual project state |
| **Methodology** | Scales defined, gaps documented, assumptions stated |
| **RMP Alignment** | Companion Risk Management Plan matches the register's methodology |

## Structured Audit Checklist

### Step 1 — Sheet Inventory

```
Load workbook → enumerate sheet names, row counts, column counts.
```

**Check:** All expected sheets present? Any duplicate headers? Any sheet that's clearly a copy/paste error (e.g. AV sheet with HSE header)?

### Step 2 — Dashboard Accuracy

For each dashboard metric, verify against the raw data:

| Dashboard Metric | Verification |
|------------------|-------------|
| Total risk count | Count rows in each detail sheet (exclude headers) |
| Critical / High / Medium / Low counts | Aggregate by rating column |
| By-category counts | Aggregate by category column |
| Live status claims | Check if the referenced risk IDs exist and are marked OPEN |

**Common issues:**
- Dashboard counts stored as floats (`41.0`, `18.0`) instead of integers — suggests broken formulas or empty source cells
- Dashboard omits entire sheets (e.g. AV risks not counted)
- "Critical" count in dashboard doesn't match actual critical-rated entries in the detail sheet

### Step 3 — Per-Sheet Completeness

For each risk entry, check these fields:

| Field | Must-Have | Common Failure |
|-------|-----------|----------------|
| Risk ID | Present, unique, follows a consistent prefix scheme | Missing IDs, duplicate IDs, inconsistent prefix (PRR- vs DRR- vs no prefix) |
| Risk Category | From a defined taxonomy/RBS | Free-text categories that don't map to any standard |
| Probability | Numeric, within scale (1-4 or 1-5) | Blank, text, out-of-range |
| Severity | Numeric, within scale | Blank, text, out-of-range |
| Risk Score | P × S = correct value | Mismatch between stated P×S and actual score, or score present but P/S blank |
| Risk Rating | Maps to the register's own rating thresholds | Rating doesn't match score (e.g. score=12 but rated Medium) |
| Risk Owner | Named person or role | Blank, ambiguous ("TBD", "Team"), or joint without lead |
| Status | OPEN / CLOSED / MITIGATED / WATCH | Blank, inconsistent values |
| Mitigation | Actionable, not just "monitor" | Vague, aspirational, or missing |

### Step 4 — Scoring Scale Audit

```
Verify the stated scale. Extract all P×S pairs. 
Recalculate. Flag any discrepancies.
```

**Master/DRR (1-4 scale):**
| Rating | Score Range | Verify |
|--------|-------------|--------|
| Critical | ≥12 | Check: score ≥ 12 that should be Critical |
| High | 8-11 | Check: medium-risk scores (4-7) not labelled High |
| Medium | 4-7 | Check: correctly bounded |
| Low | ≤3 | Check: ≤3 only |

**HSE (1-5 scale):**
| Rating | Score Range | Verify |
|--------|-------------|--------|
| Critical | ≥16 | |
| High | 10-15 | |
| Medium | 5-9 | |
| Low | ≤4 | |

**Common issues:**
- Mixing scales within the same workbook (e.g. AV sheet using HSE 1-5 scale but Master uses 1-4)
- Score thresholds applied inconsistently (e.g. score=12 labelled "High" instead of "Critical")
- Score stored as text, not number

### Step 5 — Cross-Reference & Traceability

| Check | Method |
|-------|--------|
| DRR → Master links | Every DRR "Escalated To" should point to a valid Master Risk ID |
| Dashboard → Detail | Every risk listed in the dashboard watchlist should exist in the detail sheet |
| Risk ID uniqueness | `len(set(all_ids)) == len(all_ids)` |
| Column count consistency | Every data row has the same number of columns as the header |

### Step 6 — Risk Lifecycle Assessment

| Field | Why It Matters |
|-------|----------------|
| Date Raised | When was this risk first identified? Shows risk maturity |
| Last Review Date | Is the register being maintained or is it stale? |
| Target Close Date | When will the mitigation be complete? Without this, mitigations are open-ended |
| Trigger / Early Warning | How will the owner know the risk is materialising? Without this, it's reactive |

**Common gaps:** No lifecycle columns at all → register is a snapshot, not a management tool.

### Step 7 — Residual Risk Analysis

| Pattern | Issue |
|---------|-------|
| No residual score column | Can't tell if mitigations are effective |
| Residual = Inherent | Mitigations aren't working (or weren't honestly assessed) |
| Residual > Inherent | Mathematical error — or mitigations made it worse |
| Only HSE has residual | Inconsistent treatment across sheets |

### Step 8 — Mitigation Quality

Rate each mitigation as one of:

| Grade | Criteria |
|-------|----------|
| ✅ **Specific** | Named owner, target date, verifiable action (e.g. "Commission 3D coordination study by 15-Jun") |
| ⚠️ **Vague** | Generic action, no deadline (e.g. "Coordinate with consultant") |
| ❌ **Defensive** | Contractual caveat only, no technical fix (e.g. "SOW-PROTECT: notify employer") — note: defensive is valid AS PART of a mitigation, but not valid as the ONLY mitigation |

**For SOW-PROTECT risks:** flag that a parallel technical mitigation is needed. The contractual protection is necessary but doesn't move the work forward.

### Step 9 — Methodology & Governance

| Check | Why |
|-------|-----|
| Scale definitions documented | Without these, the register is subjective |
| Open data gaps listed | Honesty about unknowns is a governance strength |
| Versioning / revision history | Is this Rev 0 or Rev 3? |
| Source data cited | Which status report, which contract clause, which survey? |

### Step 10 — RMP Alignment Check (if an RMP exists)

When the risk register has a companion Risk Management Plan (RMP), check alignment between the two. An RMP that contradicts the register is worse than having no RMP.

| Check | What to Compare | Failure Mode |
|-------|----------------|--------------|
| **Scoring scale** | RMP's stated P×I scale vs register's actual P×S scale | RMP says 1-5, register uses 1-4 (or vice versa) — fundamental methodology conflict |
| **Risk ID format** | RMP's ID convention vs register's actual IDs | RMP references PRR-001 but register uses PRR-COM-01 — cross-referencing broken |
| **Risk count** | RMP's stated count vs actual register row count | RMP says "29 risks" but register has 33 — RMP is stale |
| **Severity bands** | RMP's band definitions vs register's actual bands | RMP has 5 bands (incl. Very Low), register has 4 (no Very Low) |
| **Register architecture** | RMP's described sheets vs actual workbook sheets | RMP only mentions Master but workbook has DRR, HSE, AV, Out-of-Scope Log |
| **Response strategies** | RMP's listed strategies vs register's actual mitigations | RMP doesn't list SOW-Protect but register uses it extensively |
| **Template fields** | RMP's required fields vs register's actual columns | RMP requires 20 fields (target close date, residual score, urgency, etc.) but register has only 14 |
| **Risk format** | RMP's required risk statement format vs register's actual format | RMP requires "Condition → Consequence" but register uses "Risk Event + Project Impact" as two columns |
| **Roles & ownership** | RMP's RACI vs register's actual owners | RMP says PM is accountable, register assigns joint owners |
| **Review cadence** | RMP's stated review frequency vs actual update frequency | RMP says weekly, register has no "Last Review Date" column |

**Resolution rule:** The register is the working tool; the RMP should define and endorse the register's methodology, not contradict it. Update the RMP to match the register — not the other way around — unless the RMP was contractually approved first.

**When to flag as CRITICAL:** If the scoring scale differs (1-4 vs 1-5), the two documents cannot be consolidated without a full rescoring exercise. This is a governance blocker.

## Output Format

Deliver the audit as a structured report with these sections:

1. **Sheet Inventory** — names, sizes, purpose
2. **Critical Issues** — must fix (blocking governance acceptance)
3. **High Issues** — should fix (affecting usability)
4. **Medium Issues** — good practice (quality improvements)
5. **Positives** — what's done well (reinforce good practice)
6. **Summary Table** — quick overview of pass/fail per dimension

### Summary Table Template

| Dimension | Status | Details |
|-----------|--------|---------|
| All risks scored | ✅/❌ | Count of unscored entries |
| Dashboard accurate | ✅/❌ | Mismatches found |
| Scoring consistent | ✅/❌ | Scale violations |
| Lifecycle tracked | ✅/❌ | Missing date columns |
| Residual risks tracked | ✅/❌ | Which sheets lack |
| Mitigations actionable | ✅/⚠️/❌ | Vague or defensive mitigations |
| DRR→Master traceable | ✅/❌ | Broken links |
| Methodology documented | ✅/❌ | Gaps transparently listed |
| Cross-sheet consistency | ✅/❌ | Duplicate headers, wrong scales |
| RMP alignment | ✅/❌ | Methodology conflicts between RMP and register |

## Common Findings (from real audits)

### AV Risk Register Dead
- **Pattern:** AV sheet has HSE header (copy/paste error), no scoring data, no owners, no status
- **Root cause:** Template was duplicated from HSE but never populated
- **Fix:** The AV register needs to be rebuilt from scratch with proper scoring, owners, and status
- **Dashboard impact:** AV risks invisible to executive management — portfolio summary must include them

### Float Counts in Dashboard
- **Pattern:** `41.0`, `18.0` instead of `41`, `18`
- **Root cause:** Formulas referencing empty or linked cells that return floats
- **Fix:** Use `=ROUND(formula,0)` or source from static values

### No Residual Risk in Design-Stage Registers
- **Pattern:** Master and DRR sheets show only inherent P×S, no residual column
- **Root cause:** The register was built as a "risk inventory" not a "risk management tool"
- **Fix:** Add residual/current risk columns after mitigations are applied

### No Trigger/Early Warning Indicators
- **Pattern:** Risk has mitigation but no trigger condition
- **Root cause:** Risk owners haven't defined what "active" looks like
- **Fix:** Add a "Trigger" column. For each risk, define the observable event that means "this risk is materialising now"

### Risk Owner Joint Without Lead
- **Pattern:** "Project Director / Commercial Manager" as single owner
- **Root cause:** Avoiding single-point accountability
- **Fix:** Designate one lead owner per risk; the other is a stakeholder

### SOW-PROTECT as Only Mitigation
- **Pattern:** Risk's only mitigation is "notify employer and seek variation"
- **Root cause:** The register is being used as a contractual positioning tool, not a risk management tool
- **Fix:** Add a parallel technical mitigation that actually resolves the risk. The contractual protection stays, but a technical action must also exist.

### RMP-Register Methodology Mismatch
- **Pattern:** RMP says 1-5 P×I scale, register uses 1-4 P×S. RMP references PRR-001, register uses PRR-COM-01. RMP says 29 risks, register has 33.
- **Root cause:** RMP and register were created independently without cross-referencing
- **Fix:** Update the RMP to define and endorse the register's methodology. The register is the working tool; the RMP should document it, not contradict it.
