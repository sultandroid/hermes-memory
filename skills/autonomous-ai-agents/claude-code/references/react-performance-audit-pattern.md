# React Performance Audit — Claude Code Pattern

Use this pattern when the user reports a slow/janky React app. Read the key files below and check for the common issues.

## Files to Read (always)

| File | What to check |
|------|---------------|
| `src/App.tsx` | Component tree, z-index stacking of content vs background layers |
| `src/index.css` | `backdrop-filter`, `mix-blend-mode`, `@media print`, z-index of canvas, `cursor:none` |
| `src/hooks/use*.ts` | rAF loops, Three.js/WebGL, mousemove listeners, resize handlers |
| `src/sections/*.tsx` | ScrollTrigger usage, inline IIFEs inside render, large dataset imports |
| `src/data/*.json` | File size of imported JSON — >500KB per file causes serialization cost on every import |

## Issues to Check (in priority order)

### 1. WebGL / Canvas never pauses
- `FILE: src/hooks/use*.ts`
- Check if `requestAnimationFrame` loop runs unconditionally
- Check if `renderer.setPixelRatio()` is capped (should be ≤1, not 2)
- **Fix:** Add `paused` boolean + event listeners (`visibilitychange`, custom modal-open/close events) to skip `render()` when invisible

### 2. `backdrop-filter` over animating content
- `FILE: src/index.css` and `*.tsx` inline styles
- Every `backdrop-filter: blur()` causes GPU re-compositing of the backdrop layer
- If the backdrop is the WebGL canvas (always animating), the blur re-samples every frame
- **Fix:** Replace with solid semi-opaque background (`rgba(... ,.97)`) where the blur is decorative

### 3. Data-heavy computation inside render
- `FILE: src/sections/*.tsx`
- Check if `getMaterials()`, `json.parse()`, or large array operations run inline (not memoized)
- Check if they run on every `mousemove` handler (hover → re-render → re-merge)
- **Fix:** `useMemo` or `editMode ? fn() : []` (lazy load only when needed)

### 4. Duplicate animation engines
- `FILE: src/hooks/use*.ts`
- Check if same hook is called from parent AND child component (both mount simultaneously)
- Each call starts a separate rAF loop + event listener writing to the SAME DOM nodes
- **Fix:** `useRef<boolean>(false)` singleton guard — only first mount runs the loop

### 5. `mix-blend-mode` on moving elements
- `FILE: src/index.css`
- Forces repaint of blended region on every position change
- **Fix:** Remove blend mode if decorative, or gate behind `@media (min-resolution: 1x)`

### 6. ScrollTrigger global kill on unmount
- `FILE: src/sections/*.tsx`
- `ScrollTrigger.getAll().forEach(t => t.kill())` kills ALL triggers on the page, not just the component's own
- **Fix:** Capture only the triggers created by THIS effect in an array, kill only those

## Summary Table

| Issue | File | Severity | Quick Fix |
|-------|------|----------|-----------|
| WebGL never pauses | `use*.ts` | HIGH | Pause on modal open + tab hidden |
| backdrop-filter blur | CSS | HIGH | Replace with solid bg |
| Inline data merge | `*Viewer*.tsx` | HIGH | useMemo / lazy load |
| Duplicate cursor rAF | `use*.ts` | MEDIUM | Singleton guard |
| mix-blend-mode | CSS | MEDIUM | Remove |
| ScrollTrigger global kill | `*.tsx` | LOW | Track own triggers |
