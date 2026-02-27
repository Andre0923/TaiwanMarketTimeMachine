# M03 設計上下文（Milestone Context）

> **Milestone**：M03 — Strategy Grid 核心  
> **產生日期**：2026-02-26  
> **PRD 來源**：`docs/requirements/PRD-ASSRP.md`  
> **衝突檢查**：✅ 已執行  
> **輸出版本**：1.0.0

---

## Escalation Log（漸進式讀取紀錄）

| Stage | 讀取目標 | 讀取理由 |
|-------|----------|----------|
| Stage 1 | PRD Section Headers、M03 Milestone US ID 清單 | 建立候選比對表 |
| Stage 2 | PRD §2.2 Strategy Grid、§3 DB Schema、§4 API Response、§5 User Flow | US B-1/B-2/B-3/B-4 直接關聯 |
| Stage 2 | `specs/system/data-model.md` 全文 | 衝突比對：Entity 名稱與 stock_code 驗證規則 |
| Stage 2 | `specs/system/contracts/chart-api.md` Lines 1-200 | 衝突比對：API 格式與 stock_code 驗證 |
| Stage 2 | `specs/system/spec.md` §3 Behaviors | 衝突比對：現有行為定義範圍 |
| Stage 2 | `specs/system/ui/ui-structure.md` 全文 | 衝突比對：Grid UI Screen 定義 |
| Stage 2 | `specs/system/flows.md` Section Headers | 衝突比對：Strategy Grid 流程定義 |

---

## 一、Milestone 範圍定義

### 目標 Milestone

**M03 — Strategy Grid 核心**

### 包含的 US ID

| US ID | 摘要 | 關鍵字（用於 PRD 匹配） |
|-------|------|------------------------|
| US B-1 | 結構化條件查詢 | 條件查詢、SQL、股票代碼、日期範圍、AND/OR |
| US B-2 | Grid 多圖並列顯示 | Grid、4x5、小圖、並列、K線渲染 |
| US B-3 | 事件日置中對齊 | 事件日、置中、Event Anchoring、交易日 |
| US B-4 | 查詢結果數量限制與分頁 | 分頁、100筆、pagination |

---

## 二、PRD → Milestone 關聯性對應

### Stage 1：結構掃描結果

| PRD Section | 匹配的 US ID | 關聯類型 | 擷取類別 |
|-------------|-------------|----------|---------|
| §2.2 Strategy Grid Mode（F-04/F-05/F-06） | US B-1, B-2, B-3 | ✅ 直接關聯 | DM + CT + FL |
| §3 DB Schema（stock_daily, stock_events） | US B-1 | ✅ 直接關聯 | DM |
| §3 保險絲設計（event_study_result_cache） | (US G-1，非 M03) | ⚪ 範圍外 | — |
| §4 API Response 規範 | US B-1, B-2 | 🟡 間接關聯 | CT |
| §5 User Flow — Strategy Grid Mode | US B-1~B-4 | ✅ 直接關聯 | FL |
| §2.3 Time Window Engine（F-08~F-11） | (M04，非 M03) | ⚪ 範圍外 | — |
| §6 Roadmap Phase 2 | US B-2, B-3 | 🟡 間接關聯 | TN |

---

## 三、擷取的設計上下文

### 【DM】資料模型

#### DM-1：DB 表格結構（PRD §3）

**來源**：`docs/requirements/PRD-ASSRP.md` §3 DB Schema

| 表格名稱 | 用途 | 備註 |
|----------|------|------|
| `stock_daily` | 日 OHLCV 資料 | 主要查詢目標（US B-1 AC1） |
| `stock_events` | 事件資料（事件日期、股票代碼） | US B-3 事件日置中計算的資料來源 |

> **欄位細節**：PRD 未明確定義表格欄位，Plan 階段 SHOULD 在 `specs/system/data-model.md` 補充這兩個 Entity 的詳細schema。

#### DM-2：快取表（PRD §3 保險絲設計 1）

**來源**：`docs/requirements/PRD-ASSRP.md` §3

```
Table: event_study_result_cache
Key: hash(SQL + pre_days + post_days + horizons)
```

> ⚠️ **M03 邊界提醒**：此快取表屬於 US G-1（查詢結果快取機制）之範疇，**不在 M03 內實作**。但設計 US B-1 的查詢 API 時，SHOULD 預留快取 hook 位置，避免未來需要大幅重構。

---

### 【FL】流程設計

#### FL-1：Strategy Grid Mode 使用者流程（PRD §5）

**來源**：`docs/requirements/PRD-ASSRP.md` §5 User Flow

```
1. 設定條件（SQL / AI）          ← US B-1
2. 設定 Time Window              ← M04（US C-1，非 M03）
3. 顯示 Grid（事件置中）          ← US B-2 + B-3
4. 顯示 Micro Backtest 側欄       ← M05（US D-3，非 M03）
5. 點擊小圖放大檢視              ← 已完成（US A-3，M02）
6. 匯出 Excel                   ← M05（US E-1，非 M03）
```

**M03 負責步驟**：Step 1（條件查詢）+ Step 3（Grid 渲染 + 事件置中）  
**M03 不負責**：Step 2（Time Window 設定於 M04 實作）、Step 4/6（M05 實作）

#### FL-2：查詢分頁流程（US B-4）

```
查詢執行 → 結果 > 100 筆
  → 只載入前 100 筆
  → 顯示分頁狀態（當前頁/總頁數）
  → 使用者點擊下一頁 → 載入下一頁樣本 → 更新 Grid
```

---

### 【CT】契約定義

#### CT-1：PRD 規劃的完整 API Response 格式（PRD §4）

**來源**：`docs/requirements/PRD-ASSRP.md` §4 API Response 規範

```json
{
  "event_window": { "pre": 20, "post": 10 },
  "horizons": [1, 3, 5, 10],
  "samples": [...],
  "metrics": {
    "avg_return": {},
    "win_rate": {},
    "max_drawdown": {}
  }
}
```

> ⚠️ **M03 適用範圍說明**：  
> 此 PRD 格式為完整的 Micro Backtest API 格式（包含 M04 的 `horizons` 與 `metrics`）。  
> M03 實作查詢 API 時，**應僅包含 M03 範圍內的欄位**（`samples` 與基本查詢 metadata），`horizons` 與 `metrics` 留給 M04 擴充。  
> 設計應遵循 System contracts 的向後相容策略（chart-api.md §3.1）：以新增選填欄位方式擴充。

#### CT-2：M03 建議的查詢 API 新端點（需在 Plan 階段設計）

**來源**：PRD §2.2 F-04（條件查詢功能）

M03 需要新增查詢 endpoint（`/api/strategy/query` 或類似路徑），現有 System 只有 `GET /api/chart/daily`。  
新端點需設計：
- **Request**：查詢條件（股票代碼、日期範圍、AND/OR 邏輯）
- **Response**：符合條件的樣本清單（含股票代碼、事件日期、分頁資訊）

---

### 【CF】設定規格

#### CF-1：分頁設定（US B-4 AC1）

| 設定項目 | 規則 | 來源 |
|----------|------|------|
| 單頁最大樣本數 | 100 筆 | US B-4 AC1 |
| 分頁導航方式 | 下一頁/上一頁 + 頁碼輸入 | US B-4 AC2 |

#### CF-2：Grid 佈局設定（US B-2）

| 設定項目 | 預設值 | 範圍 | 來源 |
|----------|--------|------|------|
| Grid 欄數 | 4 | 可調整 | US B-2 AC1/AC2 |
| Grid 列數 | 5 | 可調整 | US B-2 AC1/AC2 |
| 最大渲染時間 | 3 秒 | 50+ 小圖 | US B-2 AC3 |

---

### 【TN】技術備註

#### TN-1：Grid 渲染效能（PRD §2.2 F-05）

**來源**：PRD §2.2, US B-2 AC3

- Grid 需考慮 **Virtual Scrolling** 或 **Lazy Loading** 策略
- Roadmap Phase 2 明確標示「Grid + Event Anchoring」為核心任務
- 大量小圖（50+）渲染時間需在 3 秒內完成

#### TN-2：事件日計算基準

**來源**：US B-3 AC2, US-B strategy-grid.md 技術備註

- 事件前後天數計算基準為**交易日（Trading Days）**，非日曆日
- 需建立基於台灣股市交易日曆的計算工具函式

#### TN-3：SQL 安全設計

**來源**：US B-1 AC1/AC2，M03 Milestone 風險項目

- 條件查詢 MUST 使用**參數化查詢（Parameterized Query）**，禁止字串拼接
- 複合條件（AND/OR）邏輯解析需防止 SQL Injection

#### TN-4：架構選型（PRD §1.2）

| 角色 | 技術 | 備註 |
|------|------|------|
| 前端 | Vue 3 + TradingView Lightweight Charts | 已實作（M02） |
| 後端 | FastAPI | 已實作（M01） |
| DB | Microsoft SQL Server | 使用 `stock_daily`, `stock_events` 表 |

---

## 四、衝突檢測報告

### 候選比對清單（Stage 1 建立）

| PRD 擷取項目 | 類別 | System 候選比對 |
|-------------|------|----------------|
| stock_events 表 | DM | data-model.md（無此 Entity） |
| stock_daily 表 | DM | data-model.md（無此 Entity） |
| Strategy Grid User Flow | FL | flows.md（空白範本） |
| 查詢 API Response 格式 | CT | contracts/chart-api.md（現有格式） |
| Grid UI 畫面 | UI | ui/ui-structure.md（空白範本） |
| stock_code 驗證規則 | DM | data-model.md vs chart-api.md |

---

### 衝突分析結果

#### ✅ 擴展（非衝突）—— 4 項

| 項目 | 說明 |
|------|------|
| `stock_daily` 表 | System data-model.md 無此 Entity，M03 新增為純擴展 |
| `stock_events` 表 | System data-model.md 無此 Entity，M03 新增為純擴展 |
| Strategy Grid 查詢流程 | System flows.md 為空白範本，M03 新增為純擴展 |
| Grid UI 畫面 / 查詢元件 | System ui-structure.md 為空白範本，M03 新增為純擴展 |

---

#### ⚠️ 潛在衝突 —— 2 項

---

**[CONFLICT-001]** `stock_code` 驗證規則不一致（System 內部，影響 M03）

| 屬性 | 值 |
|------|----|
| **衝突類型** | 約束衝突（Constraint Conflict） |
| **嚴重性** | MEDIUM |
| **狀態** | ✅ **已決策（方案 A，2026-02-27）** |
| **影響 M03** | YES — M03 查詢 API 統一採 4-10 字元規則 |

**現況差異**：

| 來源 | stock_code 驗證規則 |
|------|-------------------|
| `specs/system/data-model.md`（ChartMetadata） | 必須為 **4 位數字字串** |
| `specs/system/contracts/chart-api.md`（Request Params） | 長度 **4-10**，允許**數字與大寫英文** |
| `specs/system/spec.md`（ErrorCode 說明） | 代碼包含**非數字字元**時觸發錯誤 |

**影響 M03**：US B-1 設計新查詢 API 時，需決定 `stock_code` 的驗證規則（ETF 代碼如 `006208` 為 6 碼；外資代碼可能含英文字母），若沿用 4 位數字限制，可能排除有效股票代碼。

**決策結果（2026-02-27）**：

- ✅ **方案 A（已採用）**：採用 `contracts/chart-api.md` 的較寬鬆規則（4-10 字元，含大寫英文），M03 實作時統一使用，後續透過 Unify Flow 更新 `data-model.md` 與 `spec.md`
- ~~方案 B：維持 4 位數字限制~~（未採用）

> ✅ **決策已確認**：`stock_code` 驗證規則 = 4-10 字元，允許數字與大寫英文（對齊 `contracts/chart-api.md`）。  
> Unify Flow 完成後，`data-model.md`（ChartMetadata）與 `spec.md`（ErrorCode 說明）需同步更新。

---

**[CONFLICT-002]** PRD §4 API 格式範圍包含 M04 欄位（邊界待確認）

| 屬性 | 值 |
|------|----|
| **衝突類型** | 語意待確認（Scope Ambiguity） |
| **嚴重性** | LOW |
| **狀態** | 待確認 |
| **影響 M03** | 需在 Plan 階段釐清 |

**現況差異**：

| 來源 | 說明 |
|------|------|
| `docs/requirements/PRD-ASSRP.md` §4 | API 格式包含 `event_window`, `horizons`, `samples`, `metrics` 四個頂層欄位 |
| M03 邊界聲明 | M03 不涵蓋 Time Window 設定與 Micro Backtest 統計 |

**影響**：`horizons`（+1/+3/+5/+10 日報酬）屬於 M04（US D-1），`event_window` 屬於 M04（US C-1），若 M03 查詢 API 直接使用 PRD §4 格式，會引入 M03 尚不實作的欄位。

**建議解決方案**：

- **方案 A（建議）**：M03 查詢 API 僅回傳 `samples`（樣本清單）與查詢 metadata，設計時預留 `event_window`/`horizons`/`metrics` 為選填欄位，M04 實作時再填入，符合向後相容策略
- **方案 B**：M03 直接使用完整 PRD 格式但以空值/預設值填充 M04 欄位

> 🟡 **建議確認**：在 Plan 階段選擇方案 A 或 B，並在新 contract 文件中明確定義 M03 查詢 API 格式。

---

## 五、Plan 階段行動建議

### 必須在 Plan 前決策（Pre-Plan）

| 優先序 | 事項 | 狀態 |
|--------|------|------|
| ✅ 1 | `stock_code` 驗證規則統一 | **已決策（方案 A）**：4-10 字元，含大寫英文 |
| 🟡 2 | M03 查詢 API Response 格式 | 建議採方案 A（M03 子集格式，預留選填欄位） |

### Plan 階段建議新增至 System 的設計

| 類別 | 待新增項目 | 目標檔案 |
|------|-----------|---------|
| DM | `StockEvent` Entity（股票代碼、事件日期、事件類型） | `specs/system/data-model.md` |
| DM | `StrategyQueryParams`（查詢條件 DTO） | `specs/system/data-model.md` |
| DM | `SampleResult`（單筆樣本：股票代碼、事件日期） | `specs/system/data-model.md` |
| DM | `GridQueryResponse`（樣本清單 + 分頁 metadata） | `specs/system/data-model.md` |
| CT | `POST /api/strategy/query` 契約 | `specs/system/contracts/strategy-query-api.md（新建）` |
| FL | Strategy Grid Mode 查詢流程 | `specs/system/flows.md` |
| UI | Grid 畫面（[UI-SCR-002] Strategy Grid View） | `specs/system/ui/ui-structure.md` |
| UI | 查詢條件元件（[UI-CMP-002] QueryPanel） | `specs/system/ui/ui-structure.md` |

---

## 六、DoD 檢查清單

### 本文件完成標準

- [x] Milestone 範圍已定義（US B-1/B-2/B-3/B-4）
- [x] PRD 相關區段已擷取（§2.2, §3, §4, §5）
- [x] 擷取內容皆有來源標註（PRD Section + 行號範圍）
- [x] 衝突檢測已執行
- [x] Escalation Log 已完整記錄

### 衝突處理狀態

- [x] **CONFLICT-001**（MEDIUM）：stock_code 驗證規則 → ✅ 已決策（方案 A，2026-02-27）
- [ ] **CONFLICT-002**（LOW）：PRD §4 格式範圍 → 建議 Plan 階段選定方案

---

> **下一步**：執行 `speckit specify --milestone M03` 開始 M03 需求細化。
