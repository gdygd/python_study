from datetime import datetime, timezone

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from myapp.logger.logger import log

from ..request import RenewAccessTokenRequest
from ..response import RenewAccessTokenResponse, error_response

router = APIRouter(tags=["token"])


@router.post("/renew_access")
async def renew_access_token(req: RenewAccessTokenRequest, request: Request) -> JSONResponse:
    db_hnd = request.app.state.db_hnd

    # TODO: JWT refresh_token 검증
    # refresh_payload = token_maker.verify_token(req.refresh_token)
    # session_id = refresh_payload.id
    session_id = req.refresh_token  # placeholder

    try:
        session = db_hnd.read_user_session(session_id)
    except Exception as e:
        return JSONResponse(status_code=500, content=error_response(str(e)).model_dump())

    if session is None:
        return JSONResponse(status_code=401, content=error_response("session not found").model_dump())

    if session.is_blocked:
        return JSONResponse(status_code=401, content=error_response("session is blocked").model_dump())

    if session.refresh_token != req.refresh_token:
        return JSONResponse(status_code=401, content=error_response("mismatched session token").model_dump())

    if session.expires_at and datetime.now(timezone.utc) > session.expires_at:
        return JSONResponse(status_code=401, content=error_response("expired session token").model_dump())

    # TODO: 새 access_token 발급
    # access_token, access_payload = token_maker.create_token(session.username, cfg.access_token_duration)
    now = datetime.now(timezone.utc)
    rsp = RenewAccessTokenResponse(
        access_token="placeholder_access_token",
        access_token_expires_at=now,
    )
    return JSONResponse(status_code=200, content=rsp.model_dump(mode="json"))
