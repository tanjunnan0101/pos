# Order item INSERT fails: `price_cents` null violates NOT NULL

## Source

- **Service:** `pos-postgres` (Docker)
- **UTC window:** since prior log review (`2026-03-23T15:51:52Z`); incident at **`2026-03-23 15:54:28.561 UTC`**
- **Representative lines:**
  ```
  ERROR:  null value in column "price_cents" of relation "orderitem" violates not-null constraint
  DETAIL:  Failing row contains (445, 431, 7, Pozole, 1, null, null, null, f, preparing, ...
  STATEMENT:  INSERT INTO orderitem (order_id, product_id, product_name, quantity, price_cents, ...
  ```

`pos-back` tail in the same window showed no matching Python traceback in the sampled grep (request may have failed at DB layer or been logged elsewhere); confirm with full back logs around **15:54:28Z** if needed.

## High-level instructions for coder

- Trace the code path that builds **`OrderItem`** / executes **`INSERT INTO orderitem`** for staff orders (context: **order_id 431**, **product_id 7**, name **Pozole**).
- Ensure **`price_cents`** (and related monetary fields if required) are always set before insert: resolve from product/catalog, order snapshot, or explicit API payload; reject or default only if product policy allows — **do not** rely on nullable DB values where the column is NOT NULL.
- Reproduce by repeating the UI/API action that added Pozole to that order; add a regression test or assertion if the project has patterns for order-line creation.
- If this is tied to **modifiers / non-catalog lines / imported products**, align with `docs/` and existing order-item create endpoints.
