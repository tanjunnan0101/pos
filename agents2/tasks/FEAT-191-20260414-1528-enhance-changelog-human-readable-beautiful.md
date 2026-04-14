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
