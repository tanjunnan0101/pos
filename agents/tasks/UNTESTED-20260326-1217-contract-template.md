# Contract Template

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/106

## Problem / goal

Provide a **database-backed** way to manage **contract templates**: each template is tied to a **language** and a **restaurant (tenant)**. Offer **sensible default templates** based on where the restaurant is located (e.g. Spain → Spanish defaults, India → India-oriented defaults, extensible to more regions). The issue includes a long **example Spanish temporary employment contract** (camarero/a, full time) as reference content for clauses and placeholders—not necessarily verbatim production legal text.

Related prior work may exist under **staff contracts** / **contract templates** (see `docs/`, migrations, and closed tasks around employment contract templates); this issue emphasizes **locale- or country-driven defaults** and the **template catalog** concept.

## High-level instructions for coder

- Review existing **`staff_contract` / template** models, APIs, and Settings UI so new work **extends** rather than duplicates what is already shipped for tenant-managed templates.
- Design or extend the **data model** so templates support **language** and **tenant**, and so **system or seeded defaults** can be selected or suggested from **restaurant location / jurisdiction** (without hard-coding only Spain—make the rule pluggable or data-driven where practical).
- Define how **defaults** are applied when a tenant has no custom templates yet (seed, migration, or admin tooling—align with project migration and seed patterns).
- Preserve **tenant isolation**, **RBAC** consistent with existing contract permissions, and avoid logging full template bodies in application logs.
- Add or update **API + staff UI** flows so owners can see/use geography- and language-appropriate templates alongside any existing custom template CRUD.
- Cover behavior with **tests** (backend at minimum) and confirm **frontend build** stays clean per project conventions.

## Implementation summary (coder)

- **DB:** `tenant.country_code`; `staff_contract_template.locale`; table `staff_contract_template_preset` + seeded rows (ES/es, IN/en, `*` / en). Migration `back/migrations/20260326133000_contract_template_locale_presets.sql`.
- **API:** `GET /staff-contract-templates/presets`, `POST /staff-contract-templates/import-preset`; template CRUD extended with `locale`; `PUT /tenant/settings` accepts `country_code`.
- **Backend logic:** `staff_contract_template_presets.py` — infer country when unset (INR→IN, CIF→ES, timezone hints), rank presets vs tenant `country_code` + `default_language`.
- **UI:** Settings → Business: optional country code. Settings → Contract templates: catalog block + locale on own templates.

## Testing instructions

1. Apply migrations: `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m app.migrate`
2. Backend: `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python3 -m pytest tests/test_staff_contract_templates.py -q`
3. Frontend build: `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front` (no TS errors after reload)
4. Smoke: `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`
5. Manual: log in as user with `staff_contract:manage` → Settings → **Contract templates** — confirm preset table loads, **Import** adds a row, **Language** column and edit form locale work; **Business** section — save **Country (ISO code)** (e.g. ES) and verify presets reorder (ES/es template first when language matches).
