# OneDrive File Provider — Programmatic Writes Fully Blocked (macOS)

## Symptom
Every programmatic write into a OneDrive-synced folder fails with `Operation not
permitted` / Finder error `-8004` ("The operation can't be completed"):

- `cp`, `ditto`, `mv`, `python os.sendfile`, `shutil.copy2`, `cat > file` — all `Operation not permitted`
- Finder AppleScript `duplicate` / `move` — error `-8004`
- `mkdir` of a new subfolder inside a OneDrive tree — `Operation not permitted`
- OneDrive processes holding the DB do NOT explain it; even with all OneDrive
  processes killed the block persists (the File Provider extension re-launches).

Root cause: macOS **File Provider extension** (OneDrive.appex) enforces that writes
go through the sync client, not direct filesystem writes. There is no shell/API
bypass. Permissions look normal (owner `mohamedessa`, mode 700) — that's a trap;
the block is at the File Provider layer, not POSIX perms.

## The working pattern
1. Stage/organize files on a NON-OneDrive volume first — this machine uses
   `/Volumes/MIcro/Temp/` (e.g. `/Volumes/MIcro/Temp/PQ_Documents_Filed/`).
   All normal `cp`/`mkdir`/extraction works there.
2. `open` BOTH the staged folder AND the target OneDrive folder in Finder so the
   user sees both windows.
3. User does the **manual Finder drag-and-drop** from the staged folder into the
   OneDrive folder. Only manual drag works. This is an expected handoff, not a failure.

## Why the old "copy to Micro first" advice is NOT enough
The older "copy to Micro first to avoid EDEADLK" workflow only fixed *reading* large
files. Writing *into* the OneDrive tree is a separate, harder block requiring the
manual-drag handoff. Keep Micro staging (it works for both), but do NOT attempt
programmatic writes into the OneDrive tree at all — go straight to staging + user drag.

## Good practice
- Always ship a `_FILE_MAPPING.csv` (or `.md`) beside the staged files showing each
  file's destination folder, so the drag step is mechanical and auditable.
- Do all text-extraction / PDF→text / reading from the staged copy, not the OneDrive tree.
