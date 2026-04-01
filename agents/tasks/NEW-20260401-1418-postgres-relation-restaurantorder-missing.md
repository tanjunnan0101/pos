# Postgres: relation "restaurantorder" does not exist

## Source

- **Service:** `pos-postgres` (`docker logs pos-postgres`)
- **UTC window:** ~**2026-04-01T14:04:28Z**–**14:16:58Z** (preflight digest window); representative hit **2026-04-01T14:06:14.819Z**.
- **Representative lines:**
  ```
  2026-04-01 14:06:12.000 UTC [44304] FATAL:  role "postgres" does not exist
  2026-04-01 14:06:14.819 UTC [44318] ERROR:  relation "restaurantorder" does not exist at character 32
  2026-04-01 14:06:14.819 UTC [44318] STATEMENT:  SELECT table_id, COUNT(*) FROM restaurantorder GROUP BY table_id HAVING COUNT(*)>=1 LIMIT 10;
  ```

**Context:** The **`FATAL: role "postgres" does not exist`** pattern is already documented and closed (**`agents/tasks/done/2026/03/26/CLOSED-20260326-1121-postgres-fatal-role-postgres-does-not-exist.md`** — stack uses **`POSTGRES_USER`** **`pos`**, not role **`postgres`**). The **`restaurantorder`** **`ERROR`** is a **separate** symptom: raw SQL against a relation name that does **not** match this codebase’s ORM/table naming (no **`restaurantorder`** identifier found under **`back/`** in a quick search). Likely ad-hoc client, wrong database, or an external script using an assumed schema.

## High-level instructions for coder

- Confirm the **actual** order-related table name(s) in **`models.py`** / migrations (e.g. quoted vs unquoted identifiers, `RestaurantOrder` vs snake_case).
- Search the repo (scripts, seeds, docs, third-party SQL) for **`restaurantorder`** or similar; if nothing, treat as **external mis-query** and optionally add a short **README** / **`docs/`** note on correct table names for operators who run SQL manually.
- If anything **in-repo** issues this **`STATEMENT`**, fix the query or align the migration/schema so the name exists — or document the correct replacement query.
- Correlate **timestamps** with host tools / IDE DB plugins if still reproducing locally (same window as **`postgres`** role **`FATAL`** suggests a misconfigured client session).
