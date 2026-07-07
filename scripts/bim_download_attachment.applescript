-- BIM EMAIL PIPELINE v2.1 — Download attachment from Outlook message
-- Usage: osascript bim_download_attachment.applescript "Inbox" "msgId" "attachmentName" "/output/path"
on run argv
	set theFolder to item 1 of argv
	set theMsgId to item 2 of argv
	set theAttName to item 3 of argv
	set theOutPath to item 4 of argv
	tell application "Microsoft Outlook"
		try
			set f to mail folder theFolder
			try
				set m to message id theMsgId of f
				set atts to every attachment of m
				repeat with a in atts
					if name of a is theAttName then
						save a in theOutPath
						return theOutPath
					end if
				end repeat
			on error
				return "NOT_FOUND"
			end try
		on error
			return "NOT_FOUND"
		end try
	end tell
	return "NOT_FOUND"
end run
