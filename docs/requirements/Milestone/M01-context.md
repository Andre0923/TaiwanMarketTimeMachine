# M01 Milestone Context — 設計上下文擷取

> **Milestone**：M01 — 基礎繪圖與 API 格式  
> **產生日期**：2026-02-03  
> **來源文件**：`docs/requirements/PRD-ASSRP.md`  
> **衝突狀態**：✅ 無衝突（System Spec 為空白範本）

---

## 1. Milestone 範圍摘要

### 包含的 User Stories

| US ID | 摘要 | 分類 |
|-------|------|------|
| US A-1 | K 線與成交量基礎繪圖 | 基礎繪圖 |
| US A-2 | 圖表互動操作（Zoom/Pan/Crosshair） | 基礎繪圖 |
| US A-3 | 小圖點擊放大檢視 | 基礎繪圖 |
| US A-4 | 圖表載入狀態與錯誤處理 | 基礎繪圖 |
| US G-2 | API Response 固定格式設計 | 效能與格式 |

### 核心能力

- 基礎圖表渲染（K 線 + 成交量）
- 圖表互動操作（縮放、平移、十字線）
- 載入狀態管理
- API Response 格式規範

---

## 2. 技術選型（來自 PRD Section 1.2）

### 技術棧

| 角色 | 技術 | 說明 | 關聯 US |
|------|------|------|---------|
| **前端** | Vue 3 | UI 框架 | US A-1, A-2, A-3, A-4 |
| **圖表庫** | TradingView Lightweight Charts | 高效能 K 線渲染 | US A-1, A-2, A-3 |
| **後端** | FastAPI | API 與計算邏輯 | US A-4, G-2 |
| **資料庫** | Microsoft SQL Server | 台股歷史資料 | US A-1, A-4 |

### 技術決策重點

1. **TradingView Lightweight Charts**
   - 選擇理由：高效能、內建互動操作、適合金融圖表
   - 關鍵能力：K 線渲染、縮放平移、十字線
   - 注意事項：Grid 模式下大量小圖的效能優化

2. **FastAPI**
   - 選擇理由：非同步支援、自動 API 文件、Python 生態系
   - 關鍵能力：圖表資料 API、錯誤處理、Response 格式規範

3. **Microsoft SQL Server**
   - 選擇理由：台股資料來源相容性
   - 關鍵能力：OHLCV 資料查詢、日期範圍篩選

---

## 3. 資料模型（DM）

### 3.1 stock_daily 表

**來源**：PRD Section 3 — DB Schema

**用途**：儲存台股歷史日 K 線資料（OHLCV）

**推測欄位**（PRD 未明確定義，需在 Spec 階段確認）：

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| stock_code | VARCHAR(10) | ✅ | 股票代碼 |
| trade_date | DATE | ✅ | 交易日期 |
| open | DECIMAL(10,2) | ✅ | 開盤價 |
| high | DECIMAL(10,2) | ✅ | 最高價 |
| low | DECIMAL(10,2) | ✅ | 最低價 |
| close | DECIMAL(10,2) | ✅ | 收盤價 |
| volume | BIGINT | ✅ | 成交量 |

**索引建議**：
- Primary Key: `(stock_code, trade_date)`
- Index: `trade_date` （日期範圍查詢）

**關聯 US**：US A-1（K 線資料來源）、US A-4（資料載入）

---

### 3.2 stock_events 表

**來源**：PRD Section 3 — DB Schema

**用途**：儲存事件資料（M01 階段可能尚未使用）

**狀態**：延後至 M02/M03 定義

---

## 4. API 契約（CT）

### 4.1 API Response 固定格式

**來源**：PRD Section 4 — API Response 規範（保險絲設計 2）

**關聯 US**：US G-2

#### 核心設計原則

> **必須固定格式，未來擴充不需改 API**

#### Response Schema

```json
{
  "event_window": { 
    "pre": 20, 
    "post": 10 
  },
  "horizons": [1, 3, 5, 10],
  "samples": [
    {
      "stock_code": "2330",
      "event_date": "2024-01-15",
      "chart_data": {
        "dates": ["2024-01-01", "2024-01-02", "..."],
        "ohlc": [
          { "open": 580, "high": 585, "low": 578, "close": 583, "volume": 12345678 }
        ]
      }
    }
  ],
  "metrics": {
    "avg_return": { "1d": 0.5, "3d": 1.2, "5d": 2.1, "10d": 3.5 },
    "win_rate": { "1d": 0.6, "3d": 0.65, "5d": 0.7, "10d": 0.75 },
    "max_drawdown": { "1d": -2.1, "3d": -3.5, "5d": -4.2, "10d": -5.8 }
  }
}
```

#### 欄位定義

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `event_window` | Object | ✅ | 時間窗口參數 |
| `event_window.pre` | Integer | ✅ | 事件前天數（交易日） |
| `event_window.post` | Integer | ✅ | 事件後天數（交易日） |
| `horizons` | Array[Integer] | ✅ | 觀察期設定（+N 日） |
| `samples` | Array[Object] | ✅ | 樣本清單與圖表資料 |
| `samples[].stock_code` | String | ✅ | 股票代碼 |
| `samples[].event_date` | String (ISO) | ✅ | 事件日期 |
| `samples[].chart_data` | Object | ✅ | 圖表 OHLCV 資料 |
| `metrics` | Object | ✅ | 績效統計指標 |

#### 錯誤格式

```json
{
  "error": {
    "code": "INVALID_DATE_RANGE",
    "message": "查詢日期範圍超出資料庫範圍"
  }
}
```

#### 擴充性設計

- **新增指標**：在 `metrics` 物件內新增欄位，不影響既有欄位
- **向下相容承諾**：既有欄位的資料型別與語意不得改變

#### M01 階段簡化版本

在 M01 階段，由於尚未實作 Micro Backtest，API Response 可暫時簡化：

```json
{
  "stock_code": "2330",
  "chart_data": {
    "dates": ["2024-01-01", "2024-01-02", "..."],
    "ohlc": [
      { "open": 580, "high": 585, "low": 578, "close": 583, "volume": 12345678 }
    ]
  }
}
```

**但架構設計需保留未來擴充能力**。

---

### 4.2 圖表資料 API Endpoint

**建議 Endpoint**：`GET /api/chart-data`

**Query Parameters**：

| 參數 | 型別 | 必填 | 說明 |
|------|------|------|------|
| stock_code | string | ✅ | 股票代碼 |
| start_date | string (ISO) | ✅ | 起始日期 |
| end_date | string (ISO) | ✅ | 結束日期 |

**範例請求**：
```
GET /api/chart-data?stock_code=2330&start_date=2024-01-01&end_date=2024-12-31
```

**關聯 US**：US A-1（資料取得）、US A-4（載入狀態）

---

## 5. 流程設計（FL）

### 5.1 圖表載入流程

**來源**：PRD Section 2.1 基礎繪圖 + M01 US A-4

```
[使用者請求圖表]
    ↓
[顯示 Loading 指示器]  ← US A-4 AC1
    ↓
[呼叫 API /api/chart-data]
    ↓
┌─ [API 成功] → [渲染 K 線與成交量] → [啟用互動操作]  ← US A-1, A-2
│                      ↓
│                [移除 Loading]
│
└─ [API 失敗] → [顯示錯誤訊息 + 重試按鈕]  ← US A-4 AC2
                    ↓
                [使用者點擊重試] → 回到 [呼叫 API]
```

**關鍵狀態**：
- Loading：顯示 Spinner
- Success：顯示圖表
- Error：顯示錯誤訊息與重試按鈕
- Empty：顯示「無資料」提示

---

### 5.2 小圖放大流程

**來源**：M01 US A-3

```
[Grid 模式顯示多個小圖]
    ↓
[使用者點擊某小圖]  ← US A-3 AC1
    ↓
[放大至主檢視區域]
    ↓
[保留互動操作能力]  ← US A-3 AC2
    ↓
[使用者按 ESC 或點擊返回]  ← US A-3 AC3
    ↓
[返回 Grid 檢視]
```

---

## 6. UI 規格（UI）

### 6.1 K 線圖表元件

**來源**：PRD Section 2.1 基礎繪圖

**元件名稱**：`ChartComponent`

**視覺規範**：
- **K 線顏色**：紅漲綠跌（台股慣例）← US A-1 AC1
- **成交量位置**：副圖區域，時間軸對齊 ← US A-1 AC2
- **十字線**：滑鼠移動時顯示 OHLC 數據 ← US A-2 AC3

**互動規範**：
- **滑鼠滾輪**：縮放圖表 ← US A-2 AC1
- **左鍵拖曳**：平移圖表 ← US A-2 AC2
- **點擊小圖**：放大至主檢視 ← US A-3 AC1

---

### 6.2 載入狀態元件

**來源**：M01 US A-4

**元件名稱**：`LoadingState`, `ErrorState`, `EmptyState`

**狀態切換**：
```
Loading → Success (顯示圖表)
Loading → Error (顯示錯誤 + 重試按鈕)
Loading → Empty (顯示「無資料」提示)
```

**UI 文案**：
- Loading：「載入中...」+ Spinner
- Error：「載入失敗：[錯誤訊息]」 + 「重試」按鈕
- Empty：「無資料」 + 「請調整查詢條件」

---

## 7. 技術備註（TN）

### 7.1 Roadmap 對應

**來源**：PRD Section 6 — Roadmap

M01 對應 **Phase 1 — DB + API 基礎**

| Phase | 任務 | M01 狀態 |
|-------|------|----------|
| Phase 1 | DB + API 基礎 | ✅ **本 Milestone** |
| Phase 2 | Grid + Event Anchoring | ⏸️ M02 規劃 |
| Phase 2.5 | Time Window Engine | ⏸️ M02 規劃 |
| Phase 3 | Micro Backtest + Excel | ⏸️ M03 規劃 |
| Phase 4 | AI Text-to-SQL | ⏸️ M04 規劃 |

---

### 7.2 效能考量

**來源**：PRD Section 2.1 基礎繪圖（F-17 小圖點擊放大）

**Grid 模式渲染效能**：
- 需考慮大量小圖（20+）的渲染效能
- 建議實作策略：
  - Virtual Scrolling（僅渲染可見區域）
  - Lazy Loading（滾動時動態載入）
  - Canvas 渲染（避免大量 DOM 元素）

**M01 階段處理**：
- US A-3 實作小圖放大功能
- 效能優化可延後至 M02（實際 Grid 模式實作時）

---

### 7.3 台股特殊規範

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

---

## 8. 衝突檢測結果

### 8.1 與 System Spec 比對

**比對目標**：
- `specs/system/spec.md`
- `specs/system/data-model.md`
- `specs/system/flows.md`
- `specs/system/contracts/`
- `specs/system/ui/`

**檢測結果**：
- ✅ **無衝突**
- 📝 **原因**：System Spec 目前為空白範本，尚未定義任何實際內容

**結論**：
- M01 的設計內容將成為 System Spec 的**第一批內容**
- 不需要調整 PRD 設計
- 建議在 M01 完成後執行 `/flowkit.unify-flow` 將設計統一至 System Spec

---

### 8.2 衝突報告

**衝突數量**：0

**潛在風險**：無

---

## 9. 待確認事項

> 以下事項在 PRD 中未明確定義，需在 Spec 階段（`/speckit.specify`）確認。

### 9.1 資料模型細節

- [ ] **stock_daily 表完整 Schema**
  - 確認欄位名稱（snake_case or camelCase）
  - 確認資料型別與精度
  - 確認索引策略

- [ ] **資料來源與更新機制**
  - 歷史資料從何處取得？
  - 是否需要即時更新？

### 9.2 API 細節

- [ ] **圖表資料 API 的完整規格**
  - Endpoint 路徑
  - 錯誤碼定義
  - 逾時設定

- [ ] **API 驗證與權限**
  - 是否需要 API Key？
  - 是否有 Rate Limiting？

### 9.3 UI/UX 細節

- [ ] **Loading Spinner 樣式**
  - 使用哪種動畫？
  - 顏色與尺寸？

- [ ] **錯誤訊息文案**
  - 不同錯誤類型的具體文案
  - 是否需要多語系？

- [ ] **小圖放大動畫**
  - 是否需要過場動畫？
  - 動畫時長？

---

## 10. 開發建議

### 10.1 建議開發順序

根據 Milestone 文件建議：

1. **US G-2**：優先建立 API 格式規範與範例文件（無依賴，可先行）
2. **US A-1**：基礎圖表渲染能力（核心功能）
3. **US A-2**：圖表互動操作（依賴 US A-1）
4. **US A-4**：載入狀態管理（可與 US A-1/A-2 平行）
5. **US A-3**：小圖放大功能（依賴 US A-1/A-2，最後實作）

### 10.2 技術準備檢查清單

- [ ] **前端**：Vue 3 專案初始化
- [ ] **前端**：安裝 TradingView Lightweight Charts
- [ ] **後端**：FastAPI 專案初始化
- [ ] **後端**：MSSQL 連線設定與測試
- [ ] **資料庫**：建立 `stock_daily` 表
- [ ] **資料庫**：匯入至少一檔股票的測試資料（如 2330）

### 10.3 風險項目

| 風險 | 影響 | 緩解措施 |
|------|------|----------|
| TradingView Lightweight Charts 學習曲線 | 開發時程延遲 | 先完成簡單範例驗證可行性 |
| API 格式設計不夠彈性 | 未來需大幅修改 | 參考業界標準（如 JSON:API）並進行技術評審 |
| MSSQL 資料結構不明確 | 後端實作困難 | 優先定義 `stock_daily` 表 Schema |
| Grid 模式效能問題 | 使用者體驗不佳 | M01 階段先實作單圖，延後優化 |

---

## 11. 下一步行動

### ✅ 當前已完成
- [x] Milestone Context 擷取完成
- [x] 無設計衝突

### 🚀 建議的後續步驟

1. **進入 SpecKit Specify 階段**
   ```
   /speckit.specify "實作 M01 基礎繪圖與 API 格式功能"
   ```
   - 建立 Feature Spec
   - 定義詳細的行為規格與資料模型

2. **技術準備**
   - 建立前後端專案結構
   - 安裝必要套件
   - 設定開發環境

3. **實作開發**
   - 依建議順序開發 US
   - 撰寫測試
   - 進行 Code Review

4. **Unify Flow**
   ```
   /flowkit.unify-flow --milestone M01
   ```
   - M01 完成後，將設計統一至 System Spec

---

## 附錄：Escalation Log

> 記錄本次擷取過程中的讀取範圍，確保遵循 Progressive Disclosure Protocol。

| Phase | 讀取目標 | 讀取範圍 | 原因 |
|-------|----------|----------|------|
| 0 | Milestone 檔案 | Headers + US ID 清單 | 定義範圍 |
| 1 | PRD 檔案 | 完整文件（250 行） | 文件較短，完整讀取 |
| 2 | System Spec | spec.md (1-100), data-model.md (1-50) | 檢查衝突 |

**總讀取量**：約 400 行（符合漸進式揭露原則）

---

**文件版本**：v1.0.0  
**產生工具**：FlowKit Milestone-context v1.3.0  
**維護者**：AI Development Team
