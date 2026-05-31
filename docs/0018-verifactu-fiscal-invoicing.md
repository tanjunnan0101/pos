# VeriFactu-oriented fiscal invoicing (tenant modes, server issuance)

## Purpose

This document complements **`docs/0017-billing-customers-factura.md`**. It describes **Spain-oriented preparation** for tax invoicing aligned with **VeriFactu** expectations: **server-authoritative** issuance of a fiscal record per order, persisted **series and sequential number**, storage of **stub request/response JSON** for future AEAT integration, and a **print path** that shows **QR content** and **mandatory disclaimer text** returned after issuance.

## Disclaimer

- **No production AEAT submission** is implemented in this codebase path. Real endpoints, certificates, and payload field mapping **must** follow the **official AEAT technical documentation** and **professional tax advice**. Field mapping in stored JSON is **intentionally a stub** until integrated.
- Enabling **live** mode does **not** by itself satisfy legal filing obligations.

## Tenant configuration

| Setting | Meaning |
|--------|---------|
| **`fiscal_mode`**: `off` | Default. Printing a Factura behaves as before (browser-only HTML). |
| **`fiscal_mode`**: `test` | Staff printing triggers **POST `/orders/{id}/fiscal-invoice/issue`** (stub AEAT; no HTTP call to AEAT). |
| **`fiscal_mode`**: `live` | Same issuance pipeline; numbering is **production-oriented** on the server; **AEAT wire protocol is still not called** until integrated. |
| **`fiscal_invoice_series`** | Prefix for display and allocation (e.g. `VF`). |
| **`fiscal_invoice_next_number`** | Next sequence value; incremented **atomically** when a **new** fiscal row is created (not on re-print). |
| **`fiscal_aeat_api_secret`** | Optional placeholder for future AEAT client credentials; masked in API responses like payment secrets. |

Configure via **Settings → Payments** (fiscal section) or **PUT `/tenant/settings`**.

## API

| Method | Path | Role |
|--------|------|------|
| **POST** | `/orders/{order_id}/fiscal-invoice/issue` | Issue or return existing fiscal metadata (**idempotent** per order). Requires **`order:read`**. |
| **GET** | `/orders/{order_id}/fiscal-invoice` | Read persisted fiscal metadata if present. |

### Issuance rules

- **Tenant isolation**: Order must belong to the caller’s tenant.
- **Soft-deleted orders**: Not found (`404`).
- **Cancelled orders**: Cannot issue (`400`).
- **Order status**: Must be **`paid`** or **`completed`**.
- **Idempotency**: At most **one** fiscal invoice row per `(tenant_id, order_id)`; repeated calls return the same record.

## Frontend

When **`fiscal_mode`** is `test` or `live`, **Print Factura** (orders modal) and **print from edit order** call **issue** first, then render the invoice HTML including the **fiscal block** (QR + text).

## Environment

No global AEAT secrets are required for the stub. Per-tenant secrets use **`fiscal_aeat_api_secret`** (optional). Do not commit real credentials; use **`config.env`** / deployment secrets for shared keys when introduced.

## Testing

1. Set tenant **`fiscal_mode`** to **`test`** and save Settings.
2. Mark an order **paid**, then **Print Factura** — expect success and invoice showing fiscal number + QR block.
3. Set **`fiscal_mode`** to **`off`** — print should match prior behaviour without calling issue (browser-only).
4. Unpaid order with fiscal mode on — issue should fail with a clear error.
