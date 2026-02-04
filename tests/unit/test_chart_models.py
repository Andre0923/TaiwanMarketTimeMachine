"""
Unit tests for chart models.

測試 Pydantic 模型的驗證邏輯和資料結構。
"""

import pytest
from pydantic import ValidationError
from src.models.chart import (
    ChartDataPoint,
    ChartRequest,
    ChartResponse,
    ChartMetadata,
    ErrorResponse,
    ErrorDetail,
    ErrorCodes
)


class TestChartDataPoint:
    """測試 ChartDataPoint 模型。"""

    def test_valid_data_point(self):
        """測試有效的資料點。"""
        data = ChartDataPoint(
            time="2024-01-15",
            open=580.0,
            high=585.0,
            low=578.0,
            close=583.0,
            volume=12345678.0
        )
        assert data.time == "2024-01-15"
        assert data.open == 580.0
        assert data.high == 585.0
        assert data.low == 578.0
        assert data.close == 583.0
        assert data.volume == 12345678.0

    def test_invalid_date_format(self):
        """測試無效的日期格式。"""
        with pytest.raises(ValidationError) as exc_info:
            ChartDataPoint(
                time="15-01-2024",  # 錯誤格式
                open=580.0,
                high=585.0,
                low=578.0,
                close=583.0,
                volume=12345678.0
            )
        assert "日期格式必須為 YYYY-MM-DD" in str(exc_info.value)

    def test_negative_price(self):
        """測試負數價格（應該失敗）。"""
        with pytest.raises(ValidationError):
            ChartDataPoint(
                time="2024-01-15",
                open=-580.0,  # 負數
                high=585.0,
                low=578.0,
                close=583.0,
                volume=12345678.0
            )

    def test_negative_volume(self):
        """測試負數成交量（應該失敗）。"""
        with pytest.raises(ValidationError):
            ChartDataPoint(
                time="2024-01-15",
                open=580.0,
                high=585.0,
                low=578.0,
                close=583.0,
                volume=-100.0  # 負數
            )

    def test_zero_volume(self):
        """測試零成交量（應該允許）。"""
        data = ChartDataPoint(
            time="2024-01-15",
            open=580.0,
            high=585.0,
            low=578.0,
            close=583.0,
            volume=0.0
        )
        assert data.volume == 0.0


class TestChartRequest:
    """測試 ChartRequest 模型。"""

    def test_valid_request(self):
        """測試有效的請求。"""
        req = ChartRequest(
            stock_code="2330",
            start_date="2024-01-01",
            end_date="2024-01-31"
        )
        assert req.stock_code == "2330"
        assert req.start_date == "2024-01-01"
        assert req.end_date == "2024-01-31"

    def test_invalid_date_format(self):
        """測試無效的日期格式。"""
        with pytest.raises(ValidationError) as exc_info:
            ChartRequest(
                stock_code="2330",
                start_date="2024/01/01",  # 錯誤格式
                end_date="2024-01-31"
            )
        assert "日期格式必須為 YYYY-MM-DD" in str(exc_info.value)

    def test_stock_code_too_short(self):
        """測試股票代碼太短。"""
        with pytest.raises(ValidationError):
            ChartRequest(
                stock_code="123",  # 少於 4 碼
                start_date="2024-01-01",
                end_date="2024-01-31"
            )

    def test_stock_code_too_long(self):
        """測試股票代碼太長。"""
        with pytest.raises(ValidationError):
            ChartRequest(
                stock_code="12345678901",  # 超過 10 碼
                start_date="2024-01-01",
                end_date="2024-01-31"
            )


class TestChartResponse:
    """測試 ChartResponse 模型。"""

    def test_valid_response(self):
        """測試有效的回應。"""
        data_points = [
            ChartDataPoint(
                time="2024-01-15",
                open=580.0,
                high=585.0,
                low=578.0,
                close=583.0,
                volume=12345678.0
            )
        ]
        metadata = ChartMetadata(
            stock_code="2330",
            start_date="2024-01-15",
            end_date="2024-01-15",
            data_points=1
        )
        resp = ChartResponse(
            stock_code="2330",
            chart_data=data_points,
            metadata=metadata
        )
        assert resp.stock_code == "2330"
        assert len(resp.chart_data) == 1
        assert resp.metadata.data_points == 1

    def test_empty_data(self):
        """測試空資料回應。"""
        resp = ChartResponse(
            stock_code="2330",
            chart_data=[],
            metadata=None
        )
        assert resp.stock_code == "2330"
        assert len(resp.chart_data) == 0
        assert resp.metadata is None


class TestErrorResponse:
    """測試 ErrorResponse 模型。"""

    def test_valid_error(self):
        """測試有效的錯誤回應。"""
        error = ErrorResponse(
            error=ErrorDetail(
                code=ErrorCodes.NO_DATA,
                message="查無資料",
                details="指定日期範圍內無任何資料"
            )
        )
        assert error.error.code == ErrorCodes.NO_DATA
        assert error.error.message == "查無資料"
        assert error.error.details == "指定日期範圍內無任何資料"

    def test_error_without_details(self):
        """測試無詳細說明的錯誤。"""
        error = ErrorResponse(
            error=ErrorDetail(
                code=ErrorCodes.DATABASE_ERROR,
                message="資料庫錯誤"
            )
        )
        assert error.error.code == ErrorCodes.DATABASE_ERROR
        assert error.error.message == "資料庫錯誤"
        assert error.error.details is None


class TestErrorCodes:
    """測試錯誤碼定義。"""

    def test_error_codes_exist(self):
        """測試錯誤碼常數存在。"""
        assert ErrorCodes.INVALID_STOCK_CODE == "INVALID_STOCK_CODE"
        assert ErrorCodes.INVALID_DATE_RANGE == "INVALID_DATE_RANGE"
        assert ErrorCodes.NO_DATA == "NO_DATA"
        assert ErrorCodes.DATABASE_ERROR == "DATABASE_ERROR"
        assert ErrorCodes.INTERNAL_ERROR == "INTERNAL_ERROR"
