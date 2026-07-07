# Showcase Specialist Review — T&H Monitoring & Microclimate Reports

## When to use

Review any museum showcase environmental report (T&H monitoring, microclimate control) as a specialist. Apply this structured critique before the report goes to the client or loan authority.

## Review dimensions (check in order)

### 1. Device Selection Audit

| Check | What to flag |
|---|---|
| Wireless range | Bluetooth-only devices (~30m) need gateway per zone. Recommend RF/cellular for real-time remote. |
| Manual download devices | Testo 174H, EL-USB-2 — no wireless, defeats alert system. Mark as backup-only or remove. |
| Transmitters vs loggers | Rotronic HF5 is a transmitter, not a logger — needs external power + cabling. Not suitable for wireless retrofit. |
| Missing sensor types | Light/lux sensor required for most loan agreements. CO₂ if occupancy affects environment. |
| Calibration | No calibration schedule = major gap. Require NIST-traceable annual calibration. |

### 2. Threshold Corrections

| Parameter | Standard (BS EN 15757 / PAS 198) | Common error in reports |
|---|---|---|
| T change/hr | ±1°C/hr | Often written as ±2°C/hr — too loose for loaned artifacts |
| RH change/hr | ±5%/hr | Usually correct |
| RH critical low | <35% is correct, but amber should trigger at <40% to prevent desiccation | Reports often set amber too low |
| Light level | <150 lux for sensitive materials | Often missing entirely |
| Temperature range | 18-22°C for mixed collections | Usually correct |

### 3. Logger Distribution Gaps

| Area often missed | Why it matters |
|---|---|
| HVAC return air | Detects HVAC failure before it reaches showcases |
| Buffer/staging room | Artifacts staged here before installation — must be monitored |
| Spares (explicit count) | "Including spares" is too vague. State 2-3 explicitly. |

### 4. Missing Critical Sections

| Section | What it must cover |
|---|---|
| Loan agreement compliance | Verify lender's tolerances before procurement. Lenders may specify tighter ranges. |
| Integration with microclimate | If active control units exist (Freeair FL-Z81, CCI RH-33), monitoring validates their performance, not replaces them. |
| Sensor placement protocol | Center of showcase, away from airflow, 10cm from artifacts, no direct sunlight. |
| Tamper-proof mounting | Security bracket + Torx screw. Loggers visible to visitors. |
| Data integrity / backup | Local storage on logger even if gateway fails. Sync on reconnection. |
| Commissioning baseline | Minimum 2 weeks of baseline data before artifact placement. |
| Alarm testing protocol | Monthly test without triggering false evacuation. 4-test sequence: sensor trigger → notification → escalation → gateway failover. |
| Calibration schedule | Annual NIST-traceable. Quarterly accuracy check. |

### 5. Cost Estimate Verification

| Common error | Reality |
|---|---|
| Underestimates by ~40% | Distributor markup, shipping, cloud subscription, spares, mounting kits all add up. |
| Missing cloud subscription | HOBOlink ~$600/yr. Not a one-time cost. |
| Missing spares | 2-3 spare loggers at ~$200 each. |
| Missing mounting/security | Brackets, adhesive mounts, Torx screws. |

## Report structure (revised, 12 sections)

1.0 Introduction — project context, showcase architecture, microclimate integration
2.0 Recommended Devices — table with notes, removed devices explained
3.0 Monitoring Architecture — 3-tier + data integrity
4.0 Reading Frequency — per location type
5.0 Alert Thresholds — with standard references + loan agreement caveat
6.0 Logger Distribution Plan — per cluster, not per showcase
7.0 Sensor Placement and Security — placement rules + tamper-proof mounting
8.0 Calibration and Maintenance — annual/quarterly schedule
9.0 Commissioning and Baseline — 2-week minimum
10.0 Reporting and Documentation — report types table
11.0 Loan Agreement Compliance Check — pre-procurement verification
12.0 Recommendation — device rationale + revised cost estimate

## Key corrections to watch for

- **Showcase count ≠ logger count.** Connected clusters share air volume → 1 logger per cluster, not per showcase.
- **"24-26 devices" is too high** for 18 showcases in 4 clusters. Realistic: 16-19 including HVAC return + buffer + spares.
- **Cost estimate $3,500-$5,000 is ~40% under.** Realistic: ~$7,300 for HOBO system with cloud subscription.
- **Testo 174H** has no wireless — remove from primary recommendation.
- **Rotronic HF5** is a transmitter, not a logger — remove.
- **Light monitoring** is required by most loan agreements — add if missing.
