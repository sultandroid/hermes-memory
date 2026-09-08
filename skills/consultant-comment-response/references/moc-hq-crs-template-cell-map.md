# MOC_HQ CRS Template — Cell Map + Material-Cert Compliance Analysis

## The official template (USE THIS, not a custom build)

The user's standing instruction: **use the official MOC_HQ CRS template, never build a custom CRS workbook from scratch.** The user will correct you if you create a new file: "use different template, I will send the last template."

**Public URL (deployed, no auth):**
`https://samaya-factory.com/assets/templates/CRS_Template_MOC_HQ.xlsx`

**Local copy:** the user sends it as an attachment; it lands in `~/.hermes/cache/documents/`. Copy it, fill it, save as `CRS_[DocRef]_Rev[XX].xlsx` in the submittal's Rev folder on OneDrive.

**Deploy pattern for shared templates** (so any agent can fetch them):
```bash
ssh -p 65002 u517606786@samaya-factory.com "mkdir -p ~/domains/samaya-factory.com/public_html/build/assets/templates"
cat /tmp/CRS_Template_MOC_HQ.xlsx | ssh -p 65002 u517606786@samaya-factory.com "cat > ~/domains/samaya-factory.com/public_html/build/assets/templates/CRS_Template_MOC_HQ.xlsx && chmod 644 ..."
curl -s -o /dev/null -w "%{http_code}\n" https://samaya-factory.com/assets/templates/CRS_Template_MOC_HQ.xlsx   # expect 200
```
Then add a row to the style-guide table in the repo's `AGENTS.md` so every agent knows the URL.

## Template structure (verified cell map)

Sheet name: `CRS`. Header block rows 1-7, comment rows 11-41, legend/signature rows 42-50.

**Header fields (fill these):**
| Cell | Field |
|------|-------|
| D4 | PROJECT NAME (e.g. "Regional Museum (Aseer)") |
| I4 | PROGRAMME No. / doc ref |
| D5 | CRS NUMBER |
| K5 | DATE |
| D6 | DOCUMENT No. |
| K6 | DISCIPLINE |
| D7 | DOCUMENT TITLE |
| K7 | DOCUMENT TYPE |

**Comment rows (11-41), one row per CG comment:**
| Col | Field |
|-----|-------|
| A | No. |
| B | Initial |
| C | Sheet |
| D:H (merged) | Reviewer Comment |
| I:N (merged) | Originator Reply |
| O | Reply By |
| P:Q (merged) | Reply Status by Reviewer |

**openpyxl notes:**
- D:H, I:N, P:Q are merged per row — write to the top-left cell only (`ws["D11"]`, `ws["I11"]`, `ws["P11"]`).
- Column A values are strings (`'1'` not `1`).
- The "Reply Status by Reviewer" column (P) is filled by the CONSULTANT, not by us. Put a provisional Closed/Open there but expect CG to overwrite it.
- Preserve all original formatting/merges — only fill cells, never restructure.

## Material-cert compliance analysis (which certs are legit vs CG overreach)

When CG demands a batch of certificates on a material submittal (e.g. MA-0007 patinated brass), classify each before deciding to comply or push back:

| Cert | Legit? | Why |
|------|--------|-----|
| **Oddy test** | ✅ Always | Museum-critical — detects corrosive emissions that harm artefacts. The decisive one. |
| **Chemical composition** | ✅ | Proves the real alloy (e.g. CuZn37/C27200). A manufacturer datasheet (KME) covers this. |
| **MSDS** | ✅ | Standard safety sheet, easy, not a test. |
| **VOC** | ⚠️ Partial | **Metals do not emit VOC** — the lacquer/coating does. Only matters in sealed showcases, not open walls/doors. |
| **Off-gassing** | ❌ Overreach | **Duplicates Oddy + VOC.** A passed Oddy test already confirms no corrosive emissions. |
| **Fire-rated** | ❌ Overreach | **Metal does not burn.** Fire-rating matters for combustible materials (fabric, wood, plastic), not brass. |
| **2 alternative manufacturers** | ❌ Overreach | If the alloy is single-source globally (GBH confirmed), demanding 2 certified alternatives is impossible. |

**Key domain fact:** a material datasheet (e.g. KME CuZn37) is NOT a VOC test. VOC comes from the surface coating, so it must come from an emission test on the finished (lacquered) sample — not from the alloy datasheet.

**Strategy (don't fight every item):** submit what you have (Oddy PASS + composition + MSDS → 3 of 7 closed), push back with technical justification on the overreach items (fire-rated: metal non-combustible; off-gassing: covered by Oddy), and defer the rest as a Rev.02 addendum with a firm date. This puts the pressure on CG — if they reject, they're delaying the programme with unjustified demands, not us.

## MA-0007 patinated brass — current state (as of Sep 2026)
- Oddy test **PASSED** (NonaChem T2607222, 21-Aug-2026, rated P/Permanent on Ag/Cu/Pb) — clears the main Code C blocker.
- Chemical composition covered by KME CuZn37 datasheet.
- Remaining pending (GBH lead-time, Rev.02): MSDS, VOC, off-gassing, fire-rated.
- 2 alternatives: IGP 591T PARKOUR powder coat (submitted, per NRS) + PVD KSA sample (in development).
- Risk PRR-PRC-05 (Critical, target close 2026-09-14) — the Oddy PASS should drop its score; update the risk when the resubmission is accepted.
- CG's latest email (Mansour, 03-Sep-2026): "Kindly update us regarding the Patinated Brass sample" — needs a reply anchored on the Oddy PASS.
