# 480×230mm Sample Label — Formal Samaya Style (v2 Tokens)

Reference pattern for the 480×230mm landscape folder label redesigned with
Samaya `_Style-Guides` v2 tokens (navy/sky).

## Grid structure

```
┌──────────────────────────────────────────────────────┐
│ TOP STRIP  17mm  · navy #0F172A · sky bottom border  │
├──────────────────────────────────────────────────────┤
│ HERO  39mm  · sample name h1 · submittal ref panel   │
├───────────────────┬──────────────────────────────────┤
│ PHOTO PANEL 286mm │ INFO PANEL  1fr                   │
│ warm #F4F1EA bg   │ white bg · grid rows:             │
│  ┌─────────────┐  │  auto / minmax(0,1fr) / auto     │
│  │  photo      │  │                                   │
│  │  frame      │  │  info-head · info-grid · qr-band  │
│  └─────────────┘  │                                   │
├───────────────────┴──────────────────────────────────┤
│ FOOTER  14mm  · navy #0F172A · Samaya / Project / Ref │
└──────────────────────────────────────────────────────┘
```

## CSS grid rows

```css
.label-sheet {
  display: grid;
  grid-template-rows: 17mm 39mm 1fr 14mm;  /* top / hero / content / footer */
}
.content {
  display: grid;
  grid-template-columns: 286mm 1fr;
  overflow: hidden;
}
.content > * { min-height: 0; }
```

## Preventing photo overflow

The embedded sample photo is often 400–500px tall after base64, which can
force the middle grid row taller than the physical 230mm sheet. Key rules:

```css
.photo-panel {
  min-height: 0;
  display: grid;
  grid-template-rows: auto minmax(0, 1fr);
  overflow: hidden;
}
.photo-frame {
  min-height: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}
.photo-frame img {
  max-width: 100%;
  max-height: 100%;
  height: 100%;
  width: auto;
  object-fit: contain;
}
.info-panel {
  min-height: 0;
  display: grid;
  grid-template-rows: auto minmax(0, 1fr) auto;
  overflow: hidden;
}
```

## Design tokens

| Token | Value | Usage |
|-------|-------|-------|
| `--primary` | `#0F172A` | Navy — top strip, hero, footer, text headers |
| `--secondary` | `#0284C7` | Sky — accent bar, pill left rule, QR border left |
| `--bg-light` | `#F8FAFC` | Alt backgrounds, status badge bg |
| `--text-main` | `#1E293B` | Body text |
| `--text-muted` | `#64748B` | Labels, captions, metadata |
| `--border` | `#E2E8F0` | Dividers, frames |
| `--accent` | `#16A34A` | Status-pass green badge |
| `--warm` | `#F4F1EA` | Photo panel background (warmer than --bg-light) |

## Partner logo embedding sizes

Resize logos from `_Style-Guides/logos archives/` to 60px height before base64 encoding:

| Logo | Raw (resized) | Base64 chars | Rendered at 5.5mm |
|------|--------------|-------------|-------------------|
| MOC | ~9KB | ~13KB | 46×21px |
| CG | ~12KB | ~16KB | 66×21px |
| PMC | ~18KB | ~24KB | 84×21px |
| NRS | ~8KB | ~10KB | 29×21px |

Glassbau Hahn remains as inline SVG text (no PNG source available).

## Memory note

The original QR code in the SAM-FIN-PB-001 folder was blank (all white pixels,
527 bytes, 0 black pixels). `qrencode` produced a file with a valid header
and dimensions but zero actual QR data. The PNG was 396×396, 1-bit colormap,
but every pixel was `255`. Always run `verify-qr.py` after generation.
