# Implementation Plan: 基礎繪圖與 API 格式

> **Feature ID**: 001-basic-chart-api  
> **Plan Version**: 1.0  
> **Created**: 2026-02-04  
> **Spec Reference**: [spec.md](./spec.md)

---

## 1. Technical Context

### 1.1 Current State Analysis

| 組件 | 現狀 | 目標狀態 | 落差等級 |
|------|------|----------|----------|
| **後端 API** | 不存在 | FastAPI 提供 `/api/v1/chart-data` 端點 | CRITICAL |
| **資料庫連線** | 無連線模組 | pyodbc + MSSQL 連線管理 | CRITICAL |
| **日K聚合邏輯** | 不存在 | 從 1分K 聚合為日K (OHLCV) | CRITICAL |
| **前端專案** | 不存在 | Vue 3 + TradingView Lightweight Charts | CRITICAL |
| **圖表元件** | 不存在 | K線圖 + 成交量副圖 + 互動操作 | CRITICAL |
| **錯誤處理** | 無標準 | 標準化錯誤碼 + 詳細日誌 | HIGH |
| **Loading UX** | 無設計 | 300ms 最小顯示時間 + Spinner | MEDIUM |
| **快取機制** | 不存在 | 前端 5分鐘快取 | MEDIUM |

### 1.2 Technology Stack

| 項目 | 技術選擇 | 理由 |
|------|----------|------|
| **後端框架** | FastAPI 0.110+ | 非同步支援、自動 API 文件、Python 生態系 |
| **資料庫驅動** | pyodbc 5.0+ | MSSQL 官方支援的 Python DB-API |
| **環境管理** | uv | 快速、現代化的 Python 套件管理（Constitution §5.2） |
| **前端框架** | Vue 3 | 輕量、易整合、符合 PRD 技術選型 |
| **圖表庫** | TradingView Lightweight Charts 4.1+ | 高效能、內建金融圖表功能、台股紅漲綠跌可配置 |
| **HTTP Client** | Axios 或 Fetch API | 前端 API 呼叫與快取管理 |
| **測試框架** | pytest 8.0+ | Python 標準測試工具，支援 coverage |
| **日誌模組** | src/logger.py（已存在） | 專案統一日誌管理（System Context §3.3） |

### 1.3 Affected Files

**新增檔案**：
```
後端：
├── src/main.py                           # FastAPI 應用程式入口
├── src/api/
│   └── chart.py                          # 圖表 API 路由
├── src/services/
│   └── chart_service.py                  # 圖表業務邏輯（日K聚合）
├── src/db/
│   ├── __init__.py
│   ├── connection.py                     # MSSQL 連線管理
│   └── stock_repository.py               # 股票資料查詢
├── src/models/
│   ├── __init__.py
│   ├── request_models.py                 # Request DTO (ChartDataRequest)
│   ├── response_models.py                # Response DTO (ChartDataResponse, ErrorResponse)
│   └── domain_models.py                  # Domain Models (OHLCData)
├── tests/
│   ├── unit/
│   │   ├── test_chart_service.py        # Service 層單元測試
│   │   └── test_stock_repository.py     # Repository 單元測試
│   └── integration/
│       └── test_chart_api.py            # API 整合測試
└── specs/features/001-basic-chart-api/
    └── contracts/
        └── chart-api.md                  # API 契約文件

前端（待 M02 詳細規劃）：
├── frontend/                             # Vue 3 專案根目錄
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChartComponent.vue       # K線圖表元件
│   │   │   └── LoadingSpinner.vue       # Loading 指示器
│   │   ├── services/
│   │   │   └── chartApi.ts              # API 呼叫服務
│   │   └── utils/
│   │       └── cache.ts                 # 前端快取工具
│   └── package.json
```

**修改檔案**：
```
- .env.example                            # 新增資料庫連線範例
- pyproject.toml                          # 新增後端依賴套件
- .gitignore                              # 確保 .env 被排除（已完成）
- specs/features/001-basic-chart-api/data-model.md   # 確認資料表 Schema
```

---

## 2. UI/UX Plan

> 本 Feature 涉及前端圖表 UI，需定義相關 UI 行為與狀態。

### 2.1 UI Impact Summary

| 項目 | 值 |
|------|---|
| **UI Impact** | High（涉及圖表元件、互動操作、狀態管理） |
| **Current Maturity** | L0（無 UI 文件） |
| **Target Maturity** | L1（定義 Global States、Screen Catalog） |

### 2.2 UI Discovery Tasks

由於專案初期無 `specs/system/ui/` 目錄，本 Feature 暫不建立 System Level UI 文件，改以 Feature Level 方式記錄 UI 行為於 Spec AC 中。

**已完成**：
- ✅ AC 已定義 Loading/Empty/Error 狀態（US A-4）
- ✅ AC 已定義不可逆操作（N/A，本 Feature 無不可逆操作）
- ✅ AC 已定義主要互動流程（Zoom/Pan/Crosshair - US A-2）

**本次不執行**：
- ⏸️ System Level UI 文件（延後至 M02，Grid 模式時統一規劃）

### 2.3 受影響畫面

| UI ID | 畫面名稱 | 當前 Maturity | 目標 Maturity | 變更類型 |
|-------|----------|---------------|---------------|----------|
| [UI-TBD-001] | 基礎 K 線圖表 | L0 | L1（AC 已定義） | 新增 |
| [UI-TBD-002] | Loading 狀態指示器 | L0 | L1（AC 已定義） | 新增 |
| [UI-TBD-003] | 錯誤提示與重試 | L0 | L1（AC 已定義） | 新增 |

### 2.4 新增 Pattern/State

| UI ID | 類型 | 說明 |
|-------|------|------|
| [UI-STATE-001] | State | Loading 最小顯示時間 300ms |
| [UI-STATE-002] | State | 前端快取 5 分鐘 TTL |
| [UI-PAT-001] | Pattern | 小圖點擊放大（US A-3） |

### 2.5 UI 文件更新任務

**M01 階段**：
- ✅ **不建立** `specs/system/ui/` 目錄（延後至 M02）
- ✅ UI 行為已定義於 `spec.md` 的 AC 中（符合 §1.4 要求）
- [ ] 前端實作完成後，補充實際 UI ID 分配（若需要）

**M02 階段（Grid Mode）**：
- [ ] 建立 `specs/system/ui/ui-structure.md`
- [ ] 建立 `specs/system/ui/ux-guidelines.md`
- [ ] 統一分配 UI ID 給所有元件

---

## 3. Constitution Compliance Check

> 以下為 Plan 階段必須檢查的固定清單。每次執行 Plan 時 MUST 逐條填寫狀態。

### 3.1 NON-NEGOTIABLE Requirements (🔴)

| 條款 | 要求 | 本計畫對應 | 狀態 |
|------|------|------------|------|
| §1.1 | SDD 方法論 - spec.md 已完成，plan → tasks 順序正確 | spec.md 已完成並釐清，本文件為 plan.md | ✅ |
| §1.2 | 目錄結構 - 符合 SDD 目錄規範 | 所有文件放置於 `specs/features/001-basic-chart-api/` | ✅ |
| §1.2 | 測試產物 - 所有測試產物（coverage、pytest cache 等）輸出至 `.artifacts/` | pyproject.toml 已配置 `.artifacts/` 輸出路徑 | ✅ |
| §3.1 | TDD/BDD Flow - 規劃包含測試任務（先測試後實作） | Section 7 定義測試策略，Phase 2 包含測試撰寫任務 | ✅ |
| §3.2 | Observability - Section 5 已說明 logging 策略 | Section 5 完整定義 logging 策略 | ✅ |
| §5.1 | 文件一致性 - 規劃包含文件更新任務 | Phase 1 包含 contracts/ 文件產生任務 | ✅ |
| §6.1 | 不確定性處理 - 無未解決的 TODO/??? 或已記錄於 research.md | research.md 已記錄資料表 Schema 待確認事項 | ✅ |

### 3.2 條件性檢查 (🟡)

| 條款 | 觸發條件 | 要求 | 本計畫對應 | 狀態 |
|------|----------|------|------------|------|
| §1.4 | UI Impact ≠ None | UI Maturity 規劃達 L1 | Section 2 定義 UI 行為於 AC 中（L1） | ✅ |
| §3.6 | UI Impact ≠ None | AC 定義 Loading/Empty/Error 狀態 | US A-4 完整定義所有狀態 | ✅ |
| §5.2 | Python 專案 | 使用 uv 作為環境管理工具 | Section 1.2 明確使用 uv | ✅ |

### 3.3 Gate Evaluation（關卡評估）

**Gate 1: System Spec 保護**
- ✅ 本 Feature 不涉及修改 `specs/system/**`
- ✅ 新增內容僅限於 `specs/features/001-basic-chart-api/**`

**Gate 2: 測試覆蓋**
- ✅ Section 7 定義測試策略
- ✅ 包含單元測試與整合測試
- ✅ 對應所有 US 的 AC

**Gate 3: Observability**
- ✅ Section 5 定義 logging 策略
- ✅ 使用現有 `src/logger.py` 模組
- ✅ 定義 Log Event 與 Log Level

**結論**：✅ 通過所有 Gates

---

## 4. Detailed Design

### 4.1 Module: MSSQL 連線管理 (對應 US A-1, A-4)

**目標**：建立穩定的 MSSQL 連線與查詢基礎設施

**設計決策**：

| 項目 | 決策 | 理由 |
|------|------|------|
| **連線方式** | Connection Pooling | 避免每次請求建立新連線，提升效能 |
| **驅動選擇** | pyodbc | 官方支援的 MSSQL Python 驅動 |
| **連線字串** | 從 `.env` 讀取 | 敏感資訊不寫入程式碼（Constitution §6.2） |
| **錯誤處理** | Try-Except + 日誌 | 所有 DB 錯誤需記錄 (Section 5) |

**實作方式**：
```python
# src/db/connection.py
import pyodbc
import os
from src.logger import get_logger

logger = get_logger(__name__)

class DatabaseConnection:
    def __init__(self):
        self.server = os.getenv("DB_SERVER")
        self.port = os.getenv("DB_PORT")
        self.database = os.getenv("DB_DATABASE")
        self.username = os.getenv("DB_USERNAME")
        self.password = os.getenv("DB_PASSWORD")
        self.driver = os.getenv("DB_DRIVER")
        
    def get_connection(self):
        try:
            conn_str = (
                f"DRIVER={{{self.driver}}};"
                f"SERVER={self.server},{self.port};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password}"
            )
            return pyodbc.connect(conn_str)
        except pyodbc.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise
```

### 4.2 Module: 日K聚合邏輯 (對應 US A-1)

**目標**：將 1分K 資料聚合為日K OHLCV

**設計決策**：

| 項目 | 決策 | 理由 |
|------|------|------|
| **聚合位置** | 後端 Service 層 | 避免前端重複計算，減少資料傳輸量 |
| **查詢策略** | 單一 SQL GROUP BY | 利用資料庫聚合能力，效能最佳 |
| **日期處理** | 轉換為交易日 | 排除非交易日（週末、假日） |

**實作方式**：
```sql
-- 日K聚合 SQL（在 Repository 層執行）
SELECT 
    CAST(時間 AS DATE) AS trade_date,
    FIRST_VALUE(開盤價) OVER (PARTITION BY CAST(時間 AS DATE) ORDER BY 時間 ASC) AS open,
    MAX(最高價) AS high,
    MIN(最低價) AS low,
    LAST_VALUE(收盤價) OVER (PARTITION BY CAST(時間 AS DATE) ORDER BY 時間 DESC) AS close,
    SUM(成交量) AS volume
FROM [股價即時].[dbo].[1分K]
WHERE 股票代碼 = ?
  AND 時間 BETWEEN ? AND ?
GROUP BY CAST(時間 AS DATE)
ORDER BY trade_date ASC
```

**注意**：實際欄位名稱需待 Phase 0 確認後更新。

### 4.3 Module: API 端點實作 (對應 US A-1, A-4, G-2)

**目標**：提供 RESTful API，回傳標準化格式

**設計決策**：

| 項目 | 決策 | 理由 |
|------|------|------|
| **路由設計** | GET /api/v1/chart-data | RESTful 慣例，資源導向 |
| **參數驗證** | Pydantic BaseModel | FastAPI 自動驗證與文件生成 |
| **錯誤格式** | 統一 ErrorResponse 模型 | 前端可統一處理（Spec Q2） |
| **Response 格式** | ChartDataResponse 模型 | 確保向下相容（US G-2） |

**實作方式**：
```python
# src/api/chart.py
from fastapi import APIRouter, HTTPException, Query
from src.models.request_models import ChartDataRequest
from src.models.response_models import ChartDataResponse, ErrorResponse
from src.services.chart_service import ChartService
from src.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/v1", tags=["chart"])

@router.get("/chart-data", response_model=ChartDataResponse)
async def get_chart_data(
    stock_code: str = Query(..., description="股票代碼"),
    start_date: str = Query(..., description="起始日期 YYYY-MM-DD"),
    end_date: str = Query(..., description="結束日期 YYYY-MM-DD")
):
    try:
        logger.info(f"Request chart data: {stock_code}, {start_date} - {end_date}")
        service = ChartService()
        data = service.get_chart_data(stock_code, start_date, end_date)
        logger.info(f"Chart data retrieved successfully: {len(data.chart_data.dates)} data points")
        return data
    except ValueError as e:
        logger.error(f"Invalid request: {e}")
        raise HTTPException(status_code=400, detail={
            "error": {
                "code": "INVALID_DATE_RANGE",
                "message": str(e)
            }
        })
    except Exception as e:
        logger.error(f"Internal error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "系統發生錯誤，請聯繫技術支援"
            }
        })
```

### 4.4 Module: 前端圖表元件 (對應 US A-1, A-2, A-3)

**目標**：使用 TradingView Lightweight Charts 渲染 K 線圖

**設計決策**：

| 項目 | 決策 | 理由 |
|------|------|------|
| **圖表庫** | TradingView Lightweight Charts | 高效能、內建金融圖表功能 |
| **顏色配置** | 紅漲綠跌 | 符合台股慣例（Spec §7.1） |
| **狀態管理** | Vue 3 Composition API | 現代化、響應式 |
| **快取** | Memory Cache (5分鐘) | 降低 API 負載（Spec Clarifications） |
| **Loading** | 300ms 最小顯示時間 | 避免閃爍效應（Spec Clarifications） |

**實作方式**（偽碼）：
```typescript
// frontend/src/components/ChartComponent.vue
import { createChart } from 'lightweight-charts';
import { ref, onMounted } from 'vue';
import { chartApi } from '@/services/chartApi';

const chartContainer = ref(null);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  const chart = createChart(chartContainer.value, {
    width: 800,
    height: 400,
  });
  
  const candlestickSeries = chart.addCandlestickSeries({
    upColor: '#ef5350',      // 紅色（漲）
    downColor: '#26a69a',    // 綠色（跌）
    borderVisible: false,
    wickUpColor: '#ef5350',
    wickDownColor: '#26a69a',
  });
  
  try {
    const data = await chartApi.getChartData('2330', '2024-01-01', '2024-01-31');
    candlestickSeries.setData(data.chart_data.ohlc);
    
    // 300ms 最小 Loading 時間
    setTimeout(() => {
      loading.value = false;
    }, 300);
  } catch (e) {
    error.value = e.message;
    loading.value = false;
  }
});
```

---

## 5. Observability & Logging（Constitution §3.2）🔴

> **此區塊為必填**：依據憲法 §3.2，所有 plan.md MUST 說明 logging 策略。

### 5.1 本次變更是否涉及自動化流程？

- [x] **是** — 涉及後端 API 請求處理與資料庫查詢流程

### 5.2 Logging 策略

| 項目 | 說明 |
|------|------|
| **使用的 Logger 模組** | `src/logger.py`（System Context §3.3 共享模組） |
| **預期新增的 Log Event** | `api_request_start`, `api_request_end`, `api_request_error`, `db_query_start`, `db_query_end`, `db_connection_error`, `data_aggregation_start`, `data_aggregation_end` |
| **Log Level 使用方式** | • INFO：API 請求起訖、查詢成功<br>• WARNING：查詢結果為空（NO_DATA）<br>• ERROR：資料庫連線失敗、查詢錯誤、日期格式錯誤<br>• DEBUG：SQL 查詢語句、聚合邏輯細節（開發階段） |
| **是否需擴充 Log Event 定義** | 否，使用通用 Event 名稱即可 |

### 5.3 Logging 實作細節

**日誌格式（已由 `src/logger.py` 統一定義）**：
```
[YYYY-MM-DD HH:MM:SS] [LEVEL] [MODULE] MESSAGE
```

**關鍵記錄點**：

1. **API Layer** (`src/api/chart.py`)：
   ```python
   logger.info(f"[api_request_start] stock_code={stock_code}, start={start_date}, end={end_date}")
   logger.info(f"[api_request_end] status=success, data_points={len(data)}")
   logger.error(f"[api_request_error] error_code={error_code}, message={message}")
   ```

2. **Service Layer** (`src/services/chart_service.py`)：
   ```python
   logger.info(f"[data_aggregation_start] stock_code={stock_code}")
   logger.info(f"[data_aggregation_end] aggregated_days={len(daily_data)}")
   ```

3. **Repository Layer** (`src/db/stock_repository.py`)：
   ```python
   logger.debug(f"[db_query_start] SQL={sql_statement}")
   logger.info(f"[db_query_end] rows_fetched={row_count}")
   logger.error(f"[db_connection_error] error={str(e)}")
   ```

### 5.4 對應 System Design 檢查

- [x] System `flows.md` 目前為範本，M01 完成後更新（Unify Flow 階段）
- [x] System `data-model.md` 目前為範本，無 Log Event 定義需求

---

## 6. Risk Assessment

| 風險 | 可能性 | 影響 | 緩解措施 |
|------|--------|------|----------|
| **資料表 Schema 未確認** | 高 | 高 | Phase 0 優先查詢確認實際欄位名稱，若短期無法取得則使用推測 Schema 並標註待驗證 |
| **1分K 資料量過大導致聚合效能問題** | 中 | 中 | 初期使用 SQL GROUP BY 聚合，若效能不佳則考慮建立 Materialized View 或預聚合 |
| **TradingView Charts 在 Grid 模式效能問題** | 中 | 中 | M01 先實作單圖與小圖放大，Grid 模式效能優化延後至 M02 |
| **前端快取機制與資料一致性** | 低 | 低 | 5 分鐘 TTL 可接受，若需即時性可縮短或加入手動刷新 |
| **ODBC Driver 版本相容性** | 低 | 中 | 使用 ODBC Driver 18（User 已確認），若有問題可降至 Driver 17 |
| **跨時區日期處理** | 低 | 低 | 台股交易僅限台灣時區，統一使用 Asia/Taipei 或不處理時區 |

---

## 7. Test Strategy

### 7.1 測試層級與範疇

| 測試層級 | 範疇 | 工具 | 對應 US |
|----------|------|------|---------|
| **單元測試** | Service 層日K聚合邏輯 | pytest | US A-1 AC1 |
| **單元測試** | Repository 層查詢邏輯 | pytest + Mock | US A-1 AC1, US A-4 AC2 |
| **整合測試** | API 端點完整流程（含 DB） | pytest + TestClient | US A-1 AC1/AC2, US A-4 AC1/AC2, US G-2 AC1-AC5 |
| **前端單元測試** | 圖表元件渲染與狀態管理 | Vitest | US A-2 AC1/AC2/AC3, US A-3 AC1/AC2/AC3 |
| **E2E 測試**（選擇性） | 完整使用者流程 | Playwright（延後） | 所有 US |

### 7.2 測試案例設計

#### Test Group 1: 日K聚合邏輯（US A-1）

**測試檔案**：`tests/unit/test_chart_service.py`

| 測試案例 | 輸入 | 預期輸出 | 對應 AC |
|----------|------|----------|---------|
| `test_aggregate_1min_to_daily_normal` | 100 筆 1分K 資料（涵蓋 5 個交易日） | 5 筆日K，OHLCV 正確 | AC1 |
| `test_aggregate_single_day` | 1 個交易日的 1分K | 1 筆日K，open=第一根open, close=最後根close | AC1 |
| `test_aggregate_no_data` | 空查詢結果 | 空列表或拋出 NO_DATA 錯誤 | AC3 |
| `test_aggregate_incomplete_day` | 只有部分時段的 1分K（如只有上午） | 正確計算 OHLCV（不應因資料不完整而錯誤） | AC1 |

#### Test Group 2: API 錯誤處理（US A-4, G-2）

**測試檔案**：`tests/integration/test_chart_api.py`

| 測試案例 | 輸入 | 預期輸出 | 對應 AC |
|----------|------|----------|---------|
| `test_api_invalid_stock_code` | stock_code="INVALID" | 400, error_code="INVALID_STOCK_CODE" | US A-4 AC2, US G-2 AC3 |
| `test_api_invalid_date_range` | start_date > end_date | 400, error_code="INVALID_DATE_RANGE" | US A-4 AC2, US G-2 AC3 |
| `test_api_no_data` | 有效股票但日期範圍無資料 | 200, empty chart_data 或 NO_DATA 提示 | US A-1 AC3, US G-2 AC3 |
| `test_api_database_error` | Mock DB 連線失敗 | 500, error_code="INTERNAL_ERROR" | US A-4 AC2, US G-2 AC3 |
| `test_api_response_schema` | 正常請求 | Response 符合 ChartDataResponse Schema | US G-2 AC1/AC2 |

#### Test Group 3: 前端圖表渲染（US A-1, A-2）

**測試檔案**：`frontend/tests/unit/ChartComponent.spec.ts`（延後至前端實作階段）

| 測試案例 | 輸入 | 預期輸出 | 對應 AC |
|----------|------|----------|---------|
| `test_chart_renders_correctly` | Mock API 回傳 100 根 K 線 | 圖表元件渲染成功，顯示紅漲綠跌 | US A-1 AC1 |
| `test_chart_loading_state` | API 延遲 100ms 回應 | Loading 至少顯示 300ms | US A-4 AC1 |
| `test_chart_error_display` | API 回傳 500 錯誤 | 顯示錯誤訊息與重試按鈕 | US A-4 AC2 |
| `test_chart_zoom_interaction` | 模擬滑鼠滾輪事件 | 圖表縮放正常運作 | US A-2 AC1 |

### 7.3 測試數據準備

**測試資料庫**：
- 使用獨立測試環境或 Mock 資料
- 準備至少 3 檔股票的 1分K 資料（如 2330, 2317, 2454）
- 涵蓋不同情境：正常交易日、停牌日、資料缺失

**Mock 資料範例**：
```python
# tests/fixtures/mock_data.py
MOCK_1MIN_OHLC = [
    {"time": "2024-01-02 09:00:00", "open": 580, "high": 581, "low": 579, "close": 580.5, "volume": 1000},
    {"time": "2024-01-02 09:01:00", "open": 580.5, "high": 582, "low": 580, "close": 581, "volume": 1200},
    # ... 更多資料
]

EXPECTED_DAILY_OHLC = [
    {"date": "2024-01-02", "open": 580, "high": 585, "low": 578, "close": 583, "volume": 100000}
]
```

### 7.4 成功標準

- [ ] **單元測試覆蓋率** ≥ 80%（Service + Repository 層）
- [ ] **整合測試** 涵蓋所有 API 端點與錯誤情境
- [ ] **所有 AC** 都有對應的測試案例
- [ ] **CI/CD** 整合（pytest 自動執行）
- [ ] **測試產物** 輸出至 `.artifacts/`（符合 Constitution §1.2）

---

## 8. Implementation Checklist

### Phase 0: Research & Schema Confirmation（優先執行）

- [ ] **R0-1**: 查詢 `[股價即時].[dbo].[1分K]` 實際欄位名稱
  - 執行 SQL: `SELECT TOP 5 * FROM [股價即時].[dbo].[1分K]`
  - 記錄欄位名稱、型別、範例值
  - 更新 `data-model.md` 與 `research.md`
- [ ] **R0-2**: 驗證資料庫連線
  - 使用 `.env` 配置測試連線
  - 確認 ODBC Driver 18 可正常運作
  - 測試查詢效能（100 筆 1分K 查詢時間）

**產出**：`research.md` 更新（Q1 狀態改為 ✅ Resolved）

**Git Checkpoint**: `git add . && git commit -m "research: 確認資料表 Schema" && git push`

---

### Phase 1: Backend Infrastructure（後端基礎建設）

- [ ] **P1-1**: 環境設定
  - 更新 `pyproject.toml` 加入依賴套件（fastapi, uvicorn, pyodbc, pydantic）
  - 執行 `uv add fastapi uvicorn pyodbc pydantic`
  - 更新 `.env.example` 加入資料庫連線範例
- [ ] **P1-2**: 建立資料庫連線模組
  - 實作 `src/db/connection.py`
  - 實作 Connection Pooling（若需要）
  - 撰寫連線測試 `tests/unit/test_connection.py`
- [ ] **P1-3**: 建立 Repository 層
  - 實作 `src/db/stock_repository.py`
  - 實作 `query_1min_kline(stock_code, start_date, end_date)` 方法
  - 撰寫 Mock 測試 `tests/unit/test_stock_repository.py`
- [ ] **P1-4**: 建立 Pydantic 資料模型
  - 實作 `src/models/request_models.py` (ChartDataRequest)
  - 實作 `src/models/response_models.py` (ChartDataResponse, ErrorResponse)
  - 實作 `src/models/domain_models.py` (OHLCData)
- [ ] **P1-5**: 實作日K聚合邏輯
  - 實作 `src/services/chart_service.py`
  - 實作 `aggregate_to_daily(one_min_data)` 方法
  - 撰寫單元測試 `tests/unit/test_chart_service.py`
- [ ] **P1-6**: 實作 API 端點
  - 實作 `src/api/chart.py`
  - 實作 `GET /api/v1/chart-data` 端點
  - 實作錯誤處理（INVALID_STOCK_CODE, INVALID_DATE_RANGE, NO_DATA, INTERNAL_ERROR）
- [ ] **P1-7**: FastAPI 應用程式入口
  - 實作 `src/main.py`
  - 註冊 Router
  - 設定 CORS（若需要）
- [ ] **P1-8**: 整合測試
  - 撰寫 `tests/integration/test_chart_api.py`
  - 測試所有 AC（US A-1 AC1/AC2/AC3, US A-4 AC1/AC2, US G-2 AC1-AC5）
- [ ] **P1-9**: 產生 API 契約文件
  - 建立 `specs/features/001-basic-chart-api/contracts/chart-api.md`
  - 記錄 Request/Response 格式、錯誤碼、範例

**產出**：
- 可運行的 FastAPI 後端
- 所有後端單元測試與整合測試通過
- API 契約文件

**Git Checkpoint**: `git add . && git commit -m "feat: 完成後端 API 與測試 [Phase 1]" && git push`

---

### Phase 2: Frontend Chart Component（前端圖表元件）

> **注意**：M01 階段優先完成後端，前端實作可選擇性執行或延後至 M02 詳細規劃。

- [ ] **P2-1**: Vue 3 專案初始化
  - 執行 `npm create vue@latest frontend`
  - 安裝 TradingView Lightweight Charts: `npm install lightweight-charts`
  - 安裝 Axios: `npm install axios`
- [ ] **P2-2**: 建立 API 服務層
  - 實作 `frontend/src/services/chartApi.ts`
  - 實作 `getChartData(stock_code, start_date, end_date)` 方法
  - 實作 5 分鐘快取機制（Memory Cache）
- [ ] **P2-3**: 建立圖表元件
  - 實作 `frontend/src/components/ChartComponent.vue`
  - 配置 TradingView Charts 紅漲綠跌
  - 實作 Loading 狀態（300ms 最小顯示時間）
  - 實作錯誤提示與重試按鈕
- [ ] **P2-4**: 實作互動功能
  - 實作 Zoom（滑鼠滾輪）
  - 實作 Pan（拖曳）
  - 實作 Crosshair（十字線數據顯示）
- [ ] **P2-5**: 實作小圖放大功能（US A-3）
  - 實作點擊事件處理
  - 實作放大/縮小動畫（200ms, Fade + Scale）
  - 實作 ESC 或「返回」按鈕
- [ ] **P2-6**: 前端單元測試
  - 撰寫 `frontend/tests/unit/ChartComponent.spec.ts`
  - 測試圖表渲染、Loading、錯誤處理、互動操作
- [ ] **P2-7**: 整合前後端
  - 設定前端 Proxy 或 CORS
  - 測試完整使用者流程（E2E）

**產出**：
- 可運行的前端圖表應用
- 所有前端單元測試通過
- 前後端整合成功

**Git Checkpoint**: `git add . && git commit -m "feat: 完成前端圖表元件 [Phase 2]" && git push`

---

### Phase 3: Documentation & Cleanup（文件與清理）

- [ ] **P3-1**: 更新 README.md
  - 加入專案說明
  - 加入環境設定指引
  - 加入執行方式
- [ ] **P3-2**: 更新 quickstart.md
  - 補充實際執行步驟
  - 補充測試執行方式
- [ ] **P3-3**: 程式碼 Review
  - 檢查所有 TODO / FIXME
  - 檢查 Docstring 完整性
  - 檢查日誌記錄是否完整
- [ ] **P3-4**: 效能測試（選擇性）
  - 測試 100 根 K 線渲染時間（目標 < 1 秒）
  - 測試 API 回應時間（目標 < 500ms）
- [ ] **P3-5**: 準備 Unify Flow
  - 檢查是否所有 US 都已實作
  - 檢查是否所有 AC 都有對應測試
  - 檢查是否有需要更新至 System Spec 的內容

**產出**：
- 完整的專案文件
- 乾淨的程式碼
- 準備好的 Unify Flow 材料

**Git Checkpoint**: `git add . && git commit -m "docs: 完成文件與清理 [Phase 3]" && git push`

---

## 9. Appendix

### A. 參考資料

- [TradingView Lightweight Charts 文件](https://tradingview.github.io/lightweight-charts/)
- [FastAPI 官方文件](https://fastapi.tiangolo.com/)
- [pyodbc 文件](https://github.com/mkleehammer/pyodbc/wiki)
- [Vue 3 官方文件](https://vuejs.org/)
- [Pydantic 文件](https://docs.pydantic.dev/)

### B. 相關文件

- [Feature Spec](./spec.md)
- [Research Report](./research.md)
- [Data Model](./data-model.md)
- [Quick Start Guide](./quickstart.md)
- [Milestone M01 Context](../../../docs/requirements/Milestone/M01-context.md)
- [System Context](../../../.flowkit/memory/system-context.md)

### C. 決策記錄

| 日期 | 決策 | 理由 |
|------|------|------|
| 2026-02-04 | 使用 `[股價即時].[dbo].[1分K]` 作為資料來源 | User 明確指定，符合現有資料結構 |
| 2026-02-04 | 日K聚合於後端 Service 層執行 | 避免前端重複計算，減少資料傳輸量 |
| 2026-02-04 | 前端快取 5 分鐘 TTL | 平衡資料即時性與 API 負載 |
| 2026-02-04 | Loading 最小顯示時間 300ms | 避免閃爍效應，提升 UX |
| 2026-02-04 | 使用 ODBC Driver 18 | User 已提供 `.env` 配置 |
| 2026-02-04 | M01 階段優先完成後端，前端可選擇性實作 | 符合 PRD Phase 1 定義（DB + API 基礎） |

---

**Plan 版本**：1.0  
**產生日期**：2026-02-04  
**產生工具**：SpecKit Plan  
**維護者**：AI Development Team
