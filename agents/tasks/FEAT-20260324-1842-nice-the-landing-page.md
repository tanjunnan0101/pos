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
