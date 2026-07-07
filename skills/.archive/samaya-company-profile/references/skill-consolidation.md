# Skill Consolidation Note

Three skills currently cover the same class of work (Samaya Factory profile website):

| Skill | Description | Status |
|---|---|---|
| `samaya-company-profile` | Build, design, deploy — umbrella | **Active** |
| `samaya-factory-profile` | Maintain and update | Overlap — merge into umbrella |
| `samaya-profile-editorial` | Edit, redesign, deploy | Overlap — merge into umbrella |

The `samaya-company-profile` skill is the broadest umbrella and should be the single source of truth for all profile work. The other two are session-specific spinoffs that duplicate its content.

**Next step for curator**: delete `samaya-factory-profile` and `samaya-profile-editorial` (with `absorbed_into="samaya-company-profile"`) once confirmed no cron jobs reference them.
