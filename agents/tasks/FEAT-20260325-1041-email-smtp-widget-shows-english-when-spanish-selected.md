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
