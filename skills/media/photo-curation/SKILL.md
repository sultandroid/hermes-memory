---
name: photo-curation
description: Curate large photo collections from phone galleries (WhatsApp, camera roll) for website/portfolio use — classify by quality and content, organize into folders, multi-agent verification pipeline.
tags: [photos, curation, classification, website, media, organization, sips]
related_skills: [bulk-file-organization, document-analysis]
---

# Photo Curation for Website/Portfolio

Methodology for classifying 1K-10K+ photos from phone galleries (WhatsApp, camera roll) into website-ready collections. Designed for construction, fabrication, and workshop photos where you need to separate "clean" product shots from casual/screenshots/low-quality.

## Multi-Agent Pipeline

### Phase 1: Manifest & Rule-Based Tiering

Build a comprehensive metadata index first. Never classify blind.

```python
import os, json

BASE = "/path/to/photos"
manifest = []

for root, dirs, files in os.walk(BASE):
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext not in ('.jpg','.jpeg','.png','.heic','.webp'):
            continue
        fp = os.path.join(root, f)
        sz = os.path.getsize(fp)
        
        # Infer category from naming pattern
        name_upper = f.upper()
        if 'FINISHED-PROJECT' in name_upper:   cat = 'Finished-Product'
        elif 'WORKSHOP' in name_upper:          cat = 'Workshop'
        elif 'MATERIAL' in name_upper:          cat = 'Material-Sample'
        elif 'DOCUMENT' in name_upper:          cat = 'Document'
        else:                                   cat = 'Other'
        
        manifest.append({
            'file': f, 'path': os.path.relpath(fp, BASE),
            'category': cat, 'size_bytes': sz,
        })

# Tier by quality heuristics
POOR_THRESHOLD  = 100_000   # <100KB -> poor quality
LOW_THRESHOLD   = 200_000   # <200KB -> low quality
HIGH_THRESHOLD  = 1_000_000 # >1MB -> high quality (for Finished-Project)
```

**Rule-based tiering logic:**

| Category | Size Condition | Tier |
|----------|---------------|------|
| Finished-Product | >1MB | HIGH |
| Finished-Product | 500KB-1MB | MEDIUM |
| Finished-Product | <500KB | REVIEW |
| Workshop | >2MB | HIGH |
| Workshop | 1-2MB | MEDIUM |
| Material-Sample | >2MB | HIGH |
| Document | any | SKIP |
| Everything else | <200KB | LOW/SKIP |

### Phase 2: sips Metadata Extraction (macOS)

Use `sips` (macOS built-in) to get real image quality metrics. This is faster and more reliable than trying to load images in Python.

```bash
sips -g pixelWidth -g pixelHeight -g make -g model -g creation photo.jpg
```

For bulk extraction:
```python
import subprocess
r = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', path],
                   capture_output=True, text=True, timeout=5)
lines = r.stdout.strip().split('\n')
info = {}
for line in lines:
    if ':' in line:
        k, v = line.split(':', 1)
        info[k.strip()] = v.strip()
```

**Quality thresholds from sips:**
- Width or height >= 2000px → excellent for website hero images
- Width or height >= 1200px → good for gallery/thumbnails
- Width or height >= 800px → acceptable for website use
- Both < 800px → low quality, discard unless content is unique

**Camera source matters:** Photos from Samsung Galaxy S24 Ultra (and similar flagship phones) at 3648×2052+ are excellent quality. Photos with `<nil>` make/model may be from unknown sources or compressed.

### Phase 3: Multi-Agent Parallel Classification

Delegate MEDIUM-tier photos to sub-agents for vision review. Split by time period for parallelism:

```python
# Split MEDIUM tier into 3 batches for parallel agents
batches = [
    ("Q1 (Jan-Mar)", medium_by_month['Jan-Mar']),
    ("Q2 (Apr-Jun)", medium_by_month['Apr-Jun']), 
    ("Q3-Q4 (Jul-Dec)", medium_by_month['Jul-Dec']),
]
# Delegate each to a sub-agent with toolsets=['terminal','file']
```

**Sub-agent instructions must include:**
- Exact sips command to check resolution
- Move (mv) command template for promoted files
- Clear KEEP/DISCARD criteria based on resolution thresholds
- Target folder structure for each content type

### Phase 4: Deduplicate & Audit

After all agents complete, run a Codex audit pass:

```bash
# Check for duplicates between website-ready and review folders
find classified/website-ready -type f -exec basename {} \; | sort > /tmp/ws_files.txt
find classified/review -type f -exec basename {} \; | sort > /tmp/rv_files.txt
comm -12 /tmp/ws_files.txt /tmp/rv_files.txt  # files in both
```

**Deduplication:**
- Files that are in BOTH website-ready AND review → remove from review (already classified)
- Best-High-Res subset of Finished-Products → expected duplication, not an error
- Review folder should only contain truly unique files needing human inspection

### Phase 5: Output Structure

```
classified/
├── website-ready/
│   ├── 01-Finished-Products/      # Completed products (gates, railings, stairs)
│   ├── 02-Workshop-Environment/   # Factory/workshop floor shots
│   ├── 03-Onsite-Installations/   # Photos at client sites
│   ├── 04-Material-Samples/       # Material close-ups and details
│   ├── 05-Opening-Ceremony/       # Event photos
│   └── 06-Best-High-Res/          # >3MB photos for hero/slider use
├── review/
│   └── needs-vision-check/         # Borderline photos needing human eye
```

## Common Photo Categories from WhatsApp

Phone gallery photos from construction/fabrication projects typically fall into:

| Naming Pattern | Content | Website Value |
|---------------|---------|---------------|
| `Finished-Project-*` | Completed installations (gates, railings, stairs, canopies) | HIGHEST |
| `Workshop-*` | Fabrication process, factory floor | MEDIUM-HIGH |
| `Material-Sample-*` | Material close-ups, color samples | MEDIUM |
| `Document-*` | Screenshots of chats, PDFs, text messages | SKIP |
| `IMG-*` or `IMG_*` | Unrenamed WhatsApp photos | Variable |
| `Opening-*` or ceremony folder | Events and inaugurations | MEDIUM |

## Pitfalls

- **OneDrive is slow**: Bulk copy/move on OneDrive-synced folders (especially with thousands of files) is extremely slow. Use `shutil.copy2` in batches or delegate to background processes with patience.
- **WhatsApp compression**: Photos shared via WhatsApp lose quality. A 600KB WhatsApp photo may still have decent resolution (1200×1600) and be usable despite small file size. Always check sips dimensions, not just file size.
- **Duplicate filenames**: Multiple agents may copy the same files. Run dedup as final step.
- **Vision tools may not be available**: Not all sub-agents can actually view images. Build your primary classification on objective metadata (resolution, size, naming pattern) and leave content-judgment calls to human review.
- **Agent 1 used mv (move)**: If one sub-agent uses `mv` instead of `cp`, originals disappear. Be explicit about copy-vs-move in sub-agent instructions.
- **Finished-Products can be missed**: Some renamed photos may have different naming but still be finished products. Check for photos matching any date pattern that aren't already in the target.
- **Arabic folder names**: Folders with Arabic names (e.g., `001 يناير 2025`) require proper Unicode handling. Python's `os.listdir` handles this, but shell scripts may struggle — use Python or quote properly in bash.

## References

- `references/samaya-factory-classification-2025.md` — Real-world application classifying 4,570 WhatsApp photos from Samaya metal fabrication factory (Dec 2024 - Dec 2025).

## Example: Quick-Start Classification Script

```python
import os, json, subprocess, shutil
from collections import defaultdict

def build_manifest(base_path):
    """Phase 1: Build photo manifest with size and naming category."""
    manifest = []
    for root, dirs, files in os.walk(base_path):
        for f in files:
            if not f.lower().endswith(('.jpg','.jpeg','.png','.heic')):
                continue
            fp = os.path.join(root, f)
            manifest.append({
                'file': f, 'path': os.path.relpath(fp, base_path),
                'size_bytes': os.path.getsize(fp),
                'category': infer_category(f),
            })
    return manifest

def infer_category(filename):
    name = filename.upper()
    if 'FINISHED-PROJECT' in name: return 'Finished-Product'
    if 'WORKSHOP' in name: return 'Workshop'
    if 'MATERIAL' in name: return 'Material-Sample'
    if 'DOCUMENT' in name: return 'Document'
    return 'Other'

def get_resolution(path):
    r = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', path],
                       capture_output=True, text=True, timeout=5)
    info = {}
    for line in r.stdout.strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            info[k.strip()] = v.strip()
    return int(info.get('pixelWidth', 0)), int(info.get('pixelHeight', 0))
```
