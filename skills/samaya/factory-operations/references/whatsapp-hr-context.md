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
