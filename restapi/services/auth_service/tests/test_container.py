from unittest.mock import MagicMock, patch

import pytest

from src.container.container import Container, new_container


@pytest.fixture(autouse=True)
def reset_container():
    """각 테스트 전후로 싱글톤 상태를 초기화한다."""
    import src.container.container as mod
    mod._container = None
    yield
    mod._container = None


class TestNewContainer:
    def test_returns_container_instance(self, monkeypatch):
        mock_config = MagicMock()
        mock_repo = MagicMock()

        with patch("src.container.container._init_config", return_value=mock_config), \
             patch("src.container.container._init_database", return_value=mock_repo):
            c = new_container()

        assert isinstance(c, Container)

    def test_container_has_config(self, monkeypatch):
        mock_config = MagicMock()
        mock_repo = MagicMock()

        with patch("src.container.container._init_config", return_value=mock_config), \
             patch("src.container.container._init_database", return_value=mock_repo):
            c = new_container()

        assert c.config is mock_config

    def test_container_has_db_hnd(self):
        mock_config = MagicMock()
        mock_repo = MagicMock()

        with patch("src.container.container._init_config", return_value=mock_config), \
             patch("src.container.container._init_database", return_value=mock_repo):
            c = new_container()

        assert c.db_hnd is mock_repo

    def test_sets_global_singleton(self):
        import src.container.container as mod

        mock_config = MagicMock()
        mock_repo = MagicMock()

        with patch("src.container.container._init_config", return_value=mock_config), \
             patch("src.container.container._init_database", return_value=mock_repo):
            c = new_container()

        assert mod._container is c

    def test_raises_on_config_error(self):
        with patch("src.container.container._init_config", side_effect=Exception("file not found")):
            with pytest.raises(RuntimeError, match="config loading error"):
                new_container()

    def test_db_init_error_does_not_raise(self):
        """DB 초기화 실패 시 예외를 던지지 않고 repo를 반환한다 (Go 동작과 동일)."""
        mock_config = MagicMock()
        mock_repo = MagicMock()
        mock_repo.init.side_effect = Exception("connection refused")

        with patch("src.container.container._init_config", return_value=mock_config), \
             patch("src.container.container.MariaDbRepository", return_value=mock_repo):
            c = new_container()  # 예외 없이 반환되어야 한다

        assert c.db_hnd is mock_repo

    def test_init_database_passes_config_fields(self):
        mock_config = MagicMock()
        mock_config.db_user = "admin"
        mock_config.db_passwd = "secret"
        mock_config.db_name = "auth_db"
        mock_config.db_address = "127.0.0.1"
        mock_config.db_port = 3306

        mock_repo = MagicMock()

        with patch("src.container.container._init_config", return_value=mock_config), \
             patch("src.container.container.MariaDbRepository", return_value=mock_repo) as mock_cls:
            new_container()

        mock_cls.assert_called_once_with(
            user="admin",
            pw="secret",
            dbname="auth_db",
            host="127.0.0.1",
            port=3306,
        )
