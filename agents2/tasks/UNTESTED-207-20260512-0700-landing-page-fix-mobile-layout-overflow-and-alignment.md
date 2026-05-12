# Landing page — fix mobile layout overflow and alignment issues

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/207
- **207**

## Problem / goal
On narrow mobile viewports, the public landing page (`/`) has three CSS-only problems in `front/src/app/landing/landing.component.ts` (inline styles): the language picker appears detached from the hero; the three value-proposition bullets stack with uneven widths; the table-code input row overflows horizontally. Desktop layout must stay unchanged.

## High-level instructions for coder
- Fix **Bug 1** (language picker): On mobile breakpoints, contain the picker inside the hero (e.g. `position: relative` on hero + adjust picker positioning, or flow it with flex) so it stays visible, tappable, and does not overlap the title.
- Fix **Bug 2** (value bullets): On mobile, stack with consistent width (e.g. column layout, equal `max-width` on items) so copy and icons align cleanly.
- Fix **Bug 3** (table code row): Prevent flex overflow (`min-width: 0` on input), reduce button horizontal padding on small screens, verify down to ~320px width; scope to landing only.
- Verify at ~375px and ~414px widths; confirm desktop (>960px) unchanged.
- After build: check `docker logs` for `pos-front`; run `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front`.
- Update `CHANGELOG.md` under `[Unreleased]` per issue text when shipping.

## Implementation summary

- **`front/src/app/landing/landing.component.ts`:** Moved `<app-language-picker>` into `<header class="landing-hero">` inside `.landing-hero__top`. **Mobile (≤960px):** toolbar is in normal flow (`flex-end`) so the picker stays part of the hero. **Desktop (≥961px):** `.landing-hero__top` is `position: absolute` top-right on the hero (pointer-events wrapper) so wide layout matches the prior corner placement.
- **Value bullets:** `@media (max-width: 960px)` — column stack, `max-width: 20rem` + centered list, each `.landing-value` full width for even alignment.
- **Table code row:** `.table-code-row` / `.table-code-input` use `min-width: 0` and `flex: 1 1 0` on the input; `.btn-go` `flex-shrink: 0`; tighter `padding-inline` under 480px; under 360px row wraps so the button can sit on a second line.
- **`CHANGELOG.md`:** `[Unreleased]` **Fixed** entry for #207.

## Testing instructions

1. **Responsive UI:** Open `/` at **~375px** and **~414px** width. Confirm: language picker is in the hero’s top band (not visually separated from the hero); three value lines stack with consistent width; table-code field and **Go** fit without horizontal page scroll (try **~320px**).
2. **Desktop:** At **≥961px**, confirm picker remains top-right of the hero, value bullets in a horizontal wrap as before, guest panel unchanged.
3. **Build:** `docker logs --since 10m pos-front 2>&1 | grep -iE 'error|NG8'` — expect no matches after a save/rebuild.
4. **Smoke:** From repo root: `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front`. If the footer semver differs from `front/package.json` (stale `COMMIT_HASH` / image), use `SKIP_LANDING_PACKAGE_VERSION_CHECK=1` for the same run (see script header in `front/scripts/test-landing-version.mjs`).
