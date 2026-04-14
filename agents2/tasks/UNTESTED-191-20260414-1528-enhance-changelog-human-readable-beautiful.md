# Enhance CHANGELOG.md for human readability and presentation

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/191
- **191**

## Problem / goal
Improve `CHANGELOG.md` so it stays a clear, scannable, human-facing record of product changes (not an internal dump). Entries should be chronological (newest first), consistently structured (Unreleased plus versioned releases), and written with user impact in mind. Align categorization (Added / Changed / Fixed / Removed / Security) and semantic versioning expectations with team practice; when cutting a release, move Unreleased content into a dated version section and refresh Unreleased.

## High-level instructions for coder
- Review current `CHANGELOG.md`, `front/package.json` version, and `.cursor/rules/commit-changelog-version.mdc` / `AGENTS.md` conventions for releases.
- Apply the structure and style from the issue: Keep a Changelog–style sections, past tense, one line per bullet where possible, group related work, avoid unnecessary commit hashes in prose.
- Ensure **Unreleased** reflects recent notable work; when preparing a release, add `## [X.Y.Z] - YYYY-MM-DD`, move items from Unreleased, and bump version in `front/package.json` / lockfile as required by project rules.
- Optionally tighten formatting or light styling (e.g. headings, spacing) if it improves readability without breaking Markdown tooling; avoid unrelated refactors elsewhere in the repo.

## Implementation summary
- Rewrote `CHANGELOG.md` intro: Keep a Changelog + semver pointer, newest-first reminder, past tense / user-impact note.
- Consolidated **Unreleased** into **Added** / **Changed** / **Fixed** with shorter issue refs, grouped related items, removed internal-only bullets (e.g. task filename churn, log reviewer sweep) from the user-facing list.
- Polished **2.0.75** entry into a single scannable **Changed** bullet aligned with the same style.
- No version bump (formatting-only change; release cut still follows `commit-changelog-version.mdc` when promoting Unreleased).

## Testing instructions
1. Open `CHANGELOG.md` in the repo editor or Markdown preview and confirm structure (Unreleased then dated release), headings, and readability.
2. With the dev stack up (`docker compose` dev overlay, HAProxy e.g. port 4202), run from `front/`:  
   `BASE_URL=http://127.0.0.1:4202 npm run test:changelog`  
   (requires `LOGIN_EMAIL` / `LOGIN_PASSWORD` or `.env` demo credentials). Expect: **What’s new** modal loads and shows changelog content (length > 100, version headings).
3. Optional: open Dashboard → **What’s new** and skim the modal for formatting (no raw markdown breakage in the renderer).
