"""
Integration tests for Chart API.

測試 US A-1 的 Acceptance Criteria 與 API 整合。
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from datetime import datetime
from src.main import app
from src.models.chart import ErrorCodes

client = TestClient(app)


class TestChartAPIIntegration:
    """整合測試：Chart API 端點。"""

    @patch('src.api.routes.chart.ChartService')
    def test_ac1_kline_data_returned(self, mock_service_class):
        """
        AC1: K線資料正確回傳。
        
        Given: 有效的股票代碼與日期範圍
        When: 呼叫 GET /api/chart/daily
        Then: 回傳日K資料（含 open, high, low, close）
        """
        # Mock Service 回應
        mock_service = Mock()
        mock_service.get_daily_chart.return_value = Mock(
            stock_code="2330",
            chart_data=[
                Mock(
                    time="2024-01-15",
                    open=580.0,
                    high=585.0,
                    low=578.0,
                    close=583.0,
                    volume=12345678.0
                )
            ],
            metadata=Mock(
                stock_code="2330",
                start_date="2024-01-15",
                end_date="2024-01-15",
                data_points=1
            )
        )
        mock_service_class.return_value = mock_service

        # Execute
        response = client.get(
            "/api/chart/daily",
            params={
                "stock_code": "2330",
                "start_date": "2024-01-15",
                "end_date": "2024-01-15"
            }
        )

        # Verify
        assert response.status_code == 200
        data = response.json()
        assert data["stock_code"] == "2330"
        assert len(data["chart_data"]) == 1
        assert data["chart_data"][0]["open"] == 580.0
        assert data["chart_data"][0]["high"] == 585.0
        assert data["chart_data"][0]["low"] == 578.0
        assert data["chart_data"][0]["close"] == 583.0

    @patch('src.api.routes.chart.ChartService')
    def test_ac2_volume_aligned_with_dates(self, mock_service_class):
        """
        AC2: 成交量資料與日期對齊。
        
        Given: 多日資料
        When: 呼叫 GET /api/chart/daily
        Then: 每個資料點的成交量與對應日期正確對齊
        """
        mock_service = Mock()
        mock_service.get_daily_chart.return_value = Mock(
            stock_code="2330",
            chart_data=[
                Mock(time="2024-01-15", open=580.0, high=585.0, low=578.0, close=583.0, volume=1000000.0),
                Mock(time="2024-01-16", open=583.0, high=590.0, low=582.0, close=588.0, volume=2000000.0),
            ],
            metadata=Mock(stock_code="2330", start_date="2024-01-15", end_date="2024-01-16", data_points=2)
        )
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024-01-15", "end_date": "2024-01-16"}
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data["chart_data"]) == 2
        
        # 驗證日期與成交量對齊
        assert data["chart_data"][0]["time"] == "2024-01-15"
        assert data["chart_data"][0]["volume"] == 1000000.0
        assert data["chart_data"][1]["time"] == "2024-01-16"
        assert data["chart_data"][1]["volume"] == 2000000.0

    @patch('src.api.routes.chart.ChartService')
    def test_ac3_no_data_handling(self, mock_service_class):
        """
        AC3: 無資料時的適當回應。
        
        Given: 不存在的股票或日期範圍無資料
        When: 呼叫 GET /api/chart/daily
        Then: 回傳空陣列或適當錯誤訊息
        """
        mock_service = Mock()
        mock_service.get_daily_chart.return_value = Mock(
            stock_code="9999",
            chart_data=[],  # 空資料
            metadata=Mock(stock_code="9999", start_date="2024-01-15", end_date="2024-01-15", data_points=0)
        )
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "9999", "start_date": "2024-01-15", "end_date": "2024-01-15"}
        )

        # 此處設計為 200 + 空陣列（前端可自行處理）
        # 若需要 404 回應，可在 Router 調整邏輯
        assert response.status_code == 200
        data = response.json()
        assert data["stock_code"] == "9999"
        assert len(data["chart_data"]) == 0
        assert data["metadata"]["data_points"] == 0

    def test_invalid_stock_code_format(self):
        """測試無效的股票代碼格式。"""
        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "12", "start_date": "2024-01-15", "end_date": "2024-01-15"}
        )
        assert response.status_code == 422  # FastAPI 驗證錯誤

    def test_invalid_date_format(self):
        """測試無效的日期格式。"""
        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024/01/15", "end_date": "2024-01-15"}
        )
        assert response.status_code == 422  # FastAPI 驗證錯誤

    @patch('src.api.routes.chart.ChartService')
    def test_invalid_date_range(self, mock_service_class):
        """測試無效的日期範圍（起始日期 > 結束日期）。"""
        mock_service = Mock()
        mock_service.get_daily_chart.side_effect = ValueError("起始日期不得大於結束日期")
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024-01-31", "end_date": "2024-01-01"}
        )

        assert response.status_code == 400
        data = response.json()
        assert "error" in data["detail"]
        assert data["detail"]["error"]["code"] == ErrorCodes.INVALID_DATE_RANGE

    @patch('src.api.routes.chart.ChartService')
    def test_internal_server_error(self, mock_service_class):
        """測試伺服器內部錯誤處理。"""
        mock_service = Mock()
        mock_service.get_daily_chart.side_effect = Exception("Unexpected error")
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024-01-15", "end_date": "2024-01-15"}
        )

        assert response.status_code == 500
        data = response.json()
        assert "error" in data["detail"]
        assert data["detail"]["error"]["code"] == ErrorCodes.INTERNAL_ERROR


class TestAPIResponseFormat:
    """測試 API 回應格式（US G-2）。"""

    @patch('src.api.routes.chart.ChartService')
    def test_response_format_compliance(self, mock_service_class):
        """
        US G-2 AC1: API 回應固定格式。
        
        驗證回應包含：stock_code, chart_data, metadata
        """
        mock_service = Mock()
        mock_service.get_daily_chart.return_value = Mock(
            stock_code="2330",
            chart_data=[Mock(time="2024-01-15", open=580.0, high=585.0, low=578.0, close=583.0, volume=1000.0)],
            metadata=Mock(stock_code="2330", start_date="2024-01-15", end_date="2024-01-15", data_points=1)
        )
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024-01-15", "end_date": "2024-01-15"}
        )

        assert response.status_code == 200
        data = response.json()
        
        # 驗證固定格式欄位存在
        assert "stock_code" in data
        assert "chart_data" in data
        assert "metadata" in data
        
        # 驗證 chart_data 結構
        assert isinstance(data["chart_data"], list)
        if data["chart_data"]:
            point = data["chart_data"][0]
            assert "time" in point
            assert "open" in point
            assert "high" in point
            assert "low" in point
            assert "close" in point
            assert "volume" in point

    @patch('src.api.routes.chart.ChartService')
    def test_error_format_compliance(self, mock_service_class):
        """
        US G-2 AC3: 錯誤回應統一格式。
        
        驗證錯誤回應包含：error.code, error.message, error.details
        """
        mock_service = Mock()
        mock_service.get_daily_chart.side_effect = ValueError("日期格式錯誤")
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024-01-31", "end_date": "2024-01-01"}
        )

        assert response.status_code == 400
        data = response.json()
        
        # 驗證錯誤格式
        assert "detail" in data
        assert "error" in data["detail"]
        error = data["detail"]["error"]
        assert "code" in error
        assert "message" in error
        # details 為選填
