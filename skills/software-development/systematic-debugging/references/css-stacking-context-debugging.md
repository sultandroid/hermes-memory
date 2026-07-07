# CSS Stacking Context Debugging

## Common Patterns from React/Web Apps

### 1. Fixed-Position Canvas Behind Content (WebGL Background)

**Symptom:** WebGL/canvas at `position:fixed;z-index:0` appears ON TOP of content sections that should be above it.

**Root cause:** The stacking context relationship between `position:fixed` elements and their siblings. Even with `z-index:0`, a fixed element creates its own stacking context that can interfere with sibling elements.

**Fix:**
```html
<!-- Give the root div position:relative;z-index:1 to create a stacking context ABOVE the canvas -->
<div id="root" style="position:relative;z-index:1;min-height:100vh;"></div>
<canvas id="webgl" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:-1;pointer-events:none;"></canvas>
```

**Key insight:** `position:relative;z-index:1` on the root wrapper puts ALL content in a stacking context at layer 1. The canvas at `z-index:-1` is definitively below everything. Add `pointer-events:none` to prevent the canvas from intercepting clicks/scrolling.

### 2. Media Query Specificity Override Failure

**Symptom:** A `@media (max-width:768px)` rule sets `overflow:auto` on an element, but the element still clips content with `overflow:hidden`. The media query appears correct in the CSS file but doesn't apply.

**Root cause:** CSS cascade order. If the base class (`.modal-image-wrap { overflow:hidden; }`) appears AFTER the media query in the CSS file, the base rule wins because both have the same specificity (one class). The media query only adds a condition — it doesn't change specificity.

**Fix:** Use higher-specificity selectors inside the media query:
```css
/* Instead of: */
@media (max-width: 768px) {
  .modal-image-wrap { overflow: auto; }  /* specificity 0,1,0 — overridden by later base class */
}

/* Use: */
@media (max-width: 768px) {
  .gallery-modal .modal-image-wrap { overflow: auto; }  /* specificity 0,2,0 — beats base class */
}
```

**Verification:** Check the COMPILED CSS bundle via `curl | grep` to see which selectors actually ship. Vite/Tailwind can reorder CSS during optimization.

### 3. Fixed/Sticky Elements Inside Scrollable Modals

**Symptom:** A `position:absolute` button at `top:-12px;left:-12px` inside a modal is invisible or unreachable on mobile.

**Root cause:** The button is outside its positioned parent's bounds, and the parent's `overflow:hidden` clips it. On mobile with `align-items:flex-start`, the modal starts at the viewport top — the button at `top:-12px` is above the viewport.

**Fix:** Use `position:fixed` on mobile + `!important` to override the base position:
```css
@media (max-width: 768px) {
  .gallery-modal .modal-close-btn {
    position: fixed !important;
    top: 12px !important;
    left: 12px !important;
    z-index: 99999 !important;
  }
}
```

**Key insight:** `!important` is justified here because the base class (`position:absolute`) would otherwise win due to cascade ordering.

### 4. backdrop-filter Compositing Over Animated Content

**Symptom:** The page is laggy/choppy on desktop when a modal is open over an animated WebGL background.

**Root cause:** `backdrop-filter:blur()` on the sidebar/tooltip composites against the continuously-animating canvas behind it. The browser must re-sample and blur the entire backdrop every frame — expensive GPU work.

**Fix:** Replace `backdrop-filter:blur()` with opaque or near-opaque backgrounds:
```css
/* Instead of: */
background: rgba(245,241,235,.9); backdrop-filter: blur(12px);

/* Use: */
background: rgba(245,241,235,.97);
```

**Trade-off:** Tiny visual difference (barely perceptible at α≥.97), huge performance win.

### 5. Pointer Events Blocking

**Symptom:** An element is visible but clicks/taps never reach its event handler.

**Root cause:** A parent or overlay element has `pointer-events:auto` or is intercepting via stacking context.

**Diagnosis:** Check via browser console:
```javascript
getComputedStyle(element).pointerEvents  // 'none'?
getComputedStyle(element).zIndex         // behind another element?
```

**Common patterns:**
- A `position:fixed;inset:0` backdrop without explicit `z-index` can still intercept clicks because it's a sibling at the same stacking level.
- Fix: Give positioned containers explicit `z-index` values: `.modal-backdrop { z-index: 1 }` `.modal-container { z-index: 2 }`

### 6. Three.js Canvas Performance

**Symptom:** Heavy WebGL shader always runs at full speed even when covered by a modal or when the tab is backgrounded.

**Fix:** Pause the `requestAnimationFrame` loop:
```typescript
let paused = false;
const onVis = () => { paused = document.hidden; };
const onModalOpen = () => { paused = true; };
const onModalClose = () => { paused = false; };
document.addEventListener('visibilitychange', onVis);
window.addEventListener('gallery-modal-open', onModalOpen);
window.addEventListener('close-gallery-modal', onModalClose);

const animate = () => {
  rafRef.current = requestAnimationFrame(animate);
  if (paused) return;  // skip render
  // ... render
};
```

Also reduce pixel ratio: `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 1))` instead of 2.

### 7. Singleton Animation Loop (Duplicate rAF)

**Symptom:** `.custom-cursor` or other animated elements visibly stutter or jump because two independent rAF loops write to the same DOM nodes.

**Root cause:** A React hook (`useCustomCursor()`) is called from multiple components (e.g., parent Gallery and child GalleryViewer). Each call creates an independent rAF loop writing `transform` to the same DOM elements.

**Fix:** Make the animation loop a singleton using a module-level flag:

```typescript
export function useCustomCursor() {
  const startedRef = useRef(false);
  useEffect(() => {
    if (startedRef.current) return;
    startedRef.current = true;
    // existing animation loop
  }, []);
}
```

### 8. Selective ScrollTrigger Kill

**Symptom:** Page scroll animations break after a component unmounts because it killed ALL ScrollTriggers.

**Root cause:** `ScrollTrigger.getAll().forEach(t => t.kill())` kills every trigger on the page.

**Fix:** Track only the triggers this component created:

```typescript
const myTriggers: ScrollTrigger[] = [];
cards.forEach((c,i) => {
  const tween = gsap.fromTo(c, ...);
  if (tween.scrollTrigger) myTriggers.push(tween.scrollTrigger);
});
return () => myTriggers.forEach(t => t.kill());
```

### 9. Lazy-Load Expensive Computations

**Symptom:** Full-dataset operations (1.2MB JSON) run on every mousemove.

**Fix:** Gate behind the action that needs it:

```typescript
<EditorOverlay
  materials={editMode ? getMaterials() : []}
  isOpen={editMode}
/>
```

### 10. mix-blend-mode Cursor Cost

**Symptom:** Custom cursor lags over animated content.

**Root cause:** `mix-blend-mode` forces repaint on every cursor move over the animating canvas.

**Fix:** Drop blend mode for a simple colored cursor dot.

