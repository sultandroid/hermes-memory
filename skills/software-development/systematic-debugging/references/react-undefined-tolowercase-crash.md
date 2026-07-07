# React Crash: `.toLowerCase()` on `undefined`

## Symptom

Typing in a search/input field causes the entire page or component to **disappear** (unmount / crash). The page works fine when the field is empty.

## Root Cause

```javascript
// ❌ CRASHES when any field is undefined:
items.filter(item => 
  item.name.toLowerCase().includes(query)
)

// TypeError: Cannot read properties of undefined (reading 'toLowerCase')
```

When data comes from a dynamic source (API, Excel extraction, merged JSON), some fields may be `undefined` or `null` for certain items. If the filter/search function calls `.toLowerCase()` (or `.includes()`, `.trim()`, etc.) on a potentially undefined value, **the entire React render crashes** — causing the component tree to unmount.

## Why It "Disappears" Instead of Showing an Error

React's error boundary catches the crash during rendering. Without a custom error boundary, React unmounts the entire component tree below the crash point. The user sees a **blank/white page** or the **component disappears** — not a visible error.

## Debugging Checklist

- [ ] Does the crash only happen when the search/filter returns matches (not when empty)?
- [ ] Does a `.filter()` or `.map()` call process values that could be undefined?
- [ ] Does the code call `.toLowerCase()`, `.includes()`, `.trim()`, `.replace()` on a value?

## Fix Pattern

```javascript
// ✅ Safe — null/undefined fields are skipped:
items.filter(item => {
  const fields = [item.name, item.description, item.category];
  return fields.some(f => f && f.toLowerCase().includes(query));
});

// OR — optional chaining + default:
items.filter(item => 
  (item.name?.toLowerCase() || '').includes(query)
);

// OR — explicit guard:
items.filter(item => {
  if (!item.name) return false;
  return item.name.toLowerCase().includes(query);
});
```

## Why This Happens With Merged/Extracted Data

- Data from Excel extraction often has null fields
- Merged JSON datasets may have different field shapes per item
- Normalized field names (`colour` vs `Colour`) may not match all items
- Items from different schedule types have different fields

## Affected UX Patterns (This Session)

| Component | Trigger | Fix |
|-----------|---------|-----|
| EditorOverlay (MaterialPicker) | Typing in search | Added null guard on each field |
| Schedule.tsx table filter | Typing in search | `fields.some(f => f && f.includes(q))` |
| Gallery.tsx sidebar filter | Typing in search | Same pattern |

## Lesson

**Always null-guard `.toLowerCase()` calls** in filter/search functions when data comes from external sources (Excel, API, merged JSON). The data WILL have undefined fields for some items.

Use `fields.some(f => f && f.toLowerCase().includes(q))` as the standard safe pattern.

## Related

- `references/css-pointer-events-blocking-clicks.md` — another "component disappears" cause
- MDN: [TypeError: Cannot read properties of undefined](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Errors/Cannot_read_property)
