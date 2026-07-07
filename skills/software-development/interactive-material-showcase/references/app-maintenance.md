# Aseer Material Showcase — App Maintenance Guide

## Key Files
| File | Purpose |
|------|---------|
| `src/sections/Gallery.tsx` | Gallery modal, image viewer, sidebar legend, hotspot pins, SCHEDULE_FIELD_GROUPS |
| `src/sections/Schedule.tsx` | Schedule table with dropdown filter, pagination, search |
| `src/index.css` | Modal styles, responsive breakpoints, tooltip card CSS (.htc-* classes) |
| `src/lib/utils.ts` | cleanName(), summarizeDescription() — dimension trimming |
| `src/data/materials.json` | All material records (~1.2MB) with schedule_key, source, code, description |
| `src/lib/materialStore.ts` | localStorage-backed CRUD store with merge from materials.json |
| `~/Desktop/deploy.sh` | Build + scp to samaya-factory.com:65002 |

## SCHEDULE_FIELD_GROUPS (Info Card Layout)
In `Gallery.tsx`, this constant maps each `schedule_key` → array of field groups. Each group has:
- `label`: group header text
- `fields[]`: `{ key: 'exact JSON key', label: 'Display label', mono?: true, full?: true }`

**⚠ Key casing**: must match materials.json exactly. Common lowercase keys: `description`, `colour`, `finish`, `supplier`, `substrate`. Never copy casing from schedule JSON files — use materials.json as source of truth.

### Group naming convention
- Code/ID fields → `mono: true`
- Long text fields → `full: true` (spans both grid columns)
- 2–3 groups max per type, 2–4 fields per group
- Most important identity fields first

## Sidebar Legend Grouping
Materials in the sidebar are grouped by `schedule_key` with labeled section headers. Group order (defined in code):
```
Finishes → Setwork → Showcase → Graphic → Wayfinding → FF&E → Object
→ Exhibit → Art Commission → Media → AV Equipment → Lighting
→ (remaining alphabetical)
```

Colors: header label `#5A4E2A` (dark brown) on `rgba(200,164,92,.12)` background, `fontWeight:700`.
Sidebar width: `320px`.

## Responsive Modal
- **Desktop**: image left + 320px sidebar right in flex row
- **Mobile (≤768px)**: image capped at 50vh, `flexWrap` drops sidebar below, modal has `overflow-y:auto` for natural scrolling
- No custom drag/pan — page scrolls normally

## Stage-Based Data Filtering
```js
// In Gallery.tsx — filter matMap to exclude unnecessary schedules
const matMap = new Map(mats.filter((m:any)=>
  !m.schedule_key?.includes('mockup')
).map((m:any)=>[m.code, m]));
```
Also filter Schedule.tsx dropdown keys and remove unused SCHEDULE_FIELD_GROUPS entries.

## Dimension Trimming (utils.ts)
`cleanName(desc)` strips:
- Leading dimensions: `"2500 x 450mm "`, `"1960x450mm "`, `"3500(w) x 4000(h) x 400(d)mm "`
- Leading `"Nx "` patterns: `"8x "`, `"3x "`
- Trailing dimension fragments: `" - 420mm x 1420mm"`, `" / 286 x 205mm"`
- Thickness: `"3mm thick "`, `"10mm thick "`

Applied to: `.htc-name` (tooltip title), sidebar material descriptions. Not applied to Schedule.tsx table.

`summarizeDescription(desc, maxLen=100)` — cleans name then truncates with ellipsis.

## Deploy
```bash
bash ~/Desktop/deploy.sh
```
1. `npm run build` in the `app/` directory
2. tar dist/
3. scp -P 65002 to samaya-factory.com
4. Extract to `public_html/build/aseer/`
