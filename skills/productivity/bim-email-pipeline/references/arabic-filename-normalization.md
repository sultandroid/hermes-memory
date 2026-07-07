# Arabic Filename Normalization for Sub-Agent File Comparison

Confirmed: 2026-06-10 during automated cron pipeline — Codex sub-agent reported 4 "new" files that were actually already in BIM OneDrive. Root cause: Arabic Unicode normalization differences between attachment filenames (from email extraction) and BIM destination filenames (from manual upload).

## The Problem

Arabic text has multiple Unicode representations for the same "visual" character. Common normalization issues:

| Base Letter | Forms | Unicode Range | Example |
|------------|-------|---------------|---------|
| Alef | ا (U+0627), أ (U+0623), إ (U+0625), آ (U+0622), ٱ (U+0671) | U+0622–U+0671 | `استثمارية` vs `اإستثمارية` |
| Yeh | ي (U+064A), ى (U+0649), ئ (U+0626) | U+0626–U+064A | `عسير` vs `عسير` (same visually, different code point) |
| Teh Marbuta | ة (U+0629), ه (U+0647) | U+0629, U+0647 | `متحف` vs `متحفة` |
| Tashkeel (diacritics) | Various | U+064B–U+0652 | Short vowels, shadda, sukun |

When an email attachment has filename `العرض الفني والمالي - شركة سمايا الإستثمارية - متحف عسير.pdf` and the BIM file has `العرض الفني والمالي - شركة سمايا الإستثمارية - متحف عسير.pdf`, they may look identical but differ at the byte level (U+0627 Alef vs U+0623 Alef with Hamza Below).

## When This Bites You

- **Sub-agent file comparison:** A sub-agent (Codex, Claude, Kimi) builds a set of BIM filenames via `find -name` and compares against attachment filenames. Arabic normalization differences cause false "new file" reports.
- **Dedup verification:** The `already_filed` set contains `filename.lower()` but Alef with vs without Hamza are different bytes, so the check fails.
- **Shell `find -name` patterns:** `find -name "*العرض*"` may not match `*العرض*` if the `ا` is from a different Unicode block.

## Fix: Normalize Before Comparison

### Python (inside execute_code or sub-agent scripts)

```python
import unicodedata
import re
import string

def normalize_filename(name: str) -> str:
    """Normalize Arabic filename for string comparison."""
    # Step 1: NFC normalization (composed form)
    name = unicodedata.normalize('NFC', name)
    
    # Step 2: Strip Arabic diacritics (tashkeel)
    name = re.sub(r'[\u064B-\u0652]', '', name)
    
    # Step 3: Normalize Alef variants to base Alef
    name = re.sub(r'[أإآٱ]', 'ا', name)
    
    # Step 4: Normalize Yeh variants to base Yeh
    name = re.sub(r'[ىئ]', 'ي', name)
    
    # Step 5: Normalize Teh Marbuta to Heh
    name = re.sub(r'[ة]', 'ه', name)
    
    # Step 6: Lowercase
    name = name.lower()
    
    # Step 7: Strip ASCII whitespace and punctuation
    name = name.strip()
    name = re.sub(r'[^\w\s\-\.\(\)]', '', name)
    
    return name


def is_same_file(name1: str, name2: str) -> bool:
    """Check if two filenames refer to the same file (accounting for Arabic normalization)."""
    return normalize_filename(name1) == normalize_filename(name2)


# For fuzzy matching (file renamed with _1, _2 suffix):
def is_similar_file(name1: str, name2: str, threshold: float = 0.9) -> bool:
    """Check if two filenames likely refer to the same file."""
    import difflib
    n1 = normalize_filename(name1)
    n2 = normalize_filename(name2)
    return difflib.SequenceMatcher(None, n1, n2).ratio() >= threshold
```

### Instructing Sub-Agents (Orchestration Protocol)

When delegating file comparison to sub-agents for BIM projects with Arabic filenames, add this context to every task:

> **Arabic normalization:** Filenames containing Arabic characters may have multiple Unicode representations of the same letter. Use `unicodedata.normalize('NFC', name).lower()` and normalize Alef variants (`أإآٱ` → `ا`), Yeh variants (`ىئ` → `ي`), and Teh Marbuta (`ة` → `ه`). Strip diacritics (U+064B–U+0652) before comparison. Use SequenceMatcher with threshold > 0.9 as a fallback for files with `_1`, `_2` suffixes.

### Shell Workaround (for `find -name` dedup)

```bash
# Normalize Arabic in shell before passing to find
find "$BIM_ROOT" -type f | while read f; do
    basename=$(basename "$f" | sed 's/[أإآٱ]/ا/g; s/[ىئ]/ي/g; s/ة/ه/g')
    echo "$basename" >> /tmp/normalized_bim_files.txt
done

# Then compare attachment names (also normalized)
for att in /path/to/attachments/*.pdf; do
    att_basename=$(basename "$att" | sed 's/[أإآٱ]/ا/g; s/[ىئ]/ي/g; s/ة/ه/g')
    if grep -qiF "$att_basename" /tmp/normalized_bim_files.txt; then
        echo "FOUND: $att"
    fi
done
```

## Real-World Confirmation (Jun 10, 2026)

Files flagged as "new" by Codex sub-agent that were actually already in BIM:

| Attachment (as reported) | BIM file (actual) | Difference |
|--------------------------|-------------------|------------|
| `العرض الفني والمالي - شركة سمايا الإستثمارية - أعمال الدراسات والتصميم الإنشائي متحف عسير.pdf` | `العرض الفني والمالي - شركة سمايا الإستثمارية - أعمال الدراسات والتصميم الإنشائي متحف عسير.pdf` | Alef variants (إ vs ا), Yeh variants (ي vs ى), standalone vs medial forms |
| `01-AL JALAL WAL JAMAL 02 (2).pdf` | Same filename in `99_Images/` | Exact match — sub-agent just didn't search the full BIM tree |

The first case is a true Unicode normalization problem. The second case is a search-scope problem (sub-agent only searched 7 specific folders, not the full BIM tree). Always instruct sub-agents to do a full-tree `find -iname` pass.
