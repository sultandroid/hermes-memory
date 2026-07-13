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
- `ws.cell(row=N)` without column argument raises TypeError — always pass both row and column
- Ibrahim Shaaban's "قائمة المهام تم" comments are task completion, not payment. Always check `payment_state` on the invoice.
- Odoo `purchase.order` does NOT have a `payment_state` field — that is on `account.move` (the invoice). Query invoices via PO's `invoice_ids`.
- When checking payment, query `account.move` with: `[[('id', 'in', inv_ids)]]` and read `payment_state` field.
