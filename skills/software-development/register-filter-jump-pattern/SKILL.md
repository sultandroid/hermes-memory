---
name: register-filter-jump-pattern
title: Filter-to-Schedule Jump — UX Pattern for Register Web Apps
description: When a user clicks any high-level filter on a register page (matrix cell, category bar, KPI card, chip, select), scroll the schedule table into view and flash it so the user sees the update. Used on the live Aseer Risk Register and reusable on any Samaya register web app (Risk, Lessons Learned, Submittals, NCRs, SIs).
---

## When to use

Any Samaya register web app built from the `register-webapp-template` umbrella. The user clicks a filter up top, the table further down updates silently, and the user doesn't notice. This pattern fixes that with a smooth scroll + brief flash.

## Reference

Live example: https://samaya-factory.com/aseer/registers/Risk/

The `register-webapp-template` umbrella is the source of truth for the register style. This skill only adds the scroll/flash behaviour on top.

## The pattern (4 steps)

### 1. Anchor the table

```html
<div class="tcard" id="schedule">
  <div class="tscroll">
    <table>
      <thead><tr id="thead"></tr></thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>
</div>
```

### 2. CSS — scroll offset for the sticky topbar + flash animation

```css
#schedule { scroll-margin-top: 96px; }
#schedule.flash { animation: scheduleFlash 1.1s ease-out; }
@keyframes scheduleFlash {
  0%   { box-shadow: 0 0 0 0 rgba(2,132,199,0); border-color: var(--border); }
  15%  { box-shadow: 0 0 0 4px rgba(2,132,199,.25); border-color: #0284C7; }
  100% { box-shadow: 0 0 0 0 rgba(2,132,199,0); border-color: var(--border); }
}
```

`scroll-margin-top: 96px` keeps the table header from disappearing under the sticky topbar after the jump. The topbar is roughly 70-80px tall.

### 3. Distinguish user-driven re-renders from initial load

Add a flag, set it only at user-action sites:

```javascript
let userFilterPending = false;

// At every user click handler (matrix cells, bar rows, KPI cards, chips, selects,
// toggleRating, toggleStatus, clearAll):
userFilterPending = true;
renderAll();
```

Do NOT set the flag inside `init()`, `syncSelects()`, `updateShowing()`, or any helper called by `renderAll()` itself — only at true user-action entry points.

### 4. The jump + flash, inside `renderAll()`

```javascript
function renderAll(){
  renderMatrix(); renderCatBars(); renderStatusBars(); renderOwnerBars();
  renderChips(); renderTable(); updateShowing(); syncActive();

  if (userFilterPending && $('#schedule')) {
    userFilterPending = false;
    const t = $('#schedule');
    t.scrollIntoView({behavior:'smooth', block:'start'});
    t.classList.remove('flash');   // restart animation if mid-flash
    void t.offsetWidth;            // force reflow
    t.classList.add('flash');
  }
}
```

## Why each piece matters

- `t.classList.remove('flash'); void t.offsetWidth; t.classList.add('flash');` — without the forced reflow, re-adding the same class does nothing because the browser doesn't see a class change. The reflow forces it.
- `scroll-behavior: smooth` is the default; users with `prefers-reduced-motion: reduce` get instant scroll automatically.
- The flash is purely decorative (box-shadow + border colour) — it does not interfere with screen readers.

## User-action sites in the risk-register template

These are all the places that must set `userFilterPending = true`:

- Matrix cell click (`renderMatrix` — `.cell[data-p]` onclick)
- Category bar click (`renderCatBars` — `barChart(..., {onClick: ...})`)
- Status bar click (`renderStatusBars` — same)
- Owner bar click (`renderOwnerBars` — same)
- KPI cards (`renderKPIs` — each card's `act:` lambda, since they call `toggleRating`/`toggleStatus`/`clearAll`)
- Rating chips (`renderChips` — `#rateChips .chip` onclick)
- Status chips (`renderChips` — `#statusChips .chip` onclick)
- Category select (`renderSelects` — `#catSelect.onchange`)
- Owner select (`renderSelects` — `#ownerSelect.onchange`)
- `toggleRating`, `toggleStatus`, `clearAll` directly (all are user-driven)

## Exclusions

- The `search` input is intentionally excluded — typing into search should not scroll the page. It only calls `renderTable()` and `updateShowing()`, not `renderAll()`.
- `init()` and the initial render must NOT set the flag, otherwise the page scrolls on load.

## Live deploy path (confirmed 2026-07-24)

When editing the live Aseer Risk Register:

```bash
# Local file path
/tmp/risk_index.html

# Server path (source of truth — NOT public_html/aseer/...)
/home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/Risk/index.html

# Public URL
https://samaya-factory.com/aseer/registers/Risk/
```

Deploy via SSH (see `register-webapp-template` Skill 8 — SSH pipe is the most reliable method on LiteSpeed hosts; SCP can silently return exit 0 without writing).

## Accessibility

- The flash is purely decorative — screen readers do not announce it.
- Keyboard users get the same behaviour because the same onclick fires on Enter.
- `prefers-reduced-motion: reduce` users get instant scroll (browser default).

## Verifying a live deploy (browser session fragility + cache busting)

This is the **only reliable sequence** for confirming the pattern is live and working in the browser. Use it after every deploy, every JS edit, every CSS tweak on any register app that uses this pattern.

### The problem (3 things to know about this stack)

1. **LiteSpeed aggressively caches HTML.** A `curl` after `scp` may return the new file, but the browser keeps serving the old one for minutes.
2. **The browser session can drop JS state mid-conversation.** `browser_console` can return `null` / 0 elements even though the snapshot from `browser_navigate` shows the rendered page. DOM is intact; the JS-driven mutations (matrix cells, table rows) are not there for the console to find yet.
3. **`scp` can silently return exit code 0** without writing the file on this Hostinger host. Always grep on the server.

### Reliable sequence (5 steps)

**1. Confirm server has the change** (server-side grep — never trust scp exit code):

```bash
ssh -p 65002 -o ConnectTimeout=10 u517606786@samaya-factory.com \
  "grep -c 'userFilterPending' /home/u517606786/domains/samaya-factory.com/public_html/build/aseer/registers/Risk/index.html"
```

Non-zero = landed. Zero = deploy failed; retry via SSH pipe (umbrella section 8).

**2. Confirm HTTP serves the new file** (defeats server-side cache):

```bash
curl -s "https://samaya-factory.com/build/aseer/registers/Risk/?v=$(date +%s)" | grep -c 'userFilterPending'
```

Server has it but curl doesn't → LiteSpeed hasn't picked it up yet → wait 30s, retry, or use a fresh cache-bust token.

**3. Browser verification with cache buster AND a single combined console call.**

Do NOT split into `browser_click` → `time.sleep` → `browser_console`. The `time.sleep` runs in a different runtime and the next `browser_console` can find a stale DOM. Put the click and the read in ONE expression:

```python
browser_console("""(() => {
  document.querySelector('.cell[data-p="4"][data-s="4"]').click();
  return {
    showing: document.getElementById('showing')?.innerText,
    scheduleTop: Math.round(document.getElementById('schedule')?.getBoundingClientRect().top),
    scrollY: Math.round(window.scrollY),
    rows: document.querySelectorAll('#tbody tr').length,
    activeBar: document.querySelector('#catBars .bar-row.active')?.getAttribute('data-key')
  };
})()""")
```

Atomically fires the click, lets the synchronous post-render JS settle, returns the truth in one call. No `time.sleep`, no intermediate `browser_click`.

**4. If `browser_console` returns nulls while the snapshot shows the page rendered:** session lost JS state. Fix with a fresh reload using a new cache-bust token:

```python
browser_navigate("https://samaya-factory.com/aseer/registers/Risk/?v=N+1")
```

Increment `?v=N` so it's a different URL from the last load. Then re-do step 3. One retry usually suffices.

**5. For the flash, do NOT assert on `classList.contains('flash')` from a delayed console call.** The animation is 1.1s; the class is removed (by `setTimeout` or by the next user click) by the time you check. Assert on the static post-render state: `showing`, `rows`, `activeBar`, `scrollY`, `scheduleTop`. The flash is a visual confirmation only.

### Anti-patterns (do NOT)

- **Click via `browser_click`, sleep, check via `browser_console` in separate turns.** Session can drop between them.
- **Trust `scp` exit code on this host.** Always grep on the server.
- **Assert on `classList.contains('flash')` from a delayed call.** It's a 1.1s animation; the class is gone by the time you check.
- **Use `time.sleep` from `execute_code` to wait for a smooth scroll.** Use the combined-click-and-read pattern instead.
- **Reload without `?v=N` after a recent deploy.** You may get the cached version and conclude the change is broken when it isn't.
- **Trust a `browser_navigate` snapshot alone as proof the page works.** The snapshot reads raw HTML; it can show 51 rows when JS hasn't initialised yet, and the next console call sees an empty DOM. Always combine snapshot reads with a console read.
