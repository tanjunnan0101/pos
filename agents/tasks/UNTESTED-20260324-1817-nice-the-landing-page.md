# Nice the landing page

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/69

## Problem / goal
The public landing at `http://127.0.0.1:4202/` (and production equivalent) should feel polished and welcoming for both restaurant owners and guests. The issue suggests benchmarking modern landing patterns (example reference in the issue) and upgrading visuals, layout, and overall experience—not a minimal placeholder.

## High-level instructions for coder
- Review the current landing route/components and branding constraints (tenant vs global landing if applicable).
- Research a small set of reference patterns (accessibility, performance, mobile-first) and align with existing Angular/design tokens in the repo rather than one-off CSS sprawl.
- Propose or implement improved hero, value props, and clear paths for owners vs clients; keep load time and SSR/dev build implications in mind.
- Smoke-test locally (e.g. landing Puppeteer script / curl) after changes; document any env-specific assets in README only if behavior changes.

## Coder notes (2026-03-24)
- **`front/src/app/landing/landing.component.ts`:** Hero with radial gradient using `--color-primary-light`, clamp typography, three value props (inline SVG, `aria-hidden`), mobile-first two-column split (guests: table code + takeaway; staff: copy + primary CTA to `/register`), restaurants block with section heading; tenant cards use `<article>` + `<h3>` for structure. Footer and `data-testid` for version / provider links unchanged.
- **`front/public/i18n/*.json`:** New `LANDING.*` strings (values, section titles, staff CTA, restaurants heading); refreshed title/subtitle; `zh-CN` / `hi` gained `ORDER_TAKEAWAY` for parity.

---

## Testing instructions

### What to verify
- `/` loads without console/build errors; hero, value row, guest panel (table code), staff panel (register CTA), restaurant grid (when tenants exist), footer, and version bar look correct on narrow and wide viewports.
- Language switcher still works; new strings appear translated per locale.
- Provider footer links and staff register link navigate correctly.

### How to test
- Stack up (e.g. `docker compose -f docker-compose.yml -f docker-compose.dev.yml`); open `http://127.0.0.1:4202/`.
- `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — no Angular/TS errors after edits.
- From `front/`: `BASE_URL=http://127.0.0.1:4202 node scripts/test-landing-version.mjs` (optional: with `DEMO_LOGIN_*` / `LOGIN_*` for extended nav test).
- `BASE_URL=http://127.0.0.1:4202 node scripts/test-landing-provider-links.mjs`

### Pass / fail criteria
- **Pass:** Builds clean; both Puppeteer scripts exit 0; manual spot-check shows no layout breakage or missing i18n keys (no raw `LANDING.*` in UI).
- **Fail:** Any build error, script exit non-zero, or obvious regression on `/` (broken table lookup, tenant cards, or footer links).
