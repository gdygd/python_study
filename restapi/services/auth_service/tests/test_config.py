import os
from datetime import timedelta

import pytest

from src.config.config import Config, load_config


class TestConfigDefaults:
    def test_default_environment(self):
        cfg = Config()
        assert cfg.environment == "development"

    def test_default_db_port(self):
        cfg = Config()
        assert cfg.db_port == 3306

    def test_default_http_server_address(self):
        cfg = Config()
        assert cfg.http_server_address == "0.0.0.0:8080"

    def test_default_access_token_duration(self):
        cfg = Config()
        assert cfg.access_token_duration == timedelta(minutes=15)

    def test_default_refresh_token_duration(self):
        cfg = Config()
        assert cfg.refresh_token_duration == timedelta(hours=24)

    def test_default_process_interval(self):
        cfg = Config()
        assert cfg.process_interval == timedelta(seconds=10)


class TestConfigFromEnv:
    def test_load_from_env_vars(self, monkeypatch):
        monkeypatch.setenv("ENVIRONMENT", "production")
        monkeypatch.setenv("DB_ADDRESS", "db.example.com")
        monkeypatch.setenv("DB_PORT", "5432")
        monkeypatch.setenv("DB_USER", "admin")
        monkeypatch.setenv("DB_NAME", "auth_db")

        cfg = Config()

        assert cfg.environment == "production"
        assert cfg.db_address == "db.example.com"
        assert cfg.db_port == 5432
        assert cfg.db_user == "admin"
        assert cfg.db_name == "auth_db"

    def test_duration_from_env_minutes(self, monkeypatch):
        monkeypatch.setenv("ACCESS_TOKEN_DURATION", "30m")
        cfg = Config()
        assert cfg.access_token_duration == timedelta(minutes=30)

    def test_duration_from_env_hours(self, monkeypatch):
        monkeypatch.setenv("REFRESH_TOKEN_DURATION", "48h")
        cfg = Config()
        assert cfg.refresh_token_duration == timedelta(hours=48)

    def test_duration_from_env_seconds(self, monkeypatch):
        monkeypatch.setenv("PROCESS_INTERVAL", "30s")
        cfg = Config()
        assert cfg.process_interval == timedelta(seconds=30)

    def test_duration_from_env_plain_int(self, monkeypatch):
        monkeypatch.setenv("ACCESS_TOKEN_DURATION", "900")
        cfg = Config()
        assert cfg.access_token_duration == timedelta(seconds=900)

    def test_debug_level(self, monkeypatch):
        monkeypatch.setenv("DEBUG_LV", "2")
        cfg = Config()
        assert cfg.debug_lv == 2

    def test_token_key(self, monkeypatch):
        monkeypatch.setenv("TOKEN_SYMMETRIC_KEY", "supersecretkey123456789012345678")
        cfg = Config()
        assert cfg.token_symmetric_key == "supersecretkey123456789012345678"


class TestLoadConfig:
    def test_load_config_from_file(self, tmp_path):
        env_file = tmp_path / "app.env"
        env_file.write_text(
            "ENVIRONMENT=staging\n"
            "DB_ADDRESS=staging-db.internal\n"
            "DB_PORT=3306\n"
            "DB_USER=svc_user\n"
            "DB_PASSWD=secret\n"
            "DB_NAME=auth\n"
            "ACCESS_TOKEN_DURATION=15m\n"
            "REFRESH_TOKEN_DURATION=24h\n"
            "HTTP_SERVER_ADDRESS=0.0.0.0:8080\n"
            "TOKEN_SYMMETRIC_KEY=12345678901234567890123456789012\n"
        )

        cfg = load_config(str(tmp_path))

        assert cfg.environment == "staging"
        assert cfg.db_address == "staging-db.internal"
        assert cfg.db_user == "svc_user"
        assert cfg.db_passwd == "secret"
        assert cfg.access_token_duration == timedelta(minutes=15)
        assert cfg.refresh_token_duration == timedelta(hours=24)

    def test_load_config_missing_file_uses_defaults(self, tmp_path):
        cfg = load_config(str(tmp_path))
        assert cfg.environment == "development"
        assert cfg.db_port == 3306
