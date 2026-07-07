# React Section Redesign via delegate_task

Adding/redesigning sections in a React app by delegating to subagents. Proven on Aseer Museum Material Explorer (Vite + TypeScript + Tailwind).

## Workflow

### Step 1: Create new section file (standalone)
Write the new component as a standalone `.tsx` file. Follow the project's existing design system (fonts, colors, animation patterns). Use inline styles only if the project doesn't use a CSS framework.

### Step 2: Wire into app
Update three places:
1. **App.tsx** -- add `import` and render in the right position
2. **Navigation.tsx** -- add nav link with the correct `#section-id`
3. **TableOfContents.tsx** (if exists) -- add TOC entry

### Step 3: Delegate section redesigns in parallel batches
Use `delegate_task(tasks=[...])` for independent sections. Critical rules:

**Batch structure:** Group sections that modify DIFFERENT files. Each task gets its own file -- no overlap.

**Goal requirements (mandatory):**
1. Specify the exact file path the subagent should read/modify
2. Tell the subagent which changes to make AND which to AVOID
3. **Critical: List identifiers to preserve** -- section badges (e.g. "01 / Gallery"), section IDs (#gallery, #schedule), data arrays, animation logic
4. Specify the design tokens: fonts, colors (hex), spacing patterns
5. Say "Use inline styles only" if the project doesn't use CSS modules
6. Say "Do NOT modify" for data arrays, complex logic, or imports that must stay stable

### Step 4: Build verification
After ALL batch tasks complete:
```
npx vite build  (or npm run build)
```
Check exit code. If it fails, check TypeScript errors. The build is the real integration test -- individual tasks compile in isolation and may still break when combined.

### Step 5: Structural integrity check
```
# Check section tag balance
python3 -c "import re; f=open('file.tsx').read(); print('OK' if f.count('<section')==f.count('</section>') else 'IMBALANCE')"

# Check IDs preserved
grep -c 'id="hero"' Hero.tsx    # should return 1
grep -c 'id="gallery"' Gallery.tsx  # should return 1
```

## Pitfalls

### Badge number drift
Subagents told to "refine header styling" may also change the section badge number (e.g. "01 / Gallery" -> "05 / Gallery") because they see the new page order. **Always explicitly forbid badge number changes** in the delegation goal.

### Component rename
A subagent may rename the exported component (e.g. `Gallery` -> `GallerySection`), breaking the import in App.tsx. The build will catch this, but it wastes a turn. Add "Preserve the export name" to the goal.

### CSS class removal
Subagents converting inline styles may drop CSS classes that other components reference (e.g. `.gallery-card` used by GSAP selectors). List all class names used by animations.

### Section ordering
After adding a new section between existing ones, verify the render order in App.tsx matches the intended page flow. A subagent may reorder siblings.

## Verification checklist (after any section batch)
- [ ] Build passes (exit 0)
- [ ] Section tag balance (<section> == </section> for each file)
- [ ] All IDs preserved (#hero, #gallery, #schedule, #toc, #materials, #contact)
- [ ] Navigation links point to valid section IDs
- [ ] TOC entries reference real section IDs
- [ ] App.tsx renders sections in correct order
- [ ] Export names match import names across all files
