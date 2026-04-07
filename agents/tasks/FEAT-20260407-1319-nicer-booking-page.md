# Nicer booking page

## GitHub Issues
- [github.com/satisfecho/pos/issues](https://github.com/satisfecho/pos/issues)
- `gh issue list --repo satisfecho/pos --state open --limit 40`
- Optional: `--json number,title,labels,updatedAt,url`
- **Issue:** https://github.com/satisfecho/pos/issues/173

## Problem / goal
Improve the public booking page (example tenant URL in issue: `/book/1081` on local dev). **Readability:** the `hero-content` area should use styling (background, rounded corners, padding/margins) so text stays readable over the existing background image—keep the image, improve contrast and legibility. **Links:** when the restaurant has a website URL configured, expose it as a normal clickable link in the UI.

## High-level instructions for coder
- Locate the booking page component/template and styles for the hero section; align with existing design tokens and `front/public/i18n` for any new strings.
- Implement a readable overlay or panel for hero text (background, radius, spacing) without removing the background image.
- Wire the restaurant website field so it renders as a proper anchor (`href`, accessibility, open behavior per product norms).
- Smoke-test the public booking flow for at least one tenant; verify responsive layout.
