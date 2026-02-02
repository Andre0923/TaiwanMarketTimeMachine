"""
日誌設定模組
============

本模組提供統一的日誌設定，符合專案憲章 3.7 節的要求：
- 日誌檔案固定放在專案根目錄下的 logs/ 資料夾
- 檔名格式：YYYYMMDD_HHMMSS.log
- 同時輸出到終端機與檔案
- 支援不同日誌等級
- 所有 logger 共用同一個日誌檔案

使用方式:
--------
from src.logger import setup_logger

logger = setup_logger(__name__)
logger.info("程式開始執行")
logger.debug("除錯訊息")
logger.error("錯誤訊息")

日誌等級指南:
-----------
- DEBUG: 詳細除錯資訊（變數值、計算過程）
- INFO: 一般流程資訊（函式開始/結束、成功訊息）
- WARNING: 警告訊息（不影響執行，但需注意）
- ERROR: 錯誤訊息（影響功能）
- CRITICAL: 嚴重錯誤（系統無法繼續）
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


# 模組級別的 logger 實例快取
_loggers: dict[str, logging.Logger] = {}
_log_file: Optional[Path] = None


def get_project_root() -> Path:
    """
    取得專案根目錄
    
    Returns:
        Path: 專案根目錄路徑
    """
    # 從 src/logger.py 往上兩層即為專案根目錄
    return Path(__file__).parent.parent


def setup_logger(
    name: str = __name__,
    log_level: int = logging.DEBUG
) -> logging.Logger:
    """
    設定日誌系統
    
    符合憲章 3.7 節要求：
    - 所有日誌寫入專案根目錄下的 logs/ 資料夾
    - 檔名格式：YYYYMMDD_HHMMSS.log
    - 所有 logger 共用同一個日誌檔案
    - 同時輸出到終端機與檔案
    
    Args:
        name: Logger 名稱，通常使用 __name__
        log_level: 日誌等級 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        logging.Logger: 設定完成的 logger 物件
    
    範例:
        >>> logger = setup_logger(__name__)
        >>> logger.info("這是一般訊息")
        >>> logger.error("這是錯誤訊息")
    
    注意:
        所有呼叫 setup_logger() 的 logger 會共用同一個日誌檔案，
        檔案位置在第一次呼叫時決定，後續呼叫會沿用相同檔案。
    """
    global _log_file
    
    # 如果已經建立過，直接返回
    if name in _loggers:
        return _loggers[name]
    
    # 固定使用專案根目錄下的 logs/ 資料夾（符合憲章 3.7）
    log_path = get_project_root() / "logs"
    
    # 確保 logs 資料夾存在
    log_path.mkdir(exist_ok=True)
    
    # 以執行時間命名日誌檔 (YYYYMMDD_HHMMSS.log)
    # 使用共享的日誌檔案，所有 logger 寫入同一個檔案
    if _log_file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        _log_file = log_path / f"{timestamp}.log"
    
    # 建立 logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # 避免重複加入 handler
    if logger.handlers:
        _loggers[name] = logger
        return logger
    
    # 檔案 handler - 記錄所有等級
    file_handler = logging.FileHandler(_log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    
    # Console handler - 只輸出 INFO 以上
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # 格式設定
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # 加入 handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # 快取 logger
    _loggers[name] = logger
    
    return logger


def get_current_log_file() -> Optional[Path]:
    """
    取得當前日誌檔案路徑
    
    Returns:
        Optional[Path]: 日誌檔案路徑，若尚未初始化則為 None
    """
    return _log_file


def log_execution_context(logger: logging.Logger, **kwargs) -> None:
    """
    記錄執行環境資訊
    
    Args:
        logger: Logger 物件
        **kwargs: 要記錄的鍵值對
    
    範例:
        >>> logger = setup_logger()
        >>> log_execution_context(
        ...     logger,
        ...     python_version="3.13.0",
        ...     user="Victor",
        ...     project="speckit-template"
        ... )
    """
    logger.info("=" * 50)
    logger.info("執行環境資訊")
    for key, value in kwargs.items():
        logger.info(f"  {key}: {value}")
    logger.info("=" * 50)


# 使用範例
if __name__ == "__main__":
    # 設定 logger
    logger = setup_logger(__name__)
    
    # 記錄程式啟動
    logger.info("=" * 50)
    logger.info("Logger 模組測試")
    logger.info(f"執行時間: {datetime.now()}")
    logger.info(f"日誌檔案: {get_current_log_file()}")
    logger.info("=" * 50)
    
    # 記錄執行環境
    import sys
    log_execution_context(
        logger,
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        platform=sys.platform,
        script=__file__
    )
    
    # 不同等級的日誌範例
    logger.debug("這是除錯訊息（詳細資訊）")
    logger.info("這是一般訊息（流程進度）")
    logger.warning("這是警告訊息（可能的問題）")
    logger.error("這是錯誤訊息（需要關注）")
    logger.critical("這是嚴重錯誤（系統無法繼續）")
    
    logger.info("=" * 50)
    logger.info("Logger 模組測試完成")
    logger.info("=" * 50)
