# Push develop to master

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/112

## Problem / goal
Tras promover **`development` → `master`**, el autor del issue indica que hubo un problema y pide revisarlo y resolverlo. El texto del issue es breve; hace falta **aclarar qué falló** (despliegue, CI, app en producción, migraciones, SSL, etc.) y corregirlo o documentar el siguiente paso.

Contexto de política de ramas: **`.cursor/rules/git-development-branch-workflow.mdc`**, **`docs/agent-loop.md`**, **`docs/0001-ci-cd-amvara9.md`** (si aplica amvara9). La tarea anterior relacionada (**#111**) quedó archivada en **`agents/tasks/done/2026/03/27/CLOSED-20260327-1001-push-from-develop-to-master.md`** — úsala como referencia de lo que ya se hizo en git, sin asumir que el problema actual sea el mismo.

## High-level instructions for coder
- Reproducir o localizar el fallo concreto (preguntar en el issue si hace falta más detalle: URL, error en pantalla, hora aproximada, entorno).
- Si es **producción / amvara9**: seguir **`AGENTS.md`** / **`docs/error-investigation-workflow.mdc`** — logs Docker en servidor, HAProxy, migraciones, `config.env`.
- Si es **CI o build**: revisar el pipeline y el último merge a **`master`**; alinear con el estado de **`development`**.
- Corregir en código o configuración según corresponda; añadir pruebas o smoke acordes al cambio (**`docs/testing.md`**).
- Dejar comentario en **#112** con causa raíz y verificación; actualizar etiquetas del issue según el flujo del equipo.

## Implementation (feature coder 006, 2026-03-27 UTC)

- **Causa raíz (amvara9):** Un despliegue alrededor de **10:05 UTC** detuvo **front / back / haproxy / ws-bridge** (`deploy-amvara9.sh` fase *Stopping app-tier*). El script no llegó a **`up -d`** porque **`python -m app.migrate` falló**: en la BD ya existía **`staff_contract_template_preset`** (vacía) **sin** la restricción **`uq_staff_contract_template_preset_region_locale_key`**. Con **`CREATE TABLE IF NOT EXISTS`** PostgreSQL no recrea la tabla, así que el **`INSERT … ON CONFLICT (region_code, locale, template_key)`** fallaba. El código en imagen ya esperaba **`tenant.country_code`**, lo que generaba errores en arranque si el backend hubiera estado arriba sin migrar.
- **Código:** En **`back/migrations/20260326133000_contract_template_locale_presets.sql`** se añadió un bloque **`DO $preset_uq$ … END`** idempotente que hace **`ALTER TABLE … ADD CONSTRAINT … UNIQUE (region_code, locale, template_key)`** solo si falta el constraint.
- **Producción:** Tras integrar el fix en **`master`** y **`git pull`** en **`/development/pos`**, ejecutar migraciones y **`docker compose --env-file config.env -f docker-compose.yml -f docker-compose.prod.yml up -d --remove-orphans`** (o **`bash scripts/deploy-amvara9.sh`** para un despliegue completo con rebuild).

## Testing instructions

1. **Migración (local):** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python -m app.migrate` → termina sin error (BD ya al día o aplica pendientes).
2. **amvara9:** Tras pull de **`master`**, `… run --rm back python -m app.migrate` y `… run --rm back python -m app.migrate --sync-idempotent` → OK; `… ps` → **haproxy**, **front**, **back**, **ws-bridge**, **db**, **redis** en **Up** (no solo db/redis).
3. **Humo público:** Desde una red que alcance el servidor, `curl -sS -o /dev/null -w "%{http_code}\n" https://satisfecho.de/` → **200**.
4. **Esquema:** En PostgreSQL, `\d tenant` incluye **`country_code`**; `\d staff_contract_template_preset` lista la restricción **`uq_staff_contract_template_preset_region_locale_key`** (o equivalente UNIQUE en esas columnas).
