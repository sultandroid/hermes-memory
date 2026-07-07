# Outlook Folder Hierarchy — sultan@samayainvest.com

Discovered May 31, 2026 via AppleScript enumeration of `every mail folder`.

## Account Structure

```
On My Computer/                    ← Local PST/OLM store
├── Inbox                              18,099 msgs (Jul 2022)
├── Outbox
├── Sent Items
├── Drafts
├── Deleted Items
└── Junk E-mail

Exchange: sultan@samayainvest.com/    ← Server-side store (currently disconnected)
├── Inbox                                    0 msgs ❗
│   ├── Asher Regional Museum              649 msgs (latest Oct 2025)
│   ├── Mousa Babiker
│   ├── Notes
│   ├── Sent
│   ├── SPMS
│   ├── Trash
│   ├── Zamzam Project                      46 msgs (latest Oct 2025)
│   └── Zamzam Projects                    828 msgs (latest Jul 2025)
├── Archive                                 59 msgs (latest Oct 2025)
├── Conversation History
├── Deleted Items
│   └── Zamzam Project  (trailing space!)   49 msgs (latest May 19, 2026)
├── Drafts
├── erp                                    433 msgs (latest Feb 12, 2026)
├── Junk Email                              25 msgs
├── RSS Feeds
├── Sent Items
├── Snoozed                                  0 msgs
├── Sync Issues
│   ├── Conflicts
│   ├── Local Failures
│   └── Server Failures
└── Clutter                                  0 msgs
```

## Key Findings

1. **Exchange Inbox is empty** — 0 messages. The account is disconnected/sync broken.
2. **"On My Computer" Inbox has 18K messages** — but stopped syncing July 2022.
3. **Project subfolders under Exchange are stale** — latest activity Oct 2025–Feb 2026.
4. **Most recent project emails** (May 19, 2026, Ahmed Elgharib/EGEC) are in **Deleted Items > Zamzam Project** (trailing space version).
5. **erp folder** has notifications for purchase orders (P01147, P01197, P01182 etc.), latest Feb 12, 2026.

## Folder Name Quirks

AppleScript returns folder names **exactly as stored** — including trailing spaces:

```applescript
tell application "Microsoft Outlook"
    repeat with f in (every mail folder)
        set fn to name of f
        -- "Zamzam Project " has a trailing space!
        -- "Zamzam Project" does not
    end repeat
end tell
```

### Identifying the Right Folder

```applescript
-- List all folders containing "Zamzam" with their container
tell application "Microsoft Outlook"
    set results to {}
    repeat with f in (every mail folder)
        set fn to name of f
        if fn contains "Zamzam" then
            set containerName to ""
            try
                set containerName to name of (container of f)
            end try
            set mc to count of (every message of f)
            set end of results to containerName & " > '" & fn & "' (" & mc & " msgs)"
        end if
    end repeat
    return results
end tell
```

Result:
- `Inbox > 'Zamzam Project' (46 msgs)`
- `Inbox > 'Zamzam Projects' (828 msgs)`
- `Deleted Items > 'Zamzam Project ' (49 msgs)` ← trailing space, most recent

## Exchange Account Health Check

```applescript
tell application "Microsoft Outlook"
    try
        set accts to every exchange account
        set a to item 1 of accts
        return "Account: " & name of a & " (" & email address of a & ")"
    on error errMsg
        return "Error: " & errMsg
    end try
end tell
```

Expected: `Account: sultan@samayainvest.com (sultan@samayainvest.com)`

Online status cannot be read via AppleScript alone — check manually in Outlook → Tools → Accounts.

## Pipeline Script Correction

The current `bim_email_pipeline.py` only checks `["Inbox"]`. To scan all project folders:

```python
FOLDER_MAP = [
    # (folder_name, project_key)
    ("Asher Regional Museum", "Aser"),
    ("Zamzam Project", "Zamzam"),       # Under Inbox — no trailing space
    ("Zamzam Projects", "Zamzam"),
    ("Zamzam Project ", "Zamzam"),      # Under Deleted Items — trailing space!
    ("erp", "General"),
]
```
