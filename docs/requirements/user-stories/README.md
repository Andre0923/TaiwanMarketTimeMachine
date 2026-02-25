# User Story Index

> **專案名稱**：AI-Assisted Stock Strategy Research Platform（ASSRP）  
> **核心定位**：視覺化事件研究與型態標記平台  
> **建立日期**：2026-02-03  
> **最後更新**：2026-02-03

---

## 📋 目錄（Table of Contents）

### Group 索引

| Group | 名稱 | US 數量 | 檔案 |
|-------|------|---------|------|
| A | 基礎繪圖與互動 | 4 | [US-A-basic-chart.md](US-A-basic-chart.md) |
| B | Strategy Grid 模式 | 4 | [US-B-strategy-grid.md](US-B-strategy-grid.md) |
| C | Time Window Engine | 4 | [US-C-time-window.md](US-C-time-window.md) |
| D | Micro Backtest 統計 | 5 | [US-D-micro-backtest.md](US-D-micro-backtest.md) |
| E | 資料匯出功能 | 1 | [US-E-data-export.md](US-E-data-export.md) |
| F | AI 協作查詢 | 2 | [US-F-ai-collaboration.md](US-F-ai-collaboration.md) |
| G | 效能與快取機制 | 2 | [US-G-performance.md](US-G-performance.md) |

**總計**：7 個 Group，22 個 User Stories

---

### User Story 索引

| US ID | 摘要 | Group | 狀態 |
|-------|------|-------|------|
| US A-1 | K 線與成交量基礎繪圖 | A | ✅ M01 已完成 |
| US A-2 | 圖表互動操作（Zoom/Pan/Crosshair） | A | ✅ 已完成 |
| US A-3 | 小圖點擊放大檢視 | A | ✅ 已完成 |
| US A-4 | 圖表載入狀態與錯誤處理 | A | ✅ 已完成 |
| US B-1 | 結構化條件查詢 | B | ⏳ 尚未規劃 |
| US B-2 | Grid 多圖並列顯示 | B | ⏳ 尚未規劃 |
| US B-3 | 事件日置中對齊 | B | ⏳ 尚未規劃 |
| US B-4 | 查詢結果數量限制與分頁 | B | ⏳ 尚未規劃 |
| US C-1 | 時間窗口參數設定 | C | ⏳ 尚未規劃 |
| US C-2 | 全 Grid 窗口一致化渲染 | C | ⏳ 尚未規劃 |
| US C-3 | 事件日標記線顯示 | C | ⏳ 尚未規劃 |
| US C-4 | 預設窗口快速切換 | C | ⏳ 尚未規劃 |
| US D-1 | 事件後報酬計算 | D | ⏳ 尚未規劃 |
| US D-2 | 績效指標彙總統計 | D | ⏳ 尚未規劃 |
| US D-3 | 側邊績效面板顯示 | D | ⏳ 尚未規劃 |
| US D-4 | 績效明細表檢視 | D | ⏳ 尚未規劃 |
| US D-5 | 績效統計更新機制 | D | ⏳ 尚未規劃 |
| US E-1 | Excel 報表匯出 | E | ⏳ 尚未規劃 |
| US F-1 | 自然語言轉 SQL 查詢 | F | ⏳ 尚未規劃 |
| US F-2 | AI 生成 SQL 驗證與修正 | F | ⏳ 尚未規劃 |
| US G-1 | 查詢結果快取機制 | G | ⏳ 尚未規劃 |
| US G-2 | API Response 固定格式設計 | G | ✅ 已完成 |

---

## 📊 狀態快照（Status Snapshot）

> **更新時間**：2026-02-25

### 狀態統計

| 狀態 | 圖示 | 數量 | 百分比 |
|------|------|------|--------|
| 尚未規劃 | ⏳ | 17 | 77% |
| Milestone 執行中 | 🧩 | 0 | 0% |
| 部分完成 | 🔶 | 0 | 0% |
| 已完成 | ✅ | 5 | 23% |

---

### 依狀態分類

#### ✅ 已完成（5 個）

**Group A — 基礎繪圖與互動**
- US A-1（K 線與成交量基礎繪圖 - Backend）（Milestone M01）
- US A-2（圖表互動操作）（Milestone M02）
- US A-3（小圖點擊放大檢視）（Milestone M02）
- US A-4（圖表載入狀態與錯誤處理）（Milestone M02）

**Group G — 效能與快取機制**（Milestone M01）
- US G-2（API Response 格式設計）

---

#### 🧩 Milestone 執行中（0 個）

（無）

#### ⏳ 尚未規劃（17 個）

**Group B — Strategy Grid 模式**
- US B-1, US B-2, US B-3, US B-4

**Group C — Time Window Engine**
- US C-1, US C-2, US C-3, US C-4

**Group D — Micro Backtest 統計**
- US D-1, US D-2, US D-3, US D-4, US D-5

**Group E — 資料匯出功能**
- US E-1

**Group F — AI 協作查詢**
- US F-1, US F-2

**Group G — 效能與快取機制**
- US G-1

---

## 🎯 Milestone 追蹤

### 已完成的 Milestone

**[M01 — 基礎繪圖與 API 格式](../Milestone/M01-basic-chart-and-api.md)** ✅ 已完成
- 包含：US A-1, G-2
- 完成日期：2026-02-04
- 交付：Backend API + 資料模型 + 錯誤碼規範 + 61 個測試（89% 覆蓋率）

### 進行中的 Milestone

**[M02 — 前端圖表互動功能](../Milestone/M02-frontend-chart-interactions.md)** ✅ 已完成
- 包含：US A-2, A-3, A-4
- 完成日期：2026-02-09
- 交付：Vue 3 + Electron 前端應用 + TradingView Lightweight Charts 5.1 整合

### 規劃建議

建議依以下順序規劃 Milestone：

1. ✅ **M01 — 基礎繪圖與 API 格式**（已完成）
2. ✅ **M02 — 前端圖表互動功能**（已完成）
3. **M03 — Strategy Grid 核心**（Group B + C）
4. **M04 — 事件研究統計**（Group D + E + US G-1）
5. **M05 — AI 協作增強**（Group F）

---

## 📝 使用說明

### 如何開始下一步

#### 方式一：自動規劃 Milestone
```
執行 FlowKit BDD-Milestone --milestone
```
AI 將自動分析尚未規劃的 US，產生適合的 Milestone。

#### 方式二：手動指定 US
```
執行 FlowKit BDD-Milestone --milestone US-A-1,US-A-2,US-G-2
```
將指定的 US 拆分至新 Milestone。

#### 方式三：整組規劃
```
執行 FlowKit BDD-Milestone --milestone Group-A
```
將 Group A 整組規劃成 Milestone。

---

## 🔗 相關文件

- [PRD 原始文件](../PRD-ASSRP.md)
- [Milestone 目錄](../Milestone/)
- [System Spec](../../specs/system/spec.md)

---

**文件版本**：v1.0.0  
**維護者**：FlowKit BDD-Milestone Builder
