#!/usr/bin/env python3
"""Dump a .docx to flat numbered lines WITHOUT python-docx.

Why: python-docx may be missing from the sandbox interpreter, and inline
heredocs can be blocked by the gateway command filter. Write this file, then
run it from terminal:

    python3 read_docx_text.py "<path to .docx>" > /tmp/doc.txt
    grep -n "RESPONSIBILITY MATRIX" /tmp/doc.txt

Table cells land on one line separated by ' | ', so question->answer pairs in
response tables can be read and misalignment spotted at a glance.
"""
import html
import re
import sys
import zipfile


def dump(path: str) -> str:
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf8", errors="ignore")
    xml = re.sub(r"</w:p>", "\n", xml)
    xml = re.sub(r"<w:tab/>", "\t", xml)
    xml = re.sub(r"</w:tc>", " | ", xml)
    xml = re.sub(r"</w:tr>", "\n", xml)
    text = html.unescape(re.sub(r"<[^>]+>", "", xml))
    lines = [ln.rstrip() for ln in text.split("\n")]
    return "\n".join(ln for ln in lines if ln.strip())


if __name__ == "__main__":
    body = dump(sys.argv[1])
    lines = body.split("\n")
    print(f"LINES: {len(lines)}")
    for i, line in enumerate(lines):
        print(i, "|", line)
