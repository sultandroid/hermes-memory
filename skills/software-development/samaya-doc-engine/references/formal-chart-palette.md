# Formal Engineering Chart Palette — Rationale & Application

## Why the change

The initial Samaya Document Framework used bright/saturated colors (`#0284C7` sky blue, `#F59E0B` amber, `#10B981` green) that looked "shiny" and unprofessional in print. The user rejected them as inappropriate for formal engineering technical proposals.

## The principle

All colors in the formal palette must pass the "government tender submission" test — imagine the document printed in grayscale on a desk in a procurement office. The colors should:
- Be distinguishable in grayscale (different luminance values)
- Never be distracting or draw attention away from content
- Suit a formal engineering / construction context
- Work with `-webkit-print-color-adjust: exact`

## Color mapping (bright → formal)

| Old (bright)     | New (formal)     | Use case                            |
|------------------|------------------|-------------------------------------|
| `#0284C7` sky   | `#1E40AF` navy   | Accent bars, secondary headers      |
| `#0369A1` sky   | `#1E3A5F` navy   | SVG box fills                       |
| `#F59E0B` amber | `#92400E` brown  | Highlights, warnings, review gates  |
| `#EA580C` orange| `#92400E` brown  | Warnings, attention markers         |
| `#10B981` green | `#065F46` teal   | Approval, completion, pass status   |
| `#16A34A` green | `#065F46` teal   | Completion, go-to-green             |
| `#6366F1` indigo| `#4338CA` indigo | Chart series, secondary data        |
| `#7C3AED` purple| `#4338CA` indigo | Tertiary data                       |
| `#d91e2e` red   | `#991B1B` burgundy| Rejection, fail, critical           |
| `#EF4444` red   | `#991B1B` burgundy| Alerts, errors                      |
| `#1D8649` green | KEEP             | Samaya tree logo (brand color, exempt)|
| `#14B8A6` teal  | `#0F766E` teal   | Chart series 6                      |
| `#8B5CF6` purple| `#6D28D9` purple | Chart series 7                      |

## Implementation

When creating SVGs, use the actual hex values (not CSS variables — SVG doesn't inherit `var()` reliably):

```svg
<!-- CORRECT for formal engineering doc -->
<rect fill="#1E40AF" .../>
<text fill="#92400E" .../>

<!-- WRONG — shiny/bright, user rejected -->
<rect fill="#0284C7" .../>
<text fill="#F59E0B" .../>
```

## Global color replacement script

When bulk-updating colors across all SVG charts in a document:

```python
formal_map = {
    '#0284C7': '#1E40AF',   # sky → navy
    '#F59E0B': '#92400E',   # amber → brown
    '#10B981': '#065F46',   # green → teal
    '#16A34A': '#065F46',   # green → teal
    '#6366F1': '#4338CA',   # indigo → deeper indigo
    '#7C3AED': '#4338CA',   # purple → deeper indigo
    '#EA580C': '#92400E',   # orange → brown
    '#d91e2e': '#991B1B',   # red → burgundy
}

for f in page_files:
    content = open(f).read()
    for old, new in formal_map.items():
        content = content.replace(old, new)
    open(f, 'w').write(content)
```

**Caveat:** Ensure brand logo colors (e.g., `#1D8649` Samaya tree) are NOT replaced by the green→teal mapping. Either exclude the cover page or add the brand color to an exclusion list.
