# Odoo Timesheet & Description Conventions (Samaya)

## Timesheet `unit_amount` Field

**CRITICAL:** `unit_amount` on `account.analytic.line` is stored in **minutes**, not hours or decimal hours.

| Value | Meaning | Correct Use |
|-------|---------|-------------|
| 30 | 30 minutes | `unit_amount: 30` |
| 60 | 1 hour | `unit_amount: 60` |
| 90 | 1.5 hours | `unit_amount: 90` |
| 120 | 2 hours | `unit_amount: 120` |
| 240 | 4 hours | `unit_amount: 240` |

**Never** pass decimal hours (e.g., 1.5, 2.0, 4.5). Always convert to minutes first.

## Task Description Rules

- Descriptions must be **plain text / minimal HTML**.
- **No emoji or icons** allowed in task descriptions.
- Use simple `<h3>`, `<p>`, `<ul>`, `<li>`, `<b>` only when necessary.
- Keep descriptions factual and concise. Avoid decorative symbols.

These rules were established after repeated user corrections during active timesheet and task updates on the Samaya Odoo instance.