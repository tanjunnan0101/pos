"""Tests for product bulk import preview and confirm."""

from __future__ import annotations

import unittest
from datetime import timedelta

from pg_client_mixin import PgClientTestCase

from app import models, security
from app.product_bulk_import import (
    ProductBulkImportConfirmRequest,
    ProductBulkImportItemIn,
    ProductBulkImportPreviewRow,
    ProductBulkImportRequest,
    build_preview,
    confirm_import,
    parse_json_import_payload,
)


def _owner_headers(user: models.User) -> dict[str, str]:
    data = {
        "sub": user.email,
        "tenant_id": user.tenant_id,
        "provider_id": getattr(user, "provider_id", None),
        "token_version": user.token_version,
    }
    token = security.create_access_token(data, expires_delta=timedelta(minutes=30))
    return {"Authorization": f"Bearer {token}"}


class TestProductBulkImport(PgClientTestCase):
    def setUp(self) -> None:
        super().setUp()
        tenant = models.Tenant(name="Bulk Import Test")
        self.session.add(tenant)
        self.session.commit()
        self.session.refresh(tenant)
        self.tenant_id = tenant.id

        self.owner = models.User(
            email="bulk-owner@test.local",
            hashed_password=security.get_password_hash("secret"),
            full_name="Owner",
            tenant_id=self.tenant_id,
            role=models.UserRole.owner,
        )
        self.session.add(self.owner)
        self.session.commit()
        self.session.refresh(self.owner)
        self.headers = _owner_headers(self.owner)

    def test_parse_json_import_payload_list(self):
        items = parse_json_import_payload([{"name": "Soup", "price": 5.5}])
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].name, "Soup")

    def test_build_preview_create_and_update(self):
        self.session.add(
            models.Product(tenant_id=self.tenant_id, name="Existing Dish", price_cents=1000)
        )
        self.session.commit()

        req = ProductBulkImportRequest(
            items=[
                ProductBulkImportItemIn(name="Existing Dish", price=12.0),
                ProductBulkImportItemIn(name="New Dish", price=8.5, category="Starters"),
                ProductBulkImportItemIn(name="", price=1.0),
            ]
        )
        preview = build_preview(self.session, self.tenant_id, req.items)
        self.assertEqual(preview.summary.total, 3)
        self.assertEqual(preview.summary.valid, 2)
        self.assertEqual(preview.summary.update, 1)
        self.assertEqual(preview.summary.create, 1)

    def test_preview_json_api(self):
        payload = {"items": [{"name": "Tiramisu", "price": 6.5, "category": "Desserts"}]}
        r = self.client.post(
            "/products/bulk-import/preview-json",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertEqual(body["summary"]["valid"], 1)
        self.assertEqual(body["items"][0]["name"], "Tiramisu")

    def test_confirm_api_creates_products(self):
        preview = self.client.post(
            "/products/bulk-import/preview-json",
            json={"items": [{"name": "Bruschetta", "price": 4.0}]},
            headers=self.headers,
        ).json()
        r = self.client.post(
            "/products/bulk-import/confirm",
            json={"items": preview["items"]},
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json()["created"], 1)

        listed = self.client.get("/products", headers=self.headers)
        names = [p["name"] for p in listed.json()]
        self.assertIn("Bruschetta", names)

    def test_confirm_skips_invalid_rows(self):
        result = confirm_import(
            self.session,
            self.tenant_id,
            ProductBulkImportConfirmRequest(
                items=[
                    ProductBulkImportPreviewRow(
                        row_index=0,
                        name="Bad",
                        price_cents=None,
                        valid=False,
                        errors=["price_required"],
                        action="skip",
                    ),
                    ProductBulkImportPreviewRow(
                        row_index=1,
                        name="Good",
                        price_cents=500,
                        valid=True,
                        errors=[],
                        action="create",
                    ),
                ]
            ).items,
        )
        self.assertEqual(result.created, 1)
        self.assertEqual(result.skipped, 1)


if __name__ == "__main__":
    unittest.main()
