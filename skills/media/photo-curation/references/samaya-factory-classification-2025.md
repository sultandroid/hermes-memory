# Samaya Factory Photo Classification (June 2025)

Real-world application of the photo-curation skill on 4,570 WhatsApp photos from Samaya metal fabrication factory.

## Source

```
/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Orders/2025/
  00000 صور واتساب سنة 2025 الورشة/
```

## Data Profile

| Metric | Value |
|--------|-------|
| Total images | 4,570 |
| Time span | Dec 2024 — Dec 2025 |
| Source | WhatsApp shared photos (Samsung Galaxy S24 Ultra) |
| Folders | 14 monthly folders (Arabic names: يناير, فبراير, مارس...) |
| Renaming | Files pre-renamed with prefix: `Finished-Project-`, `Workshop-`, `Material-Sample-`, `Document-` |
| Camera | Samsung Galaxy S24 Ultra (SM-S928B) — 3648×2052, 4000×1848, up to 6.7MB |

## File Size Distribution

| Tier | Threshold | Count |
|------|-----------|-------|
| HIGH (>2MB) | >2,000,000 bytes | 570 |
| GOOD (1-2MB) | 1,000,000-2,000,000 | 493 |
| FAIR (500KB-1MB) | 500,000-1,000,000 | 128 |
| LOW (200-500KB) | 200,000-500,000 | 542 |
| POOR (<200KB) | <200,000 bytes | 2,837 |

## Pipeline Results

| Phase | Tool | Result |
|-------|------|--------|
| Manifest | Python | 4,570 photos indexed with category + size |
| Rule tiering | Python | HIGH: 1,063, MEDIUM: 670, LOW: 2,799, SKIP: 38 |
| sips resolution analysis | macOS sips | Medium Finished-Products: all >2000px — promoted |
| Q1 review | Claude Code | 624 promoted from original folders |
| Q2 review | Kimi | 98/99 promoted from review folder |
| Q3-Q4 review | Codex | 415/421 promoted from review folder |
| Audit | Codex | Found 148 duplicates, coverage gap, 7 unique stragglers |
| Final cleanup | Python | Deduped 148, added 94 more Finished-Products |

## Final Output

```
classified/website-ready/         2,688 photos (3.2 GB)
├── 01-Finished-Products          1,158  (2.3 GB)
├── 02-Workshop-Environment         816  (175 MB)
├── 03-Onsite-Installations           1  (80 KB) — UNDER-represented
├── 04-Material-Samples             474  (56 MB)
├── 05-Opening-Ceremony              72  (100 MB)
└── 06-Best-High-Res                167  (580 MB)

classified/review/
└── needs-vision-check                7  files

Total processed: 2,695 / 4,570 (59%)
```

## Key Learnings

### WhatsApp Compression Quirk
WhatsApp compresses images heavily. A 600KB WhatsApp photo can still be 1200×1600 resolution. **Always check sips pixel dimensions, not just file size**, when classifying WhatsApp-sourced photos.

### Multi-Agent Issue: mv vs cp
Agent 1 (Claude Code) used `mv` to move photos from original folders to classified. Agents 2-3 correctly used `cp` from the review folder. Be explicit about copy-vs-move in sub-agent instructions.

### Deduplication Pattern
Files >3MB were copied to both `01-Finished-Products` AND `06-Best-High-Res`. This intentional subset duplication is fine. The audit flagged 141 as "expected duplicates" for this reason.

### Onsite Installation Gap
Only 1 installation photo was found. WhatsApp gallery focused on workshop and finished products. If the website needs installation shots, they must be sourced separately.

## Remaining Work

1. Classify remaining ~1,800 unprocessed photos in monthly folders
2. Source more onsite installation photos
3. Human review of 7 borderline photos in `needs-vision-check/`
4. Fix 4 files with spacing in filenames
