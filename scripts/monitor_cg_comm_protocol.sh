#!/bin/bash
# Monitor Mansour Alrezeni (CG) emails for direct communication with sub-consultants/subcontractors
# Runs daily, checks last 24h of emails from malrezeni@cg.com.sa

DB="$HOME/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite"

# Check if DB is accessible
if [ ! -f "$DB" ]; then
    echo "ERROR: Outlook DB not found"
    exit 1
fi

# Query: Mansour emails in last 24h where To includes non-Samaya/non-CG/non-PMC addresses
# (excluding MoC and A.AlAjmi which are legitimate)
sqlite3 "$DB" "
SELECT 'VIOLATION: ' || datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as time,
       m.Message_NormalizedSubject as subject,
       m.Message_ToRecipientAddressList as to_list,
       m.Message_CCRecipientAddressList as cc_list
FROM Mail m
JOIN folders f ON m.Record_FolderID = f.Record_RecordID
WHERE m.Message_TimeReceived >= strftime('%s', 'now', '-1 day', 'localtime')
  AND m.Message_SenderAddressList = 'malrezeni@cg.com.sa'
  AND (
       m.Message_ToRecipientAddressList LIKE '%@nissenrichardsstudio%'
    OR m.Message_ToRecipientAddressList LIKE '%@studiozna%'
    OR m.Message_ToRecipientAddressList LIKE '%@rawasin%'
    OR m.Message_ToRecipientAddressList LIKE '%@glasbau%'
    OR m.Message_ToRecipientAddressList LIKE '%@graphite%'
    OR m.Message_ToRecipientAddressList LIKE '%@namaa%'
    OR m.Message_ToRecipientAddressList LIKE '%@adeng%'
    OR m.Message_ToRecipientAddressList LIKE '%@evergreen%'
    OR m.Message_ToRecipientAddressList LIKE '%@acoustieg%'
    OR m.Message_ToRecipientAddressList LIKE '%@jocavi%'
    OR m.Message_ToRecipientAddressList LIKE '%@ame-ts%'
    OR m.Message_ToRecipientAddressList LIKE '%@transorient%'
  )
ORDER BY m.Message_TimeReceived DESC;
" 2>/dev/null

# Also check: non-Samaya senders emailing CG directly without Samaya in CC
sqlite3 "$DB" "
SELECT 'SUBCONTRACTOR-TO-CG: ' || datetime(m.Message_TimeReceived, 'unixepoch', 'localtime') as time,
       m.Message_SenderList as sender,
       m.Message_SenderAddressList as email,
       m.Message_NormalizedSubject as subject
FROM Mail m
WHERE m.Message_TimeReceived >= strftime('%s', 'now', '-1 day', 'localtime')
  AND m.Message_SenderAddressList NOT LIKE '%samayainvest%'
  AND m.Message_SenderAddressList NOT LIKE '%cg.com.sa%'
  AND m.Message_SenderAddressList NOT LIKE '%ace-mb%'
  AND m.Message_SenderAddressList NOT LIKE '%moc.gov.sa%'
  AND m.Message_SenderAddressList NOT LIKE '%noreply%'
  AND m.Message_SenderAddressList NOT LIKE '%aconex%'
  AND (m.Message_ToRecipientAddressList LIKE '%cg.com.sa%'
       OR m.Message_CCRecipientAddressList LIKE '%cg.com.sa%')
  AND (m.Message_CCRecipientAddressList NOT LIKE '%samayainvest%'
       AND m.Message_ToRecipientAddressList NOT LIKE '%samayainvest%')
ORDER BY m.Message_TimeReceived DESC;
" 2>/dev/null

echo "---END---"
