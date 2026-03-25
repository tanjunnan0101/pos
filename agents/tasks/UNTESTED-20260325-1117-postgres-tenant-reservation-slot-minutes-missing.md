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

## Coder notes (2026-03-25)

- **Origin of `SELECT`:** No `reservation_slot_minutes` string existed in this repo before this change; the statement may come from an external SQL client, an unreleased branch, or another service. The ORM path in `main.py` loads full `Tenant` rows, so it would not emit that two-column projection.
- **Resolution:** Added migration `20260325120000_add_tenant_reservation_slot_minutes.sql`, `Tenant` / `TenantUpdate` field, `PUT /tenant/settings` validation (5–120 or ≤0 to clear), and wired public/staff slot grids to `_effective_reservation_slot_minutes` (null → 15). Staff UI: Settings → Reservations (i18n en/es/de/fr/ca).
- **`POST /reservations` 400:** Not tied to this column in current code; 400 remains possible for validation (date/time, opening hours, capacity). Postgres errors for the missing column are addressed by the migration.

---

## Testing instructions

### What to verify

- Migrations apply; `SELECT timezone, reservation_slot_minutes FROM tenant WHERE id=1` succeeds on PostgreSQL.
- Public booking week grid and next-available still return 200; optional: set `reservation_slot_minutes` to 30 and confirm offered times align to 30-minute steps.
- Settings save/load includes the new field; Angular build is clean.

### How to test

- From repo root (dev compose):  
  `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec -T back python -m app.migrate`  
  `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec -T db psql -U pos -d pos -c "SELECT timezone, reservation_slot_minutes FROM tenant WHERE id=1;"`  
  `curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:4202/api/reservations/book-week-slots?tenant_id=1&party_size=2"`
- Frontend: `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` (no TS/NG errors).  
  `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`
- Optional Puppeteer: `node front/scripts/debug-reservations-public.mjs` (with `BASE_URL` if not default) after changing slot minutes.

### Pass/fail criteria

- **Pass:** Schema version includes `20260325120000`; the SQL `SELECT` above returns no error; `book-week-slots` returns 200; front logs show successful bundle generation; `test:landing-version` exits 0.
- **Fail:** Migration errors, missing column, 5xx on reservation public endpoints, or Angular compile errors in front logs.
