# Multi-Repo Topic Search — "هل عندنا نقاش عن X؟"

When the user asks whether a topic/discussion/decision already exists on the repo
(e.g. "هل عندنا نقاش عن فصل المصنع على الريبو؟"), do NOT assume it's absent.
The user's work is split across **three** Samaya repos, and a topic may live in
any of them — or only as a commit, a GitHub issue, or an ERP/config setup record.

## The three repos

| Repo | Scope |
|------|-------|
| `aseer-museum-pm` | Aseer Museum project (registers, discussions, CG responses) |
| `samaya-profile` | Factory company profile + admin reports |
| `samaya-workspace` | Factory operations (Odoo, POs, OT, decisions, tickets) |

## Search recipe (run ALL of these before concluding "not found")

```bash
# 1. Content grep across all three repos (Arabic + English terms)
grep -rln "فصل المصنع\|فصل.*المصنع\|استقلال\|كيان مستقل\|factory separation" \
  aseer-museum-pm samaya-profile samaya-workspace --include="*.md" 2>/dev/null \
  | grep -v node_modules

# 2. git log --grep — topic may be in a commit message, not a file
for d in aseer-museum-pm samaya-profile samaya-workspace; do
  git -C $d log --all --oneline --grep="فصل\|separat\|استقلال\|كيان" -i | cat
done

# 3. GitHub issues (per repo)
gh issue list --repo sultandroid/$repo --search "<topic>" --state all

# 4. The canonical discussions INDEX (aseer project)
cat aseer-museum-pm/09_Agent_Workspace/discussions/INDEX.md
```

## Key pitfall — distinguish record TYPES

A topic may exist only as an **ERP/config setup record**, not as a
discussion/decision file. Example: "فصل المصنع" exists as the Samaya Factory
being set up as a **separate Odoo company** (`parent_id=False`, company ID 7,
name "Samaya Factory — كيان مستقل") — see
`~/.hermes/skills/software-development/odoo/references/samaya-odoo-factory-setup.md`.
That is a technical/setup record, NOT a discussion/decision.

Before telling the user "it doesn't exist", say which type you found:
- **Setup/technical record** exists (ERP config, Odoo entity) → report it, and
  offer to create a proper discussion/decision file if that's what they want.
- **Discussion/decision file** exists → point to it directly.
- **Nothing** → only then say it's absent.

## Session example (2026-09-04)

User asked about a "فصل المصنع" discussion. Searches found only the Odoo
separate-company setup record (14-06-2026) — no discussion/decision file. The
correct answer distinguished the two and asked which the user meant.
