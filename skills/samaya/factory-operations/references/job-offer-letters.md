# Job Offer Letters (عروض وظيفية) — Factory Positions

## When to Use

User asks for offer letters for factory workers (نجارين / عمال). The request usually comes with:
- A "طلب استحداث وظيفة" DOCX form (specifies positions, quantities, department, manager)
- An "إقامات" XLSX file (worker names, iqama numbers, phone numbers, nationality)

## Script

`~/.hermes/scripts/gen_offers.py` — generates Samaya-branded DOCX offer letters using SamayaDoc template.

## Workflow (from 2026-08-06 session)

1. **Read the request form** — extract positions, quantities, department, manager, location
2. **Read the iqama file** — extract worker names (AR + EN), iqama numbers, phone numbers, nationality
3. **Ask user for mapping** — which worker goes to which position (e.g. "1 and 2 are carpenters, 3 and 4 are workers")
4. **Run gen_offers.py** — generates personalized offer letters on Desktop
5. **Deliver files** — send to user or to the factory group chat

## Offer Letter Contents

Each letter includes:
- Samaya header (logo, company name, doc ref)
- Candidate info: name (AR/EN), iqama number, phone, position, department, location, manager
- Offer details table: salary, contract type, duration, hours, overtime, housing, transport, insurance, leave
- Probation period clause (3 months)
- Terms & conditions
- Acceptance signature block

## Salary Mapping (from 2026-08-06 session)

| Position | Salary |
|----------|--------|
| نجار / Carpenter | 2,500 SAR |
| عامل / Worker | 2,000 SAR |
| مساعد نجار / Assistant | 2,000 SAR |

## HR Register

After generating offers, create/update `HR/APPLICANTS_REGISTER.md` in `samaya-workspace` repo with:
- Full applicant list (name, position, salary, iqama, phone, nationality, source, status)
- Hiring tracker (interview date, offer date, hire date, status)
- Status workflow: جديد → قيد المراجعة → مقابلة → عرض وظيفي → تم التعيين / مرفوض

## Pitfalls

- **Names come from the iqama file, not the request form** — the form only has position counts and quantities
- **Always confirm the position-to-worker mapping** with the user before generating
- **Use SamayaDoc template** (navy #1E293B + gold, Calibri 11pt, A4 portrait, logo header) — import from `aseer-museum-pm/_Style-Guides/Doc Style Guide/samaya_doc_template.py`
- **Leave name field blank** if names aren't available yet
- **Deliver to repo, not webapp** — user prefers markdown registers in the repo over web-based tools
- **Send files to factory group chat** when user asks to share with the team
