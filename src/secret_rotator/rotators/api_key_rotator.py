import secrets as stdlib_secrets

from secret_rotator.models.secret import Secret
from secret_rotator.rotators.base import RotationResult


class ApiKeyRotator:
    async def generate_new_value(self, secret: Secret) -> RotationResult:
        prefix = secret.config.get("prefix", "sk")
        key = f"{prefix}_{stdlib_secrets.token_urlsafe(40)}"
        return RotationResult(new_value=key)

    async def activate_new_value(
        self, secret: Secret, new_value: str, old_value: str | None
    ) -> None:
        pass

    async def verify_new_value(self, secret: Secret, new_value: str) -> bool:
        return len(new_value) > 10

    async def revoke_old_value(self, secret: Secret, old_value: str) -> None:
        pass
