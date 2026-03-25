# Two factor authentication button decoration

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/83

## Problem / goal

In **Settings → Security**, the two-factor authentication control sits flush against the text above. Add spacing (e.g. margin-top) so the button is visually separated from the preceding copy, consistent with other settings sections.

## High-level instructions for coder

- Locate the security / 2FA settings template and styles (Angular).
- Add layout spacing between the explanatory text block and the 2FA action button without breaking responsive layouts.
- Verify in the UI that spacing matches nearby settings cards and accessibility (focus order unchanged).

## Implementation summary

- Scoped style on `[data-testid='settings-security-section'] .form-card > p.hint` with `margin-bottom: var(--space-4)` so OTP explanatory copy (and the setup-flow hint before the secret row) is separated from the following control, aligned with `.otp-enabled-msg` spacing.

## Testing instructions

1. Log in as a user who can open **Settings** (e.g. demo staff).
2. Open **Settings → Security** (`data-testid="settings-security-section"`).
3. When OTP is **not** enabled: confirm clear vertical space between the description paragraph and **Enable two-factor authentication** (primary button).
4. Start setup (if testing further): confirm space between the “add to app” hint and the secret/QR row.
5. Optional: `BASE_URL=http://127.0.0.1:4202 npm run test:landing-version --prefix front` (includes navigating to `/settings`).
