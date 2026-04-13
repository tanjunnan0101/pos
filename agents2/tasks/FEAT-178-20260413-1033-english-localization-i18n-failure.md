# English Localization Resource Failure (i18n)

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/178
- **178**

## Problem / goal
When the user selects **English (EN)**, the UI shows **raw translation keys** (e.g. `NAV.DASHBOARD`, `AUTH.SIGN_IN`) instead of human-readable strings. **Other locales** (e.g. Spanish, French) render correctly, so the problem is isolated to **English resources**, not the general i18n pipeline.

Likely areas to verify: `en.json` (or equivalent) present in the app bundle, valid JSON (no syntax errors), and that deploy/CI copies i18n assets as expected for EN.

## High-level instructions for coder
- Compare **`front/public/i18n/en.json`** (and any EN-specific paths) with a working locale such as **`es.json`**: structure, required keys, and file validity (parse as JSON locally).
- Confirm Angular/ngx-translate (or project equivalent) loads **`en`** the same way as other languages; fix missing merge, wrong path, or loader failure for EN only.
- Reproduce in dev: switch language to English and confirm keys vs strings; after fix, spot-check main nav and auth strings.
- If production-only: verify build output and deployment include **`en.json`**; align with **`docs/`** and **`.cursor/rules/angular-ngx-translate.mdc`** if applicable.
