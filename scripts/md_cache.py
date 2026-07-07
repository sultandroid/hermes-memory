#!/usr/bin/env python3
"""
MD File Cache Utility — read, write, and manage .pdf.md sidecar files.

Usage:
  python3 md_cache.py write <filepath> [--type TYPE] [--code CODE] [--subject SUBJECT] [--parties PARTIES]
  python3 md_cache.py read <filepath>
  python3 md_cache.py check <filepath>
"""

import os, sys, json, hashlib, frontmatter
from datetime import datetime

BIM_ROOT = os.path.expanduser("~/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit")


def checksum(filepath, bytes_limit=65536):
    """Compute MD5 of first 64KB for quick dedup."""
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        h.update(f.read(bytes_limit))
    return h.hexdigest()


def get_cache_path(filepath):
    """Get the .pdf.md sidecar path for any file."""
    return filepath + ".md"


def read_cache(filepath):
    """Read existing .md sidecar. Returns (metadata dict, body text) or (None, None)."""
    cache_path = get_cache_path(filepath)
    if not os.path.exists(cache_path):
        return None, None

    try:
        post = frontmatter.load(cache_path)
        return dict(post.metadata), post.content
    except Exception:
        # Fallback: try reading as narrative markdown (no frontmatter)
        with open(cache_path) as f:
            content = f.read()
        return {"format": "narrative"}, content


def write_cache(filepath, metadata, summary=""):
    """Write .md sidecar with YAML frontmatter. Returns cache path."""
    cache_path = get_cache_path(filepath)

    # Auto-fill checksum if not provided
    if "checksum" not in metadata and os.path.exists(filepath):
        metadata["checksum"] = checksum(filepath)

    if "date" not in metadata:
        metadata["date"] = datetime.now().strftime("%Y-%m-%d")

    post = frontmatter.Post(summary, **metadata)

    with open(cache_path, "w") as f:
        f.write(frontmatter.dumps(post))

    return cache_path


def cache_exists(filepath):
    """Check if a valid cache exists (same checksum)."""
    cache_path = get_cache_path(filepath)
    if not os.path.exists(cache_path):
        return False

    meta, _ = read_cache(filepath)
    if not meta:
        return False

    cached_cs = meta.get("checksum")
    if cached_cs and os.path.exists(filepath):
        current_cs = checksum(filepath)
        return cached_cs == current_cs

    return True  # No checksum to compare, assume valid


def find_all_caches(root_dir):
    """Recursively find all .md sidecar files."""
    caches = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith(".pdf.md") or f.endswith(".docx.md") or f.endswith(".xlsx.md"):
                caches.append(os.path.join(dirpath, f))
    return caches


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <read|write|check|find> [args...]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "read" and len(sys.argv) >= 3:
        meta, body = read_cache(sys.argv[2])
        if meta:
            print(json.dumps(meta, indent=2, ensure_ascii=False))
            if body:
                print(f"\n---\n{body[:500]}")
        else:
            print("No cache found")
            sys.exit(1)

    elif action == "check" and len(sys.argv) >= 3:
        exists = cache_exists(sys.argv[2])
        print(f"{'VALID' if exists else 'MISSING/STALE'}: {sys.argv[2]}")
        sys.exit(0 if exists else 1)

    elif action == "write" and len(sys.argv) >= 3:
        filepath = sys.argv[2]
        metadata = {"file": os.path.basename(filepath)}

        # Parse --key value pairs
        for i in range(3, len(sys.argv), 2):
            if sys.argv[i].startswith("--"):
                key = sys.argv[i][2:]
                val = sys.argv[i + 1] if i + 1 < len(sys.argv) else ""
                try:
                    val = json.loads(val)
                except (json.JSONDecodeError, ValueError):
                    pass
                metadata[key] = val

        path = write_cache(filepath, metadata)
        print(f"Cache written: {path}")

    elif action == "find":
        root = sys.argv[2] if len(sys.argv) >= 3 else BIM_ROOT
        caches = find_all_caches(root)
        print(f"Found {len(caches)} cache files")
        for c in caches[:50]:
            print(f"  {c}")
        if len(caches) > 50:
            print(f"  ... and {len(caches) - 50} more")

    else:
        print(f"Unknown action: {action}")
