# NRS Email Drafting — Forwarding CG Review Comments

When forwarding CG/PMC review comments to NRS (Nissen Richards Studio) via email, follow this pattern.

## Tone & Style
- **Informal & collaborative** — "Hi Jim", "Thanks", "let us know if you want a call", "we know you haven't had X input yet"
- **No formal/approval language** — this is a design team coordination, not a contractual submission
- **Address NRS by name** — Jim directly, not "Dear Sir" or "Dear Consultant"
- **Always re-draft the full email from the beginning** when asked for changes — do not patch snippets piecemeal

## Email Structure

```
Ref: [project document reference like MOC-MUS-ASE-1A0-ZD-0063]

Hi Jim,

Thanks for the [Package Name] submission. We've shared it with CG (PMC) for review
and just received their feedback.

[Context paragraph — what's attached, what's forwarded, any coordinating note]

Overall the package still needs some work before we can move forward. CG raised
[N] main areas that need attention. I've summarised the key ones below, and a
detailed checklist is attached.

---

### 1. [Topic] (CG #[N])
- [Bullet 1: what CG said]
- [Bullet 2: what's needed / action required]
- **What's needed:** [clear directive]

### 2. [Topic] (CG #[N])
...

---

### Priority Summary

| Priority | Item | Who |
|----------|------|-----|
| P0 | [blocker] | NRS |
| P0 | [blocker] | NRS |
| P1 | [important but not blocking] | NRS/Samaya |
| P2 | [minor / admin] | Samaya |

---

[Closing note — timing, offer of call, which items Samaya handles in-house]

Best,

[Sender Name]
[Title] — [Project Name]
[Company]

---

**Attached:**
1. [Checklist file]
2. [Report file]
3. [Source email — description of what it actually is, not assumed]
```

## CC Line
- **Always CC**: Maged Zamzam (mzamzam@cg.com.sa), Hossam Mabrouk (hmabrouk@cg.com.sa), Sultan Issa
- Format: `Cc: Sultan Issa, Mohamed Sultan, Maged Zamzam <mzamzam@cg.com.sa>, Hossam Mabrouk <hmabrouk@cg.com.sa>`

## Common CG Comment Areas (DD Architecture Review)

CG comments on DD architectural drawings typically fall into these buckets:

| Area | Title | Typical Content |
|------|-------|----------------|
| #1 | Title Block Compliance | Template compliance, reference logs incomplete |
| #2 | Drawing Numbering/ISO | Numbers not following DMP/BEP coding convention |
| #3a | Internal Elevations | Missing hatches, legends, dimension strings, fixtures |
| #3b | Floor Finish Plans | Remove construction joints (IFC detail), simplify hatches |
| #3c | Reflected Ceiling Plans | Strip background clutter (furniture, wall labels), show only ceiling + coordinated MEP |
| #4 | Building Sections | Missing or outdated — CG expects 4+ sections minimum |
| #5 | 3D Views | Materials selection presentation, dress code for figures |
| #6 | Missing/Unstamped | Drawings not delivered, unstamped sheets, register mismatch |

## Pre-empting NRS Pushback

- **MEP not available for RCPs**: Explicitly acknowledge NRS hasn't received MEP coordination inputs. Suggest using approved tender/Stage 3 drawings as reference base in the meantime.
- **Unfinished renders for 3D views**: Label dress code concerns as "not a major concern at this stage" — will be addressed during final visualisation.

## Materials Selection Presentation

When CG requests a materials selection presentation within 3D views, Samaya handles this in-house. Explicitly tell NRS: *"We'll handle this from Samaya's office, no action needed from your team."*

## Attachment Descriptions

Always verify what an attachment actually contains before describing it. Example: Maged Zamzam's email with subject "Submission of Comprehensive Scenography Drawings Package" is a submission request, not CG review comments. Label attachments accurately.

## Verification Checklist

- [ ] Tone is collaborative ("Hi Jim", "Thanks", "let us know"), not formal
- [ ] Each CG comment area has a clear "What's needed" directive
- [ ] Items Samaya handles in-house are explicitly noted
- [ ] NRS pushback is pre-empted (missing MEP, unfinished renders)
- [ ] Attachment descriptions accurately reflect file content
- [ ] CC line includes Maged Zamzam, Hossam Mabrouk, Sultan Issa
- [ ] Full draft shown from beginning when changes requested
