# Translate e-Mail Password reset

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/97

## Problem / goal

Password-reset emails must be available in all five supported languages. The copy is produced in the backend (see `back/app/email_service.py`); align with the project’s translation approach (e.g. `i18n.json` / locale files used elsewhere).

## High-level instructions for coder

- Audit how password-reset (and related auth) emails are built today in `email_service.py` and which strings are hard-coded.
- Add or extend translation sources so every user-visible string in those emails exists for all five locales; wire the sender to pick the recipient’s language (or a documented fallback) consistently with other mail flows.
- Keep behaviour and security unchanged (same links, expiry, no leakage of account existence beyond current design); add or adjust tests if the repo already covers email templates.
- Smoke any path that triggers the reset email in dev if practical.
