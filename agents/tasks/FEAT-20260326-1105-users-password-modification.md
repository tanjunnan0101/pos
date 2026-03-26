# Users — password modification

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/105

## Problem / goal
On **Users → User management → modify user** (`/users`), when the **account owner** changes a user’s password, the flow must require **current password** first, then **new password** (and typical confirmation), so password changes are not possible without re-authentication.

## High-level instructions for coder
- Trace the existing **edit user** / password-change API and UI on `/users`; compare with any existing “change my password” or security patterns in the repo.
- Extend or adjust the **owner-modifies-user-password** flow so the backend validates **current password** of the acting owner (or session) before applying a new password; align error messages and i18n with project conventions.
- Ensure non-owner roles cannot bypass the rule; keep tenant scoping and permissions consistent with adjacent user-management endpoints.
- Add or extend tests (API and/or e2e) for success and failure (wrong current password, missing fields). Run relevant pytest and front build checks.
