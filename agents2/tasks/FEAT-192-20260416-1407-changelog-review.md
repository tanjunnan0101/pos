# Changelog Review

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/192
- **192**

## Problem / goal
Review the repository root `CHANGELOG.md`, especially the `[Unreleased]` section. Compare it to recent commits on `development` and ensure entries match what actually shipped or is about to ship: add missing user-relevant items, fix inaccurate wording, and trim noise. Keep scope to changelog accuracy and repo release conventions unless the issue is expanded later.

## High-level instructions for coder
- Inspect `CHANGELOG.md` and cross-check with `git log` / recent merges on `development` so `[Unreleased]` reflects real changes.
- Apply project rules in `.cursor/rules/commit-changelog-version.mdc` (and `AGENTS.md`) for when to version-bump vs leave items under `[Unreleased]`.
- Update `README.md` or `docs/` only if the changelog review reveals documented behavior that no longer matches reality.
- After edits, run an appropriate smoke check if anything beyond markdown could be affected; pure changelog edits may only need quick sanity review.
