# Tables — floor plan UX (auto-save, join snap-back, name refresh)

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/145

## Problem / goal
Improve the Tables floor-plan experience in three areas: (1) **auto-save** — persist layout changes with debounce (e.g. 300–800 ms), dedupe in-flight saves, correct “Unsaved changes” handling, and safe behavior on route leave / optional `beforeunload`, using existing APIs and tenant scoping; document user-visible behavior in CHANGELOG if needed. (2) **After joining tables** — when a join completes, restore dragged table(s) to their canvas positions from before the join gesture; grouping remains logical for service; clarify that join is grouping, not permanent overlap on the saved floor plan. (3) **Table name in floor view** — changing the name in the sidebar must update the visible label (and in-canvas title) immediately; debounced save must not delay local UI updates (fix binding/change detection so the name reflects the current model without requiring focus elsewhere).

Acceptance: after join, tables snap back to pre-gesture positions while the group stays joined; editing a name shows it immediately on the floor/canvas and persists after debounce/reload; no extra “click elsewhere” to see the name.

## High-level instructions for coder
- Implement debounced auto-save for floor layout with superseding saves and coherent dirty/unsaved state; handle navigation leave safely.
- After successful join, reset canvas positions to pre-gesture layout while preserving logical table group for service.
- Ensure table rename updates UI immediately; separate debounced persistence from local display state.
- Reuse existing floor/table APIs; keep tenant scoping and authorization consistent with adjacent tables code.
- Update CHANGELOG if behavior is user-visible.
