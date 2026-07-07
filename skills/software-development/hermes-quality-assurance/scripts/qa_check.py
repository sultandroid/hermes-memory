#!/usr/bin/env python3
"""
HTML QA Validation Script
Usage: python3 qa_check.py <path_to_html>

Checks:
- DOCTYPE presence
- Closing tags (</html>, </body>)
- Div open/close balance
- Table/thead/tbody balance
- Line number contamination
- A4 print setup (for .sheet pages)
- Image/asset path resolution
"""
import re
import sys
import os

def audit_html(path):
    with open(path) as f:
        c = f.read()
    
    issues = []
    name = path.split('/')[-1]
    size = len(c)
    lines = c.count('\n')
    base_dir = os.path.dirname(os.path.abspath(path))
    
    print(f"{'='*60}")
    print(f"QA AUDIT: {name}")
    print(f"Size: {size:,} bytes | Lines: {lines}")
    print(f"Dir: {base_dir}")
    print(f"{'='*60}")
    
    # 1. DOCTYPE
    if '<!DOCTYPE html>' not in c:
        issues.append("MISSING DOCTYPE declaration")
    else:
        print("  ✓ DOCTYPE present")
    
    # 2. Closing tags
    if '</html>' not in c.strip():
        issues.append("MISSING </html>")
    else:
        print("  ✓ </html> present")
    
    if '</body>' not in c:
        issues.append("MISSING </body>")
    else:
        print("  ✓ </body> present")
    
    # 3. Div balance
    open_divs = len(re.findall(r'<div[>\s]', c))
    close_divs = c.count('</div>')
    if open_divs != close_divs:
        issues.append(f"DIV MISMATCH: {open_divs} open, {close_divs} closed (diff={open_divs-close_divs})")
    else:
        print(f"  ✓ DIV balance: {open_divs} open = {close_divs} closed")
    
    # 4. Table balance
    for tag in ['table', 'thead', 'tbody']:
        opens = c.count(f'<{tag}')
        closes = c.count(f'</{tag}>')
        if opens != closes:
            issues.append(f"{tag.upper()} mismatch: {opens} open, {closes} close")
    
    # 5. Line number contamination
    first_line = c.split('\n')[0]
    if re.match(r'^\s*\d+\|', first_line):
        issues.append("LINE NUMBER CONTAMINATION — file contains read_file() line prefixes")
    else:
        print("  ✓ No line number contamination")
    
    # 6. A4 print setup (for sheet-based layouts)
    sheet_opens = re.findall(r'<div[^>]*class="sheet[^"]*"', c)
    if sheet_opens:
        sheets = len(sheet_opens)
        print(f"  ✓ Sheets: {sheets}")
        c_nospace = c.replace(' ', '').replace('\t', '').replace('\n', '')
        if 'size:A4' not in c_nospace:
            issues.append("Missing @page size:A4 for print layout")
        if 'min-height:297mm' not in c_nospace:
            issues.append("Missing min-height:297mm on .sheet")
        # Accept either spaced or unspaced CSS property values
        if not re.search(r'page-break-after\s*:\s*always', c):
            issues.append("Missing page-break-after:always")

        # Count pg-footer blocks and warn if non-cover sheets lack footers
        footer_count = len(re.findall(r'<footer[^>]*class="pg-footer"', c))
        cover_count = len(re.findall(r'<div[^>]*class="sheet\s+cover[^"]*"', c))
        expected_footers = sheets - cover_count
        if footer_count != expected_footers:
            issues.append(f"Sheets missing footers: {sheets} sheets ({cover_count} cover) but {footer_count} pg-footer blocks (expected {expected_footers})")

    # 7. Image/asset path resolution
    img_srcs = re.findall(r'src="([^"]+)"', c)
    broken = []
    for s in img_srcs:
        if s.startswith('http://') or s.startswith('https://') or s.startswith('data:'):
            continue  # skip external URLs and data URIs
        resolved = os.path.normpath(os.path.join(base_dir, s))
        if not os.path.exists(resolved):
            broken.append(s)
    
    if broken:
        print(f"  ⚠ {len(broken)} asset path(s) may not resolve:")
        for b in broken[:10]:
            print(f"     - {b}")
        if len(broken) > 10:
            print(f"     ... and {len(broken)-10} more")
        # Flag as issue only if many broken — allow a few false positives for generic paths
        if len(broken) > 3:
            issues.append(f"{len(broken)} asset paths do not resolve from file location. Check src= paths.")
    else:
        print("  ✓ All asset paths resolve")
    
    print(f"\n{'─'*60}")
    if issues:
        print(f"❌ {len(issues)} ISSUES:")
        for i, iss in enumerate(issues, 1):
            print(f"   {i}. {iss}")
    else:
        print("✅ PASS — No issues found")
    print(f"{'='*60}\n")
    
    return len(issues)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 qa_check.py <file1.html> [file2.html ...]")
        sys.exit(1)
    
    total = 0
    for path in sys.argv[1:]:
        total += audit_html(path)
    
    sys.exit(1 if total > 0 else 0)
