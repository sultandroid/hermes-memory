# CG Submission Schedule Methodology

When CG requests a design phase schedule (e.g., Mohammad Elbaz 20-Jun-2026 email), they specify exactly **4 categories** that must all be submitted AND approved within the deadline:

1. **Design Development Drawings (DD)**
2. **Material Submittals & Finishing Samples**
3. **Issued for Construction Drawings (IFC)**
4. **Coordination Drawings**

## CG's Explicit Rules (from Elbaz email)

- **Basement first** — Basement floor drawings are the priority milestone
- **Staggered submissions** — No clustering; minimum 5 WD gap between same-discipline submissions
- **Review period buffer** — Include adequate time for CG to review, comment, and approve
- **Fixed deadline** — 3 months from DMP approval date (e.g., 21 May → 21 Aug 2026)
- **Scope** = "all design drawing works" — all 4 categories must be fully delivered AND approved

## Buffer Rules by Complexity

### Samaya Internal Review
| Complexity | Duration | Example |
|-----------|----------|---------|
| Simple | 2 WD | Single drawing/spec, GH submittal |
| Medium | 3 WD | Multi-sheet package, BOD report |
| Complex | 5 WD | Full discipline package (NRS 246 dwgs) |

### CG Review
| Complexity | Duration | Example |
|-----------|----------|---------|
| Simple | 7 WD | Stair IFC, Terrace Shade IFC |
| Medium | 14 WD | AV/FLS/Structural packages |
| Complex | 14-21 WD | Full DD package, MEP Design |

### Resubmission Cycle (Code B/C)
| Phase | Duration |
|-------|----------|
| Consultant revision | 3-10 WD (depends on complexity) |
| Samaya re-review | 2-5 WD |
| CG re-review | 7-10 WD |

## Dependency Chain

```
DD Approval → Consultant IFC Prep → Samaya IFC Review → CG IFC Review → IFC Approval
```

**⛔ Critical:** IFC depends on DD **approval**, not just submission. This means the timeline for IFC must start counting from when DD is approved, which for complex packages can be 4-18 Aug, leaving insufficient time for IFC before a 21 Aug deadline.

## Scheduling Algorithm (Working Days, Sun-Thu)

For each submission item:
1. Start = today or predecessor approval date
2. Consultant prep = complexity-based working days
3. Samaya review = complexity-based working days
4. CG submit date = start + prep + Samaya
5. CG review = complexity-based working days
6. Expected response = submit + CG review
7. If Code B/C: add revision + Samaya + CG re-review
8. If same discipline as previous item: enforce 5 WD stagger gap

## Practical Application — Aseer Museum Example

### Phase 1 (DD Drawings — 10 items) — ALL ✅ by 18 Aug
- MEP Mechanical (Basement priority): Prep 8 WD, Samaya 5 WD, CG 14 WD → submit 8 Jul, approve 4 Aug
- Exhibition Fit-Out (NRS): Prep 12 WD, Samaya 5 WD, CG 14 WD → submit 14 Jul, approve 10 Aug
- Structural: Simple/Medium items interleaved with 5 WD stagger gaps

### Phase 2 (Material Submittals — 8 items) — ALL ✅ by 22 Jul
- Runs fully parallel with DD
- All materials submitted by 5 Jul, approved by 22 Jul

### Phase 3 (IFC — 10 items) — Only 2/10 ✅
- Simple IFC (Stair, Terrace Shade) → approved by 13 Aug ✅
- Complex IFC (MEP, NRS Exhibition) → need until 10-24 Sep ❌
- Root cause: IFC depends on DD approval, which for complex items arrives 4-18 Aug

### Phase 4 (Coordination Drawings) — 0/1 ❌
- Depends on all DD approvals (last at 18 Aug) → needs until 1 Oct

## Verification Checklist

- [ ] All 4 categories included? (DD, Materials, IFC, Coordination)
- [ ] Staggered — no two same-discipline items on same date?
- [ ] Basement priority honored? (MEP Mechanical first)
- [ ] Review buffers realistic? (not optimistic)
- [ ] IFC start date based on DD approval, not submission?
- [ ] Working day calendar = Sun-Thu, off Fri-Sat?
- [ ] If deadline impossible, proposed phased mitigation included?

## Recommended Mitigations When Deadline Can't Be Met

1. **Parallel IFC prep** — Start IFC work during DD review (before formal approval) — saves 8-10 WD
2. **Negotiate 7 WD CG review** for medium-complexity IFC (AV, FLS, Stramp) instead of 14
3. **Split Basement MEP IFC** early while upper-floor DD continues
4. **Present 3-phase plan**: Phase 1 (DD+Materials by deadline) | Phase 2 (Complex IFC by mid-Sep) | Phase 3 (Coordination by handover)
