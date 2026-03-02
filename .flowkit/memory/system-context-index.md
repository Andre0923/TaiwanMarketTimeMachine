# Context Index v1.0.0

> 最後更新: 2026-03-02 | 完整版: `.flowkit/memory/system-context.md`

## One-liner
台股時光機: 視覺化事件研究平台，以互動式 K 線圖與 Grid 多圖並列協助策略研究員探索台股歷史事件對股價的影響。

## Boundaries (模組邊界，禁止跨越)
- `src/api/routes/`: HTTP 端點定義、請求驗證 | Owns: HTTP contract | API: `chart.py`
- `src/services/`: 業務邏輯（1分K聚合、策略查詢） | Owns: 聚合演算法 | API: `chart_service.py`
- `src/models/`: Pydantic 資料模型（Request/Response DTO）| Owns: 資料結構 | API: `chart.py`
- `src/db/`: MSSQL 連線管理、SQL 查詢 | Owns: DB 連線 | API: `stock_repository.py`
- `frontend/src/components/`: 可重用 Vue UI 元件 | Owns: 元件 props/events
- `frontend/src/composables/`: 前端狀態管理與互動邏輯 | Owns: 前端狀態機

## Entry Points (開發從這裡開始)
- Backend: `src/main.py` — FastAPI app 初始化
- API: `src/api/routes/chart.py` — GET /api/chart/daily
- Core: `src/services/chart_service.py` — _aggregate_to_daily()
- DB: `src/db/stock_repository.py` — SQL 查詢
- UI: `frontend/src/App.vue` — Vue 根元件
- Chart: `frontend/src/components/ChartWidget.vue` — 圖表互動元件
- Data: `frontend/src/composables/useChartData.ts` — 前端狀態機

## Shared Services (共享模組)
- `src/logger.py` — 統一 logging 設定（全專案使用，禁 print）
- `src/models/chart.py` — ChartDataPoint / ChartResponse / ErrorResponse（全 API 共用）
- `frontend/src/components/ChartLoading.vue` + `ChartError.vue` — 全域 UI 狀態元件

## Golden Flows (核心流程)
1. **日 K 線查詢**: GET /api/chart/daily → chart.py 驗證 → chart_service 聚合 → stock_repository SQL → ChartResponse
2. **前端圖表渲染**: useChartData.ts (idle→loading→success/error) → ChartWidget → TradingView Charts
3. **M03 策略查詢(待實作)**: QueryPanel 前端驗證 → POST /api/strategy/query → 篩選 stock_events → 取 pre=20/post=10 K線 → GridQueryResponse → ChartGrid

## Current Feature
**003-strategy-grid** | 狀態: Draft | spec: `specs/features/003-strategy-grid/spec.md`
- US B-1: 結構化條件查詢（4-10字元 stock_code、AND/OR、前端即時驗證）
- US B-2: Grid 多圖並列（4×5 預設，最多100圖，3秒內渲染50圖）
- US B-3: 事件日置中（pre=20 / post=10 交易日，系統常數）
- US B-4: 分頁（每頁100筆）

## Where-to-Look
- API 格式/欄位 → `specs/system/contracts/chart-api.md`
- 資料模型定義 → `specs/system/data-model.md`
- M03 需求/決策 → `specs/features/003-strategy-grid/spec.md` + `spec-delta-log.md`
- 錯誤碼規範 → `specs/system/spec.md §5`
- 前端狀態機規則 → `specs/system/spec.md §3.4`
- 設計衝突決策 → `docs/requirements/Milestone/M03-context.md`

## NON-NEGOTIABLE
1. 環境管理: `uv only`（禁止 pip/conda/poetry）
2. 日誌: `logging` only（禁止 print）；日誌 → `logs/YYYYMMDD_HHMMSS.log`
3. 測試產物: 必須輸出至 `.artifacts/`
4. System Spec: 禁止直接改 `specs/system/**`（唯一通道：Unify Flow）
5. Test-First: 先從 AC 寫測試，再改 `src/`
6. API 向下相容: 既有欄位型別/語意不得改變
7. NO_DATA: HTTP 200（不是錯誤），`chart_data=[]`，`data_points=0`

## Known Pitfalls
- **stock_code 規則衝突**: data-model.md 記載 4 位數字，但實際已決策 4-10 字元（含大寫英文）→ 以新規則為準，待 Unify 同步
- **M03 event_type 不是查詢條件**: 僅供顯示，不可加入 StrategyQueryParams
- **M03 pre/post 是常數**: pre=20/post=10 不提供 UI，M04 才開放
- **stock_events 唯讀**: M03 只 SELECT，不 INSERT/UPDATE/DELETE
- **ChartLoadingState 4 狀態**: idle/loading/success/error，新功能勿破壞狀態機

## Full Context
See: `.flowkit/memory/system-context.md`
