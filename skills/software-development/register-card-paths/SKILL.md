---
name: register-card-paths
description: Fix register card navigation paths on multi-page risk register webapps when sub-pages (DDR/HSE/AVR) have wrong relative hrefs.
---

# Register Card Paths Fix

## The Problem

Multi-register risk webapps (PRR, DDR, HSE, AVR) at `/Risk/`, `/Risk/DDR/`, `/Risk/HSE/`, `/Risk/AV/` have register card navigation (big cards showing PRR/DDR/HSE/AVR). The template hardcodes hrefs like `href="DDR/"` which work on the PRR page but **break on sub-pages** where paths should be `../DDR/`.

## The Clickability Trap (CRITICAL)

Two mechanisms **actively prevent the current-page register card from being clickable** — both must be neutralised to make the Master Risk Register (or any current card) a working link.

### Trap 1: JS replaces `<a>` with `<div>`

The `fixCards()` IIFE in `init()` deliberately destroys the link on the current card:

```javascript
// BEFORE fix (BROKEN — replaces <a> with <div>, kills the link):
if (isCur && el.tagName === 'A') {
    var d = document.createElement('div');
    d.innerHTML = el.innerHTML;
    d.className = el.className;
    // ... add badge ...
    el.parentNode.replaceChild(d, el);  // ← link is gone
}

// AFTER fix (keep <a>, just add badge):
if (isCur && el.tagName === 'A') {
    var h = el.querySelector('.reg-head');
    if (h && !el.querySelector('.reg-badge')) {
        var b = document.createElement('span');
        b.className = 'reg-badge'; b.textContent = 'current';
        h.insertBefore(b, h.firstChild);
    }
    // No replaceChild — <a> stays intact with href="."
}
```

**Same anti-pattern in `fix_cards_static.py`** (the post-processing build script). Lines like:
```python
f'    <div class="reg-card reg-current">\n'
```
Must be:
```python
f'    <a class="reg-card reg-current" href=".">\n'
```

### Trap 2: CSS `cursor: default`

The CSS rule on `.reg-card.reg-current` sets `cursor: default` which overrides the natural pointer cursor of an `<a>` tag:

```css
/* BEFORE: hides link affordance */
.reg-card.reg-current { background: ...; border-color: ...; cursor: default; }

/* AFTER: let the browser show the pointer for <a> */
.reg-card.reg-current { background: ...; border-color: ...; }
```

**Three files must be patched:** All 4 built HTML pages, all templates (`template.html`, `av/template_av.html`), and `fix_cards_static.py`.

### Full fix checklist

| What | Files |
|------|-------|
| HTML: PRR card `<div>` → `<a href=".">` | `src/index.html` (PRR), `av/template_av.html` |
| JS: Stop replacing `<a>` with `<div>` | All 4 `src/*/index.html`, `template.html`, `av/template_av.html` |
| CSS: Remove `cursor: default` | All 4 `src/*/index.html`, `template.html`, `av/template_av.html` |
| Post-build: `fix_cards_static.py` output `<a>` not `<div>` | `fix_cards_static.py` |
| Build script: AVR banner uses `<a>` | `av/build_av.py` |

After patching, rebuild all 4 registers and verify with `curl | grep 'reg-card reg-current'` that all current cards are `<a>` tags with `href="."`.

## Two-Layer Path Fix

### Layer 1: Build-time (`fix_cards_static.py`)

Post-processor that rewrites static HTML after each build. Called from the build script's `if __name__ == "__main__"` block:

```python
if __name__ == "__main__":
    ret = main()
    import subprocess, sys as _sys, pathlib
    script = pathlib.Path(__file__).resolve().parent / "fix_cards_static.py"
    if script.exists():
        subprocess.run([_sys.executable, str(script), str(OUT)], check=False)
    raise SystemExit(ret)
```

The script detects the current register from `RISK.is_ddr/is_hse/is_av` flags in the embedded JSON data, swaps `<a>` tags (current) and `<a>` (links), and rewrites hrefs to `../DDR/` etc.

### Layer 2: Runtime (JS in `template.html init()`)

```javascript
(function fixCards(){
    var reg = RISK.is_ddr ? 'DDR' : RISK.is_hse ? 'HSE' : RISK.is_av ? 'AVR' : 'PRR';
    var cards = document.querySelectorAll('#registers .reg-card');
    cards.forEach(function(el){
        var code = el.querySelector('.reg-code').textContent.trim();
        var isCur = code === reg;
        el.classList.toggle('reg-current', isCur);
        // ... add badge, fix hrefs (no more div swap) ...
    });
})();
```

## Agent Rules

1. Never remove `fixCards()` from template.html — but ensure it keeps `<a>` tags, doesn't replace them with `<div>`
2. Never remove `fix_cards_static.py` post-processing from build scripts — but ensure it outputs `<a>` not `<div>`
3. When changing card HTML, test all 4 register pages
4. Template always uses PRR-page paths — JS fixes sub-pages
5. Auto-deploy cron (15min) overwrites SCP-only fixes — commit built files to git
6. Warning comments at top of build_ddr.py, build_hse.py, build_av.py

## Verification

After fixing, confirm on the live site:

```bash
# All 4 pages must show <a> for the current card
curl -s https://samaya-factory.com/aseer/registers/Risk/ | grep 'reg-card reg-current'
curl -s https://samaya-factory.com/aseer/registers/Risk/DDR/ | grep 'reg-card reg-current'
curl -s https://samaya-factory.com/aseer/registers/Risk/HSE/ | grep 'reg-card reg-current'
curl -s https://samaya-factory.com/aseer/registers/Risk/AV/ | grep 'reg-card reg-current'
# Each should show: <a class="reg-card reg-current" href=".">
```

Also check via browser console: `document.querySelector('.reg-card.reg-current').tagName` must return `"A"` not `"DIV"`.

## Pitfalls

- **Accessibility tree may not show `<a>` as "link"** even when it's correct. The browser accessibility tree sometimes renders `<a>` wrappers around block content as "generic" containers. Verify with `curl` against raw HTML, not just the browser snapshot.
- **Build scripts rebuild from template** — if you only patch the built HTML files, the next build reverts them. Always also patch `template.html`, `fix_cards_static.py`, and the build script output logic.
- **Post-commit hook re-runs builds** — after every commit, the hook rebuilds all registers from source. This can overwrite your built files. Stash before pulling.
- **LiteSpeed cache** — Hostinger caches aggressively. Use `?cb=$(date +%s)` for curl verification and tell the user to hard refresh (Cmd+Shift+R).
