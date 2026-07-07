# CG_STATUS.md — Readable Alternative to PROJECT_MEMORY.md

**Context:** Aseer Museum PROJECT_MEMORY.md files are OneDrive cloud-only placeholders (`compressed,dataless` attribute) — cannot be read locally. The sync engine (`fileprovi`) holds an exclusive lock causing `Resource deadlock avoided` on all read attempts.

## Readable Alternative

The file `Aseer-Museum/MD/CG_STATUS.md` **IS readable** — it resides in an Obsidian vault directory that is either outside OneDrive or fully synced.

### What It Contains

- CG response status for Aseer Museum Stakeholder Plan (PL-0020 Rev.01)
- **Status:** "C — Revise and Resubmit" (received 2026-06-02)
- **19 CG comments** covering:
  - IT/Security requirements
  - Organization chart updates
  - MEP designer qualifications
  - Structural engineer credentials
  - Procurement team composition
- Lists key CG consultants and their email contacts

### When to Use

Use `CG_STATUS.md` as a proxy source when:
1. PROJECT_MEMORY.md is locked by OneDrive sync
2. You need the latest CG response codes and comment counts
3. You're generating a pipeline report and need the aggregate CG status

### Path

```
/Users/mohamedessa/Library/CloudStorage/OneDrive-SAMAYAINVESTMENT/Samaya/Technical Office/Bim Unit/Aseer-Museum/MD/CG_STATUS.md
```

### Limitation

CG_STATUS.md covers only the Stakeholder Plan. For full project memory (RFI register, daily logs, email summaries), PROJECT_MEMORY.md is the canonical source — but requires OneDrive to sync locally before it can be read.
