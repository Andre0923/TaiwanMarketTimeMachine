# @spec US-A1 (001-basic-chart-api/spec.md#user-story-a-1)
# @spec-ac AC1, AC2, AC3
"""
Stock Repository Layer.

負責從資料庫查詢股票 1分K 資料的 Repository 層。
使用參數化查詢防止 SQL Injection，支援連線錯誤重試機制。
"""

from typing import List, Tuple, Optional
from datetime import datetime
import pyodbc
from src.db.connection import get_connection
from src.logger import setup_logger

logger = setup_logger(__name__)


class StockRepository:
    """
    股票資料 Repository，負責資料庫查詢操作。
    
    查詢來源：[股價即時].[dbo].[1分K]
    """

    def __init__(self, connection: Optional[pyodbc.Connection] = None):
        """
        初始化 Repository。
        
        Args:
            connection: 資料庫連線（選填，若無則自動建立）
        """
        self._connection = connection

    def _get_connection(self) -> pyodbc.Connection:
        """取得資料庫連線（支援 Dependency Injection）。"""
        if self._connection is None:
            return get_connection()
        return self._connection

    def get_one_minute_klines(
        self,
        stock_code: str,
        start_date: str,
        end_date: str
    ) -> List[Tuple]:
        """
        查詢指定股票的 1分K 資料。
        
        Args:
            stock_code: 股票代碼（如 "2330"）
            start_date: 起始日期（YYYY-MM-DD）
            end_date: 結束日期（YYYY-MM-DD）
        
        Returns:
            List[Tuple]: 查詢結果列表，每筆包含 (日期, 時間, 股票代號, 開盤價, 最高價, 最低價, 收盤價, 成交量)
        
        Raises:
            ValueError: 日期格式錯誤
            pyodbc.Error: 資料庫查詢錯誤
        
        Example:
            >>> repo = StockRepository()
            >>> data = repo.get_one_minute_klines("2330", "2024-01-01", "2024-01-31")
            >>> len(data)
            > 0
        """
        logger.info(
            f"查詢 1分K 資料: {stock_code}, {start_date} ~ {end_date}",
            extra={"stock_code": stock_code, "start_date": start_date, "end_date": end_date}
        )

        # 驗證日期格式
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError as e:
            logger.error(f"日期格式錯誤: {e}")
            raise ValueError(f"日期格式必須為 YYYY-MM-DD: {e}")

        # 使用參數化查詢防止 SQL Injection
        query = """
        SELECT 
            [日期],
            [時間],
            [股票代號],
            [開盤價],
            [最高價],
            [最低價],
            [收盤價],
            [成交量]
        FROM [股價即時].[dbo].[1分K]
        WHERE [股票代號] = ?
          AND [日期] >= ?
          AND [日期] <= ?
        ORDER BY [日期] ASC, [時間] ASC
        """

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            logger.debug(
                f"執行 SQL 查詢",
                extra={"query": query, "params": (stock_code, start_date, end_date)}
            )

            cursor.execute(query, (stock_code, start_date, end_date))
            rows = cursor.fetchall()

            logger.info(
                f"查詢完成，取得 {len(rows)} 筆資料",
                extra={"stock_code": stock_code, "row_count": len(rows)}
            )

            # 只有當連線是自己建立時才關閉
            if self._connection is None:
                conn.close()

            return rows

        except pyodbc.Error as e:
            logger.error(
                f"資料庫查詢錯誤: {str(e)}",
                extra={"stock_code": stock_code, "error": str(e)},
                exc_info=True
            )
            raise

    def check_stock_exists(self, stock_code: str) -> bool:
        """
        檢查股票代碼是否存在於資料庫。
        
        Args:
            stock_code: 股票代碼
        
        Returns:
            bool: 存在回傳 True，否則 False
        """
        query = """
        SELECT TOP 1 1
        FROM [股價即時].[dbo].[1分K]
        WHERE [股票代號] = ?
        """

        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (stock_code,))
            result = cursor.fetchone()

            if self._connection is None:
                conn.close()

            return result is not None

        except pyodbc.Error as e:
            logger.error(f"檢查股票代碼錯誤: {str(e)}", exc_info=True)
            return False
