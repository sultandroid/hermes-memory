# Adding Odoo Chatter Comments to Purchase Orders

When the user wants to add a comment to multiple POs in Odoo (e.g., marking them with a cashout report reference), use `message_post` on the `purchase.order` model.

## Method

```python
call('purchase.order', 'message_post', [[po_id]], {
    'body': '[Cash Out Report NO 20260707 Date: 07-Jul-2026]',
    'subject': 'Cash Out Report',
    'message_type': 'comment',
    'subtype_xmlid': 'mail.mt_note'
})
```

- `message_post` is always available — it won't appear in `fields_get()` but will work.
- `subtype_xmlid='mail.mt_note'` makes it an internal note (not a notification email to followers).
- Returns the message ID.

## Find PO IDs by name

```python
ids = call('purchase.order', 'search', [[['name','=','P01094']]])
```

## Batch with status reporting

Iterate through the PO list, track success/fail counts, print each result.

## SSL fix

All Odoo XML-RPC calls need: `SSL_CERT_FILE=$(python3 -c "import certifi; print(certifi.where())")`