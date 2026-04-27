# Fix Social posts compose controls: styled file upload + “Publish immediately” row

## GitHub Issues

- **Issue:** https://github.com/satisfecho/pos/issues/201
- **201**

## Problem / goal

On **Settings → Marketing → Social posts**, replace the native **Choose File** control with a styled upload (button, filename, image preview after selection), consistent with other forms in the app. Fix **Publish immediately**: use a normal-size checkbox with the label inline and left-aligned on one row; remove the oversized centered checkbox and the distracting bordered/highlight strip. Match existing Settings spacing, typography, and form patterns. **No API changes** unless strictly required.

## High-level instructions for coder

- Locate the Social posts compose UI (settings/marketing) and align file upload with patterns used elsewhere (e.g. button + filename text + preview).
- Restructure the **Publish immediately** row: single row, label left, standard checkbox size; remove extra framing/highlight that draws attention away from content.
- Cross-check responsive layout and i18n keys if labels change.
- Smoke: open Settings → Marketing → Social posts, select an image, confirm preview and publish-immediate row look correct; ensure no regressions to OAuth/connect flows.
