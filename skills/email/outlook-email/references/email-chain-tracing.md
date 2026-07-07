# Email Forward-Chain Tracing

Reconstruct a forwarded email chain across the Outlook SQLite database to understand who asked what of whom.

## When to use

- User says "check this mail also what they want" — forwarded email, multiple hops
- Investigation message: "FW: Subject" where the chain involves 2+ forwards
- Understanding the original sender's intent vs the forwarder's intent (they may differ)
- Identifying which recipients are in the loop and when

## Why not Conversation_ConversationID

Forwards (FW:) create **new conversation IDs**. Unlike Reply (RE:) chains that share one `Conversation_ConversationID`, each forward hop starts a fresh thread. Subject-keyword matching is required to find all instances.

## Pattern: subject-keyword discovery

```sql
-- Step 1: Find ALL instances of the email by subject
-- Use multiple LIKE patterns since subject may vary slightly
SELECT Record_RecordID,
       datetime(Message_TimeReceived, 'unixepoch', 'localtime') as received,
       Message_SenderList as sender,
       Message_DisplayTo as to_list,
       Message_CCRecipientAddressList as cc_list,
       Message_HasAttachment as att
FROM Mail
WHERE Message_NormalizedSubject LIKE '%GBH Letter%'
   OR Message_NormalizedSubject LIKE '%Letter %001%'
ORDER BY Message_TimeReceived ASC;
```

**Returns all hops in chronological order.** Each hop is one forward.

## Step 2: Read preview at each hop

```sql
SELECT Record_RecordID, Message_SenderList,
       substr(Message_Preview, 1, 600) as preview
FROM Mail
WHERE Record_RecordID IN (<id1>, <id2>, <id3>);
```

`Message_Preview` holds the first ~500 chars — enough to see the forwarder's note vs the original body. There is no `Message_Body` column in this Outlook schema.

## Step 3: Understand intent at each level

| Hop | Sender | Body pattern | Intent |
|-----|--------|-------------|--------|
| Original | Subcontractor/consultant | "Kindly find attached Letter #001 and updated schedule" | Deliverable handover |
| Forward 1 | Internal (Samaya PM) | "Looping Eng. X" | Information only |
| Forward 2 | Internal (Samaya PM) | "Please check and confirm if aligned" | **Action request to you** |

The **last forwarder's note** is the active request. Earlier hops provide context but don't require your action unless the last forwarder says so.

## Step 4: Cross-reference request against project files

Once you know what's being asked (e.g. "check if GBH's updated schedule aligns with our schedule"):

```bash
# Find the referenced project files
find <project_root> -name "*schedule*" -o -name "*Programme*" -o -name "*Design*Management*" 2>/dev/null | head -10
```

Types of files to look for:
- **Design Schedule Programme:** `02_Submittals/Design_Schedule_Programme.xlsx`
- **Design Management Plan:** `10_Plans/Design Management Plan Rev C02.pdf`
- **Existing subcontractor schedule:** `24_Subcontractors/<Trade>/01_Schedule_and_BOQ/<name>.xlsx`
- **Submittal Register:** `<Trade>_Submittal_Register/*.xlsx`

Present findings as a structured summary showing:
1. Email chain (timeline: who → whom, when)
2. Action requested (the last forwarder's actual ask)
3. Relevant files on disk the user can compare against

## Pitfalls

- **Don't assume the original sender is the requester.** The last forwarder is usually the one asking you to act. Read their note separately.
- **Forwards to new people change the action owner.** If the original was CC'd to 5 people but the forward targets only you, the ask is yours.
- **Message_Preview truncates at ~500 chars.** For full body, use AppleScript (`plain text content of message id <ID>`). See the main SKILL.md for the script template.
- **Distribution list vs individual addresses.** `Message_DisplayTo` may show "m.samir@..." while `Message_CCRecipientAddressList` is semicolon-separated. Check both to see who's in the loop.
- **Recent forward may overwrite file attachment metadata.** The most recent forward (today's) owns the attachment reference in `Files` table. The original email's attachment may not be the one still reachable.

## Mandatory: don't infer email intent from document content alone

**CRITICAL workflow lesson:** When the user asks about an email/document reference (e.g. "FW: MOC-ASEER-SIC-1A0-TQ-0021 / Construction Methodology for Gallery Partitions"), DO NOT answer based only on the document content you find on the filesystem. The document tells you what the original query was about — but it does NOT tell you who forwarded it to the user, what the forwarder's note said, or what action they expect.

**Correct workflow (user expects this every time):**

1. **Read the document** from the filesystem — understand its content
2. **Then query Outlook SQLite** by subject keyword to find the email thread
3. **Get the full thread** sorted by time descending — identify the most recent emails
4. **Read previews** of the latest 2-3 emails to understand the request chain
5. **Extract attachments** from the most recent email(s) via AppleScript — the attachment in the latest forward is the one the user received
6. **Present both** — document content + what each level of the chain asked

**Example from a real session:**

User asked about "FW: MOC-ASEER-SIC-1A0-TQ-0021". The agent read the TQ PDF (NRS proposing drywall over blockwork) and answered based on inference about what "they want from me now" — which was wrong. The correct answer came from querying Outlook:

```sql
SELECT m.Record_RecordID, datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
       m.Message_SenderList, m.Message_SenderAddressList,
       substr(m.Message_Preview, 1, 500) as preview
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%TQ-0021%'
ORDER BY m.Message_TimeReceived DESC LIMIT 5;
```

The preview of the two most recent emails revealed:
- Hani Alghamdi (08:39): "We are attaching technical proposal for partitions. We need your accept of technical proposal before we can request a financial proposal."
- Muhammad Waris (09:06): "I have reviewed the attached documents. It seems ok. Please have a look it at your end prior to proceed further."

The document was the same Mada ceiling proposal studied earlier — not the TQ itself. The actual ask was: review Mada's ceiling technical proposal and sign off so Hani can request pricing.

**Checklist when the user says "what do they want from me":**
- [ ] Read the document content (filesystem search)
- [ ] Search Outlook by doc code or subject keyword (SQLite)
- [ ] Read Message_Preview of the most recent email(s) — the preview shows the active request
- [ ] Check Message_ToRecipientAddressList + Message_CCRecipientAddressList to confirm you're the target
- [ ] Extract attachments to see what was actually attached (AppleScript)
- [ ] Present: who sent → to whom → what they said → what action is expected
- [ ] Cross-reference attachments against project folder to see if already filed
