# A4 Pipeline Validation Script — Reference

Canonical `scripts/validate.js` pattern.

## Check Categories (30+ checks)

### File Integrity
- `dist/index.html` exists
- File size < 800KB

### HTML Structure
- `<!DOCTYPE html>` present
- `<html lang="ar"` 
- `<meta charset="UTF-8">`
- `<meta name="viewport">`
- `<meta name="description">`
- Google Fonts link
- `<link rel="stylesheet" href="styles/a4.css">`
- `<main>` tag present

### Semantic HTML
- At least 1 `<h1>`
- At least 1 `<h2>`
- At least 1 `<header>`, `<footer>`, `<section>`

### CSS Correctness
- `@page { size: A4 }` — NOT `A4 portrait`
- `.page` has `210mm` width and `297mm` height
- `page-break-after` rule present
- `box-sizing: border-box`
- `print-color-adjust` + `-webkit-print-color-adjust`
- CSS variables (`:root`) present

### Known Issues (zero tolerance)
- No `SVG width="auto"` anywhere
- No `@page { size: A4 portrait }` anywhere

### Placeholder Leakage
- No remaining `{{...}}` tokens in output

### Page Structure
- `.page` sections count > 10
- `<section>` opens == closes (balanced)
- Footer elements present (> 10)

### Page Numbering
- Footers found (> 10)
- Last footer: `page_num == total_pages`
- No duplicate page number strings
- Sequential numbers (allow gaps for non-footer pages)

## Example Validation Flow

```javascript
let PASS = 0, FAIL = 0;

function check(name, condition) {
  if (condition) { PASS++; console.log(`  PASS ${name}`); }
  else { FAIL++; console.log(`  FAIL ${name}`); }
}

// Usage
check('File exists', fs.existsSync(distFile));
check('<h1> present', /<h1[> ]/.test(html));
check('No SVG width=auto', !/width="auto"/.test(html));
```

## Exit Code Convention

- `process.exit(0)` — all critical checks pass (warnings OK)
- `process.exit(1)` — at least one critical check failed

## Duplicate Page Number Detection

```javascript
const seen = {};
let hasDuplicates = false;
pageNums.forEach((pn, i) => {
  if (seen[pn]) { hasDuplicates = true; warn(`Duplicate: ${pn}`); }
  seen[pn] = true;
});
check('No duplicate page numbers', !hasDuplicates);
```

Note: this checks the FULL footer string (e.g. `صفحة 20 / 41`), not just the number. Two different pages with same number AND same total WILL be caught.
