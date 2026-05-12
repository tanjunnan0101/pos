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
