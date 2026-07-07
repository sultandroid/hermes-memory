---
description: "Key lessons from the RCRC Exhibition Technical Proposal restructuring (2026-06-28)"
---

# RCRC Exhibition Restructure — Key Lessons

## 1. Simple Python Concat > Two-Pass Build

The two-pass build (Puppeteer + placeholder tokens + post-processing) was abandoned after producing broken section tags (`>>`) and timing out. The simple concat approach worked reliably:

base.html = DOCTYPE + head + CSS + body placeholder
pages/NN-title.html = one complete `<section class="page">` each
scripts/assemble.py = concatenates in order

**Key insight:** Since A4 pages use `page-break-after: always`, editing content within a page never changes its page number. Pre-numbered files stay valid.

## 2. Filesystem Slowness on macOS

Reading 49 files from ~/Documents/ took 44+ seconds in Node.js but <1s in Python. **Always use Python for file-I/O-heavy build scripts.**

## 3. Divider Pages → Part Banners

Workflow:
1. Delete divider file (pages/NN-part*-divider.html)
2. On the first content page after the divider, add a dark navy banner before content:

```html
<div style="background:var(--primary);color:#fff;padding:8px 12px;text-align:center">
  <div style="font-family:var(--font-arabic);font-size:0.9rem;font-weight:700">الجزء الثاني — المنهجيات التنفيذية</div>
  <div style="font-family:var(--font-heading);font-size:0.55rem;color:rgba(255,255,255,0.6);text-transform:uppercase">Part 2 — Execution Methodologies</div>
</div>
```

3. Renumber all remaining pages via Python closure-based counter
4. Update all footer totals (/49 → /45)

## 4. Flexbox Fills Sparse Pages — REJECTED BY USER

**The flex approach was tested, deployed, and REJECTED.** `display:flex; flex-direction:column` with `flex:1 1 auto` on content divs creates a gap between the title (h2-row) and the content below it. The user explicitly complained: "content should start after the title direct why you leave white spaces."

**Lesson: Block layout only for `.page`.** Content flows naturally after the title. The `.h2-row`'s `margin-bottom:6px` provides enough spacing. If a page has genuinely too little content, add more content (KPIs, data tables, detail paragraphs) rather than flex-stretching.

**Current correct CSS:**
```css
.page{position:relative;width:210mm;height:297mm;padding:12mm 16mm;margin:6mm auto;background:#FFFFFF;overflow:hidden;page-break-after:always;break-after:page;box-sizing:border-box}
```
No `display:flex`. No `flex-direction:column`. No `flex:1 1 auto`.

## 5. Regex >> Bug

When using re.sub() on section tags, the regex must consume the ENTIRE opening tag including >.
BAD: `/<section[^>]*class="[^"]*page[^"]*"/g` — produces `>>` at end of tag
GOOD: `/<section[^>]*class="[^"]*page[^"]*"[^>]*>/g`

Verify zero `class="page">>` in output.

## 6. Pre-Existing Malformations

Before splitting monolithic HTML, check for:
- h2-row opening on page N but closing on page N+1
- Footer before content in a section
- Content outside section tags
- Stray characters (s before section, missing <)

These must be fixed per-page — mechanical splitting preserves them.

## 7. Fixed Height vs Print Overflow

Use `height:297mm` with `overflow:hidden` on screen.
Use `overflow:visible;height:auto;min-height:297mm` in `@media print`.
