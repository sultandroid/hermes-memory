# CG Warning Letters (إنذار) — Delay Rebuttal Workflow

Class-level procedure for responding to a formal CG/PMC warning letter (e.g. Aseer
Museum MOC-MUS-ASE-LT-08.02, 02-Sep-2026, 15-day corrective-action ultimatum, signed
Acting CG PM Eng. Mansour Alrezeni). Distinct from a Code C submittal response: this is
a **contractual-position letter**, not a technical comment reply.

## Workflow

1. **Extract the PDF text first** (pypdf handles the bilingual CG layout; the Arabic
   pages extract garbled/reversed — read the reversed-letterform page carefully, it
   holds the detailed deficiency list and enclosure list).
2. **Extract every claim** with its number (progress %, days elapsed, per-discipline
   design %, itemized deficiencies) into a table.
3. **Cross-check each claim against the repo registers BEFORE drafting** — the reply is
   built from evidence, not argument (renumber: cross-check is step 3, Aconex
   verification is step 4, impact table 5, reply draft 6):
   - `submission.db` (latest-rev-wins codes — never stale files; see AGENTS Rule 10a)
   - SI register (CG's own Site Instructions that gated our work, e.g. SI-007 3D
     sequence, SI-010 cloud survey)
   - Letters register (prior warnings LT-003, EOT LT-0027/0028)
   - Weekly report board (contemporaneous S-curve, P6 float, "site not vacated" weeks)
   - Risk register (PRR-SIT-01/02 latent conditions, PRR-PRC-04 specialists, PRR-SCH-04)
   - Action items (M14-* delays with owners and dates)
4. **VERIFY EVERY CITED DOC against a fresh Aconex export before finalizing** — the
   user will typically supply `ExportDocs-YYYYMMDD.xlsx` for exactly this purpose:
   drop it in `08_Document_Index/aconex_snapshots/`, run
   `python3 scripts/build_submission_db.py` + `update_dashboard.py`, re-query each
   doc cited in the rebuttal (latest-rev-wins), and correct any stale codes. This
   session it caught: 3D Lidar Cloud Survey U→**B** (our deliverable completed —
   ball moved to CG's court), Evergreen PQ-0122 C→**B** (removed from "stuck
   specialists" list), ZD-0116 core test → C (latent-condition evidence
   strengthened). A rebuttal citing a stale code gets destroyed in one CG
   counter-check; re-verify at send time, not draft time. Then re-commit.
5. **Build a delay-impact table** in the repo (`03_Plans/08_Risk/`):
   3 parts — (a) claim-by-claim rebuttal with doc refs, (b) chronological timeline of
   delay drivers each tagged with the responsible party (CG / Employer / Samaya /
   CG-gated input), (c) quantified EOT/VO exposure. Commit it.
   Example: `03_Plans/08_Risk/2026-09-09_delay-impact-table_LT-08.02.md`.
6. **Draft the formal reply** (Aconex formal-letter English, addressed to the signatory):
   - Acknowledge receipt + state the response deadline explicitly (due date arithmetic).
   - Factual chronological narrative — dates + Aconex refs speak; no argumentative tone.
     For the *strongest* arguments (CG self-contradictions like SI-007), expand into
     numbered sub-paragraphs (2.2.1–2.2.4) each carrying its own doc refs — one dense
     paragraph buries the chain; four short ones let each fact land.
   - Reserved-rights statement referencing the open EOT file (LT-0027) and
     out-of-contract cost exposure — do not concede the delay attribution.
   - Include the corrective action plan we ARE executing (pressure meeting, gate dates,
     C/D resubmission plan, specialist appointments) — the plan is unavoidable; the
     attribution is negotiable.
   - Doc-control block per project standard (Prepared=TO Sultan, Reviewed=Samir,
     Quality=Aftab, Approved=PM Waris, DC=Hesham).
   - User reviews before anything is sent; leave money figures blank pending user input.
7. **Publish the in-progress draft to a live Surge page for team review** (user request:
   "اعمل ملف علي surge … نتابع مع الفريق"). Build the repo markdown into a single HTML
   page (`<meta http-equiv="refresh" content="60">`), `surge --domain <topic>.surge.sh
   /tmp/<dir>/`, then set up a 30-min cron that rebuilds HTML from the repo file and
   republishes, so every draft edit reaches the team automatically. Keep a "LIVE
   DRAFT — updated <timestamp>" badge on the page. Only for internal-review drafts —
   never for anything CG-facing/final. **Cron must read from repo files** (store the
   Arabic reply as `<date>_reply-draft_<ref>_AR.md` in the repo and have the cron
   script open it from there — not from /tmp, which doesn't survive); page is RTL
   Arabic when the reply language is Arabic, with page order: Arabic reply text →
   annex table → English internal reference appendix.

## Recurring rebuttal evidence patterns (Aseer)

> Note: always re-verify these against the newest DB snapshot — codes move. As of
> the 09-Sep export: cloud survey = B (approved), Evergreen PQ-0122 = B (approved),
> DB totals 250 B / 102 C / 55 D / 115 U across 826 rows.

- **CG self-blocking chain**: CG's own reviewer comments create CG-gated inputs —
  e.g. ZD-0114 ETABS Code C comments (27-Aug) explicitly say the model "must be
  confirmed after the approval of cloud survey" — while the cloud survey itself sits
  Code U with CG. Chain: CG gate → our deliverable gated → same period cited as our
  delay.
- **Latent/owner conditions**: as-built documents never delivered; failed concrete
  core test (20.7 vs 35 MPa = 59%) = Employer-risk per ER Art. 14; building licence +
  Civil Defence prior approval = OWNER (MoC) obligation (documented decision AD30-14).
- **Approval-clock evidence**: SOW/design contracts approved late (ZD-0068 MEP SOW
  Code B 11-Jul, agreement signed 15-Jul) — the specialist's 45-day design clock starts
  inside the "delay" window CG cites.
- **Employer occupancy**: weekly reports WR-01→11 all record "site not vacated" —
  employer-side delay with contemporaneous record; plus out-of-contract relocation
  lease Samaya funded to vacate the building for MoC (VO/EOT claim). Lease value
  stays blank pending user input ("per separate correspondence" fallback wording).
- **CG rejection-driven gaps**: specialists rejected/delayed by the CG PQ cycle
  (Evergreen C, SOROOH D, BTT/Saudi Emaar D); AV DD 1G-0002 Code D. DB snapshot
  (09-Sep): 228 B vs 89 C + 55 D — most "unresolved" items sit in CG's review cycle.
- **3D sequence reversal — the strongest single rebuttal argument; document it in full.**
  Don't settle for "Samaya offered 3D early, CG declined." The 09-Sep session built a
  four-part chain that turns SI-007 (19-Apr) from a neutral instruction into
  CG-documented self-contradiction: (1) approved DMP RACI row 25 already made Samaya
  Responsible for "3D Renders + Material Boards"; (2) the 3D-first requirement
  *originated in CG's own DMP comment C-3a* (DMP Rev.01 Code C, 13-May: "Pre-Design
  stage requires 3D render shots…") — CG demanded 3D, then "upheld" an SI treating the
  same demand as a compliance violation; (3) Samaya committed real budget pre-SI
  (ZD-0031, 27 visuals × SAR 8,750 = SAR 236,250, Code B) and delivered the render
  sample (ZD-0033) within days of C-3a (17–19-May, Code B 06-Jun); (4) SI-007's effect
  was to **convert a planned parallel-track process into a serial gate**, freezing
  Architectural DD 19-Apr→06-Jun behind a cycle CG itself requested. In the reply
  letter, state this as "a gate the Engineer itself imposed on a process it had itself
  requested" — factual phrasing, let the reader draw the conclusion.

## Anticipate CG counter-arguments (user-confirmed requirement)

Before finalizing any rebuttal, play CG's lawyer against each claim and pre-empt the
obvious comeback — the user explicitly probes this ("يمكن يقولك ما انت الي قدمت متأخر").

Technique: add an "Anticipated CG counter-argument — pre-empted" subsection under the
relevant claim, with a mini-table of the full chronology behind the disputed item,
each row carrying its own doc ref + which party consumed the time. Session example
(cloud survey "you submitted it late yourself"): architectural LiDAR scan started
05-Aug with no approval gate (SNA notification suffices — Daily Report 05-Aug shows
it in progress); the *structural* phase (breaking cladding) was legally gated by
dismantling approval ZD-0106 (submitted 10-Aug, Code B 25-Aug); the May–Aug gap was
consumed by CG's own PQ rejections (5 survey offices cycled Feb–Mar, one Code D),
CG's own failed subcontractor (documented in SI-010's text), and MS-0016 method
approval (24-Jun). Rule: every date we cite must survive the question "when exactly
did you submit it, and why couldn't it be earlier?" — pin submission dates from the
Aconex raw export (transmittal timestamp) AND the outgoing file timestamps in Adel's
bank before claiming "earliest possible".

## Pitfalls

- **Do not treat the warning as "our fault confirmed".** Every claim has documented
  prior correspondence; map before conceding anything. The user's framing: CG
  pressured late after stopping the design phase itself over a CG-imposed sequence.
- **Do not miss the reply deadline** (typically 14–15 days). Diary the due date
  immediately from letter date + ultimatum period.
- **Multi-phase activities need per-phase gate logic.** One activity can have a
  no-gate phase (architectural scan — SNA notification suffices) and a gated phase
  (structural scan behind dismantling approval ZD-0106). Present the two-phase
  sequence explicitly; a single-date rebuttal collapses when CG points out the gated
  part started later. Sanity-check your own timeline's internal logic before
  delivering — the user caught a contradiction (dismantling approval dated *after*
  the scan start); the answer was phases, not an error.
- **Keep Code B = closed** (AGENTS Rule 10) — an old Code C/D cleared by a later
  revision is NOT a live deficiency in the rebuttal; query the DB at run time.
- **No internal rationale/commentary in CG-facing annexes** — factual refs only
  (same rule as risk closure evidence).
- **User's negotiation stance**: present the problem and the documented record; do NOT
  propose costly solutions — let the other party request them so cost lands on their
  design decisions, not Samaya's.
- **User probes with short challenges, expects evidence-backed answers** — e.g.
  "امتي أصلا قدمته؟" (when did we actually submit it?). Treat every challenge as a
  signal to pull the raw Aconex row + outgoing file timestamps and pin the exact
  date, not defend with narrative. Also: the user connects threads mid-task ("اربطلي
  الدنيا ببعضها") — respond by linking registers/discussions/DB evidence into one
  connected picture, and record the resulting chronology in the repo, not just in chat.
- **Reply language = the letter's language (user correction 2026-09-09).** The old rule
  "English-only formal letters" was WRONG for warning letters: the CG letter arrives in
  Arabic, so the reply goes in **Arabic**, saved as a separate
  `<date>_reply-draft_<ref>_AR.md` (keep the English draft only as internal reference).
  Live-page order: Arabic text first, annex table, English appendix last.
- **Humanize the Arabic reply — no AI fingerprints (user correction 2026-09-09).** Rewrite
  any generated draft before it ships: no numbered AI sub-headings (2.2.1/2.2.2) — use
  أولاً/ثانياً/ثالثاً like Samaya's own letters; no bold-embedded rhetoric inside
  sentences; no AI transition markers ("وهنا ملاحظة جوهرية:", "Net:", "نشهد بأننا");
  break long compound academic sentences into short engineer sentences; keep the strongest
  argument phrased plainly, e.g. "الفترة… استُهلكت في دورة اعتمادات مفروضة بالتوازي مع
  تنفيذ المقاول لنفس المسار المطلوب" — same meaning, no edge. Structure: مراسل → إشارة
  للخطاب + الالتزام بالمهلة → الوقائع → خطة تصحيحية بسيطة (مسؤول/موعد) → حفظ الحقوق →
  التوقيع + السيطرة الوثائقية. Every doc ref and figure survives the rewrite — only the
  phrasing changes.
- **Connect the warning to the running delay analysis** — link the impact table to
  existing discussions (`2026-08-31_ad-delay-impact-analysis.md`), registers, and the
  EOT file so the rebuttal inherits all prior evidence, per AGENTS Rule 12
  (cross-link everything).