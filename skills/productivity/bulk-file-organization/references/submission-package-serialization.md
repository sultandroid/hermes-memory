# Submission Package Serialization

Reindexing a tender/RFP submission folder: assign contiguous serials, enforce English-only
filenames, keep one document per serial. The user does this repeatedly as a package nears
issue, so follow the conventions exactly.

## Naming convention (user's spec)

- `NN_English_Name.pdf` — two-digit zero-padded serial, underscore, English words only.
- **No project-name prefix** in the filename. Serial + descriptive English title is enough.
- **Compliance matrix is always `00_`** and goes first, ahead of everything else.
- The document's internal doc-ref (`RCRC-EXH-QLT-001`, `SMP-RCRC-TP-AR-001`) stays **inside**
the PDF — do not put the doc ref in the filename unless asked.
- Title Case-ish natural English, underscores for spaces: `04_Quality_Methodology.pdf`,
`08_BOQ_Reconciliation.pdf`, `09_Vendors_Subcontractors_List.pdf`.
- Never leave Arabic in a filename. Translate the Arabic title to English; keep the raw Arabic
only when it appears inside a shell path.

Typical serial order: 00 compliance matrix, 01 technical proposal, 02.. methodologies
(design mgmt, execution, quality, content), then team / programme / BOQ / vendors / payment /
SOW annexes.

## Procedure

1. **Enumerate in Python, never by shell glob.** List with `os.listdir('.')` and match by
   substring. Returned names are the ground truth. See the bidi pitfall below.
2. **Identify each document from its content, not its filename.** Arabic/truncated filenames are
   often ambiguous:

   ```bash
   pdfinfo "$f" | grep -Ei 'Title|Pages|CreationDate|Producer'
   pdftotext -l 1 "$f" -        # first-page text carries the internal doc ref + rev
   ```

   The first page of these Samaya packages carries `RCRC-EXH-XXX-001 | REV nn | 2026` — use that
   to map file → document → correct English title. Metadata Title is not reliable (macOS Quartz
   stamps it with the same Arabic name).
3. **Plan the full source→target mapping first and print it**, then execute. Resolve each source
   file to exactly one target; sort substring hits by name length and take the shortest so a
   broad substring cannot steal another file's match.
4. **Rename in two phases through temp names** — renumbering in place collides when a target
   name is currently held by another file in the set:

   ```python
   tmp=[]
   for i,(src,dst) in enumerate(plan):
       t=f'~tmp{i}~.pdf'; os.rename(src,t); tmp.append((t,dst))
   for t,dst in tmp: os.rename(t,dst)
   ```

5. **Re-scan before reporting.** OneDrive sync can materialise a new file mid-run (the user drops
   one in while you work). List the folder again, pick up anything new, assign it the next serial,
   and only then report. Treat "folder changed under me" as expected, not as an error.
6. **Re-serial means renumber contiguously, order preserved**: strip the existing `NN_` prefix
   from each file in current order and rewrite `f'{i:02d}_{body}'`. Same two-phase temp rename.
   No gaps, no duplicates, no reordering unless the user gives a new order.
7. **Confirm numbering decisions with `clarify` before renaming** when the folder is OneDrive
   (no undo) and there is a real choice — serial scheme, what to do with a duplicate copy. Offer
   the recommended order first.

## Bidi / Arabic filename pitfall

macOS Finder-displayed names carry invisible bidi control characters and are **truncated with
`…`** in some listing paths. A real filename can be:

```
\u200e\u202bمنهجية الجودة — معرض الهيئة المل…رياض | RCRC Quality Methodology\u202c\u200e.pdf
```

- Shell `for f in *.pdf` and string equality against a name you typed will **not** match it.
- `repr()`-printed names show the escapes; copy them from a Python listing, not from tool output.
- Matching by an ASCII substring that does survive (e.g. `'Design Management'`, `'QLT'`) is the
  robust approach. Match on the Latin half of the name, or on text extracted from the PDF.
- Verify at the end: flag any filename where `any(ord(c)>127 for c in f)` is true. The folder
  should be 100% ASCII after the pass.

## Duplicate detection in submission folders

Same document can arrive twice with **byte-different but text-identical** PDFs — a macOS Quartz
re-save (`Producer: ... Quartz PDFContext, AppendMode 1.1`) produces a different byte stream for
identical content. Byte md5 therefore reports "DIFF" when the documents are the same.

```python
import subprocess, hashlib
txt = subprocess.run(['pdftotext', f, '-'], capture_output=True, text=True).stdout
key = hashlib.md5(txt.encode()).hexdigest()   # compare text, not bytes
```

Disposition: **never delete.** Keep one as the live serial, rename the extra to
`_DUPLICATE_<Title>.pdf` at root as a flag, and tell the user. Deleting user files needs
explicit confirmation.

Also worth flagging to the user when found: serials that are **byte-identical to an earlier
package's copies** (compare md5 against the previous submission folder) — means that document was
carried over, not regenerated for this issue.

## Reporting back

State the full final serial list, then a short issues block: duplicates, carried-over documents,
files that appeared mid-run, and anything about to be deleted. Then offer the manifest
(`_MANIFEST.md` mapping serial → doc ref → rev) as an optional next step.
