from app.tenant_currency import (
    apply_tenant_currency_api_dict,
    normalize_tenant_currency_fields,
    sync_tenant_currency_symbol_from_code,
)


def test_normalize_defaults_to_sgd():
    assert normalize_tenant_currency_fields(None, None) == ("SGD", "$")
    assert normalize_tenant_currency_fields("", "$") == ("SGD", "$")


def test_normalize_forces_sgd():
    assert normalize_tenant_currency_fields("usd", None) == ("SGD", "$")


def test_apply_dict_mutates():
    d = {"currency_code": None, "currency": "$"}
    apply_tenant_currency_api_dict(d)
    assert d["currency_code"] == "SGD"
    assert d["currency"] == "$"


def test_apply_dict_forces_sgd():
    d = {"currency_code": "USD", "currency": "legacy"}
    apply_tenant_currency_api_dict(d)
    assert d["currency_code"] == "SGD"
    assert d["currency"] == "$"


def test_sync_symbol():
    assert sync_tenant_currency_symbol_from_code("SGD") == "$"
    assert sync_tenant_currency_symbol_from_code(None) == "$"
