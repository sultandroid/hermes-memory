# GanttPRO Login — Concrete Reference Example

## Site Structure

| Component | URL | Notes |
|-----------|-----|-------|
| Main site | `https://ganttpro.com/` | Marketing landing page |
| App (after login) | `https://app.ganttpro.com/` | SPA, redirects to ganttpro.com if unauthenticated |
| Auth iframe | `https://ganttpro.com/embed/embed.html?locale=en&csrfToken=TOKEN` | Loaded by the main page JS |
| Backend API | `ganttpro-services.azurewebsites.net` | ASP.NET MVC, accepts POST/OPTIONS |
| Key JS bundles | `/dest/embed.js` (481KB) | Login form rendering, RequireJS + Backbone SPA |
| | `/dest/pages/home-page.js` (463KB) | Landing page interaction, analytics |
| | `cdn.ganttpro.com/app/builds/.../app.js` | Authenticated app bundle |

## Exact Step-by-Step (Verified Working Sequence)

### Step 1: Load page and trigger auth iframe
```
browser_navigate(url="https://ganttpro.com/")
```

### Step 2: Click login (jQuery required, native click fails)
```javascript
// In browser_console:
jQuery('a[href="#/login"]').first().trigger('click');
// Wait ~1s for iframe to appear
```

### Step 3: Verify iframe loaded
```javascript
document.getElementById('gpAuthFrame') ? 'found' : 'not found'
```
If the iframe is `null`, the jQuery click didn't propagate. Retry.

### Step 4: Navigate Backbone router to render login form
The iframe's `#embed-layout` div is initially empty. The Backbone router must navigate to `/login`:

```javascript
var w = document.getElementById('gpAuthFrame').contentWindow;
w.Backbone.history.navigate('/login', {trigger: true});
```

This renders the login form template into `#embed-layout`.

### Step 5: Fill credentials
```javascript
var d = document.getElementById('gpAuthFrame').contentDocument;
d.getElementById('email').value = 'USERNAME';
d.getElementById('password').value = 'PASSWORD';
['email','password'].forEach(function(id) {
  d.getElementById(id).dispatchEvent(new Event('input', {bubbles: true}));
});
```

### Step 6: Click login button
```javascript
var d = document.getElementById('gpAuthFrame').contentDocument;
d.getElementById('login').click();
```

The iframe disappears on success → page redirects to `https://app.ganttpro.com/#/project/ID/gantt`

## Iframe DOM Structure

```
<html class="login-screen">
<body class="js-embed-frame">
  <svg>...</svg>  <!-- SVG icon definitions -->
  <div id="embed-layout" class="js-landing-addons">
    <!-- Form rendered here by Backbone router -->
    <div class="layout_container">
      <div class="js-embed-form login-form">
        <form role="form">
          <input id="email" name="email" type="email" placeholder="Enter your corporate email">
          <input id="password" name="password" type="password" placeholder="Password">
          <div id="twoFaDigitsInput">...</div>
          <a id="login" class="submit_btn embed-btn-login">Log in</a>
        </form>
      </div>
    </div>
  </div>
  <script src="/dest/embed.js"></script>
  <link href="/dest/embed.css">
</body>
</html>
```

## CSRF Token

- Read from URL params: `new URLSearchParams(window.location.search).get("csrfToken")`
- Stored in `window.CSRFTOKEN` by embed.js
- Token delivered by main page when creating the iframe
- Fresh token each page load; expires if page is stale

## Project Navigation (Post-Auth)

After login at `app.ganttpro.com`:

| Route | Purpose |
|-------|---------|
| `#/project/ID/gantt` | Gantt chart view for project ID |
| `#/portfolio` | Portfolio overview |
| Sidebar: "All projects" | `.allProjects-btn` class, lists all projects |
| Export button | `.button_OFzJlvgh` with text "Export" |

## Key Observations

- 5 projects existed on this account ("1 of 5" navigation)
- Current project was a demo ("Total estimate") — not the Aseer Museum project
- The app navigation uses pushState: `Backbone.history.start({pushState: true})`
- Hash changes alone don't reliably trigger navigation
- The embed.js uses RequireJS module loader with Backbone.js
- Parent-iframe communication uses a messenger object (`window.app.messenger`) with postMessage-style API
- Login form strings are i18n-enabled (embed.js has translations for 25+ languages)

## Post-Auth API Discovery

Once authenticated, the SPA's API is accessible via **XHR from the browser context** (HttpOnly cookies are sent automatically with `XMLHttpRequest` + `withCredentials: true` or `fetch` + `credentials: 'include'`). Direct `curl` calls fail because the ASP.NET session cookie is HttpOnly and scoped to `app.ganttpro.com`.

### Discovered API Endpoints

| Endpoint | Method | Response | Purpose |
|----------|--------|----------|---------|
| `/api/projects` | GET | JSON array of `{id, gantt_id, text, user_id, config}` | List all projects with full Gantt config |
| `/api/projects?all=true` | GET | Same as above | Returns project names/IDs |
| `/api/projects/status` | GET | `[]` (empty if no special statuses) | Project status configurations |
| `/api/projects/newTeamProjects` | GET | JSON or error | Team project listings (may 500) |
| `/importproject` | GET (SPA) | HTML page | Import project dialog (client-side route) |
| `/importpreview` | GET (SPA) | HTML page | Import preview (client-side route) |

### Calling the API from Browser Console

```javascript
// Synchronous XHR (simplest):
var xhr = new XMLHttpRequest();
xhr.open('GET', '/api/projects?all=true', false);
xhr.withCredentials = true;
xhr.send();
var projects = JSON.parse(xhr.responseText);

// Fetch (async):
fetch('/api/projects', {credentials: 'include'})
  .then(r => r.json())
  .then(data => console.log(data));
```

### localStorage Hints

The SPA stores state in `localStorage` which reveals useful info:

| Key | Value | Purpose |
|-----|-------|---------|
| `activeGanttId` | `"1781322138701"` (numeric) | Current project's Gantt chart ID |
| `bugsnag-anonymous-id` | UUID | Error tracking session |

### File Import Challenge

The import dialog (`#/importproject`) uses the **Webix framework** for file upload (class names like `webix_view`, `webix_window`, `webix_popup`). File uploads go through Webix's uploader widget, not a standard `<input type="file">`.

In headless browser mode, you **cannot**:
- Open the OS file picker (no UI)
- Programmatically set `<input type="file">` value (security restriction)

**Workarounds to try:**
1. Use `DataTransfer` API + `fetch` to POST a `FormData` to the backend's import endpoint directly
2. Look for the actual file upload API endpoint (likely at the `ganttpro-services.azurewebsites.net` backend)  
3. Use `new File([blob], 'file.xlsx')` + `FormData.append('file', file)` + `POST /importproject` with credentials

```javascript
// Attempt to inject file via fetch:
var blob = new Blob([fileBytes], {type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
var form = new FormData();
form.append('projectName', 'My Project Name');
form.append('file', blob, 'schedule.xlsx');
fetch('/importproject', {
  method: 'POST',
  body: form,
  credentials: 'include'
});
```

### Detecting Post-Auth State

After successful login, confirm by:
1. Checking iframe removal: `document.getElementById('gpAuthFrame') === null`
2. URL check: `window.location.host === 'app.ganttpro.com'`
3. localStorage: `localStorage.getItem('activeGanttId')` returns a project ID
4. API check: `fetch('/api/projects', {credentials: 'include'})` returns JSON, not HTML
