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
