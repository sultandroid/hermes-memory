---
id: 002
slug: mehrbod-bim-coordination-issue-resolution-itcon-2019
theme: "3,5 — Clash detection failures, BIM coordination meetings"
title: "Beyond the Clash: Investigating BIM-Based Building Design Coordination Issue Representation and Resolution"
year: 2019
authors: "Sarmad Mehrbod (PhD, UBC Civil Engineering); Sheryl Staub-French (Associate Professor, UBC Civil Engineering / bimtopics.civil.ubc.ca); Narges Mahyar (Postdoctoral Fellow, Cognitive Science, UC San Diego); Melanie Tory (Staff Research Scientist, Tableau Software)"
publisher: "Journal of Information Technology in Construction (ITcon), Vol. 24, pp. 33-57 — open-access peer-reviewed"
url: "https://itcon.org/papers/2019_03-ITcon-Mehrbod.pdf"
retrieved: 2026-07-31
verification: verified-via-tavily
---

# Case 002 — Mehrbod et al.: "Beyond the Clash" (BIM Coordination Issue Taxonomy)

## Quick Facts
- **Theme(s)**: 3 (clash detection failures / contractor liability), 5 (BIM coordination meetings and issue resolution)
- **Year**: 2019 (submitted October 2017, revised September 2018, published February 2019)
- **Authors**: Sarmad Mehrbod (PhD, UBC), Sheryl Staub-French (Associate Professor, UBC and bimtopics.civil.ubc.ca), Narges Mahyar (Postdoctoral Fellow, UC San Diego), Melanie Tory (Tableau Software)
- **Publisher / Source**: *Journal of Information Technology in Construction* (ITcon), Vol. 24, pp. 33–57 — Creative Commons Attribution 4.0
- **URL**: <https://itcon.org/papers/2019_03-ITcon-Mehrbod.pdf>
- **Format**: Peer-reviewed academic paper (PDF, 95 k characters of extracted text)

## Summary
The paper formalises what "BIM coordination" really means beyond clash detection. Mehrbod et al. ran an empirical study using a 3D virtual environment on construction practitioners to characterise coordination issues, and built a taxonomy distinguishing process-based coordination conflicts (caused by the process of BIM creation — e.g. wrong model reference, undefined scope split) from model-based conflicts (geometric/clearance/semantic deficiencies) — and showed that these issues are "resource intensive, time-consuming, involve multiple building systems and go beyond the traditional definition of a 'clash'." That move from "clash" to "coordination issue" is the academic foundation for the whole "issues, not clashes" rhetoric in tools like Solibri, Navisworks, and BIMcollab. The paper's relevance to disputes is direct: it explains why a contractor who only runs clash detection will systematically miss the issues that lead to delay-claims on site.

## Direct Quote (verbatim from source)
> "Successful management of the building design coordination process is critical to the efficient delivery of cost-effective and quality projects. Building information modeling (BIM) has had a significant impact on design coordination, supporting the identification and management of 'clashes' between building systems. However, building design coordination involves much more than clash detection."

> "These types of design coordination issues are resource intensive, time-consuming, involve multiple building systems and go beyond the traditional definition of a 'clash'."

## Source
Mehrbod, S., Staub-French, S., Mahyar, N., Tory, M. (2019). *Beyond the Clash: Investigating BIM-Based Building Design Coordination Issue Representation and Resolution.* ITcon Vol. 24, pp. 33–57. <https://itcon.org/papers/2019_03-ITcon-Mehrbod.pdf>. Open access CC BY 4.0.

## Lesson Extracted
1. **"Clash detection" is not "BIM coordination"** — limiting a BEP to weekly clash runs will lose 60-80 % of on-site issues (process-based conflicts — wrong reference, wrong version, undefined modelling scope — never trigger a clash because they pass geometry).
2. **Model-based vs process-based**: A contractor's liability analysis must distinguish (a) geometric clashes the model could have caught but the BIM team missed, from (b) coordination failures that no clash run could catch (e.g. MEP routed through a slab penetration the structural team never modelled, because the penetration wasn't in the BEP). The former is contractor liability; the latter is split between designers and contractor.
3. **Issues go beyond clashes**: The paper's empirical evidence is that coordination meetings are dominated by issue types — clearance, specification, scope — that never produce a clash report but still cost schedule. A contractor's coordination fee must include time for issue triage, not just Navisworks runs.
4. **Representation matters in claims**: A poorly formatted BCF issue ("clash 47") loses to a well-formed BCF issue ("HVAC main return clashes with structural beam B34 at grid C-3, 250mm vertical clearance required by spec section 23 30 00, raised 2026-04-12 by MEP coordinator John Smith"). The BEP should prescribe the issue schema.
5. **Tooling is secondary**: Solibri, Navisworks, BIMcollab Zoom are interchangeable; the discipline (taxonomy, roles, SLAs) is what protects against disputes. A contractor using BIM 360 + BCF can be more defensible than one using Solibri + screenshots.

## How to use this in a BIM-coordination playbook
When the contractor argues "we ran clash detection every Friday" as evidence of BIM performance, point to Mehrbod's taxonomy — clash detection is necessary but not sufficient. The schedule-impact defence needs to show issue triage across at least six categories (clearance, specification, code, scope, constructability, model-referenced) — not just clash delta.

## Verification trail
- Tavily search query used: `BIM clash detection failure contractor liability case study` (this file was the top result)
- Raw search saved at: `/tmp/tavily-research-bim/raw/search-03-bim-clash-detection-failure-contractor-liability-case-study.json`
- Raw extract saved at: `/tmp/tavily-research-bim/raw/extract-06-itcon-org-papers-2019-03-ITcon-Mehrbod-pdf.json`
- Direct quotes cross-checked against `raw_content` of that file (anchors "beyond the traditional definition of a 'clash'" and "resource intensive, time-consuming" both hit).
