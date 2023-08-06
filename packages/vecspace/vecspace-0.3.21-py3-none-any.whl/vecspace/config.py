from pydantic import BaseSettings
from typing import List

TELEMETRY_WHITELISTED_SETTINGS = ["vecspace_impl", "vecspace_api_impl", "vecspace_server_ssl_enabled"]


class Settings(BaseSettings):
    environment: str = ""

    vecspace_impl: str = "duckdb"
    vecspace_api_impl: str = "local"

    clickhouse_host: str = None
    clickhouse_port: str = None

    persist_directory: str = ".vecspace"

    vecspace_server_host: str = None
    vecspace_server_http_port: str = None
    vecspace_server_ssl_enabled: bool = False
    vecspace_server_grpc_port: str = None
    vecspace_server_cors_allow_origins: List[str] = []  # eg ["http://localhost:3000"]

    anonymized_telemetry: bool = True

    def __getitem__(self, item):
        return getattr(self, item)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
