#!/usr/bin/env python3
"""
HTML → Samaya-branded DOCX converter.
Walks body in order, mapping h2/h3/h4/p/table/ul/ol/hr to SamayaDoc methods.
Handles inline bold/italic, nested HTML in cells, Arabic text, and
sustainability points-stripping pre-processing.

Usage:
  python3 html-to-docx-converter.py <input.html> <output.docx> [--strip-points] [--clean]

  --strip-points: remove all points-chasing / rating-tier language
                  (for sustainability docs where ER mandates code compliance only)
  --clean:        remove decorative symbols (§ · — – → × ° •) and AI-sounding
                  phrases ("this strategy reads", "the highest-impact", etc.)

Requires: python-docx, SamayaDoc template at OneDrive _Style-Guides path.
"""

import os, re, sys

# ── Config ──────────────────────────────────────────────────────
TEMPLATE_DIR = "/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide"
if not os.path.exists(TEMPLATE_DIR):
    TEMPLATE_DIR = "/Users/mohamedessa/Library/Group Containers/UBF8T346G9.OneDriveStandaloneSuite/OneDrive - SAMAYA INVESTMENT.noindex/OneDrive - SAMAYA INVESTMENT/Samaya/Technical Office/_Style-Guides/Doc Style Guide"
sys.path.insert(0, TEMPLATE_DIR)

from samaya_doc_template import SamayaDoc, SamayaColors
from docx.shared import RGBColor, Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH


# ── Helpers ─────────────────────────────────────────────────────

def cell_to_text(td_html: str) -> str:
    s = re.sub(r'<br\s*/?>', '\n', td_html, flags=re.IGNORECASE)
    s = re.sub(r'<[^>]+>', '', s)
    for e, c in [('&amp;','&'),('&lt;','<'),('&gt;','>'),('&quot;','"'),
                 ('&nbsp;',' '),('&mdash;',' '),('&ndash;',' '),
                 ('&middot;',' '),('&sect;','Sec '),('&rarr;','to'),
                 ('&hellip;',' '),('&times;','x'),('&deg;','deg'),
                 ('&plusmn;','+/-'),('&para;',' ')]:
        s = s.replace(e, c)
    s = re.sub(r'[ \t]+', ' ', s)
    s = re.sub(r'\n[ \t]+', '\n', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()


def html_to_segments(html_fragment: str):
    """Convert HTML fragment to list of {'text','bold','italic'} dicts."""
    s = re.sub(r'<br\s*/?>', '\n', html_fragment, flags=re.IGNORECASE)
    segments = []
    pos = 0
    bold_stack = [False]
    italic_stack = [False]

    def emit(text, bold, italic):
        if not text: return
        for e, c in [('&amp;','&'),('&lt;','<'),('&gt;','>'),('&quot;','"'),
                     ('&nbsp;',' '),('&mdash;',' '),('&ndash;',' '),
                     ('&middot;',' '),('&sect;','Sec '),('&rarr;','to'),
                     ('&hellip;',' '),('&times;','x'),('&deg;','deg'),
                     ('&plusmn;','+/-'),('&para;',' ')]:
            text = text.replace(e, c)
        parts = text.split('\n')
        for i, part in enumerate(parts):
            if i > 0:
                segments.append({'text': '\n', 'bold': bold, 'italic': italic})
            if part:
                segments.append({'text': part, 'bold': bold, 'italic': italic})

    tag_re = re.compile(r'<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>')
    while pos < len(s):
        m = tag_re.search(s, pos)
        if not m:
            emit(s[pos:], bold_stack[-1], italic_stack[-1])
            break
        if m.start() > pos:
            emit(s[pos:m.start()], bold_stack[-1], italic_stack[-1])
        closing = m.group(1) == '/'
        tag = m.group(2).lower()
        if tag in ('b','strong'):
            bold_stack.pop() if closing and len(bold_stack) > 1 else bold_stack.append(True)
        elif tag in ('i','em'):
            italic_stack.pop() if closing and len(italic_stack) > 1 else italic_stack.append(True)
        elif tag == 'br':
            emit('\n', bold_stack[-1], italic_stack[-1])
        pos = m.end()
    return segments


def parse_table(table_html: str):
    """Return (headers, rows) as lists of plain text strings."""
    thead = re.search(r'<thead[^>]*>(.*?)</thead>', table_html, re.IGNORECASE | re.DOTALL)
    tbody = re.search(r'<tbody[^>]*>(.*?)</tbody>', table_html, re.IGNORECASE | re.DOTALL)
    headers = []
    if thead:
        headers = [cell_to_text(t) for t in re.findall(r'<th[^>]*>(.*?)</th>', thead.group(1), re.IGNORECASE | re.DOTALL)]
    body = tbody.group(1) if tbody else table_html
    body = re.sub(r'<thead[^>]*>.*?</thead>', '', body, flags=re.IGNORECASE | re.DOTALL)
    rows = []
    for r in re.findall(r'<tr[^>]*>(.*?)</tr>', body, re.IGNORECASE | re.DOTALL):
        cells = re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', r, re.IGNORECASE | re.DOTALL)
        if cells:
            rows.append([cell_to_text(c) for c in cells])
    if not headers and rows:
        first = re.search(r'<tr[^>]*>(.*?)</tr>', body, re.IGNORECASE | re.DOTALL)
        if first and '<th' in first.group(1).lower():
            headers = [cell_to_text(t) for t in re.findall(r'<th[^>]*>(.*?)</th>', first.group(1), re.IGNORECASE | re.DOTALL)]
            rows = rows[1:]
    return headers, rows


def strip_points_language(html: str) -> str:
    """Remove all points-chasing / rating-tier language from sustainability docs.
    
    The ER mandates code compliance (Mostadam Manual + SBC 1001), NOT a rating
    tier or points target. This function strips Silver/Gold/45+/60+/target pts/
    stretch/credit pool language so the document reads as a compliance plan.
    """
    # DC block Rating tier
    html = re.sub(r'<div class="k">Rating tier</div><div>.*?</div>\s*', '', html)
    # Revision log
    html = html.replace('(e) Rating tier reframed as <b>Samaya voluntary aspiration</b> &mdash; ER does not mandate a Mostadam tier.',
                        '(e) Rating tier removed &mdash; ER does not mandate a Mostadam tier; strategy reframed as code compliance.')
    # Employer row
    html = html.replace('Endorses sustainability initiative + targeted points (ER &sect;3.7 Performance Req). Funds Mostadam certification.',
                        'Endorses sustainability initiative per ER &sect;3.7. Funds Mostadam certification.')
    # ER cross-ref
    html = html.replace('Compliance with sustainability requirements + targeted points (General Cleaning section &mdash; corrected from &sect;2.7 in C03)',
                        'Compliance with sustainability requirements (General Cleaning section &mdash; corrected from &sect;2.7 in C03)')
    # Snap cards
    html = re.sub(r'<div class="snap green">.*?</div>\s*', '', html)
    html = re.sub(r'<div class="snap amber">.*?</div>\s*', '', html)
    html = re.sub(r'<div class="snap"><div class="lbl">Design credits</div>.*?</div>\s*', '', html)
    html = re.sub(r'<div class="snap"><div class="lbl">Constr\. credits</div>.*?</div>\s*', '', html)
    # Orphan SILVER/GOLD
    html = re.sub(r'<div class="val">SILVER</div><div class="cap">.*?</div></div>\s*<div class="val">GOLD</div><div class="cap">.*?</div>', '', html)
    # ~X pts labels
    html = re.sub(r'<div style="font-family:\'Menlo\',monospace; font-size:0\.4rem; color:var\(--text-muted\);">~?\d+\s*pts?.*?</div>', '', html)
    # CREDIT POOL banner
    html = re.sub(r'<div style="border:1px solid var\(--primary\); padding:4px 9px; font-size:0\.5rem; color:var\(--primary\); margin:0 0 6px 0;">.*?</div>', '', html)
    # SVG text
    html = re.sub(r'<text[^>]*fill="#64748B"[^>]*>~\d+ of ~\d+.*?</text>', '', html)
    html = re.sub(r'<text[^>]*fill="#64748B"[^>]*>~\d+ pts?.*?</text>', '', html)
    # TOTAL POINTS row
    html = re.sub(r'<tr style="background:#0F766E;">.*?TOTAL POINTS.*?</tr>\s*', '', html)
    # ~X pts in RACI
    html = re.sub(r'\(~\d+\s*pts?\)\s*', '', html)
    # Silver commitment paragraph
    html = re.sub(r'<p>Single-page consolidation of every credit targeted.*?</p>', '', html)
    # Column headers
    html = html.replace('>Target pts<', '>Compliance<')
    html = html.replace('>Target<', '>Compliance<')
    html = html.replace('>Stretch<', '>Status<')
    # Phase-band totals
    html = re.sub(r'Target <b>\d+ / \d+ pts?</b>', 'Compliance verified', html)
    html = re.sub(r'Target <b>\d+ / \d+</b>', 'Compliance verified', html)
    # ~X pts · descriptions
    html = re.sub(r'~\d+\s*pts?\s*·\s*', '', html)
    # Stretch language
    html = re.sub(r'Stretch ≥ \d+% \(\d+\+ pts?\)\.?\s*', '', html)
    # Mostadam credit point refs
    html = re.sub(r'\(\d+\s*pts?\s*at\s*\d+%\+.*?\)', '(per Mostadam Manual)', html)
    html = re.sub(r'\(\d+\s*pts?\s*at\s*\d+%.*?\)', '(per Mostadam Manual)', html)
    # targeted-points map
    html = html.replace('targeted-points map setup', 'compliance framework setup')
    html = html.replace('pts on track / drift / corrective actions', 'compliance status / drift / corrective actions')
    html = html.replace('credit-targeting log', 'compliance log')
    html = html.replace('credit-targeting', 'compliance')
    html = html.replace('recommends design changes to lift credit-pool toward Gold stretch',
                        'recommends design changes for compliance improvement')
    html = html.replace('Pre-credit application + targeted', 'Pre-compliance review +')
    html = html.replace('Voluntary target', 'Compliance')
    html = html.replace('Voluntary stretch', 'Status')
    html = re.sub(r'Samaya aspiration \(not ER-mandated\)', 'Code compliance', html)
    html = re.sub(r'Samaya stretch goal \(not ER-mandated\)', 'Code compliance', html)
    html = re.sub(r'<div class="body">The ER does not pre-set a Mostadam tier.*?</div>',
                  '<div class="body">The ER mandates compliance with the Mostadam Manual and SBC 1001 codes. The accredited assessor verifies compliance at each stage gate.</div>', html)
    html = html.replace('credit pool', 'compliance category')
    html = html.replace('credit pools', 'compliance categories')
    html = html.replace('>Credit<', '>Item<')
    html = re.sub(r'sub-credit pickups in.*?enhanced Cx', 'full enhanced Cx', html)
    html = re.sub(r'major win on.*?refurb\)', 'existing-building re-use intrinsic to refurb', html)
    html = html.replace('(construction-phase subset)', '')
    html = re.sub(r'design-stage EN credits.*?Part B §6', 'design-stage EN credits addressed in Part B §6', html)
    html = html.replace('Mostadam credit-targeting log (per §14)', 'Mostadam compliance log (per §14)')
    html = html.replace('Pre-DD assessor onboarding', 'Assessor onboarding')
    html = html.replace('Strategy review + assessor onboarding + targeted-points map setup',
                        'Strategy review + assessor onboarding + compliance framework setup')
    html = re.sub(r'Proposed energy use.*?ASHRAE 90\.1 baseline.*?Stretch.*?',
                  'Proposed energy use per Mostadam EN-04 minimum requirement.', html)
    html = re.sub(r'EN-13 Renewable Energy.*?on-site renewable\).*?', 'EN-13 Renewable Energy (per Mostadam Manual)', html)
    html = re.sub(r'IEQ-06 Daylight.*?regularly-occupied', 'IEQ-06 Daylight (per Mostadam Manual)', html)
    html = re.sub(r'Owner of <b>design-stage credits</b> \(~?\d+\s*pts?\)', 'Owner of <b>design-stage compliance</b>', html)
    html = re.sub(r'Owner of <b>construction-stage credits</b> \(~?\d+\s*pts?\)', 'Owner of <b>construction-stage compliance</b>', html)
    html = html.replace('Samaya commits to <b>SILVER 45+ pts</b> as minimum', 'Samaya commits to full code compliance')
    html = html.replace('GREENGUARD Gold', 'GREENGUARD')
    html = html.replace('Gallery (Tier B)', 'Gallery')
    # Cleanup
    html = re.sub(r'<div class="snap-row">\s*</div>', '', html)
    html = re.sub(r'  +', ' ', html)
    html = re.sub(r'\n{3,}', '\n\n', html)
    return html


def clean_ai_fingerprints_and_symbols(html: str) -> str:
    \"\"\"Remove AI-sounding phrases and decorative symbols from body text.
    
    Strips: § · — – → × ° • and AI cliches like 'this strategy reads',
    'read this page before', 'the highest-impact', 'the biggest X lever',
    'this is the X-defining rule', 'reading note', etc.
    \"\"\"
    # Symbols in body (not CSS)
    html = html.replace('§', 'Sec ')
    html = html.replace('·', ' ')
    html = html.replace('—', ' ')
    html = html.replace('–', ' ')
    html = html.replace('→', 'to')
    html = html.replace('×', 'x')
    html = html.replace('°', 'deg')
    html = html.replace('•', ' ')
    
    # AI fingerprints
    html = html.replace(
        'This strategy reads top-to-bottom. <b>Part&nbsp;A</b> orients on the framework and the ER mandate.',
        '<b>Part&nbsp;A</b> orients on the framework and the ER mandate.'
    )
    html = html.replace('Read this page before anything else. ', '')
    html = html.replace('Reading note:', 'Note:')
    html = html.replace('This is the museum-defining rule: ', '')
    html = html.replace('the highest-impact construction-phase category', 'the main construction-phase category')
    html = html.replace('the biggest sustainability lever', 'the main sustainability lever')
    
    # Cleanup
    html = re.sub(r'  +', ' ', html)
    html = re.sub(r'\n{3,}', '\n\n', html)
    return html

def convert(input_path: str, output_path: str, strip_points: bool = False, clean: bool = False,
            doc_ref: str = "MOC-ASEER-SIC-1K0-SC-001",
            project_name: str = "Aseer Regional Museum",
            doc_title: str = "Aseer Regional Museum — D&B Sustainability Strategy",
            revision: str = "C05", doc_type: str = "RPT", doc_date: str = "Jul 2026"):
    with open(input_path, 'r', encoding='utf-8') as f:
        html = f.read()

    if strip_points:
        html = strip_points_language(html)
    if clean:
        html = clean_ai_fingerprints_and_symbols(html)

    body = re.search(r'<body[^>]*>(.*?)</body>', html, re.IGNORECASE | re.DOTALL).group(1)
    body = re.sub(r'<script[^>]*>.*?</script>', '', body, flags=re.DOTALL | re.IGNORECASE)
    body = re.sub(r'<style[^>]*>.*?</style>', '', body, flags=re.DOTALL | re.IGNORECASE)

    first_h2 = re.search(r'<h2[^>]*>', body, re.IGNORECASE)
    if not first_h2:
        print("No H2 found in body")
        return False
    body = body[first_h2.start():]

    # Tokenize top-level blocks
    pattern = re.compile(r'<(h2|h3|h4|p|table|ul|ol|hr)\b[^>]*>', re.IGNORECASE)
    items = []
    for m in pattern.finditer(body):
        tag = m.group(1).lower()
        start = m.start()
        if tag == 'hr':
            items.append(('hr', start, start + m.end() - m.start(), None))
            continue
        if tag == 'p':
            end_m = re.search(r'</p\s*>', body[m.end():], re.IGNORECASE)
            if end_m:
                cs, ce = m.end(), m.end() + end_m.start()
                end = m.end() + end_m.end()
            else:
                cs = ce = m.end()
                end = m.end()
            items.append(('p', start, end, body[cs:ce]))
            continue
        if tag in ('h2','h3','h4'):
            end_m = re.search(rf'</{tag}\s*>', body[m.end():], re.IGNORECASE)
            if end_m:
                content = body[m.end():m.end() + end_m.start()]
                end = m.end() + end_m.end()
            else:
                content = ''
                end = m.end()
            items.append((tag, start, end, content))
            continue
        if tag == 'table':
            depth, pos = 1, m.end()
            while depth > 0 and pos < len(body):
                no = re.search(r'<table\b[^>]*>', body[pos:], re.IGNORECASE)
                nc = re.search(r'</table\s*>', body[pos:], re.IGNORECASE)
                if not nc: break
                if no and no.start() < nc.start():
                    depth += 1; pos += no.end()
                else:
                    depth -= 1; pos += nc.end()
            items.append(('table', start, pos, body[m.end():pos - len('</table>')]))
            continue
        if tag in ('ul','ol'):
            ct = f'</{tag}>'
            end_m = re.search(ct, body[m.end():], re.IGNORECASE)
            if end_m:
                content = body[m.end():m.end() + end_m.start()]
                end = m.end() + end_m.end()
            else:
                content = ''
                end = m.end()
            items.append((tag, start, end, content))
            continue

    print(f"Parsed {len(items)} top-level items")

    # Build DOCX
    doc = SamayaDoc()
    doc.create_header(project_name, doc_ref, doc_type, revision, doc_date)
    doc.create_footer(doc_ref, confidential=True)
    doc.add_h1(doc_title)

    sec_cnt = tbl_cnt = para_cnt = 0
    for kind, s, e, content in items:
        if kind == 'h2':
            text = cell_to_text(content)
            m2 = re.match(r'^(\d+(?:\.[A-Za-z0-9]+)?)\s*[.\)]\s*(.*)$', text)
            if m2:
                num, title = m2.group(1), m2.group(2)
            else:
                m2b = re.match(r'^(\S+)\s+(.*)$', text)
                num, title = (m2b.group(1), m2b.group(2)) if m2b else ('', text)
            doc.add_h2(num, title)
            sec_cnt += 1
        elif kind == 'h3':
            text = cell_to_text(content)
            m2 = re.match(r'^(\d+(?:\.\d+)*)\s*[.\)]\s*(.*)$', text)
            num, title = (m2.group(1), m2.group(2)) if m2 else ('', text)
            doc.add_h3(num, title)
        elif kind == 'h4':
            doc.add_body(cell_to_text(content), bold=True, size=11)
        elif kind == 'p':
            text = cell_to_text(content)
            if not text: continue
            segs = html_to_segments(content)
            if segs:
                doc.add_rich_body([{'text': s['text'], 'bold': s['bold'], 'italic': s['italic']} for s in segs])
            else:
                doc.add_body(text)
            para_cnt += 1
        elif kind == 'table':
            headers, rows = parse_table(content)
            if not rows and not headers: continue
            if not headers:
                headers = [f"Col {i+1}" for i in range(len(rows[0]))] if rows else []
            ncols = max(len(headers), max((len(r) for r in rows), default=0))
            headers = headers + [''] * (ncols - len(headers))
            norm = [r + [''] * (ncols - len(r)) for r in rows]
            try:
                doc.add_table(headers, norm)
                tbl_cnt += 1
            except Exception as ex:
                print(f"Table #{tbl_cnt+1} failed: {ex}")
                doc.add_body("[" + " | ".join(headers) + "]", bold=True, size=10)
                for r in norm:
                    doc.add_body(" | ".join(r), size=10)
        elif kind in ('ul','ol'):
            for li in re.findall(r'<li[^>]*>(.*?)</li>', content, re.IGNORECASE | re.DOTALL):
                txt = cell_to_text(li)
                if txt: doc.add_body(f"•  {txt}")
        elif kind == 'hr':
            doc.line()

    print(f"Processed: {sec_cnt} sections, {tbl_cnt} tables, {para_cnt} body paragraphs")
    doc.save(output_path)
    print(f"Saved: {output_path}")
    return True


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 html-to-docx-converter.py <input.html> <output.docx> [--strip-points] [--clean]")
        sys.exit(1)
    strip = '--strip-points' in sys.argv
    clean = '--clean' in sys.argv
    ok = convert(sys.argv[1], sys.argv[2], strip, clean)
    sys.exit(0 if ok else 1)
