# SysLeaders Database Schema — Full Mapping

## Entity Table Map

| Entity | Table | Purpose | Key Fields |
|--------|-------|---------|------------|
| 21 | `app_entity_21` | Projects | Rateeb = id 282, JN-Rateeb-Shop |
| 22 | `app_entity_22` | Tasks / BOQ Items | parent_id → project, 10 tasks for Rateeb |
| 25 | `app_entity_25` | Suppliers / Vendors | field_214=name, field_215=code |
| 26 | `app_entity_26` | RFQ / Quotations | field_284=project_name, field_285=code |
| 27 | `app_entity_27` | Technicians / Workers | field_241=name, field_242=job_title, field_243=phone |
| 28 | `app_entity_28` | Labor Time Records | field_254=date, field_255=worker_id, field_256=hours, field_257=rate |
| 47 | `app_entity_47` | Drawing Requests | field_573=name, field_574=code, field_575=description |
| 48 | `app_entity_48` | Samples | field_598=name, field_599=code |
| 49 | `app_entity_49` | Purchase Orders | field_622=PO#, field_623=date, field_625=type, field_626=description |
| 52 | `app_entity_52` | Invoices | field_682-685=invoice details |
| 53 | `app_entity_53` | Expenses | field_665-667=expense details |
| 54 | `app_entity_54` | Fleet Requests | field_674-678=fleet details |
| 57 | `app_entity_57` | Work Centers | field_721=name |
| 62 | `app_entity_62` | Subcontractor Orders | field_789-794=subcontract details |
| 63 | `app_entity_63` | Raw Materials | field_803=code, field_814-817=material details |
| 72 | `app_entity_72` | Delivery Notes | field_923-927=delivery details |
| 76 | `app_entity_76` | Products | field_1065=code, field_1067=qty |
| 77 | `app_entity_77` | Production Orders | field_1102=name, field_1104=description |
| 78 | `app_entity_78` | Inventory | field_1114-1118=inventory details |

## Relationship Tables (the glue)

| Table | Links |
|-------|-------|
| `app_related_items_21_28` | Project ↔ Labor Records |
| `app_related_items_22_28` | Task ↔ Labor Records |
| `app_related_items_27_28` | Worker ↔ Labor Records |
| `app_related_items_22_62` | Task ↔ Subcontractor Orders |
| `app_related_items_26_78` | RFQ ↔ Inventory |
| `app_related_items_76_78` | Product ↔ Inventory |
| `app_related_items_47_78` | Drawing Request ↔ Inventory |

## Entity 28 (Labor Time Records) — Full Field Map

| Column | Type | What It Holds |
|--------|------|---------------|
| `id` | int | Record ID |
| `parent_id` | int | Parent entity (0 = standalone, 282 = Rateeb project) |
| `parent_item_id` | int | Parent item reference |
| `linked_id` | int | Linked record |
| `date_added` | bigint | Unix timestamp when record was created |
| `date_updated` | bigint | Unix timestamp of last update |
| `created_by` | int | User ID who created |
| `sort_order` | int | Display order |
| `field_254` | bigint | **Date** (unix timestamp) |
| `field_255` | text | **Worker ID** (references entity_27) |
| `field_256` | text | **Hours worked** |
| `field_257` | text | **Rate per hour** |
| `field_262` | bigint | **Start time** (unix timestamp) |
| `field_263` | bigint | **End time** (unix timestamp) |
| `field_264` | float | **Quantity** |
| `field_267` | int | **Status** (19=active, 46=complete, 48=paid, 20=hold) |
| `field_969` | int | **Project reference** (175=default, 173/174=other) |
| `field_970` | int | **Task reference** |
| `field_1634` | varchar(64) | Additional field |
| `field_1637` | varchar(64) | Additional field |
| `field_2743` | varchar(64) | Additional field |
| `field_2744` | varchar(64) | Additional field |

## Entity 22 (Tasks/BOQ Items) — Key Fields

| Column | What It Holds |
|--------|---------------|
| `field_167` | BOQ Code (e.g. "5.2.1", "6.1.1") |
| `field_168` | Task Name (e.g. "Decorative steel structure tubes") |
| `field_169` | Quantity |
| `field_170` | Unit (SQM, rmtr, unit) |
| `field_171` | Rate per unit |
| `field_172` | Labor cost |
| `field_225` | Status |
| `field_233` | Progress (0-100) |
| `field_234` | Total Amount |

## Entity 27 (Technicians/Workers) — Key Fields

| Column | What It Holds |
|--------|---------------|
| `field_241` | Worker Name |
| `field_242` | Job Title / Trade |
| `field_243` | Phone Number |
| `field_246` | Notes |
| `field_265` | Status |
| `field_270` | Additional info |
| `field_1635` | Rate per hour |

## Entity 49 (Purchase Orders) — Key Fields

| Column | What It Holds |
|--------|---------------|
| `field_622` | PO Number (e.g. "PO00350") |
| `field_623` | PO Date (unix timestamp) |
| `field_625` | Type |
| `field_626` | Description |
| `field_627` | Status (true/false) |
| `field_637` | Supplier reference |
| `field_795` | Due date |
| `field_796` | Amount |

## How Cost Is Calculated

```
Labor Cost = field_256 (hours) × field_257 (rate)
```
Calculated **on-the-fly** — not stored in the database. Each record = one worker × one day × one task.

```
Section 5 Total = Labor (entity_28 sum) + Materials (entity_49 POs) + Other (entity_53 expenses)
```

## Data Flow

```
Project (21) ──parent_id──→ Tasks/BOQ (22)
     │                          │
     │                    app_related_items_22_28
     │                          │
     │                          ▼
     └──app_related_items_21_28──→ Labor Records (28) ←──app_related_items_27_28── Workers (27)
                                  
POs (49) ──parent_id──→ Project (21)
Invoices (52) ──parent_id──→ Project (21)
Expenses (53) ──parent_id──→ Project (21)
```

## Backup File Analysis

ALL backup files examined are **structure-only**:
- `sysleaders_samaya.sql` — CREATE TABLE only, no entity data
- `sysleaders_samaya2.sql` — CREATE TABLE only, no entity data
- `backup-7.15.2026_23-42-47_sysleaders.tar.gz` — Full cPanel backup, same structure-only SQL files
- `sysleaders_samaya2 (1).sql` — Has entity_28 data but from 2020-2021 (old factory records, not Rateeb)

The live data is ONLY on the server. A proper backup of `sysleaders_samaya` (the one with actual records) is needed.

## Live Data Extraction (Browser Method)

When API and database are blocked, use the browser to navigate the SysLeaders web app:

1. Login at `https://www.sysleaders.com/samaya/index.php?module=users/login`
2. Navigate to project: `index.php?module=items/info&path=21-282`
3. Use `browser_console` with `expression` to extract table data via JavaScript
4. The project page shows all subentities (Tasks, POs, Fleet, Delivery Notes, Labor) in a single scrollable view
5. Parse the extracted JSON to get worker names, dates, hours, rates, BOQ codes
