# Gallery Data Restoration Workflow

When the user says "go back to the morning version" or "this is the old design" after a deploy, the issue is almost always **uncommitted design changes** that were deployed alongside intended data-only changes.

## Root Cause

The app repo at `14_Completed_Tender_Package_From_NRS/07_Visualizations/Kimi_Agent_Interactive 3D Material Showcase/app/` has multiple git commits that changed the design (Navigation, Gallery layout, App.tsx, index.css). When you edit `Gallery.tsx` to add new gallery entries, you're editing the file as it exists on disk — which may include design changes from a previous session that were never committed.

## Recovery Steps

1. **Identify the original commit** — the initial state before any design changes:
   ```bash
   git log --oneline --all
   # Look for the first commit, typically "init: current state before fixing broken styles"
   ```

2. **Restore the original files from git**:
   ```bash
   git show <init-commit>:src/sections/Gallery.tsx > /tmp/gallery-orig.tsx
   git show <init-commit>:src/App.tsx > /tmp/app-orig.tsx
   git show <init-commit>:src/sections/Navigation.tsx > /tmp/nav-orig.tsx
   ```

3. **Apply only your data changes** to the original file. For gallery data, this means appending new entries to the `galleryData` array — nothing else.

4. **Build from /tmp/** (OneDrive paths cause build failures):
   ```bash
   # Copy all source files using cat pipe (not cp -R)
   mkdir -p /tmp/aseer-build/src/sections
   cat "$APP/src/sections/Gallery.tsx" > /tmp/aseer-build/src/sections/Gallery.tsx
   # ... repeat for all files
   cd /tmp/aseer-build && npm install --legacy-peer-deps && npx vite build
   ```

5. **Deploy** the clean build.

## Key Files That May Have Design Changes

| File | What changed | Restore from |
|------|-------------|--------------|
| `src/sections/Gallery.tsx` | Floor grouping, background color, card styling, subRef field, IMG_VERSION | init commit |
| `src/App.tsx` | Added ExecutiveSummary, TableOfContents sections | init commit |
| `src/sections/Navigation.tsx` | Logo/subtitle, color scheme, nav items | init commit |
| `src/index.css` | Various style changes | init commit |

## Verification

After deploy, check the live page for:
- Navigation shows "6930 ASEER" text only (no logo, no subtitle)
- Gallery shows "01 / GALLERY" with dark card style (no floor grouping)
- No Table of Contents section
- No Executive Summary section
- New gallery cards appear at the bottom of the grid
