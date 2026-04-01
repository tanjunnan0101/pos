# API error messages / language

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/143

## Problem / goal
User-visible errors must follow the app locale. Avoid surfacing raw English detail strings from the backend in the UI.

Prefer stable API error codes (and optional structured parameters) mapped to `ngx-translate` keys in `front/public/i18n/*.json` for all shipped languages. Alternatively, translate known server message patterns on the client—but do not leave untranslated server strings in the user interface.

## High-level instructions for coder
- Inventory where API errors are shown (interceptors, components, toast/dialog flows).
- Decide contract: error codes (and params) from API vs. client-side mapping of known messages; prefer codes for consistency.
- Add or extend i18n keys per language for user-facing error copy; keep developer-only detail in logs if needed.
- Update backend responses where appropriate to return codes suitable for translation, without breaking existing clients unnecessarily.
- Smoke-test at least one non-default locale to confirm no raw English leaks for handled errors.

## Implementation notes (coder)
- **Backend:** `back/app/api_errors.py` — `api_error_payload(code, lang, **kwargs)` returns `{"code", "message", "params"?}`; `main.py` endpoints that used `get_message(...)` for `HTTPException(detail=...)` now use this shape. Also: `DELETE /tables/{id}` (table has orders / reassign), public `GET /menu/{token}` (404/500), `create_reservation` validation messages, `/token` OTP pending response, `/token/otp` errors, branded `TABLE_CLOSED` uses localized `table_currently_closed` for `message`.
- **Frontend:** `front/src/app/services/api-error-message.service.ts` — resolves `API_ERRORS.<CODE>` (with optional `params` for ngx-translate), then server `message`, then FastAPI validation array, then fallback i18n key. Wired into login, register, provider auth, book, landing, working-plan, reservations, tables list, and floor canvas (including `table_has_orders` detection by `code`).
- **i18n:** New `API_ERRORS` block plus `COMMON.API_REQUEST_FAILED` and `AUTH.LOGIN_FAILED` / `AUTH.LOGIN_RATE_LIMITED` in all eight `front/public/i18n/*.json` files.
- **Tests:** `back/tests/test_user_password_update.py` asserts on structured `detail.message`.

## Testing instructions
1. Start stack: `docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d` (or `./run.sh` per README).
2. **Locale:** In the app, switch the language picker to **Deutsch** (or any non-English shipped language).
3. **Login:** Enter a wrong password on `/login` — expect translated copy from `API_ERRORS.INCORRECT_USERNAME_OR_PASSWORD`, not a hard-coded English fallback string.
4. **Public book:** Open `/book/<tenantId>`, submit with a **past** date or invalid time — errors should follow the **UI** language via `API_ERRORS.*` (not only `Accept-Language`).
5. **Tables:** On `/tables` or `/tables/canvas`, delete a table that still has orders — reassign modal should open; inline error should use `API_ERRORS.TABLE_HAS_ORDERS` in the active UI language.
6. **Backend:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python3 -m pytest tests/test_user_password_update.py -q`
7. **Frontend build:** `cd front && npx ng build --configuration=development`
8. **Smoke (optional):** With HAProxy reachable, `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front`
