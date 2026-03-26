# Contact us

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/104

## Problem / goal
Add a **Contact us** link in the **app landing** footer. Copy must respect **i18n** (all supported locales). Use contact address **`sales@saitsfecho.de`** as given in the issue; confirm spelling with product/marketing if the domain should be **`satisfecho.de`**.

## High-level instructions for coder
- Locate the landing footer component/layout and add a visible **Contact us** link (or mailto) consistent with existing footer styling.
- Add translation keys for the link label in **`front/public/i18n/*.json`** (parity with reference locale); avoid hard-coded English-only strings.
- Wire the target email to match the issue once confirmed; use existing patterns for external links or `mailto:` if the app already does so elsewhere.
- Smoke-check landing in at least two locales and run the usual front build log check after changes.
