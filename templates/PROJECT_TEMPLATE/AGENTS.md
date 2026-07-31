# AGENTS.md — Project: <PROJECT_NAME>

> **Read this BEFORE working on this project.** This file is the project-level contract. The hub (`hermes-memory` repo) has the user-level rules — this file is the project-specific layer.

---

## 1. Project Identity

| Field | Value |
|---|---|
| **Name** | <PROJECT_NAME> |
| **Type** | WORK / CONSULTING / PERSONAL |
| **Client** | <CLIENT_NAME> |
| **Doc code prefix** | <e.g. MOC-MUS-ASE> |
| **Odoo project ID** | <if applicable> |
| **Hub entry** | See hub `PROJECTS.md` row for this project |
| **Status** | <Active / On-hold / Closed> |
| **NTP** | <YYYY-MM-DD> |
| **Contract completion** | <YYYY-MM-DD> |

---

## 2. Project-Specific Rules (override hub rules ONLY where noted)

- **<Rule 1>** — context: <why this project is different>
- **<Rule 2>** — context: <why>
- **<Rule 3>** — context: <why>

> If a project rule conflicts with a hub `NEVER Do` rule, the hub wins. Project rules only ADD, never override safety rules.

---

## 3. Key People (project-specific)

| Role | Name | Contact |
|---|---|---|
| Client rep | | |
| Consultant | | |
| Contractor PM | | |
| Site lead | | |
| Document control | | |

For full Samaya team contacts, see hub `CONTACTS.md`.

---

## 4. Project Folder Structure

```
<PROJECT_NAME>/
├── 00_Admin/                  # charter, contracts, doc codes
├── 01_CLIENT_INPUTS/          # client-supplied docs (read-only)
├── 02_Submittals/             # outgoing submittals
├── 03_Design/                 # design files by phase
├── 04_Drawings/               # issued drawings register
├── 05_Specifications/         # specs
├── 06_BIM/                    # BIM models, coordination
├── 07_Meetings/               # minutes, agendas
├── 08_Schedules/              # programs, lookaheads
├── 09_Site/                   # site photos, reports
├── 10_Calculations/           # calcs, reports
├── 11_Standards/              # applicable codes
├── 99_Templates/              # reusable templates
├── AGENTS.md                  # this file
├── PROJECTS.md                # project-level index
├── README.md                  # human-facing overview
└── .gitignore                 # excludes credentials, .DS_Store, etc.
```

---

## 5. Registers (Excel — append only)

Per hub `RULES.md`: **never create new Excel files**. Append rows to existing registers.

| Register | Location | Owner |
|---|---|---|
| Risk register | | |
| LN (lesson learned) | | |
| Submittal log | | |
| Drawing register | | |
| RFI log | | |
| Material approval | | |

Each register has a `_Project_Memory/` README explaining its schema.

---

## 6. Project Memory

Project-specific facts that should NOT be written back to hub go in `_Project_Memory/PROJECT_MEMORY.md` with timestamp prefixes:

```
[YYYY-MM-DD] Project-specific fact here.
```

The agent working on this project reads this file on wake. Do not push to hub unless the fact is cross-project.

---

## 7. Sync Contract (project ↔ hub)

- **Pull on wake:** hub `AGENTS.md` → this file → `_Project_Memory/PROJECT_MEMORY.md`
- **Push back to hub (rare):** only if a fact learned here is true across all of user's projects (e.g. "Amjad prefers bilingual submittals" → goes to hub `RULES.md`)
- **Push back to project memory (default):** any project-specific learning → `_Project_Memory/PROJECT_MEMORY.md`

---

## 8. Daily Checklist (project-level)

```bash
# 1. Pull hub (identity may have updated)
cd ~/hermes-memory && git pull --no-rebase

# 2. Pull this project (someone else may have pushed)
cd <PROJECT_LOCAL_PATH> && git pull --no-rebase

# 3. Read this AGENTS.md
# 4. Read _Project_Memory/PROJECT_MEMORY.md
# 5. Run hub health check
bash ~/hermes-memory/scripts/hub_health_check.sh
```

---

*Last updated: <YYYY-MM-DD>*
