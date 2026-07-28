# Credit Supplier Statement Update Workflow

When the user provides a PDF account statement (e.g. Saba Najd, Mada Aljezera) and asks to update the Factory cashout report:

## Steps

1. **Extract the PDF** with `pdftotext -layout`
2. **Parse the statement** — identify:
   - Opening balance (الرصيد الافتتاحي)
   - Payments (سند قبض — credit entries)
   - New invoices (فاتورة مبيعات آجلة — debit entries)
   - Returns (مرتجع المبيعات آجل)
   - Closing balance (الباقي)
3. **Cross-check against Odoo** before updating the report:
   - Query all POs for the supplier's partner_id (Saba Najd = 5603, Mada Aljezera = 2427)
   - Older POs (pre-statement period) should have `payment_state = 'paid'` on linked invoices
   - Recent POs (statement period) should match the statement's new invoice amounts
   - Check Ibrahim Shaaban's comments: "قائمة المهام تم" = task completion (goods received), NOT payment
   - To check payment: get PO's `invoice_ids`, query `account.move`, check `payment_state`
4. **Open the existing cashout report** at `Samaya_Factory_Cashout_Report_Updated.xlsx`
5. **Update the Summary sheet:**
   - Update closing balance to the new value from the statement
   - Add a new row for "New Invoices (DD-MMM to DD-MMM)" with the delta
   - Update the grand total
   - Update the "Prepared" date
   - Add a note row with Odoo cross-check result (e.g. "Odoo check: 50 POs found, older POs paid, recent Jun-Jul POs unpaid")
6. **Do NOT touch individual POs** — credit supplier POs are never listed individually per user preference

## Common Pitfalls

- The PDF may have a second page with additional transactions — always check for page breaks
- Date format in the PDF may be DD/MM/YYYY — convert to DD-MMM-YYYY for the report
- The statement is for Samaya Holding (parent company), not Samaya Factory — but the balance is still tracked in the Factory cashout report as a credit supplier
- **Statement total != Factory Odoo PO total.** Example (Jul 2026):
  - صبا نجد statement: 158,574.27 SAR vs Factory Odoo POs: 30,200 SAR (4 POs) — statement covers all Samaya projects
  - مدى الجزيرة statement: 35,564.38 SAR vs Factory Odoo POs: 63,187.85 SAR (18 POs) — reverse gap due to period misalignment
- `ws.cell(row=N)` without column argument raises TypeError — always pass both row and column
- Ibrahim Shaaban's "قائمة المهام تم" comments are task completion, not payment. Always check `payment_state` on the invoice.
- Odoo `purchase.order` does NOT have a `payment_state` field — that is on `account.move` (the invoice). Query invoices via PO's `invoice_ids`.
- When checking payment, query `account.move` with: `[[('id', 'in', inv_ids)]]` and read `payment_state` field.

## Concrete Example: Jul 2026 Statement Update

The user provided م صبا نجد and م مدى الجزيرة PDFs plus a هام file:

| Supplier | Statement Source | Statement Balance | Factory Odoo POs Total |
|---|---|---|---|
| صبا نجد | PDF (pdftotext extractable) | 158,574.27 SAR | ~30,200 SAR (4 POs) |
| مدى الجزيرة | PDF (CamScanner image — no text extraction) | 35,564.38 SAR | ~63,188 SAR (18 POs) |

**هام file items tracked:**
- 17 individual POs (mix of projects) + 2 credit supplier lines + 1 zero-item line
- Non-Factory POs excluded: P01543 (Quran), P02069 (Jalal), P02070 (Jalal), P02096 (Ghamama), P02099 (Maalim), P02116 (mixed factory/labor), P02129 (Jalal), P02181 (Ghamama), P02185 (Maalim), P02191 (Jalal), PO2084 (unknown)
- Factory POs included: P01970, P02092, P02139, P02226, P02227 (+ P01543 if it's Factory)
- Credit supplier items 18-19 treated as statement lines, not individual POs
- Item 20 (صبا نجد paints) = 0 SAR, stopped pending payment

**Report update approach:**
- Show statement balances in Credit Suppliers sheet as single lines
- Add a "Statement Cross-Reference" section comparing statement balance vs Factory Odoo POs
- Never add statement balances to the "Cashout Required" total
- Include the Odoo cross-reference counts in the notes
