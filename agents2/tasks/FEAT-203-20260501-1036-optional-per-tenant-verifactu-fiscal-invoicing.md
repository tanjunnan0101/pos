# Optional per-tenant VeriFactu-ready fiscal invoicing (server-side issuance, AEAT hooks, print path)

## GitHub Issues

- **Issue:** https://github.com/satisfecho/pos/issues/203
- **203**

## Problem / goal

Multi-tenant POS (FastAPI + Angular): Spain-oriented fiscal invoicing should move toward VeriFactu readiness with **server-authoritative issuance** (persisted fiscal documents scoped by tenant and order), preparation for **AEAT** submission using **official technical documentation** (do not invent endpoints or payload shapes), and a **print path** that can render QR and mandated verification text from data returned after issuance. Today the printable invoice is generated only in the browser (`printInvoice()` in orders flow); there is no persisted fiscal entity or official series/numbering. Billing customers and related APIs are described in `docs/0017-billing-customers-factura.md`. Staff trigger printing from the Print Factura flow and the edit-order flow—both must stay consistent when fiscal mode is enabled.

## High-level instructions for coder

- Read `docs/0017-billing-customers-factura.md`; add a focused VeriFactu note under `docs/` (modes, env vars, test vs production, explicit disclaimer that field mapping follows AEAT spec and tax advisor input).
- **Backend:** SQL migrations; model(s) for issued fiscal documents linked to `order.id` and `tenant_id` with official series/number, payload/response storage, status, timestamps; new authenticated endpoints mirroring tenant isolation and auth patterns used by existing order routes in `main.py`; define idempotency (re-print vs duplicate issue) and rules for order state (e.g. paid-only), cancelled, and soft-deleted orders; pytest for permissions, tenant isolation, and success/error paths.
- **Tenant configuration:** Extend Tenant, TenantUpdate, and PATCH handler for fiscal mode (off / test / live); store secrets like other integrations (per-tenant fields and/or `config.env.example` placeholders)—never commit real credentials; optional UX gating when `country_code` is not ES is not a legal substitute.
- **Frontend:** `settings.component.ts` and API service for new settings; when fiscal mode is on, both Print Factura and print-from-edit-order call backend to issue or fetch fiscal metadata, then extend `printInvoice()` HTML or extract a small service for QR and legal strings; add `ngx-translate` keys in all `front/public/i18n/*.json` files for new copy.
- **Permissions:** Decide whether issuance matches existing roles that can print today or requires a new capability in `permissions.py`; keep behaviour aligned with who can print now.
- **Non-goals:** Do not ship guessed production AEAT calls without verified spec and tests; thermal printers only render supplied content.
- **Verification:** With stack up, smoke Puppeteer or manual checks: tenant off → current print unchanged; tenant on (stub or test env) → issuance API returns data and print includes QR block without breaking unpaid/cancelled rules.
