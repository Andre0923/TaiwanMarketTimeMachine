# @spec US-A1 (001-basic-chart-api/spec.md#user-story-a-1)
"""
MSSQL Database Connection Module.

此模組負責管理與 MSSQL 資料庫的連線，支援連線池與錯誤處理。
使用 pyodbc 連接至 [股價即時].[dbo].[1分K] 資料來源。

功能:
- 從 .env 讀取資料庫配置
- 提供連線取得函式
- 連線錯誤處理與重試機制
"""

import os
import pyodbc
from typing import Optional
from dotenv import load_dotenv
from src.logger import setup_logger

# 載入環境變數
load_dotenv()

logger = setup_logger(__name__)


class DatabaseConfig:
    """資料庫配置類別，從環境變數載入設定。"""

    def __init__(self):
        self.server = os.getenv("DB_SERVER", "localhost")
        self.port = os.getenv("DB_PORT", "1433")
        self.database = os.getenv("DB_DATABASE", "")
        self.username = os.getenv("DB_USERNAME", "")
        self.password = os.getenv("DB_PASSWORD", "")
        self.driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")

    def get_connection_string(self) -> str:
        """
        建立 ODBC 連線字串。

        Returns:
            str: ODBC 連線字串
        """
        return (
            f"DRIVER={{{self.driver}}};"
            f"SERVER={self.server},{self.port};"
            f"DATABASE={self.database};"
            f"UID={self.username};"
            f"PWD={self.password};"
            f"TrustServerCertificate=yes;"
        )


def get_connection(max_retries: int = 3, retry_delay: float = 1.0) -> pyodbc.Connection:
    """
    取得資料庫連線，支援重試機制。

    Args:
        max_retries: 最大重試次數（預設 3 次）
        retry_delay: 重試間隔秒數（預設 1 秒）

    Returns:
        pyodbc.Connection: 資料庫連線物件

    Raises:
        ConnectionError: 當所有重試都失敗時拋出此例外

    Example:
        >>> conn = get_connection()
        >>> cursor = conn.cursor()
        >>> cursor.execute("SELECT TOP 5 * FROM [股價即時].[dbo].[1分K]")
        >>> rows = cursor.fetchall()
        >>> conn.close()
    """
    config = DatabaseConfig()
    connection_string = config.get_connection_string()

    last_error: Optional[Exception] = None

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(
                f"嘗試連線至資料庫... (嘗試 {attempt}/{max_retries})",
                extra={"server": config.server, "database": config.database},
            )

            conn = pyodbc.connect(connection_string, timeout=10)

            logger.info(
                "資料庫連線成功",
                extra={"server": config.server, "database": config.database},
            )

            return conn

        except pyodbc.Error as e:
            last_error = e
            logger.warning(
                f"資料庫連線失敗 (嘗試 {attempt}/{max_retries}): {str(e)}",
                extra={"server": config.server, "attempt": attempt},
            )

            if attempt < max_retries:
                import time

                time.sleep(retry_delay)
            else:
                logger.error(
                    f"資料庫連線失敗，已達最大重試次數 ({max_retries})",
                    extra={"server": config.server, "error": str(e)},
                    exc_info=True,
                )

    # 所有重試都失敗
    raise ConnectionError(
        f"無法連線至資料庫 {config.server}:{config.port}/{config.database}。"
        f"已重試 {max_retries} 次。最後錯誤: {str(last_error)}"
    )


def test_connection() -> bool:
    """
    測試資料庫連線是否正常。

    Returns:
        bool: 連線成功回傳 True，失敗回傳 False
    """
    try:
        conn = get_connection(max_retries=1)
        conn.close()
        return True
    except ConnectionError:
        return False
