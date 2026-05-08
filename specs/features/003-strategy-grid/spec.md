---
milestone: M03
system_context: true
status: In Progress  # 允許值: Draft | In Progress | Implemented | Unified
created: 2026-03-02
updated: 2026-03-02
implement_baseline_commit: "fe4433a"
---

# Feature Specification: Strategy Grid 核心

> **Feature ID**: 003-strategy-grid  
> **Status**: In Progress

---

## 1. Feature Overview

### 1.1 Problem Statement

策略研究員在進行事件研究時，需要同時比對大量股票樣本在特定事件前後的價格型態。目前系統（M01/M02）僅支援單一股票的 K 線瀏覽，缺乏批次篩選與多圖並列能力，導致研究員必須逐一開啟每檔股票才能比較型態，效率極低。

核心痛點：
- 無法依照條件（股票代碼、日期、價格範圍）篩選符合型態的事件樣本
- 無法同時渲染多個樣本供視覺比對
- 多樣本事件日不對齊，難以橫向比較

### 1.2 Goal

本 Feature 完成後，研究員可以：
1. 透過結構化條件（股票代碼、日期範圍、價格範圍、AND/OR 邏輯）批次篩選事件樣本
2. 以 Grid 多圖並列佈局同時檢視最多 100 個 K 線小圖
3. 所有小圖以事件日為中心自動對齊，直觀比較事件前後型態
4. 查詢結果超過單頁限制時分頁瀏覽，確保系統效能穩定

### 1.3 Success Criteria

| 指標 | 目標值 | 驗證方式 |
|------|--------|----------|
| 條件查詢回應速度 | 研究員輸入條件後 5 秒內看到結果摘要 | 計時查詢到顯示樣本數量的完整流程 |
| Grid 渲染效能 | 50 個 K 線小圖在 3 秒內完成渲染 | 計時 Grid 切換到全部小圖可見的時間 |
| 事件日置中對齊正確率 | 100% 的小圖事件日位於圖表水平中心 | 視覺驗證或自動化比對事件日位置 |
| 分頁切換流暢度 | 下一頁載入時間在 3 秒內完成 | 計時分頁切換到 Grid 重新渲染的時間 |
| 大量查詢記憶體穩定性 | 查詢 100 個樣本後系統不崩潰或記憶體異常 | 執行滿負載查詢並觀察系統穩定性 |

---

## Clarifications

### Session 2026-03-02

- Q: `stock_events` 資料表由誰填入？ → A: 資料庫預載，M03 只負責查詢與篩選，不需建立或匯入事件記錄
- Q: 事件日前後交易日天數（pre/post days）如何決定？ → A: 系統預設常數（pre=20, post=10），M03 不提供 UI 調整介面，M04 才開放
- Q: 使用者輸入無效查詢條件時如何處理？ → A: 前端即時驗證，禁止提交並顯示欄位旁錯誤提示
- Q: QueryPanel 配置方式？ → A: 固定頂部，查詢條件區在上，Grid 多圖區在下
- Q: `event_type` 是否可作為 US B-1 的查詢條件？ → A: 不可以，M03 不以 event_type 篩選，明確列為 Out of Scope

---

## 2. User Stories

### US B-1: 結構化條件查詢

> TD Ref: TD-001

**As a** 策略研究員  
**I want** 透過結構化條件篩選符合特定型態的股票樣本  
**So that** 我能夠找到符合研究假設的事件案例

#### Acceptance Criteria

**AC1 — 基礎條件輸入**
- **Given** 使用者在查詢介面
- **When** 輸入股票代碼（4-10 字元，含大寫英文）、日期範圍、價格範圍等條件
- **Then** 系統應產生對應的查詢並執行，回傳符合條件的樣本清單

**AC2 — 條件邏輯組合**
- **Given** 使用者設定多個查詢條件
- **When** 使用 AND/OR 邏輯組合條件
- **Then** 系統應正確解析複合條件並執行，結果符合邏輯語意

**AC3 — 查詢結果預覽**
- **Given** 查詢執行完成且有符合結果
- **When** 系統取得結果
- **Then** 應顯示符合條件的樣本數量與每筆基本資訊（股票代碼、事件日期）

**AC4 — 無結果處理**
- **Given** 使用者設定的條件過於嚴格
- **When** 查詢結果為空
- **Then** 應向使用者顯示「無符合條件的樣本」提示，並提供放寬條件的建議

**AC5 — 條件格式驗證** [NEW]
- **Given** 使用者在 QueryPanel 填寫查詢條件
- **When** 填入無效條件（如 date_from 晚於 date_to、股票代碼格式不符 4-10 字元規則）
- **Then** 前端應即時在欄位旁顯示錯誤提示，並禁止提交查詢直到條件格式正確

---

### US B-2: Grid 多圖並列顯示

> TD Ref: TD-002

**As a** 策略研究員  
**I want** 以 4x5 或更多的 Grid 佈局同時檢視多個樣本  
**So that** 我能夠快速批次比較不同樣本的型態

#### Acceptance Criteria

**AC1 — Grid 佈局渲染**
- **Given** 查詢取得多個樣本（最多 100 個）
- **When** 使用者切換到 Grid 模式
- **Then** 應以預設 4 欄 × 5 列的 Grid 佈局顯示所有小圖，每張小圖對應一個樣本

**AC2 — Grid 尺寸可調整 [MODIFIED]**
- **Given** Grid 模式已啟動
- **When** 使用者透過欄數選擇器調整欄數（可選值：2、4、6 欄；預設 4 欄；[UI-TBD: Adjustable Grid Control]，Phase 6 UI Gate 定案具體元件）
- **Then** Grid 應依新欄數設定重新排列，每個小圖尺寸相應等比縮放

**AC3 — 高效能渲染**
- **Given** Grid 包含 50 個以上小圖
- **When** 系統渲染 Grid
- **Then** 全部小圖完成渲染的時間應在 3 秒以內，期間不應出現明顯卡頓

**AC4 — 小圖資訊標籤**
- **Given** 每個小圖已渲染
- **When** 使用者檢視 Grid
- **Then** 每個小圖應顯示對應的股票代碼與事件日期標籤

---

### US B-3: 事件日置中對齊

**As a** 策略研究員  
**I want** 所有 Grid 小圖的事件日都置中對齊  
**So that** 我能夠直觀比較事件前後的價格型態

#### Acceptance Criteria

**AC1 — 事件日居中計算**
- **Given** 每個樣本有明確的事件日期
- **When** 系統計算圖表的顯示範圍
- **Then** 事件日應位於圖表的水平中心位置（交易日計算，非日曆日）

**AC2 — 事件前後資料對稱**
- **Given** 系統預設事件前 20 個交易日（pre=20）、事件後 10 個交易日（post=10）
- **When** 系統渲染每張小圖
- **Then** 事件日左側應顯示最多 20 根 K 線，右側應顯示最多 10 根 K 線

**AC3 — 資料不足時的處理**
- **Given** 某樣本的事件前或事件後資料不足（如股票上市未滿 20 交易日）
- **When** 系統嘗試渲染該小圖
- **Then** 應顯示實際可用資料，並在小圖上標示「資料不完整」提示

---

### US B-4: 查詢結果數量限制與分頁

**As a** 策略研究員  
**I want** 查詢結果數量過多時能分頁檢視  
**So that** 系統效能不會因大量資料而降低

#### Acceptance Criteria

**AC1 — 單次載入數量限制**
- **Given** 查詢結果超過 100 個樣本
- **When** 系統載入 Grid
- **Then** 應一次只顯示前 100 個樣本，並向使用者提示還有更多結果尚未載入

**AC2 — 分頁導航**
- **Given** 查詢結果已超過單頁上限（100 筆）並分頁
- **When** 使用者點擊「下一頁」或輸入目標頁碼
- **Then** 應載入對應頁次的樣本並更新 Grid 顯示

**AC3 — 分頁狀態顯示**
- **Given** 查詢結果已分頁
- **When** 使用者檢視 Grid 介面
- **Then** 應清楚顯示當前頁次與總頁數（例如「第 1 / 5 頁，共 472 筆樣本」）

---

## 3. Assumptions

1. `stock_daily` 與 `stock_events` 資料表已存在於後端資料庫，且用於查詢的欄位（股票代碼、事件日期、OHLCV）已可存取
2. 股票代碼採用較寬鬆的驗證規則：4-10 字元，允許數字與大寫英文（對齊 CONFLICT-001 決策，涵蓋 ETF 代碼如 006208）
3. M01/M02 已交付的 K 線渲染能力（TradingView Lightweight Charts）可被 Grid 小圖複用
4. 事件前後天數計算基準為**台灣股市交易日（Trading Days）**，非日曆日
5. 查詢效能目標（3 秒內渲染 50 圖）假設使用者在正常網路條件下操作
6. M03 查詢 API 回傳格式僅包含 M03 範圍欄位（樣本清單 + 分頁 metadata），`event_window`/`horizons`/`metrics` 為選填欄位，留給 M04/M05 填入（CONFLICT-002 建議方案 A）
7. `stock_events` 為資料庫預載的唯讀資料，M03 不需提供事件建立、編輯或匯入功能
8. 事件日前後天數採系統預設常數（pre=20 交易日、post=10 交易日），M03 不提供使用者調整介面；此設定將在 M04 Time Window Engine 開放 UI 控制

---

## 4. Key Entities

### 4.1 StockEvent（事件樣本）

| 欄位 | 型別 | 說明 |
|------|------|------|
| stock_code | String (4-10 chars) | 股票代碼，含大寫英文與數字 |
| event_date | Date | 事件日期（交易日） |
| event_type | String | 事件類型標籤（可選，僅供顯示用途；M03 不以此欄位篩選）|

### 4.2 StrategyQueryParams（查詢條件 DTO）

| 欄位 | 型別 | 說明 |
|------|------|------|
| stock_codes | String[] | 股票代碼清單（選填，空則查全部） |
| date_from | Date | 事件日期範圍起始 |
| date_to | Date | 事件日期範圍結束 |
| price_min | Decimal | 事件日收盤最低價（選填） |
| price_max | Decimal | 事件日收盤最高價（選填） |
| logic | Enum: AND/OR | 條件組合邏輯 |

### 4.3 GridQueryResponse（查詢回應）

| 欄位 | 型別 | 說明 |
|------|------|------|
| samples | SampleResult[] | 符合條件的樣本清單 |
| total_count | Integer | 符合條件的樣本總數 |
| page | Integer | 當前頁碼（從 1 起算） |
| total_pages | Integer | 總頁數 |
| page_size | Integer | 每頁最大樣本數（預設 100） |

### 4.4 SampleResult（單筆樣本）

| 欄位 | 型別 | 說明 |
|------|------|------|
| stock_code | String | 股票代碼 |
| event_date | Date | 事件日期 |
| chart_data | OHLCV[] | 事件日前後 K 線資料（交易日對齊） |
| data_complete | Boolean | 事件前後資料是否完整 |

> **完整欄位定義見** `data-model.md § SampleResult`（含 plan 階段精鍊新增的 `event_bar_index: int` 欄位，供前端 TradingView `setVisibleLogicalRange()` 置中渲染使用）。

---

## 5. Dependencies

- **資料庫表格**：`stock_daily`（日 OHLCV 資料）、`stock_events`（事件資料）— 需確認表格 schema 與存取權限
- **既有 K 線渲染能力**：M02 已交付的圖表渲染元件，Grid 小圖複用此能力
- **台灣交易日曆**：計算事件前後交易日數量，需有交易日曆資料來源或工具函式

---

## 6. UI/UX 影響評估

| 項目 | 值 |
|------|-----|
| **UI Impact** | High |
| **UI Maturity Target** | L0 |
| **涉及畫面** | [UI-TBD: Strategy Grid View — 新畫面，含查詢條件區域與 Grid 多圖並列區域] |
| **涉及模式** | [UI-TBD: Grid Layout Pattern — 可調整欄列數的多圖佈局互動模式] |
| **涉及狀態** | [UI-TBD: Loading（Grid 渲染中）、Empty（查詢無結果）、Error（查詢失敗）、Partial（資料不完整小圖）] |
| **UI Unknowns** | 1. Grid 小圖的最小/最大尺寸限制是否有設計規範（L0 暫不需定案） |

### UI References

| UI ID | 類型 | 說明 | 所屬 User Story |
|-------|------|------|-----------------|
| [UI-TBD: UI-SCR-002] | Screen | Strategy Grid View — 固定頂部佈局：QueryPanel 在上、Grid 多圖區在下 | US B-2, US B-3, US B-4 |
| [UI-TBD: UI-CMP-002] | Component | QueryPanel — 條件查詢輸入元件 | US B-1 |
| [UI-TBD: UI-CMP-003] | Component | MiniChart — Grid 小圖元件（事件置中版） | US B-2, US B-3 |

---

## 7. Out of Scope

以下項目不在本 Feature 範圍內：

1. **Time Window Engine**（M04）：全 Grid 時間窗口一致化設定（`event_window` pre/post days）由使用者動態調整 — 本 Feature 使用固定預設值
2. **Micro Backtest 統計**（M05）：事件後報酬率計算、勝率、最大回撤等統計數值
3. **Grid 資料匯出**（M05 US E-1）：Grid 樣本匯出為 Excel/CSV
4. **AI 條件生成**（未來 US）：以自然語言描述條件由 AI 轉換為結構化查詢
5. **查詢結果快取**（US G-1）：查詢結果持久化快取機制（本 Feature 需預留 hook 但不實作）
6. **事件日標記線視覺化**（M04）：在 K 線圖上畫出事件日的垂直標記線
7. **以 `event_type` 篩選事件**：`StrategyQueryParams` 不包含 event_type 過濾欄位，事件類型僅作為 StockEvent 的展示屬性，留待後續 Milestone 評估
