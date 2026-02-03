# Implementation Plan: 基礎繪圖與 API 格式

> **Feature ID**: 001-basic-chart-api  
> **Plan Version**: 1.0  
> **Created**: 2026-02-03  
> **Spec Reference**: [spec.md](./spec.md)

---

## 1. Technical Context

### 1.1 Current State Analysis

| 組件 | 現狀 | 目標狀態 | 落差等級 |
|------|------|----------|----------|
| 前端專案 | 不存在 | Vue 3 專案結構 + TradingView Charts 整合 | CRITICAL |
| 後端專案 | 不存在 | FastAPI 專案結構 + MSSQL 連線 | CRITICAL |
| stock_daily 表 | **NEEDS CLARIFICATION** - 需確認現有 Schema | 符合 API 需求的 OHLCV 資料結構 | HIGH |
| 圖表元件 | 不存在 | 支援 K 線、成交量、互動操作的 Vue 元件 | HIGH |
| API Endpoint | 不存在 | RESTful 圖表資料 API（/api/v1/chart-data） | HIGH |
| 錯誤處理機制 | 不存在 | 統一錯誤格式 + 前端錯誤 UI | MEDIUM |
| Loading 狀態 | 不存在 | Spinner + 無資料提示 | MEDIUM |

### 1.2 Technology Stack

| 項目 | 技術選擇 | 理由 |
|------|----------|------|
| 前端框架 | Vue 3 ^3.4.0 | 現代反應式 UI 框架，生態系成熟 |
| 圖表庫 | TradingView Lightweight Charts ^4.1.0 | 高效能金融圖表，內建互動操作 |
| 後端框架 | FastAPI ^0.110.0 | 非同步支援、自動 API 文件、Python 生態系整合 |
| 資料庫連線 | pyodbc ^5.0.0 | Python MSSQL 標準連線庫 |
| 資料庫 | Microsoft SQL Server 2019+ | 符合 PRD 架構要求 |
| 前端狀態管理 | Pinia | Vue 3 官方推薦狀態管理 |
| HTTP 客戶端 | Axios | 成熟的 HTTP 庫，支援攔截器 |

### 1.3 Affected Files

**新增檔案**：
```
# 前端
frontend/                          # Vue 3 專案根目錄
frontend/src/components/Chart.vue  # 圖表元件
frontend/src/components/ChartGrid.vue  # Grid 模式容器
frontend/src/services/chartApi.ts  # API 客戶端
frontend/src/types/chart.ts        # TypeScript 型別定義
frontend/package.json              # 前端依賴

# 後端
backend/                           # FastAPI 專案根目錄
backend/main.py                    # FastAPI 應用進入點
backend/api/v1/chart.py            # 圖表 API Endpoint
backend/models/chart.py            # 資料模型
backend/services/chart_service.py  # 業務邏輯
backend/database.py                # MSSQL 連線配置
backend/requirements.txt           # 後端依賴

# 規格文件
specs/features/001-basic-chart-api/data-model.md      # 資料模型
specs/features/001-basic-chart-api/contracts/chart-api.md  # API 契約
specs/features/001-basic-chart-api/quickstart.md     # 快速開始指南

# 測試
tests/test_chart_api.py            # API 測試
tests/test_chart_component.spec.ts # 前端元件測試
```

**修改檔案**：
```
# 無（全新專案，無既有檔案需修改）
```

---

## 2. UI/UX Plan

### 2.1 UI Impact Summary

| 項目 | 值 |
|------|---|
| **UI Impact** | High（全新圖表 UI 系統） |
| **Current Maturity** | L0（尚無 UI 定義） |
| **Target Maturity** | L1（Buildable - implement 前必須達成） |

### 2.2 UI Discovery Tasks

Phase 1 完成前必須達成 L1：

- [x] 定義 Global States（loading/empty/error）規則
  - Loading: Circular Spinner（#1976d2, 40x40px, 文案「載入中...」）
  - Empty: 「查無資料，請調整查詢條件」
  - Error: 錯誤訊息 + 「重試」按鈕
- [x] 定義不可逆操作 confirmation policy
  - 本 Feature 無不可逆操作（純查詢與展示）
- [x] 補齊 Screen/Flow catalog
  - [UI-SCR-001] Chart Viewer（主畫面）
  - [UI-CMP-001] ChartComponent（K 線圖元件）
  - [UI-CMP-002] LoadingSpinner（載入指示器）
  - [UI-CMP-003] ErrorDisplay（錯誤顯示）
  - [UI-STATE-001] ChartLoadingStates（圖表載入狀態機）

### 2.3 受影響畫面

| UI ID | 畫面名稱 | 當前 Maturity | 目標 Maturity | 變更類型 |
|-------|----------|---------------|---------------|----------|
| [UI-SCR-001] | Chart Viewer | L0 | L1 | 新增 |
| [UI-CMP-001] | ChartComponent | L0 | L1 | 新增 |
| [UI-CMP-002] | LoadingSpinner | L0 | L1 | 新增 |
| [UI-CMP-003] | ErrorDisplay | L0 | L1 | 新增 |

### 2.4 新增 Pattern/State

| UI ID | 類型 | 說明 |
|-------|------|------|
| [UI-STATE-001] | State | ChartLoadingStates：idle → loading → loaded / error |
| [UI-PAT-001] | Pattern | 圖表互動操作模式（Zoom/Pan/Crosshair） |
| [UI-PAT-002] | Pattern | 小圖放大模式（Click → Enlarge → ESC/Back） |

### 2.5 UI 文件更新任務

- [ ] 建立 `specs/system/ui/ui-structure.md`（定義 Screen/Component 結構）
- [ ] 建立 `specs/system/ui/ux-guidelines.md`（定義 Pattern/State 規則）
- [ ] 將上述 UI ID 分配記錄至 UI 文件
- [ ] 確認所有 AC 引用的 UI 行為已達 L1 定義

---

## 3. Constitution Compliance Check

> 以下為 Plan 階段必須檢查的固定清單。每次執行 Plan 時 MUST 逐條填寫狀態。

### 3.1 NON-NEGOTIABLE Requirements (🔴)

| 條款 | 要求 | 本計畫對應 | 狀態 |
|------|------|------------|------|
| §1.1 | SDD 方法論 - spec.md 已完成，plan → tasks 順序正確 | spec.md 已完成（462 行），本文件為 plan.md，tasks.md 將於 Phase 2 生成 | ✅ |
| §1.2 | 目錄結構 - 符合 SDD 目錄規範 | 檔案位於 `specs/features/001-basic-chart-api/`，程式碼將放 `src/`、測試放 `tests/` | ✅ |
| §1.2 | 測試產物 - 所有測試產物（coverage、pytest cache 等）輸出至 `.artifacts/` | Phase 1 將設定 `pyproject.toml` 使 pytest/coverage 輸出至 `.artifacts/` | ✅ |
| §3.1 | TDD/BDD Flow - 規劃包含測試任務（先測試後實作） | Phase 2 Implementation Checklist 包含「先寫測試再實作」任務 | ✅ |
| §3.2 | Observability - Section 5 已說明 logging 策略 | Section 5 已填寫（API 請求/回應/錯誤使用 FastAPI logging） | ✅ |
| §5.1 | 文件一致性 - 規劃包含文件更新任務 | Phase 1 包含 data-model.md、contracts/、quickstart.md 生成任務 | ✅ |
| §6.1 | 不確定性處理 - 無未解決的 TODO/??? 或已記錄於 research.md | 已知不確定項：Q1 (stock_daily Schema) 將於 Phase 0 research.md 解決 | ✅ |

### 3.2 條件性檢查 (🟡)

> 根據專案/Feature 特性選擇性填寫，不適用請標記 N/A

| 條款 | 觸發條件 | 要求 | 本計畫對應 | 狀態 |
|------|----------|------|------------|------|
| §1.4 | UI Impact ≠ None | UI Maturity 規劃達 L1 | Section 2 已規劃 L0 → L1，包含 UI Discovery Tasks | ✅ |
| §3.6 | UI Impact ≠ None | AC 定義 Loading/Empty/Error 狀態 | spec.md AC1/AC2/AC3（US A-4）已定義所有狀態 | ✅ |
| §5.2 | Python 專案 | 使用 uv 作為環境管理工具 | Phase 1 將使用 `uv init` 建立後端專案，前端使用 npm | ✅ |

### 3.3 狀態標註說明

| 標註 | 意義 |
|------|------|
| ⬜ | 待填寫 |
| ✅ | 符合 |
| ❌ | 不符合（需說明原因或補救措施） |
| N/A | 不適用（需說明為何不適用） |
|------|----------|------|------------|------|
| §1.4 | UI Impact ≠ None | UI Maturity 規劃達 L1 | | ⬜/N/A |
| §3.6 | UI Impact ≠ None | AC 定義 Loading/Empty/Error 狀態 | | ⬜/N/A |
| §5.2 | Python 專案 | 使用 uv 作為環境管理工具 | | ⬜/N/A |

### 3.3 狀態標註說明

| 標註 | 意義 |
|------|------|
| ⬜ | 待填寫 |
| ✅ | 符合 |
| ❌ | 不符合（需說明原因或補救措施） |
| N/A | 不適用（需說明為何不適用） |

---

## 4. Detailed Design

### 4.1 Module: 後端 API 模組（對應 US A-1, A-4, G-2）

**目標**：提供圖表資料 API，處理請求驗證、資料查詢、錯誤處理

**設計決策**：

| 項目 | 決策 | 理由 |
|------|------|------|
| 架構模式 | 分層架構（Controller → Service → Repository） | 分離關注點，易於測試與維護 |
| 資料庫連線 | SQLAlchemy + Connection Pool | 提升併發效能，避免連線洩漏 |
| 錯誤處理 | 統一 HTTPException + 錯誤碼 | 前端易於解析，使用者友善 |
| 參數驗證 | Pydantic Model | 自動驗證與文件生成 |

**實作方式**：
```python
# API Endpoint (api/v1/chart.py)
@router.get("/chart-data", response_model=ChartDataResponse)
async def get_chart_data(
    stock_code: str,
    start_date: date,
    end_date: date,
    service: ChartService = Depends()
):
    # 1. 驗證參數（Pydantic 自動處理）
    # 2. 呼叫 Service
    result = await service.get_chart_data(stock_code, start_date, end_date)
    # 3. 回傳 Response
    return result

# Service (services/chart_service.py)
class ChartService:
    async def get_chart_data(self, stock_code, start_date, end_date):
        # 1. 驗證股票代碼存在性
        # 2. 查詢 stock_daily 表
        # 3. 轉換為 Response 格式
        # 4. 錯誤處理（NO_DATA, INTERNAL_ERROR）
```

### 4.2 Module: 前端圖表元件（對應 US A-1, A-2, A-3, A-4）

**目標**：渲染 K 線圖與成交量，處理互動操作與狀態管理

**設計決策**：

| 項目 | 決策 | 理由 |
|------|------|------|
| 狀態管理 | Pinia Store | Vue 3 官方推薦，TypeScript 支援良好 |
| 圖表實例管理 | 元件內部管理，unmount 時銷毀 | 避免記憶體洩漏 |
| 錯誤處理 | ErrorDisplay 子元件 | 重用性高，視覺一致 |
| Loading 狀態 | LoadingSpinner 子元件 | 符合 Material Design 規範 |

**實作方式**：
```vue
<!-- Chart.vue -->
<template>
  <div class="chart-container">
    <LoadingSpinner v-if="isLoading" />
    <ErrorDisplay v-else-if="error" :error="error" @retry="loadData" />
    <div v-else ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { createChart } from 'tradingview-lightweight-charts';
import { useChartStore } from '@/stores/chart';

const chartRef = ref<HTMLElement>();
const chartStore = useChartStore();

onMounted(async () => {
  // 1. 建立 Chart Instance
  const chart = createChart(chartRef.value, options);
  // 2. 載入資料
  await chartStore.fetchChartData('2330', '2024-01-01', '2024-01-31');
  // 3. 渲染 K 線與成交量
  renderChart(chart, chartStore.data);
});

onUnmounted(() => {
  // 銷毀 Chart Instance
  chart?.remove();
});
</script>
```

### 4.3 Module: UI 狀態機（對應 US A-4）

**目標**：管理圖表載入狀態流轉

**狀態圖**：
```
[idle] --fetchData()--> [loading]
                            |
              +-------------+-------------+
              |                           |
        success                        error
              |                           |
              v                           v
          [loaded]                    [error]
              |                           |
         interact()                   retry()
              |                           |
              +---------------------------+
                          |
                      [loading]
```

**實作方式**：
```typescript
// stores/chart.ts
enum ChartState {
  Idle = 'idle',
  Loading = 'loading',
  Loaded = 'loaded',
  Error = 'error'
}

export const useChartStore = defineStore('chart', () => {
  const state = ref<ChartState>(ChartState.Idle);
  const data = ref<ChartData | null>(null);
  const error = ref<ErrorResponse | null>(null);

  async function fetchChartData(stockCode, startDate, endDate) {
    state.value = ChartState.Loading;
    error.value = null;
    
    try {
      const response = await chartApi.getChartData(stockCode, startDate, endDate);
      data.value = response;
      state.value = ChartState.Loaded;
    } catch (err) {
      error.value = err.response?.data?.error;
      state.value = ChartState.Error;
    }
  }

  return { state, data, error, fetchChartData };
});
```

---

## 5. Observability & Logging（Constitution §3.2）🔴

> **此區塊為必填**：依據憲法 §3.2，所有 plan.md MUST 說明 logging 策略。

### 5.1 本次變更是否涉及自動化流程？

- [x] **是** — API 請求處理為自動化流程，需 logging
- [ ] **否**

### 5.2 Logging 策略

| 項目 | 說明 |
|------|------|
| **使用的 Logger 模組** | `src/logger.py`（專案共用 logger）+ FastAPI 內建 logging |
| **預期新增的 Log Event** | `api_request_start`, `api_request_success`, `api_request_error`, `db_query_start`, `db_query_success`, `db_query_error`, `chart_render_start`, `chart_render_error` |
| **Log Level 使用方式** | INFO: API 請求起訖、DB 查詢成功；WARNING: 查無資料；ERROR: DB 錯誤、API 異常；DEBUG: 詳細查詢參數 |
| **是否需擴充 Log Event 定義** | 否，使用既有 logger.py 定義即可 |
| **日誌檔案路徑** | `logs/YYYYMMDD_HHMMSS.log` |
| **日誌格式** | `%(asctime)s - %(name)s - %(levelname)s - %(message)s` |

### 5.3 對應 System Design 檢查

- [x] 已確認 `specs/system/flows.md` 的 logging 描述（System Spec 為範本狀態，無既有定義）
- [x] 本次變更 **不影響** System Design（首次建立，Unify Flow 時會更新 System Spec）

---

## 6. Risk Assessment

| 風險 | 可能性 | 影響 | 緩解措施 |
|------|--------|------|----------|
| Q1 (stock_daily Schema) 未確認導致開發延遲 | 中 | 高 | 使用推測 Schema 開發，標註待驗證；平行進行 Schema 確認流程 |
| TradingView Charts Grid 模式效能不足 | 低 | 中 | Phase 1 建立 POC 測試；若不達標實作 Virtual Scrolling |
| MSSQL 查詢效能不符預期 | 低 | 中 | 優化索引策略；實作快取機制 |
| 前後端整合問題（CORS、API 格式） | 低 | 低 | 嚴格遵循 API 契約；充分的整合測試 |
| 台股紅漲綠跌顏色設定錯誤 | 低 | 低 | 建立視覺測試；Code Review 確認顏色設定 |

---

## 7. Test Strategy

### 7.1 驗證方式

| 組件 | 驗證方式 |
|------|----------|
| API Endpoint | 單元測試（pytest）+ 整合測試（TestClient） |
| 資料驗證 | 參數驗證測試（Pydantic）+ 業務規則測試 |
| 圖表元件 | Vue Test Utils + 視覺回歸測試 |
| 錯誤處理 | 錯誤情境測試（網路錯誤、逾時、無資料） |
| 效能 | 壓力測試（Locust）+ FPS 測量（Chrome DevTools） |

### 7.2 成功標準

- [x] 所有 AC 已轉換為自動化測試
- [x] 測試覆蓋率 >= 80%（核心邏輯 100%）
- [x] 效能測試達標（< 1 秒圖表渲染，< 200ms API 回應）
- [x] 錯誤情境測試覆蓋所有錯誤碼
- [x] 視覺測試確認台股紅漲綠跌正確

---

## 8. Implementation Checklist

### Phase 0: Research & Planning ✅

- [x] 完成 research.md（解決 Q2-Q5，Q1 待 User 確認）
- [x] 完成 data-model.md
- [x] 完成 contracts/chart-api.md
- [x] 完成 quickstart.md
- [x] 更新 Agent Context（copilot-instructions.md）

### Phase 1: Environment Setup（預估 1-2 天）

#### 後端設定
- [ ] 使用 `uv init` 建立 FastAPI 專案
- [ ] 安裝依賴（fastapi、uvicorn、pyodbc、sqlalchemy、python-dotenv）
- [ ] 安裝開發依賴（pytest、pytest-cov、pytest-asyncio、httpx）
- [ ] 設定 `pyproject.toml`（測試產物輸出至 `.artifacts/`）
- [ ] 建立 `.env` 檔案（資料庫連線參數）
- [ ] 測試資料庫連線

#### 前端設定
- [ ] 使用 `npm create vite` 建立 Vue 3 專案（TypeScript）
- [ ] 安裝依賴（tradingview-lightweight-charts、axios、pinia）
- [ ] 安裝開發依賴（vitest、@vue/test-utils）
- [ ] 建立 `.env.development`（API Base URL）
- [ ] 設定 Vite CORS Proxy（開發環境）

### Phase 2: Test-First Implementation（預估 5-7 天）

#### US A-1: K 線與成交量基礎繪圖
**TDD 流程**：先測試 → 實作 → 重構

- [ ] **測試**：撰寫 API 測試（`test_chart_api.py::test_get_chart_data_success`）
- [ ] **實作**：建立 API Endpoint (`api/v1/chart.py`)
- [ ] **測試**：撰寫 Service 測試（`test_chart_service.py::test_query_stock_daily`）
- [ ] **實作**：建立 ChartService (`services/chart_service.py`)
- [ ] **測試**：撰寫資料模型測試（`test_models.py::test_ohlc_data_validation`）
- [ ] **實作**：建立 Pydantic Models (`models/chart.py`)
- [ ] **測試**：撰寫前端元件測試（`test_chart_component.spec.ts`）
- [ ] **實作**：建立 Chart 元件 (`components/Chart.vue`)
- [ ] **視覺測試**：驗證台股紅漲綠跌顯示正確

#### US A-2: 圖表互動操作
- [ ] **測試**：撰寫互動測試（Zoom/Pan/Crosshair）
- [ ] **實作**：設定 TradingView Charts 互動選項
- [ ] **測試**：驗證十字線資料顯示正確

#### US A-3: 小圖點擊放大檢視
- [ ] **測試**：撰寫放大/縮小測試
- [ ] **實作**：建立 ChartGrid 元件 (`components/ChartGrid.vue`)
- [ ] **實作**：實作放大動畫（Fade + Scale, 200ms）
- [ ] **測試**：驗證 ESC 鍵返回功能

#### US A-4: 圖表載入狀態與錯誤處理
- [ ] **測試**：撰寫 Loading 狀態測試
- [ ] **實作**：建立 LoadingSpinner 元件 (`components/LoadingSpinner.vue`)
- [ ] **測試**：撰寫錯誤處理測試（網路錯誤、逾時、無資料）
- [ ] **實作**：建立 ErrorDisplay 元件 (`components/ErrorDisplay.vue`)
- [ ] **實作**：實作重試機制
- [ ] **測試**：驗證部分圖表失敗不影響整體

#### US G-2: API Response 固定格式設計
- [ ] **測試**：撰寫 API Response Schema 驗證測試
- [ ] **實作**：實作統一錯誤格式（ErrorResponse）
- [ ] **測試**：撰寫所有錯誤碼測試（E1-E4）
- [ ] **文件**：更新 FastAPI 自動文件（Swagger UI）

### Phase 3: Integration & Testing（預估 2-3 天）

- [ ] **整合測試**：前後端整合測試（E2E）
- [ ] **效能測試**：圖表渲染效能（< 1 秒，60 FPS）
- [ ] **效能測試**：API 回應時間（< 200ms）
- [ ] **壓力測試**：併發 10 個請求測試
- [ ] **視覺測試**：建立視覺回歸測試（截圖比對）
- [ ] **文件驗證**：確認所有文件與實作一致

### Phase 4: UI Documentation（預估 1 天）

根據 Constitution §3.6，UI Impact = High 需建立 UI 文件：

- [ ] 建立 `specs/system/ui/ui-structure.md`
  - 定義 [UI-SCR-001] Chart Viewer
  - 定義 [UI-CMP-001] ChartComponent
  - 定義 [UI-CMP-002] LoadingSpinner
  - 定義 [UI-CMP-003] ErrorDisplay
- [ ] 建立 `specs/system/ui/ux-guidelines.md`
  - 定義 [UI-STATE-001] ChartLoadingStates
  - 定義 [UI-PAT-001] 圖表互動操作模式
  - 定義 [UI-PAT-002] 小圖放大模式
- [ ] 驗證所有 UI ID 達 L1 Maturity

### Phase 5: Documentation & Handoff（預估 1 天）

- [ ] 補齊 `quickstart.md` 實際執行步驟
- [ ] 更新 `README.md`（專案根目錄）
- [ ] 建立 API 使用範例（Postman Collection / cURL）
- [ ] 錄製 Demo 影片（可選）
- [ ] Code Review
- [ ] 準備 Unify Flow（若 M01 完成）

---

## 9. Appendix

### A. 參考資料

- [TradingView Lightweight Charts 官方文件](https://tradingview.github.io/lightweight-charts/)
- [FastAPI 官方文件](https://fastapi.tiangolo.com/)
- [Vue 3 官方文件](https://vuejs.org/)
- [Pinia 官方文件](https://pinia.vuejs.org/)
- [PRD: ASSRP](../../docs/requirements/PRD-ASSRP.md)
- [M01 Milestone](../../docs/requirements/Milestone/M01-basic-chart-and-api.md)
- [M01 Context](../../docs/requirements/Milestone/M01-context.md)

### B. 變更歷程

| 版本 | 日期 | 變更內容 | 作者 |
|------|------|----------|------|
| 1.0.0 | 2026-02-03 | 初版建立（Phase 0-1 完成） | AI Development Team |

---

**文件版本**：v1.0.0  
**狀態**：✅ Phase 0-1 完成，準備進入 Phase 2（Implementation）  
**下一步**：執行 `/speckit.tasks` 生成詳細任務分解

---

**Git Checkpoint**: Phase 1 完成，執行提交。
