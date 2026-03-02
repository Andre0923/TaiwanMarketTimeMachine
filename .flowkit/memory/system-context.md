# 🧠 專案上下文文件 (Project Context for AI)

> **Purpose**: 提供 AI 在 Feature 開發階段所需的專案全貌理解  
> **Version**: 1.0.0  
> **Last Updated**: 2026-03-02  
> **維護頻率**: 每完成一個 Feature 並執行 Unify Flow 後更新  
> **產生指令**: `flowkit.system-context`

---

## 1. 專案定位 (Project Identity)

### 1.1 一句話描述 (One-liner)

**台股時光機 (Taiwan Market Time Machine)** 是一個**視覺化事件研究平台**，協助策略研究員以互動式 K 線圖表探索台股歷史事件對股價的影響，並支援批次多圖並列比較。

### 1.2 核心價值主張

| 面向 | 價值 |
|------|------|
| **使用者** | 以直觀 Grid 多圖界面批次比對事件前後價格型態，大幅提升研究效率 |
| **開發者** | 穩定的 `ChartResponse` API 格式，向下相容設計確保前端無需頻繁調整解析邏輯 |
| **資料層** | 1 分 K 線聚合為日 K 線（OHLCV），統一從 MSSQL 資料庫取得，支援事件樣本批次查詢 |

### 1.3 目標使用者

- **策略研究員**：透過 Grid 多圖批次比較事件前後型態，進行視覺化事件研究
- **系統架構師**：使用穩定的 API 格式設計前端應用，基於契約文件開發
- **開發者**：基於 API 契約（`specs/system/contracts/chart-api.md`）擴充新功能

---

## 2. 系統架構概覽 (Architecture Overview)

### 2.1 高階架構圖

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERFACES                             │
├─────────────────────────────────────────────────────────────────────┤
│  Electron 桌面應用                  │  (未來：Web Browser)           │
│  frontend/electron/                 │                                │
│  - Vite + Vue 3 + TypeScript        │                                │
│  - TradingView Lightweight Charts   │                                │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       FRONTEND LAYER (Vue 3)                        │
├─────────────────────────────────────────────────────────────────────┤
│  Components (frontend/src/components/)                              │
│  - ChartWidget.vue     圖表小部件（含互動）                         │
│  - ChartGrid.vue       Grid 多圖並列佈局                            │
│  - ChartLoading.vue    載入狀態指示器                               │
│  - ChartError.vue      錯誤訊息顯示                                 │
│                                                                     │
│  Composables (frontend/src/composables/)                            │
│  - useChartData.ts     圖表資料取得與狀態管理                       │
│  - useChartInteraction.ts  圖表互動（縮放/平移/十字線）             │
│                                                                     │
│  Services (frontend/src/services/)                                  │
│  - API 呼叫層，呼叫後端 FastAPI                                     │
└─────────────────────────────────────────────────────────────────────┘
                                    │ HTTP REST
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       BACKEND API LAYER (FastAPI)                   │
├─────────────────────────────────────────────────────────────────────┤
│  Entry: src/main.py                                                 │
│  Routes: src/api/routes/chart.py                                    │
│  - GET /api/chart/daily                                             │
│  - (M03) GET /api/strategy/query (待實作)                           │
└─────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
        ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
        │  src/models/  │  │ src/services/ │  │   src/db/     │
        │  chart.py     │  │chart_service  │  │ connection.py │
        ├───────────────┤  │   .py         │  │stock_repo.py  │
        │ChartDataPoint │  ├───────────────┤  └───────┬───────┘
        │ChartResponse  │  │ 業務邏輯：     │          │
        │ChartMetadata  │  │ 1分K→日K聚合  │          ▼
        │ErrorResponse  │  │ 策略查詢（M03）│  ┌───────────────┐
        └───────────────┘  └───────────────┘  │  MSSQL Server │
                                              │  [股價即時]   │
                                              │  .dbo.[1分K]  │
                                              │  .stock_daily │
                                              │  .stock_events│
                                              └───────────────┘
```

### 2.2 模組邊界與職責 (Boundaries)

> ⚠️ **禁止跨越邊界**：API 層只呼叫 service，不直接存取 db；前端只呼叫 API，不直接存取後端邏輯。

| 模組 | 職責（一句話） | 擁有的資料/契約 | Public API 路徑 |
|------|----------------|-----------------|-----------------|
| `src/api/routes/` | HTTP 端點定義、請求驗證、回應格式化 | HTTP contract | `src/api/routes/chart.py` |
| `src/services/` | 業務邏輯（聚合、查詢、規則） | 聚合演算法、查詢規則 | `src/services/chart_service.py` |
| `src/models/` | Pydantic 資料模型，Request/Response DTO | 資料結構定義 | `src/models/chart.py` |
| `src/db/` | MSSQL 連線管理、SQL 查詢執行 | DB 連線、raw SQL | `src/db/stock_repository.py` |
| `src/logger.py` | 統一日誌設定（logging module） | log 格式與輸出 | `src/logger.py` |
| `frontend/src/components/` | 可重用 UI 元件（圖表/Grid/狀態） | Vue 元件 props/events | `frontend/src/components/` |
| `frontend/src/composables/` | Vue Composables（資料取得、互動邏輯） | 前端狀態機 | `frontend/src/composables/` |

### 2.3 入口點 (Entry Points)

> 🎯 **開發時從這裡開始找**

| 類型 | 路徑 | 說明 |
|------|------|------|
| **後端主程式** | `src/main.py` | FastAPI app 初始化，router 掛載 |
| **API 端點** | `src/api/routes/chart.py` | `GET /api/chart/daily` 唯一現行端點 |
| **業務核心** | `src/services/chart_service.py` | 1分K→日K聚合 `_aggregate_to_daily()` |
| **資料庫** | `src/db/stock_repository.py` | SQL 查詢執行，MSSQL 連線 |
| **前端 App** | `frontend/src/App.vue` | Vue 應用根元件 |
| **圖表元件** | `frontend/src/components/ChartWidget.vue` | 單一圖表互動元件 |
| **Grid 元件** | `frontend/src/components/ChartGrid.vue` | 多圖並列佈局 |
| **資料取得** | `frontend/src/composables/useChartData.ts` | 前端狀態管理（idle/loading/success/error） |

---

## 3. Feature 清單 (Feature Registry)

| Feature ID | 名稱 | 狀態 | 核心能力 | 文件位置 |
|------------|------|------|----------|----------|
| 001-basic-chart-api | 基礎圖表 API | ✅ Unified (Archived) | 日K線查詢API、1分K聚合、ChartResponse格式 | `specs/history/001-basic-chart-api/` |
| 002-frontend-chart-interactions | 前端圖表互動 | ✅ Unified (Archived) | Grid多圖並列、縮放/平移/十字線、載入/錯誤狀態 | `specs/history/002-frontend-chart-interactions/` |
| 003-strategy-grid | Strategy Grid 核心 | 🟡 Draft (In Progress) | 結構化條件查詢、Grid批次渲染(最多100圖)、事件日置中對齊、分頁 | `specs/features/003-strategy-grid/` |

### 003-strategy-grid 核心能力摘要

- **US B-1**：結構化條件查詢（股票代碼 4-10 字元、日期範圍、價格範圍、AND/OR 邏輯、前端即時驗證）
- **US B-2**：Grid 多圖並列（預設 4×5、最多 100 個小圖、3 秒內渲染 50 圖）
- **US B-3**：事件日置中對齊（pre=20 交易日、post=10 交易日，系統常數）
- **US B-4**：分頁（每頁 100 筆，分頁導航顯示頁次/總數）

---

## 4. 資料模型摘要 (Data Model Summary)

> 完整定義見：`specs/system/data-model.md`

### 4.1 已定案實體（System Spec v0.3.0）

| Entity | 用途 | 核心欄位 |
|--------|------|----------|
| `ChartDataPoint` | 單一交易日 OHLCV | time, open, high, low, close, volume |
| `ChartResponse` | 圖表查詢 API 回應 | stock_code, chart_data[], metadata |
| `ChartMetadata` | 查詢結果元資料 | stock_code, start_date, end_date, data_points |
| `ErrorResponse` | 統一錯誤格式 | code, message, details |

### 4.2 M03 新增實體（Feature 003 spec，尚未 Unified）

| Entity | 用途 | 核心欄位 |
|--------|------|----------|
| `StockEvent` | 事件樣本（唯讀，DB 預載） | stock_code, event_date, event_type（僅供顯示）|
| `StrategyQueryParams` | 查詢條件 DTO | stock_codes[], date_from, date_to, price_min, price_max, logic(AND/OR) |
| `GridQueryResponse` | 策略查詢回應 | samples[], total_count, page, total_pages, page_size |
| `SampleResult` | 單筆樣本結果 | stock_code, event_date, chart_data[], data_complete |

### 4.3 重要驗證規則

| 規則 | 說明 |
|------|------|
| `stock_code` 格式 | 4-10 字元，允許數字與大寫英文（已於 CONFLICT-001 決策，涵蓋 ETF 如 006208）|
| OHLC 關係 | `high` ≥ `max(open, close)` ≥ `low` |
| 日期格式 | ISO 8601 (YYYY-MM-DD) |
| 日期範圍 | `start_date` ≤ `end_date`，不接受未來日期 |
| 無資料 | 回傳空 `chart_data[]`，`data_points=0`，HTTP 200（非錯誤）|

---

## 5. 核心流程 (Core Flows)

> `specs/system/flows.md` 尚未定義正式流程，以下為從程式碼與 spec 推導的實際流程。

### Flow 1: 日 K 線查詢 API 流程

```
前端 ChartWidget
     │
     ▼ GET /api/chart/daily?stock_code=2330&start_date=...&end_date=...
[src/api/routes/chart.py]
     │ 1. 驗證參數（Pydantic）
     │ 2. 呼叫 chart_service
     ▼
[src/services/chart_service.py]
     │ 3. 呼叫 stock_repository 取 1分K
     │ 4. _aggregate_to_daily() 聚合
     │ 5. 建構 ChartResponse
     ▼
[src/db/stock_repository.py]
     │ SQL: SELECT FROM [股價即時].[dbo].[1分K]
     ▼
MSSQL Server → 回傳 raw 1分K rows
     ▼
回傳 ChartResponse JSON → 前端渲染
```

### Flow 2: 前端圖表互動流程

```
useChartData.ts         useChartInteraction.ts
      │                        │
      ▼ fetchChartData()        ▼ 滑鼠/鍵盤事件
  狀態: loading           縮放 / 平移 / 十字線
      │                  TradingView API 直接操控
      ▼ success / error
  ChartWidget.vue 渲染
      ├── ChartLoading.vue（載入中）
      ├── ChartError.vue（失敗 + 重試）
      └── TradingView Chart（成功）
```

### Flow 3: M03 策略 Grid 查詢流程（待實作）

```
QueryPanel（前端）
     │ 1. 前端即時驗證條件格式（AC5）
     │ 2. 提交 StrategyQueryParams
     ▼ POST /api/strategy/query（待定義）
[未來 src/api/routes/strategy.py]
     │ 3. 查詢 stock_events（DB）
     │ 4. 篩選條件（AND/OR 邏輯）
     │ 5. 取每筆事件的 pre=20 / post=10 K線
     │ 6. 建構 GridQueryResponse（分頁）
     ▼
ChartGrid.vue 渲染
     │ 每個 SampleResult → MiniChart（事件日置中）
     └── 分頁導航顯示 page / total_pages
```

---

## 5.5 UI 設計摘要 (UI Design Summary)

> `specs/system/ui/ui-structure.md` 與 `ux-guidelines.md` 目前為**範本架構（尚未填入實際內容）**。  
> 具體 UI 規格定義在各 Feature spec.md 的「UI/UX 影響評估」區塊。

### 已確認的畫面與元件

| UI ID（Feature 規格） | 類型 | 說明 | 狀態 |
|-----------------------|------|------|------|
| UI-SCR-001 | Screen | 主圖表檢視畫面（單一 K 線圖 + 互動） | M02 實作 |
| UI-SCR-002（M03 TBD） | Screen | Strategy Grid View — QueryPanel 固定頂部，Grid 多圖區在下 | M03 待實作 |
| UI-CMP-001 | Component | ChartWidget — 含 OHLCV 顯示、縮放/平移/十字線 | M02 實作 |
| UI-CMP-002（M03 TBD） | Component | QueryPanel — 條件查詢輸入，前端即時驗證 | M03 待實作 |
| UI-CMP-003（M03 TBD） | Component | MiniChart — Grid 小圖，事件日置中版 | M03 待實作 |
| UI-STATE-001 | State | Loading Pattern（Spinner） | M02 實作 |
| UI-STATE-002 | State | Empty Pattern（無資料提示） | 部分實作 |
| UI-STATE-003 | State | Error Pattern（錯誤訊息 + 重試） | M02 實作 |

### 圖表載入狀態機（ChartLoadingState）

```
idle → loading → success
              ↘ error → (重試) → loading
```

---

## 6. 技術棧與約定 (Tech Stack & Conventions)

### 6.1 技術棧

| 層次 | 技術 | 版本 | 說明 |
|------|------|------|------|
| 後端框架 | FastAPI | ≥0.128.0 | 非同步 REST API |
| 資料驗證 | Pydantic | ≥2.12.5 | Request/Response schema |
| 資料庫驅動 | pyodbc | ≥5.3.0 | MSSQL 連線 |
| ASGI 伺服器 | uvicorn | ≥0.40.0 | 開發/生產環境 |
| 測試框架 | pytest | ≥7.4.0 | 單元 + 整合測試 |
| 測試覆蓋率 | pytest-cov | ≥4.1.0 | 輸出至 `.artifacts/` |
| Python 環境 | **uv** | latest | 唯一環境管理工具 |
| 前端框架 | Vue 3 | - | Options API / Composition API |
| 圖表庫 | TradingView Lightweight Charts | - | K 線/成交量渲染 |
| 桌面應用 | Electron | - | 跨平台桌面封裝 |
| 前端建置 | Vite | - | 快速建置 |
| 程式語言 | TypeScript | - | 前端強型別 |

### 6.2 NON-NEGOTIABLE 強制規範

> 🔴 以下規範**絕對不可違反**：

| 規範 | 說明 |
|------|------|
| **環境管理** | 使用 `uv` 管理 Python 環境；**禁止** pip / conda / poetry / pipenv |
| **日誌輸出** | 使用 `logging` 模組，**禁止** `print` 作為日誌；日誌寫入 `logs/` |
| **日誌命名** | `logs/YYYYMMDD_HHMMSS.log` |
| **測試產物** | coverage / pytest cache 必須輸出至 `.artifacts/`；**禁止** 輸出至 `tests/` 或根目錄 |
| **System Spec 保護** | **絕對不可**直接修改 `specs/system/**`；唯一修改通道為 Unify Flow |
| **Test-First** | 先從 AC 衍生測試，再改 `src/` 程式碼 |
| **向下相容性** | API 既有欄位的資料型別與語意**不得改變** |
| **錯誤碼** | 只能使用預定義錯誤碼：INVALID_STOCK_CODE / INVALID_DATE_RANGE / INVALID_DATE_FORMAT / NO_DATA / DATABASE_ERROR / INTERNAL_ERROR |
| **回應格式** | 錯誤回應必須使用 `ErrorResponse` 模型，結構為 `{"detail": {"error": {...}}}` |

### 6.3 資料庫命名約定

| 物件 | 命名 |
|------|------|
| 1 分 K 資料 | `[股價即時].[dbo].[1分K]` |
| 日 K 資料（M03） | `stock_daily` |
| 事件資料（M03） | `stock_events`（唯讀，DB 預載，M03 不負責建立）|

---

## 7. Where-to-Look 查找表 (Navigation Guide)

| 情境 | 優先查找位置 | 補充查找 |
|------|-------------|----------|
| 了解 API 格式、欄位定義 | `specs/system/contracts/chart-api.md` | `src/models/chart.py` |
| 修改 API 端點邏輯 | `src/api/routes/chart.py` | `src/services/chart_service.py` |
| 修改聚合演算法 | `src/services/chart_service.py` | `specs/system/spec.md §3.3` |
| 了解資料庫 Schema | `src/db/stock_repository.py` | `specs/system/data-model.md` |
| 修改前端圖表元件 | `frontend/src/components/ChartWidget.vue` | `useChartData.ts` |
| 修改 Grid 佈局 | `frontend/src/components/ChartGrid.vue` | `specs/features/003-strategy-grid/spec.md §US B-2` |
| 了解 M03 需求 | `specs/features/003-strategy-grid/spec.md` | `specs/features/003-strategy-grid/spec-delta-log.md` |
| 確認錯誤碼定義 | `specs/system/spec.md §5` | `src/models/chart.py` |
| 了解 UI 狀態規則 | `specs/system/spec.md §3.4` | `frontend/src/composables/useChartData.ts` |
| 查看已歸檔功能細節 | `specs/history/001-basic-chart-api/` | `specs/history/002-frontend-chart-interactions/` |
| 了解測試結構 | `tests/unit/` | `tests/integration/` |
| 設計決策/衝突記錄 | `specs/features/003-strategy-grid/spec-delta-log.md` | `docs/requirements/Milestone/M03-context.md` |

---

## 8. 深入探索指引 (Deep Dive Index)

> 只放路徑索引。需要時按情境查閱。

### 8.1 規格文件

| 文件 | 路徑 |
|------|------|
| System Spec（行為真相）| `specs/system/spec.md` |
| Data Model（資料模型）| `specs/system/data-model.md` |
| Core Flows（系統流程）| `specs/system/flows.md` |
| Chart API 契約 | `specs/system/contracts/chart-api.md` |
| UI 畫面結構 | `specs/system/ui/ui-structure.md` |
| UX 指引 | `specs/system/ui/ux-guidelines.md` |

### 8.2 Feature 文件

| 文件 | 路徑 |
|------|------|
| 001 歸檔（基礎 API）| `specs/history/001-basic-chart-api/` |
| 002 歸檔（前端互動）| `specs/history/002-frontend-chart-interactions/` |
| 003 規格（Strategy Grid） | `specs/features/003-strategy-grid/spec.md` |
| 003 規格差異記錄 | `specs/features/003-strategy-grid/spec-delta-log.md` |

### 8.3 需求文件

| 文件 | 路徑 |
|------|------|
| PRD | `docs/requirements/PRD-ASSRP.md` |
| User Stories README | `docs/requirements/user-stories/README.md` |
| M03 Context | `docs/requirements/Milestone/M03-context.md` |
| Milestone README | `docs/requirements/Milestone/README.md` |

### 8.4 技術文件

| 文件 | 路徑 |
|------|------|
| 技術債清單 | `docs/technical-debt.md` |
| 目錄結構規範 | `docs/00.目錄結構.md` |
| FlowKit 功能說明 | `docs/77.flowkit相關文件/` |
| SDD 開發規範 | `docs/01.開發人員doc/03.SDD開發流程指南.md` |

---

## 9. AI 開發提示 (AI Development Hints)

### 9.1 常見陷阱 (Known Pitfalls)

> 🔴 這些是已知會出錯的地方，請**優先注意**：

1. **stock_code 驗證規則與 System Spec 不一致**
   - `specs/system/data-model.md` 記載「4 位數字」，但 `contracts/chart-api.md` 與 Feature 003 已決策採用「4-10 字元，允許數字與大寫英文」。
   - System Spec 待下一次 Unify Flow 更新。**請以較寬鬆規則（4-10 字元）為準。**

2. **`NO_DATA` 不是錯誤**
   - 查無資料時 HTTP 狀態碼為 **200**，`chart_data` 為空陣列，不應回傳 404 或 400。

3. **日誌不可用 print**
   - 所有 debug/info/error 輸出必須透過 `logging`，並寫入 `logs/`。

4. **不可直接修改 `specs/system/`**
   - 即使在修 Bug，也不應直接改 System Spec；需走 Unify Flow 或 Bug Fix 後補測試。

5. **測試產物目錄**
   - pytest coverage 輸出必須在 `.artifacts/`，不可讓它出現在 `tests/` 或 `htmlcov/`。

6. **前端狀態機**
   - `ChartLoadingState` 有 4 個狀態：`idle | loading | success | error`。新增功能時不要破壞此狀態轉換。

7. **M03 `stock_events` 唯讀**
   - `stock_events` 由 DB 預載，M03 只查詢不修改；不要加入 INSERT/UPDATE/DELETE 功能。

8. **M03 pre/post 為系統常數**
   - 事件前 20 交易日、事件後 10 交易日是系統常數，UI 不提供調整介面（M04 才開放）。

### 9.2 開發 Checklist

每次實作 Feature 時確認：

- [ ] 先從 AC 衍生測試（Test-First），才修改 `src/`
- [ ] 新增的 Pydantic 模型符合 `data-model.md` 定義
- [ ] API 端點回應格式符合 `ChartResponse` 或 `ErrorResponse` 規範
- [ ] 日誌使用 `logging` 模組，不用 `print`
- [ ] 測試透過，覆蓋率未下降
- [ ] 不修改 `specs/system/**`（System Spec 保護）
- [ ] 若涉及 UI，確認 UI 狀態（Loading/Empty/Error）有處理
- [ ] 依 `stock_code` 新規則驗證（4-10 字元，允許大寫英文）

### 9.3 M03 開發注意事項

- 003-strategy-grid spec 包含 **Clarifications 區塊**，請先閱讀：`specs/features/003-strategy-grid/spec.md` Clarifications 章節
- **spec-delta-log.md** 記錄 5 筆規格差異（D1-D5），含正式決策結果
- `event_type` **不可作為查詢條件**（Out of Scope）
- QueryPanel 配置：固定頂部，查詢條件區在上，Grid 多圖區在下
- M03 API 路徑尚未最終定案，建議先討論再實作

---

## 10. 版本歷史 (Version History)

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.0.0 | 2026-03-02 | 初始建立。專案狀態：M01/M02 已完成並 Unified，M03 (003-strategy-grid) 正在 Draft 階段，spec-delta-log 包含 5 筆規格差異紀錄（D1-D5）。 |

---

## 附錄 A：精簡索引版（供自動注入）

> 精簡版正文見：`.flowkit/memory/system-context-index.md`
