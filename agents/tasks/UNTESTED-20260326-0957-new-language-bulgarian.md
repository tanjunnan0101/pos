# New language: Bulgarian

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/103

## Problem / goal
Add Bulgarian (`bg` or team-standard code) across the stack: complete `i18n` JSON coverage, expose the locale in backend and customer-facing language selectors, and verify the app builds and key routes render without missing keys.

## High-level instructions for coder
- Add Bulgarian translation files alongside existing `front/public/i18n/*.json` (and any server-side locale lists); keep key parity with the reference locale(s).
- Register the language in backend locale enumeration and any Angular `TranslateService` / language-picker configuration.
- Ensure public routes (book, feedback, etc.) and staff app can select Bulgarian where applicable.
- Run Angular build check and a minimal manual or Puppeteer pass on a few screens in `bg`; document any intentional exclusions.

## Coder notes
- Added `front/public/i18n/bg.json` with full key parity to `en.json` (1478 leaf keys). Most strings came from a cached MyMemory `en|bg` pass; strings missing from the cache (API 429) were filled with hand-reviewed Bulgarian overrides. Placeholders (`{{…}}`, `{name}`) preserved.
- Registered `bg` in `front/src/app/services/language.service.ts`, `front/src/app/shared/intl-locale.ts`, `back/app/language_service.py`, `back/app/messages.py`, `back/app/schedule_export_i18n.py`, `back/app/report_export_i18n.py`.
- Test: `tests/test_report_export_i18n.py::test_report_export_bulgarian_headers`.

## Testing instructions

### What to verify
- Language picker lists **Български**; choosing it loads `/i18n/bg.json` without console missing-key warnings on landing, login, `/book/1`, and `/feedback/public/...` (with a valid token).
- Backend accepts `Accept-Language: bg` / `?lang=bg` for normalized locale; password-reset email strings exist for `bg` in `MESSAGES`.
- Report/schedule Excel exports use Bulgarian headers when `lang=bg` is honored by the export endpoint.

### How to test
- **Backend:**  
  `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec -T back python3 -m pytest tests/test_password_reset.py::TestPasswordReset::test_password_reset_email_translations_defined_for_all_locales tests/test_report_export_i18n.py -q`
- **Frontend build:**  
  `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — expect no TS/Angular errors after rebuild.
- **Smoke:**  
  `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`
- **Manual `bg`:** Open app → select Български → spot-check landing, login, book page for Cyrillic UI and no broken `KEY.NAME` literals.

### Pass/fail criteria
- Pass: pytest above green; front logs show successful bundle generation; smoke test exits 0; manual spot-check shows Bulgarian strings, not raw keys.
- Fail: any missing translation key in console, pytest failure, or Angular build error.

### Intentional exclusions
- None. Machine-translated strings may be refined by a native speaker later; structure and keys are complete.
