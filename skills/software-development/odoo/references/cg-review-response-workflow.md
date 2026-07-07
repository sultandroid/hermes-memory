# CG Review Response Workflow

Used when CG (or PMC) sends review comments on a drawing submission, plan, or deliverable. End-to-end pattern: receive → review → draft response → cross-reference → Odoo task → log time.

## Trigger

User says "CG sent comments on [document]", "we need to respond to CG comments", or shares a CG review email/PDF.

## Workflow

### Step 1 — Receive & Understand

1. User shares the CG review email (usually from "Jim" or PMC team)
2. Read each comment item carefully — identify what CG is actually asking
3. Group comments by type:
   - **Format/template issues** (title block, numbering, stamps)
   - **Content gaps** (missing drawings, incomplete sections)
   - **Quality/consistency** (hatch patterns, legends, dimensions)
   - **Compliance** (ISO coding, DMP, BEP)
   - **Cultural/presentation** (figures, entourage)

### Step 2 — Draft Response Letter

Write a professional email response addressing each CG comment:

```
Dear [Name],

Thank you for your review. Please find our response below:

1. [CG comment topic]
   Action: [what we'll do — e.g., "We will update all title blocks
   in the next submission to match the approved template."]

2. ...

Please let us know if you need any clarification.
Best regards,
Mohamed Sultan
Technical Office Manager
Samaya Factory - Aseer Museum
```

**Rules for response tone (learned from user corrections):**
- Professional but not defensive — CG is providing feedback, we acknowledge and act
- Reference back to drawing packages and actual file names (e.g. "Z-13-02-A-Z0-GF-CE-RCP-AYU1-SA1-0210_M3_Rev03")
- When CG asks for something already done, point to the existing work rather than promising a new pass
- Use specific action verbs: "We will update...", "We have already issued...", "We will coordinate..."

### Step 3 — Cross-Reference Against Actual Drawings

Before sending the response, verify claims:

1. **Check the drawing package** in the project folder:
   ```
   OneDrive.../.../04_Drawings/
   ```
   Look at actual PDFs — are title blocks complete? Are ISO codes used? Are the drawings stamped?

2. **Check what was actually submitted** — email records / transmittal logs
3. **If the drawing exists with the correct info**, cite the exact file path and sheet number in the response
4. **If it's missing**, acknowledge and commit to a delivery date

**Pattern:** User will say "before sending, check the drawing folder first, then I'll decide." Do this before deleting/committing to anything.

### Step 4 — Edit & Refine with User

1. Present the draft to the user as walk-through (item by item)
2. User will edit — soften language, correct technical references, add context
3. Key edits from past sessions:
   - Remove accusatory tone toward CG (they're doing their job)
   - Don't say "please stop doing X" — rephrase as "please ensure Y going forward"
   - Add clarity about what was actually submitted vs what CG thinks was submitted
   - Correct internal role references (e.g., "Technical Office Manager" not "Project Manager")
   - Sign with the user's full title

### Step 5 — Submit & Capture in Odoo

1. User sends the final response email
2. Create an Odoo task for the CG review cycle:

```python
tid = models.execute_kw(db, uid, pw, 'project.task', 'create', [{
    'name': 'CG-N — Respond to DD drawing review comments [topic]',
    'project_id': 219,
    'stage_id': 36,                      # DD Stage
    'parent_id': <package_task_id>,       # Under the relevant package
    'user_ids': [(4, 151)],               # Assign to Sultan
    'tag_ids': [(4, 141)],               # Plans & Procedures tag
    'date_assign': '<today>',
    'date_deadline': '<3-5 days out>',
    'state': '1_done',                   # Already responded
    'description': (
        '<h3>CG Review: DD Drawings</h3>'
        '<p><b>Items covered:</b></p>'
        '<ul>'
        '<li>Title block compliance</li>'
        '<li>Drawing numbering ISO coding</li>'
        '<li>...</li>'
        '</ul>'
        '<p><b>Response sent:</b> <today></p>'
    ),
}])
```

### Step 6 — Log Timesheet (MANDATORY)

```python
ts = models.execute_kw(db, uid, pw, 'account.analytic.line', 'create', [{
    'task_id': tid,
    'project_id': 219,
    'unit_amount': 1.5,           # hours spent
    'name': 'CG review response — DD drawing comments, cross-reference, email drafting',
    'date': '<today>',
}])
```

**The user explicitly requires timesheet logging on every task. Do not skip.**

## Checklist

- [ ] Read all CG comments carefully
- [ ] Draft response letter addressing each item
- [ ] Cross-reference against actual drawing files before sending
- [ ] User reviews and edits the draft
- [ ] Final response sent by user
- [ ] Odoo task created (or existing one updated)
- [ ] Timesheet logged
