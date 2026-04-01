# Update README.md

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/132

## Problem / goal
Improve root **README.md** so it matches the product: move rate-limiting documentation into dedicated files under **`docs/`**, refresh the feature list to reflect everything exposed in the side navigation and settings, and document **Revolut** payment where appropriate (see **`docs/REVOLUT.md`** if present).

## High-level instructions for coder
- Extract or relocate rate-limiting topics from **README** into one or more focused **`docs/*.md`** files; keep **README** pointing to those docs instead of duplicating long sections.
- Audit the app’s side nav and settings areas and update the README feature list so it is accurate and discoverable for new contributors.
- Add or cross-link Revolut payment setup/usage consistent with existing payment docs.

---

## Testing instructions

- **Review:** Root **README.md** — Payments / Security / Documentation rows mention Revolut and [docs/0020-rate-limiting-production.md](docs/0020-rate-limiting-production.md); **Staff navigation** row matches sidebar; no stale “rate limiting not implemented” claim.
- **Docs index:** [docs/README.md](docs/README.md) includes **REVOLUT.md** in quick links and feature guides.
- **Links:** Spot-check relative links to `docs/REVOLUT.md` and `docs/0020-rate-limiting-production.md` from repo root.
