# AppleScript on macOS — File-Based vs Inline Scripts

## Lesson from Session (May 28, 2026)

When building the BIM Email Pipeline, we discovered that **inline AppleScript via `-e`** is unreliable for complex multi-line scripts. macOS `osascript` would choke on syntax it couldn't parse within `-e` strings, especially when they contained special characters, raw Python strings, or multi-line `on run argv` handlers.

## The Fix: File-Based .applescript Scripts

Instead of embedding AppleScript in Python raw strings:

```python
# ❌ DON'T: Inline via -e (fragile, syntax errors)
proc = subprocess.run(["osascript", "-e", long_complex_script, "--", arg1, arg2])

# ✅ DO: File-based .applescript
proc = subprocess.run(["osascript", script_path, arg1, arg2])
```

### Benefits

| Aspect | Inline `-e` | File-based `.applescript` |
|--------|-------------|--------------------------|
| Syntax checking | Runtime only | Compile-time (Script Editor can validate) |
| Special chars | Must escape for both Python + AppleScript | Just AppleScript |
| Multi-line | Fragile with r''' strings | Natural |
| Debugging | Impossible to inspect | Open in Script Editor |
| Reliability | Broke with >50 lines | Stable at any length |

### Implementation Pattern

```python
# 1. Write the .applescript file
# 2. Pass args as separate command-line args (not interpolated)
# 3. AppleScript accesses them via `item N of argv`
# 4. No escaping needed — subprocess handles quoting

FETCH_SCRIPT_PATH = "~/.hermes/scripts/bim_fetch_emails.applescript"

def run_osascript(script_path, args, timeout=120, retries=2):
    cmd = ["osascript", script_path]
    if args:
        cmd.extend(args)
    for attempt in range(1, retries + 2):
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            if proc.returncode == 0:
                return proc
        except subprocess.TimeoutExpired:
            pass  # retry with backoff
        time.sleep(2 ** attempt)
    return None
```

### AppleScript Argument Passing

Arguments passed as separate CLI args to `osascript script.applescript arg1 arg2` are available in AppleScript as:

```applescript
on run argv
    set val1 to item 1 of argv  -- "arg1"
    set val2 to item 2 of argv  -- "arg2"
end run
```

No need to escape quotes or special characters — `subprocess.run` with a list handles this safely.

### When to Keep Inline

Inline `-e` is fine for **one-liners**:

```bash
osascript -e 'tell app "Microsoft Outlook" to get name of every mail folder'
```
