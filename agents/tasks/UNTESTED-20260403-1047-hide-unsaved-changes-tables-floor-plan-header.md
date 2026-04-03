# Hide “unsaved changes” label on tables floor-plan header

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- `gh issue list --repo satisfecho/pos --state open --limit 40`
- Optional: `--json number,title,labels,updatedAt,url`
- **Issue:** https://github.com/satisfecho/pos/issues/157

## Problem / goal
Remove the visible unsaved-changes indicator in the tables floor-plan header (the `TABLES.UNSAVED_CHANGES` span in header actions) and clean up any now-unused `.unsaved-indicator` styles. Keep all dirty-state logic intact: `hasUnsavedChanges`, autosave behavior, Save layout enablement, and `canDeactivate` / `beforeunload` must continue to work as today—only hide that UI text.

## High-level instructions for coder
- In `tables-canvas` (component template/styles as referenced in the issue), remove or stop rendering the header unsaved-changes label while preserving underlying state.
- Remove dead CSS for `.unsaved-indicator` if nothing else relies on it; grep for other uses before deleting.
- Do not weaken navigation guards or save flows; smoke the tables floor plan after edits (drag layout, confirm Save / leave prompts still behave).
- Relevant context: recent floor-plan / canvas work in `docs/` or closed tasks under `agents/tasks/done/` if you need UX expectations for dirty layout.

## Implementation notes (coder)
- **`front/src/app/tables/tables-canvas.component.ts`:** Removed the `@if (hasUnsavedChanges())` block that rendered the translated span; removed `.unsaved-indicator` styles. **`hasUnsavedChanges()`** still drives **Save layout** `[disabled]` and all existing dirty tracking, autosave, guards, and `beforeunload`.

## Testing instructions
1. **Angular build:** With stack up (`docker compose -f docker-compose.yml -f docker-compose.dev.yml`), confirm `docker compose … logs --tail=40 front` shows **Application bundle generation complete** with no TS/template errors after the change.
2. **Smoke:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — exit 0.
3. **Tables canvas:** `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-tables-canvas-view-options.mjs` — exit 0.
4. **Manual (recommended for tester):** Log in → `/tables/canvas` → drag a table → confirm **no** “Unsaved changes” text in the header, but **Save layout** enables while dirty and works; navigate away with dirty layout and confirm **canDeactivate** / confirm dialog still appears as before; after save or discard, navigation works.
