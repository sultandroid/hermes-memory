# iCloud EDEADLK Workaround for Cron Jobs

## Problem

Files in `~/Documents/` (iCloud Drive-synced) return `OSError: [Errno 11] Resource deadlock avoided` on any read attempt — `open()`, `cat`, `head`, `cp`, `python3 open()`, even after `brctl download` reports the file is local.

This affects cron jobs that need to read/write register files in iCloud-synced project directories.

## Reliable Workaround: brctl download + cat > /tmp (PRIMARY)

The most consistently reliable method for **reading** iCloud-synced files in `~/Documents/`:

```bash
# Step 1: Force iCloud to sync the file locally
brctl download ~/Documents/Asher_Regional_Museum_Document_Control/01_Registers/submittal_register.md

# Step 2: Wait for sync — 2s is often NOT enough for large or cold-stub files
sleep 5

# Step 3: Verify the file is actually local before trying to read
stat -f "%Sf" ~/Documents/.../file.md
# Output must be "-" (local). If "dataless" or "compressed,dataless", repeat step 1+2.

# Step 4: Copy to /tmp using shell redirect (NOT cp — cp uses fcopyfile which deadlocks)
cat ~/Documents/.../file.md > /tmp/file.md

# Step 5: Read from /tmp with normal tools
cat /tmp/file.md
```

The `cat > /tmp/` redirect bypasses the `fcopyfile` syscall that `cp` uses, which is what triggers the deadlock. This works even when `osascript -e 'do shell script \"python3 ...\"'` also fails with EDEADLK.

**Pitfall: `brctl download` may need multiple attempts.** A single `brctl download` + `sleep 2` often leaves the file as `dataless`. The sync engine needs more time or a second trigger. Always verify with `stat -f "%Sf"` before attempting to read. If still dataless, retry `brctl download` + `sleep 5`.

**Pitfall: `cat > /tmp/` may produce 0-byte output** if the file is still a cloud stub (dataless). The redirect silently succeeds but writes nothing. Always check `wc -c /tmp/file.md` after the copy. If 0 bytes, the file wasn't fully local — retry `brctl download` with longer sleep.

**Pitfall:** `cp` to /tmp fails with `fcopyfile failed: Resource deadlock avoided`. Always use `cat <src> > /tmp/<dest>` instead of `cp <src> /tmp/<dest>`.

## Writing files (write-back to iCloud)

For **writing** back to iCloud-synced files, three patterns exist, ordered by reliability:

### Pattern 1: Hermes `write_file` tool (BEST — use first)

The Hermes built-in `write_file` tool is the **only** method that consistently writes to iCloud Drive paths when everything else fails (cat >, cp, python3 open(), osascript bridge all hit EDEADLK). It bypasses the iCloud sync engine lock entirely.

```python
# In your direct tools (not via terminal):
write_file(path="/Users/mohamedessa/Documents/.../file.md", content="...file content...")
```

✅ No `brctl download` needed. ✅ No `rm -f` first. ✅ Works even when the file is a cold stub.
**This is the approved pattern for cron jobs that need to update iCloud-synced register files.**

### Pattern 2: Python script via terminal (fallback — unreliable)

1. **First, force the file local** — writes to cold stubs also fail with EDEADLK:
   ```bash
   brctl download ~/Documents/.../file.md
   sleep 5
   stat -f "%Sf" ~/Documents/.../file.md  # must be "-"
   ```

2. Write a Python script to `/tmp/` using the `write_file` tool

3. Execute it directly: `python3 /tmp/script.py`

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

**Pitfall: writes to cold stubs fail.** The claim that "writes trigger implicit iCloud download" is false for cold (compressed+dataless) stubs. The `open()` for reading raises `OSError: [Errno 11] Resource deadlock avoided`. Always run `brctl download` + verify with `stat -f "%Sf"` before attempting any Python read/write on iCloud files.

### Pattern 3: Delete + Write (LAST RESORT — corrupts files)

```bash
rm -f /path/to/icloud/file.md
# Wait for iCloud to release the lock (2-3s)
write_file(path="/path/to/icloud/file.md", content="...")
```

**⚠️ DANGER: `rm -f` + `cp` produces 0-byte stubs.** Deleting an iCloud file and then using `cp` or `cat >` to recreate it leaves the file as a 0-byte (or 135-byte) stub. The iCloud sync engine catches the `rm` event and re-creates a placeholder before the write completes. Only use `write_file` after `rm -f` — the Hermes tool writes atomically and the sync engine does not interfere.

### Pattern 4: `rm -f` + `cat >` (DANGEROUS — DO NOT USE)

```bash
rm -f /path/to/icloud/file.md
sleep 2
cat /tmp/source.md > /path/to/icloud/file.md
```

**❌ CORRUPTS FILES.** iCloud re-creates the file as a 0-byte stub between the `rm` and the `cat >`. The resulting file is empty or truncated. This was observed in production — a 16KB register file became 135 bytes.

### Verification

After writing via any method, the file may still be a cold stub that `cat`/`head` can't read. Verify with `stat`:
```bash
ls -la /path/to/icloud/file.md
```
If the file shows the expected size (e.g., 16018 bytes), the write succeeded even if `cat` returns nothing due to iCloud sync lag.

**Pitfall: `read_file` tool dedup quirk.** After writing, the `read_file` tool may return "unchanged" (cached from a read earlier in the same session). Use `terminal` with `head` or `ls -la` to verify writes instead — the file on disk is actually updated even if `read_file` says unchanged.

## Workarounds Summary (ordered by reliability)

| Method | Read | Write | Notes |
|--------|------|-------|-------|
| `write_file` tool (Hermes built-in) | ✅ Best | ✅ Best | Only method that works on cold stubs. No `brctl download` needed. |
| `osascript -e 'do shell script "rm -f /tmp/dest && cp /path/to/icloud/src /tmp/dest"'` | ✅ Best | N/A | **NEW: Most reliable read pattern.** `rm -f` on the /tmp destination first releases any lock, then `cp` from iCloud source works. Verified working on macOS 26.5.2. |
| `osascript -e 'do shell script "rm -f /path/to/icloud/dest && cp /tmp/source /path/to/icloud/dest"'` | N/A | ✅ Works | **NEW: Reliable write pattern.** `rm -f` on the iCloud destination releases the sync engine lock, then `cp` from /tmp source succeeds. Verified: 16KB register files written correctly. |
| `brctl download` + `cat <src> > /tmp/<dest>` | ✅ Works | N/A | Use `cat >` not `cp` — avoids fcopyfile deadlock. Verify with `stat -f \"%Sf\"` first. May produce 0-byte output if file is still a cold stub. |
| `brctl download` + `python3 /tmp/script.py` | ✅ Works | ✅ Works | Must `brctl download` + verify local first. Writes to cold stubs also fail. |
| `osascript -e 'do shell script \"python3 ...\"'` | ⚠️ Sometimes | ⚠️ Sometimes | Fails on some macOS versions |
| `brctl download` + `cp` | ❌ Fails | ❌ Fails | `cp` uses fcopyfile which deadlocks |
| `cat <src> > /tmp/x && mv /tmp/x <dest>` | OneDrive only | OneDrive only | iCloud produces 0-byte output |
| `rm -f <target> && cp /tmp/source <target>` (direct shell, no osascript) | ❌ Fails | ❌ Fails | Direct shell `cp` after `rm -f` still deadlocks. Must go through `osascript -e 'do shell script'` bridge. |

## Detection

```bash
# Check if file is an iCloud stub
mdls -name com_apple_provenance_isDownloaded <path>
# Check if file is fully local
stat -f "%Sf" <path>  # "-" = local, "d" = dataless stub
```

## New Pattern: `com.apple.provenance` xattr + `compressed,dataless` flag

On macOS 26.5.2, iCloud-synced files in `~/Documents/` can have a **persistent `com.apple.provenance` extended attribute** that survives `xattr -d` and `xattr -c` removal attempts. The file shows as `compressed,dataless` in `ls -laO` output. When this flag is present:

- **ALL read methods fail:** `cat`, `head`, `cp`, `ditto`, `rsync`, `python3 open()`, `osascript -e 'do shell script "cat > /tmp/"'`, `perl -e 'open()'`, `dd`, `od`, `strings` — all return `Resource deadlock avoided`
- **`xattr -d` and `xattr -c` appear to succeed** (exit 0) but the attribute is immediately re-applied by the iCloud sync engine
- **`brctl download` + `sleep 5` does NOT resolve it** — the file remains `compressed,dataless` even after `brctl download` reports success
- **`mv` (rename) succeeds** — renaming the file breaks the iCloud sync lock, but the renamed file (.bak) is ALSO locked because iCloud has already indexed the new name
- **The only reliable read path:** `mv <file> <file>.bak` → `brctl download <file>.bak` → `sleep 5` → `cat <file>.bak > /tmp/<file>` — the rename breaks the sync engine's lock, `brctl download` forces local sync of the renamed file, and `cat > /tmp/` avoids `fcopyfile` deadlock

### Detection of this state

```bash
# Check for the persistent xattr
xattr -l <path>  # shows com.apple.provenance
# Check for compressed,dataless flag
ls -laO <path>   # shows "compressed,dataless" in the flags column
# Try to read
cat <path>       # returns "Resource deadlock avoided"
```

### Workaround for this specific state

```bash
# Step 1: Rename to break iCloud sync lock
mv /path/to/file.md /path/to/file.md.bak

# Step 2: Force iCloud to sync the renamed file
brctl download /path/to/file.md.bak
sleep 5

# Step 3: Copy to /tmp using shell redirect (avoids fcopyfile)
cat /path/to/file.md.bak > /tmp/file.md

# Step 4: Read from /tmp
cat /tmp/file.md

# Step 5: Restore original name
mv /path/to/file.md.bak /path/to/file.md
```

**Pitfall: Step 5 (restore) may re-lock the file.** After restoring the original name, the file may again be `compressed,dataless` with the `com.apple.provenance` xattr. This is expected — the iCloud sync engine re-applies the flag. The content is preserved on disk; it just can't be read again until the next rename cycle.

**Pitfall: `xattr -c` (clear all) does NOT work.** Even after `xattr -c` reports success, the `com.apple.provenance` attribute is immediately re-applied by the sync engine. Do not rely on xattr removal as a workaround.

**Pitfall: `chflags nouchg` does NOT help.** The `compressed,dataless` flag is not a user-controllable flag — it's managed by the iCloud sync engine. `chflags` operations have no effect on it.

**Pitfall: `patch` tool also fails on `compressed,dataless` files.** The `patch` tool internally reads the file before applying edits, so it also hits EDEADLK on this state. Use the `mv` + `brctl download` + `cat > /tmp/` workaround to read, then `write_file` to write back.

## Pattern for Cron Jobs

When a cron job needs to read/write register files in `~/Documents/`:

1. **Force files local first** — both reads and writes fail on cold stubs:
   ```bash
   brctl download ~/Documents/.../file.md
   sleep 5
   stat -f "%Sf" ~/Documents/.../file.md  # must be "-"
   # If still dataless, retry brctl download + sleep 5
   ```

2. Write all processing logic to `/tmp/script.py` using the `write_file` tool

3. For reading: `cat <src> > /tmp/<dest>` — the shell redirect avoids `fcopyfile` deadlock. Verify with `wc -c /tmp/<dest>` (0 bytes = still a stub).

4. For writing: execute `python3 /tmp/script.py` — the Python `open()` works once the file is local.

5. **Do NOT use `osascript -e 'do shell script "python3 ..."'`** as the primary bridge — it also fails with EDEADLK on some macOS versions. Use `cat > /tmp/` for reads and direct `python3 /tmp/script.py` for writes instead.

6. **Do NOT use `cp`** to copy from iCloud — it uses `fcopyfile` which deadlocks on cloud stubs.

7. **`read_file` tool dedup quirk:** After writing via `python3 /tmp/script.py`, the `read_file` tool may return "unchanged" (cached from earlier read in the same session). Use `cat` or `terminal` to verify writes instead — the file on disk is actually updated even if `read_file` says unchanged.
