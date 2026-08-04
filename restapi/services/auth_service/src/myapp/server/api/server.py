import asyncio

import uvicorn
from fastapi import FastAPI

from myapp.config import Config
from myapp.db import DbHandler
from myapp.logger.logger import log

from .middleware import AuthMiddleware, build_cors_middleware
from .router import router

from myapp.service import ServiceInterface
from myapp.service.api.apiservice import ApiService

R_TIMEOUT = 5
SHUTDOWN_TIMEOUT = 5  # graceful shutdown 최대 대기 시간 (초)


class Server:

    def __init__(self, ct) -> None:
        self._config: Config = ct.config
        self._db_hnd: DbHandler = ct.db_hnd
        self._app = FastAPI()
        self._uv_server: uvicorn.Server | None = None
        self._serve_done = asyncio.Event()  # serve() 완료 시 세팅

        self._service: ServiceInterface = ApiService(ct.db_hnd)

        self._setup_router()

    def _setup_router(self) -> None:
        origins = [o.strip() for o in self._config.http_allow_origins.split(",")]

        cls, kwargs = build_cors_middleware(origins)
        self._app.add_middleware(cls, **kwargs)

        # self._app.add_middleware(AuthMiddleware)

        self._app.state.db_hnd = self._db_hnd
        self._app.state.config = self._config
        self._app.state.service = self._service
        self._app.include_router(router)

    async def start(self) -> None:
        """이벤트 루프 안에서 uvicorn을 실행한다 (serve() 사용)."""
        host, port_str = self._config.http_server_address.rsplit(":", 1)
        uv_config = uvicorn.Config(
            self._app,
            host=host,
            port=int(port_str),
            timeout_keep_alive=R_TIMEOUT,
            log_level="warning",
        )
        self._uv_server = uvicorn.Server(uv_config)
        self._app.state.uv_server = self._uv_server
        log.info("FastAPI server start. addr={}", self._config.http_server_address)
        try:
            await self._uv_server.serve()
        except asyncio.CancelledError:
            pass  # force_exit 시 정상적으로 발생하는 취소 신호
        finally:
            self._serve_done.set()  # serve() 리턴 = 서버 완전 종료

    async def shutdown(self, timeout: int = SHUTDOWN_TIMEOUT) -> None:
        """Graceful shutdown.

        Go의 srv.Shutdown(context.WithTimeout(ctx, 5s)) 와 동일한 메커니즘.
        timeout 내 완료되지 않으면 force_exit으로 강제 종료 후 serve() 완전 종료를 기다린다.
        """
        if self._uv_server is None:
            return

        # 새로운 요청은 안받고, 서버가 종료되길 기다림.
        self._uv_server.should_exit = True
        log.info("server graceful shutdown requested (timeout={}s)", timeout)

        try:
            await asyncio.wait_for(self._serve_done.wait(), timeout=timeout)
            log.info("server shutdown complete")
        except asyncio.TimeoutError:
            log.error("server shutdown timed out after {}s, forcing exit", timeout)
            self._uv_server.force_exit = True   # 강제 종료
            await self._serve_done.wait()   # 강제종료 끝날때 까지 대기
            log.info("server force exit complete")
