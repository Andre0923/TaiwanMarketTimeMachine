# Research Report: 基礎繪圖與 API 格式

> **Feature ID**: 001-basic-chart-api  
> **Research Version**: 1.0  
> **Created**: 2026-02-03  
> **Status**: Completed

---

## 1. 研究目標

本研究旨在解決 Feature Spec 中列出的 5 個 Open Questions，確保開發前所有技術決策明確。

---

## 2. Research Items

### R1: 1分K 資料表 Schema（對應 Q1）

**研究問題**：確認現有資料表的完整 Schema，包括欄位名稱、型別、索引策略。

**研究結果**：✅ **已確認**（2026-02-04）

**資料來源**：`[股價即時].[dbo].[1分K]`

**確認方式**：
```sql
SELECT TOP 5 * FROM [股價即時].[dbo].[1分K]
```

**實際 Schema**：

| 欄位名稱（中文） | 對應英文 | 資料型別 | 說明 |
|-----------------|---------|----------|------|
| 日期 | date | VARCHAR/DATE | 交易日期（格式：YYYY-MM-DD） |
| 時間 | time | VARCHAR/TIME | 分鐘時間點（格式：HH:MM:SS） |
| 股票代號 | stock_code | VARCHAR | 股票代碼（如："1101"） |
| 開盤價 | open_price | FLOAT | 該分鐘開盤價 |
| 最高價 | high_price | FLOAT | 該分鐘最高價 |
| 最低價 | low_price | FLOAT | 該分鐘最低價 |
| 收盤價 | close_price | FLOAT | 該分鐘收盤價 |
| 成交量 | volume | FLOAT | 該分鐘成交量（單位：股） |
| 成交金額 | amount | FLOAT | 該分鐘成交金額（新台幣） |
| 更新時間 | updated_at | DATETIME | 資料更新時間戳記 |

**範例資料（前 5 筆）**：
```
日期         時間        股票代號  開盤價    最高價    最低價    收盤價    成交量    成交金額      更新時間
2022-01-03  09:01:00   1101    48.05    48.15    48.0     48.1     311.0    14944400.0  2023-11-30 20:42:08.753
2022-01-03  09:01:00   1102    44.4     44.45    44.4     44.45    122.0    5417100.0   2023-11-30 20:42:20.547
2022-01-03  09:01:00   1103    20.75    20.75    20.75    20.75    1.0      20750.0     2023-11-30 20:42:30.677
2022-01-03  09:01:00   1104    21.7     21.7     21.7     21.7     19.0     412300.0    2023-11-30 20:42:34.327
2022-01-03  09:01:00   1108    11.9     11.9     11.9     11.9     7.0      83300.0     2023-11-30 20:42:37.410
```

**關鍵發現**：
1. ✅ 欄位名稱為**中文**，需在 Repository 層處理對應
2. ✅ 資料型別為 FLOAT（非 DECIMAL），需注意精度問題
3. ✅ 資料格式：日期與時間分開為兩個欄位
4. ✅ 包含「成交金額」欄位（本 Feature 暫不使用）
5. ⚠️ 資料最早為 2022-01-03（測試時需注意日期範圍）

**日K聚合策略**（Service 層實作）：
- **Open（開盤）**：當日第一筆（按 `時間` ASC）的 `開盤價`
- **High（最高）**：當日所有 `最高價` 的 MAX
- **Low（最低）**：當日所有 `最低價` 的 MIN
- **Close（收盤）**：當日最後一筆（按 `時間` DESC）的 `收盤價`
- **Volume（成交量）**：當日所有 `成交量` 的 SUM

**SQL 查詢範例**（Repository 層）：
```sql
SELECT 
    [日期],
    [股票代號],
    (SELECT TOP 1 [開盤價] 
     FROM [股價即時].[dbo].[1分K] AS inner_t
     WHERE inner_t.[日期] = outer_t.[日期] 
       AND inner_t.[股票代號] = outer_t.[股票代號]
     ORDER BY [時間] ASC) AS [開盤價],
    MAX([最高價]) AS [最高價],
    MIN([最低價]) AS [最低價],
    (SELECT TOP 1 [收盤價] 
     FROM [股價即時].[dbo].[1分K] AS inner_t
     WHERE inner_t.[日期] = outer_t.[日期] 
       AND inner_t.[股票代號] = outer_t.[股票代號]
     ORDER BY [時間] DESC) AS [收盤價],
    SUM([成交量]) AS [成交量]
FROM [股價即時].[dbo].[1分K] AS outer_t
WHERE [股票代號] = :stock_code
  AND [日期] BETWEEN :start_date AND :end_date
GROUP BY [日期], [股票代號]
ORDER BY [日期] ASC
```

**後續行動**：
1. ✅ 已更新 `data-model.md`
2. ✅ 已記錄至 `research.md`
3. ⏭️ 進入 Phase 1 實作階段

---

### R2: API Endpoint 設計（對應 Q2）

**研究問題**：完整的 Endpoint 路徑、Query Parameters、錯誤碼規範。

**決策**：**選項 A** — RESTful 慣例，錯誤碼清晰分類

**Rationale**：
- RESTful 設計易於理解和維護
- 語意化錯誤碼（INVALID_STOCK_CODE 等）便於前端錯誤處理
- 符合業界標準實務

**詳細設計**：

#### Endpoint
```
GET /api/v1/chart-data
```

#### Query Parameters
| 參數 | 類型 | 必填 | 說明 | 範例 |
|------|------|------|------|------|
| `stock_code` | String | ✅ | 股票代碼 | 2330 |
| `start_date` | String | ✅ | 起始日期（YYYY-MM-DD） | 2024-01-01 |
| `end_date` | String | ✅ | 結束日期（YYYY-MM-DD） | 2024-01-31 |

#### 成功 Response (200 OK)
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
      }
    ]
  }
}
```

#### 錯誤 Response
```json
{
  "error": {
    "code": "INVALID_STOCK_CODE | INVALID_DATE_RANGE | NO_DATA | INTERNAL_ERROR",
    "message": "描述性錯誤訊息"
  }
}
```

#### 錯誤碼定義

| 錯誤碼 | HTTP Status | 說明 | 前端行為 |
|--------|-------------|------|----------|
| `INVALID_STOCK_CODE` | 400 | 股票代碼不存在或格式錯誤 | 顯示：「查無此股票代碼，請確認後重試」 |
| `INVALID_DATE_RANGE` | 400 | 日期範圍不合法（如 end < start） | 顯示：「日期範圍不正確，請調整後重試」 |
| `NO_DATA` | 404 | 查詢結果為空（該期間無交易資料） | 顯示：「查無資料，請調整查詢條件」 |
| `INTERNAL_ERROR` | 500 | 伺服器錯誤（DB 連線失敗等） | 顯示：「系統發生錯誤，請聯繫技術支援」 |

**Alternatives Considered**：
- 選項 B（簡化版）：統一錯誤碼會降低前端錯誤處理精確度
- 選項 C（GraphQL）：學習成本高，本階段不適用

---

### R3: Loading Spinner 視覺樣式（對應 Q3）

**研究問題**：使用哪種動畫？顏色與尺寸？

**決策**：**選項 A** — Material Design Circular Spinner

**Rationale**：
- Material Design 為業界標準，使用者熟悉度高
- 與 Vue 3 生態系（如 Vuetify、Element Plus）整合良好
- 不會干擾圖表主視覺

**詳細規格**：

| 屬性 | 值 |
|------|---|
| 動畫類型 | Circular Spinner（圓形旋轉） |
| 顏色 | Primary Color (#1976d2) |
| 尺寸 | 40x40px |
| 文案 | 「載入中...」 |
| 位置 | 圖表容器中央，垂直水平置中 |
| 背景 | 半透明遮罩（rgba(255,255,255,0.9)） |

**實作建議**：
```vue
<template>
  <div v-if="isLoading" class="loading-overlay">
    <div class="spinner"></div>
    <p>載入中...</p>
  </div>
</template>

<style scoped>
.loading-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e3f2fd;
  border-top-color: #1976d2;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
```

**Alternatives Considered**：
- 選項 B（進度條）：無法預測載入時間，不適用
- 選項 C（骨架屏）：實作成本高，優先度低

---

### R4: 錯誤訊息使用者文案（對應 Q4）

**研究問題**：不同錯誤類型的具體文案。

**決策**：**選項 A** — 清楚說明問題與建議行動

**Rationale**：
- 符合 UX Writing 最佳實務（問題 + 行動建議）
- 降低使用者困惑與支援成本
- 提升整體使用者體驗

**文案規範**：

| 錯誤類型 | 使用者文案 | 行動按鈕 |
|----------|-----------|----------|
| 網路錯誤 | 「無法連線至伺服器，請檢查網路連線後重試」 | 「重試」 |
| 逾時錯誤 | 「請求逾時，請稍後再試」 | 「重試」 |
| 資料不存在 | 「查無資料，請調整查詢條件」 | 「返回」 |
| 伺服器錯誤 | 「系統發生錯誤，請聯繫技術支援」 | 「返回」+ 錯誤碼顯示 |
| 無效參數 | 「查詢條件不正確，請重新輸入」 | 「返回」 |

**錯誤 UI 元件規格**：
```vue
<template>
  <div class="error-display">
    <div class="error-icon">⚠️</div>
    <h3 class="error-title">{{ errorTitle }}</h3>
    <p class="error-message">{{ errorMessage }}</p>
    <button @click="handleRetry" v-if="showRetry">重試</button>
    <button @click="handleBack">返回</button>
  </div>
</template>
```

**Tone & Voice 原則**：
- 使用繁體中文，避免過於技術化的術語
- 語氣平和、提供解決方向
- 避免「失敗」、「錯誤」等負面字眼的過度使用

**Alternatives Considered**：
- 選項 B（簡化版）：資訊不足，使用者無法判斷問題
- 選項 C（技術詳細版）：一般使用者難以理解

---

### R5: 小圖放大過場動畫（對應 Q5）

**研究問題**：是否需要過場動畫？動畫時長？

**決策**：**選項 A** — Fade + Scale 動畫，200ms

**Rationale**：
- 200ms 為人眼可感知但不造成延遲的平衡點
- Fade + Scale 提供流暢的視覺過渡
- 提升使用者體驗，不會影響效能

**動畫規格**：

| 屬性 | 值 |
|------|---|
| 動畫效果 | Fade（透明度 0→1）+ Scale（縮放 0.95→1） |
| 動畫時長 | 200ms |
| Easing Function | ease-in-out（緩入緩出） |
| 觸發時機 | 小圖點擊 → 放大檢視 |

**實作建議**：
```vue
<template>
  <transition name="enlarge">
    <div v-if="isEnlarged" class="enlarged-chart">
      <!-- Chart Component -->
    </div>
  </transition>
</template>

<style scoped>
.enlarge-enter-active,
.enlarge-leave-active {
  transition: all 0.2s ease-in-out;
}

.enlarge-enter-from {
  opacity: 0;
  transform: scale(0.95);
}

.enlarge-enter-to {
  opacity: 1;
  transform: scale(1);
}

.enlarge-leave-from {
  opacity: 1;
  transform: scale(1);
}

.enlarge-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
```

**效能考量**：
- 使用 CSS Transition（硬體加速）
- 避免 JavaScript 動畫（效能較差）
- 動畫期間禁用互動（防止連續點擊）

**Alternatives Considered**：
- 選項 B（無動畫）：直接切換，缺乏視覺連貫性
- 選項 C（400ms 複雜動畫）：過長會造成延遲感

---

## 3. 技術棧最佳實務研究

### 3.1 TradingView Lightweight Charts

**研究重點**：台股紅漲綠跌設定、Grid 模式效能

**發現**：
1. **顏色設定**（已驗證）：
   ```javascript
   const candlestickSeries = chart.addCandlestickSeries({
     upColor: '#ef5350',      // 紅色（漲）
     downColor: '#26a69a',    // 綠色（跌）
     borderVisible: false,
     wickUpColor: '#ef5350',
     wickDownColor: '#26a69a',
   });
   ```

2. **Grid 模式效能優化**（待實測）：
   - 建議每個 Chart Instance 獨立建立（不共用）
   - 小圖使用較低解析度（如 200x150px）
   - 延遲載入：僅載入可見區域的圖表

3. **記憶體管理**：
   - 元件銷毀時必須呼叫 `chart.remove()`
   - 避免記憶體洩漏

**推薦資源**：
- [官方文件](https://tradingview.github.io/lightweight-charts/)
- [GitHub Examples](https://github.com/tradingview/lightweight-charts)

---

### 3.2 FastAPI + MSSQL 整合

**研究重點**：非同步連線、錯誤處理

**發現**：
1. **連線池設定**：
   ```python
   from sqlalchemy import create_engine
   from sqlalchemy.pool import QueuePool
   
   engine = create_engine(
       "mssql+pyodbc://...",
       poolclass=QueuePool,
       pool_size=10,
       max_overflow=20
   )
   ```

2. **非同步支援**：
   - pyodbc 不支援原生非同步
   - 使用 `run_in_executor` 包裝同步呼叫
   - 或考慮 `aioodbc`（實驗性）

3. **錯誤處理模式**：
   ```python
   try:
       result = await db.execute(query)
   except pyodbc.IntegrityError:
       raise HTTPException(status_code=400, detail={"code": "INVALID_STOCK_CODE"})
   except pyodbc.OperationalError:
       raise HTTPException(status_code=500, detail={"code": "INTERNAL_ERROR"})
   ```

---

## 4. 待驗證假設

### A1: TradingView Charts Grid 模式效能

**假設**：20+ 小圖同時渲染的效能可接受（60 FPS）

**驗證方式**：
- Phase 1 建立 POC，測試 20 個小圖並列
- 使用 Chrome DevTools Performance 測量 FPS
- 若不達標，實作 Virtual Scrolling

**風險等級**：MEDIUM

---

### A2: API 回應時間 < 2 秒

**假設**：MSSQL 查詢 100 根 K 線的回應時間 < 2 秒

**驗證方式**：
- Phase 1 實作 API 後進行壓力測試
- 測試情境：單一查詢、併發 10 個查詢
- 若不達標，實作快取或索引優化

**風險等級**：LOW（資料量不大，SQL 查詢簡單）

---

## 5. 決策摘要表

| 問題 | 決策 | 優先級 | 狀態 |
|------|------|--------|------|
| Q1: stock_daily Schema | 使用現有表，**等待 User 提供** | 高 | ⚠️ Pending |
| Q2: API Endpoint | RESTful + 語意化錯誤碼 | 高 | ✅ Resolved |
| Q3: Loading Spinner | Circular Spinner (#1976d2, 40px) | 中 | ✅ Resolved |
| Q4: 錯誤訊息文案 | 清楚說明 + 行動建議 | 中 | ✅ Resolved |
| Q5: 放大動畫 | Fade + Scale, 200ms | 低 | ✅ Resolved |

---

## 6. 後續行動

### 立即行動（Phase 0 → Phase 1）

1. ✅ 完成本 research.md
2. ⏳ **等待 User 提供 stock_daily Schema**（Q1）
3. ✅ 準備進入 Phase 1（生成設計文件）

### Phase 1 行動

1. 建立 `data-model.md`（使用 User 提供的 Schema 或推測 Schema + 標註待驗證）
2. 建立 `contracts/chart-api.md`（依據 R2 決策）
3. 建立 `quickstart.md`（開發環境設定指南）
4. 建立 UI 文件（`specs/system/ui/*`）

---

**文件版本**：v1.0.0  
**研究完成度**：4/5 項已解決，1 項等待 User 輸入  
**下一步**：進入 Phase 1（設計文件生成）
