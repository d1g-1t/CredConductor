import re

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

SECRET_FIELDS = re.compile(
    r'("(?:password|secret|token|key|credential|value)":\s*")([^"]+)(")',
    re.IGNORECASE,
)


class SecretMaskingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        return await call_next(request)
