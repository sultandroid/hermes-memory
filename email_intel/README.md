---
name: email-intel
description: Cross-project email intelligence agent — classify senders/contacts, route emails to project repos, analyze behavior & replies, detect gaps, raise issues when a reply is required.
version: 1.0.0
owner_agent: Hermes (digitalhermes)
status: active
source: hermes-memory hub (cross-project, not tied to any single project)
last_updated: 2026-08-12
---

# Email Intel — Cross-Project Email Intelligence Agent

> **نظام وكيل متخصص لفحص الإيميلات على مستوى كل المشاريع** (وليس مشروع واحد).
> يعمل على الهب `hermes-memory` — **خارج المشاريع** — ويصنّف المرسلين، يربط الإيميلات بمشاريعها، يحلل السلوك والردود، ويكشف الأخطاء/السياق، ويرفع Issues عند وجوب الرد.

---

## 1. What this system is

A **cross-project email intelligence layer** that lives in the hub (`hermes-memory`), NOT inside any single project repo. It:

1. **Ingests emails** from the user's mailbox(es).
2. **Classifies senders/contacts** → `contacts.json` (role, project, trust level).
3. **Classifies emails & routes them to project repos** → `projects.json` (which repo owns this email, if any).
4. **Analyzes sender behavior** → `behavior/sender_profiles.json` (response speed, attachment habits, patterns).
5. **Analyzes replies / threads** → `threads/` (is this email answered? is it stale?).
6. **Detects gaps / errors / context** → contradictions, missing info, pending asks.
7. **Raises Issues when a reply is required** → `issues/ISSUE-NNN.md`.

**File-only rule:** everything is **Markdown (`.md`) or JSON (`.json`)**. **No binaries** (no Excel, no PDF, no images). This is a coordination/intelligence system, not a document archive.

---

## 2. Directory layout

```
hermes-memory/
└── email_intel/
    ├── README.md                  # this file
    ├── contacts.json              # sender/contact classification (role, project, trust)
    ├── projects.json              # project routing map (email → repo)
    ├── inbox/                     # one .md per ingested email
    │   └── YYYY-MM-DD-<sender>-<subject>.md
    ├── behavior/
    │   └── sender_profiles.json   # per-sender behavior analysis
    ├── threads/                   # conversation-thread tracking
    │   └── THREAD-<id>.md
    ├── issues/                    # raised issues (reply required / gap / error)
    │   └── ISSUE-NNN.md
    └── archive/                   # processed/closed items (append-only, never delete)
```

---

## 3. Data schemas

### `contacts.json`
```json
{
  "version": 1,
  "contacts": [
    {
      "email": "raoof@samayainvest.com",
      "name": "Raoof",
      "role": "Workshop Supervisor",
      "project": "samaya-factory",
      "trust": "high",
      "reply_speed": "fast",
      "notes": "Sends OT files, PO requests, leave requests"
    }
  ]
}
```

### `projects.json`
```json
{
  "version": 1,
  "projects": [
    {
      "id": "aseer-museum",
      "repo": "sultandroid/aseer-museum-pm",
      "local_path": "~/projects/aseer-museum-pm",
      "email_domains": ["@cg.com.sa", "@nissenrichardsstudio.com"],
      "keywords": ["aseer", "museum", "MOC", "CG", "NRS", "ACE"]
    },
    {
      "id": "samaya-factory",
      "repo": "sultandroid/new-samaya-factory",
      "local_path": "~/projects/new-samaya-factory",
      "email_domains": ["@samayainvest.com"],
      "keywords": ["samaya", "factory", "ورشة", "مصنع"]
    }
  ]
}
```

### `issues/ISSUE-NNN.md`
```markdown
---
issue_number: 001
status: open | in-progress | closed
raised: YYYY-MM-DD
email_ref: inbox/YYYY-MM-DD-<sender>-<subject>.md
project: <project-id or null>
priority: high | medium | low
---
# ISSUE-001 — <short title>

## Why raised
<reason: reply required / gap / contradiction / stale thread>

## Evidence
- Email: <ref>
- Sender: <name>
- Context: <what's missing or what needs a reply>

## Required action
<what must happen: reply to sender, chase, escalate, update register>

## Resolution
<filled when closed>
```

---

## 4. The agent script

`scripts/email_intel_agent.py` — the executable agent. Run modes:

```bash
# Full run: ingest → classify → route → analyze → raise issues
python3 scripts/email_intel_agent.py --run

# Dry-run / plan only (no writes)
python3 scripts/email_intel_agent.py --plan

# Ingest a single email file
python3 scripts/email_intel_agent.py --ingest path/to/email.eml

# Re-analyze behavior only
python3 scripts/email_intel_agent.py --behavior

# List open issues
python3 scripts/email_intel_agent.py --issues
```

**Pipeline stages (each stage is independent; a failure in one does not block the others):**

| Stage | Output | Failure handling |
|-------|--------|------------------|
| 1. Ingest | `inbox/*.md` | log, continue |
| 2. Classify sender | `contacts.json` | log, continue |
| 3. Route to project | `projects.json` match | log, continue |
| 4. Behavior analysis | `behavior/sender_profiles.json` | log, continue |
| 5. Thread/reply analysis | `threads/THREAD-*.md` | log, continue |
| 6. Gap/error detection | `issues/ISSUE-NNN.md` | log, continue |

---

## 5. ⚠️ WHAT THE MAC PRO AGENT MUST DO (read this)

> **This section is the contract for the agent that has access to the user's emails on the Mac Pro.**

The Mac Pro runs **macOS with Outlook + AppleScript** — it is the ONLY machine that can read the user's Microsoft/Outlook mailbox directly (this Linux box cannot, and the mailbox requires MFA/App-Password that only the Mac's interactive Outlook session can satisfy).

**Primary mailbox: `sultan@samayainvest.com`** (Microsoft 365 / Outlook). The Mac Pro agent is the **EMAIL INGESTION FRONT-END** for this mailbox. Its job is to **pull emails out of Outlook and hand them to this hub system as `.eml`/`.md` files** — nothing more. It does NOT own the intelligence layer; this hub does.

### Required responsibilities (in order)

1. **Export new emails from Outlook** (AppleScript → save as `.eml` or extract body+attachments to `.md`).
   - Source mailbox: **`sultan@samayainvest.com`** (Microsoft 365 / Outlook).
   - Use the existing `bim_fetch_emails.applescript` / `bim_download_attachment.applescript` patterns as a starting point.
   - Export to a staging dir, e.g. `~/email_intel_staging/`.

2. **Push the exported emails into this hub** so the intelligence agent can process them:
   - Copy `.eml`/`.md` files into `email_intel/inbox/` (or a `staging/` subfolder the agent watches).
   - OR commit them to the `hermes-memory` repo under `email_intel/inbox/`.

3. **Do NOT duplicate the intelligence work.** The Mac agent:
   - ❌ Does NOT classify senders (that's `contacts.json` here).
   - ❌ Does NOT route to project repos (that's `projects.json` here).
   - ❌ Does NOT analyze behavior / replies / gaps (that's this hub).
   - ❌ Does NOT raise issues (that's this hub).
   - ✅ ONLY exports emails and delivers them to the hub.

4. **Keep the export clean:**
   - Strip nothing — keep full body + all attachments (attachments may be referenced by path, not stored as binaries in the repo).
   - Name files: `YYYY-MM-DD-<sender>-<subject>.eml` (or `.md`).
   - Never delete an email from Outlook after export — the hub is a mirror, not the source of truth.

5. **Notify the hub agent** when new emails are staged (e.g. `hermes_notify.sh telegram "New emails staged for email_intel"`), so the intelligence agent runs its pipeline.

### Why this split
- **Mac Pro** = the only mailbox reader (Outlook + MFA + AppleScript). It is the **sensor**.
- **Hub (this repo)** = the cross-project brain. It is the **analyst**.
- Keeping the analyst on the hub means **every project and every agent** benefits from the same intelligence, and the system is **not tied to one machine or one project**.

---

## 6. Raising issues (reply-required detection)

The agent raises an `issues/ISSUE-NNN.md` when ANY of these is true:

- **Reply required** — an email asks a question or requests action and has no reply in the thread.
- **Stale thread** — a thread has been open > N days with no response.
- **Gap / missing info** — an email references an attachment, decision, or document that isn't present.
- **Contradiction** — an email conflicts with a prior decision/register entry.
- **Escalation needed** — a high-priority sender (client, consultant, finance) is waiting.

Each issue is a standalone `.md` file (append-only). Closing = update `status: closed` + fill `Resolution` — never delete.

---

## 7. Anti-patterns

- ❌ **No binaries** in this folder — attachments are referenced by path, not stored.
- ❌ **No Excel registers** — this is MD/JSON only.
- ❌ **No project-specific content** — project deliverables go to project repos; this hub only holds cross-project intelligence + routing.
- ❌ **No `rm -rf`** — archive, never delete.
- ❌ **Mac agent must not duplicate the analysis** — it only ingests.

---

## 8. Related

- `samaya-email` skill — Gmail-based monitor (Raoof OT/PO/leave) — legacy, single-project.
- `bim_email_pipeline.py` — macOS Outlook pipeline — legacy, single-project, Excel-based.
- `multi-agent-hub-ops` — hub operational patterns.
- `discussion-then-decision-protocol` — governance for system-level changes.

*Last updated: 2026-08-12*
