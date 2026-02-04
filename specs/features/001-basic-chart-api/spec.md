---
milestone: M01
system_context: false
created: 2026-02-03
updated: 2026-02-04
---

# Feature Specification: 基礎繪圖與 API 格式

> **Feature ID**: 001-basic-chart-api  
> **Status**: Draft  
> **Milestone**: M01 — 基礎繪圖與 API 格式

---

## Clarifications

### Session 2026-02-04

- Q: 實際使用的資料表欄位結構 → A: 使用現有 `[股價即時].[dbo].[1分K]` 表結構，需查詢確認欄位名稱
- Q: K線時間粒度需求 → A: 聚合成日 K 線（從 `1分K` 計算 OHLC）
- Q: API 錯誤處理策略層級 → A: 標準化錯誤碼 + 詳細日誌（依 Spec Q2 建議）
- Q: Loading 狀態最小可見時間 → A: 300ms 最小顯示時間（避免閃爍）
- Q: 圖表資料快取策略 → A: 前端快取 5 分鐘（降低 API 負載）

---

## 1. Feature Overview

### 1.1 Problem Statement

**目前的痛點**：
- 缺乏視覺化工具來檢視台股歷史 K 線資料
- 無法進行互動式圖表操作（縮放、平移、查看細節）
- 沒有統一的 API 格式規範，未來擴充會造成前端解析邏輯修改
- 圖表載入過程缺乏明確的狀態提示，使用者體驗不佳

**為什麼需要這個 Feature？**
- 基礎圖表能力是整個「視覺化事件研究平台」的基石
- 符合 PRD Roadmap Phase 1 — DB + API 基礎
- 為後續的 Strategy Grid Mode 和 Micro Backtest 提供基礎設施

**影響範圍**：
- 前端：Vue 3 + TradingView Lightweight Charts
- 後端：FastAPI + MSSQL
- 資料庫：`[股價即時].[dbo].[1分K]` 表（需聚合為日 K 線）

### 1.2 Goal

**本 Feature 完成後，系統將具備**：

1. **基礎圖表渲染**：
   - 顯示標準的日 K 線圖（OHLC），符合台股顯示慣例（紅漲綠跌）
   - 成交量副圖，時間軸完全對齊

2. **圖表互動操作**：
   - 滑鼠滾輪縮放
   - 拖曳平移
   - 十字線查看 OHLC 與成交量數據

3. **小圖放大檢視**：
   - Grid 模式下任一小圖可點擊放大
   - 放大後保留所有互動操作能力
   - 支援返回 Grid 檢視

4. **載入狀態管理**：
   - Loading 指示器
   - 錯誤提示與重試機制
   - 無資料提示

5. **API Response 格式規範**：
   - 建立穩定的 API 格式，確保向下相容
   - 支援未來擴充（metrics 可新增欄位）

### 1.3 Success Criteria

| 指標 | 目標值 | 驗證方式 |
|------|--------|----------|
| K 線顯示正確性 | 100% 符合台股慣例（紅漲綠跌） | 視覺測試 + E2E 測試 |
| 成交量對齊精度 | 時間軸完全對齊（誤差 0） | 自動化測試 |
| 互動操作流暢度 | 60 FPS，無卡頓 | 效能測試 |
| 圖表渲染速度 | < 1 秒（100 根 K 線） | 效能測試 |
| API Response 一致性 | 100% 符合 Schema | JSON Schema 驗證 |
| 錯誤處理覆蓋率 | 涵蓋所有關鍵錯誤情境 | 單元測試 + 整合測試 |

---

## 2. User Stories

### US A-1: K 線與成交量基礎繪圖

**As a** 策略研究員  
**I want** 看到標準的日 K 線圖與成交量副圖  
**So that** 我能夠觀察股票的價格與成交量變化

#### Acceptance Criteria

**AC1 — K 線正確顯示**
- **Given** 系統載入了某股票（如 2330）的歷史資料
- **When** 圖表元件渲染完成
- **Then** 應顯示標準 OHLC K 線，紅漲綠跌（台股慣例）

**AC2 — 成交量副圖對齊**
- **Given** K 線圖已顯示
- **When** 系統渲染成交量資料
- **Then** 成交量應顯示在副圖區域，時間軸與 K 線完全對齊

**AC3 — 無資料時的處理**
- **Given** 查詢結果為空或資料不足
- **When** 圖表嘗試渲染
- **Then** 應顯示「無資料」提示，不應出現錯誤畫面

---

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

### US G-2: API Response 固定格式設計

**As a** 系統架構師  
**I want** API Response 有穩定的格式  
**So that** 未來新增功能時不需要修改前端解析邏輯

#### Acceptance Criteria

**AC1 — Response 必要欄位**
- **Given** 任何查詢 API 的回應
- **When** 前端接收 response
- **Then** 必須包含：`stock_code`, `chart_data` (dates, ohlc)

**AC2 — 擴充性設計**
- **Given** 未來需要新增統計指標（如 Sharpe Ratio）
- **When** 修改後端邏輯
- **Then** 可在 Response 中新增欄位，不影響既有欄位

**AC3 — 錯誤格式一致性**
- **Given** API 請求失敗（如 SQL 錯誤、逾時）
- **When** 系統回傳錯誤
- **Then** 應使用統一格式：`{ "error": { "code": "...", "message": "..." } }`

**AC4 — Response 範例文件**
- **Given** 開發者需要串接 API
- **When** 查閱 API 文件
- **Then** 應提供完整的 Response 範例（JSON）與欄位說明

**AC5 — 向下相容性承諾**
- **Given** 系統升級至新版本
- **When** API 新增功能
- **Then** 既有欄位的資料型別與語意不得改變（向下相容）

---

## 3. Assumptions

> 本 Feature 開發過程中做出的假設，需在實作前確認。

### 3.1 資料來源假設

- **已確認**：使用 `[股價即時].[dbo].[1分K]` 表作為資料來源
- **驗證方式**：查詢表結構確認欄位名稱對應（股票代碼、時間、OHLCV）
- **資料處理**：後端需將 1 分鐘 K 線聚合為日 K 線（以交易日為單位計算 OHLC）

### 3.2 技術棧假設

- **假設**：TradingView Lightweight Charts 支援台股紅漲綠跌設定
- **驗證方式**：建立簡單 POC 驗證 `upColor` 與 `downColor` 設定
- **若假設不成立**：評估其他圖表庫（如 ECharts、Highcharts）

### 3.3 效能假設

- **假設**：TradingView Lightweight Charts 在 Grid 模式下渲染 20+ 小圖的效能可接受
- **驗證方式**：效能測試（FPS、記憶體使用）
- **若假設不成立**：實作 Virtual Scrolling 或 Lazy Loading

### 3.4 API 設計假設

- **假設**：前端可接受 1-2 秒的 API 回應時間
- **驗證方式**：壓力測試與使用者體驗測試
- **若假設不成立**：實作快取機制或分頁載入

---

## 4. Out of Scope

> 明確列出本 Feature **不包含** 的功能，避免範疇蔓延。

| 功能 | 原因 |
|------|------|
| **條件查詢功能** | 延後至 M02（Strategy Grid 核心） |
| **多圖並列 Grid 渲染** | 延後至 M02（需先完成基礎圖表） |
| **事件日置中對齊** | 延後至 M02（需 Time Window Engine） |
| **時間窗口參數設定** | 延後至 M02（Time Window Engine） |
| **事件後績效統計** | 延後至 M03（Micro Backtest） |
| **Excel 報表匯出** | 延後至 M03（需先有統計數據） |
| **AI Text-to-SQL** | 延後至 M04（AI 協作增強） |
| **完整的 API 格式（含 metrics）** | M01 階段簡化版本，僅包含 chart_data |
| **使用者帳號系統** | PRD 明確列為非目標 |
| **技術指標系統（MA、MACD 等）** | PRD 明確列為非目標 |

---

## 5. Dependencies

### 5.1 外部依賴

| 依賴項 | 版本 | 用途 |
|--------|------|------|
| Vue 3 | ^3.4.0 | 前端 UI 框架 |
| TradingView Lightweight Charts | ^4.1.0 | 圖表渲染 |
| FastAPI | ^0.110.0 | 後端 API 框架 |
| pyodbc | ^5.0.0 | MSSQL 連線 |
| Microsoft SQL Server | 2019+ | 資料庫 |

### 5.2 內部依賴

| 依賴項 | 說明 | 狀態 |
|--------|------|------|
| `stock_daily` 表 | OHLCV 資料來源 | ⚠️ 需確認 Schema |
| MSSQL 連線設定 | 後端資料庫連線 | ⚠️ 需配置 |
| 前端專案初始化 | Vue 3 專案結構 | ⚠️ 需建立 |
| 後端專案初始化 | FastAPI 專案結構 | ⚠️ 需建立 |

---

## 6. Open Questions

> 需在實作前確認的問題。

### Q1: 資料表欄位結構 ✅ 已釐清

**決議**：使用現有 `[股價即時].[dbo].[1分K]` 表

**後續動作**：
1. 查詢表結構確認實際欄位名稱
   ```sql
   SELECT TOP 5 * FROM [股價即時].[dbo].[1分K]
   ```
2. 建立欄位對應文件（`data-model.md`）
3. 實作日 K 線聚合邏輯（以交易日為分組，計算 Open/High/Low/Close/Volume）

---

### Q2: API Endpoint 設計 ✅ 已釐清

**決議**：採用標準化錯誤碼 + 詳細日誌策略

**API 規格**：
- Endpoint: `GET /api/v1/chart-data`
- Query Parameters:
  - `stock_code` (required): 股票代碼
  - `start_date` (required): 起始日期 (YYYY-MM-DD)
  - `end_date` (required): 結束日期 (YYYY-MM-DD)
- 錯誤回應格式:
  ```json
  {
    "error": {
      "code": "INVALID_STOCK_CODE",
      "message": "股票代碼不存在",
      "details": "Stock code '9999' not found in database"
    }
  }
  ```
- 錯誤碼定義:
  - `INVALID_STOCK_CODE`: 股票代碼不存在
  - `INVALID_DATE_RANGE`: 日期範圍不合法
  - `NO_DATA`: 查詢結果為空
  - `INTERNAL_ERROR`: 伺服器錯誤
- 日誌策略：所有錯誤 MUST 記錄到 `logs/` 目錄，包含 request_id、錯誤堆疊、查詢參數

---

### Q3: Loading Spinner 樣式 ✅ 已釐清

**決議**：採用 300ms 最小顯示時間策略

**UI 規格**：
- 動畫：Circular Spinner（圓形旋轉）
- 顏色：Primary Color (#1976d2)
- 尺寸：40x40px
- 文案：「載入中...」
- **最小可見時間**：300ms（避免閃爍效應）
  - 若 API 回應時間 < 300ms，Loading 仍顯示至 300ms
  - 若 API 回應時間 ≥ 300ms，API 回應後立即隱藏

---

### Q4: 小圖放大動畫

**問題**：是否需要過場動畫？動畫時長？

**建議方案**：
- 是否需要：是（提升使用者體驗）
- 動畫類型：Fade + Scale
- 動畫時長：200ms
- Easing：ease-in-out

**決策者**：UI/UX Designer  
**期限**：開發階段

---

## 7. Technical Notes

### 7.1 台股特殊規範

**紅漲綠跌**：
- 台股慣例與國際相反
- TradingView Lightweight Charts 預設為「綠漲紅跌」
- 需調整 `upColor` 與 `downColor` 設定

**範例程式碼**：
```javascript
const candlestickSeries = chart.addCandlestickSeries({
  upColor: '#ef5350',      // 紅色（漲）
  downColor: '#26a69a',    // 綠色（跌）
  borderVisible: false,
  wickUpColor: '#ef5350',
  wickDownColor: '#26a69a',
});
```

### 7.2 效能考量

**日 K 線聚合策略**：
- 資料來源：`[股價即時].[dbo].[1分K]`（1 分鐘 K 線）
- 聚合邏輯：
  - Open：當日第一根 1 分 K 的 Open
  - High：當日所有 1 分 K 的最高 High
  - Low：當日所有 1 分 K 的最低 Low
  - Close：當日最後一根 1 分 K 的 Close
  - Volume：當日所有 1 分 K 的 Volume 總和
- 實作位置：後端 Service 層（避免前端重複計算）

**快取策略**：
- **前端快取**：5 分鐘 TTL（降低 API 負載）
- 快取鍵：`chart_data:{stock_code}:{start_date}:{end_date}`
- 實作方式：瀏覽器 Memory Cache（localStorage 可選）
- M01 階段不實作後端快取（避免增加基礎設施複雜度）

**Loading 狀態管理**：
- 最小可見時間：300ms（避免閃爍效應）
- 實作方式：前端 `setTimeout` 延遲隱藏

**Grid 模式渲染效能**：
- 需考慮大量小圖（20+）的渲染效能
- 建議實作策略：
  - Virtual Scrolling（僅渲染可見區域）
  - Lazy Loading（滾動時動態載入）
  - Canvas 渲染（避免大量 DOM 元素）

**M01 階段處理**：
- US A-3 實作小圖放大功能
- 效能優化可延後至 M02（實際 Grid 模式實作時）

### 7.3 Roadmap 對應

**M01 對應 Phase 1 — DB + API 基礎**

| Phase | 任務 | M01 狀態 |
|-------|------|----------|
| Phase 1 | DB + API 基礎 | ✅ **本 Feature** |
| Phase 2 | Grid + Event Anchoring | ⏸️ M02 規劃 |
| Phase 2.5 | Time Window Engine | ⏸️ M02 規劃 |
| Phase 3 | Micro Backtest + Excel | ⏸️ M03 規劃 |
| Phase 4 | AI Text-to-SQL | ⏸️ M04 規劃 |

---

## 8. Next Steps

### ✅ 當前已完成
- [x] Feature Spec 撰寫完成
- [x] User Stories 定義完成
- [x] Assumptions 與 Open Questions 識別

### 🚀 建議的後續步驟

1. **確認 Open Questions（Q1-Q5）**
   - 由 Tech Lead、PM、Designer 決策

2. **建立資料模型文件**
   ```
   創建 specs/features/001-basic-chart-api/data-model.md
   ```

3. **建立 API 契約文件**
   ```
   創建 specs/features/001-basic-chart-api/contracts/chart-api.md
   ```

4. **執行 SpecKit Plan 階段**
   ```
   /speckit.plan
   ```

5. **技術準備**
   - 建立前後端專案結構
   - 安裝必要套件
   - 設定開發環境

---

**文件版本**：v1.0.0  
**產生工具**：SpecKit Specify  
**維護者**：AI Development Team
