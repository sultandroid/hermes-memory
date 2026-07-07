#!/usr/bin/env python3
"""
docx-annotate.py — Insert highlighted annotation paragraphs after specified paragraphs in a .docx file.

Usage:
    python3 docx-annotate.py --input input.docx --output output_REVIEWED.docx

Edit the ANNOTATIONS list below with your (para_index, label, body, color) tuples.

Color codes: RED, YELLOW, GREEN, TURQUOISE, PINK
"""

import argparse, os, sys
from copy import deepcopy
from docx import Document
from docx.shared import RGBColor
from docx.enum.text import WD_COLOR_INDEX
from docx.oxml.ns import qn

# ── EDIT ANNOTATIONS HERE ──────────────────────────────────────────────
# Format: (paragraph_index, label_text, body_text, color_category)
ANNOTATIONS = [
    # Example:
    # (4, "DOCUMENT ISSUE", "Heading mismatch — says Mechanical but content is Electrical", "PINK"),
    # (15, "CRITICAL GAP — Telecom/IT Design", "Only covers power. Must subcontract CITC telecom engineer for full design.", "RED"),
]
# ───────────────────────────────────────────────────────────────────────

COLOR_MAP = {
    "RED": WD_COLOR_INDEX.RED,
    "YELLOW": WD_COLOR_INDEX.YELLOW,
    "GREEN": WD_COLOR_INDEX.BRIGHT_GREEN,
    "TURQUOISE": WD_COLOR_INDEX.TURQUOISE,
    "PINK": WD_COLOR_INDEX.PINK,
}

LABEL_COLOR_MAP = {
    "RED": RGBColor(0xCC, 0x00, 0x00),
    "YELLOW": RGBColor(0x99, 0x88, 0x00),
    "GREEN": RGBColor(0x00, 0x80, 0x00),
    "TURQUOISE": RGBColor(0x00, 0x66, 0x80),
    "PINK": RGBColor(0xCC, 0x00, 0x66),
}

HL_TO_OXML = {
    WD_COLOR_INDEX.RED: "red",
    WD_COLOR_INDEX.YELLOW: "yellow",
    WD_COLOR_INDEX.BRIGHT_GREEN: "green",
    WD_COLOR_INDEX.TURQUOISE: "cyan",
    WD_COLOR_INDEX.PINK: "magenta",
}


def add_annotation(para, label, body_text, label_color=RGBColor(0x80, 0x00, 0x00),
                   hl_color=WD_COLOR_INDEX.RED):
    """Insert a highlighted annotation paragraph immediately after `para`."""
    # Create new paragraph element via oxml
    new_p_elem = deepcopy(para._element.getparent().makeelement(qn("w:p"), {}))
    para._element.addnext(new_p_elem)
    new_para = type(para)(new_p_elem, para._parent)

    # Paragraph spacing (tight)
    pPr = new_p_elem.find(qn("w:pPr"))
    if pPr is None:
        pPr = new_p_elem.makeelement(qn("w:pPr"), {})
        new_p_elem.insert(0, pPr)
    spacing = pPr.find(qn("w:spacing"))
    if spacing is None:
        spacing = pPr.makeelement(qn("w:spacing"), {})
        pPr.append(spacing)
    spacing.set(qn("w:before"), "0")
    spacing.set(qn("w:after"), "60")

    # ── Label run (bold, colored) ──
    r1 = new_p_elem.makeelement(qn("w:r"), {})
    rPr1 = r1.makeelement(qn("w:rPr"), {})
    r1.append(rPr1)
    # Font size 8pt = 16 half-pts
    sz1 = rPr1.makeelement(qn("w:sz"), {})
    sz1.set(qn("w:val"), "16")
    rPr1.append(sz1)
    # Bold
    b1 = rPr1.makeelement(qn("w:b"), {})
    rPr1.append(b1)
    # Label color
    lc = rPr1.makeelement(qn("w:color"), {})
    if hasattr(label_color, "__getitem__") and len(label_color) == 3:
        lc.set(qn("w:val"), f"{label_color[0]:02X}{label_color[1]:02X}{label_color[2]:02X}")
    else:
        lc.set(qn("w:val"), "800000")
    rPr1.append(lc)

    t1 = r1.makeelement(qn("w:t"), {})
    t1.set(qn("xml:space"), "preserve")
    t1.text = f"\U0001F50D {label} \u2014 "
    r1.append(t1)
    new_p_elem.append(r1)

    # ── Body run (italic, highlighted) ──
    r2 = new_p_elem.makeelement(qn("w:r"), {})
    rPr2 = r2.makeelement(qn("w:rPr"), {})
    r2.append(rPr2)
    sz2 = rPr2.makeelement(qn("w:sz"), {})
    sz2.set(qn("w:val"), "16")
    rPr2.append(sz2)
    # Italic
    i2 = rPr2.makeelement(qn("w:i"), {})
    rPr2.append(i2)
    # Highlight
    hl_name = HL_TO_OXML.get(hl_color, "yellow")
    hl_elem = rPr2.makeelement(qn("w:highlight"), {})
    hl_elem.set(qn("w:val"), hl_name)
    rPr2.append(hl_elem)

    t2 = r2.makeelement(qn("w:t"), {})
    t2.set(qn("xml:space"), "preserve")
    t2.text = body_text
    r2.append(t2)
    new_p_elem.append(r2)

    return new_para


def main():
    parser = argparse.ArgumentParser(description="Annotate a .docx with highlighted gap-analysis paragraphs.")
    parser.add_argument("--input", "-i", required=True, help="Input .docx path")
    parser.add_argument("--output", "-o", default=None, help="Output .docx path (default: input_REVIEWED.docx)")
    parser.add_argument("--list", action="store_true", help="List paragraphs and exit (no annotations)")
    args = parser.parse_args()

    doc = Document(args.input)
    paragraphs = list(doc.paragraphs)

    if args.list:
        for i, p in enumerate(paragraphs):
            text = p.text.strip()
            if text:
                print(f"[{i}] {text[:150]}")
        return

    if not ANNOTATIONS:
        print("ERROR: No ANNOTATIONS defined. Edit the ANNOTATIONS list in the script or use --list to see paragraph indices.")
        sys.exit(1)

    output = args.output or args.input.replace(".docx", "_REVIEWED.docx")
    if output == args.input:
        output = args.input.replace(".docx", "_REVIEWED.docx")

    # Sort descending so inserts don't shift indices
    sorted_annots = sorted(ANNOTATIONS, key=lambda x: x[0], reverse=True)

    for idx, label, body, color in sorted_annots:
        if idx >= len(paragraphs):
            print(f"WARNING: Index {idx} out of range ({len(paragraphs)} paragraphs). Skipping.")
            continue
        p = paragraphs[idx]
        hl = COLOR_MAP.get(color, WD_COLOR_INDEX.YELLOW)
        lc = LABEL_COLOR_MAP.get(color, RGBColor(0x66, 0x66, 0x00))
        add_annotation(p, label, body, label_color=lc, hl_color=hl)

    doc.save(output)
    print(f"Saved: {output}")
    print(f"Annotations: {len(sorted_annots)}")


if __name__ == "__main__":
    main()
