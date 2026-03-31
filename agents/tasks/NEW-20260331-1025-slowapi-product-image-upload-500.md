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
