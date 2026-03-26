# Postgres: FATAL — role "postgres" does not exist

## Source

- **Service:** `pos-postgres` (`docker logs pos-postgres`)
- **UTC window:** since prior **001** review stamp **2026-03-26T09:33:22Z** through this sweep (**~2026-03-26T11:21Z**).
- **Representative lines:**
  ```
  2026-03-26 10:57:39.359 UTC [92354] FATAL:  role "postgres" does not exist
  ```

Compose defaults use **`POSTGRES_USER`** **`pos`** (not the conventional superuser name `postgres`). A client is connecting with username **`postgres`**, which is invalid for this instance. Prior **001** notes treated an earlier occurrence as a possible one-off; this run shows **another** hit in the window — worth tracing the source (host tool, wrong `psql`/GUI DSN, third-party image, copy-pasted connection string, etc.) and aligning docs or env examples if needed.

## High-level instructions for coder

- Identify what initiated the connection (correlate **PID**/timestamp with host processes or other containers if possible; check common culprits: IDE DB plugins, manual `psql`, monitoring, backup scripts).
- Confirm **`config.env` / `docker-compose`** expectations: app and operators should use **`POSTGRES_USER`** (e.g. `pos`), not assume role `postgres`.
- If the connection is from developer ergonomics only, document the correct user in **`README.md`** or **`docs/`** (where DB access is described) so the FATAL does not recur from confusion.
- Do **not** treat this as a GitHub-issue queue item unless product requirements say otherwise; fix config/tooling or document, not necessarily add a `postgres` role to the DB.
