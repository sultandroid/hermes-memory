# <PROJECT_NAME>

> One-line description of the project. <Client, scope, timeline>.

## Type

**WORK** | **CONSULTING** | **PERSONAL** — see `AGENTS.md` §1.

## Quick Start

```bash
git clone https://github.com/sultandroid/<REPO_NAME>.git
cd <REPO_NAME>

# Read the project contract
cat AGENTS.md

# Check project memory
cat _Project_Memory/PROJECT_MEMORY.md

# Pull latest hub identity (one-time)
cd ~/hermes-memory && git pull --no-rebase
```

## Contents

| Path | What |
|---|---|
| `AGENTS.md` | Machine-readable project contract (read first) |
| `PROJECTS.md` | Project-level index (mirrors hub) |
| `_Project_Memory/PROJECT_MEMORY.md` | Project-specific facts and lessons |
| `00_Admin/` | Charter, contracts, doc codes |
| `01_CLIENT_INPUTS/` | Client-supplied (read-only) |
| `02_Submittals/` | Outgoing submittals |
| `03_Design/` | Design files by phase |
| `99_Templates/` | Reusable templates |

See `AGENTS.md` §4 for the full folder structure.

## Sync Model

This project is **one layer** of a two-layer system:
- **Hub** = `sultandroid/hermes-memory` (identity + skills + project *index*)
- **Project** = this repo (state + deliverables + project memory)

Cross-project facts go to hub. Project-specific facts stay here.

## Contact

Eng. Mohamed Sultan — Technical Office Manager — sultan@samayainvest.com
