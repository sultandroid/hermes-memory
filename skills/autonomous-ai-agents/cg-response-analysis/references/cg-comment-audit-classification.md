# CG Comment Audit & Classification (don't blindly "Comply")

When CG returns a submittal Code C, the correct response is **NOT** to mark every comment "Complied." Audit each comment against the governing docs and classify it. This is a recurring user expectation — the user explicitly asked "why do you comply with every comment? audit each one."

## The governing clauses (Aseer Museum)

| Clause | What it says | Use it to push back on |
|---|---|---|
| **ER §2.4** (Approval Framework) | PMC review is **conformance-only**, NOT technical review; design liability stays with Contractor even after "approval" | CG demanding technical design work (specialist reviews, test reports, mock-ups) as a condition of spec approval |
| **SoW §6.11** | Product data / test reports / certs are **IFC-package submittals**, "shall not be submitted independently" | CG demanding test reports/certs/warranties at the spec stage |
| **SoW §13.12** + ER §2.4.F | Mock-ups per the **Mockups Schedule**, construction phase | CG demanding mock-ups at the spec stage |
| **ZD-0026** (NRS Methodology, Code B) | NRS owns architectural design/specs; acoustic specialist provides *input to Samaya*, not a reviewer; review chain = Supplier/TO → Samaya → NRS → CG/MoC | CG demanding "acoustic specialist must review the architectural specs" — contradicts CG's own approved methodology |

## Classification taxonomy

| Verdict | Meaning | When |
|---|---|---|
| ✅ **Comply** | Legitimate, embed into spec | Technical criteria (NRC, DCOF, fire rating, compressive strength) traceable to ER/SoW |
| 🔴 **Not applicable / wrong stage** | Push back with clause citation | Evidence deliverables (test reports, certs, mock-ups) demanded at spec stage; specialist review that contradicts ZD-0026 |
| 📍 **Wrong place** | Valid requirement, wrong section — move it, don't add it to the execution section | 360° photo/video documentation demanded in 01 73 29 (Cutting & Patching) — belongs in Division 01 (01 32 00 Construction Progress Documentation) or the ITP, not the execution section. Reply: "requirement accepted, will be located in Division 01 / ITP, not this section" |
| ⚪ **Noted** | Boilerplate, no action | "approval does not relieve responsibility", "no variation to price/schedule" |
| 🟠 **Open / clarify** | Downstream symptom, needs a decision | "display cases suspended" when the real issue is the showcase *design* (1G-0009) being Code C |

## Pitfalls (learned 2026-08-29, 1G-0012)

1. **CG often requests things ALREADY in the spec.** Before writing "Complied, we'll add it," READ the actual NRS spec section. Example: CG's "Cutting & Patching" comments (no holes >10mm, no rebar cutting, no chasing hollow block, 0.125 joist notch) were ALL already in NRS spec §3.02/3.05/3.07 verbatim. Only the 360° photo documentation was genuinely new. Reply: "already specified at §X — no revision required" not "we'll add it."

2. **CG references a CRS sheet it never attached.** The DS cover page says "See attached CRS Sheet" but the email carries only the PDF + a signature image. The comments are written as plain text inside the PDF. Verify the actual attachments (Outlook `count of (every attachment of m)`) before hunting for a missing .xlsx. Respond using Samaya's own CRS template.

3. **Specialist-review demands can be self-contradictory.** CG demanded the acoustic specialist's sign-off (G2) while that specialist (TransOrient PQ-0128) was still Code U pending CG's own review — AND ZD-0026 says the acoustic specialist is an input-provider, not a reviewer. Two independent grounds to push back.

4. **Oddy test is scope-limited, not universal.** Oddy applies only to materials inside/near display voids (in contact with artifacts), not all materials. ER §6.11 ("non-deleterious to museum-grade objects") is the governing principle. SoW §8.1 "all materials" is overly broad — read in context.

5. **Verify register codes before citing them in a CG-facing doc.** The specialist register listed TransOrient as both "Appointed 🟢" (Tier 2) and "Prequalify 🟡" (Tier 3). A CRS reply that said "Code B, appointed" was factually wrong — it was Code U, pending. Cross-check any rated/status register against the source before writing it into a CG-facing document.

6. **The CRS "Sheet" column = the CG's own page number, not our sheet number.** The "Sheet" column must map to the page in CG's response document where that comment appears — NOT a generic "1"/"2", and NOT our workbook's sheet. CG responses are often a multi-page PDF with one section per page. Extract the page-per-section map (`pdftotext` + split on `\f`, then find which page each section code appears on) and set each row's Sheet to the correct page so the reviewer can trace back. Example (1G-0012): G1–G10 → page 1; S1 (01 73 29) → page 3; S2 (03 54 00) → page 4; … S21 (09 12 00) → page 23.

## Workflow

1. Extract the full CG response (pdftotext -layout, all pages).
2. For each comment, identify its type: design / spec / evidence / boilerplate / downstream-symptom.
3. Map to the governing clause (table above).
4. Classify (Comply / Not-applicable / Wrong-place / Noted / Open) with a clause citation.
5. For "Comply" items, READ the actual NRS spec section first — if already present, reply "already specified at §X."
6. Build the CRS with the classification, not blanket "Complied."

## Clause-mapping technique (prove "already written" at scale)

When CG returns a *specifications* submittal Code C with many section comments, don't hand-check each one — extract every NRS spec `.docx` to text and grep each CG-requested term to its clause number. This produces a defensible "X% already written" finding.

```python
import docx, glob, os, re
base = "<OneDrive>/.../DD Specification MasterFormat"
outdir = "/tmp/specs_text"; os.makedirs(outdir, exist_ok=True)
for f in glob.glob(base + "/**/*.docx", recursive=True):
    if "Conversion Register" in f: continue
    d = docx.Document(f)
    text = "\n".join(p.text for p in d.paragraphs if p.text.strip())
    open(os.path.join(outdir, os.path.basename(f).replace(".docx",".txt")), "w").write(text)

# then per section, find which clause each CG term appears in:
def find_clauses(text, terms):
    res, cur = {}, ""
    for line in text.splitlines():
        m = re.match(r'^(\d\.\d\d)\s', line.strip())
        if m: cur = m.group(1)
        for t in terms:
            if t.lower() in line.lower(): res.setdefault(t, set()).add(cur)
    return res
```

Pitfalls:
- OneDrive `.docx` files are often EDEADLK-locked (cloud placeholder). `open` the file in Finder first, wait ~6s for hydration, then `docx.Document()` works. Some files fail with "Package not found" — that's the lock, not a missing file; retry after `open`.
- The result is usually ~90% "already written" — the genuinely-missing items are single values/dimensions (e.g. "50×50 mm mesh", "single batch", "guillotine", "split-batten", "tight-butted", "fire-door ratings", "30×200 mm baffle"). This is the strongest possible CRS position: cite the exact clause for every "exists" item and list only the handful of real additions.
- Deliver this as a clause-mapping discussion file (one table per section: CG demand → status → NRS clause), plus a roll-up of "genuinely missing" vs "wrong place/stage".
