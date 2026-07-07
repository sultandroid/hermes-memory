# Codex Research & Document-Creation Prompt Template

Use this template when delegating research-heavy document-creation tasks to Codex. Fill in the bracketed `[placeholders]` for each task.

## Template

```
Create a [DOCUMENT TYPE: e.g. comprehensive meeting preparation file / market comparison report / feasibility study / vendor evaluation] for [PURPOSE: e.g. a Leica RTC360 scanner evaluation meeting]. Save as '[FILENAME.md]' in the current directory.

## Context
[Background: who we are, what project, who the audience is, what decision is being made]
[Reference files: mention any files in the current directory Codex should read first]

## The document MUST cover:

### 1. [Section Title]
- [sub-point A]
- [sub-point B]

### 2. [Section Title]
- [sub-point A]
- [sub-point B]

### 3. Questions to [Clarify/Research] — organized by category
- [Category 1 heading]
  - [Specific question 1]
  - [Specific question 2]
- [Category 2 heading]
  - [Specific question 1]

### 4. Market / Alternatives Research (REQUIRED — search the web)
Research and compare at least these [alternatives / options]:

#### [Option 1 Name]
- Price range
- Key specs
- Pros/Cons vs primary

#### [Option 2 Name]
- Price range
- Key specs
- Pros/Cons vs primary

### 5. [Recommendation / Decision Framework]
- Comparison matrix / decision matrix
- Weighted scoring table (if applicable)
- Suggested negotiation points
- Recommended path forward

### 6. Action Items
- Pre-XXX checklist
- During-XXX agenda
- Post-XXX follow-ups

## Important
- Research actual data online — don't make up numbers
- Cite sources with URLs in a Source Notes section
- Write in clear English, appropriate for [target audience description]
- Add a table of contents
- Add a Source Notes section at the end with all URLs referenced
```

## Example: Vendor Evaluation Meeting Prep

See this session (31 May 2026) for a working example — the full prompt used in the Leica RTC360 meeting prep task is in the conversation transcript. Key elements:
- Supplier discussion points document as reference
- Two pricing paths to compare
- 7 market alternatives all researched via web search
- Weighted scoring matrix with 6 criteria
- 55+ specific questions organized by category
