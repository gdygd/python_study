from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from myapp.logger.logger import log


class AuthMiddleware(BaseHTTPMiddleware):
    """JWT 토큰 검증 미들웨어. 현재는 pass-through."""

    EXCLUDED_PATHS = {"/heartbeat", "/user", "/login", "/token/renew_access"}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        log.info("authMiddleware path={}", request.url.path)

        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)

        # TODO: JWT 토큰 검증
        # authorization = request.headers.get("Authorization")
        # if not authorization or not authorization.startswith("Bearer "):
        #     return JSONResponse(status_code=401, content=error_response("missing token").model_dump())
        # token = authorization.removeprefix("Bearer ")
        # payload = verify_token(token)  # raise on invalid

        return await call_next(request)


def build_cors_middleware(origins: list[str]) -> tuple[type, dict]:
    """CORSMiddleware와 kwargs를 반환한다. app.add_middleware()에 전달."""
    log.info("cors origins={}", origins)
    return CORSMiddleware, dict(
        allow_origins=origins,
        allow_methods=["HEAD", "OPTIONS", "GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Origin", "Content-Type", "Authorization", "Accept"],
        max_age=43200,  # 12h
    )
