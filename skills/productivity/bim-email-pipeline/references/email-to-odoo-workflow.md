# Email-to-Odoo Task Cross-Reference Workflow

After processing project emails and extracting attachments, create/update Odoo tasks to track document submissions, statuses, and deadlines.

## Workflow Steps

1. **Extract attachments** via AppleScript → `/tmp/outlook_extracts/`
2. **Read PDF content** via `pdftotext` to identify document codes and CG status
3. **Determine CG status codes:**
   - `A` = Approved (03_approved)
   - `B` = Approved with Comments (03_approved)
   - `C` = Revise & Resubmit (02_changes_requested)
   - `D` = Rejected or Resubmission Required
4. **Determine project folder** from document code prefix
5. **Copy attachment** to the correct subfolder
6. **Create/update Odoo task** under the correct package with dates and status

## Odoo Task Mapping from Email Findings

```python
# After reading email body and attachments

known_statuses = {
    'PL-0057': ('02_changes_requested', 0.5, 
        'C — Revise & Resubmit. CG: pricing basis missing.'),
    'ZD-0058': ('02_changes_requested', 0.5,
        'C — Revise & Resubmit. Sustainability Pkg A.'),
    'PL-0040': ('03_approved', 1.0,
        'B — Approved with Comments. Site Security Plan.'),
    'MS-0015': ('03_approved', 1.0,
        'B — Approved with Comments. Escalators Removal.'),
}

for kw, (state, prog, desc) in known_statuses.items():
    tasks = models.execute_kw(db, uid, pw, 'project.task', 'search',
        [[['project_id', '=', 219], ['name', '=ilike', f'%{kw}%']]])
    for tid in tasks:
        models.execute_kw(db, uid, pw, 'project.task', 'write', [[tid], {
            'state': state,
            'progress': prog,
            'description': f'<p>{desc}</p><p>Source: email batch.</p>',
        }])
```

## Connecting Email IDs to Odoo Actions

For each email processed, record in the backlog log:

```markdown
| Doc | Sender | Status (Email) | Odoo State | Date |
|-----|--------|----------------|------------|------|
| PL-0057 | H. Mabrouk | C - Revise & Resubmit | 02_changes_requested | 2026-06-11 |
| ZD-0056 | M. Elbaz | B - Approved w/ Comments | 03_approved | 2026-06-11 |
```

## Recalculating Package Progress

After updating subtask states/progress:

```python
kids = models.execute_kw(db, uid, pw, 'project.task', 'search_read',
    [[['parent_id', '=', pkg_id]]], {'fields': ['progress']})
total = sum(k.get('progress') or 0 for k in kids)
avg = total / len(kids) if kids else 0
models.execute_kw(db, uid, pw, 'project.task', 'write', [[pkg_id], {'progress': avg}])
```

See the `odoo` skill (`references/odoo-task-hierarchy.md`) for full task hierarchy, date assignment, and progress recalculation patterns.
