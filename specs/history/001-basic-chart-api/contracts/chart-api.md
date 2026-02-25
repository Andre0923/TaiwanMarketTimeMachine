# Chart API 契約文件

> **版本**: v1.0.0  
> **生效日期**: 2026-02-04  
> **對應 Feature**: 001-basic-chart-api  
> **對應 User Story**: US G-2 (API Response 格式設計)

---

## 概述

本文件定義台股時光機「日K線圖表 API」的完整契約規範，包括：
- Request/Response 格式（US G-2 AC1）
- 擴充性設計原則（US G-2 AC2, AC5）
- 錯誤格式標準（US G-2 AC3）
- API 版本管理策略（US G-2 AC4）

---

## 1. API 端點規範

### 1.1 取得日K線資料

#### 基本資訊

| 項目 | 內容 |
|------|------|
| **端點** | `GET /api/chart/daily` |
| **用途** | 查詢指定股票的日K線資料（從 1分K 聚合） |
| **認證** | 無（開發階段） |
| **速率限制** | 無（開發階段） |

#### Request Parameters

| 參數 | 類型 | 必填 | 格式 | 說明 | 範例 |
|------|------|------|------|------|------|
| `stock_code` | string | ✅ | 4-10 字元 | 股票代碼 | `2330`, `1101` |
| `start_date` | string | ✅ | YYYY-MM-DD | 起始日期 | `2024-01-01` |
| `end_date` | string | ✅ | YYYY-MM-DD | 結束日期 | `2024-01-31` |

**驗證規則**：
- `stock_code`: 長度 4-10，允許數字與大寫英文
- `start_date`, `end_date`: 必須符合 ISO 8601 日期格式（YYYY-MM-DD）
- 日期範圍：`start_date` ≤ `end_date`

#### Response Format (Success)

**HTTP Status**: `200 OK`

```json
{
  "stock_code": "2330",
  "chart_data": [
    {
      "time": "2024-01-15",
      "open": 580.0,
      "high": 585.0,
      "low": 578.0,
      "close": 583.0,
      "volume": 12345678.0
    },
    {
      "time": "2024-01-16",
      "open": 583.0,
      "high": 590.0,
      "low": 582.0,
      "close": 588.0,
      "volume": 13456789.0
    }
  ],
  "metadata": {
    "stock_code": "2330",
    "start_date": "2024-01-15",
    "end_date": "2024-01-16",
    "data_points": 2
  }
}
```

**欄位說明**：

| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `stock_code` | string | ✅ | 股票代碼（與請求參數相同） |
| `chart_data` | array | ✅ | K線資料陣列（可為空陣列） |
| `chart_data[].time` | string | ✅ | 交易日期（YYYY-MM-DD） |
| `chart_data[].open` | number | ✅ | 開盤價（> 0） |
| `chart_data[].high` | number | ✅ | 最高價（> 0） |
| `chart_data[].low` | number | ✅ | 最低價（> 0） |
| `chart_data[].close` | number | ✅ | 收盤價（> 0） |
| `chart_data[].volume` | number | ✅ | 成交量（≥ 0） |
| `metadata` | object | 🟡 | 資料 metadata（可為 null） |
| `metadata.stock_code` | string | ✅ | 股票代碼 |
| `metadata.start_date` | string | ✅ | 實際資料起始日期 |
| `metadata.end_date` | string | ✅ | 實際資料結束日期 |
| `metadata.data_points` | integer | ✅ | 資料點數量 |

**資料聚合邏輯** (1分K → 日K):
- **Open**: FIRST_VALUE(開盤價) 按時間 ASC
- **High**: MAX(最高價)
- **Low**: MIN(最低價)
- **Close**: LAST_VALUE(收盤價) 按時間 DESC
- **Volume**: SUM(成交量)

---

## 2. 錯誤格式標準（US G-2 AC3）

### 2.1 統一錯誤結構

所有錯誤回應遵循以下格式：

```json
{
  "detail": {
    "error": {
      "code": "ERROR_CODE",
      "message": "人類可讀的錯誤訊息",
      "details": "詳細說明（選填）"
    }
  }
}
```

### 2.2 錯誤碼對照表

| 錯誤碼 | HTTP Status | 說明 | 觸發情境 |
|--------|-------------|------|----------|
| `INVALID_STOCK_CODE` | 400 | 股票代碼格式錯誤 | 長度不符、包含非法字元 |
| `INVALID_DATE_RANGE` | 400 | 日期範圍無效 | 起始日期 > 結束日期、格式錯誤 |
| `NO_DATA` | 404 | 查無資料 | 指定日期範圍無任何資料 |
| `DATABASE_ERROR` | 500 | 資料庫錯誤 | 連線失敗、查詢超時 |
| `INTERNAL_ERROR` | 500 | 伺服器內部錯誤 | 未預期的系統錯誤 |

### 2.3 錯誤回應範例

#### 範例 1: 日期範圍錯誤（400 Bad Request）

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

#### 範例 2: 股票代碼格式錯誤（422 Unprocessable Entity）

FastAPI 內建驗證錯誤格式（Pydantic ValidationError）：

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["query", "stock_code"],
      "msg": "String should have at least 4 characters",
      "input": "12"
    }
  ]
}
```

#### 範例 3: 查無資料（設計選擇：200 + 空陣列）

目前設計：回傳 200 OK + 空 `chart_data` 陣列

```json
{
  "stock_code": "9999",
  "chart_data": [],
  "metadata": {
    "stock_code": "9999",
    "start_date": "2024-01-01",
    "end_date": "2024-01-31",
    "data_points": 0
  }
}
```

**設計考量**：
- ✅ **優點**: 前端可統一處理回應結構，無需區分 200 vs 404
- 🔴 **替代方案**: 回傳 404 + `NO_DATA` 錯誤碼（需修改 Router 邏輯）

---

## 3. 擴充性設計原則（US G-2 AC2, AC5）

### 3.1 向後相容策略

#### ✅ 允許的變更（不破壞相容性）

1. **新增選填欄位**（`metadata` 新增欄位）
   ```json
   {
     "metadata": {
       "stock_code": "2330",
       "start_date": "2024-01-15",
       "end_date": "2024-01-16",
       "data_points": 2,
       "trading_days": 2,          // ✅ 新增：交易日數量
       "total_volume": 25802467.0  // ✅ 新增：總成交量
     }
   }
   ```

2. **新增選填 Query 參數**
   ```
   GET /api/chart/daily?stock_code=2330&start_date=2024-01-01&end_date=2024-01-31&interval=5m
   ```
   - `interval` 為選填，預設 `daily`
   - 舊客戶端不傳此參數仍正常運作

3. **新增 Response 欄位（選填層級）**
   ```json
   {
     "chart_data": [...],
     "metadata": {...},
     "indicators": null  // ✅ 新增：技術指標資料（選填）
   }
   ```

#### ❌ 禁止的變更（破壞相容性）

1. **刪除必填欄位**
   ```json
   // ❌ 移除 stock_code
   {
     "chart_data": [...]
   }
   ```

2. **修改欄位類型**
   ```json
   // ❌ volume 從 number 改為 string
   {
     "volume": "12345678"
   }
   ```

3. **修改必填參數名稱**
   ```
   // ❌ stock_code 改為 symbol
   GET /api/chart/daily?symbol=2330&start_date=...
   ```

### 3.2 版本管理策略（US G-2 AC4）

#### 方案 A: URL 版本控制（推薦）

```
GET /api/v1/chart/daily
GET /api/v2/chart/daily  // 未來版本
```

**優點**：
- 明確的版本邊界
- 易於路由與維護
- 支援多版本並存

#### 方案 B: Header 版本控制

```http
GET /api/chart/daily
Accept: application/vnd.taiwanmarket.v1+json
```

**優點**：
- URL 保持簡潔
- 符合 REST 最佳實踐

#### 當前實作

- 目前採用**無版本號**（`/api/chart/daily`）
- 承諾維持向後相容（遵循 3.1 原則）
- 若需破壞性變更，將遷移至 `/api/v2/chart/daily`

---

## 4. API 使用範例

### 4.1 成功查詢

#### curl

```bash
curl -X GET "http://localhost:8000/api/chart/daily?stock_code=2330&start_date=2024-01-01&end_date=2024-01-31" \
  -H "Accept: application/json"
```

#### Python (requests)

```python
import requests

response = requests.get(
    "http://localhost:8000/api/chart/daily",
    params={
        "stock_code": "2330",
        "start_date": "2024-01-01",
        "end_date": "2024-01-31"
    }
)

if response.status_code == 200:
    data = response.json()
    print(f"股票: {data['stock_code']}")
    print(f"資料點數: {len(data['chart_data'])}")
    for point in data['chart_data'][:5]:  # 顯示前 5 筆
        print(f"{point['time']}: O={point['open']}, C={point['close']}, V={point['volume']}")
else:
    error = response.json()
    print(f"錯誤: {error['detail']['error']['code']}")
    print(f"訊息: {error['detail']['error']['message']}")
```

#### JavaScript (fetch)

```javascript
const fetchChartData = async (stockCode, startDate, endDate) => {
  const url = new URL('http://localhost:8000/api/chart/daily');
  url.searchParams.append('stock_code', stockCode);
  url.searchParams.append('start_date', startDate);
  url.searchParams.append('end_date', endDate);

  try {
    const response = await fetch(url);
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`API Error: ${error.detail.error.code}`);
    }
    const data = await response.json();
    return data.chart_data;
  } catch (error) {
    console.error('Failed to fetch chart data:', error);
    throw error;
  }
};

// 使用範例
fetchChartData('2330', '2024-01-01', '2024-01-31')
  .then(chartData => console.log('Data points:', chartData.length))
  .catch(error => console.error(error));
```

### 4.2 錯誤處理

#### 日期範圍錯誤

```bash
curl -X GET "http://localhost:8000/api/chart/daily?stock_code=2330&start_date=2024-01-31&end_date=2024-01-01"
```

**Response (400)**:
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

## 5. 前端整合指引

### 5.1 TradingView Lightweight Charts 整合

API 回應格式**直接相容** TradingView Lightweight Charts：

```javascript
import { createChart } from 'lightweight-charts';

// 1. 取得 API 資料
const response = await fetch('/api/chart/daily?stock_code=2330&start_date=2024-01-01&end_date=2024-01-31');
const data = await response.json();

// 2. 建立圖表
const chart = createChart(document.getElementById('chart'), { width: 600, height: 400 });
const candlestickSeries = chart.addCandlestickSeries();

// 3. 直接餵入資料（格式相容）
candlestickSeries.setData(data.chart_data);

// 4. 建立成交量副圖
const volumeSeries = chart.addHistogramSeries({
  color: '#26a69a',
  priceFormat: { type: 'volume' },
  priceScaleId: '',
});
volumeSeries.setData(
  data.chart_data.map(d => ({ time: d.time, value: d.volume }))
);
```

### 5.2 Loading / Empty / Error 狀態處理

#### Loading State

```javascript
const [chartData, setChartData] = useState(null);
const [loading, setLoading] = useState(true);

useEffect(() => {
  setLoading(true);
  fetchChartData('2330', '2024-01-01', '2024-01-31')
    .then(data => setChartData(data))
    .finally(() => setLoading(false));
}, []);

if (loading) return <Spinner />;
```

#### Empty State（無資料）

```javascript
if (chartData && chartData.chart_data.length === 0) {
  return <EmptyState message="查無資料，請調整日期範圍或股票代碼" />;
}
```

#### Error State

```javascript
const [error, setError] = useState(null);

fetchChartData(...)
  .catch(err => {
    if (err.response?.data?.detail?.error) {
      const apiError = err.response.data.detail.error;
      setError(`${apiError.code}: ${apiError.message}`);
    } else {
      setError('網路錯誤，請稍後再試');
    }
  });

if (error) return <ErrorBanner message={error} />;
```

---

## 6. 測試契約

### 6.1 契約測試範圍（US G-2 AC1, AC3）

| 測試類型 | 驗證項目 | 測試檔案 |
|---------|---------|----------|
| **Response Schema** | 必要欄位存在、類型正確 | `test_api_contract.py` |
| **錯誤格式** | 所有錯誤符合統一格式 | `test_api_contract.py` |
| **資料正確性** | OHLC 邏輯、成交量對齊 | `test_chart_api.py` |
| **邊界條件** | 空資料、極端日期 | `test_chart_api.py` |

### 6.2 契約測試範例（Pseudocode）

```python
def test_response_schema_compliance():
    """驗證 Response 符合定義的 Schema（US G-2 AC1）"""
    response = client.get("/api/chart/daily", params={...})
    assert response.status_code == 200
    
    data = response.json()
    # 必要欄位檢查
    assert "stock_code" in data
    assert "chart_data" in data
    assert isinstance(data["chart_data"], list)
    
    # 若有資料，檢查 ChartDataPoint 結構
    if data["chart_data"]:
        point = data["chart_data"][0]
        assert all(k in point for k in ["time", "open", "high", "low", "close", "volume"])
        assert isinstance(point["open"], (int, float))
        assert point["open"] > 0

def test_error_format_consistency():
    """驗證所有錯誤符合統一格式（US G-2 AC3）"""
    # 測試 400 錯誤
    response = client.get("/api/chart/daily", params={"stock_code": "2330", "start_date": "invalid"})
    assert response.status_code in [400, 422]
    
    # 檢查錯誤結構（若為自定義錯誤）
    if response.status_code == 400:
        error = response.json()["detail"]["error"]
        assert "code" in error
        assert "message" in error
```

---

## 7. 附錄

### 7.1 相關規格文件

| 文件 | 路徑 | 說明 |
|------|------|------|
| Feature Spec | `specs/features/001-basic-chart-api/spec.md` | User Story 完整定義 |
| Data Model | `specs/features/001-basic-chart-api/data-model.md` | 資料結構與聚合邏輯 |
| Tasks | `specs/features/001-basic-chart-api/tasks.md` | 實作任務清單 |

### 7.2 變更日誌

| 版本 | 日期 | 變更內容 |
|------|------|----------|
| v1.0.0 | 2026-02-04 | 初版：定義日K線 API 契約，建立錯誤格式標準 |

---

**文件維護者**: AI Agent (GitHub Copilot)  
**最後更新**: 2026-02-04
