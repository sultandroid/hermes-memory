# Deployed JS Verification — Stale Build Detection

## When to Use

- Source code config (e.g. `SCHEDULE_FIELD_GROUPS`) looks correct but the UI on the live site shows different fields
- User reports dimensions/fields appearing that were already removed from source
- Any "it should work but it doesn't on production" scenario where source inspection shows the right code

## Technique

### 1. Fetch the deployed JS bundle

```bash
# Find the JS asset URL from the page
# On the deployed page, check <script src="..."> tags
curl -s 'https://your-domain.com/assets/index-*.js' > /tmp/deployed.js
```

### 2. Search for config values

```bash
# Should be present (new config fields)
grep -c 'Climate Control' /tmp/deployed.js

# Should NOT be present (removed config fields)
grep -c 'Ext. Height' /tmp/deployed.js
```

### 3. Extract the full config object (minified JS)

Use `tr ';' '\n'` to split the minified JS into statements, then grep for the config key:

```bash
curl -s 'https://your-domain.com/assets/index-*.js' \
  | tr ';' '\n' \
  | grep 'showcase_schedule' \
  | head -1
```

### 4. Targeted field group parsing (Python)

When the config is an inline object literal (not a separate JSON file), grep alone can be misleading because data values contain the same strings. Use Python to parse the specific config definition block:

```python
# Extract the SCHEDULE_FIELD_GROUPS config block for a specific schedule type
import re
data = open('/tmp/deployed.js').read()

# Find the config object key for showcase_schedule
idx = data.find('showcase_schedule:[{')
if idx >= 0:
    block = data[idx:idx+800]
    has_dims = '"Dimensions"' in block     # group label for dimension section
    has_display = '"Display"' in block      # compact group label
    has_ext_width = 'Ext. Width' in block   # dimension field
    print(f'Dimensions group: {has_dims}')
    print(f'Display group: {has_display}')
    print(f'Ext. Width field: {has_ext_width}')
```

This approach uses positional proximity (finding `showcase_schedule:[{` then scanning the next ~800 chars) to distinguish the config definition from data values that happen to contain the same keys.

### 4. Compare against local built version

```bash
# Local built JS
grep -c 'Climate Control' dist/assets/index-*.js

# Remote deployed JS
curl -s 'https://your-domain.com/assets/index-*.js' | grep -c 'Climate Control'
```

If counts differ, the deployed version is stale — rebuild and redeploy.

## Bonus: Blank Page After Deploy — Three Causes

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| Console shows empty JS exception, page blank | **Three.js import crash** — `import * as THREE` with old three.js + Vite | Fix imports to individual named exports, rebuild |
| Console shows "Script load error" with no detail | **`crossorigin` without CORS headers** — Vite adds `crossorigin` but Hostinger omits `Access-Control-Allow-Origin` | Remove `crossorigin` from script tag in dist/index.html, re-upload |
| Module script fails silently | **Wrong MIME type** — Hostinger serves `.js` as `application/x-javascript` | Remove `type="module"` from script tag (bundle is IIFE), re-upload |

## Common Causes of Stale Builds

| Cause | Symptom | Fix |
|-------|---------|-----|
| `tsc -b` times out on OneDrive JSON files | Build script only runs `vite build` without `tsc` | Run `tsc -b` separately with increased timeout, or skip tsc only when no TS errors |
| Old `dist/` not cleaned | Previously built artifacts survive | `rm -rf dist/` before rebuild |
| Different build pipeline | npm scripts may have changed | Check `npm run build` vs manually invoking `vite build` |
| OneDrive file locks | Source files read as empty during build | Copy project to `/tmp/` and build there |

## Aseer Museum Case Study

**Symptom:** Showcase tooltip cards showed dimension fields (Ext. Width, Ext. Height, Label Height, etc.) even though `SCHEDULE_FIELD_GROUPS` in `Gallery.tsx` only listed Type, ID, Exhibit + Display fields with no dimensions.

**Root cause:** The deployed `index-*.js` contained a verbose 5-group config (Showcase + Dimensions + Specifications + Environment + Hardware sections) with all dimension fields. The local source had the correct compact 2-group config, but the deployed JS was from an older build. The usual `npm run build` (which runs `tsc -b && vite build`) hangs on OneDrive-hosted JSON data files, so the last successful build predated the source change.

**Fix:**
1. **Rebuild** using `node build.mjs` (vite build directly, bypassing tsc):
   ```js
   // build.mjs
   import { build } from 'vite';
   await build({ logLevel: 'info' });
   ```
2. **Incremental deploy** — upload only changed files (not full 47MB tarball):
   ```bash
   scp -P 65002 assets/index-<newhash>.js user@host:/remote/assets/
   scp -P 65002 assets/index-<newhash>.css user@host:/remote/assets/
   scp -P 65002 index.html user@host:/remote/
   scp -P 65002 sync.php user@host:/remote/
   ssh -p 65002 user@host "cd /remote/assets && rm -f ._* *.bak*"
   ```
3. **Verify** by fetching the deployed JS and checking that the "Dimensions" group label and all dimension field keys are absent from the `showcase_schedule` config block.
