# Cron 24h Email Scan Pattern

Trigger: Scheduled cron job checking for project-critical emails in last 24 hours.

## Key Constraints

- **No TCC SQLite access** — `sqlite3` returns "authorization denied". Use AppleScript Outlook object model only.
- **`every folder` fails** — must target `inbox` directly or `folder "Name" of inbox` for project folders. Standalone `folder "Name"` fails.
- **No user present** — must be fully autonomous with no clarification.
- **SILENT protocol** — if nothing new, output `[SILENT]` only.

## AppleScript Pattern

### Phase 1: Scan Inbox (all messages, last 24h)

```applescript
tell application "Microsoft Outlook"
    set today to current date
    set yesterday to today - (24 * 60 * 60)
    set output to ""
    
    set inboxMsgs to (every message of inbox)
    repeat with m in inboxMsgs
        set msgTime to time received of m
        if msgTime ≥ yesterday then
            set msgSubject to subject of m
            set msgSender to sender of m
            set senderName to ""
            try
                set senderName to name of msgSender
            end try
            set hasAtt to (count of (every attachment of m)) > 0
            set msgPreview to ""
            try
                set msgPreview to (text 1 thru 300 of (plain text content of m))
            end try
            set output to output & (id of m as text) & "|Inbox|" & senderName & "|" & msgSubject & "|" & (hasAtt as text) & "|" & msgPreview & return
        end if
    end repeat
    
    return output
end tell
```

### Phase 2: Scan Project Folders by Name

```applescript
tell application "Microsoft Outlook"
    set projectFolderNames to {"Asher Regional Museum", "Zamzam Projects", "RCRC Exhibition"}
    repeat with pfName in projectFolderNames
        try
            set pf to folder pfName
            set pfMsgs to (every message of pf)
            -- same message loop as Phase 1
        end try
    end repeat
end tell
```

### Phase 3: Get Email Details (body + attachments)

```applescript
tell application "Microsoft Outlook"
    set theMsg to message id <ID>
    set msgSubject to subject of theMsg
    set msgSender to sender of theMsg
    set senderName to name of msgSender
    set senderAddr to address of msgSender
    set msgTime to time received of theMsg
    set hasAtt to (count of (every attachment of theMsg)) > 0
    
    -- Body text
    set msgBody to plain text content of theMsg
    
    -- List attachments with types
    set atts to (every attachment of theMsg)
    repeat with att in atts
        set attName to name of att
        set attType to content type of att
    end repeat
end tell
```

## Filter Criteria (Project-Critical)

Include emails matching ANY of:
- Sender: Aconex Notification, Mimon Allitou, Hesham Abdelhameed, Mohammad Elbaz, Abdrabo Shahin
- Subject: Transmittal, RFI, SI-, TQ-, NCR, Code A/B/C/D, Submittal, MAR, IR-, VO
- Folder: Asher Regional Museum, Zamzam Projects, RCRC Exhibition

Silently skip ops/logistics: car requests, shipments, housing, technician transport, promotions.

## Report Format

Use emoji status column:
- 🆕 NEW — not previously reported, needs attention
- ⚠️ ACTION — requires immediate action (WeTransfer links, RFI responses due, CG Code C/D)
- ℹ️ INFO — admin/backlog, no action needed

Keep one line per item unless critical action needed. Translate Arabic subjects to English.

## Key Sender Verification

After scanning, explicitly state which key senders were NOT seen (e.g., "❌ Mimon Allitou — no emails"). This proves the scan ran and the absence was detected, not missed.
