# Feedback page needs translation

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/67

## Problem / goal
The feedback page has UI text that is not localized. Translations needed for different languages (i18n). This is a feature/enhancement issue.

## High-level instructions for coder
- Review feedback Public component UI strings and identify text that needs localization
- Map out missing translation keys for common patterns (titles, labels, buttons)
- Implement i18n configuration and translation files; update feedback component template and code to use localization pipes or services with locale-aware text
- Run smoke test: access feedback page and verify language appears correctly
- Ensure translation keys are consistent with existing i18n structure in the codebase
- No database or backend API changes required; pure frontend UI localization work