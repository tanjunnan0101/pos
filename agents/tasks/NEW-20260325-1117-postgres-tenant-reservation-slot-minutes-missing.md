# Postgres: missing column `reservation_slot_minutes` on `tenant`

## Source

- **Service:** `pos-postgres` (Docker).
- **UTC:** `2026-03-25T11:06:39.512Z`.
- **Representative lines:**
  - `ERROR:  column "reservation_slot_minutes" does not exist at character 18`
  - `STATEMENT:  SELECT timezone, reservation_slot_minutes FROM tenant WHERE id=1;`

**Context:** Same window on `pos-back` shows reservation traffic (`GET /reservations/...`, `POST /reservations` returning **400**). Repo-wide search (host tree + `pos-back` container) did not find the string `reservation_slot_minutes`; current `Tenant` model uses other reservation timing fields (e.g. `reservation_average_table_turn_minutes`) but not this column name.

## High-level instructions for coder

- Identify which process issued the `SELECT` (application code path, ad-hoc client, or another service) and whether it is reproducible.
- Align persistence with intent: either add a proper migration + `Tenant` field if the feature is real, or remove/replace the query if the column was renamed or never shipped.
- If the failure correlates with `POST /reservations` **400**, trace that handler and any raw SQL / partial row loads for `tenant`.
