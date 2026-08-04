import asyncio
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import time
from myapp.logger.logger import log

router = APIRouter(tags=["system"])


@router.get("/heartbeat")
async def heartbeat() -> JSONResponse:
    return JSONResponse(status_code=200, content=None)


@router.get("/terminate")
async def terminate(request: Request) -> JSONResponse:
    log.info("Accept terminate command..")
    uv_server = request.app.state.uv_server
    if uv_server:
        uv_server.should_exit = True
    return JSONResponse(status_code=200, content=None)


@router.get("/test")
async def testapi(request: Request) -> JSONResponse:
    db_hnd = request.app.state.db_hnd
    try:
        sysdate = db_hnd.read_sysdate()
        log.info("testapi sysdate={}", sysdate)
    except Exception as e:
        log.error("testapi err={}", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})    
    
    # time.sleep(7)
    await asyncio.sleep(7)

    # start = time.time()
    # while time.time() - start < 7:
    #     # 반복 작업
    #     pass

    # print("7초 경과")
    
    return JSONResponse(status_code=200, content={"sysdate": sysdate})
