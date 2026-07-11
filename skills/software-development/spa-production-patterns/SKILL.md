---
name: spa-production-patterns
description: "Production patterns for Single Page Applications: iframe-based authentication with CSRF tokens and Backbone/React routers, and server-side persistence with PHP sync endpoints on shared hosting."
version: 1.0.0
author: Hermes Agent
tags: [spa, authentication, iframe, persistence, php, sync, collaboration, hosting]
---

# SPA Production Patterns

Two common production challenges for Single Page Applications: authenticating through iframe-based login flows, and adding server-side data persistence without a dedicated backend.

## Contents

1. [Iframe-Based Authentication](#1-iframe-based-authentication)
2. [Server-Side Persistence](#2-server-side-persistence)

---

## 1. Iframe-Based Authentication

### When to Use

Modern web apps often authenticate via an embedded `<iframe>` that loads a separate auth SPA. The login form is rendered dynamically by JavaScript (Backbone, React, Angular) inside the iframe. Standard `browser_click` on login links may not work because the login link uses hash-based routing, jQuery click handlers don't propagate, or the iframe auth form is async.

### Detection

Check for these signals:
1. Hidden iframes on the landing page: `document.querySelectorAll('iframe')`
2. Login links with hash-based URLs: `href="#/login"`, `href="#/signup"`
3. Auth messenger events: `GP_auth_started`, `GP_auth_completed`
4. Auth-related containers: `gpAuthFrame`, `embed-layout`, `js-embed-form`

### Step-by-Step Workflow

**1. Load the main page** → `browser_navigate(url="https://example.com")`

**2. Trigger the login dialog** — when standard click fails, inject jQuery click directly:
```javascript
jQuery('a[href="#/login"]').first().trigger('click');
// Alternative: native DOM click
document.querySelector('a[href="#/login"]').click();
```

**3. Wait for the auth iframe:**
```javascript
document.getElementById('gpAuthFrame') ? 'found' : 'not found'
```

**4. Access iframe contents** (same-origin only):
```javascript
var d = document.getElementById('gpAuthFrame').contentDocument;
```

**5. Trigger Backbone/React router to render the form** — if `#embed-layout` is empty:
```javascript
var w = document.getElementById('gpAuthFrame').contentWindow;
w.Backbone.history.navigate('/login', {trigger: true});
// Or via requirejs:
w.requirejs(['router'], function(router) {
  router.navigate('/login', {trigger: true});
});
```

**6. Fill credentials:**
```javascript
d.getElementById('email').value = 'user@example.com';
d.getElementById('password').value = 'password';
['email','password'].forEach(function(id) {
  d.getElementById(id).dispatchEvent(new Event('input', {bubbles: true}));
});
```

**7. Submit:**
```javascript
d.getElementById('login').click();
```

**8. Verify success** — iframe removed or URL changes to authenticated route.

### CSRF Token Handling

Auth iframes often pass the CSRF token via URL:
```javascript
var iframe = document.getElementById('gpAuthFrame');
var params = new URLSearchParams(iframe.src.split('?')[1]);
var csrfToken = params.get('csrfToken');
```

### Post-Auth API Discovery

Once authenticated, the SPA's internal API becomes accessible via HttpOnly cookies (not `curl`):
```javascript
var xhr = new XMLHttpRequest();
xhr.open('GET', '/api/projects', false);
xhr.withCredentials = true;
xhr.send();
JSON.parse(xhr.responseText);
```

### Troubleshooting

| Issue | Fix |
|-------|-----|
| jQuery `.click()` does nothing | Use `Backbone.history.navigate('/login', {trigger: true})` in iframe |
| Router not found | Check for `requirejs`, then `requirejs(['router'], fn)` |
| Form rendered but invisible | Check for 2FA wrapper (`#twoFaDigitsInput`) |
| Iframe contentDocument null | Cross-origin — must be same-origin |
| embed-layout stays empty | Try navigating iframe directly with fresh CSRF token |

---

## 2. Gallery Data Patterns

### When to Use

SPAs that display interactive gallery views with hotspot pins (architectural visualizations, material showcases, photo annotation tools). Views typically have a filename, description, and hotspot array.

### Data Shape

```typescript
interface View {
  viewName: string;       // unique id (e.g., 'G4_View_1')
  filename: string;       // image path on server
  desc: string;           // short display description
  subRef?: string;        // submission/document reference (e.g., full MoC code)
  hotspots: Hotspot[];    // {code: string, x: number, y: number}[]
}
```

### Submission Reference Field (`subRef`)

When gallery photos are replaced with formally issued submission drawings (e.g., "MOC-ASE-AR-ARC-BF-DDD-VIS001"), display the full submission code as a badge in the UI:

```typescript
// View entry
{viewName:'G4_View_1', filename:'/aseer/images/g4_G4_View_1.jpg',
 subRef:'MOC-ASE-AR-ARC-BF-DDD-VIS001', desc:'Main gallery hall overview',
 hotspots:[...]},

// Display in sidebar (React)
{view.subRef && (
  <div style={{
    fontFamily:"'IBM Plex Mono',monospace", fontSize:'0.55rem',
    color:'#C8A45C', background:'rgba(200,164,92,.1)',
    padding:'3px 8px', borderRadius:'4px', marginBottom:'8px',
    display:'inline-block', letterSpacing:'0.02em',
  }}>{view.subRef}</div>
)}
```

**Benefit:** The server-side filename can stay short (`g4_G4_View_1.jpg`) while the UI shows the formal submission reference. No need to rename files on disk.

### Cache-Busting Image Version

When replacing photos (keeping the same server filename), browsers serve old cached images. Use a version constant:

```typescript
const IMG_VERSION = '2'; // bump when replacing photos

// In JSX:
<img src={`${view.filename}?v=${IMG_VERSION}`} alt={view.desc} />
```

**Increment the constant on each batch of photo replacements.** All images served with the new version number bypass browser cache.

### Empty Hotspots Pattern

When hotspot data isn't ready yet, create gallery entries with `hotspots:[]`. The user can add pins later via an admin panel:

```typescript
{viewName:'LGF_Vis017', filename:'/aseer/images/lgf_vis017.jpg',
 desc:'Lower Ground Floor – Welcome Gallery',
 hotspots:[]},
```

The gallery card will show "0 materials" and the view opens with no pins visible.

### Summary

| Pattern | When | Key Line |
|---------|------|----------|
| `subRef` | Formal submission name differs from server filename | `subRef:'MOC-...-VIS001'` |
| `IMG_VERSION` | Replacing photos on same server path | `const IMG_VERSION = '2'` |
| Empty hotspots | Photo uploaded but pin data pending | `hotspots:[]` |

---

## 3. Server-Side Persistence

### When to Use

You built a static SPA (React, Vue, plain HTML) that stores data in localStorage. The team needs to share data (hotspots, notes, annotations) across devices with no backend server available.

### Architecture

```
Browser (SPA)          Web Host (PHP)
    │                       │
    ├─ GET  sync.php?gallery=X&view=Y ──→ reads JSON from disk
    │                       │
    └─ POST sync.php ──────────────→ writes JSON to disk
         {gallery, view, hotspots}
```

- **Both storage layers**: browser localStorage + server JSON file
- **Read**: check server first, fall back to localStorage
- **Write**: save locally + push to server (fire-and-forget)
- **Offline**: localStorage works when server is unreachable

### PHP Sync Server

```php
<?php
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }

$dataDir = __DIR__ . '/../../hotspot-data'; // OUTSIDE deploy dir
if (!is_dir($dataDir)) mkdir($dataDir, 0755, true);

if ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $gallery = $_GET['gallery'] ?? ''; $view = $_GET['view'] ?? '';
    $file = "$dataDir/{$gallery}_{$view}.json";
    header('Content-Type: application/json');
    echo file_exists($file) ? file_get_contents($file) : '[]';
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $body = json_decode(file_get_contents('php://input'), true);
    $file = "$dataDir/{$body['gallery']}_{$body['view']}.json";
    file_put_contents($file, json_encode($body['hotspots'], JSON_PRETTY_PRINT));
    echo json_encode(['ok' => true]);
    exit;
}
```

### Client-side Store

```typescript
const SYNC_URL = 'https://your-domain.com';

async function loadFromServer(gallery: string, view: string) {
  const res = await fetch(`${SYNC_URL}/sync.php?gallery=${gallery}&view=${view}`);
  const data = await res.json();
  return Array.isArray(data) && data.length > 0 ? data : null;
}

async function saveToServer(gallery: string, view: string, hotspots: any[]) {
  await fetch(`${SYNC_URL}/sync.php`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ gallery, view, hotspots }),
  });
}
```

### Data Directory Persistence (Critical)

**Symptom:** Saved data disappears after every redeploy.
**Root cause:** `sync.php` stores data in `__DIR__ . '/hotspot-data'` which resolves within the deploy directory. The deploy script does `rm -rf` on that directory.
**Fix:** Store data OUTSIDE the deploy directory:
```php
$dataDir = __DIR__ . '/../../hotspot-data';
```

### Pitfalls

- **🔴 Hotspot-data wiped on every deploy**: Always use `__DIR__ . '/../../hotspot-data'` (two levels up from sync.php) so data survives `rm -rf <build-dir>`.
- **🔴 Uncommitted design changes get deployed with data-only edits**: Before editing gallery data, run `git diff src/sections/Gallery.tsx` to check for uncommitted design changes. If the file has accumulated design changes from a previous session, restore from the init commit first, then re-apply only your data additions. See `references/gallery-data-restoration.md`.
- **PHP not available on Surge**: Surge.sh is static-only. Need a host with PHP (Hostinger, SiteGround, etc.).
- **localStorage is truth, server is cache**: Always write to localStorage first, then sync to server.
- **Admin password in JS is visible**: For casual access control only — use a proper backend for real security.
- **CORS**: PHP needs `Access-Control-Allow-Origin: *` to work cross-origin.
- **Last-write-wins**: Flat-file approach doesn't handle concurrent edits. Add `modified_at` for conflict detection.
