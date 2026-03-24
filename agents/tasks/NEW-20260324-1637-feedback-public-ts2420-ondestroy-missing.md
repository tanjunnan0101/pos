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
