# "Update Memory" Protocol — Multi-Store Synchronization

## The Rule
When the user says **"update memory"**, update ALL known knowledge stores — not just one.

## Stores To Update (in order)

### 1. Hermes Agent Memory
Use the `memory(action='add')` tool. Save:
- Session outcomes (what was done, what changed, any issues)
- New project knowledge (scope clarifications, document updates)
- New labor workflow or tooling rules

### 2. Project Memory Files
Find and update the master memory file. For Aseer Museum:
- `Scripts/PROJECT_MEMORY.md` — append a "Session Update" section
- `Scripts/notes/*.md` — update any relevant summary files

### 3. Notion Project Page
Use the `ntn` CLI to insert a new section at the bottom:
```bash
ntn api v1/pages/{page_id}/markdown -X PATCH -d '{"type":"insert_content","insert_content":{"content":"## Session Update - YYYY-MM-DD\n\nKey changes here..."}}'
```
The Notion page for Aseer Museum is: `2e36d275-a6c9-4857-87c7-094084138b6a`

### 4. Other Relevant Stores
- Skills (skill_manage create/patch)
- Registers or log files
- Summary documents in project folders
- BOQ reference files, audit reports

## What NOT To Do
- Do NOT update only Hermes memory and stop
- Do NOT skip the Notion page because it requires API auth
- Do NOT assume "update memory" means just the memory tool

## Checklist
- [ ] Hermes memory updated
- [ ] Project memory file appended
- [ ] Notion page section inserted
- [ ] Other stores (skills, registers) checked
