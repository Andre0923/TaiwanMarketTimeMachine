# Technical Debt Registry

> **Last Updated**: 2026-02-25 (pr-review 補充 TD-004/005)

---

## Active Items

| ID | 標題 | 優先級 | 狀態 |
|----|------|--------|------|
| TD-001 | MSSQL 真實資料庫整合測試 | P2 | Open |
| TD-002 | Electron E2E 自動化測試（Playwright） | P2 | Open |
| TD-003 | test_connection PytestReturnNotNoneWarning | P3 | Open |
| TD-004 | CORS allow_origins 正式環境限縮 | P3 | Open |
| TD-005 | ChartService 改用 FastAPI Depends DI 模式 | P3 | Open |

---

## Items

### TD-001: MSSQL 真實資料庫整合測試

- **Priority**: P2
- **Type**: test-regression
- **Status**: Open
- **Created**: 2026-02-25
- **Source**: code-check
- **Feature-Origin**: 001-basic-chart-api
- **Milestone-Candidate**: true
- **Dedup-Key**: `test-regression:tests/integration/mssql-real-db`
- **Evidence-Ref**: `.artifacts/code-check-report-feature-001.md`
- **Detection-Count**: 1
- **Last-Detected**: 2026-02-25

**描述**: 現有整合測試使用 `unittest.mock` 替代 MSSQL 連線，未驗證實際資料庫查詢（`[股價即時].[dbo].[1分K]`）、欄位映射與 SQL 聚合邏輯。

**影響範圍**: `tests/integration/test_chart_api.py`、`tests/integration/test_api_contract.py`、`src/db/stock_repository.py`

**建議解法**: 建立帶 MSSQL 測試 fixture 的整合測試環境（可以 docker-compose 或測試用 MSSQL 實例），補充真實資料查詢測試。

**相關檔案**: `tests/integration/`, `src/db/connection.py`, `src/db/stock_repository.py`

---

### TD-002: Electron E2E 自動化測試（Playwright）

- **Priority**: P2
- **Type**: test-regression
- **Status**: Open
- **Created**: 2026-02-25
- **Source**: code-check
- **Feature-Origin**: 001-basic-chart-api
- **Milestone-Candidate**: true
- **Dedup-Key**: `test-regression:frontend/e2e-electron`
- **Evidence-Ref**: `.artifacts/code-check-report-feature-001.md`
- **Detection-Count**: 1
- **Last-Detected**: 2026-02-25

**描述**: `frontend/package.json` 無 `test:e2e` 腳本，尚未配置 Playwright Electron 測試套件。K 線渲染、互動操作（縮放/平移/十字線）、小圖放大等 UI 流程無自動化 E2E 驗證。

**影響範圍**: `frontend/src/components/`, `frontend/src/composables/`, Electron 主視窗

**建議解法**: 新增 `playwright.config.ts`、安裝 `@playwright/test`，以 `_electron` API 驅動 Electron 視窗，覆蓋 US A-1/A-2/A-3/A-4 的 E2E 腳本。

**相關檔案**: `frontend/package.json`, `frontend/playwright.config.ts`（待建立）

---

### TD-003: test_connection PytestReturnNotNoneWarning

- **Priority**: P3
- **Type**: code-quality
- **Status**: Open
- **Created**: 2026-02-25
- **Source**: code-check
- **Feature-Origin**: 001-basic-chart-api
- **Milestone-Candidate**: false
- **Dedup-Key**: `code-quality:tests/unit/test_db_connection.py`
- **Evidence-Ref**: `.artifacts/code-check-report-feature-001.md`
- **Detection-Count**: 1
- **Last-Detected**: 2026-02-25

**描述**: `tests/unit/test_db_connection.py::test_connection` 函式回傳 `bool` 而非 `None`，觸發 `PytestReturnNotNoneWarning`。應使用 `assert` 替代 `return`。

**影響範圍**: `tests/unit/test_db_connection.py`（1 行修改）

**建議解法**: 將 `return result` 改為 `assert result`。成本 EASY（1 行）。

**相關檔案**: `tests/unit/test_db_connection.py`

---

### TD-004: CORS allow_origins 正式環境限縮

- **Priority**: P3
- **Type**: security
- **Status**: Open
- **Created**: 2026-02-25
- **Source**: pr-review
- **Feature-Origin**: 001-basic-chart-api
- **Milestone-Candidate**: false
- **Dedup-Key**: `security:src/main.py:cors-wildcard`
- **Evidence-Ref**: `.artifacts/pr-review-report-feature-001.md`
- **Detection-Count**: 1
- **Last-Detected**: 2026-02-25

**描述**: `src/main.py` 中 `allow_origins=["*"]` 使用萬用字元，任何本機網頁皆可呼叫 API（即使是桌面 Electron 應用程式也存在潛在風險）。代碼已有備注「正式環境需限制」。

**影響範圍**: `src/main.py`（CORS 設定）

**建議解法**: 透過環境變數 `CORS_ALLOWED_ORIGINS` 設定允許來源清單（預設 `["http://localhost:5173", "http://127.0.0.1:5173"]`），正式 Electron 打包環境改為 `file://`。

**相關檔案**: `src/main.py`, `.env.example`

---

### TD-005: ChartService 改用 FastAPI Depends DI 模式

- **Priority**: P3
- **Type**: design-debt
- **Status**: Open
- **Created**: 2026-02-25
- **Source**: pr-review
- **Feature-Origin**: 001-basic-chart-api
- **Milestone-Candidate**: false
- **Dedup-Key**: `design-debt:src/api/routes/chart.py`
- **Evidence-Ref**: `.artifacts/pr-review-report-feature-001.md`
- **Detection-Count**: 1
- **Last-Detected**: 2026-02-25

**描述**: `src/api/routes/chart.py` 的 `get_daily_chart` handler 內直接 `service = ChartService()` 實例化，而非使用 FastAPI 推薦的 `Depends()` 依賴注入機制。目前可藉由 `@patch` mocker 測試，但耦合到具體類別而非介面。

**影響範圍**: `src/api/routes/chart.py`

**建議解法**: 新增 `get_chart_service()` 工廠函式，route 改為 `service: ChartService = Depends(get_chart_service)`，測試改用 `app.dependency_overrides`。

**相關檔案**: `src/api/routes/chart.py`, `tests/integration/test_chart_api.py`

---

## Template

```markdown
### TD-XXX: [標題]

- **Priority**: P1/P2/P3
- **Status**: Open / In Progress / Resolved
- **Created**: YYYY-MM-DD

**描述**: 

**影響範圍**: 

**建議解法**: 

**相關檔案**: 
```
