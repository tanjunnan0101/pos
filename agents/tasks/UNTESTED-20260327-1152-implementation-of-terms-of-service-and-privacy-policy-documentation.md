# feat: implementation of Terms of Service and Privacy Policy documentation

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/113

## Problem / goal
Formalizar documentación legal para cumplir requisitos de APIs externas (p. ej. TikTok Login Kit): redactar **Términos de servicio (ToS)** y **Política de privacidad** para `satisfecho.de`, publicarlas en rutas públicas accesibles y usables como URLs oficiales en configuración OAuth (“Global Config”). El contenido debe ser coherente con GDPR/transparencia y con el branding actual; responsive en móvil.

## High-level instructions for coder
- Revisar si ya existen rutas o contenido legal en el front (p. ej. `/terms`, `/privacy`, componentes legales, `legal-urls`) y alinear con el issue sin duplicar trabajo cerrado en #110 si aplica.
- Implementar o completar páginas públicas que respondan en producción como `https://satisfecho.de/terms` y `https://satisfecho.de/privacy` (sin 404); ver despliegue/nginx/HAProxy según `docs/` si hace falta.
- Asegurar que el texto y la estructura cubran recogida, uso y almacenamiento de datos de usuario de forma razonable para GDPR; coordinar redacción legal con el propietario del producto si el repo no debe contener texto legal definitivo.
- Verificar enlaces desde flujos que requieran ToS/privacidad (registro, reservas, OAuth) y que las URLs configurables apunten a estas páginas tras el despliegue.

## Coder notes (implementation)
- **Front:** Rutas públicas `terms` y `privacy` en `app.routes.ts`; componente `front/src/app/legal/legal-document.component.ts` (selector de documento vía `data.legalDoc`). Texto en `LEGAL.DOC.*` (en/de/es/fr/ca completos; bg/zh-CN/hi reutilizan el cuerpo EN para las mismas claves).
- **Back:** `_global_terms_url()` / `_global_privacy_url()` en `main.py`: si las env explícitas están vacías y `PUBLIC_APP_BASE_URL` es http(s) válida, se devuelve `{base}/terms` y `{base}/privacy`. Misma lógica vía `_legal_urls_effective` para resúmenes de tenant. Tests en `tests/test_guest_feedback.py`.
- **Config:** `config.env.example` — ejemplos `satisfecho.de` y nota de fallback; sin cambios nginx/HAProxy necesarios (SPA ya sirve `index.html` para rutas desconocidas en prod).

---

## Testing instructions

### What to verify
- `/terms` y `/privacy` cargan (200) en el front detrás de HAProxy y muestran título, secciones, enlace cruzado y “volver al inicio”.
- `GET /api/public/legal-urls` (o `/public/legal-urls` según montaje) devuelve URLs https cuando `PUBLIC_APP_BASE_URL` está definida y las env de términos/privacidad están vacías.
- Pytest `test_guest_feedback` pasa (incl. nuevos casos de fallback y override explícito).

### How to test
- Con stack dev: `docker compose -f docker-compose.yml -f docker-compose.dev.yml`
- `curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:4202/terms` y `…/privacy` → esperado `200`.
- Opcional: `curl -s http://127.0.0.1:4202/api/public/legal-urls` (ajustar host/puerto según `ROOT_PATH`) con `PUBLIC_APP_BASE_URL` en `config.env`.
- `docker compose … exec -T back python3 -m pytest tests/test_guest_feedback.py -q`
- Smoke: `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`

### Pass / fail criteria
- **Pass:** Las cuatro comprobaciones anteriores OK; sin errores de compilación en logs del contenedor `front`.
- **Fail:** 404 en `/terms` o `/privacy`, JSON `legal-urls` sin fallback cuando toca, o tests en rojo.
