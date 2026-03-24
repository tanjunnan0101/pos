# Nice the landing page

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/69

## Problem / goal
The public landing at `http://127.0.0.1:4202/` (and production) should feel polished and welcoming for both restaurant owners and restaurant clients. The reporter pointed at a reference layout (wz-it “AnythingLLM” page) as inspiration: research strong landing patterns, then evolve our landing toward a clearer, more beautiful experience without abandoning existing design tokens and i18n expectations. Prior closed tasks archived implementation and verification notes; treat this queue item as the feature-coder path until the issue is closed on GitHub.

## High-level instructions for coder
- Re-read issue body and any `agents/tasks/done/**/CLOSED-*nice-the-landing-page*.md` for what was already shipped vs what might still be open.
- Compare current `/` against the issue’s acceptance: hero, owner vs guest paths, mobile-first layout, accessibility, and `LANDING.*` (or equivalent) strings across `front/public/i18n/*.json`.
- If gaps remain, implement minimal, cohesive UI changes aligned with existing Angular patterns; run frontend build/smoke as in `AGENTS.md`.
- If work is complete, hand evidence to closer / maintainer to close **#69** on GitHub (or post a short verification comment).

## Coder notes (2026-03-24, feature-coder pickup)
- **Prior work:** `agents/tasks/done/2026/03/24/CLOSED-20260324-1817-nice-the-landing-page.md` and `CLOSED-20260324-1842-nice-the-landing-page.md` document the refreshed `LandingComponent` (hero, value props, guest/staff panels, restaurants block, footer provider links with i18n) and tester **PASS**.
- **This run:** No additional product code changes required. Re-verified current tree matches that scope.
- **i18n:** All seven files under `front/public/i18n/*.json` share the same 27 `LANDING.*` keys (parity script: OK).
- **GitHub #69:** Still **open** (body: polish landing for owners/clients; reference URL). Implementation aligns with intent; **maintainer/closer** should close **#69** or comment after tester PASS (token scope may block automated `gh issue comment`, per archived notes).
- **Smoke (local Docker, ~2026-03-24T18:58–18:59Z):** `curl` → `200` on `/`; `test-landing-provider-links.mjs` exit `0`; `test-landing-version.mjs` exit `0`; `docker compose … logs --tail=80 front` shows successful bundle generation, no TS/NG errors in tail.

---

## Testing instructions

### What to verify
- `/` loads; hero, value row, guest panel (table code + takeaway link), staff panel (register CTA), restaurants section (or empty state), footer (including translated provider links), version bar.
- No raw `LANDING.*` keys in UI when switching language (e.g. DE).
- `data-testid="landing-provider-login"`, `landing-provider-register`, `landing-staff-register`, `landing-version` still present where applicable.

### How to test
- Stack: `docker compose -f docker-compose.yml -f docker-compose.dev.yml` (or existing dev stack); `http://127.0.0.1:4202/`.
- `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — no Angular/TS build errors.
- From `front/`: `BASE_URL=http://127.0.0.1:4202 node scripts/test-landing-provider-links.mjs`
- From `front/`: `BASE_URL=http://127.0.0.1:4202 node scripts/test-landing-version.mjs` (optional: `.env` / `LOGIN_*` for extended nav).
- Manual: narrow + wide viewport; language picker → non-English locale.

### Pass / fail criteria
- **Pass:** Both scripts exit `0`; build log clean; footer and hero strings localized (no exposed keys); no layout regression on `/`.
- **Fail:** Non-zero script exit, build errors, missing i18n keys, or broken table lookup / tenant cards / footer routes.
