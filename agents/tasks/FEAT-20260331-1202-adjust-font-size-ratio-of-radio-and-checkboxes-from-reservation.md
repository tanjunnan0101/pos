# Adjust font size ratio of radio and checkboxes from reservation

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/128

## Problem / goal
In the **Reservations** UI, improve visual balance: **radio buttons and checkboxes** should use a **font size ratio** that matches the rest of the form (readable and consistent with labels). The reporter also asks to **remove a redundant “allergic” textarea**—keep a **single** allergies/allergic free-text field (avoid duplicating the same textarea).

## High-level instructions for coder
- Locate reservation forms (staff/internal and public booking if both show the same controls) and audit styles for **radio** and **checkbox** inputs vs surrounding typography.
- Adjust sizing (and spacing if needed) via existing theme / component SCSS so controls align with design tokens or nearby inputs—no one-off hacks unless the codebase already uses that pattern.
- Remove the **duplicate** allergies textarea; ensure one clear field remains and translations/i18n keys stay consistent.
- Verify in browser (reservation flow) at a typical viewport; check `docker compose` front logs for a clean Angular build after changes.
