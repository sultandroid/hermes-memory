# Single-File HTML Web App Pitfalls

## JSON-in-HTML regex truncation

When editing a single-file HTML app that embeds JSON in a `<script>` tag on one line:

```javascript
const RISK = {"project":"...","risks":[...]};\n
// rest of JS code follows...
```

**DO NOT** use regex like `r'(const RISK = )({.*?})(;\s*$)'` with `re.MULTILINE` to extract the JSON. In MULTILINE mode, `$` matches end-of-line (the `\n` after `};`), so everything after that line (the rest of JS, `</script>`, `</body>`, `</html>`) is discarded when you reconstruct the file.

**Safe approach — use json.dumps() to replace the parsed data only:**

```python
import json, re
with open('index.html') as f:
    content = f.read()

# Find the full RISK assignment line
m = re.search(r'(const RISK = )({.*?})(;?\n)', content, re.DOTALL)
prefix = m.group(1)    # "const RISK = "
old_json = m.group(2)  # the JSON object
suffix = m.group(3)    # ";\n" or similar

# Parse, modify, re-serialize
data = json.loads(old_json)
data['risks'].append(new_risk)
new_json = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

# Replace ONLY the JSON part, keep everything else
new_content = content[:m.start(2)] + new_json + content[m.end(2):]
```

This replaces the JSON string in-place without touching the surrounding HTML/CSS/JS.

## Deployment: post-commit hooks overwrite SCP

The aseer-museum-pm repo has a `.git/hooks/post-commit` that rebuilds and deploys register web apps. After a `git push`, the hook fires and can overwrite files you just SCP'd to the server.

**Workarounds:**
1. Disable the hook temporarily: `chmod -x .git/hooks/post-commit`
2. Or deploy via the repo's own build/deploy mechanism instead of SCP
3. Or commit the locally-fixed file first (so the hook deploys your version), then push

## Multi-register deployment locations

```
Public:  samaya-factory.com/build/aseer/registers/{Reg}/index.html
Alt:     samaya-factory.com/technical-office/aseer/registers/{Reg}/index.html
```

Always verify the server file MD5 matches local after deploy:
```bash
MD5_LOCAL=$(md5 -q local.html)
MD5_REMOTE=$(ssh -p 65002 server "md5sum remote.html" | awk '{print $1}')
if [ "$MD5_LOCAL" = "$MD5_REMOTE" ]; then echo "MATCH"; else echo "MISMATCH"; fi
```

## Toolbar content (user preference)

Only **RESET** and **DOWNLOAD SNAPSHOT** buttons in the top toolbar. No CSV, no PRINT. These were removed by user request on 2026-07-26 across all 4 register pages.
