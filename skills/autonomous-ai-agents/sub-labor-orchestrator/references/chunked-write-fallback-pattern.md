# Chunked Write Fallback Pattern — Large Document Timeout Recovery

## Problem

`delegate_task` with Claude Code writing large files (>30KB) can timeout at 600s when the subagent's response payload exceeds the stream's capacity. A secondary failure mode: the **Hermes-to-subagent tool call** itself times out when `write_file` or the full response exceeds ~8K tokens in argument size.

This happened generating 15 project management documents for the RCRC Exhibition tender (June 2026): Batch 2 tasks (Mobilization Plan, Resource Plan, BEP) timed out at 600s while the subagent was writing a ~50KB file in one shot.

## Root Cause

The subagent (Claude Code via delegate_task) reads source files, generates content, and calls `write_file` with the complete document in a single argument. When the document body is >30KB (~8K tokens in JSON-serialized form), the stream carrying the tool result back to Hermes hits the token/byte limit and stalls. The terminal timeout (600s) fires before the stream finishes.

## Workaround: Chunked Write via section-by-section patch

Instead of having the subagent write the whole file, **build the document section by section** using `write_file` + `patch` from the orchestrator (you):

1. **Write the doc control block + section 1** with `write_file` (keep under ~4KB per call)
2. **Append each subsequent section** with `patch` (find a unique anchor string at the end of what's been written so far, replace with the new section appended)
3. **Repeat until the document is complete**

### Example: Building a Master Programme document

```python
# Step 1: Write header + sections 1-3 (~4.7KB)
write_file("25_MASTER_PROGRAMME.md", content="""# Title\n\n## 1. ...\n\n## 2. ...\n\n## 3. ...\n\nMILESTONES ...""")

# Step 2: Patch to add sections 4-7 (replace end-anchor with new content)
patch("25_MASTER_PROGRAMME.md", old_string="MILESTONES ...", new_string="MILESTONES ...\n\n## 4. ...\n\n## 5. ...")

# Step 3: Patch to add sections 8-end
patch("25_MASTER_PROGRAMME.md", old_string="## 7. ...", new_string="## 7. ...\n\n## 8. ...\n\n## 9. ...\n\n## Document Control")
```

Each `patch` call stays well under the 8K-token stream limit because only the delta is sent.

### For delegate_task specifically

When the subagent's write is too large:
1. The subagent's output gets truncated/timed out anyway — don't retry the same delegate_task
2. Instead, **do the writes yourself** on the orchestrator side
3. Use the subagent's partial output (if any arrived before timeout) as the starting point
4. Fill in remaining sections by writing them directly based on what you know from the SOW/ER/context

### When to use this pattern

| Signal | Action |
|--------|--------|
| delegate_task times out at 600s during file generation | Try the chunked write fallback |
| System says stream timeout (>8K tokens in arg) | Split across multiple write_file + patch calls |
| File being generated is >30KB (approx) | Preemptively use chunked pattern instead of one-shot write |

### When NOT to use this

- Small files (<10KB) — one-shot write works fine
- Binary files (Excel, images) — use terminal with Python/openpyxl instead
- The subagent already completed before timeout — the chunking is unnecessary overhead