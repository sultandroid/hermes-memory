# Custom Event Cross-Component Communication

## Problem

Two sibling React components need to communicate (Component A triggers an action in Component B) but they're not connected via parent/child props, and adding a shared state manager (Context, Redux) is overkill.

Common scenario: clicking a card in `Materials` section should switch the schedule in `Schedule` section and scroll to it.

## Solution: Custom DOM Events

Use `window.dispatchEvent` + `window.addEventListener` with `CustomEvent`.

### Emitter (Component A)

```tsx
const handleCardClick = (scheduleName: string) => {
  // Optionally persist to sessionStorage for page-reload resilience
  sessionStorage.setItem('selected_schedule', scheduleName);
  
  // Dispatch custom event
  window.dispatchEvent(new CustomEvent('schedule-change', { detail: scheduleName }));
  
  // Navigate
  document.getElementById('schedule')?.scrollIntoView({ behavior: 'smooth' });
};
```

### Listener (Component B)

```tsx
const [activeSchedule, setActiveSchedule] = useState(
  () => sessionStorage.getItem('selected_schedule') || 'Default'
);

useEffect(() => {
  const handler = (e: Event) => {
    const detail = (e as CustomEvent).detail;
    if (detail) setActiveSchedule(detail);
  };
  window.addEventListener('schedule-change', handler);
  return () => window.removeEventListener('schedule-change', handler);
}, []);
```

## Why This Works

- **No prop drilling** — sibling components don't need a shared parent to wire them
- **No extra library** — `CustomEvent` is native DOM API
- **Clean teardown** — the `useEffect` cleanup removes the listener on unmount
- **Type-safe** — `(e as CustomEvent).detail` gives typed access to the payload
- **Decoupled** — the emitter doesn't need to know if the listener exists

## When NOT to Use Custom Events

| Use Case | Better Approach |
|----------|---------------|
| Parent→child data flow | Props |
| Deeply nested state | Context / Redux / Zustand |
| Form state | React Hook Form |
| Real-time updates (WebSocket) | Dedicated event bus or RxJS |
| Many-to-many communication | Context or state manager |

## Debugging Custom Events

In browser console:
```javascript
// Listen for all custom events
window.addEventListener('schedule-change', console.log);
// Or monitor all custom events
monitorEvents(window, ['schedule-change']);
```

To verify a listener exists:
```javascript
// Check if listener is registered (DevTools → Event Listeners tab)
// Or dispatch a test event and check if the handler fires
```

## Related

- MDN: [CustomEvent](https://developer.mozilla.org/en-US/docs/Web/API/CustomEvent)
- MDN: [dispatchEvent](https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/dispatchEvent)
