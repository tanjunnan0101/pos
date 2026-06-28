import unittest
from unittest.mock import patch

from pg_client_mixin import PgClientTestCase

from app import models


class TestPaymentSecurity(PgClientTestCase):
    def setUp(self):
        super().setUp()
        self.setup_data()

    def setup_data(self):
        self.tenant = models.Tenant(
            name="Test Restaurant",
            currency_code="SGD",
            currency="$",
            hitpay_api_key="hitpay_test_key",
            hitpay_mode="sandbox",
        )
        self.session.add(self.tenant)
        self.session.commit()
        self.session.refresh(self.tenant)

        self.floor = models.Floor(name="Main", tenant_id=self.tenant.id)
        self.session.add(self.floor)
        self.session.commit()

        self.table = models.Table(
            name="Take Away",
            tenant_id=self.tenant.id,
            floor_id=self.floor.id,
            is_active=True,
            order_pin="1234",
        )
        self.session.add(self.table)
        self.session.commit()
        self.session.refresh(self.table)

        self.product = models.Product(
            name="Expensive Wine",
            price_cents=10000,
            tenant_id=self.tenant.id,
        )
        self.session.add(self.product)
        self.session.commit()
        self.session.refresh(self.product)

    def _create_order_with_hitpay_request(self, request_id: str = "hp_req_123") -> int:
        response = self.client.post(
            f"/menu/{self.table.token}/order",
            json={
                "items": [{"product_id": self.product.id, "quantity": 1}],
                "notes": "Expensive Order",
            },
        )
        self.assertEqual(response.status_code, 200)
        order_id = response.json()["order_id"]
        order = self.session.get(models.Order, order_id)
        self.assertIsNotNone(order)
        order.hitpay_payment_request_id = request_id
        self.session.add(order)
        self.session.commit()
        return order_id

    @patch("app.main._hitpay_retrieve_payment_request")
    def test_prevent_payment_bypass_amount_mismatch(self, mock_retrieve):
        order_id = self._create_order_with_hitpay_request()
        mock_retrieve.return_value = {
            "id": "hp_req_123",
            "status": "completed",
            "amount": "1.00",
            "currency": "SGD",
            "reference_number": f"pos-order-{order_id}",
        }

        response = self.client.post(
            f"/orders/{order_id}/confirm-hitpay-payment",
            params={"table_token": self.table.token},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("amount does not match", response.json()["detail"])

    @patch("app.main._hitpay_retrieve_payment_request")
    def test_prevent_payment_bypass_order_mismatch(self, mock_retrieve):
        order_id = self._create_order_with_hitpay_request()
        mock_retrieve.return_value = {
            "id": "hp_req_123",
            "status": "completed",
            "amount": "100.00",
            "currency": "SGD",
            "reference_number": "pos-order-9999",
        }

        response = self.client.post(
            f"/orders/{order_id}/confirm-hitpay-payment",
            params={"table_token": self.table.token},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("reference does not belong", response.json()["detail"])

    @patch("app.main._hitpay_retrieve_payment_request")
    def test_payment_success(self, mock_retrieve):
        order_id = self._create_order_with_hitpay_request()
        mock_retrieve.return_value = {
            "id": "hp_req_123",
            "status": "completed",
            "amount": "100.00",
            "currency": "SGD",
            "reference_number": f"pos-order-{order_id}",
        }

        response = self.client.post(
            f"/orders/{order_id}/confirm-hitpay-payment",
            params={"table_token": self.table.token},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "paid")


if __name__ == "__main__":
    unittest.main()
