# Working plan — per-user calendar colors

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/109

## Problem / goal

On **Working plan**, the calendar should use a **distinct, smooth color per user/staff** who appears in the calendar, so multiple people in the same view are easy to tell apart at a glance.

## High-level instructions for coder

- Locate the working plan calendar UI (shift rendering, legend, any shared color logic) and how users/workers are bound to events.
- Define a stable, per-user color assignment (e.g. hash user id → HSL palette) so the same user always gets the same color; prefer accessible, distinguishable “smooth” tones (not harsh primaries only).
- Ensure the palette works in light (and dark, if applicable) theme; avoid clashes when many users appear in one range.
- Add or extend tests/smoke as appropriate (e.g. working-plan Puppeteer if it covers calendar) and verify manually with several users on the same day/week.

## Testing instructions

1. **Angular build:** With Docker dev stack up, `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — no TS/NG errors after reload.
2. **Puppeteer (from `front/` with app on 4202):**
   - `BASE_URL=http://127.0.0.1:4202 HEADLESS=1 npm run test:working-plan`
   - `BASE_URL=http://127.0.0.1:4202 HEADLESS=1 npm run test:working-plan-calendar`
3. **Manual:** Log in as staff with schedule access → **Working plan** → **Calendar**. Days with shifts: each shift row is a soft colored chip with left accent; same staff member keeps the same color across days. **Week** view: each shift card has a matching left border. Toggle OS dark mode (if used): chips should remain readable.
4. **Unit (optional, needs Chrome):** `npx ng test --watch=false --browsers=ChromeHeadless --include=**/working-plan-shift-colors.spec.ts` from `front/` when `CHROME_BIN` is set (e.g. on host with Chrome).
