import asyncio
from typing import Protocol, runtime_checkable

from myapp.logger.logger import log
from myapp.server.api import Server as ApiServer


# ============================================================================
# Server 인터페이스 - REST, gRPC, Socket 등 모든 서버가 구현해야 하는 Protocol
# ============================================================================

@runtime_checkable
class ServerProtocol(Protocol):
    async def start(self) -> None: ...
    async def shutdown(self) -> None: ...


# ============================================================================
# Application - 여러 서버를 하나의 이벤트 루프에서 async task로 관리
# ============================================================================

class Application:

    def __init__(self, servers: list[ServerProtocol]) -> None:
        self._servers = servers
        self._tasks: list[asyncio.Task] = []

    async def run(self) -> None:
        """각 서버를 독립적인 async task로 생성하고 모두 완료될 때까지 대기한다."""
        self._tasks = [
            asyncio.create_task(server.start(), name=type(server).__name__)
            for server in self._servers
        ]
        log.print(3, "Application started {} server(s)", len(self._tasks))
        await asyncio.gather(*self._tasks, return_exceptions=True)

    async def shutdown(self) -> None:
        """각 서버에 shutdown을 요청한다. serve() 루프가 끝나면 task가 자연히 완료된다."""
        log.print(3, "Application shutdown start")
        for server in self._servers:
            log.print(3, "shutdown server: {}", type(server).__name__)
            await server.shutdown()
        log.print(3, "Application shutdown complete")


# ============================================================================
# Factory
# ============================================================================

def new_application(ct) -> Application:
    servers: list[ServerProtocol] = []

    # REST API 서버
    try:
        api_server = ApiServer(ct)
        servers.append(api_server)
    except Exception as e:
        log.error("Api server initialization fail.. {}", str(e))

    # TODO: gRPC 서버
    # try:
    #     grpc_server = GrpcServer(ct)
    #     servers.append(grpc_server)
    # except Exception as e:
    #     log.error("gRPC server initialization fail.. {}", str(e))

    # TODO: Socket 서버
    # try:
    #     socket_server = SocketServer(ct)
    #     servers.append(socket_server)
    # except Exception as e:
    #     log.error("Socket server initialization fail.. {}", str(e))

    return Application(servers)
