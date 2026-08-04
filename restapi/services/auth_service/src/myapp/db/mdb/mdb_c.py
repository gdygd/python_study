from myapp.db.mdb.mdb_handler import MariaDbHandler
from myapp.db.mdb.mdb_r import read_user, read_user_session
from myapp.db.model import CreateSessionParams, CreateUserParams, Session, User
from myapp.logger import log


def create_user(handler: MariaDbHandler, arg: CreateUserParams) -> User:
    query = """
        INSERT INTO users (
            username,
            hashed_password,
            full_name,
            email,
            password_changed_at,
            created_at
        ) VALUES (%s, %s, %s, %s, now(), now())
    """

    conn = handler.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                query,
                (arg.username, arg.hashed_password, arg.full_name, arg.email),
            )
        conn.commit()
        return read_user(handler, arg.username)
    except Exception as e:
        conn.rollback()
        log.error("create_user failed: {}", str(e))
        raise
    finally:
        conn.close()


def create_user_session(handler: MariaDbHandler, arg: CreateSessionParams) -> Session:
    query = """
        INSERT INTO sessions (
            id,
            username,
            refresh_token,
            user_agent,
            client_ip,
            is_blocked,
            expires_at,
            created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, now())
    """

    conn = handler.get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                query,
                (
                    arg.id,
                    arg.username,
                    arg.refresh_token,
                    arg.user_agent,
                    arg.client_ip,
                    arg.is_blocked,
                    arg.expires_at,
                ),
            )
        conn.commit()
        return read_user_session(handler, arg.id)
    except Exception as e:
        conn.rollback()
        log.error("create_user_session failed: {}", str(e))
        raise
    finally:
        conn.close()
