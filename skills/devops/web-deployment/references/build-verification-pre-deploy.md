# Pre-Deploy Build Verification Checklist

## Why

Three build-time issues cause deployed-but-broken sites that look correct locally:

1. **Three.js import resolution failure** — Vite warns at build time but still produces a bundle that crashes silently at runtime
2. **Script `crossorigin` + no CORS headers** — `<script crossorigin>` requires `Access-Control-Allow-Origin` that shared hosting doesn't send
3. **Config mismatch** — deployed JS has different config than source (stale build)

## Checklist (run before any deploy)

### 1. Scan build log for Three.js warnings

```bash
npm run build 2>&1 | tee /tmp/build.log
if grep -q 'is not exported by' /tmp/build.log; then
  echo "❌ Three.js import resolution issue — app will crash silently"
  echo "   Fix: change import * as THREE to individual named imports"
  exit 1
fi
```

### 2. Fix script attributes

```bash
# Remove crossorigin (no CORS headers on Hostinger)
sed -i '' 's/ crossorigin//g' dist/index.html
# Remove type="module" (server MIME type rejection)
sed -i '' 's/type="module" //g' dist/index.html
```

The bundle is a single IIFE (no `import`/`export` statements) — it runs fine as a regular script.

### 3. Verify config in built JS

```bash
BUILT_JS=$(ls dist/assets/index-*.js 2>/dev/null | head -1)
if [ -n "$BUILT_JS" ]; then
  # Positive check — expected config present
  grep -q 'Climate Control' "$BUILT_JS" && echo "OK: expected config found" || echo "❌ config missing"
  # Negative check — removed fields absent
  grep -q 'Ext. Height' "$BUILT_JS" && echo "❌ stale dimension field found" || echo "OK: no stale dims"
fi
```

### 4. Check MIME type on server (post-deploy)

```bash
curl -sI "https://domain/assets/$(ls dist/assets/index-*.js | xargs basename)" \
  | grep -i content-type | grep -q 'application/javascript' \
  && echo "OK: JS MIME type correct" \
  || echo "⚠️  Wrong MIME type (may affect module scripts)"
```

## Recovery

If page is blank after deploy:
1. Open browser console — look for silent JS exceptions (no message = Three.js crash)
2. Check if `crossorigin` is on script tag → remove and re-upload index.html
3. Check if `type="module"` is on script tag → remove and re-upload index.html
4. Verify the built JS actually runs: `node -e "eval(require('fs').readFileSync('dist/assets/index-*.js','utf8'))"` — if this fails, the bundle has a syntax issue
