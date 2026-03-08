from secret_rotator.rotators.base import BaseRotator, RotationResult
from secret_rotator.rotators.generic_rotator import GenericRotator
from secret_rotator.rotators.database_rotator import DatabaseRotator
from secret_rotator.rotators.api_key_rotator import ApiKeyRotator
from secret_rotator.rotators.hmac_rotator import HMACRotator
from secret_rotator.models.secret import SecretType

ROTATOR_REGISTRY: dict[str, BaseRotator] = {
    SecretType.DATABASE_PASSWORD: DatabaseRotator(),
    SecretType.API_KEY: ApiKeyRotator(),
    SecretType.HMAC_SECRET: HMACRotator(),
    SecretType.SYMMETRIC_KEY: GenericRotator(),
    SecretType.OAUTH_CLIENT_SECRET: GenericRotator(),
    SecretType.GENERIC: GenericRotator(),
}


def get_rotator(secret_type: str) -> BaseRotator:
    return ROTATOR_REGISTRY.get(secret_type, GenericRotator())


__all__ = [
    "BaseRotator",
    "RotationResult",
    "GenericRotator",
    "DatabaseRotator",
    "ApiKeyRotator",
    "HMACRotator",
    "ROTATOR_REGISTRY",
    "get_rotator",
]
