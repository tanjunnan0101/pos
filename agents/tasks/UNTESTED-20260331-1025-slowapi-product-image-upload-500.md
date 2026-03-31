# Product image upload POST returns 500 (slowapi `response` type)

## Source

- **Service:** `pos-back` (`docker logs pos-back`)
- **UTC window:** traceback tied to **`POST /products/423/image`** (sampled **2026-03-31** stack session; **500** on upload path)
- **Representative lines:**

```
INFO: ... "POST /products/423/image HTTP/1.1" 500 Internal Server Error
ERROR: Exception in ASGI application
...
File ".../slowapi/extension.py", line 382, in _inject_headers
    raise Exception(
Exception: parameter `response` must be an instance of starlette.responses.Response
```

## High-level instructions for coder

- Inspect **`slowapi`** usage on **`POST /products/{id}/image`** (multipart upload): the limiter’s `_inject_headers` path is raising because it does not receive a **`starlette.responses.Response`** instance from the wrapped endpoint.
- Fix by aligning the route with SlowAPI/FastAPI expectations (e.g. ensure a proper **`Response`** object flows through the decorator chain, or adjust rate-limit wiring for file-upload handlers).
- Re-test authenticated **`POST /products/<id>/image`**; expect **200** and persisted image — no **500** from middleware.

## Coder notes

- **`upload_product_image`** and **`provider_upload_product_image`** returned plain **`dict`** values. With **`@limiter.limit`**, slowapi’s **`_inject_headers`** expects the route return to be a **`starlette.responses.Response`** (same pattern as **`POST /tables`** and **`POST /tenant/header-background`** in this codebase).
- **Change:** return **`JSONResponse(content=..., status_code=200)`**; use **`product.model_dump(mode="json")`** for JSON-safe payload.

---

## Testing instructions

### What to verify

- Authenticated **`POST /products/{product_id}/image`** (multipart file) returns **200** with JSON body (product fields + `image_size_bytes` / `image_size_formatted`) and no traceback from **`slowapi.extension`** in **`docker logs pos-back`**.
- Optional: **`POST /provider/products/{product_id}/image`** also returns **200** JSON (same slowapi fix).

### How to test

1. Stack: **`docker compose -f docker-compose.yml -f docker-compose.dev.yml`** (HAProxy e.g. **`http://127.0.0.1:4202`**).
2. In the staff UI, open **Products / catalog**, edit a product, **upload a raster image** (jpg/png/webp within size limits).
3. Or use **curl** with a staff JWT and **`multipart/form-data`** file field against **`POST /api/products/<id>/image`** (path may be proxied; match your **`BASE_URL`** from **`docs/testing.md`**).

### Pass / fail criteria

- **Pass:** HTTP **200**, image appears on the product, **`pos-back`** logs show no **500** / **`parameter \`response\` must be an instance of starlette.responses.Response`** for that request.
- **Fail:** **500** on upload with the slowapi **`Response`** exception, or broken JSON shape vs previous client expectations (should match prior dict serialization).
