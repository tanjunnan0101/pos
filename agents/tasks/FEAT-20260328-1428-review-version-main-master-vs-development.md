# Review version of main/master vs development

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/115

## Problem / goal
Decidir si conviene integrar **`development` → `master`** y desplegar a producción (p. ej. amvara9) porque hay muchas novedades pendientes. Tras un despliegue, revisar el estado del workflow de despliegue en GitHub. Ejecutar smoke tests contra **https://satisfecho.de** para confirmar que el sitio responde bien y no hay errores **500** ni **503** por fallos del backend.

Contexto de ramas y cuándo promover a **`master`**: **`.cursor/rules/git-development-branch-workflow.mdc`**, **`docs/agent-loop.md`**, **`docs/0001-ci-cd-amvara9.md`**, **`AGENTS.md`** (smoke / Puppeteer).

## High-level instructions for coder
- Comparar el estado de **`master`** frente a **`development`** (commits, changelog, versión en `front/package.json` si aplica) y decidir si procede la promoción según las reglas del repo (ventana ~2 h, cambio grande a producción, o petición explícita en el issue).
- Si se despliega a amvara9: seguir el flujo documentado (`scripts/deploy-amvara9.sh`, migraciones antes de servir tráfico) y verificar la ejecución del action de despliegue en GitHub.
- Tras despliegue o si ya está al día: smoke en **satisfecho.de** (p. ej. landing, rutas críticas, sin 5xx); documentar resultado en el issue **#115**.
- No asumir merge a **`master`** sin alinearlo con la política de promoción; si solo aplica empujar **`development`**, dejarlo claro en el comentario del issue.
