from datetime import timedelta
from pathlib import Path
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_duration(value: Any) -> timedelta:
    """Parse duration from Go-style string (15m, 1h, 30s) or seconds (int/float)."""
    if isinstance(value, timedelta):
        return value
    if isinstance(value, (int, float)):
        return timedelta(seconds=value)
    s = str(value).strip()
    if s.endswith("h"):
        return timedelta(hours=float(s[:-1]))
    if s.endswith("m"):
        return timedelta(minutes=float(s[:-1]))
    if s.endswith("s"):
        return timedelta(seconds=float(s[:-1]))
    return timedelta(seconds=float(s))


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="app.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General
    environment: str = "development"
    debug_lv: int = 0

    # Database
    db_driver: str = "mysql"
    db_address: str = "127.0.0.1"
    db_port: int = 3306
    db_user: str = ""
    db_passwd: str = ""
    db_name: str = ""

    # Redis
    redis_address: str = "127.0.0.1:6379"

    # Token
    token_symmetric_key: str = ""
    access_token_duration: timedelta = timedelta(minutes=15)
    refresh_token_duration: timedelta = timedelta(hours=24)

    # Server
    http_server_address: str = "0.0.0.0:8080"
    grpc_server_address: str = "0.0.0.0:9090"
    grpc_gw_server_address: str = "0.0.0.0:9091"
    http_allow_origins: str = "*"
    cookie_domain: str = ""

    # Process
    process_interval: timedelta = timedelta(seconds=10)

    @field_validator("access_token_duration", "refresh_token_duration", "process_interval", mode="before")
    @classmethod
    def parse_duration(cls, v: Any) -> timedelta:
        return _parse_duration(v)


def load_config(path: str = ".") -> Config:
    """Load configuration from app.env in the given directory path."""
    env_file = Path(path) / "app.env"
    return Config(_env_file=str(env_file))
