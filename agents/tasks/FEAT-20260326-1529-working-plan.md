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
