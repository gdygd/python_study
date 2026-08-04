import threading

import uvicorn
from fastapi import FastAPI

from src.config import Config
from src.db import DbHandler
from src.logger.logger import log

from .middleware import AuthMiddleware, build_cors_middleware
from .router import router

R_TIMEOUT = 5
W_TIMEOUT = 5


class Server:

    def __init__(self, ct) -> None:
        self._config: Config = ct.config
        self._db_hnd: DbHandler = ct.db_hnd
        self._app = FastAPI()
        self._uv_server: uvicorn.Server | None = None
        self._thread: threading.Thread | None = None

        self._setup_router()

    def _setup_router(self) -> None:
        origins = [o.strip() for o in self._config.http_allow_origins.split(",")]

        # CORS 미들웨어
        cls, kwargs = build_cors_middleware(origins)
        self._app.add_middleware(cls, **kwargs)

        # Auth 미들웨어 (주석 해제하면 활성화)
        # self._app.add_middleware(AuthMiddleware)

        # app.state에 의존 객체 주입
        self._app.state.db_hnd = self._db_hnd
        self._app.state.config = self._config

        # 라우터 등록
        self._app.include_router(router)

    def start(self) -> None:
        """서버를 시작한다 (블로킹)."""
        host, port_str = self._config.http_server_address.rsplit(":", 1)
        uv_config = uvicorn.Config(
            self._app,
            host=host,
            port=int(port_str),
            timeout_keep_alive=R_TIMEOUT,
            log_level="warning",
        )
        self._uv_server = uvicorn.Server(uv_config)
        # terminate 엔드포인트에서 접근할 수 있도록 state에 등록
        self._app.state.uv_server = self._uv_server
        log.info("FastAPI server start. addr={}", self._config.http_server_address)
        self._uv_server.run()

    def start_in_thread(self) -> None:
        """별도 스레드에서 서버를 시작한다."""
        self._thread = threading.Thread(target=self.start, daemon=True)
        self._thread.start()

    def shutdown(self) -> None:
        """Graceful shutdown (최대 5초 대기)."""
        if self._uv_server:
            self._uv_server.should_exit = True
            log.info("server shutdown requested")
        if self._thread:
            self._thread.join(timeout=W_TIMEOUT)
        log.info("server shutdown complete")
