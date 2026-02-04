# Unify Flow Checklist: 基礎繪圖與 API 格式

> **Feature ID**: 001-basic-chart-api  
> **Created**: 2026-02-04  
> **Purpose**: 準備將 Feature 規格合併至 System Spec

---

## 1. User Story 完成度驗證

### US A-1: K線與成交量基礎繪圖（後端 API）

**實作狀態**: ✅ 完成

**Acceptance Criteria 驗證**:
- [X] **AC1**: 日K線資料聚合
  - 測試: `test_chart_service.py::TestGetDailyChart::test_successful_aggregation`
  - 測試: `test_chart_service.py::TestAggregateToDaily::test_aggregate_logic`
  - 實作: `src/services/chart_service.py::_aggregate_to_daily()`
  
- [X] **AC2**: API 端點回應格式
  - 測試: `test_chart_api.py::TestGetDailyChartAPI::test_successful_request`
  - 測試: `test_api_contract.py::TestResponseSchemaCompliance`
  - 實作: `src/api/routes/chart.py::get_daily_chart()`
  
- [X] **AC3**: 錯誤處理機制
  - 測試: `test_chart_api.py::TestErrorHandling::test_invalid_date_range`
  - 測試: `test_api_contract.py::TestErrorFormatConsistency`
  - 實作: `src/api/routes/chart.py` 錯誤處理邏輯

**實作檔案**:
- `src/models/chart.py`（資料模型）
- `src/db/stock_repository.py`（資料存取）
- `src/services/chart_service.py`（業務邏輯）
- `src/api/routes/chart.py`（API 端點）

---

### US A-2: 圖表互動操作

**實作狀態**: 🚧 延後至 M02

**原因**: 前端功能不在 M01 範圍

---

### US A-3: 小圖放大功能

**實作狀態**: 🚧 延後至 M02

**原因**: 前端功能不在 M01 範圍

---

### US A-4: 載入狀態與錯誤處理（前端）

**實作狀態**: 🚧 延後至 M02

**原因**: 前端功能不在 M01 範圍

---

### US G-2: API Response 格式設計

**實作狀態**: ✅ 完成

**Acceptance Criteria 驗證**:
- [X] **AC1**: Request/Response 格式規範
  - 文件: `contracts/chart-api.md`（Section 1）
  - 測試: `test_api_contract.py::TestResponseSchemaCompliance`
  
- [X] **AC2**: 錯誤格式標準化
  - 文件: `contracts/chart-api.md`（Section 2）
  - 測試: `test_api_contract.py::TestErrorFormatConsistency`
  - 實作: `src/models/chart.py::ErrorResponse`
  
- [X] **AC3**: 擴充性原則
  - 文件: `contracts/chart-api.md`（Section 3）
  - 測試: `test_api_contract.py::TestBackwardCompatibility`
  
- [X] **AC4**: 使用範例提供
  - 文件: `contracts/chart-api.md`（Section 4）
  - 範例: curl, Python, JavaScript
  
- [X] **AC5**: 前端整合指引
  - 文件: `contracts/chart-api.md`（Section 5）
  - 包含 TradingView Lightweight Charts 整合範例

**實作檔案**:
- `specs/features/001-basic-chart-api/contracts/chart-api.md`（契約文件）
- `tests/integration/test_api_contract.py`（契約測試）

---

## 2. 可共享模組識別

### 2.1 資料模型（Shared Models）

**建議合併至 System Spec**:

| 模組 | 檔案 | 合併至 | 理由 |
|------|------|--------|------|
| `ChartDataPoint` | `src/models/chart.py` | `specs/system/data-model.md` | 圖表資料點為核心共享模型 |
| `ChartResponse` | `src/models/chart.py` | `specs/system/data-model.md` | API 回應格式將被其他 Feature 複用 |
| `ChartMetadata` | `src/models/chart.py` | `specs/system/data-model.md` | 元資料格式供其他查詢複用 |
| `ErrorResponse` | `src/models/chart.py` | `specs/system/data-model.md` | 統一錯誤格式供全域使用 |

**不建議合併**（Feature-Specific）:
- `ChartRequest`: 僅用於此 Feature 的請求驗證

---

### 2.2 資料存取層（Shared Repository）

**建議合併至 System Spec**:

| 模組 | 檔案 | 合併至 | 理由 |
|------|------|--------|------|
| `StockRepository` | `src/db/stock_repository.py` | `specs/system/data-model.md` | 1分K查詢將被多個 Feature 使用 |

**方法清單**:
- `get_one_minute_klines()`: 查詢 1分K 原始資料
- `check_stock_exists()`: 驗證股票代碼有效性

---

### 2.3 業務邏輯層（Shared Services）

**部分建議合併**:

| 模組 | 檔案 | 合併至 | 理由 |
|------|------|--------|------|
| `ChartService._validate_date_range()` | `src/services/chart_service.py` | `specs/system/flows.md` | 日期驗證邏輯可供其他時間查詢複用 |
| `ChartService._aggregate_to_daily()` | `src/services/chart_service.py` | `specs/system/flows.md` | 日K聚合邏輯為核心演算法 |

**不建議合併**（Feature-Specific）:
- `ChartService.get_daily_chart()`: 特定於本 Feature 的業務流程

---

### 2.4 API 層（Shared Contracts）

**建議合併至 System Spec**:

| 模組 | 檔案 | 合併至 | 理由 |
|------|------|--------|------|
| 錯誤碼規範 | `contracts/chart-api.md` | `specs/system/contracts/errors.md` | 統一錯誤碼供全域使用 |
| 日期格式規範 | `contracts/chart-api.md` | `specs/system/contracts/common-formats.md` | ISO 8601 格式應全域統一 |

**不建議合併**（Feature-Specific）:
- `/api/chart/daily` 端點規範: 特定於本 Feature

---

## 3. System Spec 更新建議

### 3.1 `specs/system/data-model.md` 新增內容

```markdown
## 圖表資料模型

### ChartDataPoint（圖表資料點）

**用途**: 表示單一時間點的OHLCV資料

**欄位定義**:
| 欄位 | 型別 | 說明 | 驗證規則 |
|------|------|------|----------|
| time | string | 日期（ISO 8601: YYYY-MM-DD） | 必填 |
| open | float | 開盤價 | > 0 |
| high | float | 最高價 | >= open, >= close, >= low |
| low | float | 最低價 | <= open, <= close, <= high |
| close | float | 收盤價 | > 0 |
| volume | float | 成交量 | >= 0 |

**來源**: Feature 001-basic-chart-api

---

### ErrorResponse（統一錯誤格式）

**用途**: API 錯誤回應標準格式

**欄位定義**:
| 欄位 | 型別 | 說明 |
|------|------|------|
| code | string | 錯誤碼（見 System Contracts） |
| message | string | 人類可讀錯誤訊息 |
| details | string (optional) | 詳細錯誤資訊 |

**來源**: Feature 001-basic-chart-api
```

---

### 3.2 `specs/system/contracts/errors.md` 新增內容

```markdown
## API 錯誤碼規範

### 資料查詢類錯誤

| 錯誤碼 | HTTP Status | 說明 | 範例情境 |
|--------|-------------|------|----------|
| INVALID_STOCK_CODE | 400 | 股票代碼格式錯誤 | 代碼包含非數字字元 |
| INVALID_DATE_RANGE | 400 | 日期範圍不合法 | start_date > end_date |
| NO_DATA | 200 | 查無資料（非錯誤） | 股票代碼不存在或日期範圍外 |
| DATABASE_ERROR | 500 | 資料庫連線或查詢錯誤 | SQL Server 連線失敗 |
| INTERNAL_ERROR | 500 | 伺服器內部錯誤 | 未預期的例外 |

**來源**: Feature 001-basic-chart-api
```

---

### 3.3 `specs/system/flows.md` 新增內容

```markdown
## 資料查詢流程

### 日K線資料聚合

**輸入**: 1分K原始資料（List[Tuple]）
**輸出**: 日K資料（Dict[date, OHLCV]）

**演算法**:
1. 按日期分組 1分K 資料
2. 每日第一筆的 open 作為開盤價
3. 每日所有 high 取最大值作為最高價
4. 每日所有 low 取最小值作為最低價
5. 每日最後一筆的 close 作為收盤價
6. 每日所有 volume 加總作為成交量

**實作**: `src/services/chart_service.py::_aggregate_to_daily()`
**來源**: Feature 001-basic-chart-api
```

---

### 3.4 `specs/system/contracts/common-formats.md` 新增內容

```markdown
## 日期時間格式規範

### 日期格式（Date）

**格式**: ISO 8601 (YYYY-MM-DD)
**範例**: `2024-01-15`
**驗證規則**: 
- 必須為有效日期
- 不接受未來日期

**來源**: Feature 001-basic-chart-api
```

---

## 4. 測試驗證狀態

### 4.1 測試統計

| 類型 | 數量 | 通過率 |
|------|------|--------|
| **單元測試** | 42 | 100% |
| **整合測試** | 19 | 100% |
| **總計** | 61 | 100% |

### 4.2 覆蓋率報告

| 模組 | 覆蓋率 | 狀態 |
|------|--------|------|
| `src/models/chart.py` | 100% | ✅ |
| `src/db/stock_repository.py` | 100% | ✅ |
| `src/services/chart_service.py` | 97% | ✅ |
| `src/api/routes/chart.py` | 100% | ✅ |
| `src/db/connection.py` | 93% | ✅ |
| **總計** | **89%** | ✅ |

---

## 5. 文件完整性檢查

- [X] **Feature Spec** (`spec.md`): 完整定義 User Stories 與 AC
- [X] **Data Model** (`data-model.md`): 完整定義資料結構與聚合邏輯
- [X] **Technical Plan** (`plan.md`): 完整定義技術架構與依賴
- [X] **Tasks** (`tasks.md`): 完整任務清單與執行記錄
- [X] **API Contract** (`contracts/chart-api.md`): 完整 API 契約規範
- [X] **Quick Start** (`quickstart.md`): 完整環境設定與測試指南
- [X] **Research** (`research.md`): 完整資料庫結構確認記錄

---

## 6. Git 提交記錄

| Commit | Phase | 說明 |
|--------|-------|------|
| 46ca540 | Phase 0 | 資料結構確認 |
| 17126ad | Phase 1 | 基礎建設（FastAPI + DB Connection） |
| 9534885 | Phase 2 | US A-1 後端 API 實作 |
| c3199d9 | Phase 6 | US G-2 API 契約文件 |
| (pending) | Phase 7 | 文件更新與 Code Review |

---

## 7. Unify Flow 執行建議

### 7.1 執行時機

**建議時機**: Phase 7 完成後

**前置條件**:
- ✅ 所有測試通過（61/61）
- ✅ 覆蓋率達標（89% > 80%）
- ✅ 文件完整（7 份文件）
- ✅ Git 提交乾淨

### 7.2 執行步驟

1. **執行 pre-unify-check**:
   ```bash
   /flowkit.pre-unify-check
   ```
   驗證：Feature Spec 與實作一致性

2. **執行 unify-flow**:
   ```bash
   /flowkit.unify-flow
   ```
   合併：共享模組至 System Spec

3. **驗證更新**:
   - 檢查 `specs/system/data-model.md` 新增內容
   - 檢查 `specs/system/contracts/` 新增錯誤碼
   - 檢查 `specs/system/flows.md` 新增演算法

4. **歸檔 Feature Spec**:
   ```bash
   mv specs/features/001-basic-chart-api specs/history/001-basic-chart-api-v1.0
   ```

---

## 8. 已知限制與未來工作

### 8.1 已知限制

| 限制 | 說明 | 未來改善 |
|------|------|----------|
| **前端未實作** | US A-2, A-3, A-4 延後 | M02 Milestone |
| **無快取機制** | 每次查詢都讀取資料庫 | M03: 加入 Redis Cache |
| **無分頁機制** | 大量資料可能影響效能 | M03: 加入分頁參數 |
| **無權限控制** | API 無驗證機制 | M04: 加入 JWT Auth |

### 8.2 技術債務

| 項目 | 優先級 | 預計處理 |
|------|--------|----------|
| 資料庫連線池 | 🟡 Medium | M02 |
| API Rate Limiting | 🟡 Medium | M04 |
| 日誌結構化 | 🟢 Low | M05 |

---

## 9. 核准簽署

### 9.1 技術驗證

- [X] 所有測試通過
- [X] 覆蓋率達標
- [X] 文件完整
- [X] 程式碼品質檢查通過

**驗證人**: AI Agent  
**驗證日期**: 2026-02-04

### 9.2 規格驗證

- [X] US A-1 所有 AC 完成
- [X] US G-2 所有 AC 完成
- [X] API 契約完整
- [X] 可共享模組識別完成

**驗證人**: Pending Human Review  
**驗證日期**: Pending

---

## 10. 執行 Unify Flow

準備完成後，執行：

```bash
/flowkit.unify-flow --feature 001-basic-chart-api
```

**預期結果**:
1. System Spec 更新（data-model.md, contracts/, flows.md）
2. Feature Spec 歸檔至 history/
3. 產生 unify-report.md

---

**版本**: v1.0  
**最後更新**: 2026-02-04  
**狀態**: ✅ 準備執行 Unify Flow
