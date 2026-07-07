# Forwarding CG Review Comments to Design Consultant (NRS)

## When to Use

CG (PMC) has reviewed a drawing submittal from the design consultant (NRS / ZNA / AD Engineering) and returned review comments. Samaya Technical Office needs to forward these comments to the designer with context, priorities, and practical guidance — not as formal rejection, but as collaborative feedback for the next submission round.

## Key Principles

### 1. Tone — Informal / Collaborative for "Review Only"

CG review comments forwarded for **review** (not formal approval/IFC) should use an informal, collaborative tone:

- "Still needs some work" not "substantially non-compliant"
- "What's needed" not "must comply"
- "Let us know timing" not "deadline: X date"
- "If that works?" not "required by"

### 2. Always Draft From Beginning

Write the complete email in one pass. Do not send patch-style updates or incremental revisions. The user reviews the full text, not a diff.

### 3. Structure Comments by CG Reference, With Actionable "What's Needed"

Each comment area gets:
- CG reference number (e.g., CG #3c)
- What CG said (1-2 bullet points)
- **What's needed:** The specific action NRS should take

### 4. Prioritise With a Table

| Priority | Item | Who |
|----------|------|-----|
| P0 | Blocker — must fix before next review | NRS |
| P1 | Important — address in this round | NRS |
| P2 | Administrative — Samaya can handle | Samaya PM |

P0 items are "blockers for further review" — CG will not proceed without them.

### 5. Anticipate Design Consultant Pushback

When CG comments assume coordination data the designer hasn't received (e.g., MEP ceiling items for RCPs), acknowledge the gap and suggest a practical fallback — don't just pass through the demand. Example: *"We know you haven't received the full MEP coordination inputs yet — use the already-approved tender/Stage 3 drawings as a reference base for the coordinated MEP elements in the meantime."*

### 6. Pre-empt "Already Submitted" Pushback When Forwarding PMC Requests

When forwarding a PMC request for NEW deliverables (e.g., Maged's scenography drawings request):
- The consultant may resist by saying "we already submitted this."
- Pre-empt this by asking them to identify gaps: *"review the scope and let us know if there are items that need to be prepared that we haven't already submitted in previous DD packages"*
- This phrasing is collaborative (not accusatory) and leaves room for them to confirm what's already done.

### 7. Flag Samaya-In-House Items Clearly

When a CG request includes deliverables Samaya will produce internally (e.g., materials selection presentation for 3D views), state clearly in the email: *"We'll handle this from Samaya's office; no action needed from your team; we will send for your review only."* This prevents the consultant from pricing or duplicating work.

### 8. Split Unrelated CG Communications Into Separate Emails

When CG sends multiple types of communication — e.g., (a) review comments on a submittal and (b) a separate request for new deliverables — send them as **distinct emails** to the same consultant. Do not bundle them.

**Email 1** = Review comments on the submittal (the main review cycle).
**Email 2** = Forwarded PMC request with its own context.

### 9. CC Convention for Forwarded Requests

When forwarding a PMC email to the consultant:
- CC the original sender (e.g., Maged Zamzam) so they're in the loop
- CC Samaya PM + Technical Office internally
- Subject prefix: "FW:" with the original subject preserved

### 6. Emphasise ISO Naming Convention Prominently

The ISO-compliant drawing numbering (per DMP / BEP) must be called out as a separate section, not buried in a generic "title block" item. CG has already shared the coding structure — reference that.

## Email Structure

```
Subject: CG Review Comments — [Package Type] / Aseer Regional Museum
Ref: [Document reference number]

Hi [Name],

Thanks for the [package] submission. We've shared it with CG (PMC) for
review and just received their feedback.

Overall the package still needs some work before we can move forward.
CG raised [N] main areas that need attention. I've summarised the key
ones below, and a detailed checklist is attached.

---

### 1. [Topic] — [Short label] (CG #[N])
- [CG comment summary, bullet points]
- **What's needed:** [Specific action]

... (repeat for all topics)

---

### Priority Summary

| Priority | Item | Who |
|----------|------|-----|
| P0 | [Blocker item] | [Party] |
| P1 | [Important item] | [Party] |
| P2 | [Admin item] | Samaya PM |

---

Let us know if you want to set up a quick call to go through any of
these. Also let us know what timing looks like for a revised package
— aim for [X weeks] if that works?

Regards,

[Sender Name]
[Role]
Samaya Investment
```

---

## Email Template 2 — Forwarding a PMC Request for New Deliverables

Use when the PMC (CG) sends a separate request that is NOT review comments on a recent submittal — e.g., requesting a new package (scenography drawings) or new deliverables.

```
Subject: FW: [Original Subject]
CC: [Original PMC Sender], Samaya PM, Tech Office

Dear Mr. Jim,

Hope you're doing well.

Please find below a request from [PMC contact] at CG (PMC) regarding
[summary of what the request covers].

Could you please review the scope and let us know if there are items
that need to be prepared that we haven't already submitted in previous
[package type] packages? We'd appreciate your advice on this so we can
plan accordingly.

We appreciate your help on this.

Regards,

[Sender Name]
[Role]
Samaya Investment
```

### Standard Variations for Second Email

| Element | Pattern |
|---------|---------|
| CC | Original PMC sender + Samaya PM + Tech Office |
| Tone | Collaborative, consultative — asking for their advice/gap analysis |
| Pre-emptive phrasing | "let us know if there are items that need to be prepared that we haven't already submitted" — leaves room for "already done" without sounding demanding |
| Forwarding note | "Please find below a request from [name] at CG regarding..." |

---

## Pitfalls

| Topic | CG Ref | Typical Issues |
|-------|--------|---------------|
| Building Sections | CG #4 | Missing or outdated sections; minimum 4 sections required |
| Internal Elevations | CG #3a | Missing hatch patterns, finish legends, type marks, dimensions |
| RCPs | CG #3c | Too much background clutter — strip to ceiling + MEP only |
| Floor Finish Plans | CG #3b | Floor/construction joints not needed at DD stage |
| 3D Views | CG #5 | Figures must be in Saudi national dress (Thobe/Abaya only) |
| Drawing Numbering / ISO | CG #2 | Must follow ISO coding from DMP/BEP |
| Title Block | CG #1 | Use Samaya-approved template; complete reference log |
| Missing / Unstamped | CG #6 | Drawing register mismatch; missing sheets; unstamped sets |

## Pitfalls

- **Don't write formally** — user corrected: "remove formal because it's not formal, we submit for review only"
- **Don't use patch/update format** — user corrected: "always draft from beginning" — always write the complete email in one go
- **Don't bury ISO naming in title block** — it deserves its own section with emphasis
- **Don't set arbitrary deadlines** — use collaborative timing questions ("3 weeks if that works?")
- **Don't skip attachments** — reference the detailed checklist and summary report
- **Don't make Samaya's internal items sound like NRS's problem** — split responsibility in priority table + closing
- **Don't ignore designer's side of the story** — if CG demands data the designer doesn't have, acknowledge it and propose a pragmatic workaround
