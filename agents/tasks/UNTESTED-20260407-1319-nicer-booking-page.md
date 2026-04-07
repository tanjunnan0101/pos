# Nicer booking page

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- `gh issue list --repo satisfecho/pos --state open --limit 40`
- Optional: `--json number,title,labels,updatedAt,url`
- **Issue:** https://github.com/satisfecho/pos/issues/173

## Problem / goal
Improve the public booking page (example tenant URL in issue: `/book/1081` on local dev). **Readability:** the `hero-content` area should use styling (background, rounded corners, padding/margins) so text stays readable over the existing background image—keep the image, improve contrast and legibility. **Links:** when the restaurant has a website URL configured, expose it as a normal clickable link in the UI.

## High-level instructions for coder
- Locate the booking page component/template and styles for the hero section; align with existing design tokens and `front/public/i18n` for any new strings.
- Implement a readable overlay or panel for hero text (background, radius, spacing) without removing the background image.
- Wire the restaurant website field so it renders as a proper anchor (`href`, accessibility, open behavior per product norms).
- Smoke-test the public booking flow for at least one tenant; verify responsive layout.

## Implementation summary (feature coder)
- **Front:** `book.component.html` — wrapped hero logo + info in `.hero-content-panel`; added website link when `tenant().website` is set (`target="_blank"`, `rel="noopener noreferrer"`). **Styles:** `.hero-content-panel` — rounded panel, padding, border, backdrop blur; stronger tint when `.hero-header.has-bg-image`.
- **API:** `TenantSummary.website` + `_tenant_to_summary` uses `_normalize_public_http_url(t.website)`. **`get_public_tenant`** explicit JSON body now includes **`website`** (was omitted; list endpoint already returned the model).
- **Types:** `TenantSummary.website` in `api.service.ts`.
- **i18n:** `BOOK.WEBSITE` in all `front/public/i18n/*.json`.
- **Tests:** `tests/test_public_tenant_whatsapp.py` — asserts `website` key and value when set.

## Testing instructions
1. **Backend:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec -T back python3 -m pytest tests/test_public_tenant_whatsapp.py -q` — all pass.
2. **API:** `curl -s "http://127.0.0.1:4202/api/public/tenants/1"` — JSON includes `"website"` (normalized `https://…` or `null`).
3. **Browser:** Open `/book/1` (or a tenant with header image + website in settings). Confirm hero text sits on a readable frosted panel; **Website** link opens the restaurant URL in a new tab when configured.
4. **Smoke:** With stack on port 4202: `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`.
