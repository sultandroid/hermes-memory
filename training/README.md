# Training & Learning Hub

> **Purpose:** A dedicated area for building **domain expertise** by studying real cases, contract precedents, arbitration rulings, codes & standards, and lessons learned across all projects.
>
> **Distinct from:**
> - `references/` — cross-entity facts (sister companies, Odoo patterns, etc.)
> - `MEMORY.md` / `USER.md` / `RULES.md` — behavioral rules, not domain knowledge
> - `skills/` — procedural skills (how to do X), not domain knowledge
> - Project repos — live work and project-specific facts
>
> **This hub is cross-project and cross-entity** (where legal). Every topic here can be applied to multiple projects.

## When the agent reads this

On user request for **learning** (training case, lesson extracted, "what can I learn from X"), search this directory first. If user asks a **domain question** (e.g. "how do I draft a variation order"), search here for precedents and lessons before answering from general knowledge.

## Folder Structure

```
training/
├── README.md                    # this file
├── READING_GUIDE.md             # how to study any case (5-min scan, 30-min deep read, 5-lesson extraction)
├── vocabulary.md                # cross-topic Arabic ↔ English terms (general)
│
├── claims-arbitration/          # nullity petitions, arbitration awards, dispute cases
├── contract-administration/     # VO, EOT, claims drafting, contract clauses
├── construction-management/     # site execution, method statements, HSE
├── design-management/           # RIBA stages, technical design, design reviews
├── procurement/                 # PQ, MA, vendor management, logistics
├── project-management/          # PMBOK, scheduling, risk, earned value
├── qs-cost-control/             # BOQ, variations, cost reporting, payments
├── bim-coordination/            # LOD, clash detection, ISO 19650
├── codes-standards/             # Saudi Building Code, FIDIC, NFPA, IBC
└── negotiation-disputes/        # pre-arbitration tactics, settlement, mediation
```

Every topic folder follows the same internal structure:

```
<topic>/
├── README.md        # purpose, scope, why it matters
├── vocabulary.md    # Arabic ↔ English terms specific to this topic
├── lessons.md       # top 5-10 lessons curated across all cases in this topic
├── resources.md     # online references, reading lists, links
└── cases/           # extracted case studies, one .md per case
    ├── 001-...
    ├── 002-...
    └── NNx-source.pdf  # original PDF archived alongside the extraction
```

## Cross-Topic Conventions

- **Case numbering:** `NNN-short-name-YYYY.md` (e.g. `001-binladin-vs-munshaat-2022.md`)
- **Anonymization:** when case involves real entities, anonymize to roles (Contractor, Claimant) unless the case is a public court ruling
- **Source PDF:** always archive the original PDF alongside the extraction (for re-reading and verification)
- **Lessons are extracted, not summarized:** every case produces 5 lessons minimum (see READING_GUIDE.md)
- **Vocabulary tables:** mark each term with **legal weight** (✅ strong / ⚠️ defensible / ❌ weak) so reading is faster

## How to Add a New Case

1. User pastes a PDF (or links a public ruling)
2. I extract: parties, contract type, dispute trigger, monetary heads, tribunal reasoning, court ruling, 5 lessons
3. Save to `cases/NNN-name-YYYY.md` + `cases/NNN-name-YYYY-source.pdf`
4. Update topic `lessons.md` with the new lessons (don't duplicate — link to the case for detail)
5. Update topic `vocabulary.md` if new terms emerged
6. Commit + push to hub

## How to Add a New Topic

1. Create `training/<topic-slug>/` with the 5-file scaffold
2. Add the topic to the folder tree above
3. Add the topic to the index in `PROJECTS.md` (if you want it visible there) — or skip, since training/ is self-discoverable
4. Add at least 1 case to make the topic real (empty scaffolds are a smell)

## Current Topics Status

| Topic | Status | Cases | Lessons |
|---|---|---|---|
| claims-arbitration | Active | 1 (Binladin vs Munshaat 2022) | 5 |
| contract-administration | Scaffolded | 0 | 0 |
| construction-management | Scaffolded | 0 | 0 |
| design-management | Scaffolded | 0 | 0 |
| procurement | Scaffolded | 0 | 0 |
| project-management | Scaffolded | 0 | 0 |
| qs-cost-control | Scaffolded | 0 | 0 |
| bim-coordination | Scaffolded | 0 | 0 |
| codes-standards | Scaffolded | 0 | 0 |
| negotiation-disputes | Scaffolded | 0 | 0 |

---

*Last updated: 2026-07-31 — restructured from `references/training/` to top-level per user instruction (cross-project, not a child of references/).*
