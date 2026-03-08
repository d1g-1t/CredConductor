from typing import Protocol

from secret_rotator.models.dependent import DependentService
from secret_rotator.schemas.rotation import RotationNotification


class BaseNotifier(Protocol):
    async def notify(
        self,
        dependent: DependentService,
        notification: RotationNotification,
    ) -> None: ...
