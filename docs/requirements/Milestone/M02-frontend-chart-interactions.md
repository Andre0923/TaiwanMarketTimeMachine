# Milestone 02 — 前端圖表互動功能

> **建立日期**：2026-02-04  
> **狀態**：🔘 待規劃  
> **預估規模**：3 個 User Story

---

## 能力邊界說明

### 本 Milestone 完成後具備的能力

1. **完整的前端圖表渲染**
   - 基於 M01 Backend API，實作 Vue 3 + TradingView Lightweight Charts 前端
   - 使用者可在瀏覽器中看到標準的 K 線圖與成交量副圖

2. **互動操作能力**
   - 滑鼠滾輪縮放圖表
   - 拖曳平移時間軸
   - 十字線即時顯示 OHLC 與成交量數據

3. **小圖放大檢視**
   - 點擊 Grid 中的小圖可放大至主檢視區域
   - 放大後保留完整互動能力
   - 支援返回 Grid 檢視

4. **載入狀態與錯誤處理**
   - Loading Spinner 顯示載入中狀態
   - 錯誤提示與重試機制
   - Grid 模式下單一圖表失敗不影響其他圖表

### 下一 Milestone 將擴展的方向

- **M03**：Strategy Grid 核心功能（結構化條件查詢、多圖並列、事件日對齊）
- **M04**：Time Window Engine（時間窗口參數設定、統一窗口渲染）
- **M05**：Micro Backtest 統計（事件後報酬計算、績效指標彙總）

---

## 包含的 User Stories

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

## 延後的 User Stories

本 Milestone 聚焦於基礎圖表互動，以下 User Stories 延後至後續 Milestone：

| US ID | 原因 |
|-------|------|
| US B-1, B-2, B-3, B-4 | Group B（Strategy Grid）需先完成基礎圖表功能 |
| US C-1, C-2, C-3, C-4 | Group C（Time Window Engine）依賴於 Strategy Grid |
| US D-1 ~ D-5 | Group D（Micro Backtest）依賴於 Time Window 與 Grid |

---

## 技術範疇

### 前端技術棧

| 技術 | 用途 | 版本 |
|------|------|------|
| **Vue 3** | 前端框架 | ^3.4.0 |
| **Vite** | 建置工具 | ^5.0.0 |
| **TradingView Lightweight Charts** | 圖表庫 | ^4.1.0 |
| **Pinia** | 狀態管理（選用）| ^2.1.0 |
| **Axios** | HTTP Client | ^1.6.0 |

### 專案結構

```
frontend/
├── src/
│   ├── components/
│   │   ├── ChartWidget.vue         # 單一圖表元件
│   │   ├── ChartGrid.vue           # Grid 模式容器
│   │   ├── ChartLoading.vue        # Loading 狀態
│   │   └── ChartError.vue          # 錯誤提示
│   ├── composables/
│   │   ├── useChartData.ts         # 資料取得邏輯
│   │   └── useChartInteraction.ts  # 互動邏輯
│   ├── services/
│   │   └── chartApi.ts             # API 呼叫封裝
│   ├── types/
│   │   └── chart.ts                # TypeScript 型別定義
│   └── App.vue
├── vite.config.ts
├── package.json
└── tsconfig.json
```

### API 整合

**使用 M01 建立的 Backend API**：
- **Endpoint**：`GET /api/chart/daily`
- **Query Params**：`stock_code`, `start_date`, `end_date`
- **Response**：`ChartResponse` 格式（與 Backend 契約一致）

---

## 開發前置準備

### 1. 前端專案初始化

```bash
# 建立 Vite + Vue 3 + TypeScript 專案
npm create vite@latest frontend -- --template vue-ts

cd frontend
npm install

# 安裝依賴
npm install lightweight-charts axios
npm install -D @types/node
```

### 2. 環境設定

**`.env.development`**：
```env
VITE_API_BASE_URL=http://localhost:8000
```

**`.env.production`**：
```env
VITE_API_BASE_URL=https://your-production-api.com
```

### 3. TypeScript 型別定義

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
```

---

## 測試策略

### 1. 單元測試（Vitest）

**測試範疇**：
- `chartApi.ts`：API 呼叫邏輯
- `useChartData.ts`：資料處理與狀態管理
- `useChartInteraction.ts`：互動邏輯

**範例測試案例**：
```typescript
describe('useChartData', () => {
  it('應正確處理 API 回應', async () => {
    // Given: Mock API 回應
    // When: 呼叫 fetchChartData
    // Then: 狀態應更新為 loaded，資料格式正確
  });

  it('應處理 API 錯誤', async () => {
    // Given: Mock API 錯誤
    // When: 呼叫 fetchChartData
    // Then: 狀態應為 error，顯示錯誤訊息
  });
});
```

### 2. 元件測試（Vue Test Utils）

**測試範疇**：
- `ChartWidget.vue`：圖表渲染與互動
- `ChartGrid.vue`：Grid 模式佈局
- `ChartLoading.vue`：Loading 狀態顯示
- `ChartError.vue`：錯誤提示與重試

**範例測試案例**：
```typescript
describe('ChartWidget', () => {
  it('應在載入時顯示 Loading 狀態', () => {
    // Given: 圖表處於 loading 狀態
    // When: 元件渲染
    // Then: 應顯示 ChartLoading 元件
  });

  it('應在載入完成後顯示圖表', async () => {
    // Given: API 回應成功
    // When: 資料載入完成
    // Then: 應渲染 TradingView Chart
  });
});
```

### 3. E2E 測試（Playwright）

**測試範疇**：
- 完整的使用者互動流程
- 跨瀏覽器相容性

**範例測試案例**：
```typescript
test('應能縮放與平移圖表', async ({ page }) => {
  // Given: 導航至圖表頁面
  await page.goto('/chart?stock_code=2330');
  
  // When: 滾動滑鼠滾輪
  await page.mouse.wheel(0, -100);
  
  // Then: 圖表應放大（驗證可視範圍縮小）
  // ...
});
```

---

## 效能考量

### 1. 圖表渲染效能

| 指標 | 目標 | 測量方式 |
|------|------|----------|
| **首次繪製時間** | < 500ms | Performance API |
| **互動回應時間** | < 16ms (60 FPS) | Frame timing |
| **Grid 模式渲染** | 同時顯示 20 個小圖 < 2s | Performance API |

### 2. 效能優化策略

- **虛擬滾動**：Grid 模式下使用 `vue-virtual-scroller`
- **圖表複用**：使用 Object Pool 避免重複建立 Chart 實例
- **延遲載入**：視口外的圖表延遲載入
- **資料快取**：使用 Pinia 或 Vuex 快取已載入的圖表資料

---

## 完成標準（Definition of Done）

### 功能完成度

- [ ] US A-2 所有 AC 實作完成並通過測試
- [ ] US A-3 所有 AC 實作完成並通過測試
- [ ] US A-4 所有 AC 實作完成並通過測試

### 測試完成度

- [ ] 單元測試覆蓋率 ≥ 80%
- [ ] 所有元件測試通過
- [ ] E2E 測試涵蓋主要使用者流程

### 文件完成度

- [ ] README.md 包含前端專案說明與啟動步驟
- [ ] API 整合文件完整
- [ ] 元件使用文件完整

### 品質標準

- [ ] ESLint 無錯誤
- [ ] TypeScript 編譯無錯誤
- [ ] Chrome DevTools Lighthouse Performance Score ≥ 90

### Code Review

- [ ] 至少 1 位 Reviewer 審核通過
- [ ] 所有 Review Comments 已處理

---

## 預期交付產物

### 1. 前端應用程式

- `frontend/` 目錄完整的 Vue 3 + TypeScript 專案
- 可執行的本地開發環境
- 可建置的生產版本

### 2. 測試報告

- 單元測試報告（Vitest）
- 元件測試報告（Vue Test Utils）
- E2E 測試報告（Playwright）
- 測試覆蓋率報告

### 3. 文件

- 前端專案 README.md
- API 整合文件
- 元件使用文件
- 開發指南

### 4. Demo

- 部署至開發環境的可訪問 URL
- 展示影片或截圖（選用）

---

## 風險與依賴

### 技術風險

| 風險 | 影響 | 緩解策略 |
|------|------|----------|
| TradingView Charts 學習曲線 | 中 | 預先建立 POC，參考官方範例 |
| Grid 模式效能問題 | 高 | 實作虛擬滾動，延遲載入 |
| 跨瀏覽器相容性 | 中 | 使用 Browserslist，E2E 測試多瀏覽器 |

### 外部依賴

| 依賴 | 狀態 | 備註 |
|------|------|------|
| M01 Backend API | ✅ 已完成 | `/api/chart/daily` 已可用 |
| TradingView Lightweight Charts | ✅ 穩定 | 開源專案，版本穩定 |

---

## 參考資源

### TradingView Lightweight Charts

- **官方文件**：https://tradingview.github.io/lightweight-charts/
- **GitHub**：https://github.com/tradingview/lightweight-charts
- **範例集**：https://tradingview.github.io/lightweight-charts/tutorials/

### Vue 3 + TypeScript

- **Vue 3 文件**：https://vuejs.org/
- **TypeScript 文件**：https://www.typescriptlang.org/

### 測試框架

- **Vitest**：https://vitest.dev/
- **Vue Test Utils**：https://test-utils.vuejs.org/
- **Playwright**：https://playwright.dev/

---

**Milestone 狀態**：🔘 待規劃  
**建立日期**：2026-02-04  
**預估開發週期**：2-3 週
