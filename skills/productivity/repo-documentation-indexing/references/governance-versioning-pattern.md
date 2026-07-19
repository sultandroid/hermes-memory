# Governance Versioning Pattern

When a user asks for CHANGELOG.md, VERSION.md, or CONSTITUTION amendment tracking, use this pattern.

## CHANGELOG.md

Structured semver format with three sections:

```markdown
## [Unreleased]
### Added / Changed / Fixed
(Pending — next agent session)

## [1.0.0-beta] — YYYY-MM-DD
### Added — [Category]
- Item with description and rationale

## [0.1.0] — YYYY-MM-DD (Initial Repository)
### Added
- Core structure, governance, navigation
```

Group changes by category (Governance, Scripts, CI/CD, Documentation, Plans, etc.) under each version heading.

## VERSION.md

Component-level tracking table + phase completion table + governance amendment log:

| Component | Version | Status | Date |
|-----------|---------|--------|------|
| Repository | 1.0.0-beta | 🟢 100% Complete | YYYY-MM-DD |
| CONSTITUTION.md | 1.0 | ✅ Stable | YYYY-MM-DD |

| Phase | Name | Status | Completion |
|-------|------|--------|------------|
| Phase N | Name | ✅ Complete | 100% |
| **OVERALL** | | ✅ **Complete** | **100%** |

## CONSTITUTION Amendment Log

Replace a simple version/date table with:

| Amendment # | Date | Type | Change | Approver | Status |
|-------------|------|------|--------|----------|--------|
| 1.0 | YYYY-MM-DD | Initial | Repository creation & governance | Role | ✅ Active |
| 1.1 | YYYY-MM-DD | Enhancement/Enforcement | Specific change description | Agent | ✅ Active |

Plus: How to Propose Amendments (7-step procedure) and Last Review Date with monthly cadence.

## Source

Worked example in `aseer-museum-pm` repo: CHANGELOG.md (19 entries, 3 versions), VERSION.md (10 components, 4 phases, 5 amendments), CONSTITUTION.md Article X (7 amendments).
