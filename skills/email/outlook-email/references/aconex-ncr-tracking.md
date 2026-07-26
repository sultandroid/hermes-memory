# Aconex NCR Transmittal Tracking

CG issues NCRs (Non-Conformance Reports) via Aconex workflow transmittals. These arrive as Aconex notification emails with the subject pattern:

```
CGP-WTRAN-000NNN: (WF-000NNN) Failure to ... / Formal Notice ...
```

## Query Pattern

Find NCR transmittals by searching for Aconex emails with "Failure" or "NCR" or "NC-" in the subject:

```sql
SELECT datetime(m.Message_TimeReceived, 'unixepoch') as dt,
       m.Message_NormalizedSubject,
       m.Message_SenderAddressList as sender,
       substr(m.Message_Preview, 1, 200) as preview
FROM Mail m
WHERE m.Message_NormalizedSubject LIKE '%Failure%'
   OR m.Message_NormalizedSubject LIKE '%NC-%'
   OR m.Message_NormalizedSubject LIKE '%Non-Conformance%'
ORDER BY m.Message_TimeReceived DESC;
```

## NCR Subject Pattern

Aconex NCR subject lines follow this format:

```
CGP-WTRAN-000186: (WF-000171) Failure to complete Electrical & Low Current
assessment works and submit compliant reports by the contractual deadline of
23/07/2026, coupled with unauthorized site abandonment and lack of professional
cooperation by SAMAYA...
```

The NCR number is embedded in the transmittal subject (e.g. WF-000171) and the CG's NCR reference (e.g. NC-1E0-015) appears in the CG's separate email or the Aconex attachment.

## CG Formal Notice Pattern

Separate from Aconex, CG sometimes sends direct "Formal Notice of Non-Response" emails:

```
Formal Notice of Non-Response – NCR No. MOC-MUS-CG-ASE-NC-1E0-0010
```

These come from CG consultants like `malrezeni@cg.com.sa` and reference an existing NCR number that Samaya hasn't responded to.

## Register Update Pattern

When processing NCR transmittals:

1. Assign a sequential NCR number: `NC-{Discipline}-{SEQ}` (e.g. NC-1E0-015)
2. Extract the date from the email timestamp
3. Identify the owner (MEP Lead for electrical, Site Manager for construction, etc.)
4. Link to existing PRR risk from the risk register
5. Add to `01_Registers/ncr_register.md` with Open status
6. Update `01_Registers/risk_register.md` dashboard if the NCR affects a PRR entry

## Example NCR Entry Format

```
||| NC-1E0-015 | 26-Jul-2026 | CG (CGP-WTRAN-000186) | Failure to complete Electrical
& Low Current assessment works by contractual deadline 23/07, unauthorized site abandonment,
lack of professional cooperation | Open | MEP Lead | — | PRR-MEP-02 |
```

## Pitfall: Preview Truncation

Aconex notification email previews are truncated to ~150 chars — not enough to see the full NCR scope. Always note the CGP-WTRAN-XXXXXX reference so the full document can be opened in Aconex.
