# Document Naming & Search — Samaya Project

## The Problem
Hesham (Document Controller) changes naming conventions when sending. What's on the internal file ≠ what gets sent.

## Known Variations

| Internal Ref | How Actually Sent | Type Change |
|---|---|---|
| `ARM-SIC-MOC-LET-006` | `MOC-MUS-ASE-1A0-TQ-0026` | LET → TQ (Technical Query) |
| `ARM-SIC-MOC-...` | `MOC-MUS-ASE-...` | Prefix change |
| — | `MOC-ASEER-SIC-...` | Another prefix variant |

## How to Find Sent Documents

**Do NOT search by the internal document number alone.** Use this protocol:

1. **Outlook SQLite DB** (fastest, most reliable):
   ```
   DB: /Users/mohamedessa/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite
   ```
   Query sent items by Hesham (Hesham Abdelhameed):
   ```sql
   SELECT Message_NormalizedSubject, datetime(Message_TimeSent, 'unixepoch'), Message_DisplayTo
   FROM Mail 
   WHERE Message_SenderList LIKE '%hesham%'
     AND Message_IsOutgoingMessage = 1
     AND Message_TimeSent > [unix_timestamp]
   ORDER BY Message_TimeSent DESC;
   ```
   
   **Use Arabic keywords** for subject search — Hesham sends with Arabic subjects:
   ```sql
   WHERE Message_NormalizedSubject LIKE '%طلب%'
      OR Message_NormalizedSubject LIKE '%بحث%'
      OR Message_NormalizedSubject LIKE '%محتوى%'
   ```

2. **Email Archive** (`~/Desktop/Work_Projects/Aseer-emails-md-only-2026-05-22/Email_Archive/`):
   - Only goes up to ~20-22 May 2026
   - Files named by date + subject (usually truncated English)

3. **Email Attachments** (`~/Desktop/Work_Projects/Aseer_Email_Attachments_ALL/`):
   - 390+ .eml files, bulk exported
   - Some SENT_ prefixed (sent items)
   - All dated 3 May 20237 (bulk export date — check headers for actual send date)

4. **Aconex** (if no Outlook result):
   - Hesham may have sent via Aconex transmittal instead of email
   - Check Aconex notifications in email archive

## Pattern Recognition
- If it's a formal request to MoC, Hesham typically uses **TQ** (Technical Query) not **LET** (Letter)
- Even if the internal doc says "LET-006", ask: "Did this get sent as TQ-# instead?"
- The project prefix `MOC-MUS-ASE` is the current/active convention. `ARM-SIC-MOC` is legacy.
