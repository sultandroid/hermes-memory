---
name: entity-intake
description: When encountering a new project entity (company, contractor, supplier) in the Tqanny or Moqtana portfolio — research it via web, map its cloud portfolio, document the structure, and save to memory. Handles entity isolation (e.g. NOT Samaya).
version: 1.0.0
author: Hermes Agent
platforms: [macos]
metadata:
  hermes:
    tags: [project, research, onboarding, portfolio]
    examples: [outline-enterprise-intake]
---

# Entity Intake — Onboard a New Project Entity

## When to Use

- User mentions a new project/entity name you don't recognize
- A new folder appears in Tqanny_Projects or Moqtana projects
- User says "this is not [other entity] project" — entity isolation signal
- User asks "check this" or "study this" about an unknown entity

## Workflow

### Phase 1: Identify the Entity

Extract from context:
- Entity name (Arabic + English) — check PDF logos, folder names, file names
- Project number/code (if in Tqanny_Projects e.g. /010)
- Entity isolation — ask: "Is this [EntityName] or [OtherEntity]?" If user corrects you, note it prominently in the portfolio doc
- If a PDF exists with a logo but no text: use PyMuPDF render → tesseract OCR to extract any visible text

### Phase 2: Web Research (4 Sources Minimum)

Use DuckDuckGo (Google often returns captcha). Search Arabic and English names.

| Source | What to extract | Method |
|--------|----------------|--------|
| DuckDuckGo | Search result snippets, URLs | `curl -sL "https://duckduckgo.com/html/?q=<query>"` parse with regex |
| LinkedIn | Company description, size, sectors, year | LinkedIn page scraping for meta description |
| Company website | Products, services, about page | Check both `/en/` and `/ar/` URLs |
| Social media | Instagram bio, Facebook, X bio | Instagram `@handle` for bio text |

Extract these facts minimally:
- Full name (AR + EN)
- Parent company / group
- Years in market
- Number of factories / offices
- Products / services
- Client sectors served
- Social handles

### Phase 3: Cloud Portfolio Mapping

If the entity has a Google Drive folder:

1. Navigate with browser tool to the folder URL
2. Extract all row data via browser_console JS query:
   ```js
   Array.from(document.querySelectorAll('[role=row]')).map(r => r.textContent.trim())
   ```
3. Classify folders by sector (residential, hospitality, commercial, government, healthcare)
4. Note shortcuts vs shared folders
5. If view is truncated, scroll down and re-query

### Phase 4: Create Portfolio MD

Create an MD file in the project directory path:
```
Tqanny_Projects/[NNN]/ENTITY_NAME_PORTFOLIO.md
```

Structure:
- Entity header (name, parent, key stats)
- Google Drive link
- Portfolio table(s) by sector
- Local files inventory (from existing project folder)
- Entity isolation note if applicable (e.g. "NOT Samaya")

**Google Drive Browser Scanning — extract folder IDs for direct links:**
When viewing a shared Drive folder without login, the DOM may not expose folder IDs directly.
Use this multi-strategy approach to extract IDs:

1. Primary: query elements with `[data-id]` attribute:
   ```js
   Array.from(document.querySelectorAll('[data-id]')).map(el => el.getAttribute('data-id'))
   ```
2. Fallback: look at clickable row elements for identifier patterns in aria-label or class names
3. If only names are visible without IDs, document the names and note "folder IDs require login"
4. Document whether each item is a Shared folder, Shortcut, or file

### Phase 5: Save to Memory

Save a concise entry with:
- Entity name + project number
- NOT [other entity] isolation
- Key facts (sector, products, size)
- What exists locally
- What needs development

Keep under 250 chars in memory. Memory is finite (2,200 chars).

### Phase 7: Trigger Prequalification Design (if applicable)

If the entity is a supplier, manufacturer, or contractor that needs prequalification documents:

1. Note this in the gap analysis
2. Reference/suggest creating the following:
   - Factory/Manufacturer-specific prequalification checklist (not generic subcontractor template)
   - Company capability statement (profile + data sheet)
   - Compliance matrix for spec adherence
   - HTML/DOCX formatted professional profile
3. If the user asks to proceed, use `supplier-prequalification` skill for the document design phase

The entity-intake covers RESEARCH. The design of prequal documents is a separate class of work handled by the supplier-prequalification skill.

## Pitfalls

- **Google Drive requires login for full visibility.** Public views show limited data. Note "requires login" if critical folders are invisible.
- **DuckDuckGo may rate-limit.** If you get empty results, wait or use a different User-Agent.
- **ole.sa and similar Saudi sites often have broken English pages** with template content from the theme. Use the Arabic URL path instead for real content.
- **Entity isolation is critical.** If the user corrects "this is NOT Samaya" or similar, the portfolio MD must state it clearly. Memory must also carry the isolation note.
- **LinkedIn meta descriptions** are often the most reliable single source for company facts. Extract the `og:description` meta tag.
- **Google Drive DOM is in an iframe** on the main page. The grid rows may live in the main document or be nested. Query `[role=row]`, `[role=gridcell]`, and text from the root document first.
- **Don't create a new skill for every entity.** One entity intake does not warrant a skill — the entity facts go to memory, the technique goes in this skill.
