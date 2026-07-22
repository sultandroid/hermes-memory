# CG Communication Plan Violation Detection

Detect when CG bypasses Samaya and contacts subcontractors/specialists directly. This is a recurring compliance check for the Aseer Museum project.

## Trigger

User asks to "check mails for communication plan violations" or "see if CG is contacting subcontractors directly."

## Detection Method

### Step 1 — Identify CG senders

```sql
SELECT DISTINCT m.Message_SenderList, m.Message_SenderAddressList
FROM Mail m
WHERE m.Message_SenderAddressList LIKE '%cg.com.sa%'
ORDER BY m.Message_SenderList;
```

### Step 2 — Find CG emails to non-Samaya, non-CG recipients

```sql
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject,
       m.Message_ToRecipientAddressList as to_list,
       m.Message_CCRecipientAddressList as cc_list
FROM Mail m
WHERE m.Message_TimeReceived >= strftime('%s', 'now', '-14 days', 'localtime')
  AND m.Message_SenderAddressList = 'malrezeni@cg.com.sa'
  AND m.Message_ToRecipientAddressList NOT LIKE '%samayainvest%'
  AND m.Message_ToRecipientAddressList NOT LIKE '%cg.com.sa%'
  AND m.Message_ToRecipientAddressList NOT LIKE '%ace-mb%'
  AND m.Message_ToRecipientAddressList NOT LIKE '%moc.gov.sa%'
ORDER BY m.Message_TimeReceived DESC;
```

### Step 3 — Find subcontractors/specialists emailing CG directly without Samaya in CC

```sql
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
       m.Message_SenderList as sender,
       m.Message_SenderAddressList as email,
       m.Message_NormalizedSubject as subject,
       m.Message_ToRecipientAddressList as to_list,
       m.Message_CCRecipientAddressList as cc_list
FROM Mail m
WHERE m.Message_TimeReceived >= strftime('%s', 'now', '-14 days', 'localtime')
  AND m.Message_SenderAddressList NOT LIKE '%samayainvest%'
  AND m.Message_SenderAddressList NOT LIKE '%cg.com.sa%'
  AND m.Message_SenderAddressList NOT LIKE '%ace-mb%'
  AND m.Message_SenderAddressList NOT LIKE '%moc.gov.sa%'
  AND m.Message_SenderAddressList NOT LIKE '%noreply%'
  AND m.Message_SenderAddressList NOT LIKE '%aconex%'
  AND (m.Message_ToRecipientAddressList LIKE '%cg.com.sa%'
       OR m.Message_CCRecipientAddressList LIKE '%cg.com.sa%')
  AND (m.Message_CCRecipientAddressList NOT LIKE '%samayainvest%'
       AND m.Message_ToRecipientAddressList NOT LIKE '%samayainvest%')
ORDER BY m.Message_TimeReceived DESC;
```

### Step 4 — Check specific known subcontractor/specialist domains

```sql
AND (m.Message_ToRecipientAddressList LIKE '%@studiozna%'
     OR m.Message_ToRecipientAddressList LIKE '%@rawasin%'
     OR m.Message_ToRecipientAddressList LIKE '%@glasbau%'
     OR m.Message_ToRecipientAddressList LIKE '%@nissenrichards%'
     OR m.Message_ToRecipientAddressList LIKE '%@adeng%'
     OR m.Message_ToRecipientAddressList LIKE '%@graphite%'
     OR m.Message_ToRecipientAddressList LIKE '%@namaa%')
```

## Violation Severity Classification

| Severity | Pattern | Example |
|----------|---------|---------|
| **HIGH** | CG emails sub-consultant (NRS, ZNA, AD Engineering) directly, bypassing Samaya | Mansour emailing Jim Richards (NRS) 5 times on "large stone" thread |
| **HIGH** | CG directs specialist (ZNA, AD) to act without Samaya approval | Mansour emailing Dogan (ZNA) "Dear Dogan, please reply to this email" |
| **MEDIUM** | Subcontractor emails CG directly with Samaya in To but not managing the channel | Rawasin sending Teams invite to CG with Samaya in To |
| **LOW** | Specialist CC's CG on reply to Samaya, creating direct line | ZNA replying to Waris but CC'ing Mansour and addressing him by name |

## Violation Report Template

```
## CG Communication Plan Violations — [Date Range]

### 1. [Reviewer] Emailing [Specialist] Directly — [Severity]

| Date | Subject | To | CC |
|------|---------|----|----|
| [date] | [subject] | [to_list] | [cc_list] |

**Evidence:** [email subject, date]
**Issue:** [what the violation is — e.g., "CG bypassing Samaya to direct NRS"]
**Action needed:** [e.g., "Raise with CG PM. All communication to sub-consultants must go through Samaya."]

### 2. [Subcontractor] Emailing CG Directly — [Severity]

...
```

**IMPORTANT — reference emails by date + subject, not internal email IDs.** Internal email IDs (Record_RecordID from SQLite) are not meaningful to anyone outside the agent session. Use date and subject line so the recipient can find the email in their own Outlook. Example: "9 Jul 2026, subject: A large stone mentioned in Art Commission Schedule" not "Email ID 48008".

## Known Violations (Aseer Museum, Jul 2026)

| # | Violation | Severity | Evidence | Who Initiated |
|---|-----------|----------|----------|---------------|
| 1 | Mansour Alrezeni emailing NRS (Jim Richards) directly | HIGH | 5 emails 9-18 Jul, NRS in To field, bypassing Samaya | **Mansour** — no Samaya person CC'd NRS first |
| 2 | Mansour Alrezeni emailing ZNA (Dogan Kozan) directly | HIGH | 21 Jul, Dogan in To, "Dear Dogan, please reply" | **Waris** — CC'd Dogan on his reply to Mansour first; Mansour then exploited it |
| 3 | Rawasin (Shihab) emailing CG (Venu) directly | MEDIUM | 8 Jul, Teams invite to CG with Samaya in To | **Shihab** — subcontractor initiated |
| 4 | ZNA (Dogan) CC'ing Mansour on reply to Samaya | LOW | 21 Jul, reply to Waris with Mansour in CC | Secondary effect of #2 |

### Critical lesson — trace the thread before assigning fault

In violation #2, the initial report blamed Mansour alone. Full thread analysis showed:
1. Waris CC'd Dogan on his reply to Mansour (20 Jul, ID 48813)
2. Dogan replied to Waris CC'ing Mansour (21 Jul, ID 48843)
3. Mansour then put Dogan in To (21 Jul, ID 48913)

**Always use Conversation_ConversationID to reconstruct the full thread** before concluding who breached protocol. The first person to include a specialist on a CG thread is the one who opened the door, even if CG later escalated.

## Communication Plan Reference

The project communication plan (MOC-ASEER-SIC-1K0-PL-0018 Rev C02) defines:

### Section 12.6 — Subcontractor Communication Protocol

| Rule | Text |
|------|------|
| **S-1** | "All subcontractor correspondence must flow through the Samaya channel — direct subcontractor-to-CG communication is not permitted." |
| **S-2** | "Subcontractor → Samaya Tech Review → CG. Samaya owns technical completeness before forwarding." |
| **S-3** | "Subcontractor → Samaya Site → CG. Samaya screens for duplication & completeness." |
| **S-5** | "NCR raised against Samaya. Samaya passes corrective-action to subcontractor. Samaya owns closure." |
| **S-6** | "Subcontractor weekly report → Samaya Site → feeds R-01 DPR. No separate subcontractor report to CG." |

### Section 1.2 — Authority Chain

| Party | Role |
|-------|------|
| Samaya Investment Company | Design & Build Contractor |
| NRS (Nissen Richards Studio) | Design Lead / Architect of Record — under Samaya |
| ZNA (Studio ZNA) | Lighting Design Specialist — under Samaya |
| Rawasin | AV/IT Subcontractor — under Samaya |

### Communication Matrix (PMC Rev 01, 18 Jan 2026)

All 20 items show flow: **Contractor → CG**. No direct sub-consultant or subcontractor path exists.

### Key SQL Patterns for PL-0018 Compliance Check

**Detect CG emailing NRS directly (violates S-1, S-2):**
```sql
AND m.Message_ToRecipientAddressList LIKE '%@nissenrichards%'
```

**Detect CG emailing ZNA directly (violates S-1, S-3):**
```sql
AND m.Message_ToRecipientAddressList LIKE '%@studiozna%'
```

**Detect CG emailing any specialist directly (violates S-1):**
```sql
AND (m.Message_ToRecipientAddressList LIKE '%@studiozna%'
     OR m.Message_ToRecipientAddressList LIKE '%@rawasin%'
     OR m.Message_ToRecipientAddressList LIKE '%@glasbau%'
     OR m.Message_ToRecipientAddressList LIKE '%@nissenrichards%'
     OR m.Message_ToRecipientAddressList LIKE '%@adeng%'
     OR m.Message_ToRecipientAddressList LIKE '%@graphite%'
     OR m.Message_ToRecipientAddressList LIKE '%@namaa%'
     OR m.Message_ToRecipientAddressList LIKE '%@evergreen%'
     OR m.Message_ToRecipientAddressList LIKE '%@acoustieg%'
     OR m.Message_ToRecipientAddressList LIKE '%@jocavi%'
     OR m.Message_ToRecipientAddressList LIKE '%@ame-ts%'
     OR m.Message_ToRecipientAddressList LIKE '%@transorient%')
```

### Report Template with Clause References

When writing a violation report, cite the specific PL-0018 clause:

```
**Violated clauses:**
- PL-0018 Sec 12.6 S-1 — "All subcontractor correspondence must flow through the Samaya channel."
- PL-0018 Sec 12.6 S-2 — Submittal path requires Subcontractor -> Samaya Tech Review -> CG.
- Communication Matrix (PMC Rev 01) — No direct sub-consultant -> CG path exists.
```
