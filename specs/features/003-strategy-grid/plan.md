# Implementation Plan: Strategy Grid 核心

> **Feature ID**: 003-strategy-grid  
> **Plan Version**: 1.0  
> **Created**: 2026-03-02  
> **Spec Reference**: [spec.md](./spec.md)  
> **Research Reference**: [research.md](./research.md)  
> **Milestone**: M03

---

## 1. Technical Context

### 1.1 Current State Analysis

| 組件 | 現狀 | 目標狀態 | 落差等級 |
|------|------|----------|----------|
| 後端策略查詢 | 不存在（僅有 `GET /api/chart/daily`） | `POST /api/strategy/query`，支援條件查詢 + 分頁 | CRITICAL |
| DB 查詢層 | `StockRepository`（只查 1分K） | 新增 `StrategyRepository`，查 `stock_events` + `stock_daily` | CRITICAL |
| 前端查詢介面 | 不存在 | `QueryPanel.vue`（[UI-CMP-002]）含即時驗證 | CRITICAL |
| 前端 Grid 多圖 | `ChartGrid.vue` 支援 M02 Grid（手動選股） | 整合事件日置中 MiniChart，支援自動批次渲染 | HIGH |
| MiniChart 元件 | 不存在 | `MiniChart.vue`（[UI-CMP-003]），事件日置中版小圖 | CRITICAL |
| 分頁控制 | 不存在 | 後端 Offset-based 分頁 + 前端分頁導航 UI | HIGH |
| 交易日曆計算 | 不存在 | 查 `stock_daily` DISTINCT 日期序列，計算 pre/post | HIGH |
| 資料模型 | 無 Strategy 相關 Pydantic model | `StrategyQueryParams`, `GridQueryResponse`, `SampleResult`, `StockEvent` | HIGH |

### 1.2 Technology Stack

| 項目 | 技術選擇 | 理由 |
|------|----------|------|
| 後端語言/框架 | Python + FastAPI（既有，延用）| 一致性，避免技術異構 |
| 資料驗證 | Pydantic v2（既有，延用）| 與現有 model 一致 |
| 資料庫查詢 | pyodbc + 參數化查詢（既有，延用）| SQL Injection 防護（R-07）|
| 分頁策略 | Offset-based（`page` + `page_size`）| stock_events 唯讀且有序（R-09）|
| 前端框架 | Vue 3 Composition API（既有，延用）| 與 M02 一致 |
| 前端圖表 | TradingView Lightweight Charts（既有，延用）| MiniChart 直接複用 |
| 前端驗證 | Vue 3 computed 響應式（R-06）| 不引入新套件，驗證規則簡單 |
| 測試框架 | pytest（後端）/ Vitest（前端）（既有，延用）| 一致性 |

### 1.3 Affected Files

**新增檔案**：
```
# 後端
src/models/strategy.py                          ← M03 Pydantic models
src/db/strategy_repository.py                   ← stock_events + stock_daily 查詢
src/services/strategy_service.py                ← 業務邏輯（條件查詢、交易日計算、資料對齊）
src/api/routes/strategy.py                      ← POST /api/strategy/query 端點

# 前端元件
frontend/src/components/QueryPanel.vue          ← [UI-CMP-002] 查詢條件輸入
frontend/src/components/MiniChart.vue           ← [UI-CMP-003] Grid 小圖（事件日置中）
frontend/src/composables/useStrategyQuery.ts    ← 策略查詢狀態管理

# 測試
tests/unit/test_strategy_service.py             ← 後端業務邏輯單元測試（US B-1/B-3/B-4）
tests/unit/test_strategy_repository.py         ← DB 查詢單元測試（mock）
tests/integration/test_strategy_api.py         ← API 整合測試

# 文件
specs/features/003-strategy-grid/data-model.md ← M03 新增實體定義（feature-level）
specs/system/contracts/strategy-query-api.md    ← POST /api/strategy/query 契約
```

**修改檔案**：
```
src/main.py                                     ← 掛載 strategy router
frontend/src/App.vue                            ← 新增 Strategy Grid 模式切換
frontend/src/components/ChartGrid.vue           ← 整合 MiniChart 事件日置中版
specs/features/003-strategy-grid/plan.md        ← 本文件
```

---

## 2. UI/UX Plan

> 本 Feature 的 UI Impact = **High**；UI Maturity Target = **L0**（spec.md 明確指定）。  
> Target L0 允許 `[UI-TBD]` markers 存在，implement 前須升至 L1。本 Plan 階段只分配 UI ID，不產生 Discovery Tasks。

### 2.1 UI Impact Summary

| 項目 | 值 |
|------|---|
| **UI Impact** | High |
| **Current Maturity** | L0（spec.md 中仍有 [UI-TBD] 標記）|
| **Target Maturity** | L0（spec.md 明確設置）|
| **說明** | L0 允許留存 [UI-TBD]；implement 指令執行前 MUST 升為 L1 |

> **M03 Plan 階段不產生 L0→L1 Discovery Tasks**（Target 本身為 L0，由 `speckit.implement` 前另行處理）。

### 2.2 UI Discovery Tasks（Target = L0，暫不執行）

> 無需在 Plan 階段產生 Discovery Tasks。  
> `speckit.implement` 執行前，需先發起 UI 定義提升至 L1，否則 Gate 不通過。

### 2.3 受影響畫面

| UI ID | 畫面名稱 | 當前 Maturity | 目標 Maturity | 變更類型 |
|-------|----------|---------------|---------------|----------|
| [UI-SCR-002] | Strategy Grid View（QueryPanel + Grid 多圖）| L0 | L0（Plan）→ L1（Implement 前）| 新增 |

### 2.4 新增 Pattern/State

| UI ID | 類型 | 說明 | 狀態 |
|-------|------|------|------|
| [UI-CMP-002] | Component | QueryPanel — 結構化條件輸入，含即時驗證 | 新增 |
| [UI-CMP-003] | Component | MiniChart — Grid 小圖，事件日置中 | 新增 |
| [UI-STATE-004] | State | Partial Data Pattern — 資料不完整小圖（US B-3 AC3）| 新增 |
| [UI-STATE-001] | State | Loading Pattern（已存在，Grid 批次渲染延用）| 延用 M02 |
| [UI-STATE-002] | State | Empty Pattern（已存在，查詢無結果延用）| 延用 M02 |
| [UI-STATE-003] | State | Error Pattern（已存在，查詢失敗延用）| 延用 M02 |

### 2.5 UI ID 分配（解析 [UI-TBD]）

以下將 spec.md 中的 `[UI-TBD]` 正式分配 UI ID：

| spec.md 中的 [UI-TBD] | 正式 UI ID | 類型 |
|-----------------------|-----------|------|
| `[UI-TBD: UI-SCR-002]` | **[UI-SCR-002]** | Screen — Strategy Grid View |
| `[UI-TBD: UI-CMP-002]` | **[UI-CMP-002]** | Component — QueryPanel |
| `[UI-TBD: UI-CMP-003]` | **[UI-CMP-003]** | Component — MiniChart |
| `[UI-TBD: Loading/Empty/Error/Partial state]` | [UI-STATE-001/002/003/004] | States |

### 2.6 UI 文件更新任務（Implement 前執行）

- [ ] 更新 `specs/system/ui/ui-structure.md`：填入 [UI-SCR-002] Strategy Grid View Screen 定義
- [ ] 更新 `specs/system/ui/ui-structure.md`：填入 [UI-CMP-002] QueryPanel + [UI-CMP-003] MiniChart 元件定義
- [ ] 更新 `specs/system/ui/ux-guidelines.md`：填入 [UI-STATE-004] Partial Data Pattern 規則
- [ ] 更新 spec.md：將所有 `[UI-TBD: UI-SCR-002]` → `[UI-SCR-002]` 等正式 ID

---

## 3. Constitution Compliance Check

> 以下為 Plan 階段必須檢查的固定清單。每次執行 Plan 時 MUST 逐條填寫狀態。

### 3.1 NON-NEGOTIABLE Requirements (🔴)

| 條款 | 要求 | 本計畫對應 | 狀態 |
|------|------|------------|------|
| §1.1 | SDD 方法論 - spec.md 已完成，plan → tasks 順序正確 | spec.md 已完成並含 Clarifications 區塊（D1-D5 已決策）；plan → tasks 順序正確 | ✅ |
| §1.2 | 目錄結構 - 符合 SDD 目錄規範 | 新增檔案皆放在 `src/`, `tests/`, `specs/features/003-*/`, `specs/system/contracts/` 正確位置 | ✅ |
| §1.2 | 測試產物 - 所有測試產物輸出至 `.artifacts/` | `pyproject.toml` 已配置 `cache_dir = ".artifacts/pytest_cache"`，coverage 目標 `.artifacts/coverage/` | ✅ |
| §3.1 | TDD/BDD Flow - 規劃包含測試任務（先測試後實作）| Section 7 Test Strategy 與 Section 8 Checklist 均規劃測試先行 | ✅ |
| §3.2 | Observability - Section 5 已說明 logging 策略 | Section 5 已完整填寫 | ✅ |
| §5.1 | 文件一致性 - 規劃包含文件更新任務 | Section 1.3 列出契約文件新增；Section 2.6 UI 文件更新任務；Section 8 Checklist 包含文件同步 | ✅ |
| §6.1 | 不確定性處理 - 無未解決的 TODO/??? 或已記錄於 research.md | research.md 記錄 10 筆決策，無殘留 NEEDS CLARIFICATION；R-03 DB schema 為實作 TODO 非規格不確定 | ✅ |

### 3.2 條件性檢查 (🟡)

| 條款 | 觸發條件 | 要求 | 本計畫對應 | 狀態 |
|------|----------|------|------------|------|
| §1.4 | UI Impact ≠ None | UI Maturity 規劃達 L1 | Target = L0（spec.md 明確設定）；Plan 記錄 L0→L1 須在 implement 前執行；Section 2.6 列出任務 | ✅ |
| §3.6 | UI Impact ≠ None | AC 定義 Loading/Empty/Error 狀態 | US B-2 AC3 定義 Grid 渲染效能；US B-1 AC4 定義 Empty；US B-3 AC3 定義 Partial；M02 已定義 Loading/Error  | ✅ |
| §5.2 | Python 專案 | 使用 uv 作為環境管理工具 | 使用 `uv add` 安裝套件，不引入新套件依賴（M03 在既有套件範圍內實作）| ✅ |

### 3.3 狀態標註說明

| 標註 | 意義 |
|------|------|
| ✅ | 符合 |
| ❌ | 不符合（需說明原因或補救措施）|
| N/A | 不適用（需說明為何不適用）|

---

## 4. Detailed Design

### 4.1 Module: 資料模型（src/models/strategy.py）對應 US B-1/B-2/B-3/B-4

**目標**：定義 M03 所有 Pydantic 模型，提供 API 請求/回應 schema

**設計決策**：

| 項目 | 決策 | 理由 |
|------|------|------|
| stock_code 驗證 | regex `^[0-9A-Z]{4,10}$` | CONFLICT-001 決策（R-01）|
| QueryLogic | `Enum("AND", "OR")` | 防止 SQL Injection（R-07）|
| event_bar_index | 加入 `SampleResult`，指定事件日在 chart_data 中的 index | 前端置中渲染需要明確的事件日位置（R-10）|
| 選填欄位 | `event_window/horizons/metrics` 為 Optional，預設 None | 向後相容，M04 填入（R-01）|

**核心 Models**：

```python
class QueryLogic(str, Enum):
    AND = "AND"
    OR = "OR"

class StrategyQueryParams(BaseModel):
    stock_codes: List[str] = []            # 空 = 查全部
    date_from: date
    date_to: date
    price_min: Optional[Decimal] = None
    price_max: Optional[Decimal] = None
    logic: QueryLogic = QueryLogic.AND

class SampleResult(BaseModel):
    stock_code: str
    event_date: date
    event_type: Optional[str] = None       # 僅顯示，非查詢條件
    chart_data: List[ChartDataPoint]       # pre+post K線，已對齊
    data_complete: bool                    # 資料是否完整
    event_bar_index: int                   # 事件日在 chart_data[] 的 index

class GridQueryResponse(BaseModel):
    samples: List[SampleResult]
    total_count: int
    page: int
    total_pages: int
    page_size: int
    event_window: Optional[dict] = None   # M04 填入：{"pre": 20, "post": 10}
    horizons: Optional[List[int]] = None  # M04 填入
    metrics: Optional[dict] = None        # M05 填入
```

---

### 4.2 Module: StrategyRepository（src/db/strategy_repository.py）對應 US B-1/B-3

**目標**：查詢 `stock_events` 與 `stock_daily` 兩張表，提供業務邏輯所需的原始資料

**設計決策**：

| 項目 | 決策 | 理由 |
|------|------|------|
| 欄位名稱 | 實作時確認（`SELECT TOP 1 * FROM stock_events/stock_daily`）| PRD 未定義精確欄名（R-03）|
| 查詢方式 | 全面參數化查詢（`pyodbc` `?` 佔位符）| 防 SQL Injection（R-07）|
| 批次策略 | 一次取所有涉及 event dates 範圍的 trading days | 避免 N+1 查詢（R-04）|

**主要方法**：

```python
class StrategyRepository:
    def query_events(
        self,
        params: StrategyQueryParams,
        page: int,
        page_size: int
    ) -> Tuple[List[StockEventRow], int]:
        """查詢符合條件的 stock_events，回傳分頁結果與 total_count"""
        ...

    def get_trading_days_range(
        self,
        start_date: date,
        end_date: date
    ) -> List[date]:
        """從 stock_daily 取 DISTINCT 交易日清單（R-04 決策）"""
        ...

    def get_daily_klines_batch(
        self,
        stock_code: str,
        start_date: date,
        end_date: date
    ) -> List[DailyKlineRow]:
        """取單一股票在指定日期範圍的日K線（複用既有邏輯）"""
        ...
```

---

### 4.3 Module: StrategyService（src/services/strategy_service.py）對應 US B-1/B-3/B-4

**目標**：核心業務邏輯—條件篩選、交易日計算、事件日置中、資料組裝

**設計決策**：

| 項目 | 決策 | 理由 |
|------|------|------|
| 交易日計算 | 查 stock_daily DISTINCT 日期序列（R-04）| 最準確，無外部依賴 |
| pre/post 常數 | `PRE_DAYS = 20`, `POST_DAYS = 10`（模組常數）| 系統常數，易於 M04 改為設定項 |
| 快取 Hook | `_cache_hook()` 空方法（R-08）| 預留 US G-1 實作位置 |
| Logging | 記錄 query_start / query_result_count / assembly_error | 符合 §3.2 |

**核心方法**：

```python
PRE_DAYS = 20
POST_DAYS = 10

class StrategyService:
    def query_grid(
        self,
        params: StrategyQueryParams,
        page: int = 1,
        page_size: int = 100
    ) -> GridQueryResponse:
        """主要查詢入口：條件篩選 → 批次取K線 → 事件日對齊 → 組裝回應"""
        ...

    def _align_to_event_date(
        self,
        stock_code: str,
        event_date: date,
        trading_days: List[date]
    ) -> Tuple[List[ChartDataPoint], int, bool]:
        """
        取 event_date 前 PRE_DAYS + 後 POST_DAYS 個交易日的 K線
        Returns: (chart_data, event_bar_index, data_complete)
        """
        ...

    def _cache_hook(self, cache_key: str) -> Optional[GridQueryResponse]:
        """TODO: M04+ 實作查詢快取（US G-1）"""
        return None
```

---

### 4.4 Module: Strategy API Route（src/api/routes/strategy.py）對應 US B-1/B-4

**目標**：定義 `POST /api/strategy/query` 端點，處理請求/回應與錯誤

**設計決策**：

| 項目 | 決策 | 理由 |
|------|------|------|
| HTTP Method | POST（body 傳複合條件）| GET query string 難以表達陣列+邏輯（R-02）|
| 分頁參數 | query params `?page=1&page_size=100` | URL 可共享，body 僅放條件（R-02）|
| 錯誤格式 | `ErrorResponse` 統一格式 | 符合 System Spec §5.2 |

**端點定義**：

```python
@router.post("/query", response_model=GridQueryResponse)
async def query_strategy_grid(
    params: StrategyQueryParams,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=100, ge=1, le=100),
    service: StrategyService = Depends(get_strategy_service)
) -> GridQueryResponse:
    ...
```

---

### 4.5 Module: QueryPanel.vue（frontend/src/components/QueryPanel.vue）對應 US B-1

**目標**：結構化條件查詢輸入介面，含即時驗證（US B-1 AC5）

**設計決策**：

| 項目 | 決策 | 理由 |
|------|------|------|
| 驗證策略 | Vue 3 `computed` 響應式即時驗證 | 不引入新套件（R-06）|
| 提交控制 | `isValid` computed 為 false 時 button disabled | 禁止無效條件提交（US B-1 AC5）|
| 佈局 | 固定頂部，QueryPanel 在上 Grid 在下 | Clarification D4 決策 |
| 邏輯切換 | AND/OR Radio Button 或 Toggle | 簡單明確 |

---

### 4.6 Module: MiniChart.vue（frontend/src/components/MiniChart.vue）對應 US B-2/B-3

**目標**：Grid 小圖元件，以 TradingView 渲染 pre+post K線，事件日置中

**設計決策**：

| 項目 | 決策 | 理由 |
|------|------|------|
| 置中機制 | 接收 `eventBarIndex`，用 TradingView `setVisibleLogicalRange()` 設定可見範圍 | 後端已計算 event_bar_index（R-10）|
| 資料不完整 | `dataComplete=false` 時顯示「資料不完整」標籤（US B-3 AC3）| [UI-STATE-004] Partial 狀態 |
| Props | `SampleResult` 對應 props：`stockCode`, `eventDate`, `chartData[]`, `dataComplete`, `eventBarIndex` | 與後端 model 對應 |

---

## 5. Observability & Logging（Constitution §3.2）🔴

> **此區塊為必填**：依據憲法 §3.2，所有 plan.md MUST 說明 logging 策略。

### 5.1 本次變更是否涉及自動化流程？

- [x] **是** — 後端 API 為自動化查詢流程

### 5.2 Logging 策略

| 項目 | 說明 |
|------|------|
| **使用的 Logger 模組** | `src/logger.py`（現有 `setup_logger(__name__)` 模式，延用 M01/M02）|
| **預期新增的 Log Event** | `strategy_query_start`（INFO）、`strategy_query_result`（INFO，含 total_count）、`strategy_assembly_error`（ERROR，含 stock_code + event_date）、`db_schema_mismatch`（WARNING，若欄名對應失敗）|
| **Log Level 使用方式** | INFO: query 開始/結束 + 結果筆數；WARNING: 資料不完整樣本；ERROR: DB 查詢失敗、組裝異常；DEBUG: 每筆樣本 pre/post 交易日計算細節 |
| **是否需擴充 Log Event 定義** | 否，延用現有 `setup_logger` 模式，`extra` dict 傳入結構化欄位 |

**log 範例**：
```python
logger.info("策略查詢開始", extra={"feature_id": "003", "page": page, "params_logic": params.logic})
logger.info("策略查詢完成", extra={"total_count": total, "page": page, "page_size": page_size})
logger.warning("樣本資料不完整", extra={"stock_code": stock_code, "event_date": event_date})
logger.error("DB 查詢失敗", extra={"error": str(e), "query": "strategy_query"})
```

### 5.3 對應 System Design 檢查

- [x] 已確認 `specs/system/flows.md` 目前為空白範本（無 logging 描述影響）
- [x] 本次變更**不影響** `specs/system/data-model.md` 的 Log Event 定義（logging 不屬於資料模型層）
- [x] 待 Unify Flow 後，`specs/system/flows.md` 應補入 Strategy Grid 查詢流程（包含 logging 節點）

---

## 6. Risk Assessment

| 風險 | 可能性 | 影響 | 緩解措施 |
|------|--------|------|----------|
| DB Schema 欄位名稱與推算不符（R-03）| 高 | 中 | 實作 `strategy_repository.py` 前先執行 `SELECT TOP 1 * FROM stock_events/stock_daily` 確認欄名，以常數管理欄位名稱 |
| `stock_events` 表無 index，查詢 100 筆慢 | 中 | 中 | 若查詢超時，請 DBA 在 `(stock_code, event_date)` 加複合索引；M03 查詢 API 設 5 秒 timeout（success criteria §1.3）|
| Grid 渲染 50 圖 > 3 秒（US B-2 AC3) | 中 | 高 | 先測試後優化；若需要用 Intersection Observer 延遲渲染 viewport 外的圖表（R-05 備案）|
| 前端 TradingView `setVisibleLogicalRange()` 置中邏輯不准確 | 低 | 高 | 單元測試驗證 event_bar_index 計算；視覺測試確認事件日確實在水平中心 |
| `stock_events` 資料稀疏，AND 條件過嚴查詢 0 筆 | 中 | 低 | US B-1 AC4 已定義空結果處理；前端 Empty Pattern（[UI-STATE-002]）顯示放寬條件建議 |
| pre/post 計算邏輯：事件日不在 stock_daily 中（假日匯入異常）| 低 | 中 | `_align_to_event_date()` SHOULD 驗證 event_date 是否在 trading_days 列表中；若不在，回傳 data_complete=false |

---

## 7. Test Strategy

### 7.1 驗證方式

| 組件 | 驗證方式 | 對應 AC |
|------|----------|---------|
| `StrategyService._align_to_event_date()` | 單元測試：pre=20/post=10 完整資料 + 資料不足邊界情況 | US B-3 AC1/AC2/AC3 |
| `StrategyService.query_grid()` | 單元測試：AND 邏輯、OR 邏輯、空結果、分頁計算 | US B-1 AC1/AC2/AC4, US B-4 AC1/AC2/AC3 |
| `StrategyRepository.query_events()` | 單元測試（mock DB）：SQL 參數化、條件組合 | US B-1 AC1/AC2 |
| `POST /api/strategy/query` | 整合測試：合法請求/無效條件/空結果/分頁 | US B-1 AC1/AC3/AC4/AC5, US B-4 |
| `QueryPanel.vue` 即時驗證 | Vitest 元件測試：無效代碼/日期反序/禁止提交 | US B-1 AC5 |
| `MiniChart.vue` 事件日置中 | Vitest 元件測試：eventBarIndex 正確傳遞 | US B-3 AC1/AC2 |
| `MiniChart.vue` 資料不完整 | Vitest 元件測試：dataComplete=false 顯示標籤 | US B-3 AC3 |
| Grid 渲染效能 | 手動測試（非自動化）：50 圖 < 3 秒 | US B-2 AC3 |

### 7.2 成功標準

- [ ] 所有後端單元測試通過，coverage ≥ 既有基準（不得下降）
- [ ] 整合測試：`POST /api/strategy/query` 各場景均回傳符合 `GridQueryResponse` 格式的 response
- [ ] 前端元件測試：QueryPanel 的即時驗證邏輯（AC5）所有路徑測試通過
- [ ] 手動驗收：50 個 MiniChart 在 3 秒內完成渲染
- [ ] 手動驗收：事件日 K 線視覺上位於每個 MiniChart 的水平中心

---

## 8. Implementation Checklist

> 以下為 speckit.tasks 將展開的完整任務清單（依序執行）。

### Phase 1: 後端資料模型與基礎

- [ ] **[TEST-FIRST]** 撰寫 `tests/unit/test_strategy_service.py`（US B-1/B-3/B-4 AC 衍生，跑 fail）
- [ ] **[TEST-FIRST]** 撰寫 `tests/unit/test_strategy_repository.py`（mock DB）
- [ ] 確認 `stock_daily`、`stock_events` 實際欄位名稱（`SELECT TOP 1 *`）
- [ ] 建立 `src/models/strategy.py`（R-01 決策：含 event_bar_index, Optional M04 欄位）
- [ ] 建立 `src/db/strategy_repository.py`（參數化查詢、白名單驗證）
- [ ] 建立 `src/services/strategy_service.py`（_align_to_event_date, _cache_hook）
- [ ] 確認後端測試全通過

### Phase 2: 後端 API 端點

- [ ] 建立 `src/api/routes/strategy.py`（`POST /api/strategy/query`）
- [ ] 修改 `src/main.py` 掛載 strategy router
- [ ] 撰寫 `tests/integration/test_strategy_api.py`
- [ ] 確認 API 整合測試通過，`ErrorResponse` 格式符合規範

### Phase 3: UI 定義升至 L1（Implement Gate）

- [ ] 更新 `specs/system/ui/ui-structure.md`：填入 [UI-SCR-002], [UI-CMP-002], [UI-CMP-003]
- [ ] 更新 `specs/system/ui/ux-guidelines.md`：填入 [UI-STATE-004] Partial Data Pattern
- [ ] 更新 `specs/features/003-strategy-grid/spec.md`：將 [UI-TBD] 全部替換為正式 UI ID
- [ ] 確認 UI Maturity 達 L1

### Phase 4: 前端元件實作

- [ ] **[TEST-FIRST]** 撰寫 `QueryPanel.vue` Vitest 測試（US B-1 AC5）
- [ ] **[TEST-FIRST]** 撰寫 `MiniChart.vue` Vitest 測試（US B-3 AC1/AC2/AC3）
- [ ] 建立 `frontend/src/components/QueryPanel.vue`（[UI-CMP-002]）
- [ ] 建立 `frontend/src/components/MiniChart.vue`（[UI-CMP-003]）
- [ ] 建立 `frontend/src/composables/useStrategyQuery.ts`
- [ ] 修改 `frontend/src/components/ChartGrid.vue` 整合 MiniChart
- [ ] 修改 `frontend/src/App.vue` 新增 Strategy Grid 模式切換（[UI-SCR-002]）
- [ ] 確認前端元件測試通過

### Phase 5: 手動驗收與文件

- [ ] 手動測試 Grid 渲染效能（50 圖 < 3 秒）
- [ ] 手動驗收事件日水平置中視覺效果
- [ ] 更新 `specs/features/003-strategy-grid/spec-delta-log.md`（記錄任何實作中新發現的差異）
- [ ] 更新 `specs/system/flows.md` 補入 Strategy Grid 查詢流程
- [ ] 更新 `docs/requirements/user-stories/README.md` US B-1~B-4 狀態
- [ ] 所有測試通過 ✅，coverage 未下降

---

## 9. Appendix

### A. 參考資料

| 文件 | 路徑 |
|------|------|
| Feature Spec | `specs/features/003-strategy-grid/spec.md` |
| Research Notes | `specs/features/003-strategy-grid/research.md` |
| Spec Delta Log | `specs/features/003-strategy-grid/spec-delta-log.md` |
| Strategy Query API 契約 | `specs/system/contracts/strategy-query-api.md` |
| M03 Feature Data Model | `specs/features/003-strategy-grid/data-model.md` |
| M03 Milestone Context | `docs/requirements/Milestone/M03-context.md` |
| System Data Model | `specs/system/data-model.md` |
| Chart API 契約 | `specs/system/contracts/chart-api.md`（向後相容參考）|
| System Context | `.flowkit/memory/system-context.md` |

### B. 決策索引（快速查找）

| 決策 | 位置 | 狀態 |
|------|------|------|
| stock_code 驗證規則 4-10 字元 | CONFLICT-001（M03-context.md） + research R-01 | ✅ 已決策 |
| M03 API Response 子集格式 | research R-01 + CONFLICT-002 | ✅ 已決策 |
| API 端點 `POST /api/strategy/query` | research R-02 | ✅ 已決策 |
| 交易日曆查 stock_daily DISTINCT | research R-04 | ✅ 已決策 |
| 後端計算 chart_data + event_bar_index | research R-10 | ✅ 已決策 |
| pre=20 / post=10 為系統常數 | spec.md Clarifications + research R-08 | ✅ 已決策 |
| stock_events 唯讀 | spec.md Clarifications D1 | ✅ 已決策 |

