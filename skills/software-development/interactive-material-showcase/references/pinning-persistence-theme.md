# Pinning, Persistence & Theme Reference

## 🔴 Data Inviolability Rule

**NEVER modify original Excel field values.** During extraction:
- Preserve every column name, value, and row exactly as-is
- Add `_source` and `schedule_key` ONLY as metadata fields
- `#VALUE!` errors → store as literal `"#VALUE!"` string
- Multi-line cells with `\n` → preserve as `\n`
- When asked to verify: compare field names, row counts, and all values against source XLSX

**Pitfall — `_source` vs `source` ambiguity**: Materials may have both `source` and `_source`. Schedule groups by `m.source`. If only `_source` exists, items group under "Other". Normalize during extraction.

## 🟡 Pinning Mechanism (Click-to-Stay Tooltip)

Three-layer state for tooltip persistence:

```typescript
const pinnedRef = useRef<string | null>(null);   // synchronous for event handlers
const clickedRef = useRef(false);                 // blocks ALL mousemove tooltip changes
const [pinnedCode, setPinnedCode] = useState<string | null>(null);  // UI only
```

**Flow:** Click pin → set all three → `handleMouseMove`/`onMouseLeave`/rAF all check `pinnedRef.current` or `clickedRef.current` before clearing.

**Dismiss must clear ALL:** `pinnedRef.current = null; clickedRef.current = false; setPinnedCode(null); setTooltip(null);`

**Sidebar click fix:** Must also set `clickedRef.current = true; pinnedRef.current = hs.code; setPinnedCode(hs.code)` — otherwise tooltip disappears on next mousemove.

## 🔄 Cross-Component Navigation

Use CustomEvent instead of URL hash:

```typescript
// Sender:
window.dispatchEvent(new CustomEvent('schedule-change', { detail: name }));
// Receiver:
useEffect(() => {
  const handler = (e: Event) => setActiveSchedule((e as CustomEvent).detail);
  window.addEventListener('schedule-change', handler);
  return () => window.removeEventListener('schedule-change', handler);
}, []);
```

## 💾 Hotspot Persistence

**`hotspot-data/` MUST be outside deploy dir.** The deploy does `rm -rf aseer` which wipes the entire build directory.

```php
// sync.php — safe path:
$dataDir = __DIR__ . '/../../hotspot-data';  // → /public_html/hotspot-data/
```

**Export/Import** buttons in editor toolbar (📤/📥) for manual recovery.

## 🎨 Light/Formal Theme Palette

| Token | Hex | Usage |
|-------|-----|-------|
| Background | `#E8E3DB` | sections |
| Surface | `#EFEAE3` | cards, tables |
| Elevated | `#F5F1EB` | inputs, buttons |
| Text Primary | `#1A1D23` | headings |
| Text Muted | `#6B6F75` | secondary |
| Accent | `#C8A45C` | gold |
| Border | `rgba(26,29,35,.1)` | dividers |

### RAL Color Swatch
```typescript
// Match only standard 4-digit RAL (not RAL Design 7-digit):
const m = val.match(/\bRAL\s*(\d{4})(?!\d)/i);
```

### Schedule Table
- BG: `#E8E3DB`, Table: `#EFEAE3`, Alt rows: `#EAE5DD`
- Row hover: `rgba(200,164,92,.12)`
- Code font: `'IBM Plex Mono'`, color: `#C8A45C`
- Pagination/inputs: `#F5F1EB` surface

## 🔧 RAL-HEX Lookup (common)
```
7015:#434B4D  7016:#293133  7021:#2F3538  7035:#C5C7C4
7038:#B0B5B1  7030:#939388  7042:#8D9292  7040:#9DA1A2
9003:#F4F4F4  9005:#0A0A0A  9010:#F7F9F8  5005:#00538A
3000:#AF2B1E  6002:#2D6B2A  8004:#8D4E2A  1015:#E6D2B5
6018:#5D9B3A  1000:#C9B87C  7001:#8F9698  7004:#9DA1A3
```

## Known Bug Patterns

1. **`pointer-events: none` on pins** — pins visible but unclickable. Remove the CSS rule.
2. **`.toLowerCase()` on undefined fields** — crashes filter. Guard: `f && f.toLowerCase()`
3. **Chrome LevelDB extraction** — only `.log` files are uncompressed. `.ldb` files need `python-snappy`. Best recovery: use app's Export button.
4. **Hotspot wiped on deploy** — see persistence section above.
