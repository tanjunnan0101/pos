# Technical Instruction for UI Adjustment

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/137

## Problem / goal

On **Tables**, the canvas header area shows a **dark/black** background that should be reverted to the **original light/neutral** look. The issue points at the main header container for the tables canvas (staff flow), including floor tabs.

## High-level instructions for coder

- Find SCSS/CSS that sets a **dark background** on the tables management header / staff-flow header for this view.
- Relevant hooks from the issue: container with **`data-testid="tables-canvas-header"`**, class **`.page-header--staff-flow`**, and **`.floor-tabs`** (and related layout under the Tables / floor canvas).
- **Remove or replace** the dark background so the header matches the prior light/neutral staff-flow styling; avoid regressions on other routes that reuse shared classes—scope changes to the Tables canvas header as needed.

## Implementation notes

- **`front/src/app/tables/tables-canvas.component.ts`:** Removed `.canvas-container.tables-canvas--tablet` overrides that set `.page-header` and `.floor-tabs` to the dark canvas palette (`--tables-canvas-bg` / `#1a1f26`). Base component styles (`var(--color-bg)`, `var(--color-surface)`) apply again; dark grid/canvas remains on `.canvas-area` only.

## Testing instructions

1. Stack up (e.g. HAProxy on **4202**): `docker compose -f docker-compose.yml -f docker-compose.dev.yml ps`.
2. Log in as staff; open **Tables** → **floor plan** (`/tables/canvas` or equivalent).
3. Confirm **`[data-testid="tables-canvas-header"]`** and **`.floor-tabs`** use light/neutral backgrounds (match `/tables` tiles view header), while the **canvas** drawing area stays dark with grid.
4. Optional Puppeteer: from repo root, `BASE_URL=http://127.0.0.1:4202 LOGIN_EMAIL=… LOGIN_PASSWORD=… node front/scripts/test-tables-canvas-view-options.mjs` (requires credentials).
5. Quick smoke: `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front`.
