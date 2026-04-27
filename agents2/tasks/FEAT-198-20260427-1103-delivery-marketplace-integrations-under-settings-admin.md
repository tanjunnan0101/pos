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
