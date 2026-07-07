# QR Landing Page Print Layout & Approval Block

## File structure

Every sample landing page (`index.html`) at `samaya-factory.com/Samples/{CODE}/` should include:

1. **Screen styles** (navy header, warm background, card sections, rounded corners)
2. **Print styles** (`@media print`) — A4-ready, compact, ink-friendly
3. **Approval block** — signature table for project stakeholders

## Key conventions

| Item | Value |
|------|-------|
| Header subtitle | `"Samaya Investment — Material Submittal · {Project}"` |
| `<title>` suffix | `Samaya Material Submittal` (not `Sample`) |
| Page size (print) | A4, 12mm margins |
| Print layout | Photo 40% / Content 60%, side-by-side, no wraps |
| Approval parties | Prepared: varies (Samaya/Glasbau Hahn/manufacturer) → Reviewed: NRS, CG, PMC → Approved: Client/MoC |

## Print CSS (compact — fits one A4 page with all sections)

```css
@page { size: A4; margin: 12mm 10mm 14mm 10mm; }
@media print {
  body { background:#fff; color:#000; }
  .top { background:#fff; color:#000; padding:6px 0 4px 0; border-bottom:1px solid #999; margin-bottom:4px; }
  .top h1 { font-size:16px; color:#000; margin:0; font-family:Georgia,serif; }
  .top .code { font-size:9px; opacity:1; color:#555; }
  .top .proj-info { font-size:7px; color:#666; margin-top:1px; }
  .top .proj-info .ref { font-family:monospace; }
  .top .proj-info .s { opacity:0.3; }
  .top .tags { margin-top:2px; gap:6px; }
  .top .tags span { background:#eee; color:#333; padding:1px 6px; border-radius:2px; font-size:8px; }
  .top [style*="display:flex"] { margin-bottom:0 !important; }
  .top [style*="display:flex"] span { font-size:6px !important; opacity:1 !important; color:#555 !important; }
  .top [style*="display:flex"] img { height:10px !important; }
  .container { max-width:100%; padding:0; margin:0; }
  .grid { display:flex; gap:6px; flex-wrap:nowrap; }
  .photo { flex:0 0 40%; min-width:0; }
  .photo img { border-radius:0; box-shadow:none; max-height:140mm; object-fit:cover; }
  .details { flex:1; min-width:0; gap:4px; }
  .card { background:transparent; border-radius:0; padding:4px 8px; box-shadow:none; border:1px solid #ddd; }
  .card h2 { font-size:7px; color:#333; margin-bottom:2px; border-bottom-color:#ccc; padding-bottom:1px; letter-spacing:1px; }
  .card p { font-size:8px; color:#000; line-height:1.3; }
  .card ul { grid-template-columns:1fr 1fr; gap:1px 6px; }
  .card ul li { font-size:7px; padding-left:8px; }
  .card ul li::before { top:3px; width:3px; height:3px; border-color:#666; }
  .bottom { background:transparent; border-radius:0; padding:4px 8px; margin-top:3px; box-shadow:none; border:1px solid #ddd; display:flex; align-items:center; gap:6px; }
  .bottom img { width:28px; height:28px; border-color:#ccc; }
  .bottom .ql { font-size:7px; color:#333; letter-spacing:1px; }
  .bottom .qr-url { font-size:7px; color:#666; }
  .downloads { display:block; margin-top:2px; }
  .downloads a { display:inline; background:none; color:#000; font-size:7px; font-weight:normal; text-decoration:underline; border:1px solid #ccc; padding:1px 4px; border-radius:2px; }
  .downloads a.pdf { background:none; }
  .downloads a:hover { background:none; }
  .bottom .downloads a::before { content:"📄 "; font-size:7px; }
  .downloads a + a { margin-left:6px; }
  footer { font-size:7px; color:#888; border-top:1px solid #ddd; padding:3px; margin-top:2px; }
  a { color:#000 !important; text-decoration:underline !important; }
  a[href^="http"]::after { content:" (" attr(href) ")"; font-size:6px; color:#666; }
  .approvals { background:transparent; border-radius:0; padding:3px 8px; margin-top:2px; box-shadow:none; border:1px solid #ddd; }
  .approvals h2 { font-size:7px; letter-spacing:1px; margin-bottom:2px; border-bottom:1px solid #ccc; padding-bottom:1px; text-transform:uppercase; color:#333; }
  .approvals table { width:100%; border-collapse:collapse; font-size:7px; }
  .approvals td { padding:2px 4px; border:1px solid #ccc; vertical-align:top; }
  .approvals .role { font-weight:bold; white-space:nowrap; width:35px; font-size:6px; color:#555; }
  .approvals .entity { font-weight:bold; white-space:nowrap; width:65px; font-size:6px; color:#555; }
  .approvals .sig-line { border-bottom:1px solid #999; display:block; height:9px; margin-top:1px; }
  img[alt="Samaya"] { height:10px !important; }
}
```

## Approval block HTML

Insert between the QR/datasheets `.bottom` div and the `<footer>`:

```html
<div class="approvals">
  <h2>Approval</h2>
  <table>
    <tr>
      <td class="entity">Prepared by</td>
      <td><strong>[Sample provider — e.g. Samaya Tech Office, Glasbau Hahn]</strong><span class="sig-line"></span></td>
      <td class="role">Date</td>
      <td><span class="sig-line"></span></td>
    </tr>
    <tr>
      <td class="entity">Reviewed by</td>
      <td><strong>NRS</strong><span class="sig-line"></span></td>
      <td class="role">Date</td>
      <td><span class="sig-line"></span></td>
    </tr>
    <tr>
      <td class="entity">Reviewed by</td>
      <td><strong>CG</strong><span class="sig-line"></span></td>
      <td class="role">Date</td>
      <td><span class="sig-line"></span></td>
    </tr>
    <tr>
      <td class="entity">Reviewed by</td>
      <td><strong>PMC</strong><span class="sig-line"></span></td>
      <td class="role">Date</td>
      <td><span class="sig-line"></span></td>
    </tr>
    <tr>
      <td class="entity">Approved by</td>
      <td><strong>Client — MoC</strong><span class="sig-line"></span></td>
      <td class="role">Date</td>
      <td><span class="sig-line"></span></td>
    </tr>
  </table>
</div>
```

## Approval CSS (screen)

```css
.approvals { background:#fff; border-radius:6px; padding:16px 20px; margin-top:20px; box-shadow:0 1px 6px rgba(0,0,0,.04); }
.approvals h2 { font-size:11px; text-transform:uppercase; letter-spacing:1.5px; color:var(--bronze,#C8904A); margin-bottom:10px; border-bottom:1px solid #eee; padding-bottom:4px; }
.approvals table { width:100%; border-collapse:collapse; }
.approvals td { padding:8px 12px; border:1px solid #e0e0e0; vertical-align:top; font-size:13px; }
.approvals .entity { font-weight:600; white-space:nowrap; width:100px; }
.approvals .role { font-weight:600; white-space:nowrap; width:80px; color:#6B6B6B; }
.approvals .sig-line { border-bottom:1px solid #ccc; display:block; height:20px; margin-top:4px; }
```

## Header convention

The header subtitle `<span>` must read:

```
Samaya Investment — Material Submittal · Aseer Museum
```

Not `"Material Sample Library"`. This applies to both screen display and print output (the HTML text carries through to print — no `content:` CSS property needed).

## Verification checklist

- [ ] `@media print` CSS present with A4 `@page` rule
- [ ] Header says "Material Submittal" not "Material Sample Library"
- [ ] `<title>` says "Samaya Material Submittal" not "Samaya Material Sample"
- [ ] Approval table present with NRS, CG, PMC, Client-MoC rows; Prepared by varies per sample provider
- [ ] Print layout fits one A4 page (photo 40%, content 60%, side-by-side, compact fonts)
- [ ] URL annotations on links in print (`a[href^="http"]::after`)
- [ ] Footer with submittal reference
- [ ] All original logos/visual design preserved — did NOT overwrite the full page HTML
