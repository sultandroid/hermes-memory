# Adding Photos to Project Experience Cards

## Overview

Transform text-only project experience cards (Section 8) into image+text cards with representative photo thumbnails. Used for Samaya Type B exhibition/museum proposals.

## Image Sources (priority order)

1. **Existing project renders** — Aseer Museum 3D views at:
   - `~/Desktop/asm_views_web/` (91 images)
   - `~/Desktop/aseer-backups/dist-20260617_164305/images/gallery-*.jpg` (gallery views)
   - `~/Desktop/aseer-interactive/public/images/` (gallery + gallery 3D views)

2. **AI-generated images** — Use `image_generate` tool with descriptive prompts matching each project's theme (museum interior, exhibition hall, event space, calligraphy gallery, etc.)

3. **Web search** — For projects with public references available royalty-free

## Card Layout Pattern

Convert each card from text-only to image+text:

```html
<div style="border-left:3px solid #0284C7;padding:6px 8px 6px 10px;
            border-radius:4px;background:#f8fafc;
            display:flex;gap:8px;align-items:flex-start;">
  <img src="data:image/jpeg;base64,..."
       style="width:70px;height:50px;object-fit:cover;
              border-radius:3px;flex-shrink:0;">
  <div style="flex:1;display:flex;flex-direction:column;gap:2px;">
    <!-- original card content: name, year badge, description, client -->
  </div>
</div>
```

Key points:
- `flex:1` on the text div needs `min-height:0` if inside a container with overflow
- `flex-shrink:0` on the image prevents it from collapsing on narrow viewports
- `object-fit:cover` ensures consistent 70×50 aspect ratio regardless of source dimensions
- Color borders and card background remain the same as text-only version

## Image Embedding

### Base64 Data URIs (for self-contained HTML)

```bash
# Convert image to base64 data URI
python3 -c "
import base64
with open('image.jpg','rb') as f:
    b = base64.b64encode(f.read()).decode()
    print(f'data:image/jpeg;base64,{b}')
"
```

For PNG: `data:image/png;base64,...`

Storage overhead: ~36KB per 160px-wide thumbnail → ~440KB for 12 cards. Acceptable for self-contained HTML.

### Resizing Before Embedding

```bash
# macOS sips — resize jpg to max 160px wide, Q85
sips --resampleWidth 160 --setProperty format jpeg \
     --setProperty formatOptions 85 input.jpg --out thumb.jpg
```

## Approach for Missing Project Images

When project has no existing photos:

1. Generate via `image_generate` with prompt describing the project type:
   - Museum interior: *"museum exhibition hall with display cases, warm lighting, cultural artifacts"*
   - Exhibition: *"modern exhibition space with interactive displays and ambient lighting"*
   - Arabic calligraphy: *"Arabic calligraphy art exhibition with framed works on walls"*
   - Event/entertainment: *"night entertainment venue with lights and crowds, festive atmosphere"*

2. Download the generated image (check result for `image` field — URL or local path)

3. Resize and convert to base64

4. Embed in the card

## File Size Impact

| Cards | Without images | With base64 thumbnails |
|-------|---------------|------------------------|
| 12    | ~15KB         | ~440KB                 |

This is acceptable — still well under Surge free tier limits and loads fine in browser.

## Example: Aseer Museum Card (using real render)

```html
<div style="border-left:3px solid #0284C7;padding:6px 8px 6px 10px;
            border-radius:4px;background:#f8fafc;
            display:flex;gap:8px;align-items:flex-start;">
  <img src="data:image/jpeg;base64,/9j/4AAQ...base64data..."
       style="width:70px;height:50px;object-fit:cover;
              border-radius:3px;flex-shrink:0;">
  <div style="flex:1;display:flex;flex-direction:column;gap:2px;">
    <div style="display:flex;justify-content:space-between;align-items:center;">
      <span style="font-family:'Cairo',sans-serif;font-size:11px;
                   font-weight:700;color:#0F172A;line-height:1.3;">
        متحف عسير الإقليمي
      </span>
      <span style="font-family:'Inter',sans-serif;font-size:9px;font-weight:600;
                   color:#0284C7;background:#e0f2fe;padding:1px 6px;
                   border-radius:3px;white-space:nowrap;">2025–</span>
    </div>
    <span style="font-family:'Cairo',sans-serif;font-size:9px;
                 color:#475569;line-height:1.4;">
      تصميم وتنفيذ متحف إقليمي — 7 صالات عرض، تقنيات تفاعلية، سينوغرافيا
    </span>
    <span style="font-family:'Cairo',sans-serif;font-size:9px;color:#64748b;">
      <span style="color:#94a3b8;">العميل:</span> Ministry of Culture / RCRC
    </span>
  </div>
</div>
```

## Pitfalls

- Do NOT use `<img>` with external URLs in print-ready HTML — they break without internet
- Do NOT use raw file paths (`file:///`) — they won't render in browser-based delivery or print preview
- Do NOT add images taller than ~60px or card grid alignment breaks
- Grid container has `gap:6px` — images + text must fit within the grid column without overflow
- After adding images, verify the section still fits within one A4 page (1123px height)
- For projects with photos on OneDrive, do NOT reference OneDrive paths — copy to /tmp first, resize, then base64-embed
