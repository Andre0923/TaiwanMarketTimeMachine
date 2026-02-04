# @spec Feature 001-basic-chart-api
"""
Taiwan Market Time Machine - FastAPI Application Entry Point.

台股時光機主應用程式入口，提供 RESTful API 服務。

功能:
- 初始化 FastAPI 應用程式
- 註冊 API 路由
- 設定 CORS 中介層
- 全域錯誤處理
- 健康檢查端點
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from src.logger import setup_logger
from src.api.routes import chart

logger = setup_logger(__name__)

# 初始化 FastAPI 應用程式
app = FastAPI(
    title="Taiwan Market Time Machine API",
    description="台股時光機 - 視覺化事件研究平台 API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS 設定（允許前端跨域請求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開發階段允許所有來源，正式環境需限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊 API 路由
app.include_router(chart.router)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    全域錯誤處理器，捕捉所有未處理的例外。

    Args:
        request: FastAPI Request 物件
        exc: 例外物件

    Returns:
        JSONResponse: 標準化錯誤回應
    """
    logger.error(
        f"未預期的錯誤: {str(exc)}",
        extra={
            "path": request.url.path,
            "method": request.method,
            "error_type": type(exc).__name__,
        },
        exc_info=True,
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "伺服器內部錯誤",
                "details": str(exc) if app.debug else "請聯絡系統管理員",
            }
        },
    )


@app.get("/health", tags=["System"])
async def health_check():
    """
    健康檢查端點，用於確認 API 服務運作正常。

    Returns:
        dict: 包含服務狀態的回應

    Example:
        >>> GET /health
        {
            "status": "healthy",
            "service": "taiwan-market-time-machine-api",
            "version": "0.1.0"
        }
    """
    logger.debug("健康檢查請求")

    return {
        "status": "healthy",
        "service": "taiwan-market-time-machine-api",
        "version": "0.1.0",
    }


@app.get("/", tags=["System"])
async def root():
    """
    API 根路徑，提供基本資訊。

    Returns:
        dict: API 基本資訊
    """
    return {
        "message": "Taiwan Market Time Machine API",
        "version": "0.1.0",
        "docs_url": "/docs",
        "health_check": "/health",
    }


# TODO: Phase 2 將註冊 chart router
# from src.api.routes import chart
# app.include_router(chart.router, prefix="/api", tags=["Chart"])


if __name__ == "__main__":
    import uvicorn

    logger.info("啟動 FastAPI 應用程式...")

    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # 開發模式自動重載
        log_level="info",
    )
