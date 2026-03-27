# Terms and privacy links near registration / auth actions

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/114

## Problem / goal
On the public/auth surface (e.g. login or sign-up flows), **Terms** and **Privacy** links should sit **close to** the other account actions (create account, provider login, register as provider, contact us), not isolated or easy to miss. The issue gives a target ordering example:  
`Don't have an account?` → Create account, Provider login, Register as provider, Contact us, **Terms**, **Privacy**.  
Align with existing tenant/global Terms & Privacy URL behaviour from [#110](https://github.com/satisfecho/pos/issues/110) / related settings docs if needed.

## High-level instructions for coder
- Locate the template(s) for the relevant login / registration / landing footers (Angular) where those links are rendered.
- Adjust layout so Terms and Privacy appear **adjacent** to the listed auth-related actions, consistent with UX on mobile and desktop.
- Reuse the same URL resolution as elsewhere (tenant vs global fallbacks); do not hard-code wrong domains.
- Verify i18n: link labels use translation keys like the rest of the page.
- Run a quick smoke (e.g. open the page in dev, confirm order and links work).

## Implementation notes (coder)
- **`app-legal-links`:** optional **`[inline]="true"`** — host uses `display: contents` and nav flows inline with footer separators.
- **`/login`**, **`/register`:** single **`.auth-actions-foot`** flex row: create account / sign-in, provider links, `mailto:sales@satisfecho.de`, then Terms & Privacy (via existing **`getPublicLegalUrls()`**).
- **Landing:** Terms/Privacy inline after Contact (same `·` separators); removed block wrapper that forced a line break.
- **`/provider/login`**, **`/provider/register`:** same legal URL fetch; provider login footer consolidated with i18n **`PROVIDER_AUTH.*`** + **`TranslateModule`**; register footer adds contact + inline legal links.

## Testing instructions
1. Stack up on dev HAProxy (e.g. `http://127.0.0.1:4202`).
2. **Landing `/`:** Footer reads in one flow: … Contact us · Terms · Privacy (if URLs configured). Provider links still present with testids `landing-provider-login`, `landing-provider-register`.
3. **`/login`:** After the form, order: “Don't have an account?” Create account · Provider login · Register as provider · Contact us · (Terms · Privacy if URLs exist).
4. **`/register`:** Same pattern with “Already have account?” / Sign in first.
5. **`/provider/login`**, **`/provider/register`:** Footer includes contact and legal links when URLs exist; strings respect language picker (provider login).
6. Automated: from `front/`, `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version` and `npm run test:landing-provider-links`.
