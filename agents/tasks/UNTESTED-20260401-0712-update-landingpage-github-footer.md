# Update landing page (GitHub link in footer)

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/133

## Problem / goal
Add a link to the public GitHub repository in the landing page footer so visitors can find the **pos** project source (repository: `satisfecho/pos`).

## High-level instructions for coder
- Locate the landing page footer component or template and add a clear link to **`https://github.com/satisfecho/pos/`** (label consistent with existing footer/i18n patterns).
- Ensure styling matches the landing page; avoid breaking layout on small viewports.
- If the app uses **ngx-translate**, add keys under **`front/public/i18n/`** per project i18n rules.

---

## Testing instructions

- **Build:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` — no Angular/TS errors after save.
- **Smoke:** `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version` — exit 0.
- **Manual:** Open `/` while logged out; footer shows **Source on GitHub** (or translated label) linking to `https://github.com/satisfecho/pos/` (`data-testid="landing-github"`). Resize viewport — footer wraps without overlap.
