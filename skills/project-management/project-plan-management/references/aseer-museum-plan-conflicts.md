# Aseer Museum Plan Conflicts & Gaps — Reference

> Concrete findings from the 2026-07-11 consolidated analysis. Use as a checklist when auditing any D&B museum project's plan set.

## Critical Conflicts Found

| Conflict | Plan A | Plan B | Impact |
|----------|--------|--------|--------|
| Review period: 14 calendar vs 14 working days | DMP §3.2 (ER §2.4.A) | Communication Plan OBJ-3 | ~40% difference in SLA |
| Handover date: 01 Mar 2027 vs 30 Sep 2026 | PEP §1 (P01 draft) | All other plans + AGENTS.md | 5-month gap — PEP may be wrong |
| LOD: 300 vs 350/400 | DMP §1.7 (SoW §6.20) | BEP §5 | DMP needs updating to reference BEP |
| Sub-consultant approval: MoC vs no privity | DMP §2.2 (Contract §4 Art. 13) | Procurement §2.1 | Wording mismatch — both are correct but need reconciliation note |

## Common Overlap Clusters

These requirements appear in 4+ plans and should be de-duplicated to a single governing plan:

1. **Document control / CDE** — 6 plans (DMP, Comm Plan, PEP, BEP, PQP, Resource)
2. **Design review & approval** — 4 plans (DMP, PEP, PQP, Comm Plan)
3. **Quality control & inspection** — 5 plans (PQP, DMP, PEP, Procurement, BEP)
4. **Testing & commissioning** — 5 plans (DMP, PEP, PQP, Comm Plan, SMP)
5. **Handover deliverables** — 6 plans (DMP, PEP, PQP, BEP, Comm Plan, SMP)
6. **Risk management** — 5 plans (RMP, PEP, Procurement, Resource, Mobilization)

## Missing Plans (7)

1. Schedule Management Plan
2. Cost Management Plan (with EVM)
3. Change Management Plan
4. Commissioning Plan (integrated)
5. Security Management Plan
6. IT/AV Integration Plan
7. Training Plan

## Cross-Plan Integration Gaps (8)

| Missing Link | Between |
|-------------|---------|
| Risk register ↔ Procurement lead times | RMP ↔ Procurement |
| Quality KPIs ↔ Risk triggers | PQP ↔ RMP |
| Resource plan ↔ Mobilization schedule | Resource ↔ Mobilization |
| Sustainability ↔ Procurement evaluation | SMP ↔ Procurement |
| BIM deliverables ↔ Quality ITPs | BEP ↔ PQP |
| Communication SLAs ↔ Risk triggers | Comm Plan ↔ RMP |
| HSE plans ↔ Mobilization | HSE ↔ Mobilization |
| Stakeholder changes ↔ Communication updates | Stakeholder ↔ Comm Plan |

## Compliance Obligations — Typical Counts by Category

| Category | Count | Key Sources |
|----------|-------|-------------|
| Contractual | ~10 | ER §2.4, Contract §4, §5, §6 |
| Regulatory (codes) | ~15 | SBC 201/401/501/601/801/1001, NFPA, MOI, CITC, SEC, Oddy, Mostadam |
| Quality (PQP KPIs) | ~8 | First-time approval ≥85%, NCR ≤14d, ITP 100%, rejection ≤3%, snags ≤50 |
| Communication (SLAs) | ~6 | Report ≥95%, submittal ≤14wd, RFI ≤7wd, Aconex 100% |
| Sustainability (SMP) | ~12 | VOC ≤0.5, waste ≥60%, gallery 21±1°C/50±5%RH, Mostadam Silver 45+ |
| HSE | ~10 | NFPA 10/241/51B, SBC 801, Civil Defense, zero LTI |
| BIM | ~9 | LOD compliance, weekly updates, clash reports, as-built, COBie |

## Dependency Chains (6)

```
Design → Procurement → Construction:
  DMP §4 → Procurement §7 → Procurement §9 → Mobilization §9 → PQP §7 → PEP §8 → DMP §7/PQP §9

BIM → Quality → Handover:
  BEP §3 → BEP §5 → BEP §7 → PQP §6 → BEP §6.6 → DMP §8/BEP §3

Risk → Procurement → Schedule:
  RMP §4 → RMP §9 → Procurement §11 → Procurement §9 → PEP §5

Stakeholder → Communication → Escalation:
  Stakeholder §4 → Stakeholder §6 → Communication §3 → Communication §7 → RMP §9

Sustainability → Procurement → Quality:
  SMP §2.2 → SMP §7 → SMP §9 → Procurement §8 → PQP §7 → SMP §11

HSE → Mobilization → Construction:
  HSE Plans → Mobilization §12 → Mobilization §6 → PEP §11 → PQP §9
```
