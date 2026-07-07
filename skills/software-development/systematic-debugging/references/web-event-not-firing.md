# DOM Event Not Firing: Debugging Checklist

When a React `onClick` (or any event handler) on a DOM element doesn't fire, the problem is almost never the JavaScript — **it's the CSS or DOM structure**.

## 1. Check `pointer-events` CSS Property

**Most common cause.** The element or a parent has `pointer-events: none`.

```css
/* ❌ KILLS all mouse/click/touch events on the element */
.my-element { pointer-events: none; }

/* ✅ Allows events */
.my-element { pointer-events: auto; }
/* or simply remove the pointer-events declaration */
```

### How it manifests:
- Element is visually present (you can see it)
- Element has an `onClick` handler in React
- Click does nothing — no console error, no state change
- **Hover/mousemove still works** if those events are captured by a parent

### Why it happens:
- `pointer-events: none` is set for aesthetic reasons (to let clicks pass through an overlay)
- A parent element (like a pin dot) inherits `pointer-events: none` from a CSS class
- The element INSIDE a `pointer-events: none` parent can override with `pointer-events: auto`, but the OUTER element itself cannot receive events if it has `pointer-events: none`

### Fix:
```diff
- .pin { pointer-events: none; }
+ .pin { cursor: pointer; }
```

## 2. Check `z-index` / Element Overlap

If `pointer-events` is fine, another element might be layered ON TOP of your click target.

- Check `z-index` values
- Check if a transparent overlay (backdrop, modal) covers the element
- Use browser DevTools → inspect to see what element is at the click position

## 3. Check `stopPropagation` on Parent

If a parent element calls `e.stopPropagation()`, events may not reach the child's handler.

But this is RARE in React since React uses event delegation. More commonly:
- A parent `onClick` with `stopPropagation` doesn't affect the child's own `onClick`
- But a parent `onMouseDown` with `stopPropagation` could block a click event

## 4. Check React Key / Reconciliation Issues

If the element is rendered conditionally or has a non-unique `key`, React may unmount it before the event fires.

## 5. Quick Diagnostic

```javascript
// Add onClick directly to the element for testing
onClick={(e) => {
  console.log('CLICKED', e.target);
  console.log('pointer-events style:', window.getComputedStyle(e.target).pointerEvents);
}}
```

## Case Study: Hotspot Pin Not Clickable

**Symptom:** Pins visible on an image. `onClick` handler attached. Hover works (tooltip appears via parent's `onMouseMove`). Click does nothing.

**Root cause:** `.hotspot-pin-modal { pointer-events: none; }` in CSS.

**Why it was there:** Originally placed to let clicks "pass through" pins to the image underneath. But the `onClick` on the pin itself is the intended interaction — the pin should RECEIVE clicks, not pass them through.

**Fix:** Changed to `cursor: pointer` (or removed `pointer-events: none` entirely).

**Lesson:**
- If an element needs to receive hover events (via parent's mousemove) AND click events (via its own onClick), `pointer-events: none` makes clicks impossible
- `pointer-events: none` is NOT the same as "invisible to events" — it's "transparent to ALL events"
- Always inspect the computed `pointer-events` value in DevTools before assuming the JS handler is wrong
