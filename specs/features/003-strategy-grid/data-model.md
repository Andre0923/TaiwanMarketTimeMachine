# Data Model: 003-strategy-grid（Feature Level）

> **版本**: 1.0.0  
> **建立日期**: 2026-03-02  
> **狀態**: Plan 階段定義（待 Unify Flow 合併至 `specs/system/data-model.md`）  
> **System Data Model**: `specs/system/data-model.md`（現行 System 真相）

本文件定義 M03 新增的資料實體。所有實體均為對 System data-model 的**純擴展**（不修改現有實體），將於 Feature 完成後透過 Unify Flow 合併。

---

## 新增實體

### StockEvent（事件樣本）

**用途**：`stock_events` 資料表對應的資料實體，M03 **只讀不寫**

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `stock_code` | `str` | ✅ | 股票代碼（4-10 字元，允許數字與大寫英文）|
| `event_date` | `date` | ✅ | 事件日期（交易日）|
| `event_type` | `str` | ❌ | 事件類型標籤（僅供顯示，M03 **不以此欄位篩選**）|

#### Validation Rules
- `stock_code` 符合 `^[0-9A-Z]{4,10}$`（CONFLICT-001 決策）
- `event_date` 必須為有效日期

#### Invariants
- `stock_events` 為唯讀資料（資料庫預載，M03 不提供 INSERT/UPDATE/DELETE）

---

### StrategyQueryParams（查詢條件 DTO）

**用途**：`POST /api/strategy/query` 的 Request Body

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `stock_codes` | `List[str]` | ❌（空 = 查全部）| 股票代碼清單 |
| `date_from` | `date` | ✅ | 事件日期範圍起始 |
| `date_to` | `date` | ✅ | 事件日期範圍結束 |
| `price_min` | `Decimal` | ❌ | 事件日收盤最低價（選填）|
| `price_max` | `Decimal` | ❌ | 事件日收盤最高價（選填）|
| `logic` | `QueryLogic` | ❌（預設 AND）| 條件組合邏輯（`AND` / `OR`）|

#### Validation Rules
- `stock_codes` 各代碼符合 `^[0-9A-Z]{4,10}$`
- `date_from` ≤ `date_to`，且不得超過今日
- `price_max` ≥ `price_min`（若兩者均有填）
- `logic` 為 `AND` 或 `OR` Enum（防 SQL Injection）

---

### SampleResult（單筆樣本結果）

**用途**：Grid 中每個 MiniChart 的資料單位

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `stock_code` | `str` | ✅ | 股票代碼 |
| `event_date` | `date` | ✅ | 事件日期 |
| `event_type` | `str` | ❌ | 事件類型（僅顯示用）|
| `chart_data` | `List[ChartDataPoint]` | ✅ | 事件日前後 K 線（最多 pre+post+1=31 筆）|
| `data_complete` | `bool` | ✅ | 事件前後資料是否完整（不足時為 false）|
| `event_bar_index` | `int` | ✅ | 事件日在 `chart_data[]` 的索引（0-based）|

#### Validation Rules
- `len(chart_data)` ≤ `PRE_DAYS + POST_DAYS + 1`（= 31）
- `event_bar_index` 為有效的 `chart_data[]` 索引（0 ≤ n < len(chart_data)）
- `data_complete = false` 當 `event_bar_index < PRE_DAYS`（前置資料不足）或 `len(chart_data) - event_bar_index - 1 < POST_DAYS`（後置資料不足）

#### Invariants
- `ChartDataPoint` 格式與 `specs/system/data-model.md` 定義完全相同（向後相容）

---

### GridQueryResponse（策略查詢回應）

**用途**：`POST /api/strategy/query` 的成功 Response

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `samples` | `List[SampleResult]` | ✅ | 符合條件的樣本清單（可為空陣列）|
| `total_count` | `int` | ✅ | 符合條件的樣本總數（跨所有頁）|
| `page` | `int` | ✅ | 當前頁碼（從 1 起算）|
| `total_pages` | `int` | ✅ | 總頁數（`ceil(total_count / page_size)`）|
| `page_size` | `int` | ✅ | 本次每頁最大筆數（1-100）|
| `event_window` | `dict \| None` | ❌ | **M04 預留**：`{"pre": int, "post": int}`；M03 固定 `null` |
| `horizons` | `List[int] \| None` | ❌ | **M04 預留**：累計報酬天數；M03 固定 `null` |
| `metrics` | `dict \| None` | ❌ | **M05 預留**：統計指標；M03 固定 `null` |

#### Validation Rules
- `total_pages = ceil(total_count / page_size)`（或 0 若 total_count = 0）
- `len(samples)` ≤ `page_size`
- `page` ≤ `total_pages`（或 total_pages = 0 時 page = 1）

---

## 新增 Enumerations

### QueryLogic

**用途**：條件查詢的邏輯運算符

| 值 | 說明 |
|----|------|
| `AND` | 所有條件同時滿足（預設）|
| `OR` | 任一條件滿足 |

---

## 系統常數（Business Constants）

> 這些常數在 `src/services/strategy_service.py` 中定義，M03 不提供 UI 調整。

| 常數 | 值 | 說明 |
|------|-----|------|
| `PRE_DAYS` | `20` | 事件日前幾個交易日（M04 開放 UI 調整）|
| `POST_DAYS` | `10` | 事件日後幾個交易日（M04 開放 UI 調整）|
| `DEFAULT_PAGE_SIZE` | `100` | 每頁預設最大樣本數 |

---

## 資料流示意

```
stock_events DB
    │ (SELECT * WHERE conditions)
    ▼
StockEvent（raw DB row）
    │ StrategyService._align_to_event_date()
    ▼
SampleResult（含 chart_data[] + event_bar_index）
    │ 打包
    ▼
GridQueryResponse（含分頁資訊）
    │ POST /api/strategy/query Response
    ▼
前端 MiniChart.vue（接收 SampleResult props，TradingView 渲染）
```

---

## 與 System data-model.md 的關係

| 實體 | 作用 | Unify Flow 後 |
|------|------|---------------|
| `StockEvent` | 純擴展 | 新增至 `specs/system/data-model.md §1` |
| `StrategyQueryParams` | 純擴展 | 新增至 `specs/system/data-model.md §1` |
| `SampleResult` | 純擴展 | 新增至 `specs/system/data-model.md §1` |
| `GridQueryResponse` | 純擴展 | 新增至 `specs/system/data-model.md §1` |
| `QueryLogic` | 純擴展 | 新增至 `specs/system/data-model.md §2` |
| `ChartDataPoint` | **不修改**（延用）| 無需更新 |
| `ErrorResponse` | **不修改**（延用）| 在 ErrorCode 新增 `INVALID_QUERY_LOGIC`, `INVALID_PRICE_RANGE`, `INVALID_PAGE` |

---

## 版本歷史

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.0.0 | 2026-03-02 | Plan 階段初始定義。新增 StockEvent, StrategyQueryParams, SampleResult, GridQueryResponse, QueryLogic。確認 event_bar_index 欄位（R-10 決策）。 |
