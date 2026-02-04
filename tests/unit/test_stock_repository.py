"""
Unit tests for StockRepository.

測試 Repository 層的資料庫查詢邏輯（使用 Mock）。
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import pyodbc
from src.db.stock_repository import StockRepository


class TestStockRepository:
    """測試 StockRepository 類別。"""

    def test_init_without_connection(self):
        """測試無連線初始化。"""
        repo = StockRepository()
        assert repo._connection is None

    def test_init_with_connection(self):
        """測試有連線初始化。"""
        mock_conn = Mock(spec=pyodbc.Connection)
        repo = StockRepository(connection=mock_conn)
        assert repo._connection is mock_conn


class TestGetOneMinuteKlines:
    """測試 get_one_minute_klines 方法。"""

    @patch('src.db.stock_repository.get_connection')
    def test_successful_query(self, mock_get_conn):
        """測試成功查詢資料。"""
        # Mock connection and cursor
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = [
            (
                datetime(2024, 1, 15, 9, 0),  # 日期
                datetime(1900, 1, 1, 9, 1),   # 時間
                "2330",                        # 股票代號
                580.0,                         # 開盤價
                585.0,                         # 最高價
                578.0,                         # 最低價
                583.0,                         # 收盤價
                12345678.0                     # 成交量
            )
        ]
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        # Execute
        repo = StockRepository()
        result = repo.get_one_minute_klines("2330", "2024-01-15", "2024-01-15")

        # Verify
        assert len(result) == 1
        assert result[0][2] == "2330"  # 股票代號
        mock_cursor.execute.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch('src.db.stock_repository.get_connection')
    def test_empty_result(self, mock_get_conn):
        """測試查無資料。"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        repo = StockRepository()
        result = repo.get_one_minute_klines("9999", "2024-01-15", "2024-01-15")

        assert len(result) == 0
        mock_conn.close.assert_called_once()

    def test_invalid_date_format(self):
        """測試無效的日期格式。"""
        repo = StockRepository()
        with pytest.raises(ValueError) as exc_info:
            repo.get_one_minute_klines("2330", "2024/01/15", "2024-01-15")
        assert "日期格式必須為 YYYY-MM-DD" in str(exc_info.value)

    @patch('src.db.stock_repository.get_connection')
    def test_database_error(self, mock_get_conn):
        """測試資料庫錯誤。"""
        mock_get_conn.side_effect = pyodbc.Error("Database connection failed")

        repo = StockRepository()
        with pytest.raises(pyodbc.Error):
            repo.get_one_minute_klines("2330", "2024-01-15", "2024-01-15")

    def test_with_injected_connection(self):
        """測試使用注入的連線（不應該關閉連線）。"""
        mock_cursor = Mock()
        mock_cursor.fetchall.return_value = []
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor

        repo = StockRepository(connection=mock_conn)
        result = repo.get_one_minute_klines("2330", "2024-01-15", "2024-01-15")

        assert len(result) == 0
        mock_conn.close.assert_not_called()  # 不應該關閉注入的連線


class TestCheckStockExists:
    """測試 check_stock_exists 方法。"""

    @patch('src.db.stock_repository.get_connection')
    def test_stock_exists(self, mock_get_conn):
        """測試股票存在。"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1,)
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        repo = StockRepository()
        result = repo.check_stock_exists("2330")

        assert result is True
        mock_conn.close.assert_called_once()

    @patch('src.db.stock_repository.get_connection')
    def test_stock_not_exists(self, mock_get_conn):
        """測試股票不存在。"""
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = None
        mock_conn = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_get_conn.return_value = mock_conn

        repo = StockRepository()
        result = repo.check_stock_exists("9999")

        assert result is False
        mock_conn.close.assert_called_once()

    @patch('src.db.stock_repository.get_connection')
    def test_database_error(self, mock_get_conn):
        """測試資料庫錯誤時回傳 False。"""
        mock_get_conn.side_effect = pyodbc.Error("Database connection failed")

        repo = StockRepository()
        result = repo.check_stock_exists("2330")

        assert result is False
