# Strategy Query API 契約文件

> **版本**: v1.0.0  
> **生效日期**: 2026-03-02（Plan 階段定義）  
> **對應 Feature**: 003-strategy-grid  
> **對應 User Story**: US B-1, B-4
> **向後相容策略**: 參照 `chart-api.md §3.1`

---

## 概述

本文件定義台股時光機「策略 Grid 查詢 API」的完整契約規範，包括：
- 查詢條件 Request 格式（US B-1 AC1/AC2）
- GridQueryResponse Response 格式（US B-4 AC3）
- 分頁設計（US B-4 AC2）
- 錯誤格式（對齊 chart-api.md 規範）

**設計原則（R-01）**：M03 Response 只包含 M03 範圍欄位（`samples` + 分頁 metadata）；`event_window`、`horizons`、`metrics` 為選填欄位，留給 M04/M05 填入，以新增選填欄位方式實現向後相容。

---

## 1. API 端點規範

### 1.1 策略 Grid 查詢

#### 基本資訊

| 項目 | 內容 |
|------|------|
| **端點** | `POST /api/strategy/query` |
| **用途** | 以結構化條件篩選符合型態的事件樣本，回傳 Grid 可用的帶 K 線批次資料 |
| **認證** | 無（開發階段）|
| **速率限制** | 無（開發階段）|

#### Request Body（JSON）

```json
{
  "stock_codes": ["2330", "2317"],
  "date_from": "2023-01-01",
  "date_to": "2023-12-31",
  "price_min": 50.0,
  "price_max": 200.0,
  "logic": "AND"
}
```

#### Request 欄位說明

| 欄位 | 型別 | 必填 | 格式/約束 | 說明 |
|------|------|------|-----------|------|
| `stock_codes` | `string[]` | ❌（空 = 查全部）| 每個代碼 4-10 字元，`^[0-9A-Z]{4,10}$` | 股票代碼白名單過濾 |
| `date_from` | `string` | ✅ | YYYY-MM-DD，不得超過今日 | 事件日期範圍起始 |
| `date_to` | `string` | ✅ | YYYY-MM-DD，≥ date_from | 事件日期範圍結束 |
| `price_min` | `number` | ❌ | ≥ 0 | 事件日收盤最低價 |
| `price_max` | `number` | ❌ | ≥ price_min（若兩者均填）| 事件日收盤最高價 |
| `logic` | `string` | ❌（預設 "AND"）| `"AND"` 或 `"OR"`（Enum）| 多個條件組合邏輯 |

**驗證規則**：
- `stock_codes` 每個代碼 MUST 符合 `^[0-9A-Z]{4,10}$`（CONFLICT-001 決策，涵蓋 ETF 如 006208）
- `date_from` MUST ≤ `date_to`
- `date_from` / `date_to` MUST ≤ 今日（不接受未來日期）
- `logic` MUST 為 `"AND"` 或 `"OR"`（Enum 白名單，防 SQL Injection）

#### Query Parameters（分頁）

| 參數 | 型別 | 預設值 | 約束 | 說明 |
|------|------|--------|------|------|
| `page` | `integer` | `1` | ≥ 1 | 頁碼（從 1 起算）|
| `page_size` | `integer` | `100` | 1 ≤ n ≤ 100 | 每頁最大樣本數 |

---

## 2. Response 格式

### 2.1 成功回應（HTTP 200 OK）

```json
{
  "samples": [
    {
      "stock_code": "2330",
      "event_date": "2023-06-15",
      "event_type": "法說會",
      "chart_data": [
        {
          "time": "2023-05-15",
          "open": 520.0,
          "high": 528.0,
          "low": 518.0,
          "close": 525.0,
          "volume": 15234567.0
        }
      ],
      "data_complete": true,
      "event_bar_index": 20
    }
  ],
  "total_count": 47,
  "page": 1,
  "total_pages": 1,
  "page_size": 100,
  "event_window": null,
  "horizons": null,
  "metrics": null
}
```

### 2.2 Response 欄位說明

#### 頂層欄位

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `samples` | `SampleResult[]` | ✅ | 符合條件的樣本清單（可為空陣列）|
| `total_count` | `integer` | ✅ | 符合條件的樣本總數（跨所有頁）|
| `page` | `integer` | ✅ | 當前頁碼（從 1 起算）|
| `total_pages` | `integer` | ✅ | 總頁數 |
| `page_size` | `integer` | ✅ | 本次每頁最大筆數 |
| `event_window` | `object \| null` | ❌ | **M04 填入**：`{"pre": 20, "post": 10}`；M03 固定回傳 `null` |
| `horizons` | `integer[] \| null` | ❌ | **M04 填入**：累計報酬計算天數；M03 固定回傳 `null` |
| `metrics` | `object \| null` | ❌ | **M05 填入**：統計指標；M03 固定回傳 `null` |

#### SampleResult 欄位

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `stock_code` | `string` | ✅ | 股票代碼 |
| `event_date` | `string` | ✅ | 事件日期（YYYY-MM-DD）|
| `event_type` | `string \| null` | ❌ | 事件類型標籤（僅供顯示，非篩選條件）|
| `chart_data` | `ChartDataPoint[]` | ✅ | 事件日前後 K 線資料（最多 pre+post+1 筆），格式同 `chart-api.md` |
| `data_complete` | `boolean` | ✅ | 事件前後資料是否完整（pre < PRE_DAYS 或 post < POST_DAYS 時為 false）|
| `event_bar_index` | `integer` | ✅ | 事件日在 `chart_data[]` 中的索引（0-based），前端用於 TradingView 置中顯示 |

#### ChartDataPoint 欄位（對齊 chart-api.md，維持向後相容）

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `time` | `string` | ✅ | 交易日期（YYYY-MM-DD）|
| `open` | `number` | ✅ | 開盤價（> 0）|
| `high` | `number` | ✅ | 最高價（> 0）|
| `low` | `number` | ✅ | 最低價（> 0）|
| `close` | `number` | ✅ | 收盤價（> 0）|
| `volume` | `number` | ✅ | 成交量（≥ 0）|

---

## 3. 特殊情況處理

### 3.1 查詢結果為空（US B-1 AC4）

**HTTP Status**: `200 OK`

```json
{
  "samples": [],
  "total_count": 0,
  "page": 1,
  "total_pages": 0,
  "page_size": 100,
  "event_window": null,
  "horizons": null,
  "metrics": null
}
```

> 查無資料**不是錯誤**（與 `chart-api.md` 設計哲學一致），HTTP 200。前端應顯示 Empty Pattern（[UI-STATE-002]）。

### 3.2 資料不完整的樣本（US B-3 AC3）

當某個樣本的事件前或事件後交易日資料不足（如股票上市未滿 20 交易日），`data_complete` 設為 `false`，但仍回傳實際可用資料：

```json
{
  "stock_code": "7890",
  "event_date": "2023-02-10",
  "event_type": null,
  "chart_data": [...],
  "data_complete": false,
  "event_bar_index": 5
}
```

前端應在該 MiniChart 上顯示「資料不完整」標籤（[UI-STATE-004] Partial Pattern）。

### 3.3 分頁超出範圍

**HTTP Status**: `400 Bad Request`

```json
{
  "detail": {
    "error": {
      "code": "INVALID_PAGE",
      "message": "頁碼超出範圍",
      "details": "請求頁碼 (5) 超過總頁數 (3)"
    }
  }
}
```

---

## 4. 錯誤格式規範

所有錯誤 MUST 使用 `ErrorResponse` 模型（對齊 `chart-api.md §2`）：

```json
{
  "detail": {
    "error": {
      "code": "ERROR_CODE",
      "message": "錯誤摘要",
      "details": "詳細說明"
    }
  }
}
```

### 4.1 M03 新增錯誤碼

| 錯誤碼 | HTTP Status | 說明 | 範例情境 |
|--------|-------------|------|----------|
| `INVALID_STOCK_CODE` | 400 | 股票代碼格式錯誤 | 代碼長度超過 10 字元或含非法字元 |
| `INVALID_DATE_RANGE` | 400 | 日期範圍不合法 | date_from > date_to 或超過今日 |
| `INVALID_DATE_FORMAT` | 400 | 日期格式錯誤 | 非 YYYY-MM-DD 格式 |
| `INVALID_QUERY_LOGIC` | 400 | 邏輯運算符不合法 | logic 非 "AND" 或 "OR" |
| `INVALID_PRICE_RANGE` | 400 | 價格範圍不合法 | price_max < price_min |
| `INVALID_PAGE` | 400 | 分頁參數超出範圍 | page > total_pages |
| `DATABASE_ERROR` | 500 | 資料庫查詢錯誤 | MSSQL 連線失敗 |
| `INTERNAL_ERROR` | 500 | 伺服器內部錯誤 | 未預期的例外 |

---

## 5. 業務邏輯規範

### 5.1 條件組合邏輯（US B-1 AC2）

**AND 邏輯**（預設）：同時滿足所有填入的條件

```
(stock_code IN stock_codes OR stock_codes IS EMPTY)
AND (event_date >= date_from)
AND (event_date <= date_to)
AND (close_price >= price_min IF price_min IS NOT NULL)
AND (close_price <= price_max IF price_max IS NOT NULL)
```

**OR 邏輯**：滿足任一填入的條件（各個條件之OR，而非欄位間OR）

```
(stock_code IN stock_codes OR stock_codes IS EMPTY)
OR (event_date >= date_from AND event_date <= date_to)
OR (close_price >= price_min IF price_min IS NOT NULL)
OR (close_price <= price_max IF price_max IS NOT NULL)
```

> ⚠️ OR 邏輯的具體語意在 tasks 階段確認。stock_codes 篩選永遠是 IN 過濾，不受 AND/OR 切換影響。

### 5.2 事件日置中計算（US B-3 AC2）

- 系統常數：`PRE_DAYS = 20`，`POST_DAYS = 10`（M03 不提供 UI 調整）
- `chart_data[]` 長度：最多 `PRE_DAYS + 1 + POST_DAYS = 31` 筆
- `event_bar_index`：事件日在 `chart_data[]` 中的索引（理想情況為 20，即陣列 index 20）
- 計算基準：台灣股市**交易日**（Trading Days），非日曆日；以 `stock_daily` DISTINCT 日期序列計算

### 5.3 分頁規範（US B-4）

- `page` 從 1 起算
- `total_pages = ceil(total_count / page_size)`
- `total_count = 0` 時 `total_pages = 0`
- 排序：按 `event_date ASC`, `stock_code ASC`（穩定排序保障分頁一致性）

---

## 6. 向後相容承諾

本契約遵循 `chart-api.md §3.1` 的向後相容策略：

| 承諾 | 說明 |
|------|------|
| 現有欄位不得變更 | `samples`, `total_count`, `page`, `total_pages`, `page_size` 的型別與語意不得改變 |
| M04 擴充方式 | 填入現有選填欄位 `event_window`, `horizons`；不新增必填欄位 |
| M05 擴充方式 | 填入現有選填欄位 `metrics`；不新增必填欄位 |
| SampleResult 擴充 | 新增欄位 MUST 為選填（`Optional`），現有欄位型別與語意不得改變 |

---

## 7. 版本歷史

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.0.0 | 2026-03-02 | Plan 階段初始版本。定義 POST /api/strategy/query 完整契約，含 M03 子集格式、選填 M04/M05 預留欄位、分頁規範、錯誤碼。 |
