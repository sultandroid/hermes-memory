# QR Code & Back Cover Enhancement

Generated when the user asks to add a QR code or contact info to the deployed site's back cover.

## QR Generation

Use `api.qrserver.com` — free, no API key needed:

```bash
curl -sL -o assets/img/brand/qr-<label>.png \
  "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=<url-encoded-target>&margin=10"
```

Parameters:
- `size=300x300` — good balance for print (28-30mm at ~300dpi)
- `data=<encoded-url>` — URL-encode the target (e.g. `https://samaya-factory-profile.surge.sh`)
- `margin=10` — quiet zone padding around the QR

## Placement in back cover

The back cover is typically the last `<section>` with class `ed-back-cover` (id `p27`). It has:
- A navy background (`var(--navy)`, `#fff` text)
- Inline styles throughout (no CSS class overrides needed)
- A 3-column contact grid: Factory | Phone | Online

### Adding QR code

Insert below the contact grid's closing `</div>`:

```html
<!-- QR code row -->
<div style="display:flex; flex-direction:column; align-items:center; margin-top:5mm; gap:1.5mm;">
  <img loading="lazy" decoding="async"
       src="../assets/img/brand/qr-profile.png"
       alt="QR: your-domain.surge.sh"
       style="width:28mm; height:28mm; border-radius:1mm; background:#fff; padding:2mm;">
  <span style="font-family:'Inter',sans-serif; font-size:6.5pt; letter-spacing:.15em; color:rgba(255,255,255,.6);">your-domain.surge.sh</span>
</div>
```

Styling notes:
- `28mm` size works for A4 print readability
- White background (`#fff` with 2mm padding) ensures QR contrast on navy
- `border-radius:1mm` for subtle rounding on the white card
- URL label is 6.5pt, muted (`rgba(255,255,255,.6)`), Inter font

### Adding personal phone

Insert a third `<span>` in the Phone column's `<div>` (second column of the contact grid):

```html
<span dir="ltr" style="display:block; font-family:'Inter',sans-serif; font-size:9pt;
      color:var(--gold); margin-top:.5mm; letter-spacing:.05em; font-weight:600;">
  +966 XX XXX XXXX
</span>
```

Use `color:var(--gold)` and `font-weight:600` to visually distinguish personal lines from the company numbers (which use `#fff` or `rgba(255,255,255,.7)`).

## HTML structure reference

The back cover (ed-back-cover) structure:
```
<section class="page ed-back-cover" id="p27">
  <div style="...navy background...">
    <!-- watermark SVGs -->
    <!-- centered content flexbox -->
      <!-- TOP: brand mark + edition -->
      <!-- CENTER: gratitude statement (Thank you / شكراً) -->
      <!-- BOTTOM: contact grid (3 columns) -->
        Factory | Phone | Online
      <!-- QR CODE ROW (insert here after </div> of contact grid) -->
    <!-- close centered content -->
  </div>
</section>
```
