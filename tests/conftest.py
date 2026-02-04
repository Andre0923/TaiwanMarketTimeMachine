"""
Pytest configuration and shared fixtures.

此檔案自動載入，提供測試共用的設定與 fixtures。
"""

import sys
from pathlib import Path

# 將專案根目錄加入 Python 路徑
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
