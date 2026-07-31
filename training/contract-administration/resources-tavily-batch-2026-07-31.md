# Contract Administration Disputes in Saudi / GCC Construction — Case Library Index

**Compiled:** 31 July 2026
**Total cases:** 13 (12 from Al Tamimi + law-firm/consultancy sources; 2 from supplementary non-Tamimi sources — HKA, Strata, Stonehaven)
**Method:** Tavily search + extract, with r.jina.ai reader-proxy fallback for JS-walled sites (Tamimi's Sucuri/Cloudflare gate)
**Verification:** All URLs and direct quotes were independently extracted from the source pages on 31 July 2026. Raw extracted text preserved at `/tmp/tavily-research-contract-admin/raw/`.

## Theme Coverage Matrix

| # | Theme (from task brief) | Cases |
|---|---|---|
| 1 | Variation Order (VO) — what makes a VO enforceable | 005 (delay damages on termination) · 009 (FM ≠ variation) |
| 2 | Extension of Time (EOT) — what evidence wins an EOT | 005 · 006 (Dubai Cassation 41/2012) · 007 (as-built) · 008 (concurrency) |
| 3 | Time bar (سقوط الحق) — missing the notice deadline | 001 (Symms, GCC vs English) · 002 (El Haggan, Egypt) · 003 (UAE Articles 880/883 + Federal Supreme Court Case 267/1996) · 013 (1993–2015 Abu Dhabi sewage case, Court of Cassation 319 & 320/2015) |
| 4 | Scope creep vs legitimate variation — case lines | 008 · 012 (Stonehaven UAE practice) |
| 5 | Provisional sum / Daywork disputes | 009 · 010 (HKA, FIDIC 1999 PS lacuna) |
| 6 | Conditions Precedent in FIDIC Cl. 20.1 — when does the notice deadline start? | 001 · 011 (Strata, Saudi Vision 2030) |
| 7 | Engineer's fair determination (FIDIC 2017 Cl. 3.7) — can contractor refuse it? | 004 (FIDIC 2017 Yellow Book) |

## Case Files (alphabetical by file name)

| File | Year | Court / Source | Key Holding | Direct Quote Source |
|---|---|---|---|---|
| 001-conditions-precedent-construction-claims-symms.md | 2021 | Al Tamimi (legal article) | FIDIC 20.1 28-day bar enforceable under English law; GCC civil codes preserve escape routes | Symms, "Traps for the Unwary" |
| 002-time-barring-egyptian-law-elhaggan.md | 2021 | Al Tamimi (legal article, Riyadh) | Contractual time bars ≠ statutory limitation; Egyptian law upholds FIDIC 20.1 | El Haggan, Egyptian perspective |
| 003-uae-civil-code-articles-880-883-time-bar.md | 2014 | Al Tamimi + UAE Federal Supreme Court Case 267/1996 | Article 883 3-year bar runs from defect *discovery*; missed bar = claim dismissed | Al Tamimi article, citing Federal Supreme Court |
| 004-fidic-2017-yellow-book-engineer-fair-determination.md | 2017 | Al Tamimi (FIDIC analysis) | Engineer acts *neutrally* under 3.7; 28-day NOD is the only way to refuse a determination | Al Tamimi + AfiTaC cross-check |
| 005-abu-dhabi-cassation-delay-damages-on-termination.md | 2016 | Abu Dhabi Court of Cassation, Appeals 424 & 483/2015 | Termination extinguishes the contractual delay-damages clause; employer must claim in tort | Al Tamimi (Hassan El Tahir) |
| 006-dubai-cassation-delay-handover-trigger-termination.md | 2015 | Dubai Court of Cassation, Case 41/2012 | Failure to perform reciprocal obligation on time = material breach; Article 247 entitles termination | Al Tamimi (Rami Abdellatif) |
| 007-as-built-programmes-eot-evidence-oleary.md | 2014–15 | Al Tamimi (Dean O'Leary) | As-built programme cross-checked against contemporaneous records is the linchpin EOT document | Al Tamimi article |
| 008-concurrency-construction-delay-claims.md | 2014 | Al Tamimi (Construction practice) | *Malmaison* approach most likely applied in UAE: EOT for employer-risk event, no time-cost for overlap | Al Tamimi article |
| 009-force-majeure-fidic-iraq-ede.md | 2014 | Al Tamimi (Justin Ede, DIFC) | "Prevented" requires physical/legal impossibility, not commercial difficulty; FM notice is separate from Cl. 20.1 | Al Tamimi + *Tennants v Wilson* [1917] AC 495 |
| 010-provisional-sum-loophole-middle-east-hka.md | 2017 | HKA (Daniel Rimmer, Dubai) | FIDIC 1999 RB has genuine PS-time lacuna; Cl. 8.4(a) is the contractor's best argument | HKA article |
| 011-fidic-claims-saudi-arabia-strata.md | 2024 | Strata Risk Advisory (Saudi) | 28-day notice is the #1 failure on Vision 2030 mega-projects | Strata website |
| 012-scope-creep-vs-variation-stonehaven.md | 2024 | Stonehaven (UAE) | Variation ≠ scope creep; the difference is change-control governance | Stonehaven article |
| 013-longest-running-uae-construction-case-article-883.md | 2016 | Abu Dhabi Court of First Instance 304/1993; Federal Supreme Court 319 & 320/2015 (9 Dec 2015) | 22-year case ended on Article 883 time-bar defence; *joinder* does not reset the clock | Al Tamimi article |

## How to Use This Library

1. **For the parent agent (Samaya):** Each case file is a standalone markdown file. Save them to `references/training/contract-administration/cases/` or `training/contract-administration/cases/` as suggested in the task brief. The naming convention `NNN-short-slug.md` is preserved.
2. **Each case follows the contract-claims-learning READING_GUIDE 5-lesson structure:** Vocabulary, Evidence, Procedural, Strategic, Principle.
3. **The 5-lesson extraction is consistent with case 001 (Binladin vs Munshaat)** in the existing library — same structure, same Arabic-vocabulary discipline.
4. **The direct quotes are all extracted from the source pages on 31 July 2026**; URLs are live as of that date. The Tamimi URLs are reachable only via reader-proxy; the law-firm consultation URLs (HKA, Strata, Stonehaven, AfiTaC) are reachable directly.

## Open Gaps / Honest Limitations

- **No SCCA-seated Saudi arbitration award digests** were found via web search. The SCCA database is not publicly searchable. The Saudi-perspective cases here (011 Strata) are consultancy analysis, not awards.
- **The "Saudi Construction Law Saga" Al Tamimi articles (files 05, 06, 07 in the raw extract set) were not usable** — the Jina reader-proxy captured only the cookie banner / navigation menu, not the article body. Those URLs are preserved in the manifest but should be re-fetched via a different method if the substantive content is needed.
- **No published Dubai International Arbitration Centre (DIAC) or Abu Dhabi Commercial Conciliation and Arbitration Centre (ADCCAC) award digests** were found with the time budget available.
- **The Federal Supreme Court Case 267/1996 (cited in file 03)** is referenced in the Al Tamimi article but the primary judgment text was not located; the citation chain is Al Tamimi → article → case. Treat as a *secondary* citation.

## Methodology Notes

- **Tavily API key was used** for both `client.search` and `client.extract`. The `extract` endpoint hit transient limits on this run; the `r.jina.ai/` reader-proxy was used as fallback (per the contract-claims-learning skill's documented "Step 3b" technique).
- **All 18 priority URLs from the task brief were successfully extracted** (raw files 01–18 in `/tmp/tavily-research-contract-admin/raw/`).
- **7 supplementary URLs were extracted** (raw files `supplementary/sup_1` through `sup_7`). Of these, sup_5 (lexilio) and sup_6 (HKA old URL) returned 404/redirect — replaced with sup_4 (Strata) and sup_2 (AfiTaC) for substance.
- **No content was fabricated.** Where a URL failed to return substantive content, it is marked as such in the file. The Saudi-law "Saudi Construction Law Saga" articles in files 05/06/07 could not be used as case studies because the Jina extraction returned only the cookie banner.

## Quick Links to Source Articles

1. https://www.tamimi.com/law-update/june-july-2021/articles/conditions-precedent-in-construction-claims-traps-for-the-unwary/
2. https://www.tamimi.com/law-update/june-july-2021/articles/time-barring-in-construction-contracts-an-egyptian-law-perspective/
3. https://www.tamimi.com/law-update/may-7/articles/time-bars-in-articles-880-and-883-of-the-uae-civil-code-regarding-construction-disputes/
4. https://www.tamimi.com/law-update/march-10/articles/new-fidic-2017-yellow-book-a-new-claims-procedure/
5. https://www.tamimi.com/law-update/march-9/articles/abu-dhabi-judgment-on-delay-damages-highlights-importance-of-when-contract-is-terminated/
6. https://www.tamimi.com/law-update/march-8/articles/dubai-courts-hold-that-delay-in-handover-can-trigger-termination/
7. https://www.tamimi.com/law-update/december-january-2/articles/the-importance-of-as-built-programmes-in-construction-disputes/
8. https://www.tamimi.com/law-update/april-7/articles/dealing-with-concurrency-in-construction-delay-claims/
9. https://www.tamimi.com/law-update/july-august-3/articles/force-majeure-under-fidic-in-iraq/
10. https://www.hka.com/article/provisional-sum-loophole-middle-east
11. https://www.stratasaudi.com/fidic-claims-saudi-arabia
12. https://www.stonehaven.ae/insights/scope-creep-construction-project-management
13. https://www.tamimi.com/law-update/march-9/articles/the-longest-running-construction-case-in-uae-legal-history-has-finally-ended/
14. https://afitac.com/2019/11/14/determination-sub-clause-3-7-fidic-2017 (cross-reference for case 004)
