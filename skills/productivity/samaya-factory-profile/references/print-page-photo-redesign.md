# Print Page (p14) Photo-Driven Redesign

Use when user says "photos too small" on the Print Machines page (#p14, class v4-cmyk).

## The Problem

The page historically overflowed ~23mm. Fit-fixes in `45-overrides.css` crushed photo sizes:
- Machine card images: 17mm min-block-size
- Evidence bar images: 20mm block-size
- QA photo: 19mm min-block-size
- Hero photo: ~45mm (shared column)

## The Fix (2-page photo-led spread)

### Step 1 — Remove fit-fix overrides

Remove all `#p14`-specific rules from `45-overrides.css` (lines ~31-44). These suppress photo sizes:
```css
#p14 .v4-cmyk-evidence-img { block-size: 20mm; }
#p14 .v4-cmyk-app-img { min-block-size: 17mm; }
#p14 .v4-cmyk-qa-img { min-block-size: 19mm; }
/* etc. */
```

### Step 2 — Split into 2 pages

**Page 1 (p14)**: HERO + MACHINES
- CMYK calibration bar (top)
- Full-width hero photo (85mm) with gradient overlay, ΔE badge
- 4 machine cards in 2×2 grid with 42mm photos
- CMYK bar (bottom, decorative)

**Page 2 (p14b)**: PROCESS + OUTPUTS
- Process flow (4 steps, compact)
- Evidence bar (3 detail photos, 32mm)
- Substrates strip (9 approved substrates)
- QA note with 50mm photo + stats

### Step 3 — Add CSS to 38-cmyk.css

Add rules for the new large photos:
```css
#p14 .v4-cmyk-hero-full { min-block-size: 85mm; }
#p14 .v4-cmyk-apps { grid-template-columns: repeat(2, 1fr); }
#p14 .v4-cmyk-app-img { min-block-size: 42mm; }
#p14b .v4-cmyk-evidence-img { block-size: 32mm; }
#p14b .v4-cmyk-qa-img { min-block-size: 50mm; }
```

Also remove `overflow: hidden` and `height: calc(210mm ...)` from `.v4-cmyk .content` in 38-cmyk.css to allow 2-page flow.

### Step 4 — Post-redesign checks

- TOC: update p14 entry label, add p14b sub-entry, verify p15 entry preserved
- Footer: p14b → `<div class="num">14b</div>` (matches p13b → `13b` pattern)
- Image paths: all 7 photo paths must exist on disk
- Brand names: verify Durst/Roland removed (should be "UV Flatbed" and "Roll-to-Roll Solvent")

## Photo Size Reference

| Element | Before | After |
|---------|--------|-------|
| Hero photo | ~45mm | **85mm** full-width |
| Machine card photos | 17mm | **42mm** |
| Evidence bar photos | 20mm | **32mm** |
| QA photo | 19mm | **50mm** |

## CSS File Location

- `45-overrides.css` — REMOVE #p14 fit-fix lines
- `38-cmyk.css` — ADD new large-photo rules
- HTML — REPLACE old single-page section with 2-page structure
