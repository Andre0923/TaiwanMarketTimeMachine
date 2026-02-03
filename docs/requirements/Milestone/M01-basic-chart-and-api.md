# Milestone 01 — 基礎繪圖與 API 格式

> **建立日期**：2026-02-03  
> **狀態**：⏳ 規劃中  
> **預估規模**：5 個 User Story（Group A + US G-2）  

---

## 能力邊界說明

### 本 Milestone 完成後具備的能力

- **基礎圖表渲染**：能夠顯示標準的日 K 線圖與成交量副圖，符合台股顯示慣例
- **圖表互動操作**：支援滑鼠滾輪縮放、拖曳平移、十字線查看詳細數據
- **小圖放大檢視**：Grid 模式下任一小圖可點擊放大至主檢視區域
- **載入狀態管理**：完整的載入中、錯誤提示、重試機制
- **API 格式規範**：建立穩定的 API Response 格式，確保向下相容性

### 下一 Milestone 將擴展的方向

- **Strategy Grid 模式**：多圖並列顯示、條件查詢、事件置中對齊（M02）
- **Time Window Engine**：統一時間窗口管理、事件日標記（M02）
- **Micro Backtest**：事件後績效統計與分析（M03）

> ⚠️ **邊界聲明**：本 Milestone 不涵蓋「條件查詢」、「多圖並列 Grid」、「績效統計」功能，相關功能將於後續 Milestone 實作。本階段重點在確保基礎圖表能力穩定運作，並建立 API 規範基礎。

---

## 包含的 User Stories

> ⚠️ **優先權宣告**：若本 Milestone 的 User Story 或 AC 與 Full User Story List 有差異，**以本 Milestone 內容為準**。

---

### US A-1: K 線與成交量基礎繪圖

**As a** 策略研究員  
**I want** 看到標準的日 K 線圖與成交量副圖  
**So that** 我能夠觀察股票的價格與成交量變化

#### Acceptance Criteria

**AC1 — K 線正確顯示**
- **Given** 系統載入了某股票的歷史資料
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
- **Then** 必須包含：`event_window` (pre/post), `horizons` (觀察期), `samples` (樣本清單), `metrics` (統計指標)

**AC2 — 擴充性設計**
- **Given** 未來需要新增統計指標（如 Sharpe Ratio）
- **When** 修改後端邏輯
- **Then** 只需在 `metrics` 物件內新增欄位，不影響既有欄位

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

## 延後的 User Stories

> 以下 User Story 因故未納入本 Milestone，將於後續規劃。

| US ID | 原因 |
|-------|------|
| US B-1 ~ B-4 | Strategy Grid 功能需先完成基礎圖表能力 |
| US C-1 ~ C-4 | Time Window Engine 依賴 Grid 模式 |
| US D-1 ~ D-5 | Micro Backtest 需先有事件研究基礎 |
| US E-1 | 資料匯出需先有統計數據 |
| US F-1 ~ F-2 | AI 協作為進階功能，延後實作 |
| US G-1 | 快取機制在有實際查詢後再優化 |

---

## 與 Full User Story List 差異對照

> 本區塊列出本 Milestone 與原始 User Story 之間的差異（若無差異可省略）

| US ID | 差異類型 | 說明 |
|-------|----------|------|
| US A-1 | 無變更 | — |
| US A-2 | 無變更 | — |
| US A-3 | 無變更 | — |
| US A-4 | 無變更 | — |
| US G-2 | 無變更 | — |

---

## Milestone 摘要

| US ID | 摘要 | 來源 Group | AC 數量 |
|-------|------|------------|---------|
| US A-1 | K 線與成交量基礎繪圖 | A | 3 |
| US A-2 | 圖表互動操作 | A | 3 |
| US A-3 | 小圖點擊放大檢視 | A | 3 |
| US A-4 | 圖表載入狀態與錯誤處理 | A | 3 |
| US G-2 | API Response 固定格式設計 | G | 5 |

**總計**：5 個 User Story，17 條 Acceptance Criteria

---

## 執行建議

### 建議開發順序

1. **US G-2**：優先建立 API 格式規範與範例文件（無依賴，可先行）
2. **US A-1**：基礎圖表渲染能力（核心功能）
3. **US A-2**：圖表互動操作（依賴 US A-1）
4. **US A-4**：載入狀態管理（可與 US A-1/A-2 平行）
5. **US A-3**：小圖放大功能（依賴 US A-1/A-2，最後實作）

### 技術準備

- **前端**：Vue 3 專案初始化、TradingView Lightweight Charts 套件安裝
- **後端**：FastAPI 專案初始化、MSSQL 連線設定
- **資料庫**：`stock_daily` 表準備（至少包含一檔股票的歷史資料供測試）

### 風險項目

| 風險 | 影響 | 緩解措施 |
|------|------|----------|
| TradingView Lightweight Charts 學習曲線 | 開發時程延遲 | 先完成簡單範例驗證可行性 |
| API 格式設計不夠彈性 | 未來需大幅修改 | 參考業界標準（如 JSON:API）並進行技術評審 |
| MSSQL 資料結構不明確 | 後端實作困難 | 優先定義 `stock_daily` 表 Schema |

---

## 變更記錄

| 日期 | 變更類型 | 說明 |
|------|----------|------|
| 2026-02-03 | 初始建立 | 建立 Milestone 01，包含 Group A + US G-2 |

---

## 下一步

- [ ] 將本 Milestone 交付 SpecKit 進行 Feature 開發
- [ ] 執行 `/flowkit.Milestone-context` 從 PRD 擷取設計上下文
- [ ] 執行 `/speckit.specify` 進入 Spec 階段
