# Meeting Follow-Up Emails to Subcontractors — Workflow

## When to use

User says "draft email to [subcontractor] after yesterday's meeting" or similar — formal correspondence documenting agreed scope changes, action items, and deadlines after a project meeting.

## Pre-requisite: Look up contact info

**Before drafting**, check the Outlook email archive for the recipient's correct email address:

1. Archive: `~/Documents/04_Outlook_Connection/mails/` (numbered 01.md through 24.md)
2. Search: `grep -n -i "company name\|person name" 0*.md 1*.md 2*.md 2>/dev/null` across those files
3. Extract: `From:` header shows name + email, `To:` header shows the address originally contacted
4. Domain typically reveals the company email format

Common found formats per project:
- AD Engineering: `osama@adeng.com.sa` (Osama Abdel Shafi Moustafa), `Info@adeng.com.sa`, `supervision@adeng.com.sa`
- CG: `hmabrouk@cg.com.sa` (Hossam Mabrouk), `melbaz@cg.com.sa` (Mohammad Elbaz)
- NRS: `joshua@nissenrichards.com` (Joshua Broomer)

## Email structure

```
To: [primary contact email]
CC: [other stakeholders if needed]

Subject: [Meeting Follow-Up] — [Topic] — Aseer Regional Museum Project
Reference: Meeting held [date] at [time]

Dear [Name / Team],

Following our meeting on [date], please find below the agreed
scope and action items.

### 1. [Scope Item 1 — e.g., Mechanical Works]
- What was agreed, who does what, responsibilities
- Sub-bullets for specifics

### 2. [Scope Item 2 — e.g., Electrical Works]
- ...

### [N]. Deliverables & Timeline

| Deliverable | Responsible | Due Date |
|-------------|-------------|----------|
| [item]      | [party]     | [date]   |

Please confirm receipt and revert with the requested items by [date].

Best regards,

Sultan Issa
Technical Office Manager
Samaya Investment
```

## Key rules

- **Headline the meeting reference** (date + project name) in the subject
- **Use numbered sections** for each scope item agreed
- **End with a deliverables table** with clear deadlines
- **Always present draft to user** before sending — they may want CCs, language tweaks, or signature format changes
- **Save draft** to `09_Correspondence/` folder if user wants it filed
- **If scope revision involves CITC telecom**, reference the CITC clause pattern from samaya-docx-template's `references/mep-scope-completeness.md`

## Sample deliverables table

| Deliverable | Responsible | Due Date |
|-------------|-------------|----------|
| Revised quotation for [scope] | Subcontractor | [date] |
| CV of certified engineer | Subcontractor | [date] |
| Proposed delivery schedule | Subcontractor | [date] |
| Dedicated team nomination | Subcontractor | [date] |

## Signature block

```
Best regards,

Sultan Issa
Technical Office Manager
Samaya Investment
sultan@samayainvest.com
```
