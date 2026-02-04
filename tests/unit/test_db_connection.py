"""
Unit tests for database connection module.

測試項目:
- DatabaseConfig 配置載入
- get_connection 連線建立
- 重試機制
- 錯誤處理
"""

import pytest
from unittest.mock import patch, MagicMock
import pyodbc
from src.db.connection import DatabaseConfig, get_connection, test_connection


class TestDatabaseConfig:
    """測試 DatabaseConfig 類別。"""

    @patch.dict(
        "os.environ",
        {
            "DB_SERVER": "testserver",
            "DB_PORT": "1433",
            "DB_DATABASE": "testdb",
            "DB_USERNAME": "testuser",
            "DB_PASSWORD": "testpass",
            "DB_DRIVER": "ODBC Driver 18 for SQL Server",
        },
    )
    def test_config_loads_from_env(self):
        """測試從環境變數載入配置。"""
        config = DatabaseConfig()

        assert config.server == "testserver"
        assert config.port == "1433"
        assert config.database == "testdb"
        assert config.username == "testuser"
        assert config.password == "testpass"

    @patch.dict(
        "os.environ",
        {
            "DB_SERVER": "testserver",
            "DB_DATABASE": "testdb",
        },
    )
    def test_connection_string_format(self):
        """測試連線字串格式正確。"""
        config = DatabaseConfig()
        conn_string = config.get_connection_string()

        assert "DRIVER={ODBC Driver 18 for SQL Server}" in conn_string
        assert "SERVER=testserver," in conn_string
        assert "DATABASE=testdb" in conn_string
        assert "TrustServerCertificate=yes" in conn_string


class TestGetConnection:
    """測試 get_connection 函式。"""

    @patch("src.db.connection.pyodbc.connect")
    def test_successful_connection(self, mock_connect):
        """測試成功建立連線。"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn

        conn = get_connection(max_retries=1)

        assert conn == mock_conn
        mock_connect.assert_called_once()

    @patch("src.db.connection.pyodbc.connect")
    def test_retry_on_failure(self, mock_connect):
        """測試重試機制。"""
        # 前兩次失敗，第三次成功
        mock_connect.side_effect = [
            pyodbc.Error("Connection failed"),
            pyodbc.Error("Connection failed"),
            MagicMock(),
        ]

        conn = get_connection(max_retries=3, retry_delay=0.1)

        assert conn is not None
        assert mock_connect.call_count == 3

    @patch("src.db.connection.pyodbc.connect")
    def test_max_retries_exceeded(self, mock_connect):
        """測試超過最大重試次數拋出例外。"""
        mock_connect.side_effect = pyodbc.Error("Connection failed")

        with pytest.raises(ConnectionError) as exc_info:
            get_connection(max_retries=2, retry_delay=0.1)

        assert "無法連線至資料庫" in str(exc_info.value)
        assert mock_connect.call_count == 2


class TestTestConnection:
    """測試 test_connection 函式。"""

    @patch("src.db.connection.get_connection")
    def test_connection_success(self, mock_get_connection):
        """測試連線測試成功。"""
        mock_conn = MagicMock()
        mock_get_connection.return_value = mock_conn

        result = test_connection()

        assert result is True
        mock_conn.close.assert_called_once()

    @patch("src.db.connection.get_connection")
    def test_connection_failure(self, mock_get_connection):
        """測試連線測試失敗。"""
        mock_get_connection.side_effect = ConnectionError("Connection failed")

        result = test_connection()

        assert result is False
