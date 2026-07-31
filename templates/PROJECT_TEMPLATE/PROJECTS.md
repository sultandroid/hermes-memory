# PROJECTS — <PROJECT_NAME>

> Project-level index. Mirrors the hub `PROJECTS.md` row + adds project-local pointers (registers, submittals, key dates).

## Hub Reference

| Field | Value |
|---|---|
| Hub `PROJECTS.md` row | <link or section> |
| Type | WORK / CONSULTING / PERSONAL |
| Hub `AGENTS.md` §3 | route via this project repo |

## Project Status

| Milestone | Date | Status |
|---|---|---|
| NTP | | |
| DD complete | | |
| IFC issued | | |
| Construction start | | |
| Substantial completion | | |
| Handover | | |

## Registers (paths within this repo)

| Register | Path | Last updated |
|---|---|---|
| Risk | `_Project_Memory/registers/risk.xlsx` | |
| LN | `_Project_Memory/registers/ln.xlsx` | |
| Submittal log | `_Project_Memory/registers/submittals.xlsx` | |
| RFI | `_Project_Memory/registers/rfi.xlsx` | |
| Drawing register | `_Project_Memory/registers/drawings.xlsx` | |

## Project Memory

See `_Project_Memory/PROJECT_MEMORY.md` for project-specific facts and lessons learned.

## Key Stakeholders

See `AGENTS.md` §3.

## Quick Commands

```bash
# Sync this project
cd <PROJECT_LOCAL_PATH>
git pull --no-rebase

# Open project in Hermes
hermes --project <PROJECT_NAME>

# Daily health check
bash ~/hermes-memory/scripts/hub_health_check.sh
```
