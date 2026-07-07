# `ditto` Workaround for iCloud Drive Dataless Files

Confirmed: 2026-06-06 during automated cron pipeline run.

## Problem

iCloud Drive files under `~/Documents/Documents - Mohamed's MacBook Pro/` are stored as `compressed,dataless` APFS placeholders. These cannot be read by `cat`, `cp`, `dd`, Python `open()`, `read_file`, or even `brctl download` (which returns `Error Domain=NSCocoaErrorDomain Code=257` permission errors when called from an automated/cron context where the full user session isn't available).

## The Workaround

```bash
ditto "/path/to/dataless/file.md" /tmp/file.md
cat /tmp/file.md   # now readable
```

**Why it works:** `ditto` uses `copyfile()` with COPYFILE_DATA flag, which macOS's APFS `fileprovi` hydration engine handles differently than the standard POSIX `read()` syscall used by `cat` and most tools. Small state files (<10KB) hydrate quickly; larger archives may not.

## Detection

```bash
# Check if a file is dataless (cloud-only placeholder)
stat -f "%N %z %Sf" <file>
# Output: "file.md 4630 compressed,dataless"  → cloud-only
# Output: "file.md 4630 -"                     → fully local, readable
```

## Priority Order for Reading iCloud Drive Dataless Files

1. **`ditto <src> /tmp/`** — best chance. Try first.
2. **`python3 <script>`** — only for `.py` scripts (confirmed working Jun 6 because Python's import path bypasses fileprovi)
3. **`brctl download <path>`** — may fail with permission errors from non-GUI contexts
4. **`NSFileCoordinator` (Swift)** — **Ultimate fallback.** When all POSIX workarounds fail, use Apple's `NSFileCoordinator` API to read via the `fileprovi` coordination path. See `references/nsfilecoordinator-workaround.md` for the full Swift template. Proven Jun 10, 2026 on 32 iCloud dataless files.
5. If all fail: log as sync-blocked and proceed

## Comparison with OneDrive Lock Pattern

| Feature | iCloud Drive | OneDrive |
|---------|-------------|----------|
| Lock symptom | `compressed,dataless` flag | `Resource deadlock avoided` |
| `brctl download` | Permission errors (non-GUI) | Works (may need retry) |
| `ditto` workaround | **Works** (confirmed Jun 6) | Does NOT work |
| `read_file` tool | Does NOT work | **Works** |
| Files affected | `Documents - Mohamed's MacBook Pro/04_Outlook_Connection/` | `OneDrive-SAMAYAINVESTMENT/Bim Unit/` |
