# CSS `pointer-events: none` Blocking Click Handlers

## Symptom

Click handlers (`onClick`, `onMouseDown`, etc.) on React components **never fire**, even though the element is visually present and positioned correctly. The element is visible but events pass through it.

## Root Cause

```css
.clickable-element {
  pointer-events: none; /* ← THIS */
}
```

`pointer-events: none` tells the browser to **pretend the element doesn't exist for all mouse/touch events**. The browser delivers the event to whatever element is **behind** this one, never to this element.

The React `onClick` handler is never called because the JS event never reaches the DOM node.

## Common Scenarios

| Scenario | Why `pointer-events: none` was added | Fix |
|----------|--------------------------------------|-----|
| Hotspot pins on an image overlay | To let clicks pass through to the image underneath | Change to `cursor: pointer` (remove the property) |
| Tooltip cards | To keep hover working on elements behind the card | Toggle: `.pinned { pointer-events: auto }` when frozen |
| Custom overlays | To prevent blocking interaction with underlying UI | Use `isClickable` prop to set `pointer-events: auto` conditionally |
| Decorative elements | To make them non-interactive | Don't attach onClick to them — or use CSS class toggle |

## Debugging Checklist

- [ ] Is the element **visible** (not `display: none`, `opacity: 0`)?
- [ ] Does the element have `pointer-events: none` in any CSS rule?
- [ ] Does a parent element have `pointer-events: none` that children inherit?
- [ ] Is there a dialog/overlay between the click and the element (z-index issue)?
- [ ] Is the click handler `onClick` (React) vs `onclick` (native)? React uses synthetic events.
- [ ] Does `e.stopPropagation()` prevent the event from bubbling to a parent listener?

## Test

```javascript
// Add to the element's click handler:
onClick={(e) => {
  console.log('CLICK FIRED', e.target, e.currentTarget);
  e.stopPropagation();
  handlePinClick(hs);
}}
```

If the console.log never appears → **the event never reached the element**.

If it appears but the pin doesn't work → the event handler logic has a bug (check the handler code).

## Why This Sneaks Through

- **Visually the element looks clickable** (hover effect, cursor pointer expected)
- **The onClick handler looks correct** in JSX
- **The z-index is correct** (element is on top)
- **The element has the right dimensions and position**

The one invisible CSS property `pointer-events: none` is the only thing between a working click handler and a dead one.

## Related

- `references/web-event-not-firing.md` in this skill
- React docs: [Handling Events](https://reactjs.org/docs/handling-events.html)
- MDN: [pointer-events](https://developer.mozilla.org/en-US/docs/Web/CSS/pointer-events)
