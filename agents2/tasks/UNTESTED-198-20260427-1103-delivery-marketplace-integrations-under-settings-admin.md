# Delivery marketplace integrations under Settings (admin)

## GitHub Issues
- **Issue:** https://github.com/satisfecho/pos/issues/198
- **198**

## Problem / goal
Expose third-party delivery marketplace connectivity under **Settings → Integrations** (admin), not as a separate top-level staff navigation entry. Support multiple providers (e.g. Uber Eats, Glovo, Deliveroo): per-provider connection status, credential handling **server-side only**, test connection, optional store linkage, catalog/menu mapping between external items and POS products/modifiers, and operational visibility (webhook/API event log with import errors). Architecture should be **provider-agnostic UI** with **pluggable backend adapters** so new brands reuse the same patterns. Ingested orders must flow through the **existing POS order and kitchen pipeline** for MVP—no parallel silo.

## High-level instructions for coder
- Add or extend Settings (admin) with an **Integrations** area dedicated to delivery marketplaces; align layout and navigation with existing settings patterns.
- Implement secure storage and use of credentials on the **backend**; avoid exposing secrets to the browser beyond what is required for OAuth or similar documented flows.
- Provide per-provider surfaces for: connection state, credentials/setup, **test connection**, optional store linkage, mapping UI for external catalog ↔ POS catalog, and logs for inbound events and mapping/import failures.
- Design backend **adapter interfaces** per provider brand; shared routes/services where possible so new adapters plug in without duplicating the whole UI.
- Ensure routed-in orders normalize into the same **Order** model and kitchen/service flow already used elsewhere; verify multi-tenant scoping matches adjacent tenant APIs.
- Add testing appropriate to scope: targeted API tests and/or Puppeteer smoke if a stable entry path exists; document manual verification steps for integrations that need external sandbox credentials.

## Testing instructions

1. **Migrate:** From repo root with Docker dev stack up:  
   `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m app.migrate`
2. **Unit tests:**  
   `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m pytest tests/test_delivery_credentials.py tests/test_delivery_adapters.py -q`
3. **UI (admin):** Open **Settings** → **Integrations**. Expand a provider (e.g. Uber Eats). Enter credentials JSON `{"api_key":"test"}` (stub requires non-empty `api_key`), save, run **Test connection** (expect success). Optionally set external store id. Add at least one **catalog mapping** (external item id → POS product), save mappings. Enable the integration and **copy webhook URL**.
4. **Webhook ingest:** `POST` JSON to the copied URL (same shape as stub):  
   `{"external_order_ref":"demo-1","customer_name":"Demo","lines":[{"external_item_id":"<your mapped sku>","quantity":1}]}`  
   Expect **200** and a new row in **Recent events**. Confirm **Orders** shows a new order with table label **Delivery** and kitchen pipeline items.
5. **Smoke:** `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:4202/` → **200** (when stack is up).
