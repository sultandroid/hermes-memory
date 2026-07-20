# Deemed-Approval Rule — Submittal Register

## Rule

Per ER §2.4.A, the PMC/CG has **14 calendar days** to review a submittal. If no response is received within that period, the submittal is **Deemed Approved (DA)**.

## Status Code

| Code | Meaning |
|------|---------|
| **DA** | Deemed Approved — CG silent >14 days per ER §2.4.A |

Add to the status codes legend in the submittal register:
```
> **Status codes:** A=Approved | B=Approved w/ comments | C=Revise & Resubmit | D=Disapproved | TBV=To Be Verified | **DA=Deemed Approved** (CG silent >14 days per ER §2.4.A)
```

## When to Apply

Any agent updating the submittal register should check every row where:
- `CG Response` column is empty or `—`
- `Submitted` date is >14 days before today
- `Code` is not already DA

## Note Format

```
CG silent N days (14-day review period per ER §2.4.A). Deemed approved.
```

## Retroactive Application

Scan the entire register on first activation. All submittals meeting the criteria get DA status immediately.

## Auto-Rule (Document Controller Dashboard)

The Document Controller lane at `10_Manager_Lanes/10_Document_Controller/dashboard.md` should have an Auto-Rules section:

| Rule | Trigger | Action |
|------|---------|--------|
| **Deemed Approval** | Submittal with no CG response >14 days after submission (per ER §2.4.A) | Auto-flag as **DA (Deemed Approved)** in submittal register. Update `last_updated` and log in decision log. |
| **Overdue Alert** | Submittal >10 days with no response | Flag for escalation in weekly coordination meeting. |

## Daily Cron Job

A daily cron job (`daily-manager-lanes`) runs at 7:00 AM KSA and:

1. Scans `01_Registers/submittal_register.md` for DA candidates
2. Marks them with `**DA**` code and note
3. Checks all 11 manager lane dashboards for staleness (>7 days)
4. Updates master dashboard timestamp
5. Logs overdue alerts (submittals >10d without response)
6. Git commit + push

## Source

- ER §2.4.A: "14 calendar days for PMC conformance review"
- DMP Rev C04 §3.4: Review cycle definition
- SoW §5.5: Submittal review procedure
