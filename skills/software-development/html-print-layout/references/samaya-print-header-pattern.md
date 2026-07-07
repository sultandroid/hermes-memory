# Samaya Print Header Pattern (for HTML/React Portal Print Views)

Established during the Aseer Museum Material Explorer print feature (Jun 2026).

## Header Layout

```
[Samaya logo (native white PNG)] | 6930 PROJECT NAME     [MoC] [PMC] [CG] [NRS] | Rev: X | [QR]
                                    Project Subtitle                                Date
└──────────────────────────────────────────────────────┴──────────────────────────────────────┘
                       Gold accent line (#C8A45C, 1.5px)
```

### Structure

```tsx
const header = (
  <div style={{
    position: 'relative',
    background: '#1A1D23', color: '#fff', padding: '3mm 6mm',
  }}>
    <div style={{
      display: 'flex', justifyContent: 'space-between', alignItems: 'center',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        {/* Samaya logo: native white PNG — NO filter needed */}
        <img src="samaya.png" alt="Samaya" style={{ height: 18 }} />
        <div style={{ borderLeft: '1px solid rgba(200,164,92,.35)', height: 24 }} />
        <div>
          <div style={{ fontWeight: 700, fontSize: '7pt', letterSpacing: '0.04em' }}>
            PROJECT NAME
          </div>
          <div style={{ fontSize: '5.5pt', color: '#C8A45C' }}>
            Subtitle
          </div>
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: 5 }}>
        {/* Partner logos — MUST use white filter on dark bg */}
        <img src="moc.png" alt="MoC" style={{ height: 14, filter: 'brightness(0) invert(1)', opacity: 0.85 }} />
        <img src="pmc.png" alt="PMC" style={{ height: 12, filter: 'brightness(0) invert(1)', opacity: 0.85 }} />
        <img src="cg.png" alt="CG" style={{ height: 12, filter: 'brightness(0) invert(1)', opacity: 0.85 }} />
        <img src="nrs.png" alt="NRS" style={{ height: 12, filter: 'brightness(0) invert(1)', opacity: 0.85 }} />
        <div style={{ borderLeft: '1px solid rgba(200,164,92,.3)', height: 18 }} />
        <div style={{ textAlign: 'right', fontSize: '5.5pt', color: 'rgba(255,255,255,.55)' }}>
          <div>Rev: {rev}</div>
          <div>{date}</div>
        </div>
        <img src="qrcode.png" alt="QR" style={{ width: 30, height: 30 }} />
      </div>
    </div>
    <div style={{
      position: 'absolute', bottom: 0, left: 0, right: 0,
      height: 1.5, background: '#C8A45C',
    }} />
  </div>
);
```

**⚠ CRITICAL:** Partner logos (MoC, PMC, CG, NRS) are typically dark-colored PNGs that are INVISIBLE against the dark #1A1D23 header background. Always apply `filter: brightness(0) invert(1)` to render them white. Samaya logo is already a white PNG and needs NO filter. The user explicitly flagged this: *"if the bg are dark please switch to white logos"*.

## Section Title Style (Samaya Doc H1)

Each print page's title follows the Samaya document heading style:

```tsx
<div style={{
  borderBottom: '1px solid rgba(200,164,92,.3)',
  paddingBottom: 2, marginBottom: 4,
}}>
  <div style={{
    fontFamily: "'Playfair Display', Georgia, serif",
    fontWeight: 700, fontSize: '14pt', color: '#1A1D23',
    textTransform: 'uppercase', letterSpacing: '0.02em',
  }}>{viewTitle}</div>
  <div style={{ fontSize: '7.5pt', color: '#4A4D52' }}>{viewDesc}</div>
</div>
```

## Footer Bar

```tsx
<div style={{
  borderTop: '1px solid rgba(200,164,92,.25)',
  padding: '2mm 0', marginTop: '4mm',
  display: 'flex', justifyContent: 'space-between',
  fontFamily: "'Inter', sans-serif", fontSize: '5.5pt', color: '#7E828A',
}}>
  <span>TECHNICAL OFFICE · BIM UNIT — Prepared by Samaya Technical Office</span>
  <span>Page {pageNum} of {total}</span>
</div>
```

## Page Background

- Page body: `#E8E3DB` (warm beige, same as site background)
- Each print page: `#F5F1EB` (slightly lighter, matches site card areas)
- Image containers: white `#fff` with `1px solid #ddd` border

## Key Rules

1. Partner logos are placed to the RIGHT of the header (after the vertical divider), not interleaved with the project name
2. Samaya logo is the only logo on the left — it represents the issuing party. Use the native white PNG (no `filter: brightness(0) invert(1)` needed)
3. All logos are PNGs from `/aseer/images/` (no SVGs)
4. The gold accent line spans the full header width, positioned at the bottom of the dark bar
5. No `crossorigin` attribute on script/link tags (Hostinger/LiteSpeed doesn't send CORS headers — the script silently fails)
