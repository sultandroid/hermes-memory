# Aseer Museum — Cross-Interface Risks Report

**Source review:** Structural Report (12), FLS/Risk Assessments (15), Acoustics Report (13), Accessibility Report (08), Interface Statement (14), Visitor Occupancy & Flow (09), Drawing Register, Programming (03)

**Date:** 14 July 2026  
**Stage:** RIBA 3 (Concept/Developed) – scheme stage design, not IFC

---

## 1. STRUCTURAL × FIRE/LIFE SAFETY (FLS)

### RISK S1: Evacuation routes pass through structurally modified zones with unverified fire ratings
- **Evidence:**
  - LGF TG — new external wall opening with 203UC46 picture frame (if column in grid I is present) — this opening puts evacuees next to a structurally modified retaining wall whose fire-resistance rating is unverified.
  - The structural report acknowledges unknown external-wall construction/reinforcement; the fire resistance of the modified wall section is not addressed.
  - Interface Statement §8 confirms **no integrated FLS solution** exists; material fire ratings are "currently unknown."
- **Impact:** Structural modifications (TG opening, EX2 ramp demolition, CL1 stair infill) could compromise compartmentation if fire-stopping isn't coordinated.
- **Mitigation needed:** Fire strategy D&B contractor must receive structural modification schedule for fire-rating verification.

### RISK S2: Suspended art commissions obstruct escape routes / headroom
- **Evidence:**
  - BF G7: 4 timber frames 3.5×3.6 m suspended from soffit — potential headroom reduction in basement escape routes.
  - GF lobby: Neon "ariels" ≤300 kg suspended from grillage — same risk in entrance hall (primary egress path).
- **Impact:** Escape route headroom (min 2.0 m typical) may be compromised; suspended elements could become falling hazards in fire.
- **Mitigation needed:** Suspended-load GAs must be cross-referenced with Fire Escape Distance GAs (XX_{floor}_0011).

### RISK S3: EX2 external ramp "In Abeyance" — missing FLS analysis for alternative egress route
- **Evidence:** EX2 (external stair/ramp, GF) is flagged "In Abeyance" in the structural report; original ramp is at/near capacity and needs full demolition + steel/composite deck replacement.
- **Impact:** If EX2 is a fire-escape route (likely serving GF level), its deferred status means the egress strategy for the GF is incomplete.
- **Mitigation needed:** Confirm EX2's role in FLS strategy; scope the ramp replacement as a critical-path item linked to fire compliance.

### RISK S4: CL1 new stair (replacing escalator) — fire rating of infill slab not specified
- **Evidence:** Structural report proposes filling the escalator void with lightweight concrete or polystyrene void-former, casting 150 mm slab, resin-fixed reinforcement. No fire rating specified for the infill.
- **FLS context:** Stairs are fire-escape routes; escalator void penetrates 3 floors (BF→LGF→GF). The infill must achieve the same fire-resistance as the existing floor slab.
- **Impact:** If the void-former (polystyrene) is used without fire-rated topping, the slab-to-slab junction becomes a fire-path.
- **Mitigation needed:** Specify fire-rated void-former or fire-resistant concrete infill; coordinate with fire strategy D&B contractor.

---

## 2. STRUCTURAL × ACOUSTICS

### RISK A1: Acoustic ceiling treatments conflict with structural suspension points for art/AV
- **Evidence:**
  - Acoustic Report: Option 1 specifies Class A Sonacoustic ceiling panels, Class B Sonaspray (80% min coverage), Class C baffles, and ceiling-mounted acoustic panels.
  - Interface Statement §1e: "Numerous suspended exhibition elements + AV (projectors, speakers)" with fixings deferred to Detailed Design.
  - Structural report: BF G7 suspended from 2× spar beams fixed to perimeter beams; GF lobby grillage suspended from beam/column intersections.
- **Impact:** Acoustic ceiling treatments may occupy the same soffit zones required for suspension cables (RLI ≥ 4× safety factor). Where structural spar beams are placed, acoustic absorption coverage must be reduced or detailed around them.
- **Mitigation needed:** Ceiling-mounted acoustic treatment GAs must be overlaid with AV/structure suspension point GAs at Detailed Design.

### RISK A2: Ribbed floor slabs — vibration transmission between adjacent spaces
- **Evidence:**
  - Structural report: Floors are ribbed RC (tertiary ribs → secondary ribs → primary beams), thin and vulnerable to punch-through.
  - Acoustics Report: Vibration limit ≤0.05 m/s² for all occupied areas per ISO 2631-2:2003; equipment (lifts, HVAC) must be isolated from structure.
  - G2 Film Space (RT target 0.5–0.8 s) adjoins circulation and other galleries via ribbed slab — structure-borne noise from footfall and MEP is not addressed.
- **Impact:** The ribbed slab's stiffness and damping characteristics are unknown; footfall in CL1.BF (circulation adjacent to G7) may transmit vibration into G7/G12, exceeding the 0.05 m/s² threshold.
- **Mitigation needed:** Vibration modelling across the ribbed slab (CadnaR already in use for acoustic modelling — extend to vibration).

### RISK A3: Library spreader beams vs acoustic ceiling void
- **Evidence:** LR1 (1F Library) needs steel spreader beams "on the floor within finishes or dry-packed to soffit" to handle 17.9 kN/m² book-shelf load.
- **Acoustics:** Library target RT 0.9–1.5 s; achieving this requires ceiling acoustic treatment + Class A panels.
- **Impact:** If spreaders are dry-packed to soffit, they occupy the ceiling void that otherwise carries acoustic treatment. If on the floor within finishes, the raised floor depth must accommodate spreaders without reducing headroom to escape-route minimum.
- **Mitigation needed:** Library section detail must resolve spreader beam location × acoustic ceiling depth × escape headroom in one coordinated drawing.

---

## 3. STRUCTURAL × ACCESSIBILITY

### RISK D1: 1F ramp modifications (CL1) — structural capacity of existing base structure unknown
- **Evidence:**
  - Accessibility: 1:20 max ramp gradient required; new ramp at 1F CL1 proposed.
  - Structural report: Existing timber/stone steps demolished back to "base structure" for new timber+plywood ramp. Base structure construction is not identified.
- **Impact:** If the base structure is lightweight timber (as existing steps appear to be), it may not support the revised ramp loading + DDA-compliant handrail loads (0.74 kN/m line load typical at 900 mm).
- **Mitigation needed:** Structural assessment of the 1F CL1 base structure before ramp detail is finalised.

### RISK D2: TG new window (accessibility) × hidden column (structural)
- **Evidence:**
  - TG (LGF Temporary Gallery): New window opening proposed in 300 mm RC retaining wall.
  - Structural report: Grid I column (600×300 mm) exists in the wall — opening must avoid it. If column exists, a 203UC46 steel picture frame is needed.
  - TG is also the accessible route from King Khaled Road Entrance (LB2) into the galleries.
- **Impact:** Window sill height, threshold, and accessible viewing height (800–2000 mm per Accessibility) must be reconciled with the steel picture frame depth (203UC46 ≈ 203 mm deep) that may intrude into the window opening zone. If the column is present, window position shifts — potentially affecting the accessible path geometry.
- **Mitigation needed:** Confirm column location via intrusive survey before accessibility GA for TG is finalised.

### RISK D3: Goods-lift dependency for MEWP maintenance — lift structural capacity unverified
- **Evidence:**
  - Accessibility Report Part 1: Scissor lift (stored on site, moved via existing goods lift) provides 7.8 m working height; spider boom weighs 2280 kg.
  - Structural Report: Existing lift/escalator pit detail (ST-06) is **missing** from the drawing set — the only lift shaft detail is unknown.
- **Impact:** If the existing goods lift cannot bear 2280 kg (spider boom) or the scissor lift's transport weight, the entire maintenance access strategy (Option A) collapses, forcing scaffold-only access for all galleries.
- **Mitigation needed:** Survey existing goods lift capacity; verify ST-06 missing drawing content via RFI.

---

## 4. FIRE/LIFE SAFETY × ACOUSTICS

### RISK FA1: Lowered sprinklers (FLS requirement) conflict with ceiling acoustic baffles
- **Evidence:**
  - Interface Statement §1c: "Drop ceilings to create service voids — sprinklers lowered below ceiling height to maintain FLS response."
  - Acoustics Report: Option 1 includes Class C baffles, ceiling-mounted acoustic panels, and acoustic curtains (G2 Film Space).
- **Impact:** Sprinkler head placement and spray pattern coverage (NFPA 13 / SBC) may be obstructed by acoustic baffles; conversely, baffle placement may be driven solely by RT targets without accounting for sprinkler clearance zones (min 300 mm below sprinkler deflectors per NFPA 13).
- **Mitigation needed:** Combined reflected ceiling plan (RCP) showing sprinkler heads + acoustic baffles + lighting + AV — must be developed at Detailed Design.

### RISK FA2: NR 30 MEP noise target (galleries) — fire dampers and smoke-control fans
- **Evidence:**
  - Acoustics: Exhibition spaces require NR 30 — the most stringent target; drives fan-coil and duct silencer selection.
  - Interface Statement §3: HVAC modifications + additions throughout; MEP designed by D&B contractor.
  - Risk Assessment R1_4: No overall fire strategy; evac distances exceed 30 m SBC max in places.
- **Impact:** Smoke-control fans required for atrium smoke management (if the entrance hall / LB1 / retail combined space is open atria, which acoustic treatment suggests) will generate noise well above NR 30. Balancing smoke-extract acoustic performance with gallery noise targets is not addressed.
- **Mitigation needed:** Atrium smoke-extract fan specification must include acoustic silencers sized for NR 30 compliance; coordinate with acoustic consultant.

---

## 5. FIRE/LIFE SAFETY × ACCESSIBILITY

### RISK FS1: Evacuation distances exceed SBC 30 m — impacts on accessible egress
- **Evidence:**
  - Risk Assessment R1_4: Fire safety strategy gap — evac distances exceed Saudi BC max (30 m) in places; no overall fire strategy.
  - Interface Statement §8: "Several areas exceed Saudi BC max 30 m evac distance."
  - Accessibility: Wheelchair users require 900 mm movement width, 1600 mm turning circle. 1:20 ramp gradients for refuges.
- **Impact:** If evac distances are over 30 m, the fire strategy must provide refuges / phased evacuation for wheelchair users. Currently no refuges are identified. The 1:20 ramp gradients and 1600 mm turning circles required for wheelchair mobility must be factored into refuge locations — but no refuges are marked on any GA.
- **Mitigation needed:** Fire Strategy D&B contractor must produce refuge location GA cross-referenced with Accessibility GA (XX_{floor}_0006) for every floor.

### RISK FS2: Sprinkler relocation × accessible ceiling heights
- **Evidence:**
  - Interface Statement: Sprinklers proposed lowered in some locations + fire hose cabinets relocated — pending Fire Strategy validation.
  - Accessibility: 150 lux min lighting level; display heights 800–2000 mm; no headroom requirements explicitly stated but SBC requires 2100 mm min in accessible routes.
- **Impact:** Lowered sprinklers may reduce headroom below 2100 mm in accessible routes; relocated fire hose cabinets may intrude into accessible 900 mm clear width zones.
- **Mitigation needed:** All sprinkler relocation GAs must be checked against accessible route headroom + width.

---

## 6. ACOUSTICS × ACCESSIBILITY

### RISK AD1: Audio loop / hearing augmentation × acoustic panel placement
- **Evidence:**
  - Accessibility: Bilingual Arabic + English audio — all films; audio panel heights for ease of access.
  - Acoustics: NR 30 (galleries) means ambient noise must be very low; acoustic panels (Class A / B / C) are planned for walls and ceilings.
  - Interface Statement §4: Public Address system with fire-alarm relay → AV rack rooms.
- **Impact:** Induction loop systems for hearing augmentation require clear wall zones free of acoustic absorption that would dampen the electromagnetic field. Acoustic wall panels directly conflict with loop radiator placement. Floor-standing audio panels (eye-height for seated users) must be coordinated with wall-absorption panel layouts.
- **Mitigation needed:** Hearing-augmentation system GAs overlaid with acoustic wall-panel GAs at D&B stage.

### RISK AD2: Acoustically treated gallery zones × flexible/reconfigurable spaces for accessibility
- **Evidence:**
  - Programming: G2 Film, G5 Making, G14 Event Space, TG, EC Education Centre — all reconfigurable.
  - Acoustics: Derogations accepted for G1 Welcome, G3/G14, G5 Making — target RT not fully achievable due to adjacent-space coupling.
  - Accessibility: Minimum 1800 mm corridors, 1600 mm turning circles, 900 mm wheelchair clearance.
- **Impact:** Reconfigurable spaces (movable walls in TG, G5, G14) make it impossible to fix acoustic treatment to walls if the walls move. Yet the acoustic strategy relies on fixed wall-absorption panels. If TG walls are "alterable," the acoustic absorption must be in the ceiling, not walls — but ceiling-mounted acoustic panels conflict with suspension cables for AV + art. This triangle (flexible walls × fixed acoustic treatment × suspended AV/structural elements) is unresolved.
- **Mitigation needed:** Acoustic strategy for all reconfigurable galleries must be ceiling-dominant (not wall-dependent); coordinate with AV suspension points.

---

## 7. STRUCTURAL × COLUMN GRID IRREGULARITIES

### RISK G1: Grid I hidden column (LGF TG) — coordination across STRUCTURE, ARCHITECTURE, FLS
- **Evidence:** Structural report identifies a possible 600×300 mm column within the 300 mm RC retaining wall on grid I (per ST-04 & ST-09), cast monolithically.
- **Cross-interface implications:**
  - If confirmed, the new TG window location must shift (→ architectural GA change)
  - Window sill height and visual connection (→ accessibility viewing height 800–2000 mm)
  - Steel picture frame (203UC46) adds ~200 mm depth to window frame (→ potential thermal bridge / condensation risk)
  - Window penetration through fire-rated retaining wall (→ FLS compartmentation)
  - This is on the critical path because the report says "investigation required" — but no intrusive survey is scheduled in the current programme.
- **Mitigation needed:** Pre-construction intrusive survey of grid I wall is a CPP (Critical Path Predecessor) for architectural, structural, FLS, and accessibility drawings for LGF.

### RISK G2: No explicit column grid GA showing structural grid across all disciplines
- **Evidence:** Drawing register lists XX_{floor}_0007 "Building Grid GA" sheets but these are exhibition-furniture grids, not structural column grids. The structural report's only grid reference is to ST-04 & ST-09.
- **Impact:** Without a coordinated structural grid, multiple disciplines (MEP riser locations, partition lines, showcase alignment) cannot coordinate with existing columns.
- **Mitigation needed:** Publish a combined Structural Grid + Exhibition Grid GA at Detailed Design.

---

## 8. SYSTEMIC / PROGRAMME RISKS

### RISK P1: Three critical documents deferred entirely to D&B contractor
- Fire Strategy (full)
- MEP design (full)
- Security strategy (full)

The Interface Statement explicitly assigns FLS design to D&B contractor, yet the scheme-stage structural and acoustic reports have already committed to specific interventions (suspended loads, ceiling treatments, sprinkler lowering). **The D&B contractor inherits these commitments without being party to the design decisions.** This creates a high risk of redesign/rework when the fire strategy is developed and contradicts scheme assumptions.

### RISK P2: Missing drawing ST-06 (escalator pit) blocks multiple workstreams
- Blocks: CL1 new stair structural design → fire-rating of infill → MEP routing through escalator void → accessibility of new stair circulation.
- No RFI has been raised in the available documents.

### RISK P3: Art-commission weights are assumptions
- GF LB1 lobby artwork (2400 kg cylindrical): based on weight "provided" but not verified.
- GF CL1 lobby neon antennas (≤300 kg): "anticipated" — no confirmed weight.
- BF G7 suspended frames: final load depends on fabric tensioning.
- These assumed weights feed into structural cable sizing, which feeds into suspension-point fire-rating requirements.

### RISK P4: IFC-0004 Code C reference — not located in current document set
- The reference "IFC-0004" or "Code C" does not appear in any of the 7 reports reviewed. This likely originates from:
  - A consultant design review comment register (not in the pre-appointment pack)
  - A GC or MoC instruction separate from the CMS documentation
  - An issue-specific drawing note (maybe on a structural or FLS GA not included)
- **Action:** Request the IFC-0004 comment/review document from the project team to identify the specific concerns.

---

## SUMMARY OF CROSS-INTERFACE RISK SEVERITY

| Risk ID | Disciplines Involved | Severity |
|---------|---------------------|----------|
| S1 | STRUCTURAL × FLS | HIGH |
| S2 | STRUCTURAL × FLS | HIGH |
| S3 | STRUCTURAL × FLS | HIGH |
| S4 | STRUCTURAL × FLS | HIGH |
| A1 | STRUCTURAL × ACOUSTICS | HIGH |
| A2 | STRUCTURAL × ACOUSTICS | MED |
| A3 | STRUCTURAL × ACOUSTICS | MED |
| D1 | STRUCTURAL × ACCESSIBILITY | MED |
| D2 | STRUCTURAL × ACCESSIBILITY | MED |
| D3 | STRUCTURAL × ACCESSIBILITY | MED |
| FA1 | FLS × ACOUSTICS | HIGH |
| FA2 | FLS × ACOUSTICS | MED |
| FS1 | FLS × ACCESSIBILITY | HIGH |
| FS2 | FLS × ACCESSIBILITY | MED |
| AD1 | ACOUSTICS × ACCESSIBILITY | MED |
| AD2 | ACOUSTICS × ACCESSIBILITY | HIGH |
| G1 | STRUCTURAL × ALL | HIGH |
| G2 | STRUCTURAL × ALL | MED |
| P1–P4 | PROGRAMMATIC | HIGH |

**17 cross-interface risks identified, 9 rated HIGH severity.**

## Documents reviewed

| # | Report | File |
|---|--------|------|
| 1 | Structural Report | 12-Structural Report_rev A / 24120 - Aseer - Art Museum in KSA - Structural Report -.pdf |
| 2 | Designer Risk Assessments | 15-Risk Assessments_rev A / 6930_Aseer_Designer Risk Assessments.md |
| 3 | Acoustic Design Strategy | 13-Acoustics Report / 6930_Aseer_Acoustic Design Strategy _V2.md |
| 4 | Access, Maintenance & Accessibility | 08-Accessibility_ rev A / 6930_Aseer_Accessibility.md |
| 5 | Interface Statement | 14-Interface Statement_rev A / 6930 - Aseer_Interface Statement.md |
| 6 | Visitor Occupancy + Flow Analysis | 09-Visitor Occupany & Flow Analysis_rev A / 6930_Aseer_Visitor Occupancy + Flow Analysis.md |
| 7 | Drawing Register | 02_AS_Pre-Appointment Exhibition Drawings... / 6930_Drawing Register-3.xlsx |
| 8 | Project Overview | 01-Overview_rev A / 6930_Aseer_Overview.md |
| 9 | Programming | 03-Programming / 6930_Aseer_Programming.md |
