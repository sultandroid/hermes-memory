# DOCX to Markdown Batch Conversion Template

Standalone script for batch converting DOCX files to Markdown. Handles paragraphs, tables, and heading styles.

## Template Script

```python
import os, sys
from docx import Document

base = sys.argv[1]   # Source folder (Adel's OneDrive path)
repo = sys.argv[2]   # Target repo folder

count = 0
for folder in sorted(os.listdir(base)):
    folder_path = os.path.join(base, folder)
    if not os.path.isdir(folder_path):
        continue
    for docx_name in os.listdir(folder_path):
        if not docx_name.endswith(".docx") or docx_name.startswith("~") or docx_name.startswith("._"):
            continue
        src = os.path.join(folder_path, docx_name)
        try:
            doc = Document(src)
            title = docx_name.replace(".docx", "")
            for p in doc.paragraphs[:5]:
                t = p.text.strip()
                if t and len(t) > 5:
                    title = t[:80]
                    break

            md = f"# {title}\n\n"
            md += f"**Source:** `{folder}/{docx_name}`\n\n---\n\n"

            for p in doc.paragraphs:
                t = p.text.strip()
                if t:
                    if 'Heading' in p.style.name:
                        level = p.style.name.replace("Heading ", "")
                        md += f"{'#' * min(int(level) if level.isdigit() else 2, 4)} {t}\n\n"
                    else:
                        md += t + "\n\n"

            for table in doc.tables:
                rows = []
                for row in table.rows:
                    cells = [c.text.strip().replace("|", "/") for c in row.cells]
                    rows.append(cells)
                if rows:
                    max_cols = max(len(r) for r in rows)
                    for r in rows:
                        while len(r) < max_cols:
                            r.append("")
                    md += "| " + " | ".join(rows[0]) + " |\n"
                    md += "|" + "|".join(["---"] * max_cols) + "|\n"
                    for row in rows[1:]:
                        md += "| " + " | ".join(row) + " |\n"
                    md += "\n"

            out_name = f"{folder.split('-')[0].strip().zfill(3)}.md"
            with open(os.path.join(repo, out_name), "w") as f:
                f.write(md)
            count += 1
        except Exception as e:
            print(f"ERR: {folder}/{docx_name}: {e}")

print(f"Converted {count} files")
```

## Key Patterns

### Nested folder traversal (Letters)
Letters are in `OUT/CG/NN/` and `OUT/MOC/NN/` subfolders. Adjust traversal:
```python
for direction in ["CG", "MOC"]:
    direction_path = os.path.join(base, direction)
    for folder in sorted(os.listdir(direction_path)):
        ...
```

### Revision selection (Method Statements)
When a folder has `Rev.01/`, `Rev.02/` subfolders, pick the latest:
```python
docx_files = []
for item in os.listdir(folder_path):
    if os.path.isdir(item_path) and item.startswith("Rev"):
        for f in os.listdir(item_path):
            if f.endswith(".docx"):
                docx_files.append(os.path.join(item_path, f))
# Take the last one (latest revision)
```

### Inline Python pitfall
Folder names like `05- MOC-...` cause `SyntaxError: leading zeros in decimal integer` when used in `python3 -c "..."` because the path gets interpreted as numeric. Always use a script file (`/tmp/convert.py`) instead of inline `-c`.

## Verified conversions (Aseer Museum)

| Batch | Source | Count | Target |
|-------|--------|-------|--------|
| Submittals | `02. DOC - Document Submittal/GN/` | 5 DOCX | `03_Plans/`, `07_Reports/`, `02_CG_Responses/` |
| RFIs | `05- Request For Information-RFI/` | 5 DOCX | `05_RFIs/` |
| Letters | `01- Letters/OUT/CG+MOC/` | 29 DOCX | `04_Letters/` |
| Method Statements | `09- Method Statement MWS/` | 15 DOCX | `09_Method_Statements/` |
| Plans | Various | 4 DOCX | `03_Plans/` subfolders |
