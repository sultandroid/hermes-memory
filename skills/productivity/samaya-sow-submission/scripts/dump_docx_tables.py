#!/usr/bin/env python3
"""Table-aware docx dump: prints every table with its row count and all rows.

Why: a paragraph-flattening reader silently loses a table's BODY — a table whose
data rows were deleted still shows its header line, so the section reads as
present while the content is gone. Always run this after read_docx_text.py when
reviewing a revision that contains tables (responsibility matrix, RFI/comment
table, submission programme, document control).

Usage:  python3 dump_docx_tables.py <file.docx>
"""
import html
import re
import sys
import zipfile


def cell_text(fragment: str) -> str:
    fragment = re.sub(r"<w:tab/>", "\t", fragment)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    return html.unescape(fragment).strip()


def main(path: str) -> int:
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf8", errors="ignore")
    tables = re.findall(r"<w:tbl>.*?</w:tbl>", xml, re.S)
    print(f"TABLES: {len(tables)}")
    for ti, table in enumerate(tables):
        rows = re.findall(r"<w:tr[ >].*?</w:tr>", table, re.S)
        print(f"\n===== TABLE {ti} — {len(rows)} rows =====")
        for ri, row in enumerate(rows):
            cells = re.findall(r"<w:tc>.*?</w:tc>", row, re.S)
            print(f"  r{ri}:", " | ".join(cell_text(c) for c in cells))
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        raise SystemExit(2)
    raise SystemExit(main(sys.argv[1]))
