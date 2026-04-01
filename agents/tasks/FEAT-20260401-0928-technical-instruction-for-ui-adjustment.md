# Technical Instruction for UI Adjustment

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/137

## Problem / goal

On **Tables**, the canvas header area shows a **dark/black** background that should be reverted to the **original light/neutral** look. The issue points at the main header container for the tables canvas (staff flow), including floor tabs.

## High-level instructions for coder

- Find SCSS/CSS that sets a **dark background** on the tables management header / staff-flow header for this view.
- Relevant hooks from the issue: container with **`data-testid="tables-canvas-header"`**, class **`.page-header--staff-flow`**, and **`.floor-tabs`** (and related layout under the Tables / floor canvas).
- **Remove or replace** the dark background so the header matches the prior light/neutral staff-flow styling; avoid regressions on other routes that reuse shared classes—scope changes to the Tables canvas header as needed.
