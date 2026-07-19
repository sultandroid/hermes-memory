# OneDrive Folder Audit Workflow

Systematic pattern for auditing project document folders in OneDrive and deciding what to add to the repo.

## When to use

The user says "check all one by one and decide if useful" or "read all and understand for repo" — pointing you at a OneDrive folder tree with 10-20 subfolders.

## The workflow

### Step 1: List all folders

```bash
ls -1 "/path/to/OneDrive/Master Folder/"
```

### Step 2: For each folder, read a sample

```bash
# List contents
ls "/path/to/folder/" | head -10

# Read a sample PDF
pdftotext -layout "/path/to/sample.pdf" - 2>/dev/null | head -20
```

### Step 3: Assess value against these criteria

| Keep if... | Skip if... |
|------------|------------|
| Adds new information not in any existing register | Duplicates already-tracked data (submittal register, drawing register) |
| Directly relevant to project risks, claims, or decisions | Purely operational site records (daily IRs, SNAs, inspection requests) |
| Cross-references to PRR/DRR risks | HSE task-level records already covered by PRR-HSE-01 |
| Formal correspondence (letters, warnings, instructions) | Single-instance records with no project-wide significance |

### Step 4: Create register only if useful

If the folder adds value, create a markdown register at `01_Registers/<name>_register.md` with:
- YAML frontmatter (last_updated, owner_agent: Technical Office, status, source)
- Table with columns appropriate to the document type
- Cross-references to PRR/DRR risks
- Notes on missing or misfiled documents

### Step 5: Report what was kept and what was skipped

Give the user a clear table showing each folder, what was in it, and whether it was added or skipped with the reason.

## Pitfalls

- **Never skip a folder without reading at least one document.** Folder names are misleading. "16- Safety Notices" sounds low-value but contained a formal stop-work notice linked to SI-009/SI-011. Always read a sample PDF before deciding.
- **Never batch-read OneDrive files.** OneDrive syncs hangs when multiple files are accessed simultaneously. Read one PDF at a time with individual `pdftotext` calls.
- **Never use background subagents for OneDrive paths.** The user explicitly said "one by one" — respect that literally.
- **Never assume a folder is empty because `ls` shows nothing.** Some folders have subdirectories with content. Check recursively.
- **Document what you found even if you skip it.** The user needs to know you checked and why you decided not to add it.
- **Read the actual PDF content, not just the filename.** A folder called "02- CLOSED" may contain the wrong file (NRS Portfolio instead of the SI). Only reading the PDF reveals this.
- **Check for reply/response PDFs in the same folder.** Many SIs have response documents that contain the closure evidence. Read those too.
- **OneDrive reverts direct writes.** If you create or modify a file inside the OneDrive sync folder, OneDrive may silently revert it. Always write to `/tmp` first, then copy to OneDrive. Verify by re-reading the OneDrive path after writing.
- **OneDrive "Resource deadlock avoided" errors.** If you get this error, quit OneDrive, wait 30s, retry. Or write to `/tmp` and copy. Never retry the same OneDrive path repeatedly — it makes the lock worse.
