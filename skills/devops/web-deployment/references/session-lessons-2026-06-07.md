# Session Lessons: 2026-06-07

## Image reorganization — keep filenames identical

When reorganizing images into section-based folders:

- **DO NOT rename files** — keep exact filenames. Renaming (adding prefixes like `veneer-process-`) breaks all HTML/CSS references.
- Move files with `shutil.move()` or `mv`, preserving the original filename.
- After moving, update HTML/CSS paths to reflect the new directory only, never the filename.
- Build a `filename → new path` map from the filesystem, then do a regex replace across all HTML and CSS files.

## OneDrive copy timeout workaround

When copying assets from OneDrive-synced directories, `shutil.copy2()` may time out on large files. Use `ditto` as fallback:

```python
try:
    shutil.copy2(sp, dp)
except OSError:
    subprocess.run(["ditto", sp, dp], capture_output=True)
```

## External SVG via `<object>` tag

- Use `<object type="image/svg+xml" data="path/to/file.svg">` instead of inline SVG
- Benefits: cleaner HTML, SVG can be edited independently, browser caches it
- Always check XML validity before deploying: `python3 -c "import xml.etree.ElementTree as ET; ET.parse('file.svg')"`
- Watch for unescaped `&` in `aria-label` attributes — must use `&amp;` in XML attributes
- Use CSS variables for the SVG style block, not inline styles on elements
- Scale with `viewBox` and let CSS `width: 100%; height: 100%` on the object tag handle sizing

## CSS variable URL resolution

`url()` inside CSS custom properties resolves relative to the CSS file where `var()` is used, NOT where the property is defined. This can cause broken image paths. Safer: set `background-image` directly via inline `style` attribute instead of `var(--custom-prop)`.

## Font switch pattern

When switching fonts site-wide:
1. Update all CSS `font-family` declarations (search for old font name)
2. Update the Google Fonts `<link>` in HTML
3. Fix the URL format: Google Fonts API expects `wght@...` (with `@`), not `wght;...` (with semicolon)
4. Verify no hardcoded references remain