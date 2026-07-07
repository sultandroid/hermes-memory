# React + Three.js Performance Debugging

A systematic checklist for diagnosing and fixing performance issues in apps that combine React state updates with a Three.js WebGL renderer.

## Common Patterns

### 1. WebGL Shader Runs Full-Tilt While Invisible

**Symptom:** GPU usage stays high even when modal/overlay covers the canvas or the tab is backgrounded.

**Fix:**
- Add a `paused` flag to the animation loop
- Skip `renderer.render()` when paused
- Pause triggers: gallery modal open event, `document.hidden`
- Resume triggers: modal close, tab becomes visible

```ts
let paused = false;
const onVis = () => { paused = document.hidden; };
const onModal = () => { paused = true; };
const onModalClose = () => { paused = false; };
document.addEventListener('visibilitychange', onVis);
window.addEventListener('gallery-modal-open', onModal);
window.addEventListener('close-gallery-modal', onModalClose);

const animate = () => {
  rafRef.current = requestAnimationFrame(animate);
  if (paused) return;
  // ... render
};
```

**Also:** Reduce `renderer.setPixelRatio()`. On Retina displays, `Math.min(dpr, 2)` renders 4× the pixels of standard displays. `Math.min(dpr, 1)` cuts GPU workload in half with minimal visual difference on complex shaders.

### 2. `backdrop-filter: blur()` Over Animated Canvas

**Symptom:** Desktop lag when scrolling/opening panels that use backdrop-filter while the WebGL canvas is active.

**Root cause:** `backdrop-filter` re-samples and blurs everything behind the element every frame. When the backdrop is a continuously-animating WebGL shader, each blurred panel re-runs a large blur pass at 60fps.

**Fix:** Replace `backdrop-filter` with solid/high-alpha backgrounds when layered over animated content:
- Before: `background: rgba(x,y,z,.9); backdropFilter:'blur(12px)'`
- After: `background: rgba(x,y,z,.97)` — visually near-identical, no blur cost

### 3. Expensive Computation on Every Render

**Symptom:** Interaction (mouse move in modal) is laggy.

**Check:** Is a heavy computation (e.g., processing a 1.2MB dataset) called during every render cycle?

**Fix:** Lazy-load or memoize:
- Before: `materials={getMaterials()}` (called every render)
- After: `materials={editMode ? getMaterials() : []}` (only when editor is open)
- Or use `useMemo()` with the correct dependency array

### 4. Duplicate rAF Engines

**Symptom:** Two animation loops running simultaneously, both writing to the same DOM nodes.

**Root cause:** A custom cursor hook (`useCustomCursor`) is called from two components that mount at the same time (parent + child).

**Fix:** Singleton pattern using a `useRef` flag:

```ts
const startedRef = useRef(false);
useEffect(() => {
  if (startedRef.current) return;
  startedRef.current = true;
  // ... animation loop setup
}, []);
```

### 5. `mix-blend-mode` Performance Cost

**Symptom:** Cursor movement is janky, especially over animated content.

**Root cause:** `mix-blend-mode` forces the element onto its own compositing layer and repaints the blended region against everything beneath it on every mouse move.

**Fix:** Remove `mix-blend-mode` from elements that move every frame. Use a solid color or opacity instead.

### 6. ScrollTrigger Kills All Triggers Globally

**Symptom:** Other sections' scroll animations stop working after one section unmounts.

**Root cause:** `ScrollTrigger.getAll().forEach(t => t.kill())` kills EVERY trigger on the page.

**Fix:** Track only the triggers this component created:

```ts
const myTriggers: ScrollTrigger[] = [];
const tween = gsap.fromTo(el, ...);
if (tween.scrollTrigger) myTriggers.push(tween.scrollTrigger);
return () => myTriggers.forEach(t => t.kill());
```

## Audit Order (highest impact first)

1. WebGL shader never pauses → **HIGH** (biggest GPU drain)
2. backkdrop-filter over animated canvas → **HIGH**
3. Expensive per-render computation → **HIGH**
4. Duplicate rAF engines → **MEDIUM**
5. mix-blend-mode → **MEDIUM**
6. ScrollTrigger global kill → **LOW**

Apply fixes in this order — stop after the top 2-3 and re-test. The marginal gain from MEDIUM/LOW items may not justify the code churn.
