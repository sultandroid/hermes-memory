# Exhibition/Museum MEP Systems — Complete Scope Checklist

For a modern museum/exhibition fit-out at 3,500 sqm scale, the BMA scenographic design package only covers exhibition-facing power and AV containment. The following systems are typically required and may be missing or at ballpark estimate.

Status legend:
- In BMA set: `YES`
- Partial — containment/panel only, no system design: `PARTIAL`
- Missing or ballpark estimate: `NO`

## Power & Electrical

| System | In BMA? | Why It Matters |
|--------|---------|----------------|
| LV power distribution (MDB, SMDB, final DBs) | YES | Baseline |
| Exhibition lighting grid / track busbar + Grid Switch Panel | YES | Galleries are re-lamped per show |
| Lighting distribution + dimming/control (DALI/DMX drivers) | PARTIAL | Panel is there, control system isn't |
| Showcase & plinth small power (integral, concealed) | NO | Each case needs concealed fused power + data |
| Floor boxes / poke-throughs to exhibits | NO | Free-standing exhibits need fed from slab |
| UPS — unit sizing, runtime, installation | PARTIAL | Conduit exists, unit spec/sizing missing |
| Standby/emergency generator interface + ATS | NO | Conservation HVAC and security cannot ride mains alone |
| Clean technical earth + equipotential bonding | NO | AV ground loops = hum/buzz on audio |
| Surge protection (SPD, multi-stage) | NO | KSA grid + expensive AV/IT electronics |
| Power-factor correction | NO | Large dimmed LED + AV loads |

## Life-Safety ELV — Mandatory Under Civil Defense

| System | In BMA? | Why It Matters |
|--------|---------|----------------|
| Fire detection & alarm (FACP, addressable) | PARTIAL | RCP shows fire device positions, system design separate |
| Aspirating smoke detection (VESDA) | NO | High-ceiling galleries — point detectors don't work at height |
| Voice evacuation / PAVA | NO | Public assembly occupancy requires intelligible voice alarm |
| Emergency & escape lighting + exit signage | NO | Blackout galleries are the hard case |
| Clean agent suppression (NOVEC/FM-200) | NO | Rackroom and collection stores can't take sprinkler water |

## Security ELV

| System | In BMA? | Why It Matters |
|--------|---------|----------------|
| CCTV / video surveillance + NVR | NO | Insurance/loan-agreement requirement |
| Access control + intrusion detection | NO | After-hours zoning, rackroom, plant |
| Object/artifact protection (case alarms, proximity, vibration) | NO | Exhibition-unique — tied to showcase fabrication |

## AV, Interactive & Lighting-Control

| System | In BMA? | Why It Matters |
|--------|---------|----------------|
| AV headend / rackroom + AV panel | YES | Confirmed in cable schedule |
| AV system design (displays, projectors, media players) | PARTIAL | Cable schedule exists, system design is specialist package |
| Interactive exhibit power + data (kiosks, touch, AR/sensors) | NO | Bespoke per exhibit, high outlet/data density |
| Lighting control system (DALI/DMX scene processors) | NO | Brains, separate from panels |
| Showcase integral lighting (LED drivers, fibre-optic) | NO | Conservation-grade, low-UV, dimmable |

## IT / Network Infrastructure

| System | In BMA? | Why It Matters |
|--------|---------|----------------|
| Structured cabling / data backbone + comms room | NO | Every ELV system rides on it |
| Wi-Fi / WLAN (visitor + back-of-house) | NO | Visitor app, wireless interactives |
| Assistive listening / induction loop | NO | Accessibility/code in public galleries |
| Digital signage / wayfinding | NO | Entry, orientation |

## Conservation / Environmental

| System | In BMA? | Why It Matters |
|--------|---------|----------------|
| Environmental monitoring (T/RH dataloggers, alarms) | NO | Loan agreements demand documented stable temp/RH |
| BMS integration / showcase microclimate control | PARTIAL | RCP HVAC coordination only |
| Lightning protection (building interface) | NO | Asset/electronics protection |

## The Five That Will Hurt the Proposal

1. **Life-safety package** — FA, voice evac, emergency lighting, VESDA. Mandatory under Civil Defense, never in a scenographer's set.
2. **Security suite** — CCTV, access control, artifact protection. Insurance/loan blocker.
3. **Structured cabling** — Every other ELV system depends on it. If it's a one-line allowance, the whole ELV estimate is soft.
4. **Interactive + showcase small-power/data** — Quantity-driven, routinely under-counted.
5. **UPS unit + clean earth + surge protection** — UPS conduit exists but no unit, no technical earth. AV won't perform without them.

## Recommendation

Treat the BMA set as the exhibition power + lighting-grid + AV-containment layer only. Raise a TQ/clarification asking the employer to confirm scope-ownership of life-safety, security, IT, and conservation systems before pricing. Otherwise carry them as provisional sums with a stated basis.