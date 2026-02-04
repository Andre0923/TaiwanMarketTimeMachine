# @spec US-A1 (001-basic-chart-api/spec.md#user-story-a-1)
# @spec-ac AC1, AC2, AC3
# @spec US-G2 (001-basic-chart-api/spec.md#user-story-g-2)
# @spec-ac AC1, AC2, AC3
"""
Chart API Router.

提供日K線圖表資料的 RESTful API 端點。
"""

from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional
import time
from src.services.chart_service import ChartService
from src.models.chart import ChartResponse, ErrorResponse, ErrorDetail, ErrorCodes
from src.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter(prefix="/api/chart", tags=["Chart"])


@router.get(
    "/daily",
    response_model=ChartResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request parameters"},
        404: {"model": ErrorResponse, "description": "No data found"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    },
    summary="取得日K線圖表資料",
    description="""
    查詢指定股票的日K線資料（從 1分K 聚合）。
    
    **Query Parameters**:
    - `stock_code`: 股票代碼（4-10 碼）
    - `start_date`: 起始日期（YYYY-MM-DD）
    - `end_date`: 結束日期（YYYY-MM-DD）
    
    **Response Format** (符合 US G-2):
    - 固定結構：`stock_code`, `chart_data[]`, `metadata`
    - 空資料回傳空陣列（US A-1 AC3）
    - 錯誤統一格式：`error.code`, `error.message`, `error.details`
    """
)
async def get_daily_chart(
    stock_code: str = Query(
        ...,
        min_length=4,
        max_length=10,
        description="股票代碼（如 2330）",
        examples=["2330"]
    ),
    start_date: str = Query(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="起始日期（YYYY-MM-DD）",
        examples=["2024-01-01"]
    ),
    end_date: str = Query(
        ...,
        pattern=r"^\d{4}-\d{2}-\d{2}$",
        description="結束日期（YYYY-MM-DD）",
        examples=["2024-01-31"]
    )
) -> ChartResponse:
    """
    取得日K線圖表資料。
    
    Args:
        stock_code: 股票代碼
        start_date: 起始日期
        end_date: 結束日期
    
    Returns:
        ChartResponse: 包含 K線資料與 metadata
    
    Raises:
        HTTPException: 參數錯誤、查無資料、或伺服器錯誤
    """
    request_start = time.time()
    
    logger.info(
        f"API Request: GET /api/chart/daily",
        extra={
            "stock_code": stock_code,
            "start_date": start_date,
            "end_date": end_date
        }
    )

    try:
        # 呼叫 Service 層
        service = ChartService()
        response = service.get_daily_chart(
            stock_code=stock_code,
            start_date=start_date,
            end_date=end_date
        )

        # 計算回應時間
        response_time = (time.time() - request_start) * 1000  # 轉為毫秒

        logger.info(
            f"API Response: Success",
            extra={
                "stock_code": stock_code,
                "data_points": len(response.chart_data),
                "response_time_ms": round(response_time, 2)
            }
        )

        # 若無資料，根據 AC3 回傳 404（可選設計）
        # 此處為彈性設計：回傳 200 + 空陣列，前端可自行處理
        if not response.chart_data:
            logger.warning(
                f"No data found: {stock_code} ({start_date} ~ {end_date})",
                extra={"stock_code": stock_code}
            )
            # 可選：回傳 404
            # raise HTTPException(
            #     status_code=status.HTTP_404_NOT_FOUND,
            #     detail={
            #         "error": {
            #             "code": ErrorCodes.NO_DATA,
            #             "message": "查無資料",
            #             "details": f"股票 {stock_code} 在 {start_date} ~ {end_date} 期間無資料"
            #         }
            #     }
            # )

        return response

    except ValueError as e:
        # 參數驗證錯誤（日期格式、日期範圍）
        logger.error(
            f"Validation error: {str(e)}",
            extra={"stock_code": stock_code, "error": str(e)}
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "code": ErrorCodes.INVALID_DATE_RANGE,
                    "message": "參數驗證錯誤",
                    "details": str(e)
                }
            }
        )

    except Exception as e:
        # 未預期的錯誤
        logger.error(
            f"Unexpected error: {str(e)}",
            extra={"stock_code": stock_code, "error": str(e)},
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": {
                    "code": ErrorCodes.INTERNAL_ERROR,
                    "message": "伺服器內部錯誤",
                    "details": "請稍後再試或聯繫系統管理員"
                }
            }
        )
