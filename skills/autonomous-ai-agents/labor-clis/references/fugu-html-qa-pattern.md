# Fugu HTML QA Pattern

Fugu (Sakana AI via `codex-fugu`) can autonomously write and run Python checker scripts for HTML/SVG/base64 validation. This pattern was proven in the RCRC Exhibition proposal QA session.

## Invocation

```bash
# From a git repo (sandbox access required):
cd /tmp/work && git init && echo "# qa" > README.md && git add . && git commit -m "init"
codex-fugu exec --sandbox workspace-write "
Analyze this HTML file for structural issues:
- Count SVG root elements
- Check all base64 images for valid headers
- Verify HTML tag balance
- List all image elements with their types (SVG inline, SVG <use>, <img>, base64)
Output as structured JSON. File: /tmp/work/proposal.html
"
```

## What Fugu Can Check

- **SVG element count** — tracks how many inline SVGs exist
- **`<img>` tag count** — distinguishes img from SVG
- **Base64 images** — detects `data:image/...;base64,` patterns, validates the base64 content
- **Image signature checking** — verifies PNG headers (first 8 bytes of decoded base64)
- **HTML structure** — reports any tag balancing issues

## Known Limitations

- **Rate limits**: Fugu (Sakana AI free tier) hits `ERROR: You've hit your usage limit. Try again at 8:13 AM.` after enough usage. The reset time is daily per first-usage timestamp. Use short, single-shot prompts to conserve quota.
- **OneDrive access**: Must stage files to `/tmp` via osascript Finder copy first (see labor-clis SKILL.md).
- **File size**: Large files (>200KB) may cause timeout on the read+analyze cycle.
