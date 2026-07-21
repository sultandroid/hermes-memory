# Debugging a Blank Register Web App

When a register web app loads but shows empty KPIs, blank table, and no console errors:

## Checklist (in order)

1. **Check server files exist** — `ssh` to server, verify `index.html` is present and non-empty
2. **Check HTML structure** — grep for `<div id="kpis">`, `<div id="catBars">`, `<div id="tbody">` etc. If missing, the build script didn't generate the full page
3. **Check `$` helper** — In browser console: `typeof $` -> if `"undefined"`, the `const $ = s => document.querySelector(s);` line is missing. Add it before `function init()`
4. **Check variable name case** — In browser console: `typeof LESSONS` vs `typeof lessons`. The data is declared as `const LESSONS = [...]` but every function references `lessons` (lowercase). Fix: add `const lessons = LESSONS;` after the data block, or change the declaration to `const lessons = [...]`
5. **Check `init()` was called** — In browser console: `typeof init` -> if `"function"`, call `init()` manually. If `"undefined"`, the script has a syntax error that prevents the function from being defined
6. **Check for JS syntax errors** — In browser console, look for any red error messages. Common: missing comma in JSON array, unclosed template literal, or `const` redeclaration

## Root causes found in production

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Empty page, no errors | `$` helper not defined | Add `const $ = s => document.querySelector(s);` before `init()` |
| Empty page, no errors | `LESSONS` vs `lessons` case mismatch | Add `const lessons = LESSONS;` alias after data block |
| Page loads but no data renders | JSON syntax error in data array | Validate JSON with `JSON.parse(JSON.stringify(LESSONS))` in console |
| Print button does nothing | `window.onafterprint` not `window.addEventListener('afterprint', ...)` | Fix event listener syntax |
| Fix deployed but page still blank | Browser serving cached HTML (server has fix, browser doesn't) | Hard refresh (Cmd+Shift+R) or add `?v=N` cache-buster to URL. Verify with `curl -s URL | grep -c 'const $ ='` to confirm server has the fix |
| **All KPIs and table empty, no console errors** | `const lessons = LESSONS.slice()` placed **inside** `function filtered()` instead of at top level | Move `const lessons = LESSONS.slice();` to immediately after the data array, before any function declarations. Verify with `typeof lessons` in browser console — should return `'object'`, not `'undefined'` |
| **JS parser fails silently, page renders nothing** | `function filtered()` missing its opening brace because `const lessons` line was inserted where the brace should be | After `const lessons = LESSONS.slice();`, the next line must be `function filtered(){` with a proper opening brace. Check browser console for syntax errors |
| **SCP silently deploys old file** | `scp` command succeeded but server file unchanged (possible LiteSpeed or filesystem quirk) | Use two-step method: scp to /tmp first, then cp on server. Verify with `ssh server "grep -c 'marker' path"` after deploy |
| **LiteSpeed serves cached version** | Server-side cache not invalidated after file update | Add `.htaccess` with `CacheDisable public /` and `Header set Cache-Control "no-cache, no-store, must-revalidate"`. Add `<meta http-equiv>` tags in HTML head |
| **Browser shows old version despite server having fix** | Browser cache persists across page loads | Use `curl -s URL | grep -c 'marker'` to confirm server has the fix. If yes, hard refresh browser. If still broken, the issue is browser cache, not server |
