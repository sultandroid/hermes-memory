# Appending Markdown Register / Action-Item Rows — terminal `&` guard trap

**Problem (hit 2026-08-22):** When appending rows to markdown registers (`00_Status/action_items.md`, `01_Registers/*.md`) via a terminal heredoc:

```bash
cat >> 00_Status/action_items.md << 'EOF'
...row with FF&E and Inv & AC text...
EOF
```

any `&` in the heredoc body trips the terminal tool's backgrounding guard and the **whole command is rejected** with:

```
Foreground command uses '&' backgrounding. Use terminal(background=true)...
```

This is a shell-guard rejection, NOT a file/OneDrive/syntax issue. It happens even though the `&` is inside a quoted heredoc body where the shell itself would treat it as literal text.

**Why it's a trap:** register and action-item text is full of `&` ("FF&E", "Inv & AC", "design & fabrication", "C&D waste"). You'll hit it almost every time you append a realistic action item. Re-typing with backslash-escapes (`\&`) is fiddly and doesn't always satisfy the guard.

**Fix — use the `patch` tool instead:**
1. `patch` (replace mode) on the file with:
   - `old_string` = the current last row anchor line (must be unique — pick a distinctive tail row)
   - `new_string` = `old_string + "\n" + new_row`
2. Append one row per `patch` call (or combine multiple new rows after a single anchor).

**Alternative:** write the new rows to a temp file with `write_file`, then `cat temp >> target.md` (the `cat` command itself has no `&`).

**Rule of thumb:** if the appended content is anything but plain alphanumeric prose, prefer `patch` for markdown-register appends — it sidesteps the guard entirely and is one tool call.

## Related: pipe-prefix integrity on markdown row inserts
Some registers nest rows by leading pipe count (`||`, `|||`, `||||`). When inserting a new row by replacing an anchor, verify the anchor's leading-pipe count is unchanged in the diff — `patch` can sometimes shift it, corrupting the register's table nesting. Re-read the anchor line after the patch and restore its pipe count if it drifted.
