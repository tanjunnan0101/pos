# Email SMTP widget shows English when Spanish is selected

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/81

## Problem / goal

In **Settings → Email (SMTP)**, the UI stays in **English** even when the user has chosen **Spanish** (and likely other locales). The reporter wants the SMTP/email settings widget reviewed for **all five supported languages**: Catalan, Spanish, German, Hindi, and Chinese — strings and layout should follow the active app language like the rest of Settings.

## High-level instructions for coder

- Locate the Email / SMTP section in the Angular settings module (templates, TS, and any hard-coded copy).
- Replace missing or English-only strings with the same i18n pattern used elsewhere (translation keys / JSON per locale).
- Verify each listed locale loads the correct strings (at least spot-check Spanish and one RTL or non-Latin script if applicable).
- Confirm no regressions to SMTP validation, save flow, or section routing.

## Implementation notes

- **Cause:** `SETTINGS.EMAIL_SETTINGS`, `SETTINGS.SMTP_*`, `SETTINGS.RESERVATION_CONFIRMATION_*`, etc. existed only in `en.json`, so ngx-translate fell back to English for other locales.
- **Locales updated:** `ca.json`, `de.json`, `es.json`, `fr.json`, `hi.json`, `zh-CN.json` — same keys as English, translated.
- **Template:** `settings.component.ts` — SMTP port and SMTP user inputs now use `[placeholder]="'SETTINGS.SMTP_PORT_PLACEHOLDER' | translate"` and `SMTP_USER_PLACEHOLDER`; `en.json` gained those two keys (other locales include them too).

---

## Testing instructions

### What to verify

- With UI language set to **Spanish** (and spot-check **Catalan**, **German**, **Hindi**, **Chinese**), **Settings → Email (SMTP)** shows translated section title, subtitle, labels, hints, and placeholders — not English.
- Sidebar label for the email section matches the active language.
- Saving settings and SMTP validation behaviour unchanged (no functional regression).

### How to test

1. Stack up: `docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d` (HAProxy e.g. `http://127.0.0.1:4202`).
2. Log in as a user who can open **Settings** (e.g. demo owner).
3. Change app language (user menu / language control) to **Español**, open **Configuración**, click **Correo (SMTP)** (or equivalent), confirm strings are Spanish.
4. Repeat quick checks for **ca**, **de**, **hi**, **zh-CN** if desired.
5. Smoke: `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version` (includes navigation to `/settings`).
6. Optional: `docker compose … logs --tail=80 front` — build completes without TS/template errors.

### Pass / fail criteria

- **Pass:** Email (SMTP) section and nav use the selected locale strings; `test:landing-version` succeeds; no new front build errors.
- **Fail:** Any key still shows English in a non-English locale, or save/validation broken.
