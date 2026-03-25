# Feedback: light background when product added in menu table

## GitHub
- **Issue:** https://github.com/satisfecho/pos/issues/85

## Problem / goal
When a customer or waiter adds a product from the menu table view, the chosen row/item should read as “selected” or “marked” with a **light background** (consistent with existing selection patterns elsewhere in the app). Typo in original title: “backrgound” → background.

## High-level instructions for coder
- Locate staff/menu table flows where products are added to an order from the table context; identify the list or card component that represents each product line.
- Add or reuse a visual state (e.g. selected row class, subtle tint) so recently added or active line items are clearly distinguished without hurting contrast or accessibility.
- Align colors/spacing with existing design tokens or similar “selected” states (e.g. other tables or order lines).
- Smoke-test waiter and, if applicable, customer paths; confirm no layout jump and readable text on the tinted background.
