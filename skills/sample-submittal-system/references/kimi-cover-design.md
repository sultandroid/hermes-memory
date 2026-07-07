# Kimi-Style Folder Cover Design

Reference for the double-sided folder cover used as the landing page for material samples. Adapted from the Kimi Agent React prototype for SAM-FIN-PB-001.

## Source

The original Kimi prototype was a Vite + React + shadcn/ui app hosted at `https://5lnk5b4nnjcvo.kimi.page/`. The React source was reverse-engineered from the JS bundle to produce a standalone HTML/CSS version.

## Front Cover Layout (A4 portrait — 210×297mm)

```
┌─────────────────────────────────────┐
│ [Samaya logo]          MATERIAL CODE│
│                         SAM-FIN-XXX│
├─────────────────────────────────────┤
│                                     │
│                                     │
│         Material Name               │
│         (Playfair Display 40px)     │
│                                     │
│   [TYPE BADGE] · Finish desc        │
│                                     │
│  ┌───────────────────────────────┐  │
│  │ SPECIFICATIONS                │  │
│  │ SUBSTRATE  AISI 304 · 1.5mm  │  │
│  │ FINISH     PVD Coating ...    │  │
│  │ HARDNESS   2,000–3,000 HV     │  │
│  │ CORROSION  Salt-spray 500+hrs│  │
│  │ APPLICATIONS                  │  │
│  │  [Cladding] [Hardware] ...    │  │
│  │ ● Active                      │  │
│  └───────────────────────────────┘  │
│                                     │
│ SUBMITTAL REFERENCE                  │
│ MOC-MUS-ASE-1A0-MA-XXXX             │
│                                     │
│ ┌──┐                                │
│ │QR│ Scan for datasheet             │
│ └──┘                                │
├─────────────────────────────────────┤
│ [CG] │ [NRS] │ [PMC] │ [GBH]       │
│ Cons.│Nissen │ PMC   │ Glasbau Hahn│
└─────────────────────────────────────┘
```

## Back Cover Layout

```
┌─────────────────────────────────────┐
│                         SAM-FIN-XXX│
│                                     │
│            [Samaya logo]            │
│                                     │
│          ╭─────────────╮            │
│          │    [QR]     │            │
│          ╰─────────────╯            │
│     samaya-factory.com/Samples/...  │
│                                     │
│       SAMAYA TECHNICAL OFFICE       │
│         Aseer Museum · KSA          │
│                                     │
│            SAM-FIN-XXX              │
│       MOC-MUS-ASE-1A0-MA-XXXX       │
│              ───────                │
│          MATERIAL SAMPLE            │
│                                     │
│                                     │
│   [CG]  [NRS]  [PMC]  [GBH]        │
└─────────────────────────────────────┘
```

## Color Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Navy | `#13151A` | Full background |
| Bronze | `#C8904A` | Accents, code, badges, spec headers |
| White | `#FFFFFF` | Text, logos (inverted) |
| Muted white | `rgba(255,255,255,.35)` | Secondary text |
| Panel bg | `rgba(255,255,255,.04)` | Specs panel background |
| Panel border | `rgba(255,255,255,.06)` | Specs panel border |

## Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Material name | Playfair Display | 40px | 600 |
| Type badge | Inter | 9px | 600 |
| Spec labels | Inter | 7.5px | 600 |
| Spec values | Inter | 9px | 400 |
| Code | Inter monospace | 10px | 400 |
| Party names | Inter | 7px | 400 |

## Key Measurements

- Cover: 210mm × 297mm (A4 portrait)
- Top bar: 18px padding top/bottom, 28px left/right
- Hero area: flex:1, centered vertically
- Specs panel: 16px/20px padding, 4px border-radius
- QR: 50px × 50px (front), 60px × 60px (back in 90px ring)
- Party logos: 14px height, 0.5 opacity
- Decorative rings: 220px and 160px diameter, 0.04/0.03 opacity
- Party strip: 10px padding, 16px gap between items

## Print Settings

```css
@page { size: A4 portrait; margin: 0; }
@media print {
  * { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  .front-cover, .back-cover { box-shadow: none; margin: 0; page-break-after: always; }
}
```

## Adapting for a New Sample

Variables to replace:
1. Material name (h1, title tag)
2. Code (SAM-FIN-XXX) — 4 places: top-ref-code, bg-type, back-ref-code, QR URL
3. Type badge text (e.g. "Metal Finish")
4. Subtitle text (e.g. "Brushed Colour — Patinated Brass Match")
5. Specs: Substrate, Finish, Hardness, Corrosion, Gauges
6. Applications list (7 items in apps-grid)
7. Submittal ref (MOC-MUS-ASE-XXXX-XX-XXXX)
8. QR image filename
9. Photo image filename (back cover doesn't use photo)
