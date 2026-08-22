# Vendor Reply Drafting Workflow

When the user asks "what's the reply to X" or "draft the reply to [vendor/consultant]" (e.g. a BIM/design specialist, supplier, or CG), follow this order. The goal is to determine whether a reply already exists, understand the full thread, then draft in the user's preferred format.

## 1. Find the thread (sender domain + subject)

Vendors often send from a company domain, not a personal name. Search by domain fragment AND subject keywords, always JOIN folders, always use 'localtime':

```sql
SELECT m.Record_RecordID as id,
       datetime(m.Message_TimeReceived,'unixepoch','localtime') as received,
       f.Folder_Name as folder, m.Message_SenderList as sender,
       m.Message_NormalizedSubject as subject, m.Message_HasAttachment as att
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE (m.Message_SenderList LIKE '%radiance%' OR m.Message_NormalizedSubject LIKE '%BIM%')
  AND date(m.Message_TimeReceived,'unixepoch','localtime') >= date('now','-30 days','localtime')
ORDER BY m.Message_TimeReceived DESC;
```

## 2. Read the FULL body, not the preview

`Message_Preview` is capped at 255 chars — useless for a vendor letter. Use AppleScript `plain text content of m`:

```bash
osascript -e "tell application \"Microsoft Outlook\" to set m to message id $ID" \
          -e "tell application \"Microsoft Outlook\" to get plain text content of m"
```

The full body carries the contract facts (value, phases delivered, payment schedule, requests) that the reply must address.

## 3. CHECK SENT ITEMS FIRST — has it already been replied to?

**Do not draft a reply if one already exists.** Query Sent Items for replies to the same vendor/thread:

```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived,'unixepoch','localtime') as received,
       f.Folder_Name, m.Message_NormalizedSubject
FROM Mail m JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE f.Folder_Name LIKE '%Sent%'
  AND (m.Message_ToRecipientAddressList LIKE '%radiance%' OR m.Message_NormalizedSubject LIKE '%BIM%')
ORDER BY m.Message_TimeReceived DESC;
```

Also check the thread's `Conversation_ConversationID` for any reply in any folder. If a reply exists, report it instead of drafting a new one. If none exists, say so explicitly ("no reply sent") before drafting.

## 4. Draft in the user's preferred format

- **Provide text for manual copy** — do NOT create an Outlook draft unilaterally.
- **Numbered list** (1. 2. 3.), not HTML tables.
- **Concise, no preamble** — present only the email body text.
- **Flag open decisions** — after the draft, list the points the user must decide (e.g. whether to concede a cost claim, whether to resume or close out scope) so they can adjust before sending.

## Pitfall — multiple parallel threads from the same vendor

A vendor may run several threads at once (e.g. a payment-schedule thread AND a separate PO/licensing thread to a different recipient). Distinguish them by subject + recipient before drafting — don't merge them into one reply.
