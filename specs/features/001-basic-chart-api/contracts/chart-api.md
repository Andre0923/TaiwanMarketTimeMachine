# API Contract: Chart Data API

> **Feature ID**: 001-basic-chart-api  
> **API Version**: v1  
> **Created**: 2026-02-03  
> **Status**: ✅ Ready for Implementation

---

## 1. Overview

本文件定義圖表資料 API 的完整契約，包括 Endpoint、Request/Response 格式、錯誤碼、驗證規則。

**設計原則**：
- RESTful 風格
- 統一錯誤格式
- 向下相容（未來可擴充欄位）
- 語意化錯誤碼

---

## 2. Base URL

```
http://localhost:8000/api/v1
```

**生產環境**（待定）：
```
https://api.assrp.example.com/api/v1
```

---

## 3. Endpoint: Get Chart Data

### 3.1 基本資訊

```
GET /api/v1/chart-data
```

**用途**：查詢指定股票在特定日期範圍的 OHLCV 資料

**驗證需求**：無（M01 階段無身份驗證）

### 3.2 Request

#### Query Parameters

| 參數 | 類型 | 必填 | 說明 | 格式 | 範例 |
|------|------|------|------|------|------|
| `stock_code` | String | ✅ | 股票代碼 | 台股代碼（4-6 位數字） | `2330` |
| `start_date` | String | ✅ | 起始日期 | ISO 8601: `YYYY-MM-DD` | `2024-01-01` |
| `end_date` | String | ✅ | 結束日期 | ISO 8601: `YYYY-MM-DD` | `2024-01-31` |

#### 範例 Request

```http
GET /api/v1/chart-data?stock_code=2330&start_date=2024-01-01&end_date=2024-01-31 HTTP/1.1
Host: localhost:8000
Accept: application/json
```

#### cURL 範例

```bash
curl -X GET "http://localhost:8000/api/v1/chart-data?stock_code=2330&start_date=2024-01-01&end_date=2024-01-31" \
  -H "Accept: application/json"
```

### 3.3 Response

#### Success Response (200 OK)

```json
{
  "stock_code": "2330",
  "chart_data": {
    "dates": [
      "2024-01-01",
      "2024-01-02",
      "2024-01-03"
    ],
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

#### Response Schema

```typescript
interface ChartDataResponse {
  stock_code: string;              // 股票代碼
  chart_data: {
    dates: string[];               // 交易日期陣列（ISO 8601）
    ohlc: OHLCData[];             // OHLC 資料陣列（與 dates 一一對應）
  };
}

interface OHLCData {
  open: number;                    // 開盤價
  high: number;                    // 最高價
  low: number;                     // 最低價
  close: number;                   // 收盤價
  volume: number;                  // 成交量（股數）
}
```

#### 欄位說明

| 欄位 | 型別 | 必填 | 說明 | 限制 |
|------|------|------|------|------|
| `stock_code` | String | ✅ | 股票代碼 | 回應 Request 參數 |
| `chart_data.dates` | Array[String] | ✅ | 交易日期陣列 | ISO 8601，升序排列 |
| `chart_data.ohlc` | Array[Object] | ✅ | OHLC 資料陣列 | 長度與 dates 相同 |
| `ohlc[].open` | Number | ✅ | 開盤價 | >= 0，最多 2 位小數 |
| `ohlc[].high` | Number | ✅ | 最高價 | >= open, close, low |
| `ohlc[].low` | Number | ✅ | 最低價 | <= open, close, high |
| `ohlc[].close` | Number | ✅ | 收盤價 | >= 0，最多 2 位小數 |
| `ohlc[].volume` | Number | ✅ | 成交量 | >= 0，整數 |

---

## 4. Error Responses

### 4.1 統一錯誤格式

```json
{
  "error": {
    "code": "<ERROR_CODE>",
    "message": "<USER_FRIENDLY_MESSAGE>"
  }
}
```

### 4.2 錯誤碼定義

#### E1: INVALID_STOCK_CODE

**HTTP Status**: `400 Bad Request`

**觸發條件**：
- stock_code 參數缺失
- stock_code 格式不正確（非 4-6 位數字）
- stock_code 在資料庫中不存在

**Response**：
```json
{
  "error": {
    "code": "INVALID_STOCK_CODE",
    "message": "查無此股票代碼，請確認後重試"
  }
}
```

**前端處理**：
- 顯示錯誤訊息
- 提供「返回」或「重新輸入」按鈕

---

#### E2: INVALID_DATE_RANGE

**HTTP Status**: `400 Bad Request`

**觸發條件**：
- start_date 或 end_date 參數缺失
- 日期格式不正確（非 YYYY-MM-DD）
- end_date < start_date
- 日期範圍超過限制（如 > 365 天）

**Response**：
```json
{
  "error": {
    "code": "INVALID_DATE_RANGE",
    "message": "日期範圍不正確，請調整後重試"
  }
}
```

**前端處理**：
- 顯示錯誤訊息
- 標示日期輸入欄位錯誤
- 提供修正建議（如「結束日期需晚於起始日期」）

---

#### E3: NO_DATA

**HTTP Status**: `404 Not Found`

**觸發條件**：
- 查詢結果為空（該股票在指定期間無交易資料）
- 查詢期間為非交易日（週末、國定假日）

**Response**：
```json
{
  "error": {
    "code": "NO_DATA",
    "message": "查無資料，請調整查詢條件"
  }
}
```

**前端處理**：
- 顯示「無資料」提示
- 提供「返回」或「調整條件」按鈕
- 建議調整日期範圍或更換股票代碼

---

#### E4: INTERNAL_ERROR

**HTTP Status**: `500 Internal Server Error`

**觸發條件**：
- 資料庫連線失敗
- SQL 查詢異常
- 伺服器內部錯誤

**Response**：
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "系統發生錯誤，請聯繫技術支援"
  }
}
```

**前端處理**：
- 顯示錯誤訊息
- 提供「重試」按鈕
- 紀錄錯誤日誌（含時間戳、Request ID）
- 若持續失敗，提示聯繫技術支援

---

## 5. 驗證規則

### 5.1 Request 驗證

#### V1: stock_code 驗證

```python
import re

def validate_stock_code(stock_code: str) -> bool:
    """
    驗證台股股票代碼
    - 長度：4-6 位數字
    - 範例：2330, 00878
    """
    if not stock_code:
        return False
    if not re.match(r'^\d{4,6}$', stock_code):
        return False
    return True
```

**測試案例**：
- ✅ Valid: `"2330"`, `"00878"`, `"1234"`
- ❌ Invalid: `""`, `"ABC"`, `"12"`, `"1234567"`

---

#### V2: date_range 驗證

```python
from datetime import datetime, timedelta

def validate_date_range(start_date: str, end_date: str) -> tuple[bool, str]:
    """
    驗證日期範圍
    - 格式：YYYY-MM-DD
    - end_date >= start_date
    - 最大範圍：365 天（可調整）
    """
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        return False, "日期格式不正確"
    
    if end < start:
        return False, "結束日期需晚於起始日期"
    
    if (end - start).days > 365:
        return False, "日期範圍不得超過 365 天"
    
    return True, ""
```

**測試案例**：
- ✅ Valid: `start="2024-01-01"`, `end="2024-01-31"`
- ❌ Invalid: 
  - `start="2024-01-31"`, `end="2024-01-01"` (end < start)
  - `start="2024-01-01"`, `end="2025-12-31"` (> 365 days)
  - `start="2024-13-01"`, `end="2024-01-31"` (invalid month)

---

### 5.2 Response 驗證

#### V3: OHLC 資料一致性

```python
def validate_ohlc_data(ohlc: dict) -> bool:
    """
    驗證 OHLC 資料邏輯
    - high >= open, close, low
    - low <= open, close, high
    - 所有價格 >= 0
    - volume >= 0
    """
    if ohlc['high'] < max(ohlc['open'], ohlc['close'], ohlc['low']):
        return False
    if ohlc['low'] > min(ohlc['open'], ohlc['close'], ohlc['high']):
        return False
    if any(v < 0 for v in [ohlc['open'], ohlc['high'], ohlc['low'], ohlc['close'], ohlc['volume']]):
        return False
    return True
```

---

## 6. 效能要求

### 6.1 回應時間目標

| 資料量 | 目標回應時間 | 說明 |
|--------|-------------|------|
| 1-100 根 K 線 | < 200ms | 典型查詢（1-3 個月） |
| 101-365 根 K 線 | < 500ms | 年度查詢 |
| > 365 根 K 線 | < 1000ms | 長期歷史資料 |

### 6.2 併發支援

- 支援同時 10 個併發請求，平均回應時間 < 300ms
- 使用連線池（Pool Size: 10, Max Overflow: 20）

### 6.3 快取策略（M01 不實作，預留設計）

- 歷史資料（> 7 天前）可快取 24 小時
- 近期資料（最近 7 天）不快取（可能更新）

---

## 7. 安全性考量

### 7.1 輸入驗證

- 所有參數必須經過嚴格驗證（防止 SQL Injection）
- 使用參數化查詢（Parameterized Query）

### 7.2 速率限制（M01 不實作，預留設計）

- 每 IP 每分鐘最多 60 個請求
- 超過限制回傳 `429 Too Many Requests`

### 7.3 CORS 設定

```python
# FastAPI CORS Middleware
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 開發伺服器
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)
```

---

## 8. 測試案例

### 8.1 正常流程測試

| 測試案例 | Request | 預期 Status | 預期 Response |
|----------|---------|------------|--------------|
| TC-1 | stock_code=2330, 2024-01-01 to 2024-01-31 | 200 | 包含 chart_data |
| TC-2 | stock_code=00878, 2024-01-01 to 2024-01-10 | 200 | 包含 chart_data |

### 8.2 錯誤處理測試

| 測試案例 | Request | 預期 Status | 預期 Error Code |
|----------|---------|------------|-----------------|
| TC-3 | stock_code=XXXX | 400 | INVALID_STOCK_CODE |
| TC-4 | start_date=2024-02-01, end_date=2024-01-01 | 400 | INVALID_DATE_RANGE |
| TC-5 | stock_code=9999 (不存在) | 400 | INVALID_STOCK_CODE |
| TC-6 | 查詢週末期間 | 404 | NO_DATA |
| TC-7 | DB 連線失敗 | 500 | INTERNAL_ERROR |

---

## 9. API 文件（OpenAPI Schema）

### 9.1 OpenAPI 3.0 Spec

```yaml
openapi: 3.0.0
info:
  title: ASSRP Chart Data API
  version: 1.0.0
  description: 台股視覺化事件研究平台 - 圖表資料 API

paths:
  /api/v1/chart-data:
    get:
      summary: 查詢股票圖表資料
      parameters:
        - name: stock_code
          in: query
          required: true
          schema:
            type: string
            pattern: '^\d{4,6}$'
          description: 股票代碼（4-6 位數字）
        - name: start_date
          in: query
          required: true
          schema:
            type: string
            format: date
          description: 起始日期（YYYY-MM-DD）
        - name: end_date
          in: query
          required: true
          schema:
            type: string
            format: date
          description: 結束日期（YYYY-MM-DD）
      responses:
        '200':
          description: 成功取得圖表資料
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ChartDataResponse'
        '400':
          description: 請求參數錯誤
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '404':
          description: 查無資料
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'
        '500':
          description: 伺服器錯誤
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ErrorResponse'

components:
  schemas:
    ChartDataResponse:
      type: object
      properties:
        stock_code:
          type: string
        chart_data:
          type: object
          properties:
            dates:
              type: array
              items:
                type: string
                format: date
            ohlc:
              type: array
              items:
                $ref: '#/components/schemas/OHLCData'
    
    OHLCData:
      type: object
      properties:
        open:
          type: number
        high:
          type: number
        low:
          type: number
        close:
          type: number
        volume:
          type: integer
    
    ErrorResponse:
      type: object
      properties:
        error:
          type: object
          properties:
            code:
              type: string
              enum: [INVALID_STOCK_CODE, INVALID_DATE_RANGE, NO_DATA, INTERNAL_ERROR]
            message:
              type: string
```

---

## 10. 變更歷程

| 版本 | 日期 | 變更內容 | 作者 |
|------|------|----------|------|
| 1.0.0 | 2026-02-03 | 初版建立 | AI Development Team |

---

**文件版本**：v1.0.0  
**維護者**：AI Development Team  
**最後更新**：2026-02-03
