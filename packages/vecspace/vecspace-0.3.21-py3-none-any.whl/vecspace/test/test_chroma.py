import unittest
import os
from unittest.mock import patch

import vecspace
import vecspace.config


class GetDBTest(unittest.TestCase):
    @patch("vecspace.db.duckdb.DuckDB", autospec=True)
    def test_default_db(self, mock):
        vecspace.get_db(vecspace.config.Settings(persist_directory="./foo"))
        assert mock.called

    @patch("vecspace.db.duckdb.PersistentDuckDB", autospec=True)
    def test_persistent_duckdb(self, mock):
        vecspace.get_db(
            vecspace.config.Settings(vecspace_impl="duckdb+parquet", persist_directory="./foo")
        )
        assert mock.called

    @patch("vecspace.db.clickhouse.Clickhouse", autospec=True)
    def test_clickhouse(self, mock):
        vecspace.get_db(
            vecspace.config.Settings(
                vecspace_impl="clickhouse",
                persist_directory="./foo",
                clickhouse_host="foo",
                clickhouse_port=666,
            )
        )
        assert mock.called


class GetAPITest(unittest.TestCase):
    @patch("vecspace.db.duckdb.DuckDB", autospec=True)
    @patch("vecspace.api.local.LocalAPI", autospec=True)
    @patch.dict(os.environ, {}, clear=True)
    def test_local(self, mock_api, mock_db):
        vecspace.Client(vecspace.config.Settings(persist_directory="./foo"))
        assert mock_api.called
        assert mock_db.called

    @patch("vecspace.api.fastapi.FastAPI", autospec=True)
    @patch.dict(os.environ, {}, clear=True)
    def test_fastapi(self, mock):
        vecspace.Client(
            vecspace.config.Settings(
                vecspace_api_impl="rest",
                persist_directory="./foo",
                vecspace_server_host="foo",
                vecspace_server_http_port="80",
            )
        )
        assert mock.called
