# System Specification: Taiwan Market Time Machine（台股時光機）

> **Version**: 0.3.0  
> **Last Updated**: 2026-02-09  
> **Status**: Active Development  
> **Maintained By**: AI Development Team

---

## 1. Overview

### 1.1 System Purpose

本系統為**視覺化事件研究平台**，專注於台股歷史資料的視覺化分析與策略研究。

核心能力：
1. **基礎圖表功能**：提供日 K 線圖表繪製與資料查詢 API
2. **資料聚合處理**：從 1 分 K 線聚合為日 K 線（OHLC + 成交量）
3. **API 格式規範**：統一的 API Response 格式，支援向下相容與擴充
4. **前端視覺化**：提供互動式圖表介面，支援縮放、平移、十字線查詢
5. **Grid 多圖檢視**：支援同時顯示多個股票圖表，並可點擊放大

### 1.2 Scope

本系統涵蓋：
- 台股日 K 線資料查詢與聚合
- RESTful API 服務（FastAPI 實作）
- 標準化的 API Response 格式與錯誤處理
- 資料庫連線管理（MSSQL Server）
- 前端互動式圖表應用（Vue 3 + TradingView Lightweight Charts）
- 桌面應用程式（Electron）

### 1.3 Target Users

| 角色 | 使用目的 |
|------|----------|
| **策略研究員** | 透過圖表介面進行視覺化分析，使用互動功能深入檢視價格細節 |
| **系統架構師** | 使用穩定的 API 格式設計前端應用 |
| **開發者** | 基於 API 契約開發新功能 |

---

## 2. User Stories

### US-SYS-1: K 線與成交量基礎繪圖

**As a** 策略研究員  
**I want** 透過 API 取得日 K 線圖與成交量資料  
**So that** 我能夠觀察股票的價格與成交量變化

#### Acceptance Criteria

**AC1 — K 線資料正確聚合**
- **Given** 系統查詢某股票（如 2330）的 1 分 K 線資料
- **When** 執行日 K 線聚合邏輯
- **Then** 應正確計算 OHLC（開盤、最高、最低、收盤、成交量）

**AC2 — API 回應格式正確**
- **Given** API 接收到合法的查詢請求
- **When** 系統處理資料並回應
- **Then** 回應格式應符合 `ChartResponse` 定義，包含 `stock_code`, `chart_data[]`, `metadata`

**AC3 — 無資料時的處理**
- **Given** 查詢結果為空（股票代碼不存在或日期範圍外）
- **When** API 回應
- **Then** 應回傳空的 `chart_data[]` 陣列，`data_points` 為 0，HTTP 狀態碼為 200

**來源**：Feature 001-basic-chart-api (US A-1)

---

### US-SYS-3: 圖表互動操作

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

**來源**：Feature 002-frontend-chart-interactions (US A-2)

---

### US-SYS-4: Grid 多圖檢視與放大

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

**來源**：Feature 002-frontend-chart-interactions (US A-3)

---

### US-SYS-5: 圖表載入狀態與錯誤處理

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

**來源**：Feature 002-frontend-chart-interactions (US A-4)

---

### US-SYS-2: API Response 固定格式設計

**As a** 系統架構師  
**I want** API Response 有穩定的格式  
**So that** 未來新增功能時不需要修改前端解析邏輯

#### Acceptance Criteria

**AC1 — Response 必要欄位**
- **Given** 任何圖表查詢 API 的回應
- **When** 前端接收 response
- **Then** 必須包含：`stock_code`, `chart_data[]`, `metadata`

**AC2 — 擴充性設計**
- **Given** 未來需要新增統計指標（如技術指標、績效統計）
- **When** 修改後端邏輯
- **Then** 可在 Response 中新增欄位，既有欄位的資料型別與語意不得改變

**AC3 — 錯誤格式一致性**
- **Given** API 請求失敗（參數錯誤、資料庫錯誤、內部錯誤）
- **When** 系統回傳錯誤
- **Then** 應使用統一格式：`ErrorResponse` 模型（包含 `code`, `message`, `details`）

**AC4 — Response 範例文件**
- **Given** 開發者需要串接 API
- **When** 查閱 API 契約文件
- **Then** 應提供完整的 Request/Response 範例與欄位說明

**AC5 — 向下相容性承諾**
- **Given** 系統升級至新版本
- **When** API 新增功能
- **Then** 既有欄位的資料型別與語意不得改變（Backward Compatible）

**來源**：Feature 001-basic-chart-api (US G-2)

---

## 3. Behaviors

### 3.1 圖表資料查詢

| 操作 | 前置條件 | 結果 |
|------|----------|------|
| `GET /api/chart/daily` | 有效的 `stock_code`, `start_date`, `end_date` | 回傳 `ChartResponse` 包含日 K 線資料 |
| `GET /api/chart/daily` | 無效的日期範圍（start > end） | HTTP 400，`ErrorResponse` (code: INVALID_DATE_RANGE) |
| `GET /api/chart/daily` | 查無資料 | HTTP 200，`chart_data[]` 為空，`data_points: 0` |

### 3.2 前端圖表互動

| 操作 | 前置條件 | 結果 |
|------|----------|------|
| 滑鼠滾輪縮放 | 圖表已載入顯示 | 以滑鼠位置為中心進行縮放（0.1x - 10x） |
| 拖曳平移 | 圖表已載入顯示，按住左鍵 | 圖表跟隨滑鼠移動進行平移 |
| 十字線顯示 | 滑鼠移動到 K 線上 | 顯示 OHLCV 數據與位置資訊 |
| Grid 小圖點擊 | Grid 模式下顯示多個圖表 | 展開為全螢幕模態視窗 |
| ESC 鍵關閉 | 模態視窗已展開 | 返回 Grid 多圖檢視 |

### 3.3 日 K 線聚合邏輯

**輸入**：1 分 K 線資料（List[Tuple]）  
**輸出**：日 K 線資料（Dict[date, OHLCV]）

**演算法**：
1. 按日期（交易日）分組 1 分 K 線資料
2. 每日第一筆的 `open` 作為當日開盤價
3. 每日所有 `high` 取最大值作為當日最高價
4. 每日所有 `low` 取最小值作為當日最低價
5. 每日最後一筆的 `close` 作為當日收盤價
6. 每日所有 `volume` 加總作為當日成交量

**實作位置**：`src/services/chart_service.py::_aggregate_to_daily()`

### 3.4 前端狀態管理

**圖表載入狀態** (ChartLoadingState)：
- `idle`: 初始狀態，尚未開始載入
- `loading`: 正在從 API 取得資料
- `success`: 資料載入成功，圖表已渲染
- `error`: 載入失敗，顯示錯誤訊息

**實作位置**：`frontend/src/composables/useChartData.ts`

### 3.5 日期範圍驗證

| 驗證項目 | 規則 | 失敗時行為 |
|----------|------|-----------|
| 日期格式 | 必須為 ISO 8601 (YYYY-MM-DD) | 回傳 `INVALID_DATE_FORMAT` |
| 日期範圍 | `start_date` ≤ `end_date` | 回傳 `INVALID_DATE_RANGE` |
| 未來日期 | 不接受未來日期 | 回傳 `INVALID_DATE_RANGE` |

---

## 4. Data Definitions

詳見 [data-model.md](./data-model.md)

**核心模型**：
- `ChartDataPoint`: 單一時間點的 OHLCV 資料
- `ChartResponse`: API 回應格式
- `ChartMetadata`: 查詢結果元資料
- `ErrorResponse`: 統一錯誤格式

---

## 5. Error Handling

### 5.1 API 錯誤碼規範

| 錯誤碼 | HTTP Status | 說明 | 範例情境 |
|--------|-------------|------|----------|
| `INVALID_STOCK_CODE` | 400 | 股票代碼格式錯誤 | 代碼包含非數字字元 |
| `INVALID_DATE_RANGE` | 400 | 日期範圍不合法 | start_date > end_date |
| `INVALID_DATE_FORMAT` | 400 | 日期格式錯誤 | 非 YYYY-MM-DD 格式 |
| `NO_DATA` | 200 | 查無資料（非錯誤） | 股票代碼不存在或日期範圍外 |
| `DATABASE_ERROR` | 500 | 資料庫連線或查詢錯誤 | SQL Server 連線失敗 |
| `INTERNAL_ERROR` | 500 | 伺服器內部錯誤 | 未預期的例外 |

### 5.2 錯誤回應格式

所有錯誤 MUST 使用 `ErrorResponse` 模型：

```json
{
  "detail": {
    "error": {
      "code": "INVALID_DATE_RANGE",
      "message": "參數驗證錯誤",
      "details": "起始日期 (2024-01-31) 不得大於結束日期 (2024-01-01)"
    }
  }
}
```

---

## 6. External Interfaces

詳見 [contracts/](./contracts/) 目錄。

**已定義契約**：
- `chart-api.md`: 圖表資料查詢 API 契約

---

## 7. Version History

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 0.3.0 | 2026-02-09 | **新增前端功能模組**<br>- 新增 US-SYS-3（圖表互動）、US-SYS-4（Grid檢視）、US-SYS-5（載入狀態）<br>- 新增前端行為定義（3.2）與狀態管理（3.4）<br>- 更新系統範疇：Vue 3 + Electron 桌面應用<br>來源：Feature 002-frontend-chart-interactions |
| 0.2.0 | 2026-02-04 | 新增 US-SYS-1（K線查詢）、US-SYS-2（API格式）<br>新增錯誤碼規範、日期驗證規則<br>定義日K聚合演算法 |
| 0.1.0 | 2026-02-03 | 初始版本（空白範本）|
