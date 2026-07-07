# Patching Deployed Minified JS (When Rebuild Is Blocked)

## When to Use This

The build toolchain (Vite/Rollup/webpack) is broken or incompatible with the local Node.js version, AND you only need to change a small data/config section inside the compiled JS bundle — not logic or imports.

**Do NOT use this for:** logic changes, component re-renders, imports, or anything that needs a compiler pass (TypeScript → JS).

## Technique

### 1. Download the JS bundle from the live server

```bash
curl -s "https://example.com/assets/index-abc123.js" -o /tmp/bundle.js
```

### 2. Find your target section using Python bracket matching

Minified JS is one line. `grep` can locate the section start, but finding the exact end requires depth counting:

```python
with open('/tmp/bundle.js', 'r') as f:
    content = f.read()

start = content.find('myConfigKey:[{')
if start < 0:
    start = content.find('"myConfigKey":[{')  # try with quotes

# Bracket-match to find end
depth = 0
found_start = False
end = start
for i in range(start, min(start + 5000, len(content))):
    c = content[i]
    if c == '[':
        depth += 1
        found_start = True
    elif c == ']':
        depth -= 1
        if found_start and depth == 0:
            end = i
            break

old_section = content[start:end+1]
print(f"Section: {len(old_section)} chars at {start}-{end}")
```

### 3. Build the replacement string

Must be **syntactically identical** to the original context. In minified JS:
- `true` becomes `!0` (because `!0` = `!false` = `true`)
- `false` becomes `!1`
- Object keys are unquoted (JSON-like but JS, not JSON)
- No trailing commas

```python
new_section = 'myConfigKey:[{label:"Name",fields:[{key:"Field",label:"Field"}]}]'

new_content = content[:start] + new_section + content[end+1:]
```

### 4. Verify the patched file

```python
# Quick sanity checks
assert key_check in new_content, "Lost expected content!"
assert removed_content not in new_content, "Old content still present!"
assert len(new_content) > len(content) * 0.8, "File too short (truncation)"
```

### 5. Test locally

Load the patched JS in a browser's DevTools → Sources → Overrides to verify it parses without syntax errors before uploading.

A quick syntax check:
```bash
node -e "require('fs').readFileSync('/tmp/patched.js','utf8'); console.log('Readable')"
# This only checks the file can be read, not JS syntax.
# For JS syntax checking: node --check /tmp/patched.js
```

**NOTE:** `node --check` may not work on a browser-bundled module file that uses `import` statements. The safest test is loading it in a browser.

### 6. Upload and backup

```bash
# Backup first
ssh host "cp /path/to/bundle.js /path/to/bundle.js.bak"

# Upload
scp /tmp/patched.js host:/path/to/bundle.js
```

### 7. Verify the live site after upload

```bash
curl -s "https://example.com/" | grep -q "expected string"
# AND check HTTP 200
curl -s -o /dev/null -w "%{http_code}" "https://example.com/"
```

## 🔴 Critical Pitfalls

### The replacement MUST be syntax-perfect

A single wrong character in minified JS can crash the entire app with a silent syntax error. The module script won't load, the `<div id="root">` stays empty, no error visible in console.

**Common mistakes that break everything:**
- Using JSON syntax (quoted keys) where JS object literal syntax (unquoted keys) is expected
- Adding/removing a comma — minified JS is comma-sensitive
- Using JS `true` instead of `!0` (or vice versa)
- Mismatched bracket depth in the replacement
- Special characters like `!` being interpreted by the shell/Python string

### Always backup before modifying

```bash
cp bundle.js bundle.js.bak
# Before any patch attempt
```

### If the page breaks after upload

```bash
# Restore from backup
ssh host "cp /path/to/bundle.js.bak /path/to/bundle.js"
```

### Browser caching may mask the issue

After uploading a broken file, the browser may serve the old cached version. Hard refresh (Cmd+Shift+R) or cache-busting query param (`?v=N`) is needed to see the broken state. Always test in an incognito window or with DevTools → Network → Disable Cache.

## Example Workflow

```bash
# 1. Download
curl -s "https://site.com/assets/index-abc.js" -o /tmp/orig.js

# 2. Python patch (bracket matching + replace)
python3 << 'PYEOF'
with open('/tmp/orig.js') as f: c = f.read()
s = c.find('config_key:[{')
d = 0; f = False; e = s
for i in range(s, len(c)):
    if c[i]=='[': d+=1; f=True
    elif c[i]==']': d-=1
    if f and d==0: e=i; break
new = 'config_key:[{new config here}]'
with open('/tmp/patched.js','w') as f: f.write(c[:s] + new + c[e+1:])
PYEOF

# 3. Backup + Upload
ssh host "cp /path/index.js /path/index.js.bak"
scp /tmp/patched.js host:/path/index.js

# 4. Verify
curl -s "https://site.com/" | head -5
```

## When NOT to Use This

- Logic changes require a rebuild — you can't patch functions/imports this way
- The build issue is fixable (wrong Node version, missing dep, corrupted node_modules) → fix the build instead
- The change touches many sections → rebuild is safer and less error-prone
