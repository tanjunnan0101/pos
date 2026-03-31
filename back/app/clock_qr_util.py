"""HMAC-SHA256 storage for per-tenant staff clock QR tokens (no plaintext in DB)."""

from __future__ import annotations

import hashlib
import hmac
import secrets

from app.settings import settings


def generate_clock_qr_token() -> str:
    """URL-safe random token for printed QR / deep links (32 bytes hex)."""
    return secrets.token_hex(32)


def hash_clock_qr_token(token: str) -> str:
    """Deterministic digest for persistence; uses app secret as pepper."""
    key = settings.secret_key.encode("utf-8")
    msg = token.encode("utf-8")
    return hmac.new(key, msg, hashlib.sha256).hexdigest()


def clock_qr_tokens_equal(stored_hash: str | None, token: str | None) -> bool:
    if not stored_hash or not token or not token.strip():
        return False
    digest = hash_clock_qr_token(token.strip())
    return hmac.compare_digest(stored_hash, digest)
