# MD Cache Utility

## Purpose
Avoid re-scanning files by storing extracted metadata as sidecar `.pdf.md` files alongside originals.

## Tool
`~/.hermes/scripts/md_cache.py` — uses `python-frontmatter` (pip: `python-frontmatter`).

## Commands
```bash
# Write cache for a file
python3 ~/.hermes/scripts/md_cache.py write /path/to/file.pdf \
  --type Submittal \
  --code "ASR-SAM-KP-001" \
  --subject "Key Personnel CV" \
  --parties '["Samaya","CG","MoC"]' \
  --status Submitted

# Read existing cache
python3 ~/.hermes/scripts/md_cache.py read /path/to/file.pdf

# Check if cache is valid (by checksum)
python3 ~/.hermes/scripts/md_cache.py check /path/to/file.pdf

# Find all caches under a directory
python3 ~/.hermes/scripts/md_cache.py find /path/to/project
```

## Cache Format (YAML frontmatter)
```yaml
---
file: original_filename.pdf
type: Submittal
date: 2026-05-28
project: Aseer Museum
code: ASR-SAM-KP-CV-PACK-SITE-001
subject: "description"
parties: [Samaya, CG, MoC]
revision: Rev 01
status: Submitted
checksum: md5_first64kb
---
Summary paragraph here...
```

## Backward Compatibility
Existing .pdf.md files (72 in Aseer Museum) use **narrative format** (no `---` frontmatter). Detect by checking if first line starts with `---`.
