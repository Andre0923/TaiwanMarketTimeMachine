# Feature Specification: 002-frontend-chart-interactions

> **Feature ID**: 002-frontend-chart-interactions  
> **Status**: Draft  
> **Created**: 2026-02-04  
> **Updated**: 2026-02-04  
> **Milestone**: M02  
> **System Context**: true

---

## Metadata

- **相依 Feature**: 001-basic-chart-api (已完成)
- **技術範疇**: Frontend (Vue 3 + TradingView Lightweight Charts)
- **影響範圍**: UI Layer, Chart Components, User Interactions
- **Backend 依賴**: M01 Backend API (`GET /api/chart/daily`)

---

## Problem Statement

### 問題描述

M01 已完成 Backend API 與資料聚合邏輯，但使用者仍無法在瀏覽器中看到圖表。目前缺少：

1. **前端渲染能力**：無法將 API 資料轉換為視覺化圖表
2. **互動操作**：無法透過滑鼠進行縮放、平移、查看詳細數據
3. **Grid 模式**：無法同時檢視多個股票的小圖，也無法放大單一小圖
4. **載入狀態管理**：使用者不知道系統是否正在載入資料或發生錯誤

### 影響範圍

- **使用者體驗**：策略研究員無法使用視覺化工具分析股票
- **功能完整性**：Group A 功能僅完成 40%（2/5 US）
- **後續開發**：Grid 模式（M03）與 Time Window（M04）依賴本 Feature

---

## Goals

### 主要目標

1. **建立前端專案**：Vite + Vue 3 + TypeScript + TradingView Lightweight Charts
2. **實作圖表元件**：ChartWidget（單一圖表）、ChartGrid（Grid 模式）
3. **整合 Backend API**：使用 M01 的 `/api/chart/daily` 取得資料
4. **實現互動操作**：滾輪縮放、拖曳平移、十字線顯示
5. **完成 Grid 功能**：小圖點擊放大、返回 Grid 檢視
6. **狀態管理**：Loading 狀態、錯誤處理、重試機制

### 成功標準

- [ ] 前端專案可正常啟動（`npm run dev`）
- [ ] 可渲染單一股票的 K 線圖與成交量副圖
- [ ] 互動操作流暢（縮放、平移、十字線）
- [ ] Grid 模式可同時顯示多個小圖
- [ ] 小圖點擊後可放大至主檢視區域
- [ ] Loading 與 Error 狀態正確顯示
- [ ] 元件測試覆蓋率 ≥ 80%
- [ ] E2E 測試涵蓋主要使用者流程

---

## User Stories

### US A-2: 圖表互動操作（Zoom/Pan/Crosshair）

**As a** 策略研究員  
**I want** 能夠縮放、平移圖表，並使用十字線查看詳細數據  
**So that** 我能夠深入檢視特定時間區段的價格細節

#### Acceptance Criteria

**AC1 — 滑鼠滾輪縮放**
- **Given** 圖表已顯示
- **When** 使用者滾動滑鼠滾輪
- **Then** 圖表應以滑鼠位置為中心進行縮放

**AC2 — 拖曳平移**
- **Given** 圖表已顯示
- **When** 使用者按住左鍵拖曳
- **Then** 圖表應跟隨滑鼠移動進行平移

**AC3 — 十字線資料顯示**
- **Given** 圖表已顯示
- **When** 滑鼠移動到 K 線上
- **Then** 應顯示該 K 線的 OHLC 與成交量數據

---

### US A-3: 小圖點擊放大檢視

**As a** 策略研究員  
**I want** 點擊 Grid 中的任一小圖後能放大檢視  
**So that** 我能夠更清楚地分析單一樣本的細節

#### Acceptance Criteria

**AC1 — 小圖點擊事件**
- **Given** Grid 模式下顯示多個小圖
- **When** 使用者點擊任一小圖
- **Then** 該小圖應放大至主檢視區域

**AC2 — 放大後互動保留**
- **Given** 小圖已放大至主檢視
- **When** 使用者進行縮放或平移
- **Then** 所有互動操作應正常運作

**AC3 — 返回 Grid 檢視**
- **Given** 正在檢視放大圖表
- **When** 使用者點擊「返回」按鈕或按下 ESC
- **Then** 應返回 Grid 多圖並列檢視

---

### US A-4: 圖表載入狀態與錯誤處理

**As a** 策略研究員  
**I want** 在圖表載入過程中看到明確的狀態提示  
**So that** 我知道系統正在運作或是否發生錯誤

#### Acceptance Criteria

**AC1 — 載入中狀態**
- **Given** 系統正在從 API 取得圖表資料
- **When** 圖表元件處於載入狀態
- **Then** 應顯示 Loading 指示器（如 Spinner）

**AC2 — 載入錯誤提示**
- **Given** API 請求失敗（如網路錯誤、逾時）
- **When** 圖表嘗試渲染
- **Then** 應顯示明確的錯誤訊息與重試按鈕

**AC3 — 部分圖表失敗不影響整體**
- **Given** Grid 模式下載入多個圖表
- **When** 其中一個圖表載入失敗
- **Then** 其他圖表應正常顯示，失敗的圖表單獨顯示錯誤提示

---

## Technical Design

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Browser (Vue 3 App)               │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌───────────────┐      ┌──────────────────┐      │
│  │ ChartGrid.vue │──────│ ChartWidget.vue  │      │
│  │ (Grid 容器)   │      │ (單一圖表)        │      │
│  └───────────────┘      └──────────────────┘      │
│          │                       │                 │
│          │                       │                 │
│          ▼                       ▼                 │
│  ┌───────────────────────────────────────┐        │
│  │     useChartData.ts (Composable)      │        │
│  │  - fetchChartData()                   │        │
│  │  - chartState (loading/error/success) │        │
│  └───────────────────────────────────────┘        │
│          │                                         │
│          ▼                                         │
│  ┌───────────────────────────────────────┐        │
│  │      chartApi.ts (API Client)         │        │
│  │  - getChartData(stock, start, end)    │        │
│  └───────────────────────────────────────┘        │
│          │                                         │
└──────────┼─────────────────────────────────────────┘
           │
           │ HTTP Request
           │
           ▼
┌─────────────────────────────────────────────────────┐
│         Backend API (M01 已完成)                     │
│                                                     │
│  GET /api/chart/daily                               │
│  ?stock_code=2330&start_date=...&end_date=...      │
│                                                     │
│  Response: ChartResponse (JSON)                     │
└─────────────────────────────────────────────────────┘
```

### Tech Stack

| 技術 | 版本 | 用途 |
|------|------|------|
| **Electron** | ^33.0.0 | 桌面應用框架（跨平台）|
| **Vue 3** | ^3.4.0 | 前端框架（Composition API）|
| **Vite** | ^5.0.0 | 建置工具與開發伺服器 |
| **TypeScript** | ^5.3.0 | 型別檢查與開發體驗 |
| **TradingView Lightweight Charts** | ^4.1.0 | 圖表渲染庫 |
| **Axios** | ^1.6.0 | HTTP Client |
| **electron-builder** | ^25.0.0 | 應用程式打包與分發 |
| **vite-plugin-electron** | ^0.28.0 | Vite 與 Electron 整合 |
| **Vitest** | ^1.0.0 | 單元測試 |
| **@vue/test-utils** | ^2.4.0 | 元件測試 |
| **Playwright** | ^1.40.0 | E2E 測試 |

### Project Structure

```
frontend/
├── electron/
│   ├── main.ts                  # Electron 主程序入口
│   ├── preload.ts               # Preload Script（IPC Bridge）
│   └── windows/
│       └── main-window.ts       # 主視窗管理
├── public/
│   └── favicon.ico
├── src/
│   ├── assets/
│   │   └── styles/
│   │       └── main.css
│   ├── components/
│   │   ├── ChartWidget.vue        # 單一圖表元件
│   │   ├── ChartGrid.vue          # Grid 模式容器
│   │   ├── ChartLoading.vue       # Loading 狀態
│   │   └── ChartError.vue         # 錯誤提示
│   ├── composables/
│   │   ├── useChartData.ts        # 資料取得與狀態管理
│   │   └── useChartInteraction.ts # 互動邏輯（縮放、平移）
│   ├── services/
│   │   └── chartApi.ts            # API 呼叫封裝
│   ├── types/
│   │   └── chart.ts               # TypeScript 型別定義
│   ├── App.vue                    # 根元件
│   ├── main.ts                    # 應用程式入口
│   └── env.d.ts                   # 環境變數型別定義
├── tests/
│   ├── unit/                      # 單元測試
│   ├── component/                 # 元件測試
│   └── e2e/                       # E2E 測試
├── .env.development               # 開發環境變數
├── .env.production                # 生產環境變數
├── electron-builder.json          # Electron 打包配置
├── index.html
├── package.json
├── tsconfig.json
├── tsconfig.node.json
├── vite.config.ts
└── vitest.config.ts
```

---

## Implementation Details

### TypeScript Types

**`frontend/src/types/chart.ts`**：
```typescript
// 與 Backend 契約一致
export interface ChartDataPoint {
  time: string;  // ISO 8601 datetime
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface ChartMetadata {
  stock_code: string;
  start_date: string;
  end_date: string;
  data_points: number;
}

export interface ChartResponse {
  stock_code: string;
  chart_data: ChartDataPoint[];
  metadata: ChartMetadata;
}

export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: string;
  };
}

export type ChartState = 'idle' | 'loading' | 'success' | 'error';

export interface ChartViewMode = 'grid' | 'expanded';
```

### API Integration

**`frontend/src/services/chartApi.ts`**：
```typescript
import axios from 'axios';
import type { ChartResponse, ErrorResponse } from '@/types/chart';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function getChartData(
  stockCode: string,
  startDate: string,
  endDate: string
): Promise<ChartResponse> {
  try {
    const response = await axios.get<ChartResponse>(
      `${API_BASE_URL}/api/chart/daily`,
      {
        params: { stock_code: stockCode, start_date: startDate, end_date: endDate }
      }
    );
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      const errorData = error.response.data as ErrorResponse;
      throw new Error(errorData.error.message);
    }
    throw error;
  }
}
```

### Composable Design

**`frontend/src/composables/useChartData.ts`**：
```typescript
import { ref, type Ref } from 'vue';
import { getChartData } from '@/services/chartApi';
import type { ChartResponse, ChartState } from '@/types/chart';

export function useChartData() {
  const data: Ref<ChartResponse | null> = ref(null);
  const state: Ref<ChartState> = ref('idle');
  const error: Ref<string | null> = ref(null);

  async function fetchChartData(
    stockCode: string,
    startDate: string,
    endDate: string
  ) {
    state.value = 'loading';
    error.value = null;
    
    try {
      data.value = await getChartData(stockCode, startDate, endDate);
      state.value = 'success';
    } catch (err) {
      error.value = err instanceof Error ? err.message : '未知錯誤';
      state.value = 'error';
    }
  }

  function retry() {
    // Retry logic
  }

  return { data, state, error, fetchChartData, retry };
}
```

---

## Testing Strategy

### Unit Tests (Vitest)

**測試範疇**：
- `chartApi.ts`：API 呼叫邏輯
- `useChartData.ts`：資料處理與狀態管理
- `useChartInteraction.ts`：互動邏輯

**目標覆蓋率**：≥ 80%

### Component Tests (Vue Test Utils)

**測試範疇**：
- `ChartWidget.vue`：圖表渲染與互動
- `ChartGrid.vue`：Grid 模式佈局
- `ChartLoading.vue`：Loading 狀態顯示
- `ChartError.vue`：錯誤提示與重試

### E2E Tests (Playwright)

**測試流程**：
1. 使用者導航至圖表頁面
2. 系統載入圖表資料
3. 使用者進行縮放、平移操作
4. 使用者點擊小圖放大檢視
5. 使用者返回 Grid 檢視

---

## Dependencies

### External Dependencies

| 依賴 | 版本 | 狀態 | 說明 |
|------|------|------|------|
| M01 Backend API | v0.2.0 | ✅ 完成 | `GET /api/chart/daily` |
| TradingView Lightweight Charts | ^4.1.0 | ✅ 穩定 | 開源圖表庫 |
| Vue 3 | ^3.4.0 | ✅ 穩定 | 前端框架 |

### Internal Dependencies

- System Spec v0.2.0（資料模型與 API 契約）
- ChartResponse 格式定義
- ErrorResponse 格式定義
- 錯誤碼規範（6 項標準錯誤碼）

---

## Risks & Mitigations

| 風險 | 影響 | 機率 | 緩解策略 |
|------|------|------|----------|
| TradingView Charts 學習曲線陡峭 | 中 | 高 | 預先建立 POC，參考官方範例 |
| Grid 模式效能問題（多圖渲染） | 高 | 中 | 實作虛擬滾動、延遲載入 |
| API CORS 問題 | 中 | 低 | Backend 已設定 CORS，測試驗證 |
| 跨瀏覽器相容性 | 中 | 中 | 使用 Browserslist，E2E 測試多瀏覽器 |

---

## Open Questions

1. **Grid 佈局**：需要支援多少種佈局模式？（2x2, 3x3, 4x4？）
2. **圖表快取**：是否需要快取已載入的圖表資料？
3. **響應式設計**：是否需要支援平板與手機版？
4. **主題切換**：是否需要支援深色模式？
5. **效能目標**：Grid 模式同時顯示多少個小圖為上限？

---

## Version History

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 0.1.0 | 2026-02-04 | 初始版本，定義 3 個 User Stories（US A-2, A-3, A-4）|
