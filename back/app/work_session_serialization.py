"""Shared JSON shape for WorkSession (clock in/out, reports)."""

from __future__ import annotations

from datetime import datetime, timezone

from app import models

# Default “normal day” length for overtime visibility (not persisted; not legal advice).
WORK_SESSION_CONTRACT_THRESHOLD_MINUTES = 480


def serialize_work_session(
    ws: models.WorkSession,
    user_name: str,
    *,
    now_utc: datetime | None = None,
) -> dict:
    """Build API dict. Open sessions include elapsed time and over-contract flag (>= threshold)."""
    now = now_utc if now_utc is not None else datetime.now(timezone.utc)
    duration_minutes: int | None = None
    if ws.ended_at is not None and ws.started_at is not None:
        duration_minutes = max(0, int((ws.ended_at - ws.started_at).total_seconds() // 60))

    open_duration_minutes: int | None = None
    over_contract = False
    if ws.ended_at is None and ws.started_at is not None:
        open_duration_minutes = max(0, int((now - ws.started_at).total_seconds() // 60))
        over_contract = open_duration_minutes >= WORK_SESSION_CONTRACT_THRESHOLD_MINUTES

    return {
        "id": ws.id,
        "tenant_id": ws.tenant_id,
        "user_id": ws.user_id,
        "user_name": user_name,
        "started_at": ws.started_at.isoformat() if ws.started_at else None,
        "ended_at": ws.ended_at.isoformat() if ws.ended_at else None,
        "duration_minutes": duration_minutes,
        "open_duration_minutes": open_duration_minutes,
        "contract_threshold_minutes": WORK_SESSION_CONTRACT_THRESHOLD_MINUTES,
        "over_contract": over_contract,
        "start_ip": ws.start_ip,
        "end_ip": ws.end_ip,
    }
