# A4 Pipeline Build Script — Reference

Canonical `scripts/build.js` pattern for a manifest-driven A4 document build pipeline.

## Core Algorithm

```javascript
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const SECTIONS = path.join(ROOT, 'sections');
const DIST = path.join(ROOT, 'dist');
const TEMPLATE = path.join(ROOT, 'template.html');

// Load manifest
const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, 'manifest.json'), 'utf-8'));

// 1. Assign section numbers (cover + dividers get empty string)
let counter = 0;
manifest.sections.forEach(sec => {
  if (sec.type === 'cover' || sec.type === 'divider') { sec.num = ''; return; }
  counter++;
  sec.num = counter;
});

// 2. Render each section partial
function renderSection(sec, pageNum, totalPages) {
  const partialPath = path.join(SECTIONS, `${sec.id}.html`);
  if (!fs.existsSync(partialPath)) { return ''; }
  let html = fs.readFileSync(partialPath, 'utf-8');
  const data = {
    section_number: sec.num || '',
    page_number: pageNum ?? '{{page_number}}',
    total_pages: totalPages ?? '{{total_pages}}',
    doc_code: 'SMP-RCRC-TP-AR-001',
    rev: '01',
    title_ar: sec.title_ar || '',
    title_en: sec.title_en || '',
    short_title_ar: sec.short_title_ar || '',
    chip_text: CHIP_MAP[sec.id] || '',
  };
  return html.replace(/\{\{(\w+)\}\}/g, (m, k) => data[k] ?? m);
}

// 3. Assemble into template
const body = manifest.sections.map(sec => renderSection(sec, pageNum, totalPages)).join('\n');
const finalHtml = fs.readFileSync(TEMPLATE, 'utf-8').replace('{{body}}', body);

// 4. Write output
fs.writeFileSync(path.join(DIST, 'index.html'), finalHtml);
```

## Placeholder Replacement

Use a single regex pass — NOT multiple `str.replace()`:

```javascript
const PLACEHOLDER_REGEX = /\{\{(\w+)\}\}/g;
function replacePlaceholders(str, data) {
  return str.replace(PLACEHOLDER_REGEX, (match, key) => {
    if (data[key] !== undefined) return String(data[key]);
    return match; // preserve unknown placeholders as-is
  });
}
```

## Two-Pass Rendering Pattern

```javascript
// Pass 1: Render with placeholder page numbers
const firstPass = buildDocument(undefined);
fs.writeFileSync('dist/index.html', firstPass);

// Optional Puppeteer measurement
const totalPages = await measurePages(); // returns N

// Pass 2: Re-render with real page numbers
const finalHtml = buildDocument(totalPages);
fs.writeFileSync('dist/index.html', finalHtml);
```

## Page Number Closure (avoids cascade bugs)

```javascript
let pageNum = 0;
const finalSections = [];
manifest.sections.forEach(sec => {
  if (sec.type === 'cover' || sec.type === 'divider') { pageNum++; /* no footer num */ }
  else { pageNum++; finalSections.push(renderSection(sec, pageNum, totalPages)); }
});
```

Always increment `pageNum` for EVERY section (including cover + dividers) so the absolute page count matches. Cover and dividers get no `{{page_number}}` in their footer (no footer at all) but still consume a position.
