# Landing hero: cap inner width at 50rem

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/181
- **181**

## Problem / goal
On the marketing landing page, the hero content should not stretch excessively wide on large viewports. Constrain the inner hero wrapper to a readable max width (50rem) while keeping current centering and padding behavior.

## High-level instructions for coder
- Locate the landing hero styles (component SCSS/CSS module or global landing styles).
- Add `max-width: 50rem` to the inner hero selector (e.g. `.landing-hero__inner` or equivalent in the current codebase).
- Preserve layout: centering and spacing; if the inner is block-level, use `margin-inline: auto` (or existing flex/grid patterns) so the block stays centered when width is capped.
- Verify at wide breakpoints that text does not span the full viewport width.
- Run the usual frontend build check (container logs) after the change.

## Implementation summary
- **`front/src/app/landing/landing.component.ts`:** `.landing-hero__inner` **`max-width`** set from **42rem** to **50rem**; existing **`margin: 0 auto`** and padding unchanged.

## Testing instructions
1. With the stack up (`docker compose` dev overlay), open **`http://127.0.0.1:4202/`** (or your HAProxy port).
2. Widen the browser past ~900px; confirm hero title/subtitle block stays centered and does not span the full width (inner column caps at **50rem**).
3. **`BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front`** — expect exit **0** (smoke: landing loads, optional login/nav).
4. **`docker logs --since 5m pos-front`** — no Angular build errors after the change.
