# Add Urdu (ur) as a fully supported language across POS

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/205
- **205**

## Problem / goal
Users must be able to select Urdu (“اردو”) from the language switcher and see the full product—frontend, public flows, staff areas, backend messages, emails, exports—in Urdu with correct RTL layout. No missing keys vs English; no English leakage when Urdu is active.

## High-level instructions for coder
- **Frontend:** Register `ur` in `language.service.ts` (`SUPPORTED_LANGUAGES`, normalization, browser/`Accept-Language` handling). Add `front/public/i18n/ur.json` with **1:1 key parity** vs `en.json` (same structure and placeholders). Extend language-picker and any hardcoded admin lists if present.
- **RTL:** In `LanguageService.applyLanguage()`, set `document.documentElement.dir` to `rtl` for RTL codes (start with `ur` in a small extensible list) and `ltr` otherwise, alongside `lang`. Prefer logical CSS (`margin-inline-*`, `text-align: start/end`) for obvious fixes; spot-check major routes (landing, auth, dashboard, floor, orders, reservations, public book/menu, feedback, settings, reports). Avoid full global refactor; note intentional arrow/icon exceptions in PR if needed.
- **Backend:** Add `ur` to `back/app/language_service.py` and mirror every message key in `messages.py`, `report_export_i18n.py`, `schedule_export_i18n.py`, and any other `*_i18n` modules (search for existing language blocks like `_HI` / `"hi":` to find all).
- **Docs/tests:** Update README supported-language list if present; `docs/0012-translation-implementation.md` if it lists languages; `CHANGELOG.md` `[Unreleased]`. Frontend build clean; `pytest` for language-related modules; `test:landing-version` smoke.
- **Out of scope:** Translating restaurant-owned menu or custom content—platform strings only.
