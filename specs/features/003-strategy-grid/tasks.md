# Tasks: Strategy Grid 核心

> **Feature ID**: 003-strategy-grid  
> **Created**: 2026-03-02  
> **Spec Reference**: [spec.md](./spec.md)  
> **Plan Reference**: [plan.md](./plan.md)  
> **Data Model Reference**: [data-model.md](./data-model.md)  
> **API Contract**: [specs/system/contracts/strategy-query-api.md](../../system/contracts/strategy-query-api.md)

---

## Implementation Strategy

**MVP Scope**: Phase 1–5（後端完整可用）— 完成後即可透過 API 測試工具驗證所有後端 AC；前端為 Phase 6–10 增量交付。  
**Incremental Delivery**:
1. Phase 1–2：環境與資料模型就緒
2. Phase 3–5：後端 API 可獨立驗收（US B-1/B-3/B-4 AC 全通過）
3. Phase 6：UI L0→L1 Gate（前端開發前提）
4. Phase 7–10：前端逐層疊加（QueryPanel → MiniChart → Grid → 分頁）
5. Phase 11：效能驗收 + 文件完整

---

## Phase 1: Setup（環境確認與前置調查）

> **Goal**: 確認測試基礎設施就緒，透過實際查詢取得 `stock_events` 與 `stock_daily` 的真實欄位名稱
>
> **💡 提示**：執行 DB Schema 確認前，確保 MSSQL 連線可用（`.env` 設定正確、VPN 若有需要已連線）

- [ ] T001 確認 `pyproject.toml` 的測試產物輸出設定（`cache_dir = ".artifacts/pytest_cache"`，`coverage` 輸出 → `.artifacts/coverage/`，`.gitignore` 排除 `.artifacts/`）
- [ ] T002 執行 `SELECT TOP 1 * FROM stock_events` 取得實際欄位名稱（記錄確認結果，供 T008 使用；若欄名與 plan §4.2 假設不符需更新 `research.md`）
- [ ] T003 執行 `SELECT TOP 1 * FROM stock_daily` 取得實際欄位名稱（記錄確認結果，供 T009–T010 使用）

---

## Phase 2: Foundational（資料模型 + 測試骨架，所有 US 依賴）

> **Goal**: 建立 M03 Pydantic 資料模型與所有測試骨架（測試先跑 fail，驅動後續實作）
>
> **💡 Test-First 提示**：T005–T007 應先於對應 `src/` 實作完成後執行 `uv run pytest [test_file] --co -q` 確認測試案例存在且初始狀態為 FAIL

- [ ] T004 [P] 建立 `src/models/strategy.py`（含 `QueryLogic` Enum、`StrategyQueryParams`、`SampleResult`（含 `event_bar_index: int`）、`GridQueryResponse`（含 Optional M04/M05 欄位）；複用 `ChartDataPoint` from `src/models/chart.py`）
- [ ] T005 [P] 撰寫 `tests/unit/test_strategy_service.py` 測試骨架（對應 US B-1 AC1/AC2/AC4、US B-3 AC1/AC2/AC3、US B-4 AC1/AC2/AC3 衍生測試案例；初始狀態 FAIL）
- [ ] T006 [P] 撰寫 `tests/unit/test_strategy_repository.py` 測試骨架（mock DB connection；對應 `query_events` AND/OR 邏輯、空結果、`get_trading_days_range` 回傳有序日期；初始狀態 FAIL）
- [ ] T007 [P] 撰寫 `tests/integration/test_strategy_api.py` 測試骨架（依 `specs/system/contracts/strategy-query-api.md` 契約；涵蓋合法請求、無效 stock_code、date_from > date_to、空結果、分頁、INVALID_PAGE；初始狀態 FAIL）

---

## Phase 3: US B-1 — 結構化條件查詢（後端）

> **Story Goal**: 實作 `POST /api/strategy/query` 端點，支援依股票代碼、日期範圍、價格範圍、AND/OR 邏輯篩選 `stock_events`
>
> **Independent Test**: `uv run pytest tests/unit/test_strategy_repository.py tests/unit/test_strategy_service.py -k "query or logic or stock_code or empty"` → PASS；`POST /api/strategy/query` with valid body returns HTTP 200 + `GridQueryResponse` JSON

- [ ] T008 [US1] 建立 `src/db/strategy_repository.py`（含 `query_events()` 方法；白名單欄位名稱常數、全面參數化查詢、AND/OR 邏輯動態 SQL 組合；複用 `src/db/connection.py` 的 `get_db_connection()`）
- [ ] T009 [US1] 在 `src/db/strategy_repository.py` 中實作 `get_trading_days_range()`（`SELECT DISTINCT date FROM stock_daily WHERE date BETWEEN ? AND ? ORDER BY date`；回傳 `List[date]`）
- [ ] T010 [US1] 在 `src/db/strategy_repository.py` 中實作 `get_daily_klines_batch()`（取單一股票指定日期範圍日 K 線；回傳 `List[DailyKlineRow]`）
- [ ] T011 [US1] 建立 `src/services/strategy_service.py`（含 `StrategyService` + `query_grid()` 框架 + `_cache_hook()` stub + `PRE_DAYS = 20` / `POST_DAYS = 10` 模組常數 + `setup_logger(__name__)` logging）
- [ ] T012 [US1] 建立 `src/api/routes/strategy.py`（`POST /api/strategy/query` endpoint；`Depends(get_strategy_service)`；`INVALID_STOCK_CODE`、`INVALID_DATE_RANGE`、`INVALID_QUERY_LOGIC`、`INVALID_PRICE_RANGE`、`DATABASE_ERROR`、`INTERNAL_ERROR` 錯誤處理；回應使用 `ErrorResponse`）
- [ ] T013 [US1] 修改 `src/main.py`（掛載 strategy router：`app.include_router(strategy.router, prefix="/api/strategy")`）
- [ ] T014 [US1] 確認 US B-1 後端測試通過（`uv run pytest tests/unit/test_strategy_repository.py tests/integration/test_strategy_api.py -v` 全部 PASS；涵蓋 AND/OR 邏輯、stock_code 格式驗證 `^[0-9A-Z]{4,10}$`、empty result 200 回應）

---

## Phase 4: US B-3 — 事件日置中對齊（後端）

> **Story Goal**: 實作 `_align_to_event_date()` 方法，計算每筆樣本的 `chart_data`（pre=20/post=10 交易日）與 `event_bar_index`；在 `query_grid()` 中整合
>
> **Independent Test**: `uv run pytest tests/unit/test_strategy_service.py -k "align"` → PASS；包含完整資料（event_bar_index=20）、前置不足（data_complete=false, event_bar_index<20）、後置不足（data_complete=false）、event_date 不在 trading_days（data_complete=false）

- [ ] T015 [US3] 在 `src/services/strategy_service.py` 中實作 `_align_to_event_date()`（從 `trading_days` 找 `event_date` 的 index；取前 `PRE_DAYS`、後 `POST_DAYS` 的 `StockDaily` 資料；計算 `event_bar_index = PRE_DAYS`（或實際取得前置數量）；`data_complete = (pre_actual >= PRE_DAYS and post_actual >= POST_DAYS)`）
- [ ] T016 [US3] 在 `src/services/strategy_service.py` 中將 `_align_to_event_date()` 整合進 `query_grid()`（對每筆 `stock_event` 呼叫對齊；組裝 `SampleResult`；`strategy_assembly_error` WARNING log 當 exception 發生）
- [ ] T017 [US3] 確認 US B-3 後端測試通過（`uv run pytest tests/unit/test_strategy_service.py -v` 全部 PASS；`event_bar_index` 正確、`data_complete` 邊界情況全涵蓋）

---

## Phase 5: US B-4 — 查詢結果限制與分頁（後端）

> **Story Goal**: 確認 `query_grid()` 的 offset-based 分頁邏輯完整，包含 `total_pages` 計算、`INVALID_PAGE` 錯誤、分頁導航所需資訊
>
> **Independent Test**: `uv run pytest tests/unit/test_strategy_service.py -k "pagination" tests/integration/test_strategy_api.py -k "pagination"` → PASS；page=2 回傳第 2 批樣本；page > total_pages 回傳 HTTP 400 `INVALID_PAGE`

- [ ] T018 [US4] 在 `src/services/strategy_service.py` 的 `query_grid()` 中實作分頁邏輯（`OFFSET (page-1)*page_size ROWS FETCH NEXT page_size ROWS ONLY`；`total_pages = ceil(total_count / page_size)`；`page > total_pages` 時 raise `INVALID_PAGE`；`total_count = 0` 時 `total_pages = 0`, `page = 1`）
- [ ] T019 [US4] 確認 US B-4 後端單元測試通過（`uv run pytest tests/unit/test_strategy_service.py -k "pagination" -v`；單頁、多頁、page 超出 total_pages 全通過）
- [ ] T020 [US4] 確認 US B-4 後端 API 整合測試通過（`uv run pytest tests/integration/test_strategy_api.py -v`；全部場景通過，coverage 不低於進入此 Phase 前的基準）

---

## Phase 6: UI Gate — L0 → L1 升級（前端開發前提）

> **Goal**: 將 `spec.md` 中所有 `[UI-TBD: UI-xxx]` 替換為正式 UI ID，並在 System UI 文件中建立對應定義；確認 UI Maturity 達 L1 後才可開始前端實作
>
> **⚠️ Gate 條件**：Phase 7–10 的所有前端任務不得在本階段完成前開始

- [ ] T021 更新 `specs/system/ui/ui-structure.md`（新增 `[UI-SCR-002]` Strategy Grid View Screen 定義：固定頂部佈局，QueryPanel 在上 Grid 在下；新增 `[UI-CMP-002]` QueryPanel Component；新增 `[UI-CMP-003]` MiniChart Component）
- [ ] T022 更新 `specs/system/ui/ux-guidelines.md`（新增 `[UI-STATE-004]` Partial Data Pattern：`data_complete=false` 時在 MiniChart 顯示「資料不完整」文字標籤）
- [ ] T023 更新 `specs/features/003-strategy-grid/spec.md`（將所有 `[UI-TBD: UI-SCR-002]` → `[UI-SCR-002]`；`[UI-TBD: UI-CMP-002]` → `[UI-CMP-002]`；`[UI-TBD: UI-CMP-003]` → `[UI-CMP-003]`；`[UI-TBD: Loading/Empty/Error/Partial state]` → `[UI-STATE-001/002/003/004]`）
- [ ] T024 確認 `spec.md` 中無殘留 `[UI-TBD]` 標記（`grep -n "UI-TBD" spec.md` 輸出為空 = UI Maturity L1 達成）

---

## Phase 7: US B-1 前端 — QueryPanel 條件查詢介面

> **Story Goal**: 前端結構化條件輸入介面，含即時驗證（AC5），使用者可提交查詢並觸發 API 呼叫
>
> **Independent Test**: `pnpm vitest run --reporter=verbose` QueryPanel 測試全通過；輸入無效 stock_code `12345678901` → 提交按鈕 disabled；`date_from > date_to` → 欄位旁錯誤提示見；有效輸入 → 可提交

- [ ] T025 [TEST-FIRST] [P] [US1] 撰寫 `frontend/src/components/__tests__/QueryPanel.test.ts`（Vitest 元件測試；涵蓋：股票代碼長度 > 10 字元時 submit disabled [AC5]、date_from > date_to 時 submit disabled [AC5]、price_max < price_min 時 submit disabled [AC5]、AND/OR 切換狀態正確、有效條件時 submit 按鈕 enabled；初始狀態 FAIL）
- [ ] T026 [US1] 建立 `frontend/src/components/QueryPanel.vue`（`stock_codes`/`date_from`/`date_to`/`price_min`/`price_max`/`logic` 輸入；Vue 3 `computed` 即時驗證（無需新套件）；`isValid` computed 為 false 時按鈕 disabled；欄位旁錯誤提示；emit `submit` event with `StrategyQueryParams`）
- [ ] T027 [US1] 建立 `frontend/src/composables/useStrategyQuery.ts`（`idle` / `loading` / `success` / `error` 狀態機；`execute(params, page)` 函式呼叫 `POST /api/strategy/query`；`currentPage` / `totalPages` / `totalCount` 分頁狀態；`GridQueryResponse` 回應型別）
- [ ] T028 [US1] 確認 QueryPanel.vue Vitest 測試全通過（`pnpm vitest run QueryPanel` → PASS）

---

## Phase 8: US B-3 前端 — MiniChart 事件日置中

> **Story Goal**: 建立 MiniChart 元件，接收 `SampleResult` props，以 TradingView `setVisibleLogicalRange()` 實現事件日水平置中，並處理 Partial 資料狀態 [UI-STATE-004]
>
> **Independent Test**: `pnpm vitest run MiniChart` → 全通過；`eventBarIndex=5` 時 `setVisibleLogicalRange` 被呼叫的參數起點 < 5；`dataComplete=false` 時 DOM 中存在「資料不完整」文字

- [ ] T029 [TEST-FIRST] [P] [US3] 撰寫 `frontend/src/components/__tests__/MiniChart.test.ts`（Vitest 元件測試；涵蓋：`eventBarIndex` 傳入後 TradingView `setVisibleLogicalRange` 被呼叫且範圍正確置中 [AC1]；`dataComplete=false` 時渲染「資料不完整」標籤 [UI-STATE-004] [AC3]；`stockCode` 與 `eventDate` 標籤可見 [US B-2 AC4]；初始狀態 FAIL）
- [ ] T030 [US3] 建立 `frontend/src/components/MiniChart.vue`（Props：`stockCode`, `eventDate`, `chartData`, `dataComplete`, `eventBarIndex`；TradingView Lightweight Charts 初始化日 K 線；`chart.timeScale().setVisibleLogicalRange({ from: eventBarIndex - PRE_DAYS, to: eventBarIndex + POST_DAYS })`；`dataComplete=false` 時顯示 `[UI-STATE-004]` 半透明「資料不完整」覆蓋層；顯示 `stockCode` + `eventDate` 標籤）
- [ ] T031 [US3] 確認 MiniChart.vue Vitest 測試全通過（`pnpm vitest run MiniChart` → PASS）

---

## Phase 9: US B-2 前端 — Grid 多圖並列

> **Story Goal**: ChartGrid.vue 整合 MiniChart，支援 SampleResult[] 批次渲染 4×5 Grid，App.vue 新增 Strategy Grid 模式切換 [UI-SCR-002]；每個小圖顯示 stock_code + event_date 標籤
>
> **Independent Test**: `pnpm vitest run ChartGrid` → 全通過；傳入 20 個 `SampleResult` mock → 渲染 20 個 MiniChart 元件；App.vue 模式切換顯示 QueryPanel + ChartGrid 組合

- [ ] T032 [TEST-FIRST] [P] [US2] 撰寫 `frontend/src/components/__tests__/ChartGrid.strategy.test.ts`（Vitest；傳入 `SampleResult[]` → 渲染對應數量的 MiniChart；Grid 4 欄佈局 CSS class 存在；空陣列 → 顯示 Empty Pattern [UI-STATE-002]；初始狀態 FAIL）
- [ ] T033 [US2] 修改 `frontend/src/components/ChartGrid.vue`（新增 `samples: SampleResult[]` prop（選填）；當 `samples` 存在時以 Grid 4 欄自動換列佈局渲染 MiniChart 陣列；維持現有 M01/M02 StockCode 選股模式不受影響）
- [ ] T034 [US2] 修改 `frontend/src/App.vue`（新增 Strategy Grid 模式頁籤/切換按鈕（[UI-SCR-002]）；固定頂部佈局：QueryPanel 在上，ChartGrid 在下；`useStrategyQuery` composable 串接 QueryPanel submit event → ChartGrid samples 更新）
- [ ] T035 [US2] 確認 ChartGrid Grid 模式 Vitest 測試全通過（`pnpm vitest run ChartGrid.strategy` → PASS）

---

## Phase 10: US B-4 前端 — 分頁導航 UI

> **Story Goal**: ChartGrid.vue / App.vue 加入分頁導航（「第 X / Y 頁，共 N 筆樣本」顯示 + 上/下一頁按鈕），切換頁碼時重新呼叫 API
>
> **Independent Test**: `pnpm vitest run` 分頁 UI 相關測試全通過；`currentPage=2, totalPages=5` → 顯示「第 2 / 5 頁」；點擊「下一頁」→ `useStrategyQuery.execute` 以 `page=3` 被呼叫

- [ ] T036 [US4] 在 `frontend/src/App.vue` 或 `ChartGrid.vue` 中新增分頁導航 UI（「第 {{currentPage}} / {{totalPages}} 頁，共 {{totalCount}} 筆樣本」文字；「上一頁」/ 「下一頁」按鈕；`currentPage=1` 時上一頁 disabled；`currentPage=totalPages` 時下一頁 disabled）
- [ ] T037 [US4] 將分頁按鈕事件接線至 `useStrategyQuery.ts`（點擊上/下一頁 → 呼叫 `execute(lastParams, newPage)` → 觸發 `POST /api/strategy/query?page=newPage` → `samples` 更新 → ChartGrid 重新渲染）
- [ ] T038 [US4] 確認分頁 UI 行為測試通過（`pnpm vitest run` 分頁相關 test 全 PASS；第 1 頁上一頁按鈕 disabled；`total_pages=1` 時兩個按鈕均 disabled）

---

## Phase 11: Polish & 驗收

> **Goal**: 效能驗收、手動驗收、文件同步收尾

- [ ] T039 手動測試 Grid 渲染效能（造出 50 個 `SampleResult` mock → 計時 Grid 從載入到 50 個 MiniChart 全部可見；目標 < 3 秒 [US B-2 AC3]；若超時，評估 Intersection Observer 懶載入可行性）
- [ ] T040 手動驗收事件日水平置中視覺效果（抽查 5 個以上不同 `eventBarIndex` 的 MiniChart，確認事件日 K 線視覺上位於圖表水平中心 [US B-3 AC1]）
- [ ] T041 更新 `specs/features/003-strategy-grid/spec-delta-log.md`（記錄實作過程中發現的任何 Spec 差異，尤其是 DB Schema 欄名 [T002/T003 結果]、`_align_to_event_date` 邊界行為等）
- [ ] T042 更新 `specs/system/flows.md`（補入 Strategy Grid 查詢流程：QueryPanel submit → POST /api/strategy/query → StrategyService → _align_to_event_date → GridQueryResponse → ChartGrid render MiniChart）
- [ ] T043 更新 `docs/requirements/user-stories/README.md`（US B-1~B-4 狀態同步；統計數字更新）
- [ ] T044 確認所有測試通過且 coverage 未下降（`uv run pytest --cov=src --cov-report=html:.artifacts/coverage` + `pnpm vitest run` 全部 PASS；與進入 Phase 1 前的 coverage 基準比較不下降）

---

## Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational: 資料模型 + 測試骨架)
    │
    ├──────────────────────────────────────────────────┐
    ▼                                                  │
Phase 3 (US B-1 後端: 查詢 + API)                      │（前端需等 Phase 6 Gate）
    │                                                  │
    ▼                                                  │
Phase 4 (US B-3 後端: 事件日對齊)                      │
    │                                                  │
    ▼                                                  │
Phase 5 (US B-4 後端: 分頁邏輯)                        │
    │                                                  │
    ▼                                                  │
Phase 6 (UI Gate L0→L1) ──────────────────────────────┘
    │
    ▼
Phase 7 (US B-1 前端: QueryPanel)
    │
    ▼
Phase 8 (US B-3 前端: MiniChart)
    │
    ▼
Phase 9 (US B-2 前端: Grid 整合) ← MiniChart 必須先完成
    │
    ▼
Phase 10 (US B-4 前端: 分頁 UI)
    │
    ▼
Phase 11 (Polish & 驗收)
```

**Phase 相依規則：**
- Phase 4 依賴 Phase 3（`_align_to_event_date` 整合進 `query_grid`，需先有 service 框架）
- Phase 5 依賴 Phase 3（分頁邏輯在同一 `query_grid` 方法）
- Phase 7–10 全部依賴 Phase 6（UI Gate）
- Phase 9 依賴 Phase 8（ChartGrid 使用 MiniChart 元件）

---

## Parallel Execution Opportunities

### Phase 2：4 個任務可全部平行（不同檔案）

```
T004 (src/models/strategy.py) ──────┐
T005 (tests/unit/test_service.py) ──┼── 可同時執行（4 個不同檔案）
T006 (tests/unit/test_repository.py)┤
T007 (tests/integration/test_api.py)┘
```

### Phase 7–8 跨階段平行

```
Phase 7 在前：
  T025 (寫 QueryPanel 測試)  ←── TEST-FIRST，先寫測試
  T026 (實作 QueryPanel.vue) 

Phase 8 開始後，T029（寫 MiniChart 測試）可以和 Phase 7 的 T027/T028 平行：
  T027 (實作 useStrategyQuery.ts) ──┬── 不同檔案，可平行
  T029 (寫 MiniChart 測試) ─────────┘
```

### Phase 9：T032（寫 ChartGrid 測試）可以和 Phase 8 的 T030/T031 平行

```
T030 (實作 MiniChart.vue) ──┬── 不同檔案，可平行
T032 (寫 ChartGrid 測試) ───┘
```

---

## Summary

| 指標 | 數值 |
|------|------|
| **總任務數** | 44 |
| **可平行任務 [P]** | 7（T004, T005, T006, T007, T025, T029, T032）|
| **TEST-FIRST 任務** | 6（T005, T006, T007, T025, T029, T032）|
| **US B-1 任務數** | 12（T008–T014, T025–T028）|
| **US B-2 任務數** | 4（T032–T035）|
| **US B-3 任務數** | 6（T015–T017, T029–T031）|
| **US B-4 任務數** | 6（T018–T020, T036–T038）|
| **Setup/Foundational 任務數** | 7（T001–T007）|
| **UI Gate 任務數** | 4（T021–T024）|
| **Polish 任務數** | 6（T039–T044）|
| **建議 MVP 範圍** | Phase 1–6（後端 API 完整可用 + UI Gate）|

---

## User Story 標籤對應索引

| US 標籤 | 對應 Spec | 核心測試檔 |
|---------|-----------|-----------|
| `[US1]` | US B-1 結構化條件查詢（spec.md#us-b-1）| `test_strategy_service.py`, `test_strategy_api.py`, `QueryPanel.test.ts` |
| `[US2]` | US B-2 Grid 多圖並列顯示（spec.md#us-b-2）| `ChartGrid.strategy.test.ts` |
| `[US3]` | US B-3 事件日置中對齊（spec.md#us-b-3）| `test_strategy_service.py` (-k align), `MiniChart.test.ts` |
| `[US4]` | US B-4 查詢結果限制與分頁（spec.md#us-b-4）| `test_strategy_service.py` (-k pagination), `test_strategy_api.py` (-k pagination) |
