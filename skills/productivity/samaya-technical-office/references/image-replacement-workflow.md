# Image Replacement Workflow (Preserving Hotspot Positions)

## When to use
Replacing gallery/visualization images on the server while keeping existing hotspot pins intact. The key insight: hotspot positions are tied to the **filename**, not the image content — swap the file, keep the name, hotspots survive.

## Workflow

### 1. Mapping
Create a mapping table between existing view filenames and new submission filenames:

```
Existing File               → New Submission File
g4_G4_View_1.jpg             MOC-ASE-AR-ARC-BF-DDD-VIS001.jpg
g6_G6_View_3.jpg             MOC-ASE-AR-ARC-BF-DDD-VIS003.jpg
```

### 2. Upload via SSH pipe
SCP may hang on certain hosts (Hostinger, port 65002). Use `cat | ssh` pipe instead:

```bash
cat "path/to/VIS001.jpg" | ssh -p 65002 user@host \
  "cat > /home/user/domains/example.com/public_html/build/aseer/images/g4_G4_View_1.jpg"
```

### 3. Add subRef to gallery data
Add a `subRef` field to the View interface and each view entry so the submission filename displays as a badge:

```ts
interface View { viewName: string; filename: string; desc: string; subRef?: string; hotspots: Hotspot[] }
```

Example:
```tsx
{viewName:'G4_View_1', filename:'/aseer/images/g4_G4_View_1.jpg',
 subRef:'MOC-ASE-AR-ARC-BF-DDD-VIS001', desc:'Main gallery hall overview',
 hotspots:[...]}
```

### 4. Display badge in sidebar
```tsx
{view.subRef && (
  <div style={{
    fontFamily:"'IBM Plex Mono',monospace", fontSize:'0.55rem',
    color:'#C8A45C', background:'rgba(200,164,92,.1)',
    padding:'3px 8px', borderRadius:'4px', marginBottom:'8px',
    display:'inline-block', letterSpacing:'0.02em',
  }}>{view.subRef}</div>
)}
```

### 5. No code change needed for hotspot data
Because the server **filename stays the same**, the `Gallery.tsx` reference `/aseer/images/g4_G4_View_1.jpg` still points to the correct path. Only add `subRef` — the hotspots array and all coordinates remain untouched.

### 6. Batch upload tips
- Process multiple files: list mappings, upload each with `cat | ssh`, verify with `ls -lh` on server
- Files can be 3-5MB each — set `timeout=60` per upload

## Pitfalls

### 🔴 SCP hangs on port 65002
On Hostinger/shared hosting, `scp -P 65002` often hangs after successful SSH negotiation. Use `cat | ssh` pipe instead — it's more reliable.

### 🔴 macOS `.` extended attributes
`tar` from macOS adds `._*` Apple Double files. They're harmless on Linux but visible in `ls`. Use `cat | ssh` for individual files to avoid this.

### 🔴 Verify file size after upload
After each upload, run `ls -lh` on the server to confirm the file arrived. A 100-byte file means the pipe failed.

### 🔴 Gallery text counter must be updated
When adding/removing views or galleries, update the hero subtitle text:
- Before: `"16 annotated 3D views across 8 galleries."`
- After: `"20 annotated 3D views across 12 galleries."`
Search for the exact string in `Gallery.tsx` and update.
