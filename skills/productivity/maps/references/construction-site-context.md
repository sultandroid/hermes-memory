# Construction Site Context & Neighbor Identification

Use this recipe when a user gives site coordinates and asks:
- "What buildings / roads / landmarks are around this site?"
- "Identify surrounding neighbors for the survey/MOS scope."
- "What is the site context at LAT LON?"

The `maps_client.py` `nearby` command is good for categorized POIs (mosque, hospital, supermarket, etc.), but construction site context often needs **unnamed buildings, roads, topographic features, and heritage structures** that do not map neatly to the 46 POI categories. For that, query OpenStreetMap directly via the Overpass API.

## Quick recipe

### 1. Overpass QL query

Save as `site_context.ql` and POST it to Overpass:

```text
[out:json][timeout:25];
(
  way(around:500,18.2163889,42.4990278)["building"];
  node(around:800,18.2163889,42.4990278)["name"];
  way(around:800,18.2163889,42.4990278)["name"];
);
out body center;
>;
out skel qt;
```

Adjust the radius:
- `500 m` for immediate neighbors / buildings
- `800–1500 m` for wider context (roads, wadis, districts)

### 2. Run it

```bash
curl -sL -X POST -H "Content-Type: text/plain" \
  --data-binary @site_context.ql \
  https://overpass-api.de/api/interpreter -o site_context.json
```

If `overpass-api.de` is slow, try the mirror: `https://overpass.kumi.systems/api/interpreter`.

### 3. Parse and distance-rank

```python
import json, math

lat0, lon0 = 18.2163889, 42.4990278  # site coordinate

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1-a))

with open('site_context.json') as f:
    data = json.load(f)

items = []
for el in data.get('elements', []):
    tags = el.get('tags', {})
    name = tags.get('name:en') or tags.get('name')
    if not name or tags.get('place') == 'city':
        continue
    lat = el.get('lat') or el.get('center', {}).get('lat')
    lon = el.get('lon') or el.get('center', {}).get('lon')
    if lat is None or lon is None:
        continue
    kind = (tags.get('building') or tags.get('amenity') or
            tags.get('shop') or tags.get('highway') or
            tags.get('leisure') or tags.get('tourism') or
            tags.get('healthcare') or 'feature')
    items.append({
        'name': name,
        'kind': kind,
        'dist_m': round(haversine(lat0, lon0, lat, lon)*1000, 1)
    })

items.sort(key=lambda x: x['dist_m'])
for it in items[:30]:
    print(f"{it['dist_m']:>8.1f} m  {it['kind']:<18}  {it['name']}")
```

## What the output looks like

Example for Aseer Regional Museum site (18°12′59″N 42°29′56.5″E):

| Distance | Kind | Name |
|---------:|------|------|
| 69 m | footway | Art Street pedestrian walkway |
| 85 m | mosque | King Abdulaziz Grand Mosque |
| 90 m | tertiary | King Khaled Road |
| 133 m | construction | Abha Private Hospital |
| 154 m | feature | Al Bahar Historical Square |
| 209 m | attraction | Shada Archaeological Palace |
| 299 m | park | Al-Sabeel Park |
| 334 m | pedestrian | Al-Qabil Bridge |
| 392 m | supermarket | Universal Cold Store |
| 454 m | feature | Wadi Abha |
| 740 m | feature | Al-Muftahah Village |
| 742 m | hospital | Prince Faisal Bin Khalid Cardiac Center |

## How to present results

- Group by distance rings: **immediate (<100 m)**, **adjacent (100–300 m)**, **wider context (300–1000 m)**.
- Highlight items relevant to the survey/MOS scope: roads (access/logistics), adjacent buildings (daylight/context), heritage structures (record), hospitals/mosques (noise/safety constraints).
- If the user is building a Section 4 "Survey of Surrounding Area / Neighbors" table, feed the named features straight into the Element/Purpose table.

## Pitfalls

- OSM data is community-maintained; verify critical distances against the project survey or aerial imagery.
- Named features may appear multiple times (e.g., the same road at different intersections) — de-duplicate by name + kind before presenting.
- The coordinate in the MOS may be approximate. Cross-check with the actual site boundary before claiming a neighbor is 70 m away.
- Avoid Arabic-only names in client-facing tables. Use `name:en` when available; romanize Arabic names if no English tag exists.
