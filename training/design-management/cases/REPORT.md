# Design Management — Research Report (31 July 2026)

## Mission

Build **6–10 design-management case files** from the 71 raw Tavily extracts that the previous
subagent had already archived at
`/home/hermes/.hermes/profiles/digitalhermes/home/hermes-memory/training/design-management/raw-extracts-tavily-2026-07-31/`.
The previous subagent completed the Tavily search and extraction phase but timed out before
writing the case files. This task read the existing archive, selected the strongest sources,
filled two coverage gaps with fresh Tavily searches, and produced structured case files
with a 5-lesson extraction grid (Vocabulary / Evidence / Procedural / Strategic / Principle).

## Output

**9 case files** in `/tmp/tavily-research-design-mgmt/cases/`:

| # | Slug | Lines | Bytes |
|---|---|---|---|
| 01 | `001-riba-plan-of-work-design-information-exchanges.md` | ~50 | 6.3 KB |
| 02 | `002-chambers-construction-law-2026-saudi-arabia.md` | ~55 | 7.5 KB |
| 03 | `003-hka-crux-saudi-design-information-claims.md` | ~55 | 7.0 KB |
| 04 | `004-as-built-drawings-closeout-handover.md` | ~50 | 6.5 KB |
| 05 | `005-value-engineering-saudi-50-percent-rejection.md` | ~55 | 7.1 KB |
| 06 | `006-cii-constructability-programme-not-review.md` | ~55 | 7.5 KB |
| 07 | `007-bim-coordination-saudi-national-strategy-compliance.md` | ~55 | 7.3 KB |
| 08 | `008-variation-order-management-saudi-kfu-sapi.md` | ~60 | 8.6 KB |
| 09 | `009-epc-design-freeze-engineering-phase.md` | ~60 | 8.3 KB |
| — | `INDEX.md` | — | 6.9 KB |
| — | `REPORT.md` (this file) | — | — |

**All 10 brief themes** are covered; 6 are covered by a *primary* case file, 4 are covered as
*secondary* themes within other cases (see Theme Coverage Matrix in INDEX.md).

## Methodology

### Step 1 — Inventory the archive

The previous subagent's archive at
`/home/hermes/.hermes/profiles/digitalhermes/home/hermes-memory/training/design-management/raw-extracts-tavily-2026-07-31/`
contains:

- **71 files** total
- **19 successful extract files** (`extract_*.json` with non-empty `results[]`)
- **20 search-bundle files** (`theme01_primary.json` through `theme10_secondary.json`) — the raw Tavily search results that were *input* to the extraction phase; not used for this task
- **28 single-page mirror files** (`x_*.json` and `x2_*.json`) — duplicates / second-page extracts; not used
- **2 utility scripts** (`extract_url.py`, `run_searches.py`) — subagent internals; not used
- **2 empty `extract_*.json` files** (Tamimi, FIDIC risk, autodesk, marsh, etc.) — Tavily could not fetch the page; treated as zero content

Net: **19 usable sources** for case files.

### Step 2 — Map sources to themes

Mapped all 19 sources against the 10 brief themes. The richest sources (Chambers Saudi 2026,
HKA CRUX Saudi, MDPI KFU VOM, CII RT-034, BIM Design LLC Saudi) cover **Saudi-specific
material directly relevant to the Aseer Museum brief** and were prioritised.

### Step 3 — Identify gaps

A grep across all 19 extracts for `design freeze` and `TDS` / `technical design submittal`
returned **zero hits** for the literal terms. Two themes were therefore un-covered:

- **Theme 2 (Design freeze disputes)** — covered in spirit by the EPC-flavoured sources but no
  *direct* extract existed
- **Theme 5 (TDS approval)** — covered in spirit by the RIBA Stage 4 / SBC submission materials
  but no *direct* extract existed

### Step 4 — Fill the gaps with focused Tavily searches

Two gap-fill Tavily extracts were generated and saved to `/tmp/tavily-research-design-mgmt/raw/`:

1. `gap01_design_freeze_epc.json` — captures a 2025 LinkedIn post by Haseebuddin Syed (PMP-PMI)
   arguing that "nearly 70% of EPC issues are locked in during the engineering phase" with
   *late or continuously changing design freeze* as the first named cause
2. `gap02_saudi_submittal_approval.json` — captures the 2013 Alsinaidi paper on the
   Submittal-Approval Performance Index (SAPI) for Saudi construction

### Step 5 — Select the 9 strongest cases

Each case was selected on the following criteria:

1. **Authoritative source** — preferred Chambers > HKA > CII > MDPI > RIBA > Procore > industry blog
2. **Saudi-relevance** — preferred when the source is Saudi-specific, because the user is
   working on a Saudi-delivered museum project
3. **Verbatim quotability** — required a strong, attributable verbatim quote
4. **Design-management relevance** — preferred the source that most directly addresses the theme
5. **5-lesson extraction potential** — preferred the source that yields clean vocabulary,
   evidence, procedural, strategic, and principle lessons

### Step 6 — Write case files

Each case file follows the same template (calibrated to match the existing
`contract-administration` case files in
`/home/hermes/.hermes/profiles/digitalhermes/home/hermes-memory/training/contract-administration/cases/`):

- **Citation block** — title, author, year, URL, verification status
- **Quick Facts** — forum / doc type, subject, outcome
- **Theme Mapped** — primary + secondary brief theme(s) covered
- **Direct Quote** — at least 1 verbatim quote from the source extract
- **Summary** — 2–3 sentences with the actionable insight
- **5 Lessons Extracted** — Vocabulary / Evidence / Procedural / Strategic / Principle
- **Open Questions for Follow-up** — 3 questions for future research
- **Cross-References** — links to other case files in this topic and across topics

## What Worked

- **The 5-lesson extraction grid** is a *forcing function* — it converts a generic article
  into a design-management actionable lesson by requiring the writer to think in five different
  registers (term definition, evidence artefact, workflow, choice, rule)
- **Saudi-specific sources dominate the value** — HKA CRUX Saudi, Chambers 2026 Saudi, MDPI KFU
  VOM, and BIM Design LLC Saudi carry the *jurisdiction-specific* data that a UK/US-centric
  design management article would not provide
- **The CII RT-034 extract is foundational** — for a 30+ year-old report it is still the
  cleanest statement of the constructability-programme-vs-review distinction
- **Gap-fill Tavily searches were cheap and decisive** — two searches of ~3 seconds each filled
  the two uncovered themes without burning the budget

## What Did Not Work / Caveats

- **PI / liability cap figures** — the original archive has an empty extract for the Al Tamimi
  PI primer (`extract_tamimi.com-professional-indemnity-and-fidelity-insurance.json` — failed
  Tavily fetch). Without that, Case 02 can describe the *legal envelope* of liability but not
  give a specific cap figure. **Follow-up action:** re-try the Tamimi PI primer via Tavily
  extract (not search) to get the article body, or pull a Pinsent Masons or HKA PI cap benchmark
  for Saudi consultants
- **Al Tamimi and Pinsent Masons** — the brief flagged both as priority sources, but neither
  produced a usable extract in the previous subagent's archive. The closest *legal* source is
  Chambers (GLA & Co.), which is a peer-reviewed practice guide but not a law-firm article
- **MDPI and itcon.org articles are long** (100K+ chars of raw content) — the extracts are
  readable but the verbatim quotes had to be selected from the most quotable paragraphs (the
  introduction and abstract), not the methodology or results sections. The case files therefore
  reflect the *thesis* of each article more than the *evidence*
- **Case 09 (EPC design freeze) is a LinkedIn post** — the most quotable single source on
  design freeze but the lowest-authority source in the set. It is balanced by Case 01 (RIBA),
  Case 06 (CII), and Case 07 (BIM Design LLC) which all converge on the same engineering-phase
  primacy argument

## Aseer-Museum Specific Recommendations

The user's brief notes that the user is a **Tech Office Manager at a firm working on the
Aseer Museum with Nissen Richards Studio (NRS) as design lead.** Each case file is
written to be directly actionable for that project. The five highest-leverage recommendations
are:

1. **Adopt the RIBA Plan of Work 2020 as the contractual anchor for the Aseer design
   programme** (Case 01) — populate the Stage 1 Responsibility Matrix with NRS as design lead
   and the local Saudi architect as the SBC submission lead. Without this, the multi-firm
   design responsibility question will arrive at handover
2. **Refuse to let the design programme compress into the construction programme** (Case 09
   + Case 03) — HKA CRUX shows 97.2% EOT on Saudi projects; CII RT-034 shows that late-input
   constructability has no measurable benefit. The design phase is the *risk control centre*,
   not a cost to be minimised
3. **Build the VOM process around a single Employer Design Review (EDR) gate** (Case 08 +
   Case 02) — the modified-FIDIC Saudi reality (employer's approval required, not the
   consultant's) means that ad hoc approvals are the single largest controllable delay
4. **Run a continuous BIM coordination programme on a weekly cycle, not a single pre-IFC pass**
   (Case 07) — the Saudi National BIM Strategy has made BIM coordination a compliance gate,
   and the CDE audit log is the primary evidence in any future multi-discipline dispute
5. **Hold the design freeze at RIBA Stage 4 with a signed Design Freeze Certificate, a
   Freeze Exception Register, a Post-Freeze Change Procedure, and a Constructability Review
   Log** (Case 09) — without these four artefacts, "design freeze" is a wish, not a gate

## Suggested Next Steps (for the parent agent or user)

- **Pull the Al Tamimi PI primer** — the most consequential gap in the current set. A
  successful extract of the Tamimi article would add a 10th case file on Theme 4 (PI / liability
  cap, period) with a Saudi-specific cap figure
- **Pull a Pinsent Masons or HKA article on the designer's duty of care under Saudi / NCTL
  2023** — would strengthen the legal analysis in Case 02
- **Pull a Nissen Richards Studio (NRS) reference project** — would add a peer-project
  benchmark to the Aseer case
- **Update `vocabulary.md`, `lessons.md`, and `resources.md`** in
  `/home/hermes/.hermes/profiles/digitalhermes/home/hermes-memory/training/design-management/`
  to reflect the new case files
- **Consider promoting the design-management topic to the Aseer Museum project's `cases/`
  folder** (i.e. the project repo, not the hub) so that the Aseer-specific case files are
  visible alongside the hub training material

---
*Generated 31 July 2026 by subagent task on the design-management topic. All 9 case files
and supporting documents are in `/tmp/tavily-research-design-mgmt/cases/`.*
