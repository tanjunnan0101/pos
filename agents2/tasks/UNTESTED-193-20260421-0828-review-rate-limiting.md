# Review rate limiting

## GitHub Issues

- **Issue:** https://github.com/satisfecho/pos/issues/193
- **193**

## Problem / goal

Many new backend endpoints were added recently. Ensure **rate limiting** is applied consistently across the API to reduce overload and brute-force risk. Align implementation with documented limits and add coverage where endpoints are missing protection.

Relevant docs: **`docs/0020-rate-limiting-production.md`** (limits, Redis, headers), **`docs/testing.md`** (pytest disables rate limits; `npm run test:rate-limit`), **`docs/README.md`** index entry for rate limits.

## High-level instructions for coder

- Read **`docs/0020-rate-limiting-production.md`** and map how limits are enforced in **`back/`** (middleware, decorators, Redis, per-route config).
- Inventory public and sensitive routes (auth, registration, payments, uploads, admin, public menu/booking APIs) and confirm each category has appropriate limits per the doc (or justify any intentional exception).
- Implement missing rate limits on new or uncovered endpoints; keep behaviour consistent with existing patterns (avoid duplicating logic — reuse shared helpers).
- Run **`npm run test:rate-limit`** (from `front/`, with stack up) and any existing backend tests touching auth; ensure tests still pass (`RATE_LIMIT_ENABLED` behaviour in **`back/tests/conftest.py`** remains correct).
- If you change limits or scope, update **`docs/0020-rate-limiting-production.md`** so production operators and testers stay aligned.

## Implementation summary (coder)

- Added **`back/app/rate_limits.py`**: central SlowAPI `limiter`, IP/user/payment-order key helpers, `register_rate_limit_exception_handler`, `admin_user_limit()`, `public_menu_ip_limit()`.
- **`main.py`** imports limiter from `rate_limits`; public discovery endpoints (`/public/tenants`, legal URLs, tenant detail, reservation-book-zones) and **`GET /internal/validate-table/{table_token}`** now use **`public_menu_ip_limit()`** (30/min per IP, aligned with public menu).
- Included routers (**`/inventory/*`**, **`/reports/*`** incl. attendance Excel, **`/staff-contracts/*`**, **`/staff-contract-templates/*`**, **`/tenant/data-export`**, **`/tenant/purge`**) now apply **`admin_user_limit()`** (30/min per user).
- **`docs/0020-rate-limiting-production.md`** updated for the above plus guest-feedback and password-reset bullets.

## Testing instructions

1. **Backend import:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python3 -c "import app.main"`
2. **SlowAPI subprocess test:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python3 -m pytest /app/tests/test_table_groups_slowapi_subprocess.py -q`
3. **`test:rate-limit`:** From **`front/`** with HAProxy reachable at `BASE_URL` (default `http://127.0.0.1:4202`). Local dev **`Settings._relax_rate_limits_in_dev`** raises login/register quotas when **`PRODUCTION`** is false, so **`npm run test:rate-limit`** expects 429 only when the API runs with production-like limits (e.g. **`PRODUCTION=true`** / production deploy). Smoke: script completes without crash; optional: re-run against production-like limits to assert 429 on 6th login / 4th register.
4. **Manual spot-check:** Hit **`GET /public/tenants`** and an **`/inventory`** route rapidly (or inspect response headers **`X-RateLimit-*`**) when **`RATE_LIMIT_ENABLED=true`**.
