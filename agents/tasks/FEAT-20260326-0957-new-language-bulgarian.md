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
