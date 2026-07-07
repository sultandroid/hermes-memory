# Museum Microclimate / T&H Monitoring Action Report Pattern

## Domain rule — connected vs individual showcases

| Arrangement | Units required | Example |
|-------------|---------------|---------|
| Connected clusters (share air volume) | 1 per cluster, not per showcase | Zamzam: 18 showcases in 4 clusters → 4 units |
| Individual sealed showcases | 1 per showcase | Aseer: 27 individual showcases → 27 units |

**Always verify** from the Showcase Schedule whether showcases share internal air volume. The `Climate Control` field ("P" for passive) is not the determining factor — the physical architecture (open-frame vs sealed individual) is.

## Report types to generate together

Two complementary reports:

1. **Microclimate Control Action Report** — active T/RH control units
2. **T&H Monitoring Action Report** — data logging, alerts, response protocol

Generate both in a single script to share data structures (showcase counts, distribution plan).

## Sections per report

### Microclimate Control (7 sections)
1.0 Introduction — project context, showcase count, architecture
2.0 Recommended Solution — device type, components table
3.0 Methodology — control cycle flowchart + installation flowchart
4.0 Distribution Plan — table: gallery/showcase IDs/type/qty/units
5.0 Cost Estimate — itemised, costs TBC
6.0 Comparison — alternatives table
7.0 Recommendation + next steps

### T&H Monitoring (8 sections)
1.0 Introduction — same context
2.0 Recommended Devices — logger types table
3.0 Monitoring Architecture — 3-tier: Field → Aggregation → Cloud (+ SVG)
4.0 Reading Frequency — per location type
5.0 Alert Thresholds — amber/red + response escalation
6.0 Logger Distribution Plan — per-showcase table
7.0 Reporting & Documentation — report types table
8.0 Recommendation + device rationale

## SVG flowcharts for DOCX

Three flowcharts needed:

| SVG | Content | viewBox size |
|-----|---------|-------------|
| Control Cycle | Closed-loop: Showcase Air → Filter → Sensor → Controller Decision → Peltier/Humidifier → Fan → Return | 1100×520 |
| Installation Methodology | 8 steps (2 rows of 4): Site Survey → Unit Selection → Mount → Power → Setpoint Config → Stabilization Test → Calibration Verify → Artifact Placement | 1100×520 |
| Monitoring Architecture | 3-tier stack: Field (loggers) → Aggregation (gateway) → Cloud (dashboard) | 1100×400 |

Use inline SVG strings (Python constants) with the inline-string `add_svg_to_doc` variant (see `references/svg-embedding-docx-pattern.md`). Run gen script with:
```
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib python3 gen_script.py
```

## Cost presentation rules

- Only branded option (CCI RH-33 class) in formal reports — no Alibaba/cheap alternatives
- Mark all prices as TBC — "Final pricing requires supplier quotation"
- Include installation, commissioning/calibration, and shipping as separate line items
- Silica gel in comparison table: ~$200 per showcase (passive, no control)

## Verification

Before presenting, verify:
- Showcase count and architecture from actual NRS Showcase Schedule JSON
- Unit count = clusters for connected, unit count = showcases for individual
- Logger count = showcases + gallery zones (6-8) + spares
- Cost totals are internally consistent (qty × unit price = subtotal)