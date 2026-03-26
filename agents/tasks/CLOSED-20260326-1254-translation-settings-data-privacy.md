# Translation needed for Settings > Data and privacy

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/108

## Problem / goal
Staff **Settings → Data & privacy** is English-only. The section must be translated for every locale the app already supports (same coverage as other settings areas). Align keys, JSON files under `front` i18n, and any backend strings if this section touches API messages.

## High-level instructions for coder
- Locate the Data & privacy settings UI and list all user-visible strings (titles, labels, hints, buttons, legal/helper text).
- Add or complete translation keys and entries in each supported language bundle (match existing i18n patterns for Settings).
- Manually spot-check switching languages: Data & privacy reads fully localized with no English fallbacks.
- If copy is shared with emails or exports, ensure those paths use the same keys or explicit locale handling where applicable.

## Implementation (coder)

- **UI:** `front/src/app/settings/settings.component.ts` — Data & privacy block already uses `SETTINGS.DATA_EXPORT_*`, `SETTINGS.DANGER_ZONE_*`, `SETTINGS.PURGE_*`, `SETTINGS.DATA_AND_PRIVACY_TAB` (no template changes).
- **Locales:** Added the full data-privacy key set to **`es.json`**, **`fr.json`**, **`ca.json`**, **`zh-CN.json`**, **`hi.json`** (previously absent → ngx-translate fell back to English). **`bg.json`:** translated `PURGE_CONFIRM_LABEL` from English. **`en.json`** / **`de.json`** already complete.

## Testing instructions

1. Run **`python3 -m json.tool front/public/i18n/<locale>.json`** on edited files (or the loop over `front/public/i18n/*.json`) — all must parse.
2. With the app up (e.g. Docker HAProxy **`http://127.0.0.1:4202`**), log in as **tenant owner** (purge/export are owner-only), open **Settings**, click **Data & privacy** (tab label must be localized).
3. For each shipped language (**en**, **de**, **es**, **fr**, **ca**, **bg**, **zh-CN**, **hi**): switch app language, reload Settings → Data & privacy, confirm **no English** in titles, descriptions, labels, or buttons (except business name placeholder reflecting the tenant’s actual name).
4. Smoke: **`cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`** (passes exit 0).

**Note:** API purge errors may still return an English `detail` string from the backend; the UI falls back to **`SETTINGS.PURGE_FAILED`** when `detail` is not a string.

---

## Test report

1. **Date/time (UTC):** 2026-03-26 13:09–13:11 (verification window). **Log window:** `pos-front` tail ~80 lines ending ~13:00Z rebuild entries (no errors in excerpt).

2. **Environment:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml`; **`BASE_URL`** `http://127.0.0.1:4202`; branch **`development`** @ **`8517e20`**.

3. **What was tested:** Instructions §1–4 (JSON validity, owner Settings → Data & privacy per locale, landing smoke).

4. **Results**
   - **§1 JSON parse (all `front/public/i18n/*.json`):** **PASS** — `for f in front/public/i18n/*.json; do python3 -m json.tool "$f" >/dev/null; done` exit 0.
   - **§2–§3 Localized Data & privacy (tab + section copy vs locale files):** **PASS** — Headless Puppeteer (Chrome): tenant **1** owner login from repo `.env`; for each of **en, de, es, fr, ca, bg, zh-CN, hi**: set `localStorage.pos_language`, reload, `/settings` → `[data-testid="settings-data-privacy-tab"]` label contains `SETTINGS.DATA_AND_PRIVACY_TAB` from that locale; `[data-testid="settings-data-privacy-section"]` contains full strings for `DATA_EXPORT_TITLE`, `DATA_EXPORT_DESC`, `DATA_EXPORT_BUTTON`, `DANGER_ZONE_TITLE`, `DANGER_ZONE_DESC`, `PURGE_CONFIRM_LABEL`, `PURGE_BUTTON`; non-**en** locales do **not** contain English `DATA_EXPORT_TITLE` (“Download your data”). **Evidence:** run ended with `ALL_LOCALES_PASS`, exit 0 (~59s). Script: ephemeral `/tmp/test-settings-data-privacy-i18n.mjs` with `NODE_PATH=front/node_modules`, `REPO_ROOT` = repo root (not committed).
   - **§4 Smoke `test:landing-version`:** **PASS** — exit 0; output includes `>>> RESULT: Landing version OK; demo login (tenant=1) OK; sidebar nav OK.`

5. **Overall:** **PASS**

6. **Product owner feedback:** Data & privacy now tracks the translation files for every shipped language: tab and body copy match the JSON entries, and non-English locales no longer show the English export heading. Purge/export actions were not executed (verification is copy-only). Consider adding a checked-in Puppeteer script under `front/scripts/` if you want this regression-tested in CI without a temp harness.

7. **URLs tested**
   1. `http://127.0.0.1:4202/login?tenant=1`
   2. `http://127.0.0.1:4202/settings` (eight times after language switches)
   3. `http://127.0.0.1:4202/` (landing smoke)
   4. Additional routes from `test:landing-version` sidebar/inventory navigation (dashboard, orders, reservations, …, settings)

8. **Relevant log excerpts**
   - **pos-front (compose logs --tail=80):** `Application bundle generation complete.` / no `ERROR` or `NG` compiler failures in the captured tail.
   - **Note:** `test:landing-version` browser console showed WebSocket `Invalid authentication token` (code 1008) on some pages; test still **PASS**; unrelated to i18n task.

**GitHub:** Comment posted at start of verification. `gh issue edit` to set label **`agent:testing`** failed (**label not defined** in repo); closer/human can align labels if needed.
