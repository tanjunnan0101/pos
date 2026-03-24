# TypeScript build failure: FeedbackPublicComponent OnDestroy property

## Source
- **Service:** pos-front container (hot reload build)
- **Window:** 15:00 UTC on 2026-03-24 (Application bundle generation failed)
- **Error lines:**
  - `TS2339: Property 'langSub' does not exist on type 'FeedbackPublicComponent'` at src/app/feedback-public/feedback-public.component.ts:54:9
  - `TS2339: Property 'langSub' does not exist on type 'FeedbackPublicComponent'` at src/app/feedback-public/feedback-public.component.ts:89:9
  - (Likely `TS2439` for langSub, and `TS2420` for OnDestroy implementation)

## High-level instructions for coder
- Inspect `src/app/feedback-public/feedback-public.component.ts` to find property declaration issues with `langSub` and possibly missing or incorrect `OnDestroy` implementation
- Fix TypeScript compilation errors to unblock Angular bundle generation in development
- No data flow or API changes expected; focus on fixing component class definition and lifecycle hook implementation
- After fix, verify frontend rebuild succeeds in Docker; run `docker compose logs -f front` and confirm no Angular TS errors