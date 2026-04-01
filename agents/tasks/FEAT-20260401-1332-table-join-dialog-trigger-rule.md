# Table join dialog — trigger rule

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/142

## Problem / goal
On the Tables layout, the “join / group tables” confirmation must appear only when the dragged table **actually overlaps** the other table in canvas space (bounding boxes or shape geometry intersect; intersection area greater than zero, or enforce a minimum overlap ratio if tiny touches should be ignored). Adjacent tables that are close but **not** overlapping must not open the join dialog. Do not rely on distance alone as the trigger.

Document the chosen overlap rule (e.g. AABB vs rotated rectangles) in code or a short note so behavior stays consistent with zoom and pan.

## High-level instructions for coder
- Locate the tables canvas drag/join flow and where the join confirmation is shown.
- Replace or tighten the trigger so it requires real geometric overlap in layout coordinates, not mere proximity.
- Align with how table shapes are drawn (rotation, hit testing) so the rule matches what users see.
- Add a brief, durable explanation of the overlap test for future maintainers.
- Verify with adjacent non-overlapping tables and clearly overlapping pairs.
