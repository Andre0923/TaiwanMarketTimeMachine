# @spec US-A1 (001-basic-chart-api/spec.md#user-story-a-1)
# @spec-ac AC1, AC2, AC3
"""
Chart Service Layer.

負責圖表資料的業務邏輯處理，包括：
1. 將 1分K 資料聚合為日K
2. 資料驗證與格式轉換
3. 無資料情況處理（US A-1 AC3）
"""

from typing import List, Optional
from datetime import datetime
from collections import defaultdict
from src.db.stock_repository import StockRepository
from src.models.chart import ChartDataPoint, ChartResponse, ChartMetadata
from src.logger import setup_logger

logger = setup_logger(__name__)


class ChartService:
    """
    圖表資料服務層。
    
    提供日K線資料查詢與聚合邏輯。
    """

    def __init__(self, repository: Optional[StockRepository] = None):
        """
        初始化 Service。
        
        Args:
            repository: StockRepository 實例（選填，支援 DI）
        """
        self.repository = repository or StockRepository()

    def get_daily_chart(
        self,
        stock_code: str,
        start_date: str,
        end_date: str
    ) -> ChartResponse:
        """
        取得日K線圖表資料（從 1分K 聚合）。
        
        聚合邏輯（符合 data-model.md 定義）：
        - Open: FIRST_VALUE(開盤價) ORDER BY 時間 ASC
        - High: MAX(最高價)
        - Low: MIN(最低價)
        - Close: LAST_VALUE(收盤價) ORDER BY 時間 DESC
        - Volume: SUM(成交量)
        
        Args:
            stock_code: 股票代碼
            start_date: 起始日期（YYYY-MM-DD）
            end_date: 結束日期（YYYY-MM-DD）
        
        Returns:
            ChartResponse: 包含日K資料與 metadata
        
        Raises:
            ValueError: 日期格式錯誤或日期範圍無效
        
        Example:
            >>> service = ChartService()
            >>> response = service.get_daily_chart("2330", "2024-01-01", "2024-01-31")
            >>> response.stock_code
            '2330'
        """
        logger.info(
            f"Service: 查詢日K資料",
            extra={"stock_code": stock_code, "start_date": start_date, "end_date": end_date}
        )

        # 驗證日期範圍
        self._validate_date_range(start_date, end_date)

        # 查詢 1分K 資料
        one_min_data = self.repository.get_one_minute_klines(
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date
        )

        # 處理無資料情況（US A-1 AC3）
        if not one_min_data:
            logger.warning(
                f"查無資料: {stock_code} ({start_date} ~ {end_date})",
                extra={"stock_code": stock_code}
            )
            return ChartResponse(
                stock_code=stock_code,
                chart_data=[],
                metadata=ChartMetadata(
                    stock_code=stock_code,
                    start_date=start_date,
                    end_date=end_date,
                    data_points=0
                )
            )

        # 聚合為日K
        daily_data = self._aggregate_to_daily(one_min_data)

        # 轉換為 ChartDataPoint
        chart_data = self._convert_to_chart_data(daily_data)

        # 建立 metadata
        metadata = ChartMetadata(
            stock_code=stock_code,
            start_date=chart_data[0].time if chart_data else start_date,
            end_date=chart_data[-1].time if chart_data else end_date,
            data_points=len(chart_data)
        )

        logger.info(
            f"Service: 日K資料處理完成",
            extra={
                "stock_code": stock_code,
                "data_points": metadata.data_points,
                "date_range": f"{metadata.start_date} ~ {metadata.end_date}"
            }
        )

        return ChartResponse(
            stock_code=stock_code,
            chart_data=chart_data,
            metadata=metadata
        )

    def _validate_date_range(self, start_date: str, end_date: str) -> None:
        """
        驗證日期範圍。
        
        Args:
            start_date: 起始日期
            end_date: 結束日期
        
        Raises:
            ValueError: 日期格式錯誤或起始日期 > 結束日期
        """
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError as e:
            raise ValueError(f"日期格式錯誤: {e}")

        if start > end:
            raise ValueError(f"起始日期 ({start_date}) 不得大於結束日期 ({end_date})")

    def _aggregate_to_daily(self, one_min_data: List[tuple]) -> dict:
        """
        將 1分K 資料聚合為日K。
        
        Args:
            one_min_data: 1分K 資料列表 [(日期, 時間, 股票代號, 開盤價, 最高價, 最低價, 收盤價, 成交量), ...]
        
        Returns:
            dict: {日期: {open, high, low, close, volume}, ...}
        """
        daily_aggregates = defaultdict(lambda: {
            "open": None,
            "high": float('-inf'),
            "low": float('inf'),
            "close": None,
            "volume": 0.0,
            "first_time": None,
            "last_time": None
        })

        for row in one_min_data:
            # 解構資料（對應 data-model.md 的欄位順序）
            date_val, time_val, stock_code, open_price, high_price, low_price, close_price, volume = row

            # 轉換日期為字串（YYYY-MM-DD）
            if isinstance(date_val, datetime):
                date_str = date_val.strftime("%Y-%m-%d")
            else:
                date_str = str(date_val)

            # 轉換時間（用於判斷 FIRST/LAST）
            if isinstance(time_val, datetime):
                time_obj = time_val
            else:
                time_obj = datetime.strptime(str(time_val), "%H:%M:%S")

            agg = daily_aggregates[date_str]

            # Open: FIRST_VALUE（最早時間的開盤價）
            if agg["first_time"] is None or time_obj < agg["first_time"]:
                agg["first_time"] = time_obj
                agg["open"] = float(open_price)

            # High: MAX
            agg["high"] = max(agg["high"], float(high_price))

            # Low: MIN
            agg["low"] = min(agg["low"], float(low_price))

            # Close: LAST_VALUE（最晚時間的收盤價）
            if agg["last_time"] is None or time_obj > agg["last_time"]:
                agg["last_time"] = time_obj
                agg["close"] = float(close_price)

            # Volume: SUM
            agg["volume"] += float(volume)

        # 移除輔助欄位
        for date_str in daily_aggregates:
            del daily_aggregates[date_str]["first_time"]
            del daily_aggregates[date_str]["last_time"]

        return dict(daily_aggregates)

    def _convert_to_chart_data(self, daily_data: dict) -> List[ChartDataPoint]:
        """
        將聚合後的日K資料轉換為 ChartDataPoint 列表。
        
        Args:
            daily_data: 日K資料字典
        
        Returns:
            List[ChartDataPoint]: 排序後的資料點列表
        """
        chart_data = []
        for date_str, values in sorted(daily_data.items()):  # 按日期排序
            chart_data.append(
                ChartDataPoint(
                    time=date_str,
                    open=values["open"],
                    high=values["high"],
                    low=values["low"],
                    close=values["close"],
                    volume=values["volume"]
                )
            )
        return chart_data
