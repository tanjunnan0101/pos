# Contract Template

## GitHub

- **Issue:** https://github.com/satisfecho/pos/issues/106

## Problem / goal

Provide a **database-backed** way to manage **contract templates**: each template is tied to a **language** and a **restaurant (tenant)**. Offer **sensible default templates** based on where the restaurant is located (e.g. Spain → Spanish defaults, India → India-oriented defaults, extensible to more regions). The issue includes a long **example Spanish temporary employment contract** (camarero/a, full time) as reference content for clauses and placeholders—not necessarily verbatim production legal text.

Related prior work may exist under **staff contracts** / **contract templates** (see `docs/`, migrations, and closed tasks around employment contract templates); this issue emphasizes **locale- or country-driven defaults** and the **template catalog** concept.

## High-level instructions for coder

- Review existing **`staff_contract` / template** models, APIs, and Settings UI so new work **extends** rather than duplicates what is already shipped for tenant-managed templates.
- Design or extend the **data model** so templates support **language** and **tenant**, and so **system or seeded defaults** can be selected or suggested from **restaurant location / jurisdiction** (without hard-coding only Spain—make the rule pluggable or data-driven where practical).
- Define how **defaults** are applied when a tenant has no custom templates yet (seed, migration, or admin tooling—align with project migration and seed patterns).
- Preserve **tenant isolation**, **RBAC** consistent with existing contract permissions, and avoid logging full template bodies in application logs.
- Add or update **API + staff UI** flows so owners can see/use geography- and language-appropriate templates alongside any existing custom template CRUD.
- Cover behavior with **tests** (backend at minimum) and confirm **frontend build** stays clean per project conventions.
