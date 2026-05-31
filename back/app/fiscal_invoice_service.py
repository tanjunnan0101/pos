"""Server-side fiscal invoice issuance (VeriFactu preparation). No production AEAT HTTP calls."""

from __future__ import annotations

from datetime import datetime, timezone

from fastapi import HTTPException
from sqlmodel import Session, select

from app import models

_ISSUABLE_STATUSES = frozenset(
    {
        models.OrderStatus.paid,
        models.OrderStatus.completed,
    }
)


def _verification_stub(mode: str, full_number: str, tenant_name: str) -> tuple[str, str]:
    """QR payload string and legal disclaimer text (stub until AEAT integration)."""
    base_url = "https://www.agenciatributaria.es/static_files/information/verifactu.html"
    safe_name = (tenant_name or "")[:80]
    qr_content = f"{base_url}#stub={full_number}&ref={safe_name}"
    if mode == "live":
        text = (
            "VeriFactu — internal registration only. "
            "Submission to the AEAT must follow the official technical specification and professional tax advice. "
            "This application does not replace legal compliance."
        )
    else:
        text = (
            "VeriFactu — test / draft mode. "
            "This is not a real AEAT submission. Final field mapping must follow the official specification."
        )
    return qr_content, text


def build_issue_payload(
    order: models.Order,
    tenant: models.Tenant,
    full_number: str,
    billing_customer: models.BillingCustomer | None,
) -> dict:
    bc = None
    if billing_customer:
        bc = {
            "name": billing_customer.name,
            "company_name": billing_customer.company_name,
            "tax_id": billing_customer.tax_id,
        }
    return {
        "schema": "pos.fiscal_invoice.stub.v1",
        "full_number": full_number,
        "order_id": order.id,
        "tenant_id": tenant.id,
        "tenant_tax_id": tenant.tax_id or tenant.cif,
        "billing_customer": bc,
        "disclaimer": "Stub payload; AEAT wire format is not implemented in this endpoint.",
    }


def issue_or_get_fiscal_invoice(
    session: Session,
    tenant: models.Tenant,
    order: models.Order,
) -> models.FiscalInvoice:
    mode = (tenant.fiscal_mode or "off").strip().lower()
    if mode == "off":
        raise HTTPException(status_code=400, detail="Fiscal invoicing is disabled for this tenant")
    if mode not in ("test", "live"):
        raise HTTPException(status_code=400, detail="Invalid fiscal_mode")

    existing = session.exec(
        select(models.FiscalInvoice).where(
            models.FiscalInvoice.tenant_id == tenant.id,
            models.FiscalInvoice.order_id == order.id,
        )
    ).first()
    if existing:
        return existing

    if order.deleted_at is not None:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.status == models.OrderStatus.cancelled:
        raise HTTPException(status_code=400, detail="Cannot issue fiscal invoice for a cancelled order")
    if order.status not in _ISSUABLE_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Order must be paid or completed before issuing a fiscal invoice",
        )

    billing_customer = None
    if order.billing_customer_id:
        billing_customer = session.get(models.BillingCustomer, order.billing_customer_id)
        if billing_customer and billing_customer.tenant_id != tenant.id:
            billing_customer = None

    tenant_locked = session.exec(
        select(models.Tenant).where(models.Tenant.id == tenant.id).with_for_update()
    ).first()
    if not tenant_locked:
        raise HTTPException(status_code=404, detail="Tenant not found")

    series = (tenant_locked.fiscal_invoice_series or "VF").strip() or "VF"
    num = int(tenant_locked.fiscal_invoice_next_number or 1)
    full_number = f"{series}-{num}"

    qr_content, verification_text = _verification_stub(mode, full_number, tenant_locked.name or "")
    req_payload = build_issue_payload(order, tenant_locked, full_number, billing_customer)
    resp_payload = {
        "status": "stub",
        "note": "No AEAT HTTP call performed; integrate using official AEAT technical documentation.",
    }

    fi = models.FiscalInvoice(
        tenant_id=tenant.id,
        order_id=order.id,
        series=series,
        doc_number=num,
        full_number=full_number,
        mode=mode,
        status="issued",
        issued_at=datetime.now(timezone.utc),
        request_payload=req_payload,
        response_payload=resp_payload,
        verification_qr_content=qr_content,
        verification_text=verification_text,
    )
    tenant_locked.fiscal_invoice_next_number = num + 1
    session.add(fi)
    session.add(tenant_locked)
    session.flush()
    return fi


def fiscal_invoice_public_dict(fi: models.FiscalInvoice) -> dict:
    return {
        "id": fi.id,
        "order_id": fi.order_id,
        "series": fi.series,
        "doc_number": fi.doc_number,
        "full_number": fi.full_number,
        "mode": fi.mode,
        "status": fi.status,
        "issued_at": fi.issued_at.isoformat() if fi.issued_at else None,
        "verification_qr_content": fi.verification_qr_content,
        "verification_text": fi.verification_text,
    }
