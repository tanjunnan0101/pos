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
