# Samaya Factory Company Profile — v6 Deploy Workflow

## Build & Deploy Pipeline

1. **Edit source**: `/v6/index.html` + `/v6/css/*.css` + `/assets/img/`
2. **Prepare deploy dir** in `/tmp/` (never OneDrive directly):
   - Copy `index.html`, fix `../assets/` → `assets/`
   - Copy all CSS files
   - Collect every referenced asset via regex `\.\./assets/[^"\')\s]+` and copy to matching path
3. **Deploy**: `surge --project /tmp/samaya-profile-deploy/ --domain samaya-factory-profile.surge.sh`
4. **Cleanup**: `rm -rf /tmp/samaya-profile-deploy/`

## Image Rules

- **No duplicate photos** — each image file used exactly once across the entire profile (184+ refs). Use `re.finditer` + `Counter` from `collections` to verify before deploy.
- **Web-optimize** before deploy: `sips --resampleWidth 1920 --setProperty format jpeg --setProperty formatOptions 85`
- **HQ replacements**: Project photos in `v6/مشاريع سمايا/` are high-quality originals. Copy to `assets/img/projects/` and optimize for web.
- **Replacements for duplicates**: Pull from unused images in `projects/from-work/`, `projects/from-graphite/`, `projects/from-website/`, or `05-machinery-cnc/`. Verify each replacement is single-use after the swap.

## SVG Chart Design (A4 landscape, navy+gold)

- **Inline SVG** with CSS variable fills (`fill: var(--v3-ink)`, `var(--v3-gold-deep)`) so colors cascade from page context.
- Use `viewBox` that fits the column: comparison bars at 180x44, stacked bar at 180x56, timeline at 180x42.
- For stat counters, simple numbers+labels work — don't add gauge bars or chart SVGs unless explicitly requested.
- **Org chart**: Navy-filled nodes with white text for governance/management, gold-filled hub for Factory Manager. viewBox 900x520 minimum. Thicker connection lines (stroke-width 0.7–0.9). 6 workshops in 2 rows of 3, boxes ≥190px wide.

## Design Consultation Pattern

- Delegate SVG/chart/org chart redesign to Claude Code via `delegate_task` with:
  - The exact HTML section and CSS file paths
  - The brand constraints (colors, fonts, A4 landscape)
  - Request exact `patch` commands (old_string/new_string format)
- After Claude applies changes, verify, rebuild, and deploy.
- Hard refresh (Cmd+Shift+R) needed for browser — Surge doesn't aggressively cache but browsers do.

## Preventing Overflow

- SVG `viewBox` must be wide enough for Arabic text (15 Arabic chars at 10px ≈ 165px needed).
- Stat key labels at ≤5.8pt with `text-overflow: ellipsis; white-space: nowrap;`.
- Workshop boxes: 190px wide minimum for labels like `النجارة وأعمال الخشب`.
- Footnote and authority text: natural wrapping (no `white-space: nowrap`) for long Arabic sentences.
