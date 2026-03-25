"""Staff work session (clock in/out) API."""
from __future__ import annotations

import unittest
from datetime import date, datetime, timedelta, timezone

from pg_client_mixin import PgClientTestCase

from app import models, security
from app.work_session_serialization import WORK_SESSION_CONTRACT_THRESHOLD_MINUTES, serialize_work_session


def _bearer_headers(user: models.User) -> dict[str, str]:
    data = {
        "sub": user.email,
        "tenant_id": user.tenant_id,
        "provider_id": getattr(user, "provider_id", None),
        "token_version": user.token_version,
    }
    token = security.create_access_token(data, expires_delta=timedelta(minutes=30))
    return {"Authorization": f"Bearer {token}"}


class TestWorkSession(PgClientTestCase):
    def setUp(self) -> None:
        super().setUp()
        tenant = models.Tenant(name="WS Test")
        self.session.add(tenant)
        self.session.commit()
        self.session.refresh(tenant)
        self.tenant_id = tenant.id

        self.waiter = models.User(
            email="ws-waiter@test.local",
            hashed_password=security.get_password_hash("secret"),
            full_name="Waiter W",
            tenant_id=self.tenant_id,
            role=models.UserRole.waiter,
        )
        self.session.add(self.waiter)
        self.session.commit()
        self.session.refresh(self.waiter)
        self.admin = models.User(
            email="ws-admin@test.local",
            hashed_password=security.get_password_hash("secret"),
            full_name="Admin A",
            tenant_id=self.tenant_id,
            role=models.UserRole.admin,
        )
        self.session.add(self.admin)
        self.session.commit()
        self.session.refresh(self.admin)

    def test_clock_in_out_and_report(self):
        wh = _bearer_headers(self.waiter)
        r = self.client.post("/users/me/work-session/start", headers=wh)
        self.assertEqual(r.status_code, 200, r.text)
        body = r.json()
        self.assertIn("id", body)
        self.assertIsNone(body.get("ended_at"))
        self.assertFalse(body.get("over_contract"))
        self.assertEqual(body.get("contract_threshold_minutes"), WORK_SESSION_CONTRACT_THRESHOLD_MINUTES)
        self.assertIsNotNone(body.get("open_duration_minutes"))

        r2 = self.client.post("/users/me/work-session/start", headers=wh)
        self.assertEqual(r2.status_code, 400, r2.text)

        cur = self.client.get("/users/me/work-session", headers=wh)
        self.assertEqual(cur.status_code, 200, cur.text)
        self.assertEqual(cur.json()["id"], body["id"])

        r3 = self.client.post("/users/me/work-session/end", headers=wh)
        self.assertEqual(r3.status_code, 200, r3.text)
        self.assertIsNotNone(r3.json().get("ended_at"))

        r4 = self.client.post("/users/me/work-session/end", headers=wh)
        self.assertEqual(r4.status_code, 400, r4.text)

        today = date.today().isoformat()
        lst = self.client.get(
            "/users/me/work-sessions",
            params={"from_date": today, "to_date": today},
            headers=wh,
        )
        self.assertEqual(lst.status_code, 200, lst.text)
        rows = lst.json()
        self.assertEqual(len(rows), 1)
        self.assertIsNotNone(rows[0].get("ended_at"))

        ah = _bearer_headers(self.admin)
        rep = self.client.get(
            "/reports/work-sessions",
            params={"from_date": today, "to_date": today},
            headers=ah,
        )
        self.assertEqual(rep.status_code, 200, rep.text)
        self.assertEqual(len(rep.json()), 1)
        self.assertEqual(rep.json()[0]["user_id"], self.waiter.id)

    def test_open_shift_over_contract_after_threshold(self):
        wh = _bearer_headers(self.waiter)
        r = self.client.post("/users/me/work-session/start", headers=wh)
        self.assertEqual(r.status_code, 200, r.text)
        ws_id = r.json()["id"]
        row = self.session.get(models.WorkSession, ws_id)
        self.assertIsNotNone(row)
        row.started_at = datetime.now(timezone.utc) - timedelta(
            minutes=WORK_SESSION_CONTRACT_THRESHOLD_MINUTES + 15
        )
        self.session.add(row)
        self.session.commit()

        cur = self.client.get("/users/me/work-session", headers=wh)
        self.assertEqual(cur.status_code, 200, cur.text)
        payload = cur.json()
        self.assertTrue(payload.get("over_contract"))
        self.assertGreaterEqual(
            payload.get("open_duration_minutes", 0),
            WORK_SESSION_CONTRACT_THRESHOLD_MINUTES,
        )

    def test_serialize_work_session_respects_now_override(self):
        started = datetime(2020, 1, 1, 8, 0, tzinfo=timezone.utc)
        now = started + timedelta(minutes=WORK_SESSION_CONTRACT_THRESHOLD_MINUTES)
        ws = models.WorkSession(
            tenant_id=self.tenant_id,
            user_id=self.waiter.id,
            started_at=started,
            ended_at=None,
        )
        self.session.add(ws)
        self.session.commit()
        self.session.refresh(ws)
        d = serialize_work_session(ws, "Waiter", now_utc=now)
        self.assertTrue(d["over_contract"])
        d2 = serialize_work_session(ws, "Waiter", now_utc=started + timedelta(minutes=30))
        self.assertFalse(d2["over_contract"])


if __name__ == "__main__":
    unittest.main()
