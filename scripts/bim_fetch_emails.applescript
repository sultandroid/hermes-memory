-- BIM EMAIL PIPELINE v2.1 — Fetch recent emails from an Outlook folder
-- Usage: osascript bim_fetch_emails.applescript "Inbox" 50
on run argv
	set theFolderName to item 1 of argv
	set maxN to (item 2 of argv) as integer
	set out to ""
	tell application "Microsoft Outlook"
		try
			set f to mail folder theFolderName
		on error
			return "ERR|folder_not_found|" & theFolderName
		end try
		try
			set allMsgs to every message of f
		on error
			return "ERR|cannot_fetch|" & theFolderName
		end try
		set total to count of allMsgs
		if total = 0 then return ""
		set startIdx to 1
		if total > maxN then set startIdx to total - maxN + 1
		repeat with i from startIdx to total
			set m to item i of allMsgs
			try
				set msgId to id of m as string
			on error
				set msgId to "?"
			end try
			try
				set s to sender of m
				set sn to name of s
				set se to address of s
			on error
				set sn to "?"
				set se to "?"
			end try
			try
				set tr to time received of m as string
			on error
				set tr to "?"
			end try
			try
				set subj to subject of m
			on error
				set subj to "?"
			end try
			try
				set bdy to plain text content of m
				if (length of bdy) > 5000 then set bdy to (text 1 thru 5000 of bdy) & "...[TRUNCATED]"
			on error
				set bdy to "(no body)"
			end try
			set out to out & "===EMAIL===" & linefeed
			set out to out & "ID:" & msgId & linefeed
			set out to out & "FROM:" & sn & " <" & se & ">" & linefeed
			set out to out & "DATE:" & tr & linefeed
			set out to out & "SUBJ:" & subj & linefeed
			set out to out & "BODY:" & linefeed & bdy & linefeed
			try
				set atts to every attachment of m
				repeat with a in atts
					set out to out & "ATT:" & name of a & linefeed
				end repeat
			end try
			set out to out & "===END===" & linefeed & linefeed
		end repeat
		return out
	end tell
end run
