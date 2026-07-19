---
name: repo-documentation-indexing
description: Create and maintain repository-level navigation, manifest, and cleanup-tracking documentation — FILE_MANIFEST.md, QUICK_LINKS.md, DEPRECATION_LOG.md, ASCII tree diagrams in README.md, and related index files. Covers full filesystem scan, YAML frontmatter extraction, duplicate detection, artifact identification, and structured markdown generation.
version: 1.0.0
author: Hermes Agent
platforms: [macos, linux]
tags: [repo-documentation, navigation, manifest, deprecation, file-indexing, cleanup-tracking]
related_skills: [bulk-file-organization, project-initializer]
---

# Repository Documentation & Indexing

Create comprehensive navigation, manifest, and cleanup-tracking files for any project repository. This skill covers the full workflow from filesystem scan to structured markdown generation.

## When to Use

- User asks for a "file manifest", "file listing", "complete index", or "inventory" of the repo
- User asks to "update README with tree diagram" or "add structure overview"
- User asks for a "quick links" or "quick reference" document
- User asks for a "deprecation log", "cleanup tracking", or "files to remove" document
- User asks to "audit the repo structure" or "document what's here"
- Routine repo maintenance: keeping navigation docs in sync with actual files

## Workflow

### Phase 1: Full Filesystem Scan

```bash
# Count total files
find . -not -path './.git/*' -not -path './.git' -type f | sort | wc -l

# List all files
find . -not -path './.git/*' -not -path './.git' -type f | sort

# List all directories
find . -not -path './.git/*' -not -path './.git' -type d | sort

# Get file sizes
find . -not -path './.git/*' -not -path './.git' -type f -exec stat -f "%z%t%N" {} \;
```

**Exclude:** `.git/` directory always. Also exclude `.DS_Store`, and any other hidden files the user doesn't want tracked.

### Phase 2: Extract YAML Frontmatter

For every markdown file, extract `owner_agent`, `last_updated`, and `status` from YAML frontmatter:

```python
import os, re, yaml

def extract_frontmatter(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(2000)
    except:
        return None, None
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            fm_text = content[3:end].strip()
            try:
                fm = yaml.safe_load(fm_text)
                if isinstance(fm, dict):
                    owner = fm.get('owner_agent', fm.get('owner', 'N/A'))
                    updated = fm.get('last_updated', fm.get('date', 'unknown'))
                    status = fm.get('status', 'active')
                    return str(owner) if owner else 'N/A', str(updated) if updated else 'unknown'
            except:
                pass
    return 'N/A', 'unknown'
```

Build a combined data file with columns: `folder|filename|owner|last_updated|size_bytes`.

### Phase 3: Detect Issues for Deprecation Log

Scan for these categories:

| Category | Detection | Example |
|----------|-----------|---------|
| **Duplicate files** | Same basename in both `03_Plans/` and `99_Archive/` | DMP files, Stakeholder Plan files, HSE analyses |
| **Empty stubs** | File size = 0 bytes | `.dc_purpose` files, empty `.md` files |
| **Artifacts** | Extension-based (`.bak`, `.pyc`, `.lnk`, `.log`, `.loop`) | HTML backup, compiled bytecode, Windows shortcuts |
| **Marker files** | `.dc_purpose` or similar dotfiles with unclear purpose | 50-71 byte files with no documented function |
| **Legacy content** | Files in `99_Archive/` that may be superseded by live equivalents | Old revision analyses, superseded reports |

**Duplicate detection script:**

```python
# Find basename overlaps between two directory trees
plans_basenames = {}
archive_basenames = {}

for dirpath, dirnames, filenames in os.walk('03_Plans'):
    for fn in filenames:
        plans_basenames.setdefault(fn, []).append(os.path.relpath(...))

for dirpath, dirnames, filenames in os.walk('99_Archive'):
    for fn in filenames:
        archive_basenames.setdefault(fn, []).append(os.path.relpath(...))

for fn in sorted(set(plans_basenames.keys()) & set(archive_basenames.keys())):
    if fn.endswith(('.md', '.html', '.docx')):
        print(f'DUPLICATE: {fn}')
```

### Phase 4: Create FILE_MANIFEST.md

A complete file listing with metadata columns:

```markdown
| Folder | File | Owner Agent | Status | Last Updated | Size (bytes) |
|--------|------|-------------|--------|-------------|-------------|
| `folder/` | `filename.md` | Hermes | active | 2026-07-19 | 1234 |
```

**Rules:**
- Sort alphabetically by folder, then filename
- Include ALL files except `.git/` contents
- Use `N/A` for files without frontmatter
- Add a header with total file count
- Include YAML frontmatter on the file itself

### Phase 5: Create ASCII Tree Diagram for README.md

Build a 3-level deep tree showing the repo structure:

```
aseer-museum-pm/
├── 📄 Root files
│   ├── CONSTITUTION.md          — Governing rules
│   ├── AGENTS.md                — Agent sync rules
│   └── ...
├── 00_Command_Center/           — Control entry point
├── 00_Contracts/                — READ-ONLY
├── 01_Registers/                — 31 technical registers
│   ├── submittal_register.md
│   ├── rfi_register.md
│   └── ...
├── 03_Plans/                    — 15 management plans
│   ├── 01_DMP/                  — Design Management Plan
│   ├── 02_Stakeholder/          — Stakeholder Management Plan
│   └── ...
└── scripts/                     — Automation & CI/CD
```

**Rules:**
- Use Unicode box-drawing characters (`├──`, `└──`, `│`)
- Max 3 levels deep (root → folder → subfolder contents)
- Annotate each folder with a brief purpose description
- Group related folders under section headers
- Add a tip at the bottom pointing to QUICK_LINKS.md and FILE_MANIFEST.md

### Phase 6: Create QUICK_LINKS.md

A keyword-grouped navigation index organized by topic, not by folder:

```markdown
## Governance
| File | Purpose |
|------|---------|
| `CONSTITUTION.md` | Governing rules |

## Registers (31 registers)
| Register | File |
|----------|------|
| Submittal Register | `01_Registers/submittal_register.md` |
```

**Grouping categories (typical):**
- Governance (CONSTITUTION, AGENTS, CHANGELOG, VERSION, FILE_MANIFEST, QUICK_LINKS, DEPRECATION_LOG)
- Project Status (dashboard, action items, decisions, meeting minutes)
- Contracts & Charter (READ-ONLY)
- Registers (all 20-40 registers)
- Schedule
- Management Plans (by plan name)
- Technical Office (by area)
- Communications
- Risk System
- Document Index
- Manager Lanes (by lane)
- Agent Workspace
- Scripts & CI/CD
- Style Guides
- Odoo Mapping
- Archive (by section)
- Skills
- Weekly Dashboard

### Phase 7: Create DEPRECATION_LOG.md

A cleanup-tracking document with status categories:

```markdown
| Date Marked | File/Folder | Reason | Scheduled Removal | Status |
|-------------|-------------|--------|-------------------|--------|
| 2026-07-19 | `99_Archive/01_Integration_Management/` | Duplicate — copies of live files in `03_Plans/01_DMP/` | TBD | 🔴 Duplicate |
```

**Status legend:**
| Status | Meaning |
|--------|---------|
| 🔴 Duplicate | Exact copy of live file |
| 🟡 Stub | Empty or near-empty file |
| 🟡 Artifact | Build/backup/cache file |
| 🟡 Unclear | Purpose unknown |
| 🟡 Review | Legacy content needing human review |
| ✅ Resolved | Cleanup completed |

**Include a Cleanup Recommendations section** at the bottom with actionable grouped advice.

### Phase 8: Update README.md

Insert the ASCII tree diagram after the Quick Navigation table and before the Project facts section. Use `patch()` tool for targeted insertion:

```python
# Find the insertion point and replace
patch(
    path="README.md",
    old_string="| `01_Registers/` | RFIs, NCRs, SIs, submittals, risks, assessments |\n\n## Project",
    new_string="| `01_Registers/` | RFIs, NCRs, SIs, submittals, risks, assessments |\n\n## Repo Structure\n\n```\n...tree...\n```\n\n## Project"
)
```

### Phase 9: Git Commit

```bash
git add FILE_MANIFEST.md QUICK_LINKS.md DEPRECATION_LOG.md README.md
git commit -m "ORDER N: Create Master File Manifest & Navigation — 4 index files"
```

## Pitfalls

1. **Double-pipe in table rows.** When patching a table row, the patch tool may introduce `||` (double pipe) if the old_string doesn't match exactly. Always verify the patched line in the output.
2. **Large FILE_MANIFEST.md files.** A 476-file repo produces a ~46KB manifest. This is fine for markdown but may be slow to render in some editors. Consider splitting by folder if the repo exceeds 1000 files.
3. **Frontmatter extraction failures.** Some files have malformed YAML (missing closing `---`, non-dict content). Handle gracefully with try/except and mark as `N/A`.
4. **OneDrive cloud stubs.** Files that appear as 0 bytes in `ls -la` but are actually cloud-only placeholders. Don't flag these as empty stubs — they have content in the cloud.
5. **Hidden files.** Files starting with `.` (`.dc_purpose`, `.gitignore`, `.sync_state.json`) should be included in the manifest but flagged appropriately in the deprecation log.
6. **Binary files.** PNG, XLSX, DOCX, EML, PCP, PAT, LNK files should be included in the manifest but noted as binary. The CONSTITUTION may prohibit binaries in the repo — flag these.
7. **README.md already has a Quick Links section.** Don't duplicate it. The new QUICK_LINKS.md should be more comprehensive and keyword-grouped, while the README's existing table stays as a quick-start.
8. **Don't regenerate README.md from scratch.** Use targeted patches to insert the tree diagram. Preserve all existing content, formatting, and emoji.
9. **File count changes between scan and commit.** If the repo is actively being modified, the manifest may be slightly stale by commit time. Note the scan date in the frontmatter.
10. **Duplicate detection is basename-based, not content-hash-based.** Two files with the same name but different content will be flagged as duplicates. Verify content before recommending deletion.

## Reference Files

- `references/aseer-museum-pm-indexing-session.md` — Worked example: 476 files, 80+ directories, 33 deprecation items identified (3 duplicate folders, 4 empty stubs, 5 artifacts, 4 marker files, ~17 legacy items), 4 index files created and committed.
- `references/governance-versioning-pattern.md` — CHANGELOG.md, VERSION.md, and CONSTITUTION amendment log patterns.
- `references/plan-folder-template-pattern.md` — 4-file template pattern (README.md, plan_summary.md, checklist.md, approval_log.md) for populating project management plan subdirectories. Covers template structure, plan-specific data per folder, Python generation strategy with f-string pitfalls, and verification checklist.