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
