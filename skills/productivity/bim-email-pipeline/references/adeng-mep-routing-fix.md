# Adeng.com.sa — MEP Design Routing Correction

**Date:** Jun 5, 2026 (Week 23)

## Issue

Email from `supervision@adeng.com.sa` titled "MEP Design Services – Asir Regional Museum Project" was auto-routed to `attachments/general/proposals_contracts/` by the email pipeline because neither the sender domain nor the email subject matched project-specific patterns.

## Correction

This is an **Aseer Regional Museum (متحف عسير)** project document. The `العرض الفني والمالي.pdf` (technical and financial proposal) should be filed under:

```
Aseer-Museum/Design Files/00_Scope_and_Proposals/
```

## Detection Pattern for Future

- Subject contains "Asir Regional Museum" or "متحف عسير" → project = **aseer_museum**, not general
- Sender `@adeng.com.sa` = MEP design consultant → type = **proposals_contracts**
- Even though sender domain is `adeng.com.sa` (not a known Samaya/CG domain), the subject explicitly references the project name

## Action

- [ ] Move `general/proposals_contracts/العرض الفني والمالي.pdf` → `Aseer-Museum/Design Files/00_Scope_and_Proposals/`
- [ ] Add `@adeng.com.sa` to the Aseer project classification list in the pipeline scoring engine
