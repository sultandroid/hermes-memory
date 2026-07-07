---
name: apple-ecosystem
description: Manage the Apple ecosystem on macOS — Notes, Reminders, FindMy, and iMessage via CLI tools.
tags: [apple, macos, notes, reminders, findmy, imessage]
---

# Apple Ecosystem Management

Manage Apple devices and services from the terminal: Apple Notes, Apple Reminders, FindMy (device tracking), and iMessage/SMS.

## Apple Notes — memo CLI

Manage Apple Notes using the `memo` CLI tool.

### Create a note
```bash
memo add "Note Title" --content "Note content here"
```

### Search notes
```bash
memo list | grep -i "search term"
memo show <note-id>
```

### Edit a note
```bash
memo edit <note-id>
```

### Delete a note
```bash
memo delete <note-id>
```

## Apple Reminders — remindctl CLI

Manage Apple Reminders via the `remindctl` CLI.

### Add a reminder
```bash
remindctl add "Reminder text" --list "List Name" --due-date "2026-06-30"
```

### List reminders
```bash
remindctl list --list "List Name"
```

### Complete a reminder
```bash
remindctl done <reminder-id>
```

## FindMy — Find My Device Locator

Track Apple devices and AirTags via FindMy.app on macOS using the `findmy` CLI.

### List devices
```bash
findmy list
```

### Locate a device
```bash
findmy locate "Device Name"
```

### Get current position
```bash
findmy position
```

## iMessage — imsg CLI

Send and receive iMessages/SMS via the `imsg` CLI.

### Send a message
```bash
imsg send "+15551234567" "Message text"
```

### Send to a contact
```bash
imsg send "Contact Name" "Message text"
```

### Read recent messages
```bash
imsg recent --count 10
```

### Check if contact is online
```bash
imsg online "Contact Name"
```

## Prerequisites

These CLI tools must be installed separately:
- `memo` — from `brew install memo` or from source
- `remindctl` — from `brew install remindctl`
- `findmy` — from `brew install findmy`
- `imsg` — from `brew install imsg`
