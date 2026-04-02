# My shift: scan venue QR from the page instead of requiring `?clock_qr=` in the URL

## GitHub Issues

- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- **Issue:** https://github.com/satisfecho/pos/issues/151

## Problem / goal

Staff who open **My shift** from normal navigation (without a venue QR URL) currently hit a confusing error and cannot clock in. The product goal is to let staff use the usual app flow, then **prove they are at the venue** from the My shift page—e.g. by scanning the physical venue QR with the device camera—using the same token/URL payload as today’s staff link. Server-side validation of venue tokens must stay strict; do not weaken security or expose secrets in UI or logs.

## High-level instructions for coder

- Review existing My shift / clock-QR flows and any docs under `docs/` that describe shift or QR behavior.
- Add a clear primary action on My shift (e.g. “Scan venue QR”) that opens camera-based scanning and parses the same payload as the current `?clock_qr=` flow.
- After a successful scan, treat the session as clock-QR validated so **Start shift** / **End shift** works consistently (one coherent flow: validate on scan vs. validate immediately before clock actions—pick one and document in the task outcome).
- Ensure copy is user-friendly; avoid telling end users to manually add query strings except possibly as an advanced fallback in internal docs.
- Verify acceptance: clock-in/out works when opening My shift from the sidebar after scanning the venue QR on that page; landing only via bookmarked QR URLs is no longer required.

## Implementation summary

- **Front:** `front/src/app/my-shift/my-shift.component.ts` — primary **Scan venue QR** when venue requires clock QR and the session has no token yet; modal uses **`html5-qrcode`** (`html5-qrcode@2.3.8`) with rear camera when available. Decoded text accepts the same payloads as before: full app URL with `?clock_qr=`, path+query, or raw **64-char hex** token (from `secrets.token_hex(32)`). On success, token is stored in **`sessionStorage`** (`clock_qr_{tenant_id}`) and the existing **`clockQrToken`** signal — same persistence as the **`?clock_qr=`** query-param path (which now funnels through **`persistClockQrToken`**). **Start / end shift** and break flows that require QR still use **`buildClockPayload()`**; no backend or security rule changes.
- **i18n:** New **`MY_SHIFT.*`** keys (scan UI, errors, verified line, updated **`QR_HINT`** / **`ERR_QR`**) in all shipped locale files under **`front/public/i18n/`**.
- **Coherent validation model:** Token is validated **when clock actions run** (existing API + `clock_qr` in body); the client only obtains and stores the token via URL, query on load, or scan — no separate “pre-flight” API.
- **Automated check:** `front/scripts/test-my-shift-clock-qr.mjs` — enables clock QR via API (owner session), re-logins as shift user, asserts **`GET /users/me/clock-qr-status`** and **`.scan-cta`** on `/my-shift`, then disables clock QR. Registered as **`npm run test:my-shift-clock-qr`** in **`front/package.json`**.

## Coder verification (2026-04-02)

- **`npx ng build`** (host): success.
- **Docker dev front:** If **`docker compose … logs front`** shows missing modules or TS errors, **`docker compose … restart front`** after a healthy **`node_modules`** volume usually restores a clean **`ng serve`** (anonymous volume **`/app/node_modules`** must match the image).
- **Puppeteer:** `BASE_URL=http://127.0.0.1:4202 LOGIN_EMAIL=… LOGIN_PASSWORD=… npm run test:my-shift-clock-qr --prefix front` — **PASS** (owner account with `SETTINGS_UPDATE`; optional **`OWNER_EMAIL` / `OWNER_PASSWORD`** if different from staff).
- **Landing smoke:** `SKIP_LANDING_PACKAGE_VERSION_CHECK=1 BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` — **PASS**.

## Testing instructions

### What to verify

- My shift loads **`GET /api/users/me/clock-qr-status`** when the page opens.
- With venue clock QR **required** and **no** token in URL/session, **Scan venue QR** (`.scan-cta`) is shown; copy does not tell users to hand-edit query strings.
- Physical QR scan (manual): camera opens, valid venue QR stores token and shows **Venue verified**; invalid QR shows error + retry; **Start/End shift** still work with existing API validation.
- Regression: **`/my-shift?clock_qr=TOKEN`** still ingests the token and strips the query param.

### How to test

- **Compose:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml` — app at **`http://127.0.0.1:4202`** (HAProxy) unless overridden.
- **Build:** `cd front && npx ng build` (expect success).
- **Automated:** From repo root, with a user that can call **`POST /tenant/settings/clock-qr/regenerate`** (owner/admin) and open **`/my-shift`** (same user or set **`OWNER_*`** / **`LOGIN_*`**):

  ```bash
  export BASE_URL=http://127.0.0.1:4202
  export LOGIN_EMAIL='…' LOGIN_PASSWORD='…'
  # optional: OWNER_EMAIL OWNER_PASSWORD if staff differs from settings user
  npm run test:my-shift-clock-qr --prefix front
  ```

- **Manual:** Settings → enable staff clock QR → log in as staff → **My shift** from sidebar without `clock_qr` in URL → **Scan venue QR** → scan printed QR → confirm shift actions.
- **Optional smoke:** `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` (use **`SKIP_LANDING_PACKAGE_VERSION_CHECK=1`** if footer version ≠ `front/package.json`).

### Pass/fail criteria

- **Pass:** Automated script exits **0**; manual flow shows scan CTA when QR is required and no token; **`?clock_qr=`** regression still works; **`npx ng build`** succeeds; **`docker compose … logs front`** has no compile errors after changes.
- **Fail:** No **`clock-qr-status`** request on My shift load when QR is required, **`.scan-cta`** missing with cleared **`sessionStorage`**, or build/compile errors in the front container logs.
