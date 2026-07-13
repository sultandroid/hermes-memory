# Aseer Museum Photo Replacement (Jun/Jul 2026) — Batch Workflow

## Context
Replaced all 16 basement gallery photos with updated DD submission renders (VIS001-VIS016) while preserving hotspot positions. Added 4 new LGF galleries with placeholder entries.

## Mapping Table Format
User prefers a table with blank fill-in column for photo-to-view mapping:

| # | Gallery | Current File | New VIS File |
|---|---|---|---|
| 1 | G4 – Saudi Art | g4_G4_View_1.jpg | VIS001 |

Send the table, user fills the last column and sends back.

## Batch Upload via SSH Pipe
1. Collect all mappings
2. Upload each file overwriting the same server path
3. Update subRef + desc in Gallery.tsx
4. Bump IMG_VERSION constant for cache-busting
5. Build (node node_modules/vite/bin/vite.js build)
6. Deploy tarball (index.html + assets/ + sync.php)

## Completed Mapping (Jun 26)
G4_View_1 → VIS001, G4_View_2 → VIS002, G6_View_3 → VIS003, G6_View_3B → VIS004, G6_View_4 → VIS005, G8_View_5 → VIS006, G8_View_6 → VIS007, G9_View_7 → VIS008, G11_View_8 → VIS009, G11_View_8B → VIS010, G12_View_9 → VIS011, G12_View_10 → VIS012, G12_View_10B → VIS013, LB3_View_11 → VIS014, LB3_View_12 → VIS016, G5_View_11B → VIS015

## New LGF Galleries (no hotspots yet)
G1 – Welcome Gallery (lgf_vis017.jpg), G3 – Al Muftaha (lgf_vis018.jpg), LB2 – Lobby (lgf_vis019.jpg), TG – Temporary Gallery (lgf_vis020.jpg)

## Jul 13 — Full Gallery Expansion

Added 12 new galleries across all 3 floors with NRS VIS images. Tagged v1.0.

### Ground Floor (GF) Image Mapping Correction

The original mapping had VIS022 assigned to EC (Children's Education Centre). The user corrected: **VIS022 is LB1 (Al Bahar Main Entrance) Lobby**.

| VIS Image | Gallery | Notes |
|-----------|---------|-------|
| gf_VIS21.jpg | LB1 – Al Bahar Main Entrance (View 1) | |
| gf_VIS22.jpg | LB1 – Al Bahar Main Entrance (View 2) | Was incorrectly EC |
| gf_VIS23.jpg | RT – Retail & Gift Shop | |
| gf_VIS24.jpg | VI – VIP Reception | |
| gf_VIS25.jpg | EC – Children's Education Centre | Was incorrectly LB1 |

### Key Lesson
When the user says a specific VIS number belongs to a different gallery, trust them — they have the floor plan open and can read the labels. The PDF text extraction is unreliable for VIS-to-gallery mapping on A0 drawings.

### Deploy Pattern (Jul 13)
- Images uploaded separately via scp, then permissions fixed to 644
- Only `index.html` + `assets/` deployed (not full dist/ tarball)
- Git tagged v1.0 after final corrections
