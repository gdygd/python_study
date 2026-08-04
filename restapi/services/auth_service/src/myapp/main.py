import asyncio
import signal

from myapp.app import new_application
from myapp.container import new_container
from myapp.logger import log

class AppVariable:    
    terminate: bool = False

# ------------------------------------------------------------------------------
# functions
# ------------------------------------------------------------------------------
def sig_handler(signum, frame):
    
    print(f"sig_handler {signum}")
    log.print(3, "sig_handler {}", signum)

    if signum == signal.SIGHUP:
        log.print(3, "SIGHUP {}", signum)        
        AppVariable.terminate = True
    elif signum == signal.SIGINT:
        log.print(3, "SIGINT {}", signum)                
        AppVariable.terminate = True
    else:
        print(f"Unknown signal:{signum}")


def init_signal():
    print("init signal")    
    signal.signal(signal.SIGHUP,  sig_handler)
    signal.signal(signal.SIGINT,  sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGUSR1, sig_handler)


async def main() -> None:
    log.print(3, "Application starting..")

    try:
        ct = new_container()
    except Exception as e:
        log.error("Container init failed: {}", str(e))
        return

    app = new_application(ct)

    # 시그널 수신 시 세팅되는 이벤트
    shutdown_event = asyncio.Event()

    signals = [
        signal.SIGHUP, signal.SIGINT, signal.SIGTERM
    ]

    loop = asyncio.get_running_loop()
    # for sig in (signal.SIGHUP, signal.SIGINT, signal.SIGTERM):
    for sig in signals:
        loop.add_signal_handler(sig, lambda s=sig: (
            log.print(3, "signal received: {}", s) or shutdown_event.set()
        ))

    # 모든 서버를 async task로 시작
    app_task = asyncio.create_task(app.run())


    print("signal...1")
    # # 시그널 대기
    await shutdown_event.wait()

    print("signal...2")
    # Graceful shutdown
    await app.shutdown()
    print("shutdown...")

    # serve() 루프가 끝나면 app_task도 자연히 완료된다
    await app_task

    log.print(3, "Application stopped.")


if __name__ == "__main__":
    asyncio.run(main())
