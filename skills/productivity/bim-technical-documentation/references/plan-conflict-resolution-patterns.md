# Plan Conflict Resolution Patterns — Aseer Museum

> Captured from the 2026-07-11 plan conversion session. These are the specific conflicts found and how they were resolved.

## Conflicts Found

### 1. Handover Date: 5-Month Gap
| Plan | Before | After | Source of Truth |
|------|--------|-------|-----------------|
| PEP | 01 Mar 2027 (TBC) | 30 Sep 2026 | Contract 0010003521 — 10 months from NTP (01 Dec 2025) |
| All other plans | 30 Sep 2026 | 30 Sep 2026 | — |

**Root cause:** PEP was drafted from a legacy document that used a different NTP assumption (01 May 2026 → 01 Mar 2027). The actual NTP is 01 Dec 2025 per the signed contract.

### 2. NTP Date: Ambiguous
| Plan | Before | After |
|------|--------|-------|
| PEP | 01 May 2026 (TBC) | 01 Dec 2025 |
| PEP (2nd table) | 01 May 2026 (TBC) | 01 Dec 2025 |

**Root cause:** The legacy PEP draft used a placeholder NTP. The signed contract date is 01 Dec 2025.

### 3. LOD Requirement: DMP vs BEP
| Plan | States | Resolution |
|------|--------|------------|
| DMP | LOD 300 (ER §2.3.D) | Contractual minimum for design stage |
| BEP | LOD 350/400 for RIBA 4 | Progression beyond contractual minimum is valid |

**Resolution:** BEP now has a header note: "Contractual LOD Requirement: LOD 300 per ER §2.3.D (design stage); progressed to LOD 350/400 for RIBA 4 Technical Design per BEP LOD matrix below."

### 4. Review Period: Calendar vs Working Days
| Plan | States | Source of Truth |
|------|--------|-----------------|
| DMP | 14 **calendar** days (ER §2.4) | ER §2.4 — contractual |
| Communication Plan | 14 **working** days | Approved Code B — NOT changed |

**Resolution:** DMP is the contractual source. Communication Plan is approved Code B and cannot be changed. All unapproved plans now reference 14 calendar days per ER §2.4.

### 5. Subcontractor Approval Authority
| Plan | States | Resolution |
|------|--------|------------|
| DMP | "All sub-consultant appointments subject to MoC approval" (Contract §4 Art. 13) | Source of truth |
| Procurement Plan | "MoC approval required" | Already aligned |
| PEP | "MoC final approver" | Already aligned |

## Resolution Process

1. **Identify all conflicts** from the consolidated analysis
2. **Check approval status** of each plan (approved_plans.md)
3. **Code B plans** — do NOT touch. They are the contractual baseline.
4. **Code C/D or draft plans** — fix conflicts, bump revision, add `conflict_resolution` to YAML frontmatter
5. **Update approved_plans.md** — add a "Plans — New Drafts" section listing the new revisions

## YAML Frontmatter Pattern for Resolved Plans

```yaml
---
revision: C01
conflict_resolution: |
  Conflicts identified in consolidated analysis (2026-07-11) resolved:
  - Handover date aligned to 30 Sep 2026 (was 01 Mar 2027)
  - NTP aligned to 01 Dec 2025 (was 01 May 2026 TBC)
  - Review period: 14 calendar days per ER §2.4 (was ambiguous)
  - LOD: Contractual LOD 300 per ER, progressed to LOD 350/400 per BEP
  - Subcontractor approval: MoC approval required per Contract §4 Art. 13
---
```

## Plans Updated (2026-07-11)

| Plan | Old Rev | New Rev | Status |
|------|---------|---------|--------|
| PEP | P01 | P01 | Draft — Conflicts Resolved |
| BEP | 1.0 | 1.1 | Draft — Conflicts Resolved |
| Procurement | — | C01 | Draft — Conflicts Resolved |
| Risk | — | C01 | Draft — Conflicts Resolved |
| Mobilization | — | C01 | Draft — Conflicts Resolved |
| Quality (PQP) | — | C01 | Draft — Conflicts Resolved |
| Resource | C00 | C01 | Draft — Conflicts Resolved |
| SMP | 01 | 02 | Draft — Conflicts Resolved |

## Plans NOT Changed (Code B — Approved)

DMP, Stakeholder, Communication, HSE (PL-0010/41/43/45/46/47/48/49/54)
