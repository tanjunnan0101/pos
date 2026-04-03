# Settings → Security: download printable staff clock-in QR

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- `gh issue list --repo satisfecho/pos --state open --limit 40`
- Optional: `--json number,title,labels,updatedAt,url`
- **Issue:** https://github.com/satisfecho/pos/issues/155

## Problem / goal
Owners need a **printable** staff clock-in QR from **Settings → Security**, in the **Staff clock-in QR** card. When clock QR is enabled and a valid printable URL exists (full app URL with `/my-shift?clock_qr=` and the current token, aligned with how **SETTINGS.CLOCK_QR_URL_HINT** documents the URL), add UI to **generate a high-resolution QR** (PNG or SVG) and **trigger a browser download** for venue printing. Do not surface the raw token in new places beyond what **regenerate** already exposes. Keep **tenant and role** checks consistent with existing clock-QR settings APIs and UI.

## High-level instructions for coder
- Locate Settings → Security clock-QR card and existing token/URL derivation; reuse the same rules as regenerate and documented hint text.
- Add a **Download QR for printing** (or equivalent) control, enabled only when clock QR is active and a printable payload is available.
- Implement client-side QR generation at sufficient resolution for print (PNG or SVG); trigger download with a sensible filename.
- Respect i18n for new strings (`front/public/i18n/*.json` per project rules).
- Verify only authorized roles can use the control; match backend expectations if any endpoint is involved.
- Smoke: open Settings → Security as owner, enable clock QR if needed, download file, confirm QR decodes to the expected URL pattern.
