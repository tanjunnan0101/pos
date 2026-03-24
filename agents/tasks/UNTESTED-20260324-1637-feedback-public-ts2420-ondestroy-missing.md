# pos-front: TS2420 FeedbackPublicComponent missing ngOnDestroy (dev rebuild)

## Source

- **Service:** `pos-front` (`docker logs pos-front`).
- **UTC window:** After prior log review **2026-03-24T16:20:00Z**; failure timestamp **2026-03-24T16:26:41.224Z**; successful **Application bundle generation complete** at **2026-03-24T16:26:49.341Z** (and later rebuilds through **16:28:15.820Z**).
- **Representative lines:**
  - `Application bundle generation failed. [0.297 seconds] - 2026-03-24T16:26:41.224Z`
  - `TS2420: Class 'FeedbackPublicComponent' incorrectly implements interface 'OnDestroy'. Property 'ngOnDestroy' is missing in type 'FeedbackPublicComponent' but required in type 'OnDestroy'.` (`feedback-public.component.ts:19`)

## High-level instructions for coder

- Confirm `FeedbackPublicComponent` either implements `OnDestroy` with a real `ngOnDestroy()` or drops the interface if nothing to tear down; align with Angular compiler expectations so dev hot-reload does not intermittently fail the bundle.
- Re-check related lifecycle / subscription cleanup if `OnDestroy` is kept (see archived `agents/tasks/done/2026/03/25/CLOSED-20260325-1030-feedback-typeerror-ondestroy.md` for prior context on the same component).
- After change, watch `docker compose … logs --tail=80 front` for a clean rebuild on save.

## Coder notes (implementation)

- **Cause:** **TS2420** appears when the class **`implements OnDestroy`** but **`ngOnDestroy`** is missing (e.g. partial save or bad merge during hot reload).
- **Fix (current tree):** Keep **`OnDestroy`** with a real **`ngOnDestroy()`** that unsubscribes **`titleI18nSub`**. Do **not** add **`takeUntilDestroyed`** on the inner **`translate.get(key)`** subscription: **`[2.0.53]`** changelog documents that production-static builds need that omission so **`document.title`** updates on satisfecho.de (GitHub **#67**). Merged translate events still use **`takeUntilDestroyed(this.destroyRef)`**; **`titleI18nSub?.unsubscribe()`** before each **`get()`** resubscribe avoids duplicate streams when **`updateDocumentTitle()`** runs often.
- **Comment tweak:** Clarified in source why the inner subscription stays plain **`.subscribe()`** (production-static / **#67**).

## Testing instructions

### What to verify

- Angular dev build completes with **no TS2420** (or other TS errors) for **`FeedbackPublicComponent`**.
- Public feedback i18n, document title, and subscription cleanup behave as before.

### How to test

1. Stack: `docker compose -f docker-compose.yml -f docker-compose.dev.yml up` (HAProxy host port often **4202**).
2. Force rebuild and confirm compile:  
   `touch front/src/app/feedback-public/feedback-public.component.ts`  
   `docker compose -f docker-compose.yml -f docker-compose.dev.yml logs --tail=80 front`  
   Expect **Application bundle generation complete** and **no** `TS2420` / `FeedbackPublicComponent` / `OnDestroy` errors.
3. From repo root:  
   `BASE_URL=http://127.0.0.1:4202 node front/scripts/test-feedback-public-i18n.mjs`  
   All `>>> RESULT:` lines must print **OK** (exit **0**).
4. Regression:  
   `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front`  
   Expect `>>> RESULT: Landing version OK…` and exit **0**.

### Pass/fail criteria

- **Pass:** No Angular/TS errors for `feedback-public.component.ts`; both commands exit **0**; feedback i18n script reports OK on every check.
- **Fail:** Any `TS2420` / `OnDestroy` error, or either script exits non-zero.

## Test report (coder)

1. **UTC:** ~2026-03-24T16:39–16:41Z.
2. **Environment:** `docker-compose.yml` + `docker-compose.dev.yml`; **`BASE_URL=http://127.0.0.1:4202`**; branch **`development`**.
3. **Front logs:** After save, **Application bundle generation complete** for `feedback-public-component` chunk; no TS errors in tail.
4. **`test-feedback-public-i18n.mjs`:** **PASS** (exit 0; seven `>>> RESULT:` OK).
5. **`npm run test:landing-version --prefix front`:** **PASS** (exit 0).
6. **Overall:** **PASS**.
