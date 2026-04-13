# Landing: remove redundant staff section copy

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/182
- **182**

## Problem / goal
The restaurant staff panel on the landing page repeats messaging (heading vs hint). Reduce redundancy so the section stays clear without duplicate or near-duplicate copy.

## High-level instructions for coder
- Open the landing component template for the team/staff panel and identify redundant elements (e.g. section heading vs hint paragraph).
- Remove or consolidate the redundant piece per the issue intent (drop duplicate heading, or drop the hint, or both if still redundant)—keep one clear label for the section.
- Adjust `front/public/i18n/*.json` only if keys become unused: remove obsolete `LANDING.*` strings or keep keys per project i18n convention if they may be reused.
- Confirm layout and accessibility: if a visible heading is removed, ensure the section still has an appropriate accessible name (e.g. `aria-label` on the section or a single remaining heading).
- Run the usual frontend build check (container logs) after the change.
