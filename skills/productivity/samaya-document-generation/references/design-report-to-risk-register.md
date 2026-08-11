# Extracting Risks from Design / Visitor-Experience Reports

## When to use
After ingesting a large design report (Stage 4+ Visitor Experience, Scenography, Audit Report, etc.), the user expects the **report's design findings** to drive risk-register updates — NOT just the email correspondence that accompanied it.

## User correction (2026-08)
When asked "any risks need to update?", I updated risks from the email scan (EOT, rigging PQ, AV content). The user corrected: *"i mean new or updates form the full reports i sent to you"* — they wanted risks derived from the **design report content itself**.

## Workflow
1. Read the design report fully (use kimi CLI for 10k+ line PDFs — see `kimi-cli-large-doc-extraction.md`).
2. Extract the design findings that create NEW risk or change existing risk:
   - Showcase/setwork capacity vs updated object lists (e.g. G3 Al Muftaha: 5.2m showcase insufficient for 34 objects → needs 6400mm + angled plinth + label rail + GBH fabrication amendment)
   - Art commissions on unverified structure (weight/fixing)
   - AV/interactive content now defined per gallery (changes PRR-AV-01 from "scope gap" to "production coordination")
   - Object list / grouping / hierarchy clarifications still required from MoC
3. For each finding, decide: NEW risk row, or UPDATE an existing risk's cause/response.
4. Add NEW risks with a distinct category code (e.g. `PRR-SHC-02` for showcase redesign) and cross-reference the source report + related risks (e.g. PRR-PRC-02 showcase long-lead, PRR-DES-05 object-list redesign).
5. Commit.

## Example — G3 Al Muftaha showcase redesign (PRR-SHC-02)
- **Source:** NRS Audit Report 2 (ZD-0108) + Visitor Experience Report (MOC-ASE-AR-ARC-GEN-DDD-PR01-00)
- **Finding:** Stage 3 object list had no objects; latest list has 34 items + 3 minimal-info. Current 5.2m Type 3 showcase cannot accommodate. NRS recommends angled plinth + integrated label rail + extension to 6400mm OA (4×1600mm bays). Vertical labels cast shadows — not recommended.
- **Risk:** Critical (3×4=12). Showcase redesign + GBH fabrication drawing amendment; object placement rework; programme delay to already-long-lead showcase production.
- **Response:** Confirm redesign with NRS + GBH; instruct GBH to amend fabrication drawings (variation if instructed); obtain MoC object list + grouping/hierarchy/'star' object clarification.

## Pitfall
Do NOT stop at email-driven risk updates. Design reports carry the substantive technical risks (showcase capacity, structural loading of commissions, AV content scope). Always mine the report body itself.
