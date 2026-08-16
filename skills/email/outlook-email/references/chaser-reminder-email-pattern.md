# Chaser / Reminder Email Pattern (FW: Required Documents)

A recurring email class on Aseer Museum: **Samaya chases a specialist/vendor for required documents or CG-comment responses.** These are procurement/design chasers, not scope or technical questions. Recognise them by subject keywords and handle them without burning extraction cycles.

## Recognising the class

Subject patterns (Aseer Museum, 2026-08):
- `Reminder – Required Landscape Specialist Documents and Information`
- `Reminder – Required Landscape Specialist Information and Documents`
- `Kick-Off Meeting – Required Landscape Specialist Documents and Information`
- `FW: Reminder – ...`

Sender is usually the Project Director (Muhammad Waris Sultan Khan) or a coordinator (Ahmed Yehia), addressed to the specialist (e.g. Muhammad Abid at TLC).

## Key facts

1. **The 255-char preview truncates before the actual content.** The preview shows only the greeting + first line ("Please find below the email and CG's comments regarding the landscape design...") and cuts off. The actual CG comments are in the **forwarded body below**, which is NOT in `Message_Preview`. Do NOT assume the preview is enough — for a chaser, the substance is always in the quoted original.

2. **"Recall" messages create near-identical rows.** Outlook "recall this message" generates separate Mail rows with the same subject and `Message_Preview` starting "Ahmed Yehia would like to recall the message...". When listing a thread, these are noise — dedupe by sender+subject and skip the recall rows.

3. **The referenced CG-comments attachment may be corrupt/0-byte in OneDrive.** The CG comments PDF (e.g. `P083_Landscape Design Development COMMENTS 00.pdf`) can be a 0-4 byte stub (OneDrive files-on-demand). `read_file` returns empty, `pdfminer` raises `No /Root object!`. Flag for manual re-sync rather than retrying.

## Workflow

1. **Find the thread** by subject keyword:
```sql
SELECT Record_RecordID, datetime(Message_TimeReceived,'unixepoch','localtime'),
       Message_SenderList, Message_DisplayTo, Message_Preview
FROM Mail
WHERE Message_NormalizedSubject LIKE '%Landscape Specialist%'
ORDER BY Message_TimeReceived DESC;
```
2. **Identify the authoritative message** — the one from the PD to the specialist (not the recall rows, not the coordinator's internal reminders).
3. **Read the preview** for the greeting + routing line (who coordinates with whom — e.g. "Engr. Sultan Issa, Samaya's Technical Manager, will coordinate directly with TLC").
4. **If the CG comments are needed**, they are in the forwarded body → use AppleScript `plain text content of m` or the `.olk15Message` body extraction. The preview alone will NOT contain them.
5. **Cross-reference the project registers** for context: submittal register (what was submitted, when), specialist scope README (candidate status, offer), submission plan (gate dates, slippage). This gives the "why is this being chased" answer.

## Reporting shape

Lead with what the email is (a chaser), then the chain table (time/sender/to/purpose), then the context (what was submitted, the slipped gate, the missing deliverables), then the ask. Note explicitly if the CG-comments attachment or full body could not be read and why.
