#import logging

import pymysql.cursors

from myapp.db.mdb.mdb_handler import MariaDbHandler
from myapp.db.model import Session, User
from myapp.logger import log

_DICT_CURSOR = pymysql.cursors.DictCursor

# logger = logging.getLogger(__name__)


def read_sysdate(handler: MariaDbHandler) -> str:
    query = "SELECT now() AS dt FROM dual"

    log.print(3, "read_sysdate.. %s", query)

    conn = handler.get_connection()
    try:
        with conn.cursor(_DICT_CURSOR) as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
            return str(row["dt"]) if row else ""
    except Exception as e:
        log.error("read_sysdate failed", exc_info=e)
        raise
    finally:
        conn.close()


def read_user(handler: MariaDbHandler, username: str) -> User:
    query = """
        SELECT username
             , hashed_password
             , full_name
             , email
             , password_changed_at
             , created_at
          FROM users
         WHERE username = %s
    """

    conn = handler.get_connection()
    try:
        with conn.cursor(_DICT_CURSOR) as cursor:
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            if row is None:
                raise ValueError(f"user not found: {username}")
            return User(
                username=row["username"],
                hashed_password=row["hashed_password"],
                full_name=row["full_name"],
                email=row["email"],
                password_changed_at=row["password_changed_at"],
                created_at=row["created_at"],
            )
    except Exception as e:
        log.error("read_user failed", exc_info=e)
        raise
    finally:
        conn.close()


def read_user_session(handler: MariaDbHandler, session_id: str) -> Session | None:
    query = """
        SELECT id
             , username
             , refresh_token
             , user_agent
             , client_ip
             , is_blocked
             , expires_at
             , created_at
          FROM sessions
         WHERE id = %s
    """

    conn = handler.get_connection()
    try:
        with conn.cursor(_DICT_CURSOR) as cursor:
            cursor.execute(query, (session_id,))
            row = cursor.fetchone()
            if row is None:
                raise ValueError(f"session not found: {session_id}")
            return Session(
                id=row["id"],
                username=row["username"],
                refresh_token=row["refresh_token"],
                user_agent=row["user_agent"],
                client_ip=row["client_ip"],
                is_blocked=row["is_blocked"],
                expires_at=row["expires_at"],
                created_at=row["created_at"],
            )
    except Exception as e:
        # log.error("read_user_session failed", exc_info=e)
        # raise
        return None
    finally:
        conn.close()

def read_all_sessions(handler: MariaDbHandler) -> list[Session]:
    query = """
        SELECT id
             , username
             , refresh_token
             , user_agent
             , client_ip
             , is_blocked
             , expires_at
             , created_at
          FROM sessions
    """

    conn = handler.get_connection()
    try:
        with conn.cursor(_DICT_CURSOR) as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

            sessions: list[Session] = []
            for row in rows:
                session = Session(
                    id=row["id"],
                    username=row["username"],
                    refresh_token=row["refresh_token"],
                    user_agent=row["user_agent"],
                    client_ip=row["client_ip"],
                    is_blocked=row["is_blocked"],
                    expires_at=row["expires_at"],
                    created_at=row["created_at"],
                )
                sessions.append(session)
            
            return sessions
    except Exception as e:
        log.error("read_all_session failed", exc_info=e)
        raise
    finally:
        conn.close()


def delete_user_session(handler: MariaDbHandler, session_id: str) -> None:
    query = "DELETE FROM sessions WHERE id = %s"

    conn = handler.get_connection()
    try:
        with conn.cursor(_DICT_CURSOR) as cursor:
            cursor.execute(query, (session_id,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        log.error("delete_user_session failed", exc_info=e)
        raise
    finally:
        conn.close()
