# Technical Proposal Page-by-Page Reference

Reference structure developed for Outline Enterprise (Project 010). Use as template for future manufacturer prequalification proposals.

## Page Inventory (24 pages A4 Portrait)

### Section 1: Front Matter (Pages 1-3)
| Page | Title | Key Content |
|------|-------|-------------|
| 1 | Cover | Logo, "Technical Proposal · Prequalification", Project ref, CR, Stats bar |
| 2 | Table of Contents | All 11 sections (A-K) + Appendices |
| 3 | Executive Summary | Company overview, scope statement, 4 key differentiators, photo |

### Section 2: Company & Legal (Pages 4-6)
| Page | Title | Key Content |
|------|-------|-------------|
| 4 | Section A: Legal & Corporate | 11-item table (A.1-A.11), each with status ✓/● |
| 5 | Section B: Certifications | 10-item table (B.1-B.10), ISO 9001, SASO/SABER, Supplier Auth |
| 6 | Section C: Factory & Manufacturing | Factory layout zones, equipment table (make/model/qty/condition), workforce, production capacity |

### Section 3: Systems & Processes (Pages 7-10)
| Page | Title | Key Content |
|------|-------|-------------|
| 7 | Section D: Quality Control | QC procedures, ITP descriptions, testing equipment, NCR process |
| 8 | Section E: Material Sourcing | Approved suppliers table, inventory system, logistics/storage |
| 9 | Section F: HSE | HSE policy, SBC 801 compliance, waste management, safety org |
| 10 | Section G: Project Experience | 24+ project table (6 sectors), relevant experience highlights |

### Section 4: Commercial & Compliance (Pages 11-13)
| Page | Title | Key Content |
|------|-------|-------------|
| 11 | Section H: Financial | Revenue table (3 years), insurance, bank reference |
| 12 | Section I: Local Content | Nitaqat status, Saudization %, LCWA goals, Vision 2030 alignment |
| 13-14 | Section J: Project-Specific Scope | All BOQ items, quantities, spec refs, compliance standards matrix |

### Section 5: Submission (Page 15)
| Page | Title | Key Content |
|------|-------|-------------|
| 15 | Section K: Documents Checklist | 24 items with ✓ / ● / 🔴 status indicators |

### Section 6: Appendices (Pages 16-24)
| Page | Title | Type |
|------|-------|------|
| 16 | Appendix Index | Document hierarchy, legend, status summary |
| 17 | Appendix A: Legal Documents | External doc refs with scan placeholders |
| 18 | Appendix B: Certifications | ISO scan box + Supplier Auth Letter template |
| 19 | Appendix C: Factory Documents | Equipment Inventory + Workforce Statement templates |
| 20 | Appendix D: Quality Documents | ITP + NCR Form + Calibration Register templates |
| 21 | Appendix E: Material Submittals | Submittal form for each BOQ item + Compliance Matrix |
| 22 | Appendix F: Project Execution | Shop Drawing Register + Mock-up Form + RFI Form |
| 23 | Appendix G: HSE Documents | HSE Policy + Risk Assessment + PPE Matrix |
| 24 | Appendix H: Submission Forms | Transmittal Letter + Cover Sheet + Receipt Acknowledgment |

## Key Design Numbers for A4 Portrait

| Element | Value |
|---------|-------|
| @page size | 210mm 297mm |
| @page margin | 12mm 15mm |
| .page width | 178mm |
| .page min/max height | 267mm |
| Body font size | 9pt |
| Section title (.st) | 20px / 15pt |
| Section Arabic (.sta) | 11px / 8pt |
| Body text (.sp) | 9px / 7pt |
| Table font (.tb) | 8px / 6pt |
| Image height (.ih) | 80mm |
| Page padding (.pd) | 18px 24px |
| Cover padding | 24px 32px |
| Footer font | 6.5px |
| Card padding | 7px |
| Card title | 9px |
| Card body | 8px |
| Checklist font | 7.5-8px |
| Cover h1 | 32px |
| Cover stat numbers | 12px |
| G2 gap | 5px |
| G3 gap | 4px |

## Template Design Patterns

### Status Indicators
```css
.check  /* green check: ✓ Attached */
.avail  /* amber: ● Available / In Progress */
.missing /* red: 🔴 To be provided */
```

### Table Pattern
```css
.tb { width:100%; border-collapse:collapse; font-size:8px; }
.tb th { background:var(--navy); color:#fff; padding:3px 6px; font-size:7px; text-transform:uppercase; }
.tb td { padding:3px 6px; border-bottom:1px solid var(--lg); }
```

### Section Header Pattern
```html
<div class="sl">Section 01</div>
<div class="st">Title Here</div>
<div class="sta">Arabic title</div>
```

### Footer Pattern
```html
<div class="pf">
  <span class="section-title">Section Name</span>
  <span class="page-num">01</span>
</div>
```
