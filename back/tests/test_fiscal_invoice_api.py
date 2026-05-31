"""Fiscal invoice issuance: tenant isolation, paid-only, idempotency."""
from __future__ import annotations

import unittest
from datetime import timedelta

from pg_client_mixin import PgClientTestCase

from app import models, security


def _bearer_headers(user: models.User) -> dict[str, str]:
    data = {
        "sub": user.email,
        "tenant_id": user.tenant_id,
        "provider_id": getattr(user, "provider_id", None),
        "token_version": user.token_version,
    }
    token = security.create_access_token(data, expires_delta=timedelta(minutes=30))
    return {"Authorization": f"Bearer {token}"}


class TestFiscalInvoiceApi(PgClientTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.tenant = models.Tenant(name="Fiscal Tenant", fiscal_mode="test", fiscal_invoice_series="T")
        self.session.add(self.tenant)
        self.session.commit()
        self.session.refresh(self.tenant)

        self.owner = models.User(
            email="owner-fiscal@test.local",
            hashed_password=security.get_password_hash("x"),
            full_name="Owner",
            tenant_id=self.tenant.id,
            role=models.UserRole.owner,
        )
        self.session.add(self.owner)
        self.session.commit()
        self.session.refresh(self.owner)

        floor = models.Floor(name="Main", sort_order=0, tenant_id=self.tenant.id)
        self.session.add(floor)
        self.session.commit()
        self.session.refresh(floor)

        table = models.Table(
            name="T1",
            token="tok-fiscal-1",
            floor_id=floor.id,
            tenant_id=self.tenant.id,
            x_position=0,
            y_position=0,
            rotation=0,
            shape="rect",
            width=1,
            height=1,
            seat_count=2,
            is_active=True,
        )
        self.session.add(table)
        self.session.commit()
        self.session.refresh(table)

        self.order_paid = models.Order(
            tenant_id=self.tenant.id,
            table_id=table.id,
            status=models.OrderStatus.paid,
        )
        self.order_pending = models.Order(
            tenant_id=self.tenant.id,
            table_id=table.id,
            status=models.OrderStatus.pending,
        )
        self.session.add(self.order_paid)
        self.session.add(self.order_pending)
        self.session.commit()
        self.session.refresh(self.order_paid)
        self.session.refresh(self.order_pending)

        self.t_other = models.Tenant(name="Other")
        self.session.add(self.t_other)
        self.session.commit()
        self.session.refresh(self.t_other)

        self.owner_other = models.User(
            email="owner-other-fiscal@test.local",
            hashed_password=security.get_password_hash("x"),
            full_name="Owner O",
            tenant_id=self.t_other.id,
            role=models.UserRole.owner,
        )
        self.session.add(self.owner_other)
        self.session.commit()
        self.session.refresh(self.owner_other)

    def test_issue_paid_order_returns_number_and_idempotent(self) -> None:
        h = _bearer_headers(self.owner)
        r1 = self.client.post(f"/orders/{self.order_paid.id}/fiscal-invoice/issue", headers=h)
        self.assertEqual(r1.status_code, 200, r1.text)
        body1 = r1.json()
        self.assertIn("full_number", body1)
        fn = body1["full_number"]
        r2 = self.client.post(f"/orders/{self.order_paid.id}/fiscal-invoice/issue", headers=h)
        self.assertEqual(r2.status_code, 200, r2.text)
        body2 = r2.json()
        self.assertEqual(body2["full_number"], fn)

    def test_issue_pending_order_400(self) -> None:
        h = _bearer_headers(self.owner)
        r = self.client.post(f"/orders/{self.order_pending.id}/fiscal-invoice/issue", headers=h)
        self.assertEqual(r.status_code, 400, r.text)

    def test_issue_other_tenant_order_404(self) -> None:
        h = _bearer_headers(self.owner_other)
        r = self.client.post(f"/orders/{self.order_paid.id}/fiscal-invoice/issue", headers=h)
        self.assertEqual(r.status_code, 404, r.text)


if __name__ == "__main__":
    unittest.main()
