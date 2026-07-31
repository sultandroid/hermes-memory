# OPEN QUESTIONS — Policy Decisions Awaiting User

> These are **policy / lifestyle** questions only the user can answer. An agent MUST NOT silently decide these. Each entry has: the question, why it matters, and a recommended default that the user can confirm or override.

---

## Q1. Credential storage convention

**Question:** Where should non-Odoo credentials live? (Telegram bot token, GitHub PAT, Outlook OAuth, surge token, etc.)

**Why it matters:** Right now there is no policy. Every new secret gets a new ad-hoc location, which makes rotation hard and creates audit risk.

**Known locations in use today:**
- Odoo: `~/.config/samaya/odoo.env` (per `README.md`)
- GitHub: `~/.git-credentials` (git credential helper = store)
- Surge: `~/.netrc` (machine `surge.surge.sh`)
- Telegram (Hermes): auto-discovered by `hermes_notify.sh` from `~/.hermes/config/telegram_token` and `~/.hermes/config/telegram_chat_id`

**Recommended default:**
```
~/.config/hermes/
├── odoo.env            # Odoo API key + URL + DB
├── github.env          # GitHub PAT (if not in git-credentials)
├── telegram.env        # Telegram bot token + chat IDs
├── outlook.env         # Outlook OAuth tokens
└── README.md           # what's in here, how to rotate
chmod 600 on all .env files
```

Add to `~/.gitignore` (per project) the pattern `*.env` and add a symlink convention so scripts auto-discover.

**Status:** ❓ Awaiting user decision

---

## Q2. Skill retirement / deprecation policy

**Question:** How do we mark a skill as deprecated, and how do agents know not to load it?

**Why it matters:** `skills/` has 36+ categories. Some reference 2024-era workflows, old library versions, or superseded APIs. An agent that loads them by trigger phrase wastes tokens and may give outdated advice. There is currently no mechanism for "this skill is deprecated, load `skill-name-v2` instead."

**Recommended default:**
- Add a `status:` field to skill frontmatter: `active | deprecated | experimental`
- Deprecated skills get a `DEPRECATED.md` in their folder explaining: when deprecated, what replaces it, when to remove
- `hub_health_check.sh` warns on any skill with `status: deprecated` older than 90 days (auto-removal candidate)
- New skills default to `status: experimental` for 30 days, then promote to `active` after one review

**Status:** ❓ Awaiting user decision

---

## Q3. Language policy edge cases

**Question:** `USER.md` says "English only in replies." But there are legitimate Arabic use cases — what is the exact policy?

**Edge cases the rule doesn't currently address:**

| Context | English? | Arabic? | Notes |
|---|---|---|---|
| Telegram reply to user | ✅ | ❌ | Per `USER.md` |
| Code comments | ✅ recommended | ⚠️ allowed if codebase is Arabic-native | Style choice, not a rule |
| Commit messages | ✅ | ❌ | Per `RULES.md` English-only formal output |
| File names (deliverables) | ✅ recommended | ⚠️ allowed for Arabic-named projects | E.g. `قلعة_تبوك.xlsx` is legitimate for Tqanny sub-project |
| Folder names | ✅ recommended | ⚠️ allowed if user named it so | Don't transliterate existing Arabic folder names |
| Branch names | ✅ | ❌ | Keep git internals English |
| Doc codes (MOC-MUS-ASE-*) | ✅ | ❌ | Already in English in current use |
| Project names in `PROJECTS.md` | ✅ recommended | ⚠️ allowed with translation | e.g. `Tqanny (شبرا)` — keep both for clarity |
| Email body to Egyptian client | ❌ | ✅ | Per `RULES.md` — bilingual/Arabic for Egyptian consulting offices |
| Excel cell content | depends on register | depends on register | Bilingual headers OK |

**Recommended default:** Refine `USER.md` to: "English-only in **replies to user** and **git/CLI internals**. Arabic allowed in: client-facing deliverables to Egyptian offices, folder/file names that user has already named in Arabic, and project names in `PROJECTS.md` (with English transliteration in parens)."

**Status:** ❓ Awaiting user decision

---

## How to resolve

For each question, reply with one of:
- **A (accept recommended default)** — I implement it
- **B (override with specific change)** — you tell me the rule
- **C (defer)** — leave as-is for now, revisit later

When all three are resolved, this file can be deleted (or moved to `references/resolved-decisions.md` for history).
