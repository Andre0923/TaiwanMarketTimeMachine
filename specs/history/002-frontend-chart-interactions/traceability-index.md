# Traceability Index: 002-frontend-chart-interactions

> **Generated**: 2026-02-25  
> **Feature**: 002-frontend-chart-interactions  
> **Spec Reference**: [spec.md](./spec.md)  
> **Status**: Archived（封存）

---

## Summary

| 指標 | 數值 |
|------|------|
| User Stories | 3（US A-2, US A-3, US A-4） |
| Acceptance Criteria | 9 |
| 程式碼檔案（前端） | 8 |
| 測試檔案（前端） | 7 |
| US 覆蓋率 | 100%（3/3） |
| AC 覆蓋率 | 100%（9/9） |
| 測試通過率 | 100%（54/54 tests） |

> ℹ️ 本 Feature 為事後補記（retrospective），前端程式碼檔案未包含 @spec 標記。

---

## User Story A-2: 圖表互動操作（Zoom/Pan/Crosshair）

**Spec Reference**: [spec.md#user-story-a-2](./spec.md)  
**Predecessor**: [001-basic-chart-api](../001-basic-chart-api/traceability-index.md)

### 程式碼對應

| 類型 | 檔案 | 任務 ID |
|------|------|---------|
| Type Def | [frontend/src/types/chart.ts](../../frontend/src/types/chart.ts) | T005 |
| Composable | [frontend/src/composables/useChartInteraction.ts](../../frontend/src/composables/useChartInteraction.ts) | T010 |
| Composable | [frontend/src/composables/useChartData.ts](../../frontend/src/composables/useChartData.ts) | T008 |
| Component | [frontend/src/components/ChartWidget.vue](../../frontend/src/components/ChartWidget.vue) | T016 |

### AC 覆蓋

| AC ID | 描述 | 測試檔案 | 狀態 |
|-------|------|----------|------|
| AC1 | 滑鼠滾輪縮放 | [frontend/src/composables/useChartInteraction.test.ts](../../frontend/src/composables/useChartInteraction.test.ts) | ✅ |
| AC2 | 拖曳平移 | [frontend/src/composables/useChartInteraction.test.ts](../../frontend/src/composables/useChartInteraction.test.ts) | ✅ |
| AC3 | 十字線資料顯示 | [frontend/src/composables/useChartInteraction.test.ts](../../frontend/src/composables/useChartInteraction.test.ts) | ✅ |

---

## User Story A-3: 小圖點擊放大檢視

**Spec Reference**: [spec.md#user-story-a-3](./spec.md)  
**Predecessor**: [001-basic-chart-api](../001-basic-chart-api/traceability-index.md)

### 程式碼對應

| 類型 | 檔案 | 任務 ID |
|------|------|---------|
| Component | [frontend/src/components/ChartGrid.vue](../../frontend/src/components/ChartGrid.vue) | T018 |
| Component | [frontend/src/components/ChartWidget.vue](../../frontend/src/components/ChartWidget.vue) | T016 |

### AC 覆蓋

| AC ID | 描述 | 測試檔案 | 狀態 |
|-------|------|----------|------|
| AC1 | 小圖點擊事件 | [frontend/src/components/ChartGrid.test.ts](../../frontend/src/components/ChartGrid.test.ts) | ✅ |
| AC2 | 放大後互動保留 | [frontend/src/components/ChartWidget.test.ts](../../frontend/src/components/ChartWidget.test.ts) | ✅ |
| AC3 | 返回 Grid 檢視 | [frontend/src/components/ChartGrid.test.ts](../../frontend/src/components/ChartGrid.test.ts) | ✅ |

---

## User Story A-4: 圖表載入狀態與錯誤處理

**Spec Reference**: [spec.md#user-story-a-4](./spec.md)  
**Predecessor**: [001-basic-chart-api](../001-basic-chart-api/traceability-index.md)

### 程式碼對應

| 類型 | 檔案 | 任務 ID |
|------|------|---------|
| Service | [frontend/src/services/chartApi.ts](../../frontend/src/services/chartApi.ts) | T006 |
| Composable | [frontend/src/composables/useChartData.ts](../../frontend/src/composables/useChartData.ts) | T008 |
| Component | [frontend/src/components/ChartLoading.vue](../../frontend/src/components/ChartLoading.vue) | T012 |
| Component | [frontend/src/components/ChartError.vue](../../frontend/src/components/ChartError.vue) | T014 |
| Component | [frontend/src/components/ChartWidget.vue](../../frontend/src/components/ChartWidget.vue) | T016 |

### AC 覆蓋

| AC ID | 描述 | 測試檔案 | 狀態 |
|-------|------|----------|------|
| AC1 | 載入中狀態 | [frontend/src/components/ChartLoading.test.ts](../../frontend/src/components/ChartLoading.test.ts) | ✅ |
| AC2 | 載入錯誤提示 | [frontend/src/components/ChartError.test.ts](../../frontend/src/components/ChartError.test.ts) | ✅ |
| AC3 | 部分圖表失敗不影響整體 | [frontend/src/components/ChartWidget.test.ts](../../frontend/src/components/ChartWidget.test.ts) | ✅ |

---

## Issues

| 嚴重性 | 問題 | 說明 |
|--------|------|------|
| LOW | 前端程式碼無 @spec 標記 | 因事後補記，前端檔案缺少 @spec 標記，建議在後續 Feature 補充規範 |
| LOW | 無 E2E 測試 | Playwright E2E 測試未實作，目前僅有 Vitest 單元測試 |

---

## 維護說明

- 本檔案由 `/flowkit.trace` 自動產生
- 本 Feature 為事後補記流程（retrospective），tasks.md 為反向產生
- 所有測試通過率 100%（54/54 tests，含 7 個測試檔）
- Unify Flow 已完成，本 Feature 已封存至 `specs/history/002-frontend-chart-interactions/`
