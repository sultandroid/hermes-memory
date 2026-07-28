# fix_cards_static.py — Register Card Post-Processor

Located at `webapp/fix_cards_static.py`. Called automatically by each build script.

## How it works

1. Reads the built HTML file
2. Extracts the `RISK` JSON to detect the current register (`is_ddr`, `is_hse`, `is_av` flags)
3. Replaces the entire `<div class="registers" id="registers">` section with correctly-structured cards
4. Current register gets: `<div class="reg-card reg-current">` with "current" badge
5. Other registers get: `<a class="reg-card" href="{relative_path}">`

## Relative path logic

- On PRR page: DDR → `DDR/`, HSE → `HSE/`, AVR → `AVR/`
- On DDR page: PRR → `../`, HSE → `../HSE/`, AVR → `../AV/` (and same pattern for HSE/AVR pages)

## Two-layer protection

The auto-deploy cron (every 15 min) deploys from committed git files. If the committed files predate fix_cards_static, the static build-time fix gets reverted.

**Layer 2 fixCards() in template.html:** An IIFE inside `function init()` runs on every page load and auto-corrects card hrefs using the path map: `{PRR:'../', DDR:'../DDR/', HSE:'../HSE/', AVR:'../AV/'}`. This JS survives any deployment — never remove it.

## Critical warning

The script uses nesting-aware div counting to find the registers section (not regex). If the HTML structure changes (e.g. new div wrappers), the counting logic may break.

## Self-test

```bash
python3 fix_cards_static.py src/DDR/index.html
# Should print "Fixed cards for DDR"
```
