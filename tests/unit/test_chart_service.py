"""
Unit tests for ChartService.

測試 Service 層的日K聚合邏輯與業務流程。
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from src.services.chart_service import ChartService
from src.db.stock_repository import StockRepository
from src.models.chart import ChartResponse


class TestChartService:
    """測試 ChartService 類別。"""

    def test_init_without_repository(self):
        """測試無 Repository 初始化（自動建立）。"""
        service = ChartService()
        assert service.repository is not None
        assert isinstance(service.repository, StockRepository)

    def test_init_with_repository(self):
        """測試注入 Repository 初始化。"""
        mock_repo = Mock(spec=StockRepository)
        service = ChartService(repository=mock_repo)
        assert service.repository is mock_repo


class TestGetDailyChart:
    """測試 get_daily_chart 方法。"""

    def test_successful_aggregation(self):
        """測試成功聚合 1分K → 日K。"""
        # Mock Repository
        mock_repo = Mock(spec=StockRepository)
        mock_repo.get_one_minute_klines.return_value = [
            # 2024-01-15 的 1分K 資料
            (datetime(2024, 1, 15), datetime(1900, 1, 1, 9, 0), "2330", 580.0, 582.0, 579.0, 581.0, 1000.0),
            (datetime(2024, 1, 15), datetime(1900, 1, 1, 9, 1), "2330", 581.0, 585.0, 580.0, 583.0, 1500.0),
            (datetime(2024, 1, 15), datetime(1900, 1, 1, 9, 2), "2330", 583.0, 584.0, 578.0, 580.0, 1200.0),
        ]

        service = ChartService(repository=mock_repo)
        response = service.get_daily_chart("2330", "2024-01-15", "2024-01-15")

        # 驗證回應結構
        assert isinstance(response, ChartResponse)
        assert response.stock_code == "2330"
        assert len(response.chart_data) == 1

        # 驗證聚合邏輯
        data_point = response.chart_data[0]
        assert data_point.time == "2024-01-15"
        assert data_point.open == 580.0    # FIRST_VALUE (9:00)
        assert data_point.high == 585.0    # MAX
        assert data_point.low == 578.0     # MIN
        assert data_point.close == 580.0   # LAST_VALUE (9:02)
        assert data_point.volume == 3700.0 # SUM

        # 驗證 metadata
        assert response.metadata is not None
        assert response.metadata.data_points == 1
        assert response.metadata.start_date == "2024-01-15"
        assert response.metadata.end_date == "2024-01-15"

    def test_multiple_days_aggregation(self):
        """測試多日資料聚合。"""
        mock_repo = Mock(spec=StockRepository)
        mock_repo.get_one_minute_klines.return_value = [
            # 2024-01-15
            (datetime(2024, 1, 15), datetime(1900, 1, 1, 9, 0), "2330", 580.0, 585.0, 578.0, 583.0, 1000.0),
            (datetime(2024, 1, 15), datetime(1900, 1, 1, 9, 1), "2330", 583.0, 586.0, 582.0, 585.0, 1500.0),
            # 2024-01-16
            (datetime(2024, 1, 16), datetime(1900, 1, 1, 9, 0), "2330", 585.0, 590.0, 584.0, 588.0, 2000.0),
            (datetime(2024, 1, 16), datetime(1900, 1, 1, 9, 1), "2330", 588.0, 592.0, 587.0, 590.0, 2500.0),
        ]

        service = ChartService(repository=mock_repo)
        response = service.get_daily_chart("2330", "2024-01-15", "2024-01-16")

        # 驗證有兩天的資料
        assert len(response.chart_data) == 2

        # 驗證第一天
        day1 = response.chart_data[0]
        assert day1.time == "2024-01-15"
        assert day1.open == 580.0
        assert day1.high == 586.0
        assert day1.low == 578.0
        assert day1.close == 585.0
        assert day1.volume == 2500.0

        # 驗證第二天
        day2 = response.chart_data[1]
        assert day2.time == "2024-01-16"
        assert day2.open == 585.0
        assert day2.high == 592.0
        assert day2.low == 584.0
        assert day2.close == 590.0
        assert day2.volume == 4500.0

    def test_no_data_handling(self):
        """測試無資料情況（US A-1 AC3）。"""
        mock_repo = Mock(spec=StockRepository)
        mock_repo.get_one_minute_klines.return_value = []

        service = ChartService(repository=mock_repo)
        response = service.get_daily_chart("9999", "2024-01-15", "2024-01-15")

        # 驗證回應結構
        assert response.stock_code == "9999"
        assert len(response.chart_data) == 0
        assert response.metadata is not None
        assert response.metadata.data_points == 0

    def test_invalid_date_range(self):
        """測試無效的日期範圍（起始日期 > 結束日期）。"""
        mock_repo = Mock(spec=StockRepository)
        service = ChartService(repository=mock_repo)

        with pytest.raises(ValueError) as exc_info:
            service.get_daily_chart("2330", "2024-01-31", "2024-01-01")
        assert "不得大於結束日期" in str(exc_info.value)

    def test_invalid_date_format(self):
        """測試無效的日期格式。"""
        mock_repo = Mock(spec=StockRepository)
        service = ChartService(repository=mock_repo)

        with pytest.raises(ValueError) as exc_info:
            service.get_daily_chart("2330", "2024/01/01", "2024-01-31")
        assert "日期格式錯誤" in str(exc_info.value)


class TestAggregateToDaily:
    """測試 _aggregate_to_daily 方法（內部邏輯）。"""

    def test_aggregate_logic(self):
        """測試聚合邏輯的正確性。"""
        service = ChartService()

        # 模擬 1分K 資料（同一天的多筆資料）
        one_min_data = [
            (datetime(2024, 1, 15), datetime(1900, 1, 1, 9, 0), "2330", 100.0, 105.0, 99.0, 102.0, 1000.0),
            (datetime(2024, 1, 15), datetime(1900, 1, 1, 9, 1), "2330", 102.0, 108.0, 101.0, 107.0, 1500.0),
            (datetime(2024, 1, 15), datetime(1900, 1, 1, 9, 2), "2330", 107.0, 110.0, 95.0, 98.0, 2000.0),
        ]

        result = service._aggregate_to_daily(one_min_data)

        # 驗證聚合結果
        assert "2024-01-15" in result
        day_data = result["2024-01-15"]
        assert day_data["open"] == 100.0    # FIRST (9:00)
        assert day_data["high"] == 110.0    # MAX
        assert day_data["low"] == 95.0      # MIN
        assert day_data["close"] == 98.0    # LAST (9:02)
        assert day_data["volume"] == 4500.0 # SUM

    def test_aggregate_multiple_days(self):
        """測試多日聚合。"""
        service = ChartService()

        one_min_data = [
            (datetime(2024, 1, 15), datetime(1900, 1, 1, 9, 0), "2330", 100.0, 105.0, 99.0, 102.0, 1000.0),
            (datetime(2024, 1, 16), datetime(1900, 1, 1, 9, 0), "2330", 200.0, 205.0, 199.0, 202.0, 2000.0),
        ]

        result = service._aggregate_to_daily(one_min_data)

        assert len(result) == 2
        assert "2024-01-15" in result
        assert "2024-01-16" in result
        assert result["2024-01-15"]["open"] == 100.0
        assert result["2024-01-16"]["open"] == 200.0


class TestConvertToChartData:
    """測試 _convert_to_chart_data 方法。"""

    def test_convert_and_sort(self):
        """測試轉換並排序。"""
        service = ChartService()

        daily_data = {
            "2024-01-16": {"open": 200.0, "high": 205.0, "low": 199.0, "close": 202.0, "volume": 2000.0},
            "2024-01-15": {"open": 100.0, "high": 105.0, "low": 99.0, "close": 102.0, "volume": 1000.0},
        }

        result = service._convert_to_chart_data(daily_data)

        # 驗證排序（應該按日期升序）
        assert len(result) == 2
        assert result[0].time == "2024-01-15"
        assert result[1].time == "2024-01-16"

        # 驗證資料正確性
        assert result[0].open == 100.0
        assert result[1].open == 200.0
