# OneDrive Hydration — One-File-at-a-Time Pattern

When OneDrive cloud-only placeholder files (0 blocks on disk, non-zero size) resist batch download, the reliable recovery is opening each file individually in its native app.

## Trigger

- `cp` fails with `fcopyfile failed: Resource deadlock avoided`
- `stat -f "%b %z %N"` shows 0 blocks but non-zero size
- `fileproviderctl evaluate` shows `isDownloaded=0, isDownloading=0`
- Batch approaches (`brctl download`, `fileproviderctl materialize`, `cp` loop) all fail

## The Pattern

```bash
ADEL_DIR="/path/to/OneDrive/folder"

for f in "file1.pdf" "file2.pdf" "file3.pdf"; do
  echo "Opening: $f"
  open -a Preview "$ADEL_DIR/$f"
  sleep 20   # Wait for OneDrive to hydrate
  blocks=$(stat -f "%b" "$ADEL_DIR/$f")
  echo "  Blocks: $blocks"   # Should be > 0 now
done
```

## Why It Works

`open -a Preview` triggers macOS LaunchServices to hand the file to its default handler. When Preview opens and reads the content, OneDrive hydrates the local copy. The `dataless` flag disappears and the file becomes a regular file.

## Critical Details

| Parameter | Value | Why |
|-----------|-------|-----|
| Sleep between files | 15-20 seconds | OneDrive needs time to download before next file |
| Native app | Preview for PDFs | Non-native apps (TextEdit) open blank |
| One file at a time | Never batch | Batch `open` commands queue but don't hydrate |
| Check after each | `stat -f "%b"` | 0 blocks = still placeholder; retry with longer wait |

## After Hydration

Once blocks > 0, the file can be:
- `cp` / `mv` to another location
- Read with `pdftotext`, `cat`, `head`
- Processed with Python (PyMuPDF, pdfminer)

**Note:** Preview stays running after hydration. This is normal — close it or leave it. It doesn't affect subsequent operations.

## When It Still Fails

If `open -a Preview` doesn't hydrate (blocks stay 0 after 30s):
1. The file may be orphaned (`isUploading=1 + isUploaded=0` in `fileproviderctl evaluate`)
2. Check OneDrive web (onedrive.live.com) — the file may not exist in the cloud
3. Recovery requires re-creating the file from source

## See Also

- `references/onedrive-dataless-diagnostics.md` — full diagnostic reference
- `references/incoming-document-triage.md` — processing newly hydrated documents
