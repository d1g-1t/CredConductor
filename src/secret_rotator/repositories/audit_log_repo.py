import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from secret_rotator.models.audit_log import AuditLog


class AuditLogRepository:
    async def create(self, session: AsyncSession, log: AuditLog) -> AuditLog:
        session.add(log)
        await session.flush()
        return log

    async def list_all(self, session: AsyncSession, limit: int = 100) -> list[AuditLog]:
        result = await session.execute(
            select(AuditLog).order_by(AuditLog.created_at.desc()).limit(limit)
        )
        return list(result.scalars().all())

    async def list_by_secret(
        self, session: AsyncSession, secret_id: uuid.UUID, limit: int = 100
    ) -> list[AuditLog]:
        result = await session.execute(
            select(AuditLog)
            .where(AuditLog.secret_id == secret_id)
            .order_by(AuditLog.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())
