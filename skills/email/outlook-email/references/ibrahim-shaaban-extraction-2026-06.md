# Session Reference: Ibrahim Shaaban Email Extraction

## Emails searched for Sister Companies projects (Jun 2026)

Sender: i.shaaban@samayainvest.com (IBRAHIM MUSTAFA SHAABAN)
Account: sultan@samayainvest.com

### Tayyiba_Gifts_Jabal_Noor (8 emails with attachments)
- 34500 — عرض سعر تنفيذ متجر هدايا طيبة معالم جبل عمر (also contained: Ice Coffee file + Qahwatna files as attachments)
- 33140, 2601, 2996, 3003, 3004, 3007, 3016 — same subject thread

### Holy_Quran_Store (4 emails with attachments)
- 2503 — مستخلص متجر القرأن
- 2504 — طلب اعتماد مستخلص نهائي متحف القرآن الكريم
- 2505 — اعتماد عرض سعر الأعمال الإضافية بمتحف القرآن
- 7530 — مستخلص رقم (3) لمتحف القرآن

### Khair_Al_Khalq_Museum_Store (9 emails with attachments)
- 2339 — عينه لمتحف خير الخلق
- 2514 — متجر خير الخلق (.xls attachment)
- 3419, 3420, 3437, 3438, 3450, 3451, 3581 — various procurement

### Hira_Cafe (2 emails with attachments)
- 2336 — استعاضة فواتير نقل وتركيب غار حراء
- 11120 — عقد رقم 66 - اعمال رخام - مقهى حراء (signed contract PDF)

## AppleScript Patterns Used

### Project grouping extraction
Each project got its own AppleScript block extracting all attachments from its email IDs into a project-named temp folder, then organized by file name into Sister_Companies/ directories.

### Date conversion
Outlook stores timestamps as Unix epoch. Convert with:
`datetime(Message_TimeReceived, 'unixepoch')`
