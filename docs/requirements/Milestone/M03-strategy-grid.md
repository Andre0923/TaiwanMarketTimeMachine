# Milestone 03 — Strategy Grid 核心

> **建立日期**：2026-02-26  
> **狀態**：🧩 執行中  
> **預估規模**：4 個 User Story  

---

## 能力邊界說明

### 本 Milestone 完成後具備的能力

- **批次條件查詢**：研究員可透過結構化條件（股票代碼、日期、價格範圍、邏輯組合）篩選符合型態的事件樣本
- **Grid 多圖並列**：查詢結果以 4x5（可調整）Grid 佈局同時渲染多個 K 線小圖
- **事件日置中對齊**：所有 Grid 小圖依事件日自動對齊，方便跨樣本視覺比對
- **分頁結果管理**：超量查詢結果分頁呈現，避免一次載入過多樣本造成效能問題

### 下一 Milestone 將擴展的方向

- **Time Window Engine**（Group C）：全 Grid 時間窗口一致化設定、事件日標記線
- **Micro Backtest 統計**（Group D）：基於 Grid 樣本進行事件後報酬計算與統計彙總

> ⚠️ **邊界聲明**：本 Milestone 不涵蓋 Time Window 參數設定（Group C）、報酬統計計算（Group D），相關功能將於後續 Milestone 實作。

---

## 包含的 User Stories

> ⚠️ **優先權宣告**：若本 Milestone 的 User Story 或 AC 與 Full User Story List 有差異，**以本 Milestone 內容為準**。

---

### US B-1: 結構化條件查詢

**As a** 策略研究員  
**I want** 透過結構化條件篩選符合特定型態的股票樣本  
**So that** 我能夠找到符合研究假設的事件案例

#### Acceptance Criteria

**AC1 — 基礎條件輸入**
- **Given** 使用者在查詢介面
- **When** 輸入股票代碼、日期範圍、價格範圍等條件
- **Then** 系統應產生對應的 SQL 查詢並執行

**AC2 — 條件邏輯組合**
- **Given** 使用者設定多個條件
- **When** 使用 AND/OR 邏輯組合條件
- **Then** 系統應正確解析並執行複合查詢

**AC3 — 查詢結果預覽**
- **Given** 查詢執行完成
- **When** 系統取得結果
- **Then** 應顯示符合條件的樣本數量與基本資訊（股票代碼、事件日期）

**AC4 — 無結果處理**
- **Given** 查詢條件過於嚴格
- **When** 查詢結果為空
- **Then** 應顯示「無符合條件的樣本」提示，並建議放寬條件

---

### US B-2: Grid 多圖並列顯示

**As a** 策略研究員  
**I want** 以 4x5 或更多的 Grid 佈局同時檢視多個樣本  
**So that** 我能夠快速批次比較不同樣本的型態

#### Acceptance Criteria

**AC1 — Grid 佈局渲染**
- **Given** 查詢取得多個樣本（如 20 個）
- **When** 切換到 Grid 模式
- **Then** 應以 4x5 Grid 佈局顯示所有小圖

**AC2 — Grid 尺寸可調整**
- **Given** Grid 模式已啟動
- **When** 使用者調整 Grid 行列數（如改為 5x4）
- **Then** Grid 應重新排列，每個小圖尺寸相應調整

**AC3 — 高效能渲染**
- **Given** Grid 包含大量小圖（如 50+）
- **When** 系統渲染 Grid
- **Then** 渲染時間應在 3 秒內完成，不應出現明顯卡頓

**AC4 — 小圖資訊標籤**
- **Given** 每個小圖已渲染
- **When** 使用者檢視 Grid
- **Then** 每個小圖應顯示股票代碼與事件日期標籤

---

### US B-3: 事件日置中對齊

**As a** 策略研究員  
**I want** 所有 Grid 小圖的事件日都置中對齊  
**So that** 我能夠直觀比較事件前後的價格型態

#### Acceptance Criteria

**AC1 — 事件日居中計算**
- **Given** 每個樣本有明確的事件日期
- **When** 系統計算圖表顯示範圍
- **Then** 事件日應位於圖表的水平中心位置

**AC2 — 事件前後資料對稱**
- **Given** 設定事件前 20 日、事件後 10 日
- **When** 渲染圖表
- **Then** 事件日左側應顯示 20 根 K 線，右側顯示 10 根 K 線

**AC3 — 資料不足時的處理**
- **Given** 某樣本的事件前或事件後資料不足
- **When** 系統嘗試渲染
- **Then** 應顯示實際可用資料，並標記「資料不完整」

---

### US B-4: 查詢結果數量限制與分頁

**As a** 策略研究員  
**I want** 查詢結果數量過多時能分頁檢視  
**So that** 系統效能不會因大量資料而降低

#### Acceptance Criteria

**AC1 — 單次載入數量限制**
- **Given** 查詢結果超過 100 個樣本
- **When** 系統載入 Grid
- **Then** 應一次只載入前 100 個樣本，並提示還有更多結果

**AC2 — 分頁導航**
- **Given** 查詢結果已分頁
- **When** 使用者點擊「下一頁」或輸入頁碼
- **Then** 應載入對應頁次的樣本並更新 Grid

**AC3 — 分頁狀態顯示**
- **Given** 查詢結果已分頁
- **When** 使用者檢視 Grid
- **Then** 應顯示當前頁次與總頁數（如「第 1/5 頁」）

---

## 延後的 User Stories

| US ID | 原因 |
|-------|------|
| US C-1 | 屬 Time Window Engine，依賴 B-2 Grid 能力，排入下一 Milestone |
| US C-2 | 屬 Time Window Engine，排入下一 Milestone |
| US C-3 | 屬 Time Window Engine，排入下一 Milestone |
| US C-4 | 屬 Time Window Engine，排入下一 Milestone |

---

## [OPTIONAL] Tech Debt 納入建議

> 以下為 Technical Debt Registry 中標記 `Milestone-Candidate: true` 的開放項目（Priority P2 以上）。  
> 本區段為**建議性質**，是否納入由人類決定，不影響 Milestone linting。

| TD ID | 標題 | Priority | Type | 來源 | 建議 US 編號 |
|-------|------|----------|------|------|-------------|
| TD-001 | MSSQL 真實資料庫整合測試 | P2 | test-regression | code-check | US-TD-1 |
| TD-002 | Electron E2E 自動化測試（Playwright） | P2 | test-regression | code-check | US-TD-2 |

### US-TD-1 格式範例

若人類決定納入 TD-001，可在 Milestone 中新增維護型 US：

### US-TD-1: 補充 MSSQL 真實資料庫整合測試

**As a** 開發團隊  
**I want** 建立真實 MSSQL 測試環境並補充整合測試  
**So that** 確保資料庫查詢、欄位映射與 SQL 聚合邏輯的正確性

#### Acceptance Criteria

**AC1 — 整合測試環境建立**
- **Given** 專案已有 `docker-compose` 或測試用 MSSQL 實例配置
- **When** 執行整合測試套件
- **Then** 測試應連接真實 MSSQL，驗證 `[股價即時].[dbo].[1分K]` 的實際查詢邏輯

**AC2 — 欄位映射驗證**
- **Given** MSSQL 真實資料庫整合測試環境已就緒
- **When** 執行 `tests/integration/test_chart_api.py` 與 `test_api_contract.py`
- **Then** 不再使用 `unittest.mock` 替代資料庫連線，覆蓋率應維持 85% 以上

---

### US-TD-2 格式範例

若人類決定納入 TD-002，可在 Milestone 中新增維護型 US：

### US-TD-2: Electron E2E 自動化測試（Playwright）

**As a** 開發團隊  
**I want** 新增 Playwright E2E 測試覆蓋 Electron UI 流程  
**So that** K 線渲染、互動操作與小圖放大等功能有自動化驗收保障

#### Acceptance Criteria

**AC1 — Playwright 環境建立**
- **Given** `frontend/package.json` 已安裝 `@playwright/test`
- **When** 執行 `npm run test:e2e`
- **Then** Playwright 應啟動 Electron 視窗，完成基本渲染驗證

**AC2 — 核心 UI 流程覆蓋**
- **Given** Playwright E2E 環境已就緒
- **When** 執行 E2E 測試套件
- **Then** 應覆蓋 US A-1/A-2/A-3/A-4 的核心 UI 流程（縮放/平移/十字線/小圖放大）

---

## 與 Full User Story List 差異對照

| US ID | 差異類型 | 說明 |
|-------|----------|------|
| US B-1 | 無變更 | — |
| US B-2 | 無變更 | — |
| US B-3 | 無變更 | — |
| US B-4 | 無變更 | — |

---

## Milestone 摘要

| US ID | 摘要 | 來源 Group | AC 數量 |
|-------|------|------------|---------|
| US B-1 | 結構化條件查詢 | B | 4 |
| US B-2 | Grid 多圖並列顯示 | B | 4 |
| US B-3 | 事件日置中對齊 | B | 3 |
| US B-4 | 查詢結果數量限制與分頁 | B | 3 |

**總計**：4 個 User Story，14 條 Acceptance Criteria

---

## 執行建議

### 建議開發順序

1. **US B-1**：後端條件查詢 API，無前端依賴，可先行實作
2. **US B-4**：分頁機制與 B-1 高度關聯，建議同步完成
3. **US B-3**：事件日置中演算法，後端邏輯為主
4. **US B-2**：前端 Grid 渲染，依賴 B-1/B-3/B-4 的後端能力

### 風險項目

| 風險 | 程度 | 緩解策略 |
|------|------|----------|
| Grid 大量小圖渲染效能 | 中 | 考慮 Virtual Scrolling / Canvas 渲染 |
| 複合條件 SQL 注入防護 | 高 | 使用參數化查詢（Parameterized Query），禁止字串拼接 |
| 事件日交易日計算邊界 | 低 | 建立基於交易日曆的計算工具函式 |
