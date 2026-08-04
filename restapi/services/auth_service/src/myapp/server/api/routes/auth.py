import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from myapp.db.model import CreateSessionParams
from myapp.logger.logger import log

from ..request import LoginUserRequest, LogoutUserRequest
from ..response import LoginUserResponse, UserResponse, error_response, success_response

router = APIRouter(tags=["auth"])


@router.post("/login")
async def login_user(req: LoginUserRequest, request: Request) -> JSONResponse:
    log.info("loginUser username={}", req.username)
    db_hnd = request.app.state.db_hnd

    try:
        user = db_hnd.read_user(req.username)
    except Exception as e:
        log.error("loginUser read_user err={}", str(e))
        return JSONResponse(status_code=500, content=error_response(str(e)).model_dump())

    # TODO: 비밀번호 검증 (bcrypt)
    # if not check_password(req.password, user.hashed_password):
    #     return JSONResponse(status_code=401, content=error_response("invalid password").model_dump())

    # TODO: JWT 토큰 발급 (token_maker 구현 후 교체)
    # access_token, access_payload = token_maker.create_token(user.username, cfg.access_token_duration)
    # refresh_token, refresh_payload = token_maker.create_token(user.username, cfg.refresh_token_duration)

    session_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc)

    arg = CreateSessionParams(
        id=session_id,
        username=user.username,
        refresh_token="placeholder_refresh_token",
        user_agent=request.headers.get("user-agent", ""),
        client_ip=request.client.host if request.client else "",
        is_blocked=0,
        expires_at=now,
    )

    try:
        session = db_hnd.create_user_session(arg)
    except Exception as e:
        log.error("loginUser create_session err={}", str(e))
        return JSONResponse(status_code=500, content=error_response(str(e)).model_dump())

    rsp = LoginUserResponse(
        session_id=session.id,
        access_token="placeholder_access_token",
        access_token_expires_at=now,
        refresh_token="placeholder_refresh_token",
        refresh_token_expires_at=now,
        user=UserResponse(username=user.username, email=user.email),
    )
    return JSONResponse(status_code=200, content=rsp.model_dump(mode="json"))


@router.post("/logout")
async def logout_user(req: LogoutUserRequest, request: Request) -> JSONResponse:
    db_hnd = request.app.state.db_hnd

    # TODO: JWT 토큰 검증 후 session_id 추출
    # refresh_payload = token_maker.verify_token(req.refresh_token)
    # session_id = refresh_payload.id
    session_id = req.refresh_token  # placeholder

    try:
        db_hnd.delete_user_session(session_id)
    except Exception as e:
        log.error("logoutUser err={}", str(e))
        return JSONResponse(status_code=500, content=error_response(str(e)).model_dump())

    return JSONResponse(status_code=200, content=success_response("logged out successfully").model_dump())
