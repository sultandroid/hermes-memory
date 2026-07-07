# EVM S-Curve Analysis for Consultancy Contracts

## Overview

Create a cumulative S-curve chart showing Planned Value (PV), Earned Value (EV), and Actual Cost (AC) for a consultancy subcontract. The S-curve visualises schedule and cost performance at a single point in time.

## When to Use

- Subcontractor has delivered partial scope at a stated fee value
- Multiple payment milestones exist and some billing is disputed
- Need to argue that next-stage billing is premature
- Client or PMO requires objective schedule/cost performance indicators

## Data Collection

### 1. Contract Fee Breakdown

Extract from the signed contract (DOCX) or fee schedule:

| Item | SAR | % of Total |
|------|-----|-----------|
| Stage 4 (DD + IFC) | 768,000 | 63.5% |
| Stage 5 Off-site Review | 270,000 | 22.3% |
| Stages 5-6 On-site Review | 171,000 | 14.2% |
| **Total** | **1,209,000** | **100%** |

### 2. Planned Value (PV) per Month

Spread the fee across the contract duration using a logistic (S-curve) profile. Front-load slightly for design-heavy stages:

| Month | Monthly PV | Cumulative PV | Data Source |
|-------|-----------|---------------|-------------|
| Feb-2026 | 30,000 | 30,000 | Stage 4 8-week plan |
| Mar-2026 | 50,000 | 80,000 | |
| Apr-2026 | 100,000 | 180,000 | |
| May-2026 | 140,000 | 320,000 | |
| Jun-2026 | 148,000 | 468,000 | ← TODAY |
| Jul-2026 | 120,000 | 588,000 | |
| Aug-2026 | 100,000 | 688,000 | |
| Sep-2026 | 50,000 | 738,000 | |
| Oct-2026 | 30,000 | 768,000 | Stage 4 total |

**Adjustments to consider:**
- Stage 5 billing is separate (SAR 270K + 171K) — do not include in PV until Stage 5 work period begins
- If subcontractor invoices Stage 5 before Stage 4 is complete, flag as premature

### 3. Earned Value (EV)

Estimate % of Stage 4 deliverables actually completed to a satisfactory level:

| Assessment | EV % | When to use |
|-----------|------|-------------|
| 100% | All deliverables stamped/approved per contract | Only after formal sign-off |
| 50% | DD-level deliverables delivered but not formally closed | Stage 4-A complete, Stage 4-B not started |
| 25% | Partial delivery with known gaps | Some sections behind |
| 0% | No deliverables submitted | Not yet started |

**For NRS-specific: 50% of Stage 4** — DD drawings (251 files) delivered, but Stage 4-A not closed, Stage 4-B IFC not started.

EV (SAR) = % complete × Stage budget

Example: 50% × 768,000 = 384,000 SAR

### 4. Actual Cost (AC)

Sum of all verified payments from bank receipts and cleared invoices:

| Source | Amount | Status |
|--------|--------|--------|
| Advance Payment (10%) | 120,900 | Confirmed (bank transfer) |
| Monthly Instalment #1 | X | Check invoice + bank receipt |
| Monthly Instalment #2 | Y | Check invoice + bank receipt |
| **Total AC** | **345,657** | At Jun 2026 (example) |

## SVG Chart Construction

### Chart Canvas Setup

```
<svg viewBox="0 0 1123 794" width="297mm" height="210mm">
  <rect width="1123" height="794" fill="#0F172A" />     <!-- dark background -->
```

### Coordinate Mapping

| Variable | Value | Why |
|----------|-------|-----|
| Chart area Y range | 145 (top) to 465 (bottom) | Vertical space for curves |
| Y-axis baseline | y = 352 | Where 0 SAR sits |
| Max Y (top of chart) | y = 152 | Where 800K SAR sits |
| Scale factor | 4.0 | 800K / (352-152) = 4K per pixel |
| X-axis start | x = 140 | Feb (month 1) |
| X-axis end | x = 940 | Oct (month 9) |
| Months mapping | x = 140 + (month_index × 100) | Feb at 140, Oct at 940 |

### Coordinate Formula

```
pixel_y = max_y - (SAR_value_in_K / scale_factor)
```

### PV S-Curve Data Points

| Month | Cumulative SAR | X | Y Calculation | Y |
|-------|---------------|---|-------------|---|
| Feb | 30K | 140 | 352 − 30/4 = 344.5 | 344 |
| Mar | 80K | 240 | 352 − 80/4 = 332 | 332 |
| Apr | 180K | 340 | 352 − 180/4 = 307 | 307 |
| May | 320K | 440 | 352 − 320/4 = 272 | 272 |
| **Jun** | **468K** | **540** | **352 − 468/4 = 235** | **235** |
| Jul | 588K | 640 | 352 − 588/4 = 205 | 205 |
| Aug | 688K | 740 | 352 − 688/4 = 180 | 180 |
| Sep | 738K | 840 | 352 − 738/4 = 167.5 | 168 |
| Oct | 768K | 940 | 352 − 768/4 = 160 | 160 |

### EV S-Curve Data Points (example: 50% = 384K at Jun)

| Month | Cumulative SAR | X | Y | Notes |
|-------|---------------|---|---|-------|
| Feb | 15K | 140 | 348 | Slow start |
| Mar | 30K | 240 | 344 | |
| Apr | 60K | 340 | 337 | |
| May | 180K | 440 | 307 | DD delivery ramps up |
| **Jun** | **384K** | **540** | **256** | 50% of Stage 4 complete |
| Jul | 460K (forecast) | 640 | 237 | |
| Aug | 550K (forecast) | 740 | 214 | |
| Sep | 650K (forecast) | 840 | 189 | |
| Oct | 768K (target) | 940 | 160 | |

### AC S-Curve Data Points

| Month | Cumulative SAR | X | Y |
|-------|---------------|---|----|
| Feb | 30K | 140 | 344 |
| Mar | 80K | 240 | 332 |
| Apr | 120K | 340 | 322 |
| May | 250K | 440 | 289 |
| **Jun** | **345K** | **540** | **266** |

### SVG Polyline Construction

```svg
<!-- PV curve (solid green) -->
<polyline points="140,344 240,332 340,307 440,272 540,235 640,205 740,180 840,168 940,160"
  fill="none" stroke="#22C55E" stroke-width="2.5" />

<!-- EV curve (dashed blue) -->
<polyline points="140,348 240,344 340,337 440,307 540,256"
  fill="none" stroke="#3B82F6" stroke-width="2.5" stroke-dasharray="6,3" />

<!-- EV forecast (faded dashed blue) -->
<polyline points="540,256 640,237 740,214 840,189 940,160"
  fill="none" stroke="#3B82F6" stroke-width="1.5" stroke-dasharray="3,3" opacity="0.5" />

<!-- AC curve (solid amber) -->
<polyline points="140,344 240,332 340,322 440,289 540,266"
  fill="none" stroke="#F59E0B" stroke-width="2.5" />
```

### Variance Arrows at TODAY Line

```svg
<!-- TODAY vertical line -->
<line x1="540" y1="130" x2="540" y2="465" stroke="#F59E0B" stroke-width="1.5" stroke-dasharray="4,3" />

<!-- SV arrow: from EV(256) up to PV(235) -->
<line x1="540" y1="256" x2="540" y2="235" stroke="#EF4444" stroke-width="1.5" />
<polygon points="535,240 540,232 545,240" fill="#EF4444" />   <!-- up arrowhead -->

<!-- CV arrow: from AC(266) up to EV(256) -->
<line x1="545" y1="266" x2="545" y2="256" stroke="#22C55E" stroke-width="1.5" />
<polygon points="540,261 545,253 550,261" fill="#22C55E" />   <!-- up arrowhead -->
```

The arrow length in pixels × scale_factor = SAR difference:
- SV gap = (256 − 235) × 4 = 84K (verify against stated SV)
- CV gap = (266 − 256) × 4 = 40K (verify against stated CV)

## Embedding in HTML Report

### Method: Replace `</body></html>`

```python
svg_path = "/path/to/_assets/chart.svg"
with open(svg_path) as f: svg = f.read()
with open(html_path) as f: html = f.read()

chart_sheet = (
    '<div class="sheet" style="width:297mm;min-height:210mm;">\n'
    '<div class="doc-strip">...</div>\n'
    '<div style="width:100%;overflow:hidden;">\n'
    + svg + '\n'
    '</div>\n'
    '<div class="doc-strip">...SHEET N/6</div>\n'
    '</div>\n\n'
    '</body></html>\n'
)

html = html.replace('</body></html>', chart_sheet)
# Bump last-sheet counter
html = html.replace('SHEET 5/5', 'SHEET 5/6')
with open(html_path, "w") as f: f.write(html)
```

Always use a Python script file (never inline in a heredoc that has conflicting `&amp;` or quote characters).

## Verification Checklist

Pass to a subagent (Claude Code) for independent verification:

```
[ ] SVG is valid XML (no missing closing tags)
[ ] All 3 curves have correct number of data points
[ ] PV Y-coordinates = 352 − value/4, rounded correctly
[ ] EV Y-coordinates = 352 − value/4, rounded correctly
[ ] AC Y-coordinates = 352 − value/4, rounded correctly
[ ] SV arrow gap (px) × 4 = stated SV in K SAR
[ ] CV arrow gap (px) × 4 = stated CV in K SAR
[ ] TODAY line at correct month (June = x=540)
[ ] Metric cards match chart values
[ ] Key at bottom matches chart values
[ ] Assessment recommendations are actionable
[ ] Dark theme matches existing reports (#0F172A, #1E293B, #334155)
[ ] No duplicate attributes in SVG elements
[ ] No orphan </tspan> or </text> tags
```

The subagent WILL find coordinate errors your hand-calculation missed. Do not skip this step.

## Common Errors

| Error | Symptom | Fix |
|-------|---------|-----|
| Wrong Y-axis formula | Curves don't match stated values | Recalculate with y = 352 − V/4 |
| Wrong PV magnitude | Chart shows Jun PV as 460K instead of 614K | Use actual fee schedule, not visual guess |
| Arrow position mismatch | Arrow gap doesn't match variance | Calculate gap × 4 and compare to SV/CV |
| Duplicate SVG attributes | Invalid XML | Search for repeated attribute names in SVG |
| Orphan XML tags | SVG won't render properly | Check all <tspan> have matching </tspan> |
| AC > EV but arrow wrong | Arrow shows wrong direction | EV(256) → AC(266) means AC > EV = CV positive |
