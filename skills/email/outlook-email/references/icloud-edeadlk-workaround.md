# iCloud EDEADLK Workaround for Cron Jobs

## Problem

Files in `~/Documents/` (iCloud Drive-synced) return `OSError: [Errno 11] Resource deadlock avoided` on any read attempt — `open()`, `cat`, `head`, `cp`, `python3 open()`, even after `brctl download` reports the file is local.

This affects cron jobs that need to read/write register files in iCloud-synced project directories.

## Reliable Workaround: brctl download + cat > /tmp (PRIMARY)

The most consistently reliable method for **reading** iCloud-synced files in `~/Documents/`:

```bash
# Step 1: Force iCloud to sync the file locally
brctl download ~/Documents/Asher_Regional_Museum_Document_Control/01_Registers/submittal_register.md

# Step 2: Wait for sync
sleep 2

# Step 3: Copy to /tmp using shell redirect (NOT cp — cp uses fcopyfile which deadlocks)
cat ~/Documents/.../file.md > /tmp/file.md

# Step 4: Read from /tmp with normal tools
cat /tmp/file.md
```

The `cat > /tmp/` redirect bypasses the `fcopyfile` syscall that `cp` uses, which is what triggers the deadlock. This works even when `osascript -e 'do shell script \"python3 ...\"'` also fails with EDEADLK.

**Pitfall:** `cp` to /tmp fails with `fcopyfile failed: Resource deadlock avoided`. Always use `cat <src> > /tmp/<dest>` instead of `cp <src> /tmp/<dest>`.

## Writing files (write-back to iCloud)

For **writing** back to iCloud-synced files, the working pattern is:

1. Write a Python script to `/tmp/` using the `write_file` tool
2. Execute it directly: `python3 /tmp/script.py`
3. The script opens the iCloud path directly — this works for writes even when reads fail

```python
# /tmp/update_register.py
with open('/Users/mohamedessa/Documents/.../file.md', 'r') as f:
    content = f.read()
# ... modify content ...
with open('/Users/mohamedessa/Documents/.../file.md', 'w') as f:
    f.write(content)
```

```bash
python3 /tmp/update_register.py
```

This works because macOS's iCloud sync engine allows writes to cloud-stub files (it triggers a local download first), but blocks reads from stubs. The write triggers the download implicitly.

## Fallback: osascript do shell script (when cat > /tmp fails)

On some macOS versions, `cat > /tmp/` also returns EDEADLK. In that case, wrap the Python read/write inside `osascript -e 'do shell script \"python3 /tmp/script.py 2>&1\"'`:

```bash
# Write script to /tmp first (write_file tool), then:
osascript -e 'do shell script \"python3 /tmp/script.py 2>&1\"' 2>&1
```

AppleScript's `do shell script` runs in a different security context than direct shell access. Even when macOS's iCloud sync engine has locked the file for direct access, the AppleScript bridge can sometimes still read/write it.

**Pitfall:** The osascript bridge can also fail with EDEADLK on some macOS versions. When it does, fall back to the `cat > /tmp/` redirect approach.

## Workarounds Summary (ordered by reliability)

| Method | Read | Write | Notes |
|--------|------|-------|-------|
| `brctl download` + `cat <src> > /tmp/<dest>` | ✅ Best | N/A | Use `cat >` not `cp` — avoids fcopyfile deadlock |
| `python3 /tmp/script.py` (write_file + execute) | ❌ Fails | ✅ Best | Writes trigger implicit iCloud download |
| `osascript -e 'do shell script \"python3 ...\"'` | ⚠️ Sometimes | ⚠️ Sometimes | Fails on some macOS versions |
| `brctl download` + `cp` | ❌ Fails | ❌ Fails | `cp` uses fcopyfile which deadlocks |
| `cat <src> > /tmp/x && mv /tmp/x <dest>` | OneDrive only | OneDrive only | iCloud produces 0-byte output |
| `rm -f <target> && cp /tmp/source <target>` | Medium | Medium | Delete first to release lock, then copy |

## Detection

```bash
# Check if file is an iCloud stub
mdls -name com_apple_provenance_isDownloaded <path>
# Check if file is fully local
stat -f "%Sf" <path>  # "-" = local, "d" = dataless stub
```

## Pattern for Cron Jobs

When a cron job needs to read/write register files in `~/Documents/`:

1. Write all processing logic to `/tmp/script.py` using the `write_file` tool
2. Execute via: `osascript -e 'do shell script "python3 /tmp/script.py 2>&1"' 2>&1`
3. The script reads/writes the iCloud path directly — the osascript bridge handles the lock
4. No need for `brctl download` or other pre-flight checks
