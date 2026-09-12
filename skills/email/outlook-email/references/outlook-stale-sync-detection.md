# Outlook Stale-Sync Detection — check freshness BEFORE reporting on email

## Rule

On every "check the emails / triage my inbox" request, establish **how fresh the local copy is**
before summarising anything. A local Outlook DB that stopped syncing will happily return a
complete-looking set of messages that ends days ago. Presenting that as today's inbox is the worst
failure mode in this workflow — it reads as "no new mail" when the truth is "we cannot see new mail".

## Step 1 — freshness check (always first)

```bash
DB=~/Library/Group\ Containers/UBF8T346G9.Office/Outlook/Outlook\ 15\ Profiles/Main\ Profile/Data/Outlook.sqlite

stat -f '%Sm  %N' "$DB"            # mtime == last successful local sync. NOT the current time.
sqlite3 "$DB" "select date(Message_TimeReceived,'unixepoch','localtime') d, count(*) n,
  sum(case when Message_ReadFlag=0 then 1 else 0 end) unread
  from Mail where Message_TimeReceived > strftime('%s','2026-08-28') group by d order by d;"
sqlite3 "$DB" "select count(*) from Mail;"
date '+%Y-%m-%d %H:%M'
```

Interpretation: compare the newest `Message_TimeReceived` day **and** the DB mtime against today.
A gap of more than one day = the client has stopped syncing. Lead the answer with that fact and the
number of days stale; only then describe the content.

## Step 2 — cross-check with independent sources

Never conclude "no new mail" from a single source.

```bash
# AppleScript inbox count. 0 here while Mail holds thousands of rows = client desynced, NOT empty.
osascript -e 'tell application "Microsoft Outlook" to return "inbox: " & (count of messages of inbox)'

# .eml cache newest files, per-folder pesf_* dirs
cd ~/Library/Group\ Containers/UBF8T346G9.Office/Outlook/Outlook\ 15\ Profiles/Main\ Profile
find pesf_* -name '*.eml' -print0 | xargs -0 stat -f '%Sm|%N' | sort -r | head -5

# client telemetry / service logs keep ticking even while mail is frozen
find . -name 'FileSystemStatisticsTelemetry.bin' -o -name 'HxStore.hxd' -print0 | xargs -0 stat -f '%Sm|%N'
```

A disagreement between sources (DB frozen but AppleScript returning 0, or telemetry files fresh
while mail is frozen) is itself the diagnosis: the client is running but its mail pipeline is not.

## Step 3 — confirm the sync failure from the client's own service logs

```bash
cd ~/Library/Group\ Containers/UBF8T346G9.Office/Outlook/Outlook\ 15\ Profiles/Main\ Profile/Osa
d=$(ls -td OutlookServiceApiLogs_* | head -1); echo "$d"

# dominant HTTP status among error responses
for f in "$d"/*.err.res.xmlgz; do gunzip -c "$f" 2>/dev/null \
  | grep -o '<HttpStatusCode>[0-9]*</HttpStatusCode>'; done | sort | uniq -c | sort -rn

# read one full error response: command, backend target, status
f=$(ls -t "$d"/*RedeemImapCredentials*.err.res.xmlgz | head -1)
gunzip -c "$f" | head -c 1500
```

Look for `<CommandId>RedeemImapCredentials</CommandId>` or
`<CommandId>RedeemForCloudCacheToken</CommandId>` together with:

```
<HttpStatusCode>503</HttpStatusCode>
x-backendhttpstatus: 503,503
x-calculatedfetarget: <backend>.internal.outlook.com
```

That combination = the auth/credential redeem is failing **server-side** at Microsoft. Mail never
lands in the local store, so every downstream query is stale. `65535` also appears and is a local
"no response" marker for the same failing commands.

The log directory name encodes its creation date (`OutlookServiceApiLogs_<YYYY-MM-DD>-<HH>_<hash>`);
the files inside are named with epoch-like ids, so sort by mtime, not by name.

## Step 4 — report and hand off

This is not repairable by an agent. Deliver:

1. Last successful sync timestamp and the age in days.
2. Total message count + which folder stopped at what date (map folder IDs to names first — see the
   `Folders` table note below).
3. The 503 evidence (command + status + backend host).
4. The action for the user: re-authenticate the account from Outlook (dismiss/sign in on the
   "account needs attention" banner, or sign out and back in), then escalate to Microsoft 365
   support if 503 persists.

Then offer to re-check once syncing resumes rather than ending the thread blind.

## Reading the mail despite a frozen sync

The stale DB is still the source of truth for everything that *did* arrive. Summarise what is there,
clearly labelled with the cutoff date. Filter out machine noise to keep it useful:

```bash
sqlite3 -separator ' | ' "$DB" "
select date(Message_TimeReceived,'unixepoch','localtime'),
       substr(Message_SenderList,1,28),
       substr(replace(Message_NormalizedSubject,char(10),' '),1,65)
from Mail
where Message_TimeReceived > strftime('%s','2026-09-01')
  and Message_SenderList not like '%Erp-Samaya%'
  and Message_SenderList not like '%Power Automate%'
order by Message_TimeReceived desc limit 60;"
```

For project mail, narrow to the correspondence sources rather than paging everything:

```sql
and (lower(Message_SenderList) like '%cg.com%'
  or lower(Message_SenderList) like '%nissenrichards%'
  or lower(Message_SenderList) like '%adeng%'
  or lower(Message_SenderList) like '%aconex%'
  or Message_NormalizedSubject like '%MOC-MUS-ASE%')
```

## Map folder IDs to names before reporting

`Mail.Record_FolderID` is a numeric id; folder names live in the `Folders` table. Always join — never
report a bare id to the user.

```bash
sqlite3 -header -column "$DB" "select f.Record_RecordID fid, substr(f.Folder_Name,1,34) name, m.n,
  date(max(x.Message_TimeReceived),'unixepoch','localtime') newest
from Folders f
join (select Record_FolderID, count(*) n from Mail group by Record_FolderID) m
  on m.Record_FolderID = f.Record_RecordID
left join Mail x on x.Record_FolderID = f.Record_RecordID
where m.n > 20 group by f.Record_RecordID order by m.n desc limit 16;"
```

`newest` per folder is the fastest way to spot a folder that stopped receiving before the rest.

## Account state

```bash
sqlite3 -header -column "$DB" "select Account_Name, Account_IsAccountOffline as Offline,
  Account_IsMigrated as Migrated from AccountsMail;"
```

`Offline = 0` while mail is not advancing points at the server-side redeem failure above, not a
local "work offline" toggle.
