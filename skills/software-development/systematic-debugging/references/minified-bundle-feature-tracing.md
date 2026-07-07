# Tracing Features in Minified Production JS Bundles

## When to Use

You need to find, understand, or disable a feature in a deployed SPA (React/Vue/Vite) but:
- You don't have access to the source code
- The minified JS bundle is all you have
- You need to locate a specific button, component, or behavior

## Step-by-Step Workflow

### 1. Identify the Bundle URL

From the page source, find the `<script>` tag with `type="module"`:

```bash
curl -s 'https://example.com/page/' | grep -o 'src="[^"]*\.js"'
```

This gives you the `./assets/index-XXXXX.js` path relative to the page.

### 2. Download the Bundle

```bash
curl -sL 'https://example.com/assets/index-XXXXX.js' -o bundle.js
wc -c bundle.js  # Expect 1-3MB for a real SPA
```

### 3. Search for Direct Strings

If you know the feature exists, search for its most specific string:

```bash
# Button text (Unicode emojis work)
rg -o '.{0,100}🖨️ Print PDF.{0,100}' bundle.js

# API endpoints
rg -o '.{0,50}/api/save.{0,50}' bundle.js

# window.print() — browser print trigger
rg -n 'window\.print' bundle.js

# Known function names
rg -n 'toPdf|toPDF|downloadPdf|exportPdf' bundle.js
```

### 4. Extract Context Around Matches

Minified bundles have no newlines. Use Python for context extraction:

```python
with open('bundle.js') as f:
    content = f.read()

idx = content.find('window.print()')
start = max(0, idx - 500)
end = min(len(content), idx + 1500)
print(content[start:end])
```

### 5. Trace Minified Variable Names

Production bundles use single-letter variable names (`S`, `w`, `ZB`, etc.) that change per build. The technique:

**Forward (from state to render):**
- Find `useState` calls: `[S,w]=Y.useState(!1)` → `S` is the state, `w` is the setter
- Search for where `w(true)` or `w(!0)` is called (sets state to true)
- Find the onclick handler that calls it → that's your button

**Backward (from render to state):**
- Find the JSX render: `S&&k.jsx("div",...)` → the condition `S` is your state
- Find where `S` was declared: look for `[S,...]=Y.useState(` before this point

### 6. Find the Button/Trigger

Once you know the state variable name (`S`), search for where it's set to true:

```bash
# In a minified bundle, the setter is usually `w(!0)` or `w(true)`
rg -o '.{0,100}w\(!0\).{0,100}' bundle.js
# Or for toggling:
rg -o '.{0,100}w\(!S\).{0,100}' bundle.js
```

The button's text will be nearby in the JSX:

```javascript
// Example: a button with emoji and text
// Look for the parent k.jsx("button", {.., children: "🖨️ Print PDF"})
```

### 7. Verify Button Exists in DOM

```javascript
// In browser console, find the button
document.evaluate(
  "//button[contains(text(),'Print')]",
  document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null
).singleNodeValue;
```

## Pattern: PrintView Component in Minified JS

A common pattern for print-to-PDF features:

```javascript
// Component definition (name varies per build)
function ZB({viewTitle, viewDesc, imageSrc, hotspots, materials, rev, date, onClose}) {
  const imgRef = useRef(null);
  const hasPrinted = useRef(false);
  
  useEffect(() => {
    if (hasPrinted.current) return;
    hasPrinted.current = true;
    const img = imgRef.current;
    const printFn = () => setTimeout(() => window.print(), 600);
    img ? img.complete ? printFn() : img.onload = printFn : printFn();
  }, []);
  
  useEffect(() => {
    const close = () => onClose();
    window.addEventListener("afterprint", close);
    return () => window.removeEventListener("afterprint", close);
  }, [onClose]);
  
  return (
    <div style={{background: '#fff', padding: '20mm', ...}}>
      <img ref={imgRef} src={imageSrc} />
      {/* hotspot pins with numbered badges */}
      {/* legend table */}
    </div>
  );
}
```

The trigger in the parent component:

```javascript
// State declaration
const [showPrint, setShowPrint] = useState(false);

// Button
<button onClick={() => setShowPrint(true)}>🖨️ Print PDF</button>

// Overlay — conditionally rendered
{showPrint && <PrintView {...} onClose={() => setShowPrint(false)} />}
```

## Disabling a Feature Without Source Access

If you need to remove/hide a feature and can't rebuild, inject CSS via the browser or a custom stylesheet:

```css
/* Hide by button text */
button:has(> :contains("🖨️ Print PDF")) { display: none !important; }

/* Or by parent container */
[class*="print"] { display: none !important; }
}

```

For a permanent fix, modify the source and rebuild. This technique is for **analysis only** — don't patch minified bundles directly.

## Pitfalls

- **Variable names change per build** — `ZB` in one build is `xx` in the next. Never hardcode minified names.
- **Search by strings that cross the source → build boundary intact**: button text, URLs, localStorage keys, API endpoints, known class names.
- **Large bundles (2MB+) can make `rg` output overwhelming** — use `head -N` and specific patterns to narrow.
- **Component may be defined but never used** — always verify by checking the DOM for the button.
- **Build hash changes** every deploy — the URL `index-XXXXX.js` changes. Always re-fetch.
