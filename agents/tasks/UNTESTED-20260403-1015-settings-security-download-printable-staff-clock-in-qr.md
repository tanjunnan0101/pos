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

## Implementation notes (coder)
- **`settings.component.ts`:** Next to **Copy**, **`SETTINGS.CLOCK_QR_DOWNLOAD_PRINT`** button with `data-testid="settings-download-clock-qr-png"`, only when `clockQrLastToken()` and `settings()?.clock_qr_active`. Payload URL: `origin + '/my-shift?clock_qr=' + encodeURIComponent(token)`. PNG via dynamic `import('qrcode')` → `toDataURL` width **1200**, EC level **M**; filename **`staff-clock-in-qr-{tenantId}.png`** (fallback `tenant` if no id).
- **Deps:** `qrcode@1.5.4`, `@types/qrcode@1.5.6` in **`front/package.json`** / lockfile.
- **i18n:** `SETTINGS.CLOCK_QR_DOWNLOAD_PRINT`, `SETTINGS.CLOCK_QR_DOWNLOAD_FAILED` in all **`front/public/i18n/*.json`**.

## Testing instructions
1. **Build:** From `front/`, `npm ci --ignore-scripts` then `npx ng build --configuration=development`. **Docker dev:** Compose uses an anonymous volume for `/app/node_modules` in the `front` service — after lockfile changes run `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec front sh -c "cd /app && npm ci --ignore-scripts"`, then `docker compose … restart front`; if HAProxy returns **503**, `docker compose … restart haproxy`.
2. **Manual:** Log in as a user with **Settings** update (same as clock QR regenerate). Open **Settings → Security**. Click **Generate new token** if needed. When the token block appears, confirm **Download QR for printing** is visible. Click it — browser should download **`staff-clock-in-qr-<id>.png`**. Decode the image (phone camera or QR tool): payload must be **`https?://<host>/my-shift?clock_qr=<token>`** matching the current origin and the shown token.
3. **Regression:** `BASE_URL=http://127.0.0.1:4202 npm run test:my-shift-clock-qr --prefix front` (with owner credentials in env) still passes.
4. **Smoke:** With stack up, `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front`.
