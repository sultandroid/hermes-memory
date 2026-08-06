# Email → Risk Register Cross-Reference Pattern

When investigating a specific project topic (insurance, permits, approvals, delays), cross-reference Outlook emails with the project risk register to build a complete picture.

## Workflow

### 1. Search Outlook by Arabic/English keywords

```sql
-- Arabic keywords for the topic
SELECT m.Message_NormalizedSubject, m.Message_Preview,
       datetime(m.Message_TimeSent, 'unixepoch') as sent_date,
       m.Message_SenderList
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%تأمين%'
   OR m.Message_NormalizedSubject LIKE '%insurance%'
ORDER BY m.Message_TimeSent DESC
LIMIT 20;
```

**Key insight:** Arabic subject lines work directly in `Message_NormalizedSubject` — no encoding issues. The SQLite DB stores Arabic as UTF-8.

### 2. Filter by project

Narrow to the specific project by combining topic keywords with project name:

```sql
WHERE (m.Message_NormalizedSubject LIKE '%تأمين%' OR m.Message_NormalizedSubject LIKE '%insurance%')
  AND (m.Message_NormalizedSubject LIKE '%عسير%' OR m.Message_NormalizedSubject LIKE '%Aseer%')
```

### 3. Read the risk register for matching risks

```sql
-- Search risk register for insurance-related risks
SELECT * FROM risk_register WHERE title LIKE '%insurance%' OR title LIKE '%تأمين%';
```

In the MD-based register, use `search_files`:
```
search_files(pattern='PRR-COM-07|insurance|تأمين', path='aseer-museum-pm/01_Registers/')
```

### 4. Cross-reference findings

| Source | What to check |
|--------|---------------|
| **Contract** | Article 13 (Insurance) — mandatory coverage requirements |
| **Risk Register** | PRR-COM-07 (insurance adequacy) — status, score, owner |
| **Outlook** | Emails requesting insurance quotes, CAR/EAR policy issuance |
| **Procurement Plan** | Insurance requirements in PO/contract templates |
| **Risk Management Plan** | Transfer strategy — insurance as risk response |

### 5. Build the status summary

Present as a table:

| Item | Status |
|------|--------|
| CAR (Contractor All Risk) | ✅/❌ Issued? |
| EAR (Erection All Risk) | ✅/❌ Issued? |
| Fine Arts / Transit | ✅/❌ Issued? |
| Professional Indemnity | ✅/❌ Issued? |
| Risk Register Entry | 🔴/🟡/🟢 Status + Score |

## Example: Aseer Museum Insurance Investigation

**Query:** `تأمين جميع أخطار المقاولين` (Contractor All Risk Insurance)

**Outlook result:** One email chain found — but it was for **Zamzam Museum (NWC)**, not Aseer. Baraa Anbar (NWC) replied "Already sent it (13/1/2026)".

**Risk register result:** PRR-COM-07 — "Adequacy of insurance unconfirmed across CAR/EAR, fine-art transit/installation" — **Low (3) / Open**.

**Conclusion:** No CAR/EAR policy issued for Aseer Museum. The only email found was for a different project. The risk is logged but at Low severity — may need escalation.

## Pitfalls

- **One email chain ≠ project coverage.** The email subject may match but the recipient/context may be a different project. Always check `Message_SenderList` and `Message_DisplayTo` to identify the project.
- **Risk register may under-score.** PRR-COM-07 at Low (3) may not reflect actual exposure if no policy exists. Cross-check against contract requirements (Art. 13).
- **No email evidence ≠ no action taken.** Insurance may have been arranged outside email (phone, direct contract). The absence of email evidence is a flag, not proof.
- **Arabic search terms are case-sensitive in LIKE.** Use the exact Arabic spelling as stored in the DB.
