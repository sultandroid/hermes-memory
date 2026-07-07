# Tender Project Setup — Full Pattern

Based on RCRC Exhibition tender project (Samaya Odoo Project 324).

## Sequence

1. Check portfolio stages → find "Tendering" (ID 12)
2. Discover company_id via `res.company.search_read` → Samaya = ID 1
3. Create `project.project` with stage_id=12, company_id=1, user_id=151
4. Create 18 main tasks across 9 phases in parallel (no parent_id)
5. Set initial dates spread across the tender period
6. When deadline compresses, batch-update all dates + state in one pass

## Task Stage Mapping

| Tender Phase | Odoo Stage | ID |
|-------------|------------|----|
| Mobilisation & Kick-Off | Initiation | 35 |
| Site Visit | Initiation | 35 |
| Scope Review / RFI | Design Development | 36 |
| Pricing & Estimation | Procurement | 39 |
| Technical Proposal | Design Development | 36 |
| Commercial Proposal | Procurement | 39 |
| Programme & Methods | Design Development | 36 |
| Review & Submission | Tender/DD Support | 37 |
| Post-Submission | Tender/DD Support | 37 |

## 18 Tasks for Full Tender Phase

### Phase 1: Tender Mobilisation (Stage 35)
1. Tender Document Inventory & Register
2. Tender Strategy Kick-Off

### Phase 2: Site Visit (Stage 35)
3. Site Visit & Existing Conditions Survey

### Phase 3: Scope & Technical Review (Stage 36)
4. Scope Gap Analysis / RFI Log
5. Method Statement — Preliminary Draft

### Phase 4: Pricing & Estimation (Stage 39)
6. Material Take-Off & Verification
7. Subcontractor & Supplier Enquiries
8. Pricing Model Update & Reconciliation
9. Risk & Contingency Assessment

### Phase 5: Technical Proposal (Stage 36)
10. Technical Proposal Finalisation

### Phase 6: Commercial Proposal (Stage 39)
11. Commercial Proposal Preparation

### Phase 7: Programme & Method Statement (Stage 36)
12. Tender Programme Development
13. Method Statement Compilation

### Phase 8: Review & Submission (Stage 37)
14. Internal Compliance & Quality Check
15. Management Review & Sign-Off
16. Submission & Confirmation

### Phase 9: Post-Submission (Stage 37)
17. Tender Clarifications & Negotiation Prep
18. Lessons Learned & Archive

## Date Allocation Pattern

With a hard deadline (e.g., "all before July 1"), every task starts immediately:

| Phase | Start | Deadline |
|-------|-------|----------|
| Mobilisation | Day 0 | Day 1-2 |
| Site Visit | Day 3 (Sunday) | Day 4 |
| Scope Review | Day 1 | Day 5 |
| Pricing | Day 0 | Day 5-6 |
| Technical Proposal | Day 0 | Day 5-6 |
| Commercial Proposal | Day 3 | Day 5-6 |
| Programme | Day 1 | Day 5-6 |
| Review & Submission | Day 4-5 | Day 6 |
| Post-Submission | Day 7 | Day 7 |

## Progress Pitfall

```python
# FIRST WRITE: state + description + progress (progress may NOT persist)
models.execute_kw(db, uid, pw, "project.task", "write", [[tid], {
    "state": "1_done",
    "progress": 1.0,
    "description": updated_desc,
}])

# SECOND WRITE: progress only (read back to verify)
models.execute_kw(db, uid, pw, "project.task", "write", [[tid], {"progress": 1.0}])
verified = models.execute_kw(db, uid, pw, "project.task", "read", [[tid]],
    {"fields": ["id", "progress"]})
assert verified[0]["progress"] == 1.0, "Progress did not persist after second write"
```
