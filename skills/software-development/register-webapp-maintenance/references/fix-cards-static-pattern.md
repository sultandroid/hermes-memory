# fix_cards_static.py — Post-Build Register Card Corrector

**Location:** `06_Risk_System/webapp/fix_cards_static.py`

## Purpose

After `build_ddr.py`, `build_hse.py`, or `build_risk.py` writes the output HTML, this script rewrites the register cards section with the correct current register marker and relative paths.

## How it works

1. Parses the built HTML, extracts `const RISK = {...}` JSON
2. Determines current register: `current_reg = 'AVR' if is_av else 'HSE' if is_hse else 'DDR' if is_ddr else 'PRR'`
3. Builds 4 card HTML blocks — current gets `<div class="reg-card reg-current">`, others get `<a class="reg-card" href="...">`
4. Finds the registers div using nesting-aware matching (counts `<div>`/`</div>` to find matching close)
5. Replaces the entire registers section

## Relative path logic

From sub-registers (DDR, HSE, AVR), links need `../` prefix:
- PRR → `../`
- DDR → `../DDR/`
- HSE → `../HSE/`
- AVR → `../AV/`

From PRR (master), no prefix needed:
- DDR → `DDR/`
- HSE → `HSE/`
- AVR → `AV/`

## Integration

Called from each build script's `__main__` exit:

```python
if __name__ == "__main__":
    ret = main()
    import subprocess, sys as _sys
    script = HERE / "fix_cards_static.py"
    if script.exists():
        subprocess.run([_sys.executable, str(script), str(OUT)], check=False)
    raise SystemExit(ret)
```

## Verification

After running, check the built file:
```bash
python3 -c "
import re
with open('src/DDR/index.html') as f:
    c = f.read()
m = re.search(r'reg-current.*?reg-code[^>]*>([^<]+)', c, re.DOTALL)
if m:
    print('Current:', m.group(1))
"
```

Expected output for DDR file: `Current: DDR`
Expected output for HSE file: `Current: HSE`
Expected output for PRR file: `Current: PRR`
