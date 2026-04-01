# Move GitHub link to landing-version area

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/134

## Problem / goal
Expose the repository link beside the landing page version line: add a **GitHub icon/link inside the `landing-version` region** (not only the footer). Add a short **tagline** alongside that area: open-source positioning and attribution to El Masnou (Barcelona) and Los Mochis (Mexico), with a heart symbol as in the issue. See existing landing footer GitHub work in `docs/` / closed tasks only for UX consistency, not to duplicate two competing patterns without product intent.

## High-level instructions for coder
- Locate the **landing version** UI (component/template that shows app version on the public landing page) and add a compact **GitHub** affordance (icon + link to `https://github.com/satisfecho/pos/`) within or adjacent to that **`landing-version`** block so the link reads as part of the version strip.
- Add the **tagline** copy; use **ngx-translate** keys under `front/public/i18n/` per project i18n rules (no hard-coded locale-only strings in templates).
- Reconcile with the **footer** GitHub link from prior issue **#133**: avoid cluttered double links—either move primary link to the version area, or keep one clear primary location per product decision; keep `data-testid` / smoke expectations in mind (`test:landing-version` may need selector updates).
- Verify responsive layout: narrow viewports must not break the version + icon + tagline row.
