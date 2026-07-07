---
name: aseer-dmp-study
description: Complete DMP Rev C04 governance study for Aseer Regional Museum — stage gates, RACI, workflows, KPIs, and currently open issues.
category: productivity
tags: [aseer, bim, museum, samaya, dmp]
---

# Aseer Museum — DMP Rev C04 Study

## Document Identity
**Reference:** MOC-MUS-ASE-1K0-PL-0029 Rev.02 / Rev.C04
**Project:** Aseer Regional Museum (Project 3092)
**Contract:** D&B · Lump-sum milestone (Annex 4) · No remeasurement
**Authority:** BEP Rev.01 · SoW §6 · ER §2 · ISO 9001 §8.7+§10.2

---

## 1. Contractual Foundation

**Contract type:** D&B · Lump-sum milestone · Single-point responsibility
**Key rule:** Review ≠ Approval; Approval ≠ Liability Relief
**Arabic authoritative** contract language
**Samaya = Engineer of Record (EoR)** — carries design liability regardless of MoC/PMC/CG review

---

## 2. Stage Gate Programme (D0 → D300)

| Gate | Day | Lock | Sign-off |
|------|-----|------|---------|
| G1 Kick-Off | D0 | Mobilisation | PD |
| G2 50% | D35 | Design intent | CG stamp |
| G3 90% | D65 | Pre-IFC freeze | CG stamp |
| G4 IFC NOC | D82 | Construction docs | CG IFC NOC + 5 auth NOCs |
| G5 AFC NOC | D88 | As-built ready | CG AFC stamp |

**Critical watch points:**
- **D35 FLS** — FLS gates fit-out; two-step lock
- **D65 peak** — ~61 packages; PMC review peak
- **D88 Showcase** — Glasbau Hahn 14-wk lead; AFC must hit D88

---

## 3. Joint-Authorship (Sec 5.2)

| Party | Role | Owns |
|-------|------|------|
| **NRS** | R(DL/AoR) | ALL design — all 14 disciplines |
| **Samaya** | R(EoR) | Engineering (Struct/MEP) |

**Critical:** NRS authors ALL design. Any design question on ANY system goes through NRS first.

---

## 4. Design Process Tracks (Sec 6.1)

**Track 1:** LOD 300 → 350 → IFC 400
**Track 2:** 3D renders per gallery (Saudi Gallery first, D28→D65)
Both run concurrently; converge at D88.

**4-A (D0→D35):** DD — LOD 300→350
**4-B (D35→D88):** IFC — LOD 350→400

---

## 5. Submittal Lifecycle (Sec 6.3.1) — 7 Steps

```
01 Originate → 02 Internal QA → 03 CDE Upload → 04 CG Tech → 05 PMC Strat → 06 MoC NOC → 07 Distribute + Archive
         ↑                                      ↑NOC HOLD
     B1/C1 · SLA restarts                     Resolve & Re-route
```

**4 QC signatures before Aconex upload:**
1. Prepared by — NRS DL/AoR or Samaya Tech Office
2. Checked by — BIM Manager
3. Reviewed by — QA/QC Manager (Eng. Abdelmohaymen Farag)
4. Approved by — PD (Eng. Adel Darwish) + PM (Eng. Mohammed Samir)

---

## 6. RFI / TQ Routing (Sec 6.3.2)

| Query | Route | SLA | Register |
|-------|-------|-----|---------|
| RFI — Design | → NRS (DL/AoR) | 7 d | AA — RFI/TQ Log |
| TQ — Engineering | → Samaya (EoR) | 7 d | AA — RFI/TQ Log |
| Authority Query | → CG → disc lead | per auth | AA + I |
| Site Instruction | → Samaya DM | 48h ack, 7d resp | O — SI Register |

**Escalation:** CG SLA breach >7d → Conflict Resolution Matrix → CR Cat 2

---

## 7. Change Management (Sec 6.4)

### CR Cat 1 — Minor (≤5% cost/schedule, no intent change)
→ Design Manager + PD → Aconex

### CR Cat 2 — Major (intent change OR contract sum/programme impact)
→ CG → PMC + MoC formal → MoC Change Order (Art.14) → IFC re-stamp

**Freeze Points:** F1=50% · F2=90% · F3=IFC NOC · F4=AFC NOC

---

## 8. VE (Sec 6.5)

**Contract reality:** Lump-sum milestone — NO VE/Shared-Savings/Incentive clause.
Cost-reducing VE requires MoC Change Order under Art.14.

**VE 4 mandatory components:** Cost build-up · 15-yr LCC · P6 schedule · L5 finish maintained

**Auto-reject:** Object conservation · L5 finish · Accessibility · FLS/life safety · Authority compliance · NRS design intent

---

## 9. NCR Categories (Sec 6.6)

N1 DSGN · N2 CSTR · N3 QA · N4 AUTH
Severity: CRITICAL → blocks gate / MAJOR → rework / MINOR → local fix

---

## 10. Mock-Up Types (Sec 6.11)

1. **3D-R** G2 V1 → G3 V2
2. **D-MB** weekly S4-A
3. **P-MB** A2 panels G2/G3
4. **ELEM** G3
5. **FULL** G4 (IFC NOC dependency)
6. **CONS** G5

**G4 criteria:** ±2mm · ±50K · zero gaps · L5 · RT60+NR · Oddy Pass

---

## 11. Vendor Critical Path (Sec 6.13)

| Vendor | Scope | Lead | Key Gate |
|--------|-------|------|---------|
| **Glasbau Hahn** | Showcases | **14 wk** | D88 AFC |
| Rawasin | AV/IT | TBC | AV Interface Reg |
| Mada Gypsum | Drywall | 8 wk | Gap G-018 |
| ERCO/iGuzzini | Lighting | 12 wk | Lighting Strategy |

---

## 12. BIM (Sec 7)

**CDE:** Aconex · LOD: 300→350→400→500 · Zero-clash policy
**Cycle:** Tue clash → Wed review → Sun coord meeting

---

## 13. QA/QC Tiers (Sec 8.1)

L01 Self-Check → L02 Internal → [NRS gate] → L03 Coordination → L04 External Audit → NCR → L02

KPI: First-pass ≥80% · NCR closure ≥95%

---

## 14. KPIs (Sec 15)

| KPI | Target |
|-----|--------|
| On-Time Delivery | ≥95% |
| First-Time Code A | ≥85% |
| Code A/B Quality | ≥85% |
| Clash Resolution | <72h |
| LOD 400 Compliance | 100% |
| SBC/Life Safety NCRs | **Zero** |
| Mock-up First-Time | ≥90% |

**Cadence:** Weekly Tue → Monthly DPR → Per Gate

---

## 15. Open Issues (May 28, 2026)

### 🔴 Blocking
- TQ-0016 — MoC 4+ months overdue (escalate now)
- TQ-0015 — Corian/Brass need CR Cat 2 + Art.14 CO
- Type 1 recessed/showcase — NRS meeting needed
- Type 6B back panel — glass vs powder-coated metal discrepancy

### ⚠️ Watch
- Glasbau Hahn 14-wk lead (D88 gate)
- Mock-up yard (contractual — don't skip)
- VE-AR-001 pending G-018
- RFI-008 (Type 1 pull-and-slide) — NRS blocking

---

## Key Contacts

| Role | Name |
|------|------|
| Project Director | Eng. Adel Darwish |
| Project Manager | Eng. Mohammed Samir |
| BIM Lead | Ali Abdelrahman |
| QA/QC Manager | Eng. Abdelmohaymen Farag |
| Doc Controller | Hesham Ezzat |
