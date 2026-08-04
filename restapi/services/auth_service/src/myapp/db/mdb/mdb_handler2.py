import logging
import threading

# import pymysql
# import pymysql.cursors
# from sqlalchemy import Engine, create_engine, test
import pymysql
import pymysql.cursors
from sqlalchemy import Engine, create_engine, text

logger = logging.getLogger(__name__)

MAX_POOL_SIZE = 5
MAX_OVERFLOW = 0  # pool_size 초과 임시 연결 허용 수

class MariaDbHandler:

    def __init__(
        self,
        user: str,
        pw: str,
        dbname: str,
        host: str,
        port: int,
    ) -> None:
        self._user = user
        self._pw = pw
        self._dbname = dbname
        self._host = host
        self._port = port
        self._engine: Engine | None = None
        self._lock = threading.RLock()

    def init(self) -> None:
        url = f"mysql+pymysql://{self._user}:{self._pw}@{self._host}:{self._port}/{self._dbname}"
        engine = create_engine(
            url,
            pool_size=MAX_POOL_SIZE,
            max_overflow=MAX_OVERFLOW,
            pool_pre_ping=True,
            connect_args={
                "charset": "utf8mb4",
                "cursorclass": pymysql.cursors.DictCursor,
            },
        )

        # 연결확인
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        with self._lock:
            self._engine = engine

        logger.info("db open", extra={"host": self._host, "db": self._dbname})

    def get_connection(self):
        """풀에서 raw DBAPI 커넥션을 반환한다. 사용 후 반드시 close() 호출."""
        with self._lock:
            if self._engine is None:
                raise RuntimeError("db not initialized. call init() first")
            return self._engine.raw_connection()

    def close(self) -> None:
        with self._lock:
            if self._engine is not None:
                self._engine.dispose()
                self._engine = None
            logger.info("db closed")

    def exec_tx(self, fn) -> None:
        conn = self.get_connection()
        try:
            fn(conn)
            conn.commit
        except Exception as e:
            conn.rollback()
            logger.error("transaction failed", exc_info=e)
            raise
        finally:
            conn.close()

