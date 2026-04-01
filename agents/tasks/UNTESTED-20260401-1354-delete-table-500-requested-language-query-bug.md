# DELETE /tables/{id} returns 500 — requested language is a Query object

## Source

- **Service:** `pos-back` (`docker logs pos-back`).
- **UTC window:** ~2026-04-01T13:32Z–13:53Z (matches preflight digest; reproduced in live tail).
- **Representative lines:**
  - `DELETE /tables/… HTTP/1.1" 500 Internal Server Error` with `Exception in ASGI application`.
  - Traceback ends in `delete_table` → `lang = _get_requested_language(request)` → `normalize_language_code(lang)` → **`AttributeError: 'Query' object has no attribute 'lower'`** in `language_service.py` (caller `main.py` ~6943).

## High-level instructions for coder

- Inspect `delete_table` and `_get_requested_language` in `back/app/main.py`: ensure the value passed into language normalization is a **string** (or `None`), not a **`Query`** dependency placeholder.
- Align with other endpoints that already resolve `Accept-Language` / `lang` query correctly after recent API error / i18n refactors.
- Re-test `DELETE /api/tables/{id}` (HAProxy or direct back) and confirm **2xx/4xx** for normal cases and structured errors (e.g. table has orders) without **500**.
- Optional: grep for the same `_get_requested_language` usage pattern on other handlers if the bug is copy-pasted.

## Implementation notes (coder)

- **Cause:** `delete_table` called `_get_requested_language(request)` directly. That function’s `lang` / `accept_language_query` parameters default to `Query(...)`, so without FastAPI injection the default value is a **`Query` object**, which then reached `normalize_language_code` and raised **`AttributeError: 'Query' object has no attribute 'lower'`**.
- **Fix:** `delete_table` now takes `lang: str = Depends(_get_requested_language)` like other handlers; removed the manual call.
- **Regression test:** `back/tests/test_delete_table_api.py` — 404 for missing table (exercises `api_error_payload(..., lang)`), 200 for delete of an empty inactive table.

## Testing instructions

1. **What to verify:** `DELETE /tables/{id}` never returns **500** from language resolution; **404** / **400** responses use structured `detail` (e.g. `table_not_found`, `table_has_orders`) as before.
2. **How to test:**
   - Backend: `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python3 -m pytest tests/test_delete_table_api.py -q`
   - Manual (with staff JWT and `TABLE_WRITE`): `DELETE` a non-existent id → **404**; delete an inactive table with no orders → **200**; HAProxy path e.g. `DELETE http://127.0.0.1:4202/api/tables/{id}` with `Authorization: Bearer …`.
3. **Pass/fail:** Pytest **2 passed**; manual calls return **no 500**; JSON errors remain structured (not raw traceback).
