# Download all my data

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/96

## Problem / goal

Tenant owners need **Settings** controls for **data lifecycle and ownership**: export/download all tenant data; a clearly marked **danger zone** to delete all tenant data; and a way to **promote another user to co-owner** of the restaurant. Separately, the team wants to **purge demo tenants** (ids **2, 3, 4, 5, 6, 7**) so those restaurants can be cleaned up. Align export/delete semantics with privacy expectations, role permissions, and any existing tenant/user models; see `docs/` for auth, tenant, and GDPR-style data handling if present.

## High-level instructions for coder

- Design **export “download all my data”** (scope: one tenant; formats; async job vs direct download; what entities are included — orders, reservations, users, settings, files).
- Add **Settings UI** for **delete all tenant data** with strong **danger zone** styling, confirmation, and irreversibility warnings; ensure only appropriate roles can trigger it and audit/log if the product already supports it.
- Implement **additional owner** (or co-owner) assignment from Settings with clear rules (limits, self vs other users, email lookup).
- Plan **one-off or scripted cleanup** for demo tenants **2–7** (coordinate with DB/migrations/seeds); do not conflate with production safety — use explicit tenant ids and safeguards.
- Add or extend **tests/smoke** for the new flows where the repo pattern allows (API + critical UI paths).

## Coder notes (2026-03-25 UTC)

- **Export:** synchronous ZIP (`tenant-export.json`); direct download (no job queue). Tenant row: `stripe_secret_key`, `revolut_merchant_secret`, `smtp_password` → `[REDACTED]`; users omit `hashed_password` / `otp_secret`.
- **Purge:** owner-only; `confirm_tenant_name` must match tenant name (trimmed). DB cascade in `app/tenant_lifecycle.py`; upload dirs `uploads/{tenant_id}/` and `uploads/providers/{token}/` removed via `BackgroundTasks` after response (post-commit).
- **Co-owner:** existing `PUT /users/{id}` already allows owner to set `role: owner`; **Users** UI now includes **Owner** in the role dropdown when an owner edits another user (not when creating users).
- **Demo cleanup:** `python -m app.seeds.purge_demo_tenants` with **`DEMO_PURGE_CONFIRM=1`** only; deletes tenants **2–7** if present.
- **Logging:** `logger.warning` on purge with `tenant_id`, `operator_user_id`, `operator_email`.

## Testing instructions

### What to verify

- Owner: `GET /tenant/data-export` → `application/zip` with `tenant-export.json`; payload includes `tenant`, `users`, `orders`, etc.; redacted secrets in tenant.
- Admin: `403` on `/tenant/data-export` and `/tenant/purge`.
- Purge: wrong name → `400`; correct name → tenant and tenant users removed; app signs out and navigates to `/login`.
- Owner editing another user on `/users` can set role to **Owner**; create-user flow still excludes Owner.
- Optional: demo script only runs with env flag and targets ids 2–7.

### How to test

- Backend:  
  `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python3 -m pytest tests/test_tenant_lifecycle.py -v`
- Frontend:  
  `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` (no Angular/TS build errors after changes)
- Smoke:  
  `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`
- Manual (destructive): use a **throwaway** tenant only — Settings → **Data & privacy** → type business name → purge; or exercise export only on production-like data.

### Pass/fail criteria

- `tests/test_tenant_lifecycle.py` all pass; landing smoke passes; manual export opens ZIP and valid JSON; purge test only on disposable data.
