# Forwarded Document Analysis — Thread-First Workflow

When the user forwards a document (PDF) and asks "what do they want from me" / "analyze this", the correct sequence is:

## Workflow

1. **NEVER analyze a document in isolation.** The email thread provides context — sender intent, what was requested, who approved what.

2. **Trace the Outlook thread first by subject/doc code:**
   ```sql
   SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as received,
          f.Folder_Name, m.Message_SenderList, m.Message_NormalizedSubject,
          m.Message_HasAttachment
   FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
   WHERE m.Message_NormalizedSubject LIKE '%<doc-code-or-keyword>%'
   ORDER BY m.Message_TimeReceived DESC;
   ```

3. **Read the last 2-3 email previews** to understand the direct ask:
   ```sql
   SELECT Record_RecordID, Message_SenderList, Message_SenderAddressList,
          substr(Message_Preview, 1, 800) as preview
   FROM Mail WHERE Record_RecordID IN (<id1>, <id2>, <id3>);
   ```

4. **Check To/CC lists** — determine if user is primary actionee or just informed:
   ```sql
   SELECT Message_ToRecipientAddressList, Message_CCRecipientAddressList
   FROM Mail WHERE Record_RecordID = <id>;
   ```

5. **Extract attachments** to see companion files sent in same thread.

6. **Read the document** — PyPDF2 for text PDFs, OCR (tesseract) for scanned.

7. **Cross-reference against contracts** in `01_Contracts/<vendor>_Contract/`:
   - Payment milestone clauses vs claim
   - Definitions of key terms ("Shop Drawings", "Approval", "Engineer")
   - Compare claim against contractual conditions

8. **Synthesize** — what the sender wants + whether contractual basis supports it.

## Pitfalls

- **Empty .eml stubs** are 0-byte — skip them, go directly to Outlook SQLite.
- **Don't conflate NRS approval with contractual approval** — NRS ≠ Engineer defined in contract.
- **Don't conflate CG/client approval with subcontract milestone conditions** — Many subcontarcts reference Samaya's Engineer, not the end client.
- **"Approved" means what the contract says it means** — Check the contract's definitions section.

## Example (this session)

User forwarded GBH Letter 001. Traced thread by "MOC-ASEER-SIC-1A0-TQ-0021" → found 30 emails. Last 2: Hani asked for tech acceptance → Waris forwarded to user for review. Attachment was Mada Gypsum ceiling PDP. Cross-referenced GBH contract payment clause — "25% Design and Shop Drawings approved" requires Samaya Engineer approval, not CG.
