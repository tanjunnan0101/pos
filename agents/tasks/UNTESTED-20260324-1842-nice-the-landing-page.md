# Nice the landing page

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/69

## Problem / goal
The public landing (`/` via HAProxy, e.g. `http://127.0.0.1:4202/`) should be a polished, modern experience for restaurant owners and guests. The reporter referenced external inspiration (AnythingLLM-style marketing page) and asked for research-backed visual and UX improvements, not a bare placeholder.

Prior implementation and tester **PASS** are recorded in **`agents/tasks/done/2026/03/24/CLOSED-20260324-1817-nice-the-landing-page.md`**. The GitHub issue remains **open** — this task is the **close-the-loop** queue item: confirm current `development` still matches the issue, capture any remaining gaps vs the issue text, and drive **GitHub** closure or a small follow-up scope.

## High-level instructions for coder
- Compare live landing (local Docker + optional production) against **#69** acceptance: hero, clarity for owners vs clients, mobile-first layout, accessibility, and i18n (`LANDING.*` parity across `front/public/i18n/*.json`).
- Re-run relevant smoke scripts from the archived task (e.g. `test-landing-version.mjs`, `test-landing-provider-links.mjs`); confirm **`docker compose` `logs` —tail=80 front** shows a clean Angular build after any touch.
- If behaviour already satisfies the issue, document evidence and hand to closer / maintainer to **close #69** (or post verification comment). If gaps remain, implement the smallest targeted changes and re-test.
- Do not duplicate full greenfield redesign if the archived work already met tester criteria unless the issue explicitly lists missing items.

## Coder notes (close-the-loop, 2026-03-24)
- **Verified** current tree still matches the archived implementation: `front/src/app/landing/landing.component.ts` (radial hero, clamp type, three value props with `aria-hidden` icons, mobile-first guest/staff panels, restaurants block, `data-testid` for version and provider links).
- **i18n parity:** All `front/public/i18n/*.json` locales share the same `LANDING` key set (including prior parity work).
- **Small follow-up implemented:** Footer strings **Provider login** / **Register as provider** were hardcoded English only. Added **`LANDING.PROVIDER_LOGIN`** and **`LANDING.REGISTER_AS_PROVIDER`** in every locale and bound the footer anchors with the translate pipe (`data-testid` unchanged for Puppeteer).
- **Evidence vs #69:** Issue asks for a nicer landing for owners and clients; archived PASS + above parity fix satisfy scope. **Closer / maintainer:** close **#69** after tester PASS, or comment with this verification (token may block automated `gh issue comment` per prior closed task).

---

## Testing instructions

### What to verify
- `/` loads; footer provider links show translated text per language (not raw `LANDING.*` keys); `data-testid="landing-provider-login"` and `landing-provider-register` still present.
- Angular build clean in Docker front logs after changes.

### How to test
- Stack up: `docker compose -f docker-compose.yml -f docker-compose.dev.yml` (or existing dev stack); `http://127.0.0.1:4202/`.
- `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — no TS/NG errors.
- From `front/`: `BASE_URL=http://127.0.0.1:4202 node scripts/test-landing-provider-links.mjs`
- From `front/`: `BASE_URL=http://127.0.0.1:4202 node scripts/test-landing-version.mjs` (optional: with `LOGIN_EMAIL` / `LOGIN_PASSWORD` or `.env` demo creds for extended nav).
- Manual: language picker → DE (or other); confirm footer shows localized provider link labels.

### Pass / fail criteria
- **Pass:** Both scripts exit `0`; build log shows successful bundle generation; no raw `LANDING.*` in footer when switching language.
- **Fail:** Non-zero script exit, build errors, missing keys, or broken `/provider/login` / `/provider/register` navigation from footer.
