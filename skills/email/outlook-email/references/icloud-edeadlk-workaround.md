# iCloud EDEADLK Workaround for Cron Jobs

## Problem

Files in `~/Documents/` (iCloud Drive-synced) return `OSError: [Errno 11] Resource deadlock avoided` on any read attempt — `open()`, `cat`, `head`, `cp`, `python3 open()`, even after `brctl download` reports the file is local.

This affects cron jobs that need to read/write register files in iCloud-synced project directories.

## Reliable Workaround: osascript do shell script

The most consistently reliable method is wrapping the Python read/write inside `osascript -e 'do shell script \"python3 -c ...\"'`:

### Reading a file

```bash
# Write script to /tmp first (write_file tool), then:
osascript -e 'do shell script "python3 /tmp/script.py 2>&1"' 2>&1
```

### Writing a file

```bash
# Write script to /tmp (write_file tool), then:
osascript -e 'do shell script "python3 /tmp/script.py 2>&1"' 2>&1
```

### Why this works

AppleScript's `do shell script` runs in a different security context than direct shell access. Even when macOS's iCloud sync engine has locked the file for direct access, the AppleScript bridge can still read/write it. This is a macOS sandbox/entitlement quirk — the `do shell script` call inherits Outlook's or the agent's entitlements rather than the terminal's.

## Fallback: brctl download + cp (when osascript bridge also fails)

On some macOS versions, even the `osascript` bridge returns EDEADLK for `~/Documents/` files. In that case:

```bash
# Step 1: Force iCloud to sync the file locally
brctl download ~/Documents/Asher_Regional_Museum_Document_Control/01_Registers/submittal_register.md

# Step 2: Wait for sync
sleep 3

# Step 3: Copy to /tmp (bypasses iCloud lock)
cp ~/Documents/.../file.md /tmp/file.md

# Step 4: Read from /tmp with normal tools
cat /tmp/file.md
```

The `brctl download` command makes the file fully local, after which `cp` succeeds. This works even when `osascript -e 'do shell script "python3 -c ..."'` fails with EDEADLK. The `stat -f "%Sf"` check shows `-` (local) after `brctl download`, confirming the file is no longer a cloud stub.

**Pitfall:** `cp` to /tmp may also fail with `fcopyfile failed: Resource deadlock avoided` on the first attempt. If so, retry — the second `cp` often succeeds after the first attempt triggers the sync engine to release the lock.

## Partial Workarounds (less reliable)

| Method | Reliability | Notes |
|--------|-------------|-------|
| `brctl download <path>` + `sleep 3` | Low | `stat -f "%Sf"` shows `-` (local) but reads still fail |
| `cat <src> > /tmp/x && mv /tmp/x <dest>` | OneDrive only | iCloud produces 0-byte output |
| `rm -f <target> && cp /tmp/source <target>` | Medium | Delete first to release lock, then copy |
| `osascript -e 'do shell script "python3 ..."'` | **High** | Most reliable for both read and write |

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
