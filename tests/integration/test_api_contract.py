"""
API Contract Tests.

驗證 API 契約符合 US G-2 規範：
- AC1: Response 必要欄位存在且類型正確
- AC3: 錯誤格式一致性
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from src.main import app
from src.models.chart import ErrorCodes

client = TestClient(app)


class TestResponseSchemaCompliance:
    """測試 Response Schema 符合契約（US G-2 AC1）。"""

    @patch('src.api.routes.chart.ChartService')
    def test_success_response_required_fields(self, mock_service_class):
        """
        驗證成功回應包含所有必要欄位。
        
        US G-2 AC1: Response 固定格式
        - stock_code (string)
        - chart_data (array)
        - metadata (object, nullable)
        """
        mock_service = Mock()
        mock_service.get_daily_chart.return_value = Mock(
            stock_code="2330",
            chart_data=[
                Mock(time="2024-01-15", open=580.0, high=585.0, low=578.0, close=583.0, volume=1000.0)
            ],
            metadata=Mock(stock_code="2330", start_date="2024-01-15", end_date="2024-01-15", data_points=1)
        )
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024-01-15", "end_date": "2024-01-15"}
        )

        assert response.status_code == 200
        data = response.json()

        # 驗證頂層必要欄位
        assert "stock_code" in data, "缺少必要欄位: stock_code"
        assert "chart_data" in data, "缺少必要欄位: chart_data"
        assert "metadata" in data, "缺少必要欄位: metadata"

        # 驗證類型
        assert isinstance(data["stock_code"], str)
        assert isinstance(data["chart_data"], list)
        assert data["metadata"] is None or isinstance(data["metadata"], dict)

    @patch('src.api.routes.chart.ChartService')
    def test_chart_data_point_schema(self, mock_service_class):
        """
        驗證 ChartDataPoint 結構符合契約。
        
        必要欄位: time, open, high, low, close, volume
        """
        mock_service = Mock()
        mock_service.get_daily_chart.return_value = Mock(
            stock_code="2330",
            chart_data=[
                Mock(time="2024-01-15", open=580.0, high=585.0, low=578.0, close=583.0, volume=1000.0)
            ],
            metadata=Mock(stock_code="2330", start_date="2024-01-15", end_date="2024-01-15", data_points=1)
        )
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024-01-15", "end_date": "2024-01-15"}
        )

        data = response.json()
        assert len(data["chart_data"]) > 0

        point = data["chart_data"][0]
        required_fields = ["time", "open", "high", "low", "close", "volume"]
        for field in required_fields:
            assert field in point, f"ChartDataPoint 缺少必要欄位: {field}"

        # 驗證類型
        assert isinstance(point["time"], str)
        assert isinstance(point["open"], (int, float))
        assert isinstance(point["high"], (int, float))
        assert isinstance(point["low"], (int, float))
        assert isinstance(point["close"], (int, float))
        assert isinstance(point["volume"], (int, float))

        # 驗證數值範圍
        assert point["open"] > 0, "open 必須 > 0"
        assert point["high"] > 0, "high 必須 > 0"
        assert point["low"] > 0, "low 必須 > 0"
        assert point["close"] > 0, "close 必須 > 0"
        assert point["volume"] >= 0, "volume 必須 >= 0"

    @patch('src.api.routes.chart.ChartService')
    def test_metadata_schema(self, mock_service_class):
        """
        驗證 metadata 結構符合契約。
        
        metadata 欄位: stock_code, start_date, end_date, data_points
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

        data = response.json()
        assert data["metadata"] is not None

        metadata = data["metadata"]
        required_fields = ["stock_code", "start_date", "end_date", "data_points"]
        for field in required_fields:
            assert field in metadata, f"metadata 缺少必要欄位: {field}"

        # 驗證類型
        assert isinstance(metadata["stock_code"], str)
        assert isinstance(metadata["start_date"], str)
        assert isinstance(metadata["end_date"], str)
        assert isinstance(metadata["data_points"], int)
        assert metadata["data_points"] >= 0

    @patch('src.api.routes.chart.ChartService')
    def test_empty_data_response(self, mock_service_class):
        """
        驗證無資料時的回應結構（US A-1 AC3）。
        
        應回傳空陣列但保留完整結構。
        """
        mock_service = Mock()
        mock_service.get_daily_chart.return_value = Mock(
            stock_code="9999",
            chart_data=[],
            metadata=Mock(stock_code="9999", start_date="2024-01-15", end_date="2024-01-15", data_points=0)
        )
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "9999", "start_date": "2024-01-15", "end_date": "2024-01-15"}
        )

        assert response.status_code == 200
        data = response.json()

        # 結構完整性
        assert "stock_code" in data
        assert "chart_data" in data
        assert "metadata" in data

        # 空資料驗證
        assert len(data["chart_data"]) == 0
        assert data["metadata"]["data_points"] == 0


class TestErrorFormatConsistency:
    """測試錯誤格式一致性（US G-2 AC3）。"""

    @patch('src.api.routes.chart.ChartService')
    def test_custom_error_format(self, mock_service_class):
        """
        驗證自定義錯誤符合契約格式。
        
        格式: { "detail": { "error": { "code", "message", "details" } } }
        """
        mock_service = Mock()
        mock_service.get_daily_chart.side_effect = ValueError("起始日期不得大於結束日期")
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024-01-31", "end_date": "2024-01-01"}
        )

        assert response.status_code == 400
        data = response.json()

        # 驗證錯誤結構
        assert "detail" in data
        assert "error" in data["detail"]
        
        error = data["detail"]["error"]
        assert "code" in error, "錯誤格式缺少 code"
        assert "message" in error, "錯誤格式缺少 message"
        # details 為選填
        
        # 驗證類型
        assert isinstance(error["code"], str)
        assert isinstance(error["message"], str)
        if "details" in error:
            assert isinstance(error["details"], str)

    @patch('src.api.routes.chart.ChartService')
    def test_internal_error_format(self, mock_service_class):
        """驗證伺服器錯誤格式一致性（500 Internal Server Error）。"""
        mock_service = Mock()
        mock_service.get_daily_chart.side_effect = Exception("Unexpected error")
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024-01-15", "end_date": "2024-01-15"}
        )

        assert response.status_code == 500
        data = response.json()

        # 驗證錯誤格式一致
        assert "detail" in data
        assert "error" in data["detail"]
        
        error = data["detail"]["error"]
        assert error["code"] == ErrorCodes.INTERNAL_ERROR

    def test_validation_error_format(self):
        """
        驗證參數驗證錯誤格式（422 Unprocessable Entity）。
        
        FastAPI 內建驗證錯誤格式不同於自定義錯誤。
        """
        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "12", "start_date": "2024-01-15", "end_date": "2024-01-15"}
        )

        assert response.status_code == 422
        data = response.json()

        # FastAPI 驗證錯誤格式
        assert "detail" in data
        assert isinstance(data["detail"], list)
        if data["detail"]:
            error_item = data["detail"][0]
            assert "type" in error_item
            assert "loc" in error_item
            assert "msg" in error_item


class TestBackwardCompatibility:
    """測試向後相容性（US G-2 AC2, AC5）。"""

    @patch('src.api.routes.chart.ChartService')
    def test_optional_fields_addition(self, mock_service_class):
        """
        驗證新增選填欄位不破壞現有客戶端。
        
        模擬未來新增 metadata 欄位（如 trading_days, total_volume）。
        """
        mock_service = Mock()
        # 模擬 metadata 擴充
        mock_metadata = Mock(
            stock_code="2330",
            start_date="2024-01-15",
            end_date="2024-01-15",
            data_points=1,
            # 假設未來新增這些欄位
            trading_days=1,
            total_volume=1000.0
        )
        mock_service.get_daily_chart.return_value = Mock(
            stock_code="2330",
            chart_data=[Mock(time="2024-01-15", open=580.0, high=585.0, low=578.0, close=583.0, volume=1000.0)],
            metadata=mock_metadata
        )
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024-01-15", "end_date": "2024-01-15"}
        )

        assert response.status_code == 200
        data = response.json()

        # 舊客戶端仍可讀取必要欄位
        assert "stock_code" in data
        assert "chart_data" in data
        assert "metadata" in data

        # 新欄位存在但不影響舊客戶端
        metadata = data["metadata"]
        assert "stock_code" in metadata
        assert "data_points" in metadata


class TestContractViolationPrevention:
    """防止契約違規的測試。"""

    @patch('src.api.routes.chart.ChartService')
    def test_required_fields_cannot_be_null(self, mock_service_class):
        """
        驗證必要欄位不得為 null。
        
        stock_code, chart_data 為必填。
        """
        mock_service = Mock()
        mock_service.get_daily_chart.return_value = Mock(
            stock_code="2330",
            chart_data=[],
            metadata=None  # metadata 可為 null
        )
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024-01-15", "end_date": "2024-01-15"}
        )

        data = response.json()
        assert data["stock_code"] is not None
        assert data["chart_data"] is not None
        # metadata 允許為 null（已在上方測試）

    @patch('src.api.routes.chart.ChartService')
    def test_date_format_consistency(self, mock_service_class):
        """
        驗證日期格式一致性（YYYY-MM-DD）。
        
        US G-2 AC1: 固定格式
        """
        mock_service = Mock()
        mock_service.get_daily_chart.return_value = Mock(
            stock_code="2330",
            chart_data=[
                Mock(time="2024-01-15", open=580.0, high=585.0, low=578.0, close=583.0, volume=1000.0),
                Mock(time="2024-01-16", open=583.0, high=590.0, low=582.0, close=588.0, volume=1500.0)
            ],
            metadata=Mock(stock_code="2330", start_date="2024-01-15", end_date="2024-01-16", data_points=2)
        )
        mock_service_class.return_value = mock_service

        response = client.get(
            "/api/chart/daily",
            params={"stock_code": "2330", "start_date": "2024-01-15", "end_date": "2024-01-16"}
        )

        data = response.json()
        
        # 驗證所有日期欄位格式
        import re
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        
        for point in data["chart_data"]:
            assert re.match(date_pattern, point["time"]), f"日期格式錯誤: {point['time']}"
        
        metadata = data["metadata"]
        assert re.match(date_pattern, metadata["start_date"])
        assert re.match(date_pattern, metadata["end_date"])
