# Research Notes: 003-strategy-grid

> **Phase**: Phase 0 — Research  
> **建立日期**: 2026-03-02  
> **狀態**: ✅ 全部已決策，無殘留 NEEDS CLARIFICATION

---

## 研究摘要

本文件記錄 003-strategy-grid Plan 階段所有技術決策與研究結論，作為 `plan.md` 的依據。

---

## R-01：M03 查詢 API Response 格式範圍（CONFLICT-002）

> **問題**：PRD §4 API 格式包含 `event_window`, `horizons`, `metrics` 等 M04/M05 欄位，M03 應如何處理？

**決策**：採用 **方案 A（M03 子集 + 選填欄位預留）**

**理由**：
- `horizons`（+1/+3/+5/+10 日報酬）屬 M04（US D-1），`event_window` 屬 M04（US C-1），`metrics` 屬 M05
- M03 Response 僅包含 `samples`（樣本清單）與分頁 metadata
- 設計時預留 `event_window` / `horizons` / `metrics` 為 **選填（Optional）欄位**，M04/M05 填入，符合 `chart-api.md §3.1` 向後相容策略
- 方案 B（直接使用完整格式填空值）會製造混淆，讓呼叫端無法區分「尚未實作」與「確實無資料」

**對應**：`specs/system/contracts/strategy-query-api.md`（新建）

**替代方案**：方案 B（不採用，引入語意混淆）

---

## R-02：M03 API 端點路徑

> **問題**：新端點路徑要用 `/api/strategy/query` 還是其他？

**決策**：`POST /api/strategy/query`

**理由**：
- 與現有 `GET /api/chart/daily` 命名風格一致（`/api/{resource}/{action}`）
- 條件查詢使用 POST，因 Request body 包含複合條件（stock_codes[]、AND/OR 邏輯），GET query string 難以表達複雜條件
- RESTful 慣例：查詢操作若有複雜 body，使用 POST `/資源/search` 或 `/資源/query` 是業界常見做法

**分頁設計**：使用 query params `?page=1&page_size=100`（保持 URL 可共享性），Request body 僅放查詢條件。

**替代方案**：`GET /api/strategy/events`（不採用，無法優雅傳遞複雜 body）

---

## R-03：DB 表格 Schema 推算

> **問題**：`stock_daily` 與 `stock_events` 表格欄位是什麼？PRD 僅提到表名。

**決策**：依據 PRD 描述與 `[股價即時].[dbo].[1分K]` 現有結構推算如下，**實作前 MUST 確認實際 DB schema**

### stock_daily（日 OHLCV）推算 Schema

| 欄位名稱 | 型別 | 說明 | 備註 |
|----------|------|------|------|
| 日期 / trade_date | Date | 交易日期 | 需實際確認欄名 |
| 股票代號 / stock_code | VARCHAR | 股票代碼 | 需實際確認欄名 |
| 開盤價 / open | DECIMAL | 開盤價 | |
| 最高價 / high | DECIMAL | 最高價 | |
| 最低價 / low | DECIMAL | 最低價 | |
| 收盤價 / close | DECIMAL | 收盤價 | |
| 成交量 / volume | BIGINT | 成交量 | |

> ⚠️ **實作時 TODO**：執行 `SELECT TOP 1 * FROM stock_daily` 確認實際欄位名稱，再更新 `strategy_repository.py` 中的欄位對應。

### stock_events（事件資料）推算 Schema

| 欄位名稱 | 型別 | 說明 | 備註 |
|----------|------|------|------|
| stock_code | VARCHAR | 股票代碼 | 需實際確認欄名 |
| event_date | Date | 事件日期 | |
| event_type | VARCHAR | 事件類型標籤 | 僅供顯示，M03 不作查詢條件 |

> ⚠️ **實作時 TODO**：執行 `SELECT TOP 1 * FROM stock_events` 確認實際欄位名稱與可用事件類型範例。

**影響**：`StrategyRepository` 的 SQL 查詢欄位需對應實際 schema，strategy_repository.py 中應提供常數或配置管理欄位名稱。

---

## R-04：台灣交易日曆計算方式

> **問題**：計算事件前後 20/10 個「交易日」需要什麼工具？

**決策**：**查詢 `stock_daily` 表取得實際交易日清單**，不依賴外部套件

**理由**：
- `stock_daily` 已包含所有有效交易日的 OHLCV 資料，只有交易日才有 rows
- 只需取 `DISTINCT 日期 ORDER BY 日期` 即可得到完整交易日序列
- 不需引入 `exchange_calendars` / `trading-calendars` 等外部套件，減少依賴
- 此方式在資料庫中最準確（含補充假日、國定假日特殊情況）

**實作方式**：
```python
# 取事件日期 ± N 個交易日的範圍
# 1. 查 stock_daily 取 event_date 附近的 trading days list（ORDER BY 日期）
# 2. 以 index 計算 event_date 在序列中的位置
# 3. pre_start = trading_days[event_idx - pre_days]（最多取 pre_days 筆）
# 4. post_end = trading_days[event_idx + post_days]（最多取 post_days 筆）
```

**效能考量**：批次查詢時，一次取所有 event dates 涵蓋範圍的交易日列表，避免 N+1 查詢問題。

---

## R-05：Grid 渲染策略（效能）

> **問題**：50+ 小圖在 3 秒內渲染，應採虛擬滾動（Virtual Scrolling）還是直接渲染？

**決策**：**M03 採固定分頁（每頁 100 筆）+ 渲染時批次初始化**，不引入虛擬滾動

**理由**：
- US B-4 AC1 明確限制每頁 100 筆，有效控制 DOM 數量
- TradingView Lightweight Charts 的 chart 實例初始化成本較高，Virtual Scrolling 需要頻繁建立/銷毀圖表，反而影響效能
- 分頁後單頁最多 100 個圖表，在 4×5 預設佈局下只顯示 20 個（一頁一屏），實際 viewport 內圖表數量更少
- Virtual Scrolling 實作複雜度高（成本差異 > 50%），M03 優先採簡單策略，M04+ 若效能不足再引入

**替代方案**：Vue 3 Virtual Scroller（不採用，M03 分頁機制已充分控制）

**風險緩解**：若實測 50 圖渲染 > 3 秒，考慮：
1. 使用 `v-lazy` （Intersection Observer）延遲渲染 viewport 外的 MiniChart
2. 或在每個 MiniChart mount 時加入小延遲，分散 TradingView 初始化負載

---

## R-06：前端條件驗證策略（US B-1 AC5）

> **問題**：前端即時驗證如何實作？用 VeeValidate / Zod / 純 Vue 3 響應式？

**決策**：**Vue 3 Composition API + `computed` 響應式驗證**，不引入新驗證套件

**理由**：
- M03 驗證規則簡單：stock_code 格式、date_from ≤ date_to、price_min ≤ price_max（選填）
- 引入 VeeValidate/Zod 成本差異 > 20%（套件大小、學習成本），不符合可維護性優先原則
- Vue 3 `computed` + 欄位旁錯誤訊息顯示，與現有 M02 前端代碼風格一致

**驗證規則**：
| 欄位 | 規則 | 錯誤訊息 |
|------|------|----------|
| stock_codes | 每個代碼 4-10 字元，允許數字與大寫英文 | 「股票代碼格式不正確（4-10 字元，數字或大寫英文）」 |
| date_from | 有效日期，不超過今日 | 「請輸入有效的起始日期」 |
| date_to | 有效日期，≥ date_from | 「結束日期不得早於起始日期」 |
| price_min | 選填，≥ 0 | 「最低價不得為負數」 |
| price_max | 選填，≥ price_min（若兩者均填）| 「最高價不得低於最低價」 |

---

## R-07：SQL 安全設計（防 Injection）

> **問題**：複合條件（AND/OR）動態拼裝 SQL 時如何防 Injection？

**決策**：**白名單驗證 + 參數化查詢**

**實作方式**：
1. `stock_codes` 清單：每個代碼在 Python 層先驗正規表達式（`^[0-9A-Z]{4,10}$`），再以 `IN (?, ?, ...)` 參數化
2. `AND/OR` 邏輯：使用 Enum 型別（`QueryLogic.AND` / `QueryLogic.OR`），轉換為 SQL 關鍵字時使用字串 Map，**不允許前端傳任意字串**
3. `price_min / price_max / date_from / date_to`：直接使用 `pyodbc` 參數化 `?` 佔位符
4. **禁止任何** f-string 直接嵌入使用者輸入到 SQL 字串

---

## R-08：快取 Hook 預留設計（US G-1 相關）

> **問題**：M03 不實作快取，但需預留 hook。如何預留而不過度工程化？

**決策**：在 `StrategyService.query()` 中加入空佔位 `_cache_hook()` 方法，打 `# TODO: M04+ 實作快取（US G-1）` 標記

**不做**：不建立快取相關類別、不定義快取 interface，避免過度工程化。

---

## R-09：分頁設計細節

> **問題**：分頁使用 offset-based 還是 cursor-based？

**決策**：**Offset-based 分頁**（`page` + `page_size`）

**理由**：
- 策略查詢結果固定排序（按事件日期排序），不會因插入新資料而錯頁
- `stock_events` 為唯讀資料，不存在新增/刪除導致的分頁漂移問題
- Cursor-based 複雜度高，對此場景無必要

**SQL 實作**：
```sql
ORDER BY event_date ASC
OFFSET (page - 1) * page_size ROWS
FETCH NEXT page_size ROWS ONLY
```

---

## R-10：Backend/Frontend 分工確認

> **問題**：事件日置中（pre=20/post=10）的 K 線資料切割，後端做還是前端做？

**決策**：**後端計算，回傳已切割的 chart_data**

**理由**：
- 前端只需渲染，不需要知道交易日曆計算邏輯
- 後端 `SampleResult.chart_data` 已包含對齊好的 OHLCV 陣列（預設最多 pre+post+1=31 筆），前端直接渲染
- 前端 MiniChart 元件只需負責接收 `chart_data[]` 並以 TradingView 渲染，事件日 index 由後端在 `SampleResult` 中提供（`event_bar_index` 欄位）

**新增欄位**：`SampleResult.event_bar_index`（Integer）— 指定事件日在 `chart_data[]` 中的索引位置，前端用此值設定 TradingView 的可見範圍，確保事件日置中顯示。

---

## 決策匯總

| ID | 問題 | 決策 | 信心 |
|----|------|------|------|
| R-01 | API Response 格式範圍 | 方案 A：M03 子集，選填預留 M04 欄位 | ✅ High |
| R-02 | API 端點路徑 | `POST /api/strategy/query` + query params 分頁 | ✅ High |
| R-03 | DB Schema | 推算結構，實作前 MUST 確認 | 🟡 Medium（需確認）|
| R-04 | 台灣交易日曆 | 查 stock_daily DISTINCT 日期，不用外部套件 | ✅ High |
| R-05 | Grid 渲染策略 | 固定分頁 + 批次渲染，不引入 Virtual Scrolling | ✅ High |
| R-06 | 前端條件驗證 | Vue 3 computed 響應式，不引入外部套件 | ✅ High |
| R-07 | SQL Injection 防護 | 白名單驗證 + 全面參數化查詢 | ✅ High |
| R-08 | 快取 Hook 預留 | 空佔位方法 + TODO 標記 | ✅ High |
| R-09 | 分頁設計 | Offset-based（page + page_size） | ✅ High |
| R-10 | 資料切割責任 | 後端切割，回傳 chart_data[] + event_bar_index | ✅ High |

---

## 殘留項目（無 NEEDS CLARIFICATION）

無。所有研究問題均已決策。R-03 的 DB schema 確認為**實作時的 TODO**（非規格不確定性）。
