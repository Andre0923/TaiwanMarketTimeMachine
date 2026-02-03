# Data Model: 基礎繪圖與 API 格式

> **Feature ID**: 001-basic-chart-api  
> **Version**: 1.0  
> **Created**: 2026-02-03  
> **Status**: ⚠️ **Pending Confirmation** - Q1 等待 User 提供現有表 Schema

---

## 1. Overview

本文件定義 M01 Feature 所需的資料模型。主要涉及股票歷史 OHLCV 資料的儲存與查詢。

---

## 2. Entity: stock_daily

### 2.1 用途

儲存台股歷史日 K 線資料（Open, High, Low, Close, Volume）。

### 2.2 Schema

⚠️ **狀態**：等待 User 確認現有資料表 Schema

**推測 Schema**（基於 PRD，待驗證）：

```sql
CREATE TABLE stock_daily (
    stock_code VARCHAR(10) NOT NULL COMMENT '股票代碼（如 2330）',
    trade_date DATE NOT NULL COMMENT '交易日期',
    open_price DECIMAL(10,2) NOT NULL COMMENT '開盤價',
    high_price DECIMAL(10,2) NOT NULL COMMENT '最高價',
    low_price DECIMAL(10,2) NOT NULL COMMENT '最低價',
    close_price DECIMAL(10,2) NOT NULL COMMENT '收盤價',
    volume BIGINT NOT NULL COMMENT '成交量（股數）',
    PRIMARY KEY (stock_code, trade_date),
    INDEX idx_trade_date (trade_date)
);
```

### 2.3 欄位說明

| 欄位名稱 | 資料型別 | 必填 | 說明 | 範例 |
|----------|----------|------|------|------|
| `stock_code` | VARCHAR(10) | ✅ | 股票代碼，符合台股格式 | "2330" |
| `trade_date` | DATE | ✅ | 交易日期（YYYY-MM-DD） | 2024-01-15 |
| `open_price` | DECIMAL(10,2) | ✅ | 開盤價（新台幣） | 580.00 |
| `high_price` | DECIMAL(10,2) | ✅ | 當日最高價 | 585.00 |
| `low_price` | DECIMAL(10,2) | ✅ | 當日最低價 | 578.00 |
| `close_price` | DECIMAL(10,2) | ✅ | 收盤價 | 583.00 |
| `volume` | BIGINT | ✅ | 成交量（股數） | 12345678 |

### 2.4 索引策略

#### 主鍵（Primary Key）
```sql
PRIMARY KEY (stock_code, trade_date)
```
- **理由**：確保同一檔股票在同一交易日只有一筆資料
- **效能**：支援快速查詢特定股票的歷史資料

#### 次要索引
```sql
INDEX idx_trade_date (trade_date)
```
- **理由**：支援跨股票的日期範圍查詢
- **使用情境**：查詢特定時間段內所有股票的資料（M02/M03 功能）

### 2.5 業務規則

#### BR-1: 資料完整性
- 同一檔股票在同一交易日只能有一筆資料
- 所有價格欄位必須 > 0
- 成交量必須 >= 0（停牌日可能為 0）

#### BR-2: 日期限制
- `trade_date` 必須為過去的日期（不得為未來日期）
- 僅包含交易日（排除週末、國定假日）

#### BR-3: 價格邏輯
- `high_price` >= `open_price`, `close_price`, `low_price`
- `low_price` <= `open_price`, `close_price`, `high_price`

### 2.6 查詢模式

#### Q1: 查詢單一股票的歷史資料
```sql
SELECT 
    trade_date,
    open_price,
    high_price,
    low_price,
    close_price,
    volume
FROM stock_daily
WHERE stock_code = :stock_code
  AND trade_date BETWEEN :start_date AND :end_date
ORDER BY trade_date ASC;
```

**索引使用**：Primary Key (stock_code, trade_date)  
**預期效能**：< 100ms（100 根 K 線）

#### Q2: 驗證股票代碼是否存在
```sql
SELECT COUNT(*) 
FROM stock_daily 
WHERE stock_code = :stock_code 
LIMIT 1;
```

**索引使用**：Primary Key (stock_code)  
**預期效能**：< 10ms

---

## 3. API Response Model

### 3.1 ChartDataResponse

**用途**：API 回傳圖表資料的標準格式

**Schema**：
```typescript
interface ChartDataResponse {
  stock_code: string;
  chart_data: {
    dates: string[];        // ISO 8601 format: "YYYY-MM-DD"
    ohlc: OHLCData[];
  };
}

interface OHLCData {
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}
```

**範例**：
```json
{
  "stock_code": "2330",
  "chart_data": {
    "dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
    "ohlc": [
      {
        "open": 580.0,
        "high": 585.0,
        "low": 578.0,
        "close": 583.0,
        "volume": 12345678
      },
      {
        "open": 583.0,
        "high": 590.0,
        "low": 582.0,
        "close": 588.0,
        "volume": 15678901
      },
      {
        "open": 588.0,
        "high": 595.0,
        "low": 586.0,
        "close": 592.0,
        "volume": 13456789
      }
    ]
  }
}
```

### 3.2 ErrorResponse

**用途**：統一的錯誤回傳格式

**Schema**：
```typescript
interface ErrorResponse {
  error: {
    code: ErrorCode;
    message: string;
  };
}

type ErrorCode = 
  | "INVALID_STOCK_CODE"
  | "INVALID_DATE_RANGE"
  | "NO_DATA"
  | "INTERNAL_ERROR";
```

**範例**：
```json
{
  "error": {
    "code": "NO_DATA",
    "message": "查無資料，請調整查詢條件"
  }
}
```

---

## 4. 資料流轉

### 4.1 查詢流程

```
User (Frontend)
  ↓ 1. HTTP GET /api/v1/chart-data?stock_code=2330&start_date=2024-01-01&end_date=2024-01-31
API Endpoint (FastAPI)
  ↓ 2. 驗證參數（stock_code, date_range）
  ↓ 3. 呼叫 ChartService.get_chart_data()
ChartService
  ↓ 4. 執行 SQL 查詢（stock_daily 表）
Database (MSSQL)
  ↓ 5. 回傳 Query Result
ChartService
  ↓ 6. 轉換為 ChartDataResponse 格式
API Endpoint
  ↓ 7. 回傳 JSON Response
User (Frontend)
  ↓ 8. 解析 JSON，傳遞給 TradingView Charts
```

### 4.2 錯誤處理流程

```
API Endpoint
  ↓ 1. 驗證參數失敗
  ↓ 2. 回傳 ErrorResponse (400 Bad Request, code: INVALID_STOCK_CODE 或 INVALID_DATE_RANGE)

ChartService
  ↓ 1. SQL 查詢結果為空
  ↓ 2. 回傳 ErrorResponse (404 Not Found, code: NO_DATA)

Database
  ↓ 1. 連線失敗或查詢異常
  ↓ 2. 回傳 ErrorResponse (500 Internal Server Error, code: INTERNAL_ERROR)
```

---

## 5. 未來擴充考量

### 5.1 M02/M03 可能新增欄位

以下欄位在 M01 **不需要**，但為未來擴充預留設計空間：

| 欄位 | 型別 | 用途 | 加入時機 |
|------|------|------|----------|
| `amount` | DECIMAL(15,2) | 成交金額（price × volume） | M02（條件查詢） |
| `change` | DECIMAL(10,2) | 漲跌幅（%） | M03（績效統計） |
| `change_price` | DECIMAL(10,2) | 漲跌價差 | M03（績效統計） |

### 5.2 資料來源整合

未來可能需要：
- 從證交所 API 定期同步資料
- 資料清洗與驗證機制
- 歷史資料回填策略

---

## 6. 驗證與測試

### 6.1 資料驗證測試

- [ ] 驗證主鍵約束（不允許重複 stock_code + trade_date）
- [ ] 驗證價格邏輯（high >= open/close >= low）
- [ ] 驗證成交量非負數
- [ ] 驗證日期為過去日期

### 6.2 效能測試

- [ ] 查詢 100 根 K 線 < 100ms
- [ ] 查詢 1000 根 K 線 < 500ms
- [ ] 併發 10 個查詢的平均回應時間 < 200ms

---

## 7. 狀態追蹤

| 項目 | 狀態 | 備註 |
|------|------|------|
| Schema 定義 | ⚠️ Pending | 等待 User 提供現有表結構 |
| 索引策略 | ✅ Proposed | 基於推測 Schema 設計 |
| API Response 格式 | ✅ Defined | 依據 research.md R2 決策 |
| 錯誤處理格式 | ✅ Defined | 依據 research.md R2 & R4 決策 |
| 業務規則 | ✅ Defined | BR-1 至 BR-3 |

---

**下一步**：
1. 等待 User 確認 stock_daily Schema（Q1）
2. 若 Schema 確認，更新本文件第 2.2 節並移除 ⚠️ 標記
3. 同步更新 `contracts/chart-api.md` 中的欄位對應關係

---

**文件版本**：v1.0.0  
**維護者**：AI Development Team  
**最後更新**：2026-02-03
