# Milestone 索引與狀態追蹤

> **專案名稱**：AI-Assisted Stock Strategy Research Platform（ASSRP）  
> **建立日期**：2026-02-03  
> **最後更新**：2026-02-26

---

## 📋 Milestone 總覽

| Milestone | 名稱 | US 數量 | 狀態 | 預計完成 |
|-----------|------|---------|------|----------|
| [M01](M01-basic-chart-and-api.md) | 基礎繪圖與 API 格式 | 2 | ✅ 已完成 | 2026-02-04 |
| [M02](M02-frontend-chart-interactions.md) | 前端圖表互動功能 | 3 | ✅ 已完成 | 2026-02-09 |
| [M03](M03-strategy-grid.md) | Strategy Grid 核心 | 4 | 🧩 執行中 | — |
| M04 | 事件研究統計 | 7 | 🔘 尚未規劃 | — |
| M05 | AI 協作增強 | 2 | 🔘 尚未規劃 | — |

**總計**：5 個 Milestone，22 個 User Stories

---

## 📊 狀態說明

| 圖示 | 狀態 | 說明 |
|------|------|------|
| ⏳ | 規劃中 | Milestone 已建立，尚未開始開發 |
| 🚧 | 進行中 | 部分 US 已進入開發階段 |
| ✅ | 已完成 | 所有 US 已完成並通過驗收 |
| 🔘 | 尚未規劃 | 尚未建立 Milestone 檔案 |

---

## 🎯 Milestone 詳細內容

### M01 — 基礎繪圖與 API 格式 ✅

**目標**：建立圖表資料查詢 API 與後端基礎能力

**包含的 User Stories**：
- US A-1: K 線與成交量基礎繪圖（Backend API）
- US G-2: API Response 固定格式設計

**完成日期**：2026-02-04

**交付產物**：
- Backend API (`GET /api/chart/daily`)
- 資料模型定義（ChartDataPoint, ChartResponse, ChartMetadata, ErrorResponse）
- 錯誤碼規範（6 項標準錯誤碼）
- 日 K 線聚合演算法
- 61 個測試案例（覆蓋率 89%）

---

### M02 — 前端圖表互動功能 ✅

**目標**：實作 Vue 3 前端，提供完整的圖表互動能力

**包含的 User Stories**：
- US A-2: 圖表互動操作（Zoom/Pan/Crosshair）
- US A-3: 小圖點擊放大檢視
- US A-4: 圖表載入狀態與錯誤處理

**完成日期**：2026-02-09

**交付產物**：
- Vue 3 + TypeScript + Vite 7.3.1 前端專案
- Electron 33 桶面應用框架
- TradingView Lightweight Charts 5.1.0 整合（K線圖 + 成交量副圖）
- 圖表互動操作（縮放、平移、十字線）
- Grid 多圖模式 + 小圖點擊放大
- Loading / Error 狀態元件

---

### M03 — Strategy Grid 核心 🧩 執行中

**目標**：實作批次條件查詢與 Grid 多圖並列顯示核心能力

**包含的 User Stories**：
- US B-1: 結構化條件查詢
- US B-2: Grid 多圖並列顯示
- US B-3: 事件日置中對齊
- US B-4: 查詢結果數量限制與分頁

**依賴**：M01 + M02（基礎圖表能力）

**Milestone 檔案**：[M03-strategy-grid.md](M03-strategy-grid.md)

**Tech Debt（建議納入）**：TD-001（MSSQL 整合測試）、TD-002（Playwright E2E）

---

### M04 — 事件研究統計（規劃中）🔘

**建議包含的 User Stories**：
- US D-1: 事件後報酬計算
- US D-2: 績效指標彙總統計
- US D-3: 側邊績效面板顯示
- US D-4: 績效明細表檢視
- US D-5: 績效統計更新機制
- US E-1: Excel 報表匯出
- US G-1: 查詢結果快取機制

**依賴**：M02（Strategy Grid 與 Time Window）

**建立指令**：
```
/flowkit.BDD-Milestone --milestone Group-D,Group-E,US-G-1
```

---

### M04 — AI 協作增強（規劃中）🔘

**建議包含的 User Stories**：
- US F-1: 自然語言轉 SQL 查詢
- US F-2: AI 生成 SQL 驗證與修正

**依賴**：M02（需有查詢執行機制）

**建立指令**：
```
/flowkit.BDD-Milestone --milestone Group-F
```

---

## 📈 進度追蹤

### 整體進度

```
[████░░░░░░░░░░░░░░░░] 5/22 US 已完成 (23%)，4 US M03 執行中
```

### 依狀態分佈

| 狀態 | US 數量 | 百分比 |
|------|---------|--------|
| ✅ 已完成 | 5 | 23% |
| 🧩 執行中 | 4 | 18% |
| ⏳ 已規劃 | 0 | 0% |
| 🔘 尚未規劃 | 13 | 59% |

---

## 🗓️ 時程建議

| Milestone | 預估工期 | 累積工期 |
|-----------|----------|----------|
| M01 | 2 週 | 2 週 |
| M02 | 3 週 | 5 週 |
| M03 | 3 週 | 8 週 |
| M04 | 1 週 | 9 週 |

**總預估工期**：約 9 週（約 2 個月）

> ⚠️ 以上為粗估，實際工期需視團隊規模與經驗調整。

---

## 🔗 相關文件

- [PRD 原始文件](../PRD-ASSRP.md)
- [User Story 索引](../user-stories/README.md)
- [System Spec](../../../specs/system/spec.md)

---

## 📝 使用說明

### 如何規劃下一個 Milestone

#### 方式一：自動規劃
```
/flowkit.BDD-Milestone --milestone
```
AI 將自動分析尚未規劃的 US，產生適合的 Milestone。

#### 方式二：手動指定 US
```
/flowkit.BDD-Milestone --milestone US-B-1,US-B-2,US-C-1
```
將指定的 US 拆分至新 Milestone。

#### 方式三：整組規劃
```
/flowkit.BDD-Milestone --milestone Group-B,Group-C
```
將 Group B 與 Group C 整組規劃成 Milestone。

---

## 變更記錄

| 日期 | 變更類型 | 說明 |
|------|----------|------|
| 2026-02-03 | 初始建立 | 建立 Milestone 索引，規劃 M01 |
| 2026-02-25 | 狀態更新 | M02 前端圖表互動功能完成，更新 US A-2/A-3/A-4 狀態，進度統計更新 |
| 2026-02-26 | M03 建立 | 建立 M03 Strategy Grid 核心，包含 US B-1/B-2/B-3/B-4，納入 TD-001/TD-002 Tech Debt 建議 |

---

**文件版本**：v1.0.0  
**維護者**：FlowKit BDD-Milestone Builder
