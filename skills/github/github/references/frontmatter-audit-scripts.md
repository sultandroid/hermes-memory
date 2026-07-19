# Frontmatter Audit & Fix Scripts

Reusable Python scripts for auditing and fixing YAML frontmatter compliance across markdown-heavy repos.

## audit_frontmatter.py

Scans all `.md` files in target directories and reports:
- Total files scanned
- Clean files (all required fields present, valid status)
- Critical issues (no frontmatter at all)
- Medium issues (missing fields, invalid status values)

**Usage:**
```bash
python3 audit_frontmatter.py
```

**Configuration:**
- `TARGET_DIRS` — list of directories to scan recursively
- `REQUIRED_FIELDS` — YAML frontmatter fields to check (default: last_updated, owner_agent, status, source)
- `VALID_STATUSES` — set of allowed status values (default: active, draft, superseded, closed, archived)

## fix_frontmatter.py

Auto-fixes missing frontmatter by prepending a default YAML block to any `.md` file that lacks it.

**Usage:**
```bash
python3 fix_frontmatter.py
```

**Default frontmatter added:**
```yaml
---
last_updated: YYYY-MM-DD
owner_agent: Hermes
status: active
source: <relative file path>
---
```

**Pitfalls:**
- The fix script adds `last_updated: YYYY-MM-DD` as a placeholder — update the actual date after running
- Only fixes files with NO frontmatter at all (doesn't touch files that already have `---`)
- Does NOT fix partial frontmatter (missing fields, invalid status) — that requires manual or targeted patching
- Run `audit_frontmatter.py` first to see what needs fixing, then run `fix_frontmatter.py` for the critical cases
