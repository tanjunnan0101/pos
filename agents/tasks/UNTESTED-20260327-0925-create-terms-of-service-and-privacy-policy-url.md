# Create Terms of Service URL and a Privacy Policy URL

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/110

## Problem / goal
El producto necesita URLs accesibles (y enlazables desde la app) para **Términos del servicio** y **Política de privacidad**, típicamente requeridas en registros, pies de página públicos, cumplimiento y tiendas de aplicaciones. El issue no detalla si deben ser rutas internas estáticas, páginas por tenant o enlaces externos configurables; el implementador debe alinearlo con el modelo multi-tenant y con **Settings** / datos públicos existentes. Revisar **`docs/`** y **landing / registro / ajustes** si ya hay huecos para legales o “data & privacy”.

## High-level instructions for coder
- Definir dónde viven las URLs (p. ej. campos en tenant/settings, constantes de producto, o páginas estáticas bajo rutas públicas) y cómo se resuelven en **dev** vs **producción**.
- Exponer las URLs en la API si el front las necesita desde el backend; mantener **alcance por tenant** donde aplique.
- Añadir o completar enlaces en los flujos de usuario relevantes (registro, login público, pie de página, formularios que recojan datos personales) con **i18n** coherente.
- Documentar en **README** o **`config.env.example`** cualquier variable nueva (p. ej. URL base de documentos legales) sin secretos.
- Cubrir con pruebas humo/Puppeteer si toca una ruta o formulario nuevo; comprobar logs del front tras cambios Angular.

## Implementación (resumen)
- **BD / modelo:** `tenant.public_terms_of_service_url`, `tenant.public_privacy_policy_url` (VARCHAR 2048); migración `20260327100000_public_terms_privacy_urls.sql`.
- **Config global:** `PUBLIC_TERMS_OF_SERVICE_URL`, `PUBLIC_PRIVACY_POLICY_URL` en `config.env` / `back/app/settings.py`.
- **API:** `GET /public/legal-urls` (solo globales); en `GET /public/tenants` y `GET /public/tenants/{id}` los campos efectivos `terms_of_service_url` y `privacy_policy_url` (tenant si hay URL válida, si no fallback global). `PUT /tenant/settings` acepta los dos campos `public_*` con la misma normalización http(s) que Maps.
- **Front:** `LegalLinksComponent`; landing, login, registro, `/book/:id`, feedback público; ajustes en pestaña Datos y privacidad (junto a enlaces de mapas). i18n en todos los idiomas embarcados. Versión **2.0.64**.

## Testing instructions
1. **Migración:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python3 -m app.migrate` (versión de esquema incluye `20260327100000`).
2. **Backend:** `docker compose -f docker-compose.yml -f docker-compose.dev.yml exec back python3 -m pytest tests/test_guest_feedback.py -q` (incluye `/public/legal-urls` y URLs efectivas en tenant público).
3. **Opcional env:** en `config.env` definir `PUBLIC_TERMS_OF_SERVICE_URL` y `PUBLIC_PRIVACY_POLICY_URL` con URLs `https://…`; reiniciar `back`; comprobar que aparecen enlaces en landing y login sin estar logueado.
4. **Tenant:** en Settings → Datos y privacidad rellenar URLs propias; guardar; abrir `/book/1` (o tenant de prueba) y comprobar pie con enlaces; comprobar que prevalecen sobre el global si ambos están definidos.
5. **Front:** `docker compose … logs --tail=80 front` sin errores de compilación; humo: `cd front && BASE_URL=http://127.0.0.1:4202 npm run test:landing-version`.
6. **API manual:** `curl -s http://127.0.0.1:4202/api/public/legal-urls` (vía HAProxy) debe devolver JSON con `terms_of_service_url` y `privacy_policy_url` (null o strings).
