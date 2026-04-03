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
