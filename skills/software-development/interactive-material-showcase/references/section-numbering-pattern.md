# Section Numbering & Adding New Sections

## Current Section Structure

The app uses sequential numbering with bilingual (Arabic/English) section labels:

| # | Label | Component | id | File |
|---|-------|-----------|----|------|
| 01 | Gallery / المعرض | Gallery | `#gallery` | `src/sections/Gallery.tsx` |
| 02 | Materials / المواد | Materials | `#materials` | `src/sections/Materials.tsx` |
| 03 | Material Schedules / جداول المواد | Schedule | `#schedule` | `src/sections/Schedule.tsx` |
| 04 | المحتويات / Table of Contents | TableOfContents | `#toc` | `src/sections/TableOfContents.tsx` |

Hero and Footer are unnumbered — they flank the numbered sections.

## How to Add a New Section

### 1. Create the Section Component

Place in `src/sections/<Name>.tsx`. Follow the established pattern:

```
{section_number} / {arabic_label}
```

Rendered as a `<span>` above the `<h2>`:

```tsx
<span style={{ fontFamily: "'Inter', sans-serif", fontWeight: 500, fontSize: '0.7rem',
  textTransform: 'uppercase', letterSpacing: '0.08em', color: '#C8A45C',
  display: 'block', marginBottom: '16px' }}>
  {nn} / {arabic_label}
</span>
<h2 style={{ fontFamily: "'Playfair Display', serif", fontWeight: 400,
  fontSize: 'clamp(2rem, 5vw, 4rem)', color: '#1A1D23', margin: '0 0 16px' }}>
  {arabic_title} — {english_title}
</h2>
```

### 2. Use Inline SVG Icons

Icons are inline `<svg>` strings stored in a `icon` field and rendered via `dangerouslySetInnerHTML`:

```tsx
interface SectionItem {
  name: string;
  arabicName: string;
  icon: string; // inline SVG
}

const items = [{
  arabicName: 'المعرض',
  name: 'Gallery',
  icon: '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#C8A45C" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">...</svg>',
}];

// Render
<div dangerouslySetInnerHTML={{ __html: item.icon }} />
```

Icon rules:
- `stroke="#C8A45C"` — gold/bronze color
- `strokeWidth="1.5"` — consistent thickness
- `fill="none"` — outlined style
- `width="24" height="24"` — standard size

### 3. Import & Render in App.tsx

```tsx
import NewSection from './sections/NewSection';

function App() {
  return (
    <>
      <Navigation />
      <NewSection />
      <div style={{ position: 'relative', zIndex: 1 }}>
        <Hero />
        ...
      </div>
    </>
  );
}
```

### 4. Add to Navigation

In `src/sections/Navigation.tsx`, add a nav link:

```tsx
{[
  { label: 'Arabic Label', id: '#section-id' },
  // ...
].map(item => (
  <button key={item.label} onClick={() => scrollTo(item.id)}>
    {item.label}
  </button>
))}
```

### 5. Section Layout Conventions

- **Background**: `rgba(245,241,235,0.98)` — warm off-white
- **Max width**: `1200px` for card grids, `1400px` for gallery/schedule
- **Padding**: `120px 40px` (top/bottom, left/right)
- **Cards grid**: `repeat(auto-fit, minmax(280px, 1fr))` with `gap: 16px`
- **Card hover**: gold border glow (`rgba(200,164,92,0.4)`), lift translateY(-4px) scale(1.02) rotateX(2deg), box-shadow
- **Font hierarchy**: Playfair Display for headings, Inter for body, IBM Plex Mono for codes

### 6. GSAP Scroll Animations

```tsx
useEffect(() => {
  const section = sectionRef.current;
  if (!section) return;
  const cards = section.querySelectorAll('.section-card');
  cards.forEach((card, i) => {
    gsap.fromTo(card, { opacity: 0, y: 30 }, {
      opacity: 1, y: 0, duration: 0.6, delay: i * 0.06, ease: 'power3.out',
      scrollTrigger: { trigger: section, start: 'top 70%' },
    });
  });
  return () => { ScrollTrigger.getAll().forEach(t => t.kill()); };
}, []);
```
