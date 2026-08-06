#!/bin/bash
# CG Communication Protocol Monitor
# Run as daily cron to detect PL-0018 Sec 12.6 violations
#
# Checks:
# 1. CG emails to specialist domains (NRS, ZNA, Rawasin, Glasbau, AD Eng, etc.)
# 2. Non-Samaya senders emailing CG without Samaya in CC
#
# Output: JSON summary to stdout. Empty = no violations.

DB="/Users/mohamedessa/Library/Group Containers/UBF8T346G9.Office/Outlook/Outlook 15 Profiles/Main Profile/Data/Outlook.sqlite"
LOOKBACK_DAYS=1

if [ ! -f "$DB" ]; then
  echo '{"error":"Outlook DB not found","status":"skip"}'
  exit 0
fi

# Check 1: CG emailing specialists directly
VIOLATIONS=$(sqlite3 "$DB" "
SELECT json_object(
  'type', 'cg_to_specialist',
  'id', m.Record_RecordID,
  'received', datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
  'sender', m.Message_SenderList,
  'subject', m.Message_NormalizedSubject,
  'to_list', m.Message_ToRecipientAddressList,
  'cc_list', m.Message_CCRecipientAddressList
)
FROM Mail m
WHERE m.Message_TimeReceived >= strftime('%s', 'now', '-${LOOKBACK_DAYS} days', 'localtime')
  AND m.Message_SenderAddressList LIKE '%cg.com.sa%'
  AND (m.Message_ToRecipientAddressList LIKE '%@nissenrichards%'
       OR m.Message_ToRecipientAddressList LIKE '%@studiozna%'
       OR m.Message_ToRecipientAddressList LIKE '%@rawasin%'
       OR m.Message_ToRecipientAddressList LIKE '%@glasbau%'
       OR m.Message_ToRecipientAddressList LIKE '%@adeng%'
       OR m.Message_ToRecipientAddressList LIKE '%@graphite%'
       OR m.Message_ToRecipientAddressList LIKE '%@namaa%'
       OR m.Message_ToRecipientAddressList LIKE '%@evergreen%'
       OR m.Message_ToRecipientAddressList LIKE '%@acoustieg%'
       OR m.Message_ToRecipientAddressList LIKE '%@jocavi%'
       OR m.Message_ToRecipientAddressList LIKE '%@ame-ts%'
       OR m.Message_ToRecipientAddressList LIKE '%@transorient%')
ORDER BY m.Message_TimeReceived DESC;
" 2>/dev/null)

# Check 2: Specialists emailing CG without Samaya in CC
VIOLATIONS2=$(sqlite3 "$DB" "
SELECT json_object(
  'type', 'specialist_to_cg',
  'id', m.Record_RecordID,
  'received', datetime(m.Message_TimeReceived, 'unixepoch', 'localtime'),
  'sender', m.Message_SenderList,
  'subject', m.Message_NormalizedSubject,
  'to_list', m.Message_ToRecipientAddressList,
  'cc_list', m.Message_CCRecipientAddressList
)
FROM Mail m
WHERE m.Message_TimeReceived >= strftime('%s', 'now', '-${LOOKBACK_DAYS} days', 'localtime')
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
" 2>/dev/null)

# Build output
RESULTS='[]'
if [ -n "$VIOLATIONS" ]; then
  RESULTS=$(echo "$VIOLATIONS" | jq -s '.' 2>/dev/null || echo "[]")
fi
if [ -n "$VIOLATIONS2" ]; then
  V2=$(echo "$VIOLATIONS2" | jq -s '.' 2>/dev/null || echo "[]")
  RESULTS=$(echo "$RESULTS" "$V2" | jq -s 'add' 2>/dev/null || echo "[]")
fi

echo "$RESULTS"
