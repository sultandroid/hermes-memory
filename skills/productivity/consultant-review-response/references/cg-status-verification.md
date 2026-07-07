# CG Response Status Verification — Aseer Museum

How to verify whether CG (Consultancy Group) has responded to a submitted plan document.

## Data Sources (in verification order)

| Source | Path | Purpose |
|--------|------|---------|
| CG_STATUS.md | `Docs/02_Plans_and_Procedures/02.XX_<Plan>/02_CG_Responses/CG_STATUS.md` | Per-plan status summary |
| CG_Response_Register.md | `Docs/02_Plans_and_Procedures/CG_Response_Register.md` | Master register of all CG responses |
| Register_ASEER_Professional.csv | `Docs/Email Archive/مشروع متحف عسير الإقليمي/Register_ASEER_Professional.csv` | **Authoritative** — all submission/reply emails with doc codes |
| Live Outlook Scan | AppleScript body search or SQLite direct query | Latest emails not yet in archive |

## Email Pattern (Aseer Museum)

Submission → Response flow:

```
Hesham Abdelhameed (Hesham.a@samayainvest.com)
  └─→ sends submission email to CG (Mohammad Elbaz, Sundus Alfeer, Hossam Mabrouk)
       └─→ CG (Mohammad Elbaz <melbaz@cg.com.sa>) replies "RE: <doc_code> / <title>"
            with review outcome (Code A/B/C/D or comments)
```

- If Mohammad Elbaz has sent a "RE:" email for that doc code → CG response exists
- If only Hesham's outgoing email exists and no CG reply → status is genuinely "Submitted, Awaiting Response"

## Register CSV Query

```bash
# Find all emails for a specific doc code
grep "<doc_code>" "Docs/Email Archive/مشروع متحف عسير الإقليمي/Register_ASEER_Professional.csv"

# Find all emails from CG reviewer
grep "melbaz@cg.com.sa" "Docs/Email Archive/مشروع متحف عسير الإقليمي/Register_ASEER_Professional.csv"

# Find emails after a date
awk -F',' '$1 >= "2026-05-21"' "Docs/Email Archive/مشروع متحف عسير الإقليمي/Register_ASEER_Professional.csv"
```

## Register CSV Column Structure

```
Date,Ref,Category,From,To,Subject,Action,Remarks,Status
```

Key columns:
- **Date** — email date (YYYY-MM-DD)
- **Ref** — unique email reference (ASE-EMAIL-NNNNN)
- **Category** — SDR (submittal), SI (site instruction), REP (report), etc.
- **From** — sender (may be Hesham for submissions, melbaz@cg.com.sa for CG replies)
- **Subject** — includes doc code and title. CG replies start with "RE:" or "RE:"
- **Action** — "Reviewed / Reply Sent" for both directions
- **Remarks** — contains "From: Hesham" for CG-forwarded emails, or Arabic notes
- **Status** — "Active" for current entries

## CG Reviewer Team

| Name | Email | Role |
|------|-------|------|
| Mohammad Elbaz | melbaz@cg.com.sa | Primary CG reviewer (28+ emails) |
| Mahmoud Afifi | mafifi@cg.com.sa | Project Management |
| Sundus Alfeer | salfeer@cg.com.sa | NCR/QHSE |
| Mohamed Elroby | melroby@cg.com.sa | MEP |
| Yasser Zaki | yzaki@cg.com.sa | Aconex |

## Live Outlook Scan

For emails not yet in the CSV archive:

```bash
# Body search in "Asher Regional Museum" folder
osascript scripts/outlook_body_search.applescript "<doc_code>" "Asher Regional Museum"

# Recent CG emails
osascript scripts/outlook_recent.applescript 30 "Asher Regional Museum" | grep "cg.com.sa"

# Subject search in "Asher Regional Museum" folder for specific plan
osascript scripts/outlook_body_search.applescript "<Plan Name>" "Asher Regional Museum"
```

## Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| Code A | Approved | File and close |
| Code B | Approved with Comments | Address comments in next revision |
| Code C | Revise & Resubmit | Full revision required |
| Code D | Disapproved / Rejected | Major rework needed |
| Submitted | Awaiting Response | No CG reply yet |
| 📧 Unread | CG email in Outlook not yet processed | Read and classify |
