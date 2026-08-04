from myapp.db.mdb.mdb_handler import MariaDbHandler
from myapp.db.mdb import mdb_c, mdb_r
from myapp.db.db_handler import DbHandler
from myapp.db.model import CreateSessionParams, CreateUserParams, Session, User


class MariaDbRepository(DbHandler):
    """DbHandler 인터페이스의 MariaDB 구현체."""

    def __init__(
        self,
        user: str,
        pw: str,
        dbname: str,
        host: str,
        port: int,
    ) -> None:
        self._handler = MariaDbHandler(user, pw, dbname, host, port)

    def init(self) -> None:
        self._handler.init()

    def close(self) -> None:
        self._handler.close()

    def read_sysdate(self) -> str:
        return mdb_r.read_sysdate(self._handler)

    def read_user(self, username: str) -> User:
        return mdb_r.read_user(self._handler, username)

    def read_user_session(self, session_id: str) -> Session | None:
        return mdb_r.read_user_session(self._handler, session_id)
    
    def read_all_session(self) -> list[Session]:
        return mdb_r.read_all_sessions(self._handler)


    def create_user(self, arg: CreateUserParams) -> User:
        return mdb_c.create_user(self._handler, arg)

    def create_user_session(self, arg: CreateSessionParams) -> Session:
        return mdb_c.create_user_session(self._handler, arg)

    def delete_user_session(self, session_id: str) -> None:
        mdb_r.delete_user_session(self._handler, session_id)


__all__ = ["MariaDbRepository"]
