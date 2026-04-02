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

## Testing instructions

1. **Build:** `cd front && npx ng build` (expect success).
2. **Tenant:** Enable staff clock QR in **Settings** (generate token; optional: note **`/my-shift?clock_qr=…`** URL for a printed QR).
3. **Flow:** Log in as staff → open **My shift** from the sidebar (no `clock_qr` in URL). Confirm **Scan venue QR** appears and **ERR_QR** no longer tells users to add query strings manually.
4. **Scan:** Use a device/browser with camera; tap **Scan venue QR**, allow camera; scan the venue QR (or a QR encoding the same URL/token). Confirm **Venue verified for this session** appears and **Start shift** / **End shift** (and break actions if applicable) work. If **GPS at venue** is enabled, still allow location when prompted.
5. **Negative:** Scan a random non-venue QR → expect invalid message and **Try again**; cancel closes the modal.
6. **Regression:** Open **`/my-shift?clock_qr=TOKEN`** in one tab — token should still be picked up and stripped from the URL as before.

Optional smoke: `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` (may fail if landing version banner ≠ `front/package.json` — environment-specific).

---

## Test report

1. **Date/time (UTC):** 2026-04-02 ~15:23–15:28 (log window aligned to this run).
2. **Environment:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml`; `BASE_URL=http://127.0.0.1:4202`; branch `development` (synced). Front container: ran `npm ci --ignore-scripts` then `npx ng build` under `/app` for build verification.
3. **What was tested (from Testing instructions):** §1 production build; §2 tenant clock QR enabled in DB for tenant `1` during checks, then **disabled** again after testing; §3–§6 browser/network flows against local HAProxy; optional landing smoke with `SKIP_LANDING_PACKAGE_VERSION_CHECK=1`; static review of `MY_SHIFT.ERR_QR` / `QR_HINT` in `front/public/i18n/en.json`.
4. **Results:**
   - **§1 Build (`npx ng build`):** **PASS** — succeeds after `npm ci` in the `front` container (first attempt failed: `html5-qrcode` not resolved until lockfile install).
   - **§3 Flow (Scan venue QR + copy):** **FAIL** — With tenant clock QR required (`clock_qr_token_hash` set) and `sessionStorage` cleared, a Puppeteer session logged in and opened `/my-shift`. **No** request to `GET /api/users/me/clock-qr-status` appeared; the **Scan venue QR** primary control (`.scan-cta`) was **not** in the DOM. Current source on disk includes `forkJoin({ … qr: this.api.getMyClockQrStatus() })` in `refreshAll()`, so the running dev bundle on port 4202 does **not** match the workspace (likely stale/failed `ng serve` compile; `docker compose logs front` shows many TypeScript errors in unrelated files such as `server.ts` / environments).
   - **§4 Scan (camera):** **NOT RUN** — blocked by missing UI above; headless environment also limits real camera QR validation.
   - **§5 Negative QR / cancel:** **NOT RUN** — same.
   - **§6 Regression `?clock_qr=`:** **NOT RUN** — blocked by missing clock-qr-status integration in the live bundle behavior observed.
   - **Optional landing smoke:** **PASS** with `SKIP_LANDING_PACKAGE_VERSION_CHECK=1` (login + sidebar including `/my-shift`); without skip, version check fails as documented (footer `2.0.64` vs `package.json` `2.0.69`).
   - **i18n (ERR_QR no manual query-string instructions):** **PASS** — `ERR_QR` / `QR_HINT` text in `en.json` does not instruct users to add query strings manually.
5. **Overall:** **FAIL** — failed criteria: §3, §4, §5, §6 (live app on 4202 did not exhibit the new My shift clock-QR API path or Scan UI despite DB and source indicating the feature).
6. **Product owner feedback:** Production `ng build` for the current tree succeeds and the implementation summary matches the source, but **local Docker dev** did not serve an updated My shift bundle: the browser never called `/users/me/clock-qr-status`, so staff cannot verify scan or regression in this environment until the front dev build is healthy and redeployed. Recommend fixing front compile errors (see `docker compose logs front`), restarting the front service, and re-running §3–§6; then return the task to **UNTESTED**.
7. **URLs tested (numbered):**
   1. `http://127.0.0.1:4202/`
   2. `http://127.0.0.1:4202/login?tenant=1`
   3. `http://127.0.0.1:4202/dashboard` (post-login)
   4. `http://127.0.0.1:4202/my-shift` (multiple times during Puppeteer)
8. **Relevant log excerpts:** `pos-front` logs show repeated Angular compiler errors (e.g. `server.ts`, `environment.staging.ts`), indicating the dev server is not in a clean compile state — sample: `TS2304: Cannot find name 'window'` in `src/environments/environment.ts` (see `docker compose … logs front`).

**DB note:** Tenant `1` `clock_qr_token_hash` was cleared after testing so local data matches “clock QR off” unless re-enabled in Settings.
