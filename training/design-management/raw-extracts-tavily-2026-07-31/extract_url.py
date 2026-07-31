#!/usr/bin/env python3
"""Extract raw content from a curated list of candidate URLs via Tavily extract."""
import json, os
from pathlib import Path
from tavily import TavilyClient

RAW = Path("/tmp/tavily-research-design-mgmt/raw")
api_key = os.environ["TAVILY_API_KEY"]
c = TavilyClient(api_key=api_key)

# Curated extraction list — theme -> URL slug
urls = {
    "meed-riba-saudi": "https://www.meed.com/market-talk-riba-helps-shape-saudi",
    "linkedin-riba-saudi": "https://www.linkedin.com/posts/meed_riba-helps-to-shape-saudi-with-new-working-plan_ugcPost-7412230026686423040-m5wg",
    "mdpi-bim-saudi-2023": "https://www.mdpi.com/2071-1050/15/7/6130",
    "ksu-design-and-build": "https://cap.ksu.edu.sa/sites/cap.ksu.edu.sa/files/imce/adoption_of_design_and_build.pdf",
    "riba-plan-of-work": "https://www.riba.org/work/insights-and-resources/riba-plan-of-work",
    "thenbs-riba": "https://www.thenbs.com/knowledge/riba-plan-of-work",
    "designing-buildings-riba": "https://www.designingbuildings.co.uk/wiki/RIBA_plan_of_work",
    "aceris-fidic-design-risk": "https://internationalconstructionknowledgehub.com/design-risk-fidic/",
    "aceris-fidic-risk": "https://www.acerislaw.com/understanding-risk-allocation-in-fidic-construction-contracts/",
    "hka-saudi-risks": "https://www.hka.com/article/managing-risks-and-claims-in-saudi-arabia",
    "chambers-saudi-construction-2026": "https://practiceguides.chambers.com/practice-guides/construction-law-2026/saudi-arabia",
    "kfupm-change-orders": "https://faculty.kfupm.edu.sa/CEM/assaf/Students_Reports_Reports/D.Change%20Orders%20in%20Construction%20Projects%20in%20Saudi%20Arabia.pdf",
    "mdpi-vo-model": "https://www.mdpi.com/2075-5309/14/3/726",
    "archdesk-fidic-vo-gcc": "https://archdesk.com/blog/2026-construction-fidic-variation-orders-in-the-gcc",
    "ghazzawi-fidic": "https://www.ghazzawilawfirm.com/insights/understanding-fidic-contracts-a-legal-perspective-for-saudi-clients",
    "tamimi-professional-indemnity": "https://www.tamimi.com/litigation-dispute-resolution/professional-indemnity-and-fidelity-insurance/",
    "marsh-saudi-pi": "https://www.marsh.com/en/insights/publications/saudi-arabia-construction-power-and-water.html",
    "procore-as-built": "https://www.procore.com/library/as-built-drawings",
    "lorman-as-built": "https://www.lorman.com/resources/use-and-misuse-of-as-built-drawings-record-drawings-and-measured-drawings",
    "mdpi-ve-saudi": "https://www.mdpi.com/2075-5309/14/4/1017",
    "procore-constructability": "https://www.procore.com/library/constructability",
    "ied-asu-saudi-risk-model": "https://asu.elsevierpure.com/en/publications/introducing-a-new-risk-management-model-to-the-saudi-arabian-construction-industry/",
    "construction-institute-constructability": "https://www.construction-institute.org/project-level-model-and-approaches-to-implement-constructability/",
    "pinnacle-constructability": "https://pinnacleinfotech.com/services/constructability-review-services/",
    "mehrbod-bim-coordination": "https://itcon.org/papers/2019_03-ITcon-Mehrbod.pdf",
    "catenda-design-coordination": "https://catenda.com/glossary/design-coordination-in-construction/",
    "openspace-bim-coordination": "https://www.openspace.ai/blog/what-is-bim-coordination-in-construction",
    "autodesk-10-tips": "https://construction.autodesk.com/resources/guides/10-tips-for-running-effective-construction-coordination-meetings",
    "bim-design-saudi": "https://bimdesignllc.com/bim-coordination-services-saudi/",
    "schnackel-multi-discipline": "https://schnackel.com/blogs/overcoming-multi-discipline-design-challenges-with-bim-coordination",
    "imep-mep-revisions": "https://imep-eng.com/blog/avoid-design-revisions-late-mep-coordination",
    "fcl-fidic-adjudication": "https://fcl.fidic.org/adjudication-addressing-disputes-in-engineering-projects/",
    "hka-global-construction": "https://www.hka.com/article/2024-global-construction-disputes-report",
}
