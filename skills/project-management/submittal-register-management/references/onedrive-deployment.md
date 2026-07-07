# Deploying xlsx to OneDrive

## Safe method (use this by default)
Stage to `/tmp/`, then use AppleScript Finder duplicate:
```bash
osascript -e '
tell application "Finder"
    set src to POSIX file "/tmp/filename.xlsx"
    set destFolder to POSIX file "/Users/.../OneDrive-PATH/folder/"
    duplicate src to destFolder with replacing
end tell
'
```

## Fast method (small files only)
Direct `cp` for small xlsx files (<100KB), then verify:
```bash
cp /tmp/filename.xlsx "/Users/.../OneDrive-PATH/folder/"
xxd -l 8 "/Users/.../OneDrive-PATH/folder/filename.xlsx" | head -1
# Should start: 504b0304 = PK\x03\x04 (ZIP header)
```

## Deploying .py scripts
Direct `cp` to scripts/ folder is safe (Python files are not ZIP-based):
```bash
cp /tmp/script.py /Users/.../scripts/
```

## Verification
Always verify after OneDrive copy:
```python
import openpyxl
wb = openpyxl.load_workbook(oneDrive_path)
ws = wb.active
# Check headers
hdrs = [str(ws.cell(row=1, column=c).value or '') for c in range(1, 10)]
assert 'Submittal' in hdrs[1], f"Description column missing! Headers: {hdrs}"
wb.close()
```
