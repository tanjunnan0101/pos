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

## Implementation summary
- Removed the secondary hint paragraph (`landing-panel__hint` / `LANDING.SECTION_TEAM_HINT`) from the staff panel; kept `h2` + `aria-labelledby` unchanged.
- Merged “new account” and “returning staff” guidance into a single `LANDING.SECTION_TEAM_LEDE` string in all shipped locales (`en`, `de`, `es`, `fr`, `ca`, `bg`, `hi`, `zh-CN`).
- Removed unused `SECTION_TEAM_HINT` keys and the `.landing-panel__hint` block from `landing.component.ts`.

## Testing instructions
1. With the stack up (e.g. HAProxy on `http://127.0.0.1:4202`), open `/` logged out.
2. In the **For restaurant staff** (or translated) panel: confirm one intro paragraph under the heading, then the **Create staff account** CTA; no second muted hint line below the button.
3. Confirm copy still covers both new registration and returning login (pick restaurant, then Login).
4. Optional: `docker logs --since 5m pos-front | grep -iE error` — no Angular build errors.
5. Smoke: `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version` (exit 0).
