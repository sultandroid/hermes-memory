# Risk Archetypes by Discipline — Cheat Sheet

Quick-reference archetypes to scan for when studying design documentation. Not exhaustive — use as a starting checklist.

## Lighting

| Archetype | Signal | Risk ID Pattern |
|-----------|--------|-----------------|
| Conservation lux/UV gap | No CIE 157:2004 reference in specs | DDR-LGT-002 |
| Single-source fixture dependency | Only one manufacturer per fitting type | DDR-LGT-003 |
| Ceiling void coordination clash | RCP shows fixtures but no structural/MEP overlay | CO-L-001 |
| Dual-protocol control complexity | DALI + separate DMX/Casambi in same project | DDR-AV-003 |
| Feature suspension uncoordinated | 7m+ suspended light without structural sign-off | DDR-STR-003 |
| Emergency/house dual-function | Same fitting does house + emergency — generator dependency | DDR-FLS-005 |
| External lighting orphan | Stramp/terrace designed by ZNA but executed by unappointed D&B MEP | LG-024 gap |
| Object-list cascade dependency | Design relies on unfrozen MoC object data | DDR-DES-005 |
| Heat load additive to HVAC | Lighting heat gain >5 kW not in cooling calculation | DDR-MEP-003 |
| Acoustic treatment conflict | Light boxes/baffles compete with ceiling acoustic spec | DDR-ACO-001 |

## AV / Multimedia

| Archetype | Signal | Risk ID Pattern |
|-----------|--------|-----------------|
| 12-16 week lead time | Specialist hardware with no early procurement | DDR-AV-002 |
| Heat/visibility conflict with lighting | Projector placement in high-ambient-light gallery | DDR-AV-003 |
| Mounting point uncoordinated | Projector/speaker suspension not in structural register | DDR-STR-003 |
| Integration protocol mismatch | AV control protocol different from lighting (e.g. Crestron vs DALI) | DDR-AV-001 |
| Content dependency | AV content relies on MoC-supplied media not yet received | DDR-AV-001 |

## MEP

| Archetype | Signal | Risk ID Pattern |
|-----------|--------|-----------------|
| Existing services undocumented | No riser diagrams, no plant room as-built | DDR-MEP-002 |
| Cooling capacity insufficient | Sum of AV + lighting + occupancy heat exceeds chiller | DDR-MEP-003 |
| Humidity control beyond HVAC zone capability | 45-55% RH target in gallery vs zone-based HVAC | DDR-MEP-004 |
| Design basis lagging programme | MEP lead time 12-16 weeks but 50% gate approaching | DDR-MEP-001 |
| Ceiling void routing clash with downstand beams | Ducts/lights/sprinklers compete for same void space | DDR-MEP-006 / NRS-06 |

## Structural

| Archetype | Signal | Risk ID Pattern |
|-----------|--------|-----------------|
| Slab loading unverified | BOD/submission Code C — loading assumptions unfrozen | DDR-STR-001 |
| Authority rejection risk (Stramp) | Stramp gradient standard (1:12 vs 1:20) unresolved | DDR-STR-002 |
| Suspension point uncoordinated | No coordinated suspension-point register | DDR-STR-003 |
| Vibration/deflection risk | Peak visitor loading + Stramp connection assumptions unvalidated | DDR-STR-004 |

## Showcases

| Archetype | Signal | Risk ID Pattern |
|-----------|--------|-----------------|
| Long lead time | 14-week minimum — PO must be placed early | DDR-SHC-001 |
| Oddy test failure | Paint/adhesive/substrate fails conservation testing | DDR-SHC-002 |
| Microclimate conflicts with HVAC | Individual showcase RH requirements vs zone HVAC | DDR-SHC-003 |
| Security requirements exceed manufacturer capability | Custom glazing/locking/environmental spec beyond supplier | DDR-SHC-004 |
| Alarm scope exclusion | Showcase alarm not in base scope — MoC/insurer acceptance needed | DDR-SHC-005 |

## Graphics

| Archetype | Signal | Risk ID Pattern |
|-----------|--------|-----------------|
| MoC content not received | Client content research incomplete | DDR-GRA-001 |
| Arabic text errors detected late | Proofing resource insufficient | DDR-GRA-002 |
| Substrate/fire rating conflict | Graphic build-up incompatible with wall finish or fire class | DDR-GRA-003 |

## Cross-Discipline / General

| Archetype | Signal | Risk ID Pattern |
|-----------|--------|-----------------|
| New object/customer data triggers redesign | Client data received after design is underway | DDR-DES-005 |
| Key personnel unavailable | Approved specialist replaced without CG approval | DDR-RES-001 |
| Design scope exceeds tender assumption | ER/SOW requirements exceed lump-sum design fee | DDR-COM-001 |
| CG comment not closed | 57 unresolved pre-contract drawing comments | DDR-ARC-002 |
| Design approval lags downstream | Architecture 50% approved but status unclear | DDR-ARC-001 |
