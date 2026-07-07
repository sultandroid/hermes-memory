# Structural Gallery-Per-Floor Submission Pattern

For museum fit-out projects, structural design items are often per-floor per-gallery rather than system-wide. Each gallery/art commission needs its own structural support design (hanging loads, wall openings, floor reinforcement).

## Source Document: Design Philosophy (consultant-prepared)

The Design Philosophy document (typically by LON or similar) lists by-floor structural items:

```
Basement:     G7 Contemporary Art Commission, G12 Tom Nicholson, CL1 New Stairs
LGF:          CL1 Stair, G14 Contemporary Art Commission, TG Opening in external wall
GF:           CL1 Lobby Hanging Artwork, LB1 Lobby Artwork Comm, LB1 External Signage, EX2 Stairs & Ramp
1F:           CL1 Ramp Modifications, CA2 Terrace Balustrade, LR1 Library Area
Second Floor: (if applicable)
Roof:         (if applicable)
```

## Staggered Per-Floor Start Dates

Gallery items on each floor start after Arch GA for that floor is available. Use relative offsets from the structural baseline:

```python
BASE = d(2026, 6, 29)
FLOOR_OFFSETS = {
    'BF': timedelta(days=0),    # Basement — same as baseline
    'LGF': timedelta(days=7),   # +7d after BF
    'GF': timedelta(days=14),   # +14d
    '1F': timedelta(days=21),   # +21d
    '2F': timedelta(days=28),   # +28d
    'RF': timedelta(days=35),   # +35d
}

def gallery_item(ref, desc, floor, tier, pkg, rm=''):
    start = BASE + FLOOR_OFFSETS[floor]
    return mk(ref, desc, 'Structural', tier, pkg, rm, start=start)
```

## Each Gallery Item Tracks These Steps

Per the existing Structural register pattern, gallery items have a tier-based lifecycle:

| Tier | Stage | What |
|------|-------|------|
| 1 | 50% Design | Design criteria, survey data for that gallery |
| 2 | 90% Design | Assessment — loading calculations for art commissions |
| 3 | 100% Design | Design details — support structure, connections, anchorage |
| 4 | IFC | Installation specs, ITP, AFC, O&M |

## Completed vs Pending Items

Items from earlier phases (SD Report, Design Philosophy, As-Built drawings) are already submitted. Mark them amber in the register:

```python
AMBER = PatternFill('solid', fgColor='FFF4B942')

# In the write loop:
if 'Submitted' in str(rm):
    cell.fill = AMBER
```

This lets the reader immediately distinguish what's done from what's pending.
