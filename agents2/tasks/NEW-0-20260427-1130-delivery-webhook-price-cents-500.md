# Delivery webhook intermittent 500 — `price_cents` / ingest path

## GitHub Issues

- **Related scope:** https://github.com/satisfecho/pos/issues/198 (delivery integrations; may remain open for ops tracking).
- **No dedicated GitHub issue** for this follow-up — queued as **`NEW-0`** from Docker log triage.

## Problem / goal

Live **`docker logs pos-back`** shows **`POST /public/webhooks/delivery/<ingest_token>`** returning **500** with **`KeyError` / `AttributeError: price_cents`** for some payloads; subsequent posts can return **200**. Preflight **`pos-front`** **`delivery-integrations`** TypeScript noise in the digest was **transient** during rebuild; recent logs show **`Application bundle generation complete`** — no separate front **`NEW-*`**.

Harden webhook order creation so missing or oddly shaped **price** fields and **`Row`** vs model access cannot crash ingest.

## High-level instructions for coder

- Confirm with **`docker logs pos-back`** (grep **`webhooks/delivery`**, **`price_cents`**, **`KeyError`**) and add a **pytest** case for the payload shape that triggers **500**.
- Review **`create_order_from_delivery_payload`** (and **`delivery_order_service`**) per archived **`CLOSED-198`** notes: avoid **`Row`** `.price_cents` pitfalls; use **`session.get(Product, …)`** with tenant checks where applicable.
- Default or derive **`price_cents`** safely when webhook line items omit it (mapping / catalog fallback).
- Run delivery-related **`pytest`** and re-check webhook **POST** returns **200** for the failing fixture.
