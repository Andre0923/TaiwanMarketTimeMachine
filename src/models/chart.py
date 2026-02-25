# @spec US-A1 (001-basic-chart-api/spec.md#user-story-a-1)
# @spec-ac AC1, AC2, AC3
# @spec US-G2 (001-basic-chart-api/spec.md#user-story-g-2)
# @spec-ac AC1, AC2, AC3
"""
Chart Data Models.

定義圖表資料的 Pydantic 模型，用於 API Request/Response 與資料驗證。
符合 US G-2 的 API 固定格式設計原則。
"""

from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class ChartDataPoint(BaseModel):
    """
    單一日K線資料點。
    
    Attributes:
        time: 交易日期（YYYY-MM-DD 格式）
        open: 開盤價
        high: 最高價
        low: 最低價
        close: 收盤價
        volume: 成交量
    """
    time: str = Field(..., description="交易日期（YYYY-MM-DD）", examples=["2024-01-15"])
    open: float = Field(..., gt=0, description="開盤價", examples=[580.0])
    high: float = Field(..., gt=0, description="最高價", examples=[585.0])
    low: float = Field(..., gt=0, description="最低價", examples=[578.0])
    close: float = Field(..., gt=0, description="收盤價", examples=[583.0])
    volume: float = Field(..., ge=0, description="成交量", examples=[12345678.0])

    @field_validator("time")
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        """驗證日期格式為 YYYY-MM-DD。"""
        try:
            # 嘗試解析日期
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("日期格式必須為 YYYY-MM-DD")

    @field_validator("high")
    @classmethod
    def validate_high(cls, v: float, info) -> float:
        """驗證最高價 >= 其他價格。"""
        # 注意：此驗證在 model_validator 中會更完整
        return v

    @field_validator("low")
    @classmethod
    def validate_low(cls, v: float, info) -> float:
        """驗證最低價 <= 其他價格。"""
        return v


class ChartRequest(BaseModel):
    """
    圖表資料查詢請求。
    
    Attributes:
        stock_code: 股票代碼（如 "2330"）
        start_date: 起始日期（YYYY-MM-DD）
        end_date: 結束日期（YYYY-MM-DD）
    """
    stock_code: str = Field(
        ...,
        min_length=4,
        max_length=10,
        description="股票代碼",
        examples=["2330", "1101"]
    )
    start_date: str = Field(..., description="起始日期（YYYY-MM-DD）", examples=["2024-01-01"])
    end_date: str = Field(..., description="結束日期（YYYY-MM-DD）", examples=["2024-01-31"])

    @field_validator("start_date", "end_date")
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """驗證日期格式。"""
        try:
            date.fromisoformat(v)
            return v
        except ValueError:
            raise ValueError("日期格式必須為 YYYY-MM-DD")


class ChartMetadata(BaseModel):
    """
    圖表資料的 metadata。
    
    Attributes:
        stock_code: 股票代碼
        start_date: 實際資料起始日期
        end_date: 實際資料結束日期
        data_points: 資料點數量
    """
    stock_code: str = Field(..., description="股票代碼")
    start_date: str = Field(..., description="資料起始日期")
    end_date: str = Field(..., description="資料結束日期")
    data_points: int = Field(..., ge=0, description="資料點數量")


class ChartResponse(BaseModel):
    """
    圖表資料回應（符合 US G-2 AC1, AC2 固定格式）。
    
    Attributes:
        stock_code: 股票代碼
        chart_data: K線資料陣列
        metadata: 資料 metadata（可擴充欄位，符合 US G-2 AC2）
    """
    stock_code: str = Field(..., description="股票代碼")
    chart_data: List[ChartDataPoint] = Field(..., description="K線資料陣列")
    metadata: Optional[ChartMetadata] = Field(None, description="資料 metadata")


class ErrorDetail(BaseModel):
    """
    錯誤詳細資訊。
    
    Attributes:
        code: 錯誤碼（如 INVALID_STOCK_CODE）
        message: 錯誤訊息
        details: 詳細說明（選填）
    """
    code: str = Field(..., description="錯誤碼")
    message: str = Field(..., description="錯誤訊息")
    details: Optional[str] = Field(None, description="詳細說明")


class ErrorResponse(BaseModel):
    """
    錯誤回應（符合 US G-2 AC3 統一錯誤格式）。
    
    Attributes:
        error: 錯誤詳細資訊
    """
    error: ErrorDetail = Field(..., description="錯誤詳細資訊")


# 常用錯誤碼定義
class ErrorCodes:
    """錯誤碼常數定義。"""
    INVALID_STOCK_CODE = "INVALID_STOCK_CODE"
    INVALID_DATE_RANGE = "INVALID_DATE_RANGE"
    NO_DATA = "NO_DATA"
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"
