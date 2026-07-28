# Two-Pass Routing Pattern

When extracting 20+ email attachments in a single scan, use a two-pass approach to handle both current-session and stranded files from prior cycles.

## Pass 1 — Primary Routes

Write a Python script with explicit `(filename, destination_dir)` tuples for every document you extracted this session. Use `shutil.copy2()` for OneDrive-safe copying.

```python
ROOT = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum"
STAGING = "/tmp/email_attachments"

def clean_filename(fname):
    return re.sub(r'^\d+_', '', fname)

def route_file(src, dst_dir, dst_name=None):
    if not os.path.exists(src):
        return False
    if dst_name is None:
        dst_name = clean_filename(os.path.basename(src))
    dst = os.path.join(dst_dir, dst_name)
    os.makedirs(dst_dir, exist_ok=True)
    if os.path.exists(dst):
        base, ext = os.path.splitext(dst_name)
        dst = os.path.join(dst_dir, f"{base}_dup{ext}")
    shutil.copy2(src, dst)
    return True

routes = [
    ("49393_MOC-MUS-ASE-1K0-ZD-0086 Rev.01 Reply.pdf",
     f"{ROOT}/04_Docs/02_Plans_and_Procedures/02.2_Project_Execution_Plan/02_CG_Responses"),
    # ... one tuple per file
]
```

## Pass 2 — Stranded Cleanup

After Pass 1, list remaining non-image files in staging:

```bash
ls -la /tmp/email_attachments/ | grep -v "\.jpeg\|\.jpg\|\.png\|\.gif\|\.eml"
```

These are files from previous scan cycles that missed routing (wrong ROOT, missing pattern, etc.). Write a second script routing them to correct destinations. This keeps the primary script clean and session-specific.

## When to Use

- **Primary script**: session-specific, one route per file extracted this cycle
- **Stranded script**: cumulative, routes orphaned files from any prior cycle
- Both scripts share the same `route_file()` helper and `ROOT` constant

## Pitfall — Sibling subagent overwrites

If a sibling subagent modifies the routing script concurrently, `write_file` overwrites without merging. Read the file first, or use a unique temp path per session (e.g. `/tmp/route_attachments_{timestamp}.py`).
