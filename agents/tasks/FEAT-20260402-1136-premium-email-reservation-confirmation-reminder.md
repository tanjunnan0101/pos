# Premium email experience: reservation confirmation + reservation reminder (layout, branding, localization)

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/150

## Problem / goal
Stakeholders want transactional reservation emails (confirmation after booking, reminder before visit) to look professional and on-brand: clear hierarchy, readable typography, email-safe HTML, optional tenant logo, strong CTAs where self-service links exist, human-readable localized dates/times using tenant timezone when available. Confirmation should improve defaults and wrappers while preserving owner-customizable placeholders (`reservation_email_template.py` allowlist). Reminder path should be redesigned to match confirmation quality or share a common layout module; align tone and subject with confirmation. Follow existing i18n patterns (`get_message` / messages), escape user content, avoid secrets in logs. See `docs/0030-reservation-confirmation-email-troubleshooting.md` and `docs/0024-whatsapp-reminder-notes.md` where relevant.

## High-level instructions for coder
- Audit `back/app/email_service.py` (confirmation vs `send_reservation_reminder`), `reservation_email_template.py`, and related `main.py` background tasks; plan shared layout/partials without breaking placeholder allowlists.
- Improve HTML structure and default copy for confirmation; ensure custom templates still render inside `wrap_html_email` (or equivalent).
- Redesign reminder HTML/subject to match confirmation quality; consider extracting shared header/footer or styles.
- Wire subject/body strings through existing translation/message infrastructure; document timezone fallback if tenant timezone missing.
- Add or extend tests for rendering and escaping; smoke-test send paths where the environment supports SMTP (without committing secrets).
