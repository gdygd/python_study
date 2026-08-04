from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from myapp.db.model import CreateUserParams
from myapp.logger.logger import log

from ..request import CreateUserRequest
from ..response import UserResponse, error_response, success_response

router = APIRouter(tags=["user"])


@router.post("")
async def create_user(req: CreateUserRequest, request: Request) -> JSONResponse:
    log.print(3, "create_user...")
    # db_hnd = request.app.state.db_hnd

    # TODO: 비밀번호 해싱 (bcrypt)
    hashed_password = req.password  # placeholder

    arg = CreateUserParams(
        username=req.username,
        hashed_password=hashed_password,
        full_name=req.full_name,
        email=req.email,
    )

    
    service = request.app.state.service
    user = service.create_user(arg)
    log.print(3, "user : {}", user)

    # try:
    #     user = db_hnd.create_user(arg)
    # except Exception as e:
    #     log.error("createUser err={}", str(e))
    #     return JSONResponse(status_code=500, content=error_response(str(e)).model_dump())

    resp = UserResponse(
        username=user.username,
        email=user.email,
        created_at=user.created_at,
    )
    return JSONResponse(status_code=200, content=success_response(resp.model_dump(mode="json")).model_dump())
