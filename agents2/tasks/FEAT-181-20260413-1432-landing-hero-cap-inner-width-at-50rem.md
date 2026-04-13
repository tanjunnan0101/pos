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
