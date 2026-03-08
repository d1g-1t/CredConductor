import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from secret_rotator.database import get_session
from secret_rotator.repositories.audit_log_repo import AuditLogRepository
from secret_rotator.repositories.secret_repo import SecretRepository

router = APIRouter(prefix="/audit", tags=["audit"])
audit_repo = AuditLogRepository()
secret_repo = SecretRepository()


@router.get("")
async def list_audit_logs(
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
) -> list[dict]:
    logs = await audit_repo.list_all(session, limit=limit)
    return [
        {
            "id": str(log.id),
            "secret_id": str(log.secret_id),
            "rotation_job_id": str(log.rotation_job_id) if log.rotation_job_id else None,
            "action": log.action,
            "details": log.details,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in logs
    ]


@router.get("/secrets/{name}")
async def list_secret_audit_logs(
    name: str,
    limit: int = 100,
    session: AsyncSession = Depends(get_session),
) -> list[dict]:
    secret = await secret_repo.get_by_name(session, name)
    if not secret:
        return []

    logs = await audit_repo.list_by_secret(session, secret.id, limit=limit)
    return [
        {
            "id": str(log.id),
            "secret_id": str(log.secret_id),
            "rotation_job_id": str(log.rotation_job_id) if log.rotation_job_id else None,
            "action": log.action,
            "details": log.details,
            "created_at": log.created_at.isoformat() if log.created_at else None,
        }
        for log in logs
    ]
