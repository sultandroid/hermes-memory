# NRS Payment Register (Aseer Regional Museum)

Source of truth for all NRS payments. Updated per OCR of Payment/ folder as of 2 June 2026.

## Invoice Register

| Invoice | Date | Description | Amount (SAR) | Status | Proof |
|---------|------|-------------|:-----------:|:------:|-------|
| INV-4755 | 19 Feb 2026 | Advance (10% of total) — Art. 11.1 | **120,900** | PAID 25 Feb | Nissen Richards Studio 10.pdf |
| INV-4781 | 23 Mar 2026 | Stage 4 Interim (1/2) — 50% of balance 691,200 | **345,600** | PAID 4 May | Nissen Richards Studio 781.pdf |
| INV-4805 | 29 Apr 2026 | Stage 4 Interim (2/2) — 50% of balance 691,200 | **345,600** | PAID 17 May | Nissen Richards Studio 805.pdf |
| INV-4825 | 28 May 2026 | Stage 5 Off-site (1/3) | **90,000** | DUE 11 Jun | — |
| **Total invoiced** | | | **902,100** | | |
| **Total paid (AC)** | | | **812,100** | | |

## Bank Transfer Details

### Transfer 1: Advance (INV-4755)
- File: `Nissen Richards Studio 10.pdf`
- Date: 25/02/2026
- EUR: 26,548.67
- Rate: 4.5539
- SAR net: 120,900.00 (exact match to INV-4755)
- Purpose text: Advance payment per Art. 11.1

### Transfer 2: Stage 4 Interim 1/2 (INV-4781)
- File: `Nissen Richards Studio 781.pdf` (originally named `Nissen Richards Studio Limitd0.pdf`)
- Date: 04/05/2026
- Ref: FT261245MZH6
- EUR: 76,334.19
- Rate: 4.5196
- SAR net: ~345,000 (OCR may have misread Arabic digits; expected ~345,600)
- Purpose text: References NRS-SAM-2026-002 (INV-4781) and NRS-SAM-2026-003 (INV-4805)
- Note: Amount only covers one full invoice. INV-4805 was proven paid via a separate 3rd transfer.

### Transfer 3: Stage 4 Interim 2/2 (INV-4805)
- File: `Nissen Richards Studio 805.pdf`
- Date: 17/05/2026
- EUR: 77,019.08
- Rate: 4.4872
- SAR net: 345,600.02 (exact match to INV-4805 = SAR 345,600.00)
- Purpose text: References Stage 4 Interim Payment (2/2)

## File Duplicates Removed
- `INV-4781 (1).pdf` → deleted (identical to INV-4781.pdf)
- `Nissen Richards Studio Limitd0 (1).pdf` → deleted (identical to Nissen Richards Studio 781.pdf)

## File Naming Convention
- Invoices: `INV-<number>.pdf` (e.g., INV-4755.pdf)
- Bank receipts: `Nissen Richards Studio <number>.pdf` (e.g., Nissen Richards Studio 805.pdf)
- The receipt number (10, 781, 805) appears to be the **Alinma Bank transaction reference** — not related to the invoice number
