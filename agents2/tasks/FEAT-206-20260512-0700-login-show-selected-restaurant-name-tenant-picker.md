# Login — show selected restaurant name when arriving from tenant picker

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/206
- **206**

## Problem / goal
Staff arriving from the landing tenant cards hit `/login?tenant=<id>` but see only a generic welcome form with no restaurant context. Show which restaurant they chose (name and optional logo) when `tenant` is present; keep the current experience when the query param is absent.

## High-level instructions for coder
- On login init, if `tenant` query param exists, resolve tenant display name (and `logo_filename` if available) via existing public tenants API or a suitable lightweight endpoint; filter client-side from `getPublicTenants()` if that already returns enough data.
- Render a compact contextual line/card under the main heading with logo + name; use new i18n keys (e.g. `AUTH.LOGGING_INTO`, `AUTH.CHANGE_RESTAURANT`) in all `front/public/i18n/*.json` files.
- Add a link to return to `/` for “wrong restaurant” without blocking the form; load tenant info asynchronously.
- On invalid tenant or 404, fall back silently to today’s generic login (optional console warning only).
- Do not change landing, tenant picker cards, login API contract, register, or forgot-password in this task.
- Verify: with `?tenant` → name (+ logo) + translated labels; without `?tenant` → unchanged; language switch updates copy.
- After build: `docker logs` for `pos-front`; `npm run test:landing-version --prefix front` with `BASE_URL`; changelog line per issue.
