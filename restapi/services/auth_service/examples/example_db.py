"""
MariaDbRepository 사용 예제.

실행:
    poetry run python examples/example_db.py
"""
import logging
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.db.mdb import MariaDbRepository
from src.db.model import CreateSessionParams, CreateUserParams

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    repo = MariaDbRepository(
        user=os.environ.get("DB_USER", "dev"),
        pw=os.environ.get("DB_PASSWORD", "dev"),
        dbname=os.environ.get("DB_NAME", "docker"),
        host=os.environ.get("DB_HOST", "10.1.0.119"),
        port=int(os.environ.get("DB_PORT", "33061")),
    )

    repo.init()
    logger.info("DB 연결 완료")

    try:
        # DB 시간 조회
        sysdate = repo.read_sysdate()
        logger.info("sysdate: %s", sysdate)

        # # 유저 생성
        # user = repo.create_user(
        #     CreateUserParams(
        #         username="alice1",
        #         hashed_password="$2b$12$hashed_example",
        #         full_name="Alice",
        #         email="alice@example.com",
        #     )
        # )
        # logger.info("created user: %s (%s)", user.username, user.email)

        # 유저 조회
        found = repo.read_user("alice")
        logger.info("found user: %s", found.username)

        # # 세션 생성
        # session = repo.create_user_session(
        #     CreateSessionParams(
        #         id="sess-abc-001",
        #         username="alice",
        #         refresh_token="refresh_token_value",
        #         user_agent="Mozilla/5.0",
        #         client_ip="127.0.0.1",
        #         is_blocked=0,
        #     )
        # )
        # logger.info("created session: %s", session.id)

        # 세션 조회
        found_session = repo.read_user_session("sess-abc-001")
        if found_session is None:
            logger.info("found_session is none..")
        else:
            logger.info("found session for user: %s", found_session.username)

        

        #전체세션 조회
        all_session = repo.read_all_session()
        for ss in all_session:
            logger.info("id:%s, name:%s, createat:%s", ss.id, ss.username, ss.created_at)


        # # 세션 삭제
        # repo.delete_user_session("sess-abc-001")
        # logger.info("session deleted")

    finally:
        repo.close()
        logger.info("DB 연결 종료")


if __name__ == "__main__":
    main()
