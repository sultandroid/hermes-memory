# Odoo Task Description Formatting

## Rules (from user preference)

1. **No icons, no emoji** — no checkmarks, stars, arrows, progress dots, or any Unicode decorative characters
2. **No AI fingerprint** — no "I have prepared", "this document covers", "the following sections will cover", "as shown above", "it is worth noting"
3. **Plain HTML structure** — Odoo description field accepts HTML. Use clean tags only:
   - `<p>` for paragraphs
   - `<b>` for section headings (not `<h1>`-`<h6>`)
   - `<ul><li>` for bullet lists
   - No `<br>` — use `<p>` blocks instead
4. **Short sections** — 3-5 bullets per section max
5. **No decorative borders, dividers, or horizontal rules**

## Template

```python
description = """<p>One-line summary of the task.</p>

<p><b>Section Heading</b></p>
<ul>
<li>Item one</li>
<li>Item two</li>
<li>Item three</li>
</ul>

<p><b>Another Section</b></p>
<ul>
<li>Item one</li>
<li>Item two</li>
</ul>"""
```

## Common mistakes to avoid

| Mistake | Example | Fix |
|---------|---------|-----|
| Icons/emoji | "✅ Done", "🔴 Critical" | Remove — use plain text labels |
| AI intro | "I have prepared the following report" | Start with the fact directly |
| Meta-commentary | "As shown in the section above" | Just state the fact |
| Decorative HTML | `<hr>`, `&mdash;`, `&rarr;` | Use plain text or `<p>` breaks |
| Over-nesting | 4+ levels of bullets | Flatten to 2 levels max |
