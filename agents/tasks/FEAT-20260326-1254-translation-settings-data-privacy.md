# Translation needed for Settings > Data and privacy

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/108

## Problem / goal
Staff **Settings → Data & privacy** is English-only. The section must be translated for every locale the app already supports (same coverage as other settings areas). Align keys, JSON files under `front` i18n, and any backend strings if this section touches API messages.

## High-level instructions for coder
- Locate the Data & privacy settings UI and list all user-visible strings (titles, labels, hints, buttons, legal/helper text).
- Add or complete translation keys and entries in each supported language bundle (match existing i18n patterns for Settings).
- Manually spot-check switching languages: Data & privacy reads fully localized with no English fallbacks.
- If copy is shared with emails or exports, ensure those paths use the same keys or explicit locale handling where applicable.
