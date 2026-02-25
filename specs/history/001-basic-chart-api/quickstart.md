# Quick Start Guide: 基礎繪圖與 API 格式（M01）

> **Feature ID**: 001-basic-chart-api  
> **Target Audience**: 開發者、QA  
> **Estimated Time**: 20 分鐘  
> **實作狀態**: ✅ 後端完成 | 🚧 前端延後至 M02

---

## 1. Overview

本指南協助您快速建立 M01 Feature 的開發環境，並測試後端 API 功能。

**完成後您將能夠**：
- ✅ 執行後端 API 伺服器（FastAPI）
- ✅ 測試日K線圖表資料 API
- ✅ 執行完整測試套件（61 個測試）
- ✅ 查看 API 文件與契約

**前端開發**：前端互動介面（Vue 3 + TradingView Charts）延後至 M02 實作。

---

## 2. Prerequisites

### 2.1 系統需求

| 項目 | 版本 | 安裝驗證指令 |
|------|------|--------------|
| **Python** | 3.14+ | `python --version` |
| **uv** | latest | `uv --version` |
| **Microsoft SQL Server** | 2019+ | `sqlcmd -?` (可選) |
| **Git** | 2.0+ | `git --version` |

### 2.2 安裝必要工具

#### Windows

```powershell
# 安裝 uv（Python 環境管理）
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 驗證安裝
uv --version
python --version
```

---

## 3. 環境設定

### 3.1 Clone 專案

```powershell
git clone https://github.com/Andre0923/TaiwanMarketTimeMachine.git
cd TaiwanMarketTimeMachine

# 切換至開發分支
git checkout 1-basic-chart-api
```

### 3.2 安裝 Python 依賴

```powershell
# 建立虛擬環境並安裝所有依賴
uv sync

# 驗證安裝
uv run python -c "import fastapi; print(f'FastAPI {fastapi.__version__}')"
```

**預期輸出**：`FastAPI 0.128.x`

### 3.3 資料庫連線設定

建立 `.env` 檔案（複製 `.env.example`）：

```bash
# Database Configuration
DB_SERVER=CMoney        # 您的 MSSQL Server 名稱
DB_PORT=16888
DB_DATABASE=股價即時
DB_DRIVER=ODBC Driver 18 for SQL Server
DB_TRUST_CERT=yes
```

**測試資料庫連線**：
```powershell
uv run python -c "from src.db.connection import test_connection; test_connection()"
```

**預期輸出**：
```
✅ Database connection successful!
Server: CMoney:16888
Database: 股價即時
```

**常見問題排解**：
- ❌ `Connection failed`: 檢查 DB_SERVER 與 DB_PORT 是否正確
- ❌ `Login failed`: 檢查 Windows 驗證或 SQL 帳密設定
- ❌ `Driver not found`: 安裝 [ODBC Driver 18](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)

---

## 4. 啟動後端 API 服務

### 4.1 開發模式啟動

```powershell
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**預期輸出**：
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 4.2 驗證服務啟動

開啟瀏覽器訪問：

| 端點 | 說明 | URL |
|------|------|-----|
| **健康檢查** | 確認服務運行 | http://localhost:8000/health |
| **API 文件** | Swagger UI 互動文件 | http://localhost:8000/docs |
| **ReDoc** | 詳細 API 文件 | http://localhost:8000/redoc |

**健康檢查預期回應**：
```json
{
  "status": "healthy",
  "timestamp": "2026-02-04T12:00:00",
  "version": "0.1.0"
}
```

---

## 5. 測試 API 端點

### 5.1 使用 Swagger UI（推薦）

1. 開啟 http://localhost:8000/docs
2. 展開 `GET /api/chart/daily`
3. 點擊「Try it out」
4. 輸入參數：
   - `stock_code`: `2330`
   - `start_date`: `2024-01-01`
   - `end_date`: `2024-01-31`
5. 點擊「Execute」

**預期回應**（200 OK）：
```json
{
  "stock_code": "2330",
  "chart_data": [
    {
      "time": "2024-01-02",
      "open": 585.0,
      "high": 590.0,
      "low": 583.0,
      "close": 588.0,
      "volume": 15234567.0
    }
    // ... 更多資料點
  ],
  "metadata": {
    "stock_code": "2330",
    "start_date": "2024-01-02",
    "end_date": "2024-01-31",
    "data_points": 20
  }
}
```

### 5.2 使用 curl

```bash
curl -X GET "http://localhost:8000/api/chart/daily?stock_code=2330&start_date=2024-01-01&end_date=2024-01-31" \
  -H "Accept: application/json"
```

### 5.3 使用 Python

```python
import requests

response = requests.get(
    "http://localhost:8000/api/chart/daily",
    params={
        "stock_code": "2330",
        "start_date": "2024-01-01",
        "end_date": "2024-01-31"
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"股票: {data['stock_code']}")
    print(f"資料點數: {data['metadata']['data_points']}")
    
    # 顯示前 5 筆資料
    for point in data['chart_data'][:5]:
        print(f"{point['time']}: 開={point['open']}, 收={point['close']}, 量={point['volume']}")
else:
    print(f"錯誤: {response.status_code}")
    print(response.json())
```

### 5.4 錯誤處理測試

#### 測試無效日期範圍

```bash
curl -X GET "http://localhost:8000/api/chart/daily?stock_code=2330&start_date=2024-01-31&end_date=2024-01-01"
```

**預期回應**（400 Bad Request）：
```json
{
  "detail": {
    "error": {
      "code": "INVALID_DATE_RANGE",
      "message": "參數驗證錯誤",
      "details": "起始日期 (2024-01-31) 不得大於結束日期 (2024-01-01)"
    }
  }
}
```

#### 測試查無資料

```bash
curl -X GET "http://localhost:8000/api/chart/daily?stock_code=9999&start_date=2024-01-01&end_date=2024-01-31"
```

**預期回應**（200 OK，空資料）：
```json
{
  "stock_code": "9999",
  "chart_data": [],
  "metadata": {
    "stock_code": "9999",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "data_points": 0
  }
}
```

---

## 6. 執行測試

### 6.1 執行所有測試

```powershell
uv run pytest tests/ -v
```

**預期輸出**：
```
======================== 61 passed, 1 warning in 1.5s ========================
```

### 6.2 執行特定測試

```powershell
# 只執行單元測試
uv run pytest tests/unit/ -v

# 只執行整合測試
uv run pytest tests/integration/ -v

# 執行特定測試檔案
uv run pytest tests/integration/test_chart_api.py -v
```

### 6.3 生成覆蓋率報告

```powershell
uv run pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html:.artifacts/coverage/html
```

**開啟覆蓋率報告**：
```powershell
start .artifacts/coverage/html/index.html
```

**預期覆蓋率**：89%（核心模組 100%）

---

## 7. 查看文件

### 7.1 API 契約文件

詳細的 API 規範、錯誤碼、使用範例：

```powershell
# 使用 VS Code 開啟
code specs/features/001-basic-chart-api/contracts/chart-api.md
```

**包含內容**：
- Request/Response 完整格式
- 錯誤碼對照表
- 向後相容策略
- curl/Python/JavaScript 使用範例
- TradingView Charts 整合指引

### 7.2 其他文件

| 文件 | 路徑 | 說明 |
|------|------|------|
| **Feature Spec** | `specs/features/001-basic-chart-api/spec.md` | User Story 定義 |
| **Data Model** | `specs/features/001-basic-chart-api/data-model.md` | 資料結構與聚合邏輯 |
| **Technical Plan** | `specs/features/001-basic-chart-api/plan.md` | 技術架構規劃 |
| **Tasks** | `specs/features/001-basic-chart-api/tasks.md` | 實作任務清單 |

---

## 8. 常見問題排解

### 8.1 資料庫連線失敗

**症狀**：`pyodbc.OperationalError: ('08001', ...)`

**解決方案**：
1. 檢查 `.env` 檔案中的 `DB_SERVER` 與 `DB_PORT`
2. 確認 SQL Server 服務正在運行
3. 測試連線：`sqlcmd -S CMoney,16888 -Q "SELECT @@VERSION"`
4. 檢查防火牆設定

### 8.2 測試失敗

**症狀**：部分測試失敗或 import 錯誤

**解決方案**：
```powershell
# 清除快取並重新安裝
Remove-Item -Recurse -Force .venv, .artifacts/pytest_cache
uv sync
uv run pytest tests/ -v
```

### 8.3 Port 8000 已被佔用

**症狀**：`Address already in use`

**解決方案**：
```powershell
# 使用不同 Port
uv run uvicorn src.main:app --reload --port 8001

# 或終止佔用 Port 的程序（Windows）
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### 8.4 ODBC Driver 未安裝

**症狀**：`Data source name not found`

**解決方案**：
1. 下載 [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
2. 安裝後重新測試連線

---

## 9. 下一步

### 9.1 開發新功能

```powershell
# 使用 SpecKit 流程
/speckit.clarify "新功能描述"
/speckit.plan
/speckit.tasks
/speckit.implement
```

### 9.2 前端整合（M02）

目前後端 API 已完成，前端開發將在 M02 milestone 進行：
- Vue 3 + Vite 專案初始化
- TradingView Lightweight Charts 整合
- 圖表互動操作（Zoom/Pan/Crosshair）
- Loading 狀態與錯誤處理

### 9.3 學習資源

- [FastAPI 官方文件](https://fastapi.tiangolo.com/)
- [Pydantic 驗證](https://docs.pydantic.dev/)
- [pytest 測試框架](https://docs.pytest.org/)
- [SpecKit + FlowKit 開發流程](../../docs/01.開發人員doc/03.SDD開發流程指南.md)

---

## 10. 驗收檢查清單

完成以下檢查確認環境設定正確：

- [ ] ✅ uv 與 Python 3.14+ 已安裝
- [ ] ✅ 專案依賴已安裝（`uv sync`）
- [ ] ✅ 資料庫連線測試成功
- [ ] ✅ FastAPI 服務啟動正常
- [ ] ✅ 健康檢查端點回應正常（http://localhost:8000/health）
- [ ] ✅ API 文件可訪問（http://localhost:8000/docs）
- [ ] ✅ 測試日K線 API 成功（`stock_code=2330`）
- [ ] ✅ 所有測試通過（`pytest tests/ -v`）
- [ ] ✅ 覆蓋率報告生成（89%）

---

**建議學習時間**：
- 環境設定：5 分鐘
- API 測試：5 分鐘
- 執行測試：5 分鐘
- 文件閱讀：5 分鐘

**總計**：約 20 分鐘
