"""HTML/CSS Audit — Python analysis templates.

Usage: pipe HTML content to these scripts:
  curl -sL '<URL>' | python3 check.py MODE

Replace MODE with: tag-balance, section-drift, inline-styles, dup-ids
"""

import sys
import re
from collections import Counter


def tag_balance(html):
    """Count opening vs closing tags, report mismatches."""
    tags = [
        'div', 'section', 'table', 'header', 'footer', 'span', 'p',
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'a',
        'b', 'strong', 'i', 'em', 'tbody', 'thead', 'tr', 'td', 'th',
        'svg', 'g', 'path', 'rect', 'defs', 'clipPath',
        'style', 'link', 'meta', 'title', 'head', 'body', 'html',
        'img', 'br', 'hr',
    ]
    print('=== TAG BALANCE ===')
    problems = 0
    for t in tags:
        opens = len(re.findall(rf'<{t}[\\s>]', html))
        closes = len(re.findall(rf'</{t}>', html))
        if opens != closes:
            problems += 1
            note = ''
            if t in ('img', 'br', 'hr', 'input', 'meta', 'link'):
                note = ' (void element — no close expected)'
            print(f'  {t}: {opens} opens, {closes} closes (diff: {opens-closes}){note}')
    if problems == 0:
        print('  All tags balanced.')


def section_drift(html):
    """Check <!-- SECTION N: --> comments vs <h2>N.</h2> numbers."""
    print('=== SECTION NUMBERING DRIFT ===')
    for m in re.finditer(r'SECTION (\d+):', html):
        sn = int(m.group(1))
        pos = m.start()
        rest = html[pos:pos + 800]
        hm = re.search(r'<h2[^>]*>(\d+)\\.', rest)
        h2n = int(hm.group(1)) if hm else None
        is_part = 'الجزء' in rest[:200] or 'PART' in rest[:200]
        if h2n:
            match = '✓' if sn == h2n else '✗'
            print(f'  Sec {sn:2d} → h2 #{h2n} {match}')
        elif is_part:
            print(f'  Sec {sn:2d} → (PART divider — no numbered h2)')
        else:
            print(f'  Sec {sn:2d} → (no h2 found)')


def inline_styles(html):
    """Count inline style= attributes vs CSS class usage."""
    print('=== INLINE STYLES ===')
    inline_count = len(re.findall(r'style=\"', html))
    class_count = len(re.findall(r'class=\"', html))
    print(f'  style=" attributes: {inline_count}')
    print(f'  class=" attributes: {class_count}')
    ratio = inline_count / max(class_count, 1)
    print(f'  Inline-to-class ratio: {ratio:.2f}')
    if inline_count > 50:
        print('  ⚠ High inline style count — CSS classes being bypassed.')
    if ratio > 0.5:
        print('  ⚠ More than 1 inline per 2 class references — structural issue.')


def duplicate_ids(html):
    """Flag duplicate id attributes."""
    print('=== DUPLICATE IDS ===')
    ids = re.findall(r'id=\"([^\"]+)\"', html)
    dupes = [(k, v) for k, v in Counter(ids).items() if v > 1]
    if dupes:
        for id_, count in dupes:
            print(f'  id="{id_}" appears {count}x')
    else:
        print('  No duplicate IDs found.')


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'all'
    html = sys.stdin.read()

    modes = {
        'tag-balance': tag_balance,
        'section-drift': section_drift,
        'inline-styles': inline_styles,
        'dup-ids': duplicate_ids,
    }
    if mode in modes:
        modes[mode](html)
    elif mode == 'all':
        for fn in modes.values():
            fn(html)
    else:
        print(f'Unknown mode: {mode}')
        print(f'Available: {", ".join(modes.keys())}, all')
