"""
Example: Loading configuration with Pydantic Settings.

Usage:
    poetry run python examples/example_config.py

The example reads from examples/app.env if it exists,
otherwise falls back to environment variables and defaults.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.config import load_config


def main() -> None:
    cfg = load_config(path=str(Path(__file__).parent))

    print("=== Config ===")
    print(f"environment          : {cfg.environment}")
    print(f"debug_lv             : {cfg.debug_lv}")
    print()
    print("=== Database ===")
    print(f"db_driver            : {cfg.db_driver}")
    print(f"db_address           : {cfg.db_address}")
    print(f"db_port              : {cfg.db_port}")
    print(f"db_user              : {cfg.db_user}")
    print(f"db_name              : {cfg.db_name}")
    print()
    print("=== Token ===")
    print(f"access_token_duration : {cfg.access_token_duration}")
    print(f"refresh_token_duration: {cfg.refresh_token_duration}")
    print()
    print("=== Server ===")
    print(f"http_server_address  : {cfg.http_server_address}")
    print(f"grpc_server_address  : {cfg.grpc_server_address}")
    print(f"grpc_gw_server_address: {cfg.grpc_gw_server_address}")
    print(f"http_allow_origins   : {cfg.http_allow_origins}")
    print()
    print("=== Process ===")
    print(f"process_interval     : {cfg.process_interval}")


if __name__ == "__main__":
    main()
