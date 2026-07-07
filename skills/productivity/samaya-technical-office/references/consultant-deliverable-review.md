# Consultant Deliverable Review — Gap Analysis

Used when reviewing a consultant/contractor deliverable package against the project submittal register.

## Workflow

1. **Inventory the deliverable folder** — list all files and subfolders recursively
2. **Get the submittal register** — read the relevant register Excel from `Docs/09_Registers/`
3. **Map deliverables to register items** — which register categories are covered? Which items are missing?
4. **Score by category** — % complete per register section
5. **Flag critical gaps** — empty folders, overdue items, missing numbering conventions

## Output Format

```
## Consultant Review: [Package Name]

### 1. Folder Structure — Assessment
Tree view with ✅/⚠️ annotations per folder.

### 2. Issues & Gaps
Table: Issue | Detail | Priority (High/Medium/Low)

### 3. Recommendations
Numbered action items.

### 4. Overall Status
Category table with % progress per section.
```

## Pitfalls

- OneDrive may serve stub files instead of real files — check file size (4 bytes = stub)
- Submittal register Excel may also be a stub — verify before relying on it
- Always cross-reference with SPEC.md and SCOPE_REQUEST.md in the subcontractor's _MANAGER_DASHBOARD
