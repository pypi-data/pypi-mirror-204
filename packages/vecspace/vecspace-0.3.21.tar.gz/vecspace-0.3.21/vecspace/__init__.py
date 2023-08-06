import vecspace.config
import logging
from vecspace.telemetry.events import ClientStartEvent
from vecspace.telemetry.posthog import Posthog

logger = logging.getLogger(__name__)

__settings = vecspace.config.Settings()

__version__ = "0.3.21"


def configure(**kwargs):
    """Override VecSpace's default settings, environment variables or .env files"""
    global __settings
    __settings = vecspace.config.Settings(**kwargs)


def get_settings():
    return __settings


def get_db(settings=__settings):
    """Return a vecspace.DB instance based on the provided or environmental settings."""

    setting = settings.vecspace_impl.lower()

    def require(key):
        assert settings[key], f"Setting '{key}' is required when vecspace_impl={setting}"

    if setting == "clickhouse":
        require("clickhouse_host")
        require("clickhouse_port")
        require("persist_directory")
        logger.info("Using Clickhouse for database")
        import vecspace.db.clickhouse

        return vecspace.db.clickhouse.Clickhouse(settings)
    elif setting == "duckdb+parquet":
        require("persist_directory")
        logger.warning(
            f"Using embedded DuckDB with persistence: data will be stored in: {settings.persist_directory}"
        )
        import vecspace.db.duckdb

        return vecspace.db.duckdb.PersistentDuckDB(settings)
    elif setting == "duckdb":
        require("persist_directory")
        logger.warning("Using embedded DuckDB without persistence: data will be transient")
        import vecspace.db.duckdb

        return vecspace.db.duckdb.DuckDB(settings)
    else:
        raise ValueError(
            f"Expected vecspace_impl to be one of clickhouse, duckdb, duckdb+parquet, got {setting}"
        )


def Client(settings=__settings):
    """Return a vecspace.API instance based on the provided or environmental
    settings, optionally overriding the DB instance."""

    setting = settings.vecspace_api_impl.lower()
    telemetry_client = Posthog(settings)

    # Submit event for client start
    telemetry_client.capture(ClientStartEvent())

    def require(key):
        assert settings[key], f"Setting '{key}' is required when vecspace_api_impl={setting}"

    if setting == "rest":
        require("vecspace_server_host")
        require("vecspace_server_http_port")
        logger.info("Running VecSpace in client mode using REST to connect to remote server")
        import vecspace.api.fastapi

        return vecspace.api.fastapi.FastAPI(settings, telemetry_client)
    elif setting == "local":
        logger.info("Running VecSpace using direct local API.")
        import vecspace.api.local

        return vecspace.api.local.LocalAPI(settings, get_db(settings), telemetry_client)
    else:
        raise ValueError(f"Expected vecspace_api_impl to be one of rest, local, got {setting}")
