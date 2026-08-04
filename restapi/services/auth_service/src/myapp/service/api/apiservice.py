from myapp.db import DbHandler
from myapp.logger.logger import log
import myapp.db.model as dbmodel


class ApiService:
    def __init__(self, db_hnd: DbHandler) -> None:
        self._db_hnd: DbHandler = db_hnd

    def read_sysdate(self) -> str: 
        try:
            sysdate = self._db_hnd.read_sysdate()
        except Exception as e:
            log.error("read_sysdate error={}", str(e))
            return ""
        return sysdate


    def read_user(self, username: str) -> dbmodel.User:
        try:
            user = self._db_hnd.read_user(username)
        except Exception as e:
            log.error("read_user error=%s", str(e))
            return dbmodel.User()
        return user


    def read_user_session(self, session_id: str) -> dbmodel.Session | None: 
        try:
            ss = self._db_hnd.read_user_session(session_id)
        except Exception as e:
            log.error("read_user_session=%s", str(e))
            return None
        return ss

    def read_all_session(self) -> list[dbmodel.Session]: 
        try:
            ss = self._db_hnd.read_all_session()
        except Exception as e:
            log.error("read_all_session error {}", str(e))
            return list[dbmodel.Session]
        return ss

    def create_user(self, arg: dbmodel.CreateUserParams) -> dbmodel.User: 
        try:
            user = self._db_hnd.create_user(arg)
        except Exception as e:
            log.error("create_user error %s", str(e))
            return dbmodel.User()
        return user
        
    def create_user_session(self, arg: dbmodel.CreateSessionParams) -> dbmodel.Session:
        try:
            ss = self._db_hnd.create_user_session(arg)
        except Exception as e:
            log.error("create_user_session {}", str(e))
            return dbmodel.Session()
        return ss

    def delete_user_session(self, session_id: str) -> None:
        try:
            self._db_hnd.delete_user_session(session_id)
        except Exception as e:
            log.error("delete_user_session %s", str(e))
        

