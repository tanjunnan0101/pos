"""Normalize tenant currency fields for API responses."""

DEFAULT_CURRENCY_CODE = "SGD"
DEFAULT_CURRENCY_SYMBOL = "$"


def normalize_tenant_currency_fields(
    currency_code: str | None,
    currency: str | None,
) -> tuple[str, str]:
    """Return the POS-wide currency. This installation is HitPay/SGD only."""
    return (DEFAULT_CURRENCY_CODE, DEFAULT_CURRENCY_SYMBOL)


def apply_tenant_currency_api_dict(d: dict) -> None:
    """Mutate tenant-like dict in place for consistent currency_code + currency."""
    c, s = normalize_tenant_currency_fields(d.get("currency_code"), d.get("currency"))
    d["currency_code"] = c
    d["currency"] = s


def sync_tenant_currency_symbol_from_code(currency_code: str | None) -> str | None:
    """Canonical display symbol to store on Tenant.currency."""
    return DEFAULT_CURRENCY_SYMBOL
