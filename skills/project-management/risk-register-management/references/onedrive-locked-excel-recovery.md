# OneDrive-Locked Excel Recovery Playbook

> Reference for `risk-register-management` (and any other skill that touches OneDrive-stored XLSX/DOCX files).

## Symptom

The canonical master register file (e.g. `Aseer_Museum_Risk_Register_C11.xlsx`) returns `Resource deadlock avoided` on every read attempt. The file:

- Has non-zero size (e.g. 80 KB) but `unzip -l` fails with "End-of-central-directory signature not found"
- `openpyxl.load_workbook()` raises `BadZipFile: File is not a zip file`
- Multiple retries with `sleep 5-30` between them still deadlock
- `brctl status` shows `SYNC DISABLED (app not installed)` for the parent folder
- `cp` produces a 0-byte file in `/tmp/` (silent corruption — never trust that copy)

## Root cause

macOS OneDrive client holds the file with a kernel-level lock that the agent's read attempts can't bypass. The on-disk bytes are a placeholder stub, not the real xlsx content. The cloud copy may be fine — it's the local sync that's broken.

## Recovery — in order of preference

1. **Ask the user to drop the file in chat.** The Hermes attachment pipeline extracts it to `~/.hermes/cache/documents/`. The cached copy is always clean and readable. **This is the fastest reliable path.**
2. **Read directly with openpyxl from the OneDrive path** with `read_only=True, data_only=True`. Sometimes works when `cp` doesn't. If it raises `BadZipFile`, fall back to step 1.
3. **Check `brctl status`** to see if the parent folder is `SYNC DISABLED`. If so, only the user can re-hydrate via Finder right-click → "Always keep on this device". No agent path can fix this.
4. **Wait 30-60 s and retry.** Sometimes OneDrive releases. Don't retry more than 3 times in a row — if 3 retries fail, switch to step 1.
5. **Read the PDF mirror** via `pdftotext -layout`. The PDF is often readable when the DOCX isn't, and the textual content is the same. Use this for read-only inspections.
6. **Stage the read result to a safe project location** (`06_Risk_System/source/C<rev>_reference/`) so the agent has a clean copy for downstream scripts. Always add a `README.md` indexing what's in the folder and when it was staged.

## Hard rules

- **Never write back to a OneDrive file the agent can't read.** The write will silently produce a 0-byte stub and corrupt the user's cloud copy. Once that happens, the next sync overwrites the cloud too.
- **Never trust a `cp` that produces a 0-byte file.** Check `ls -la` after every copy from OneDrive. If the file is 0 bytes, the read failed silently and the file is gone.
- **Never loop-retry more than 3 times.** If `cp`/`openpyxl`/`textutil` all deadlock on the same file, the lock is structural. Move to a different recovery path or stop and tell the user.

## OneDrive-side recovery (requires user action)

If the user wants to fix the lock at source:

1. Open Finder, navigate to the stuck folder
2. Right-click the file → "Always keep on this device" (forces full download)
3. Wait for the blue cloud icon in Finder to become a green checkmark
4. Verify with `unzip -l` that the file is now a valid zip

This is the only path that re-hydrates a `SYNC DISABLED` folder.
