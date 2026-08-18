# Pre-Signature NRS-Stamp Verification (Aseer SMP / design-lead stamped plans)

When the user sends a plan stamped by the Lead Designer (NRS) and says "review before signing" (راجع قبل التوقيع), verify the stamp is genuine and dated correctly BEFORE the user signs. Do not just read the PDF — cross-check the document's internal dates against the actual Outlook email chain.

## Workflow

1. **Extract PDF text** — `pdftotext -layout file.pdf smp.txt`; read the revision history (Document History table) and the lead-designer review appendix (e.g. "Appendix O - NRS Review Report").
2. **Verify the two critical compliance values** that have a history of being wrong (per repo CR sheets):
   - Waste diversion = **60%** (SBC 1001 Sec 8; ER 2.4D) — NOT 75% (Mostadam stretch)
   - Oddy aging = **14 days at 60°C** (SoW 1.5; ER 2.4D) — NOT 49-day
3. **Verify framing** — no Silver/Gold/Platinum "points-chasing" language; code-compliance framing with Mostadam as secondary trajectory. Role title should be "Sustainability Specialist" not "Manager".
4. **Verify the stamp visually** — extract the stamp image via pymupdf (`doc[i].get_images(full=True)`, find the large logo xref), run `vision_analyze`. NOTE: NRS's "stamp" is often just the corporate logo block (black text, no signature/date) — the actual acceptance lives in the Appendix O review report + the email.
5. **Cross-check the stamp/appendix date against the email chain** (the user's key question: "is the document date what we asked for?"):
   - Query Outlook SQLite: `SELECT Record_RecordID, datetime(Message_TimeReceived,'unixepoch','localtime'), Message_SenderList, Message_NormalizedSubject, Message_HasAttachment FROM Mail WHERE Message_NormalizedSubject LIKE '%<topic>%' ORDER BY Message_TimeReceived DESC;`
   - Read the FULL bodies via AppleScript (previews are capped at 255 chars — useless here):
     ```
     osascript -e 'tell application "Microsoft Outlook" to set theMsg to message id <ID>' \
                -e 'tell application "Microsoft Outlook" to return plain text content of theMsg' | tr '\r' '\n'
     ```
   - Build the request→reply timeline: date we asked NRS to sign vs date NRS returned the stamped copy. The stamped date must equal the day NRS actually replied, not the day we submitted.
6. **Look for unfilled placeholders** in the NRS review statement / review report — e.g. `[Doc Ref: AMA/SMP-01]` left as a bracket placeholder. Flag before signing.

## Known-issue findings from the worked example (SMP Rev01, 17-Aug-2026)
- Stamped date 17.08.26 matched the NRS email reply (Jim Richards, 18:29 same day) — correct, no date discrepancy.
- Page 3 "NRS Review Statement" had an unfilled placeholder `[Doc Ref: AMA/SMP-01]` and a wording oddity ("in accordance with the Client's (CG) instruction" — NRS is the Lead Designer, not the client). Flag both before signature.
- NRS "stamp" = logo block only (no handwritten signature); acceptance evidence = Appendix O ("No further comments", dated) + the email attachment.
