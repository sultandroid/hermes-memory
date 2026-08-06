---
name: samaya-doc-style-guide
title: Samaya Document Style Guide — Unified Style System
description: Maintain the canonical style guide repo at github.com/sultandroid/samaya-doc-style-guide, published at samaya-factory.com/style-guide/. Every project repo inherits its visual identity from here.
tags: [samaya, style-guide, branding, docx, html, pdf, logos]
---

# Samaya Document Style Guide

## Repo

- **GitHub:** `github.com/sultandroid/samaya-doc-style-guide`
- **Live:** `samaya-factory.com/style-guide/`
- **Local:** `~/samaya-doc-style-guide/`

## Structure

```
samaya-doc-style-guide/
├── general/                    # Shared style guides (immutable)
│   ├── docx/                   # .docx — Calibri Navy/Red, A4 portrait
│   ├── html-plan/              # A4 portrait plans — Montserrat/Inter, Navy/Sky/Green
│   ├── html-deck/              # A4 landscape decks — Inter/Menlo, Navy/Sky/Green
│   ├── rfi/                    # RFI/TQ letters (templates + assets)
│   ├── cv/                     # CV submittal packs
│   ├── tokens.css + style.css  # Shared CSS tokens
│   └── index.html              # Preview page
│
├── projects/                   # Per-project overrides
│   ├── aseer-museum/           # Navy #0F172A · Sky #0284C7 · MOC/CG/NRS logos
│   ├── zamzam-museum/          # NWC client · ZAM-NWC- prefix
│   └── factory-profile/        # Dual identity (see below)
│
├── assets/logos/               # Canonical logos (Samaya + clients)
├── templates/                  # Starter files
├── AGENTS.md                   # Agent instructions
├── HOWTO.md                    # How projects inherit styles
└── README.md                   # Full documentation
```

## How projects inherit styles

1. Every project repo has `_Style-Guides/README.md` pointing to this repo
2. Read `general/<type>/` for the base guide
3. Read `projects/<project-name>/` for overrides
4. Use `templates/` for starter files
5. Reference logos from `assets/logos/` by relative path — never copy logos into project repos

## Factory Profile — Dual Visual Identity

The factory profile has **two distinct identities** that must NOT be mixed:

### A. Website (samaya-factory.com)
- **Background:** Black `#000000`
- **Primary:** `--blue-accent: #1e5a9e`, `--blue-accent-dark: #162456` (most used)
- **Accent light:** `--blue-accent-light: #5ba3d9`
- **Gold:** `#a36100` · **Cream:** `#c8c0b0` · **Red:** `#fb2c36`
- **Font:** Cairo (Google Fonts) — Arabic primary
- **Direction:** RTL
- **Type:** React SPA — web experience, not print-oriented

### B. Profile Booklet (v1/v2/v3)
- **Format:** A4 landscape (297×210mm)
- **Navy:** `#0B1F3F` · **Gold:** `#C9A24A` · **Cream:** `#F7F5F0`
- **Fonts:** Cormorant Garamond (Latin display) + Tajawal (Arabic) + Inter (body)
- **Direction:** RTL primary (Arabic), LTR for English
- **6 official departments** (per user approval)
- **Design spec:** `DESIGN.md` in `samaya-profile` repo, `feature/page-4-redesign` branch

## Aseer Museum — Style Overrides

| Token | Hex | Usage |
|-------|-----|-------|
| Navy | `#0F172A` | Headings, table headers, cover |
| Sky | `#0284C7` | Section accent bars, RACI-A |
| Green | `#16A34A` | Pass/closure badges |
| Red | `#B91C1C` | Critical badges, CODE C |
| Body | `#1E293B` | Paragraphs |
| Muted | `#64748B` | Captions, metadata |

**Typography:** Montserrat (headings) + Inter (body) + Menlo (metadata) + IBM Plex Sans Arabic  
**Page model:** A4 portrait, 210×297mm, 12mm/16mm padding  
**Density system:** `.compact` / `.tight` modifiers

## How to add a new project

```bash
mkdir -p projects/<project-name>/
cat > projects/<project-name>/README.md << 'EOF'
# <Project Name> — Style Guide Overrides

**Base Guide:** `general/<type>/`
**Status:** Active

## Overrides
- (list what's different from the general guide)
EOF
```

Then add `_Style-Guides/README.md` to the project repo pointing here.

## Deploy to samaya-factory.com

```bash
cd ~/samaya-doc-style-guide
tar czf /tmp/style-guide-deploy.tar.gz --exclude='.git' .
scp -P 65002 /tmp/style-guide-deploy.tar.gz u517606786@samaya-factory.com:/home/u517606786/
ssh -p 65002 u517606786@samaya-factory.com "mkdir -p /home/u517606786/domains/samaya-factory.com/public_html/style-guide && cd /home/u517606786/domains/samaya-factory.com/public_html/style-guide && tar xzf /home/u517606786/style-guide-deploy.tar.gz && rm /home/u517606786/style-guide-deploy.tar.gz && chmod -R 755 ."
```

The `.htaccess` at root must exclude `/style-guide/` from the `/build/` rewrite rule.

## Pitfalls

- **OneDrive EDEADLK** when copying style guide files — use `cp` with retry or copy via Micro volume
- **Live site CSS extraction** — the samaya-factory.com site is a React SPA with Tailwind; CSS variables are `--black`, `--blue-accent`, `--blue-accent-dark`, `--blue-accent-light`, `--sans` (Cairo). Extract by grepping the built CSS file for `var\\(--` and hex colors.
- **.htaccess ordering** — the `/style-guide/` exclusion must come BEFORE the catch-all rewrite rule
- **Logo licensing** — only Samaya + client logos in `assets/logos/`. Never add third-party logos without confirmation.

## Known Issues (as of 2026-08-02)

- **4 logo files are 0 bytes** — `bma-logo.svg`, `nrs-logo-trans.png`, `pmc-logo-trans.png`, `rcrc-logo.svg` are empty. Copy from `aseer-museum-pm/_Style-Guides/logos archives/` to fix.
- **Live site returns HTTP 403** — `samaya-factory.com/style-guide/` is inaccessible. Check `.htaccess` exclusion rule and server permissions.
- **No index page** — `general/index.html` is a demo page, not a style guide index. Visitors see a raw file listing.
- **Empty template directories** — `templates/docx-template/` and `templates/html-deck-template/` exist but contain no files.
- **CSS token mismatch** — `tokens.css` and `style.css` use different variable sets. `tokens.css` is missing many variables defined in `style.css`.
- **No validation script** — no tool to check if a document conforms to the style guide.
- **No deploy script in repo** — deployment is manual via tar/scp; no `deploy.sh` committed.
