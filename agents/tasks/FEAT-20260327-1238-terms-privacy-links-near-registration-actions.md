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
