# Mobile Touch-Drag Panning for Image Viewer

Add touch-based drag-to-pan to the gallery image viewer for mobile devices.

## Implementation

**State & Refs** (add in GalleryViewer):
```
const [panOffset, setPanOffset] = useState({x:0, y:0});
const isPanning = useRef(false);
const panStart = useRef({x:0, y:0});
const panOffsetRef = useRef({x:0, y:0});
```

**Touch handlers** (on `.modal-image-wrap`):
```
onTouchStart={e => {
  if (e.touches.length === 1) {
    isPanning.current = true;
    panStart.current = {
      x: e.touches[0].clientX - panOffsetRef.current.x,
      y: e.touches[0].clientY - panOffsetRef.current.y
    };
  }
}}
onTouchMove={e => {
  if (!isPanning.current || e.touches.length !== 1) return;
  const nx = e.touches[0].clientX - panStart.current.x;
  const ny = e.touches[0].clientY - panStart.current.y;
  panOffsetRef.current = {x: nx, y: ny};
  setPanOffset({x: nx, y: ny});
}}
onTouchEnd={() => { isPanning.current = false; }}
```

**Container style**: `style={{overflow:'hidden', touchAction:'none'}}`

**Image transform**: add to img style:
```
transform: `translate(${panOffset.x}px, ${panOffset.y}px)`,
transition: isPanning.current ? 'none' : 'transform .2s ease',
cursor: 'grab',
```

**Reset on view change**: clear panOffset + panOffsetRef in handleViewChange.
**Reset on image load**: clear in onLoad handler.

## Key Points

- touchAction:'none' prevents browser scroll interference during pan
- isPanning ref (not state) controls transition — smooth when released, instant during drag
- Reset on both view change AND image load to handle re-renders
- Hotspot positions (percentage-based) remain correct since pan uses CSS transform on the img, not layout shift
