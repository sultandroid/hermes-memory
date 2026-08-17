# Overtime (الأوفر تايم) Follow-up Email to HR

When the user drafts a follow-up/reminder email to HR about delayed overtime
payments, the email must **cite concrete facts (وقائع) and reference helpdesk
ticket numbers** — not just restate the problem generically.

## The recurring situation (as of Aug 2026)

- Overtime payments are **chronically delayed**: some workers since **Nov/Dec**,
  many since **Jan/Mar** 2026.
- The user (Sultan, Factory Manager) sends the follow-up to HR. Primary HR
  contact for this: **Bandar Alquayyid** (بندر القييد).
- The user's own email of **1 Aug 2026** (subject "متابعة آلية صرف أجور العمل
  الإضافي (Overtime) ومعالجة تأخر المستحقات") got **no reply / no action** —
  the reminder is a follow-up to that.

## Overtime refusal / strike timeline (facts to cite)

| Date | Fact |
|------|------|
| 20/07 | Partial strike in the workshop over unpaid overtime |
| 01/08 | 3 painters (ورشة الدهانات) refused overtime — violation memos issued |
| 12/08 | Carpenters also refused overtime (محمود، موسى، وآخرون) |
| 16/08 | Repeated worker demands for overdue salaries |

## Helpdesk ticket numbers (Odoo, team 10 = HR & Admin)

Query: `helpdesk.ticket` search by `name ilike 'اوفر'/'overtime'/'الاضافي'`.

| Ticket | Subject | Stage |
|:---:|---|---|
| #1175 | متابعة صرف مستحقات العمل الإضافي (أغسطس–ديسمبر) — Sultan | Solved |
| #2010 | الأجر الإضافي لفريق العمل (Overtime problems) — Raoof | Solved |
| #2611 | ساعات العمل الإضافية / **يونيو 2026** — Hesham | **In Progress** |
| #2755 | ساعات العمل الإضافية / **يوليو 2026** — Hesham | **In Progress** |

The **open (In Progress)** tickets are #2755 (July) and #2611 (June) — these are
the ones needing follow-up. Older tickets (#2010, #1175) were closed "Solved" but
the money is still unpaid.

## Email structure (user-preferred)

1. **Subject**: تذكير — متابعة آلية صرف أجور العمل الإضافي (Overtime) ومعالجة تأخر المستحقات
2. **Opening**: إشارةً إلى إيميلنا السابق بتاريخ 1 أغسطس 2026، وحيث لم يصلنا رد أو إجراء...
3. **أولًا: حجم التأخير** — بعض العاملين منذ نوفمبر/ديسمبر، والكثير منذ يناير/مارس.
4. **ثانيًا: الوقائع المسجلة على النظام** — table of ticket numbers + dates + stages.
5. **ثالثًا: أثر التأخير على سير العمل** — strike/refusal timeline.
6. **الطلبات**: (1) الإسراع في الصرف، (2) اعتماد آلية مستقرة، (3) إفادتنا بموعد الصرف.
7. Signed محمد سلطان — مدير المصنع.

## Pitfalls

- **The user is replying to their OWN 1 Aug email** (which got no response) — the
  reminder is a follow-up, not a fresh complaint. Open with "إشارةً إلى إيميلنا السابق".
- **Cite ticket numbers, not just dates** — the user explicitly asked to استشهد
  بأرقام التذاكر. Pull real ticket IDs from Odoo `helpdesk.ticket`, don't invent them.
- **Full email body is NOT in Outlook SQLite** — `Message_Preview` is truncated
  (~255 chars). For the user's own sent email, the body may not be recoverable;
  reconstruct the facts from the WhatsApp chat + Odoo tickets instead.
- **Overtime delay ≠ a single month** — the delay spans Nov/Dec (some) through
  Jan/Mar (many) to July (current). State the range, not one month.
