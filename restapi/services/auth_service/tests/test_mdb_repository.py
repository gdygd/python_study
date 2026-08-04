"""
MariaDbRepository 테스트.
외부 DB 의존성은 Mock 처리한다.
"""
from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.db.db_handler import DbHandler
from src.db.mdb import MariaDbRepository
from src.db.model import CreateUserParams, CreateSessionParams


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def repo_with_mock_engine():
    """SQLAlchemy Engine을 mock한 MariaDbRepository."""
    repo = MariaDbRepository(
        user="test", pw="test", dbname="testdb", host="localhost", port=3306
    )

    mock_cursor = MagicMock()
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
    mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)

    mock_engine = MagicMock()
    mock_engine.raw_connection.return_value = mock_conn

    repo._handler._engine = mock_engine
    return repo, mock_conn, mock_cursor


# ── Protocol 준수 확인 ────────────────────────────────────────────────────────

def test_mariadb_repository_implements_db_handler():
    repo = MariaDbRepository(
        user="u", pw="p", dbname="db", host="localhost", port=3306
    )
    assert isinstance(repo, DbHandler)


# ── read_sysdate ──────────────────────────────────────────────────────────────

def test_read_sysdate_returns_string(repo_with_mock_engine):
    repo, _, mock_cursor = repo_with_mock_engine
    mock_cursor.fetchone.return_value = {"dt": datetime(2026, 3, 17, 11, 0, 0)}

    result = repo.read_sysdate()

    assert result == "2026-03-17 11:00:00"


# ── read_user ─────────────────────────────────────────────────────────────────

def test_read_user_returns_user(repo_with_mock_engine):
    repo, _, mock_cursor = repo_with_mock_engine
    mock_cursor.fetchone.return_value = {
        "username": "alice",
        "hashed_password": "hashed",
        "full_name": "Alice",
        "email": "alice@example.com",
        "password_changed_at": None,
        "created_at": None,
    }

    user = repo.read_user("alice")

    assert user.username == "alice"
    assert user.email == "alice@example.com"


def test_read_user_raises_when_not_found(repo_with_mock_engine):
    repo, _, mock_cursor = repo_with_mock_engine
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="user not found"):
        repo.read_user("nobody")


# ── read_user_session ─────────────────────────────────────────────────────────

def test_read_user_session_returns_session(repo_with_mock_engine):
    repo, _, mock_cursor = repo_with_mock_engine
    mock_cursor.fetchone.return_value = {
        "id": "sess-001",
        "username": "alice",
        "refresh_token": "token123",
        "user_agent": "Mozilla",
        "client_ip": "127.0.0.1",
        "is_blocked": 0,
        "expires_at": None,
        "created_at": None,
    }

    session = repo.read_user_session("sess-001")

    assert session.id == "sess-001"
    assert session.username == "alice"
    assert session.is_blocked == 0


def test_read_user_session_raises_when_not_found(repo_with_mock_engine):
    repo, _, mock_cursor = repo_with_mock_engine
    mock_cursor.fetchone.return_value = None

    with pytest.raises(ValueError, match="session not found"):
        repo.read_user_session("no-session")


# ── create_user ───────────────────────────────────────────────────────────────

def test_create_user_returns_user(repo_with_mock_engine):
    repo, mock_conn, mock_cursor = repo_with_mock_engine
    mock_cursor.fetchone.return_value = {
        "username": "bob",
        "hashed_password": "hashed_pw",
        "full_name": "Bob",
        "email": "bob@example.com",
        "password_changed_at": None,
        "created_at": None,
    }

    arg = CreateUserParams(
        username="bob",
        hashed_password="hashed_pw",
        full_name="Bob",
        email="bob@example.com",
    )
    user = repo.create_user(arg)

    mock_conn.commit.assert_called()
    assert user.username == "bob"


def test_create_user_rollback_on_error(repo_with_mock_engine):
    repo, mock_conn, mock_cursor = repo_with_mock_engine
    mock_cursor.execute.side_effect = Exception("insert error")

    arg = CreateUserParams(
        username="bob",
        hashed_password="hashed_pw",
        full_name="Bob",
        email="bob@example.com",
    )

    with pytest.raises(Exception, match="insert error"):
        repo.create_user(arg)

    mock_conn.rollback.assert_called_once()


# ── delete_user_session ───────────────────────────────────────────────────────

def test_delete_user_session_commits(repo_with_mock_engine):
    repo, mock_conn, _ = repo_with_mock_engine

    repo.delete_user_session("sess-001")

    mock_conn.commit.assert_called_once()


def test_delete_user_session_rollback_on_error(repo_with_mock_engine):
    repo, mock_conn, mock_cursor = repo_with_mock_engine
    mock_cursor.execute.side_effect = Exception("delete error")

    with pytest.raises(Exception, match="delete error"):
        repo.delete_user_session("sess-001")

    mock_conn.rollback.assert_called_once()


# ── init / close ──────────────────────────────────────────────────────────────

def test_get_connection_raises_before_init():
    repo = MariaDbRepository(
        user="u", pw="p", dbname="db", host="localhost", port=3306
    )
    with pytest.raises(RuntimeError, match="not initialized"):
        repo._handler.get_connection()


def test_close_clears_engine(repo_with_mock_engine):
    repo, _, _ = repo_with_mock_engine
    repo.close()
    assert repo._handler._engine is None
