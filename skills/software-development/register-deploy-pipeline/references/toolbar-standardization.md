# Toolbar Standardization — All Four Registers

Every register (PRR, DDR, HSE, AVR) must have identical toolbar buttons and register navigation in the same position. PRR is the reference.

## Toolbar buttons

In order, inside `.top-actions`:

```
[RESET]  [DOWNLOAD SNAPSHOT]
```

CSV and PRINT buttons are **optional** — the user may ask to remove them. When present, add after DOWNLOAD SNAPSHOT:

```
[RESET]  [DOWNLOAD SNAPSHOT]  [CSV]  [PRINT]
```

| Button | Element | ID | Action | Present by default? |
|--------|---------|----|--------|---------------------|
| RESET | `<button>` | `btnReset` | `clearAll()` | Always |
| DOWNLOAD SNAPSHOT | `<a>` | `btnSnapshot` | `href="javascript:void(0)"` | Always |
| CSV | `<button>` | `btnCsv` | `exportCSV()` | Removed by user request |
| PRINT | `<button>` | `btnPrint` | `window.print()` | Removed by user request |

### Removing CSV/PRINT buttons

When the user asks to remove CSV and PRINT:

1. Delete the `<button>` HTML elements from the topbar.
2. Remove the JS bindings from `init()`:
   ```javascript
   // Remove these lines:
   $('#btnCsv').onclick = exportCSV;
   $('#btnPrint').onclick = ()=>window.print();
   ```
3. Repeat for ALL four registers (PRR, DDR, HSE, AVR) — the user notices discrepancies across pages.
4. The `exportCSV()` function can remain in the JS (unused, no harm). Only the button and binding need removal.

## Register navigation position

```
<div class="hright">
  <span class="tag">LIVE SNAPSHOT</span>
  <div class="reg-nav" id="registerNav"></div>    ← NAV HERE
  <img class="logo" ...>
  <div class="top-actions">
    <button id="btnReset">...</button>
    ...
  </div>
</div>
```

**Do NOT** place `#registerNav` inside `htitle` or in a separate `dcline`. Must be in `hright`.

## CSS

```css
.reg-nav { font-family: var(--mono); font-size: 11px; color: var(--text-muted); white-space: nowrap; }
.reg-nav a { color: var(--secondary); text-decoration: none; font-weight: 600; }
.reg-nav a:hover { text-decoration: underline; }
```

## Init bindings (every register's init() must have these)

```javascript
$('#btnReset').onclick = clearAll;
$('#btnCsv').onclick = exportCSV;
$('#btnPrint').onclick = ()=>window.print();
```

## Verification checklist

After deploying to any register:
1. Open the page in a browser
2. Confirm RESET, DOWNLOAD SNAPSHOT, CSV, PRINT all visible
3. Click CSV — should download a `.csv` file
4. Click PRINT — should open browser print dialog
5. Confirm register nav shows: `Viewing: <register name> - <sibling links>`

## Common issues

- **Missing `exportCSV()` function**: copy from PRR's JS. It's register-agnostic (reads from RISK global and state filter).
- **Missing `btnSnapshot`/`btnCsv`/`btnPrint` HTML elements**: add them following PRR's exact SVG markup.
- **Register nav in wrong position**: if found inside `htitle` or wrapped in a `dcline`, move to `hright` between the tag and the logo.
- **Duplicate `registerNav` elements**: when migrating an older template, the old `#registerNav` in `htitle` and the new one in `hright` both exist — remove the old one.
