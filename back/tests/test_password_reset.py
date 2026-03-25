"""Password reset request/confirm API (GitHub #93)."""
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

from pg_client_mixin import PgClientTestCase

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from app import models, security


class TestPasswordReset(PgClientTestCase):
    def setUp(self):
        super().setUp()
        from app.settings import settings

        self._prev_public_base = settings.public_app_base_url
        self.tenant = models.Tenant(name="Pw Reset Cafe")
        self.session.add(self.tenant)
        self.session.commit()
        self.session.refresh(self.tenant)
        self.user = models.User(
            email="pwreset-staff@amvara.de",
            hashed_password=security.get_password_hash("old-secret-9"),
            tenant_id=self.tenant.id,
            role=models.UserRole.owner,
        )
        self.session.add(self.user)
        self.session.commit()
        self.session.refresh(self.user)

    def tearDown(self):
        from app.settings import settings

        settings.public_app_base_url = self._prev_public_base
        super().tearDown()

    @patch("app.main.email_svc.send_password_reset_email", new_callable=AsyncMock)
    def test_request_creates_token_and_sends_email(self, mock_send):
        mock_send.return_value = True
        from app.settings import settings

        settings.public_app_base_url = "http://127.0.0.1:4202"
        r = self.client.post(
            "/password-reset/request",
            json={"email": "pwreset-staff@amvara.de", "tenant_id": self.tenant.id},
        )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json().get("status"), "ok")
        mock_send.assert_called_once()
        args, kwargs = mock_send.call_args
        self.assertEqual(args[0], "pwreset-staff@amvara.de")
        self.assertIn("/reset-password?token=", args[1])
        self.assertIsNotNone(kwargs.get("tenant"))

    def test_request_unknown_email_still_ok(self):
        from app.settings import settings

        settings.public_app_base_url = "http://127.0.0.1:4202"
        r = self.client.post(
            "/password-reset/request",
            json={"email": "nobody-here-xyz@amvara.de", "tenant_id": self.tenant.id},
        )
        self.assertEqual(r.status_code, 200, r.text)
        self.assertEqual(r.json().get("status"), "ok")

    @patch("app.main.email_svc.send_password_reset_email", new_callable=AsyncMock)
    def test_confirm_updates_password_and_invalidates_token(self, mock_send):
        mock_send.return_value = True
        from app.settings import settings

        settings.public_app_base_url = "http://127.0.0.1:4202"
        self.client.post(
            "/password-reset/request",
            json={"email": "pwreset-staff@amvara.de", "tenant_id": self.tenant.id},
        )
        self.assertTrue(mock_send.called)
        reset_url = mock_send.call_args[0][1]
        token = reset_url.split("token=", 1)[1]

        r2 = self.client.post(
            "/password-reset/confirm",
            json={"token": token, "new_password": "new-secret-88"},
        )
        self.assertEqual(r2.status_code, 200, r2.text)
        self.session.refresh(self.user)
        self.assertTrue(security.verify_password("new-secret-88", self.user.hashed_password))
        self.assertGreaterEqual(self.user.token_version, 1)

        r3 = self.client.post(
            "/password-reset/confirm",
            json={"token": token, "new_password": "another-one-99"},
        )
        self.assertEqual(r3.status_code, 400, r3.text)

    def test_confirm_bad_token(self):
        r = self.client.post(
            "/password-reset/confirm",
            json={"token": "not-a-real-token-value-here", "new_password": "x" * 10},
        )
        self.assertEqual(r.status_code, 400, r.text)


if __name__ == "__main__":
    unittest.main()
