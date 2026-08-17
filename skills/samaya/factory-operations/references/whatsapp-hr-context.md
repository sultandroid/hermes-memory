# WhatsApp Chat as HR / Termination Context Source

When the user references a WhatsApp message from Raouf (رؤوف) about factory staff —
terminations, salary increases, contract end dates, overtime refusals — the full
context lives in the WhatsApp `_chat.txt` export, NOT in Odoo.

## Where the export lives

Users drop the export as a zip (`WhatsApp Chat - Raouf Eldeeb.zip`) into
`~/.hermes/cache/documents/`. Unzip to a working dir, then grep the `_chat.txt`.

```bash
unzip -o "WhatsApp Chat - Raouf Eldeeb.zip" -d raouf_chat
grep -nE "هتمشي|استقال|انتهاء|عقد|زياده|زيادة|راتب|salary" raouf_chat/_chat.txt
```

## Why it matters

- **Odoo `hr.employee` is thin for these workers** — the `sultan@samayainvest.com`
  account (uid 151) lacks rights to `identification_id, gender, birthday, marital,
  country_id, notes, contract_id` (needs "Employees / Officer: Manage all employees").
  You can read `name, job_title, department_id, work_email, work_phone, active`.
- **job_title = iqama role, not real role** — e.g. حسن البرمبالي is "Carpenter" in
  Odoo but is the veneer/veneer-team lead (القشرة). محمود عوض (عواضي) is also
  "Carpenter". Confirm real role from chat context, not Odoo.
- **The chat carries the decision trail** — who asked for a raise, who approved the
  termination, the exact contract end date. Odoo has none of this.

## Pattern: reconstruct a termination decision

1. Grep the chat for the worker's name + `عقد|هتمشي|زياده|راتب`.
2. Read the surrounding lines (sed a window) to get the full sequence:
   - salary-increase request → management counter-offer → termination decision → approval.
3. Cross-check the worker's Odoo record (name, dept, job_title) to confirm identity.
4. Report the decision trail, not just the final message.

## Contract end-date calculation (user-corrected rule)

**Contract is annual; end date = 1 year from the HIRE date (تاريخ التوظيف),**
renewing on the same date each year. The user's final decision (17/08/2026):
"تاريخ التوظيف ماشي" — use the hire date, NOT the renewal date and NOT Odoo
`create_date`. (Earlier in the same session the user first said "سنة من تاريخ
التجديد" then corrected to hire date — the hire-date rule is the operative one.)
- For extended/renewed contracts (العقود الممددة), notice must be given before
  the specified period per Saudi Labor Law (Art. 75).
- When the hire date is unknown, write **"حسب تاريخ انتهاء عقده"** (per his
  contract end date) in the memo rather than inventing one.

## Where to find hire dates (Odoo has none)

- **Odoo `hr.employee.hire_date` is empty** for factory workers; `create_date` is
  record-creation, NOT hire date.
- **`hr.contract` is unreadable** by the `sultan@samayainvest.com` account (uid 151)
  — raises `Fault 4: "You are not allowed to access 'Employee Contract' (hr.contract)"`
  (needs Contracts/Administrator or Contracts/Employee Manager).
- **Hire dates live in repo CSV exports** under `samaya-workspace/`:
  - `DATA/employees_full_details.csv` (column "تاريخ التوظيف")
  - `DATA/workshop_employees_final.csv` (column "Hire Date")
  - `DATA/workshop_dashboard.csv`, `DATA/employees_detailed.csv`
- These are historical exports, not live — treat as reference; confirm renewal dates
  with HR.

## Saudi Labor Law — notice period (Art. 75)

| Service length | Required notice |
|----------------|-----------------|
| < 5 years       | 30 days         |
| ≥ 5 years       | **60 days**     |

- If notice isn't given in time, the contract **auto-renews** on the same terms
  (Art. 74) or the worker can claim compensation for the notice period.
- "شهرين بالضبط" (exactly 2 months) in Raouf's message = the 60-day notice for
  workers with 5+ years service. HR must notify on the day that is exactly 60 days
  before the contract end date.

## Example — محمود النجار + حسن البرمبالي (Aug 2026)

- 10/06: Raouf — "محمود النجار + حسن البرمبلي كلموني على زيادة الرواتب، علشان مش عارفين يعيشوا"
- 06/08: Raouf — "النجارين كل واحد عاوز 500 ريال للسكن"; Sultan — "نجار 2500 / عامل 2000، لو مش عاجبهم يمشوا"
- 13/08: Raouf — "يوم 18 شهر 10 — عقود محمود النجار وحسن البرمبالي، الاتنين بالسلامة خلاص كفاية عليهم كدة"
- 14/08: Sultan — "برحتك / لكم الحرية / وعليا الدعم" (approval)
- 17/08: Raouf — "اليوم 17 أغسطس ويوم 18 أكتوبر = شهرين بالضبط، يجب على الموارد البشرية إخبار الناس اللي هتمشي النهاردة"

Note: the user corrected the name — it's **محمود عوض (عواضي)**, not "الحميدي".

## Full termination list (Aug 2026) — chat name → Odoo record

The user enumerated **5** workers Raouf wants to terminate (corrected from an
initial 6 — **مد المغير is NOT in this list**; he has a separate early-termination
request already sent to HR on 20/07). Map the chat/spoken name to the Odoo
`hr.employee` record — **spoken names often differ from Odoo names**:

| Chat / spoken name | Odoo record (id) | job_title | dept |
|--------------------|------------------|-----------|------|
| حسن البرمبالي | حسن حسين محمد البرمبالي (897) | Carpenter | 18 |
| محمود النجار (عواضي) | محمود عبدالحميد علي عواضي (997) | Labor | 18 |
| راسيل | مد راسل سيكدار مد (1003) | Labor | 18 |
| جعفر كاسي | **أبو جعفر كالسي (1630)** | Labor | 18 |
| نعيم | نعيم انس (3487) | عامل | 18 |

**Pitfall — don't over-count the termination list.** When the user says "اللي
رؤوف عايز يمشيهم", confirm the exact count before drafting. مد المغير (999/1634)
looks like part of the same batch but is a SEPARATE early-termination request
(20/07, already emailed to HR) — keep him out of the contract-end memo. The 5
above are the contract-end / non-renewal batch.

**Pitfall — user-provided Odoo IDs can be wrong.** The user gave "سهيل رقم 898",
but id 898 is حسن عبد الاله محمد ابوبكر (Graphic designer, inactive). سهيل is
**موحد سهيل عارف (1629)**. Always `search` by name and confirm the record matches
the person before acting on a user-supplied ID.

**مد المغير has TWO records** (999 "مد المغير" and 1634 "علم الدين ابكر ادم محمد").
Raouf himself said "مد المغير اللي هوا علم الدين". Confirm which record is the
active/real one before updating.

## Odoo hr.employee field quirks (uid 151)

- `date_of_hire` does NOT exist → the field is **`hire_date`** (type `char`, often empty).
- `work_location` does NOT exist on `hr.employee` (raises "Invalid field").
- `create_date` is the record-creation date, NOT the hire date — don't use it as
  service-length evidence. For these workers `hire_date` is usually empty, so
  service length must come from the WhatsApp chat, not Odoo.

## Termination request to HR = Odoo helpdesk ticket, NOT a formal memo (user-mandated)

**The user does NOT want formal letters/memos for terminations.** When he says
"جهز مسودة" for a termination, he means a **simple Odoo helpdesk ticket** (team
10 = Human Resources And Administration, stage 1 = New). He explicitly rejected
the memo format: "انا مش عاير خطابات انا بخطط اعمل تذكره فقط" and "اقصد تذكره
اودو وليس مذكره".

**Workflow:**
1. **Draft the ticket text first** for approval — never create it in Odoo directly.
2. Once approved, create the `helpdesk.ticket` in team 10, stage 1 (New).

**Ticket shape:**
- Subject: "الاستغناء عن عمال المصنع"
- Body: short notice that factory management no longer wants the workers + a
  table (name / real job / biometric code) + request to handle legally (notice,
  dues, iqama) and report the execution plan.
- No legal-article citations, no dues calculations, no formal letterhead — keep
  it a plain ticket.

## Aug 2026 termination list (5 workers) — with biometric codes

| # | Name | Real job | biotime_code | Hire date |
|---|------|----------|:--:|:--:|
| 1 | حسن حسين محمد البرمبالي | **مشرف قسم النجارة** (carpentry supervisor) | 725 | 18/10/2023 |
| 2 | محمود عبدالحميد علي عواضي (النجار) | نجار | 726 | 18/10/2023 |
| 3 | مد راسل سيكدار مد (راسيل) | عامل | 664 | 20/06/2022 |
| 4 | أبو جعفر كالسي (جعفر كاسي) | نجار | 1058 | 21/04/2025 |
| 5 | نعيم انس | عامل | 1171 | 16/07/2025 |

- **حسن البرمبالي's real role is مشرف قسم النجارة** (carpentry supervisor) —
  the user corrected this; earlier notes said "قائد فريق القشرة" (veneer lead).
- Biometric codes come from Odoo `hr.employee.biotime_code` (725/726/664/1058).
  **نعيم has no biotime in Odoo** — 1171 came from the WhatsApp chat.

## Department transfer (write op)

Moving a worker between departments is a legitimate `hr.employee` write (not
read-only chatter). Warehouse dept = **98** (`Samaya / المستودع`), Manufacturing = 18.

```python
models.execute_kw(db, uid, pw, 'hr.employee', 'write', [[1629], {'department_id': 98}])
```
