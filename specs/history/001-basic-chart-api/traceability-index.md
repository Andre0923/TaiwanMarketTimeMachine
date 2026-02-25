# Traceability Index: 001-basic-chart-api

> **Generated**: 2026-02-25  
> **Feature**: 001-basic-chart-api  
> **Spec Reference**: [spec.md](./spec.md)  
> **Status**: Archived（封存）

---

## Summary

| 指標 | 數值 |
|------|------|
| User Stories | 5（US A-1, US A-2, US A-3, US A-4, US G-2） |
| Acceptance Criteria | 17 |
| 程式碼檔案（後端） | 6 |
| 測試檔案（後端） | 6 |
| US 覆蓋率 | 40%（2/5，US A-2/A-3/A-4 延後至 Feature 002） |
| AC 覆蓋率（已實作 US） | 100%（8/8，含 tests） |

> ⚠️ US A-2、US A-3、US A-4 的前端實作延後至 Feature 002-frontend-chart-interactions。

---

## User Story A-1: K 線與成交量基礎繪圖

**Spec Reference**: [spec.md#user-story-a-1](./spec.md)

### 程式碼對應

| 類型 | 檔案 | @spec-ac | 任務 ID |
|------|------|----------|---------|
| Infrastructure | [src/main.py](../../src/main.py#L1) | — | T005 |
| Database | [src/db/connection.py](../../src/db/connection.py#L1) | — | T004 |
| Repository | [src/db/stock_repository.py](../../src/db/stock_repository.py#L1) | AC1, AC2, AC3 | T006 |
| Model | [src/models/chart.py](../../src/models/chart.py#L1) | AC1, AC2, AC3 | T007 |
| Service | [src/services/chart_service.py](../../src/services/chart_service.py#L1) | AC1, AC2, AC3 | T008 |
| API | [src/api/routes/chart.py](../../src/api/routes/chart.py#L1) | AC1, AC2, AC3 | T009 |

### AC 覆蓋

| AC ID | 描述 | 測試檔案 | 狀態 |
|-------|------|----------|------|
| AC1 | K 線正確顯示 | [tests/integration/test_chart_api.py](../../tests/integration/test_chart_api.py) | ✅ |
| AC2 | 成交量副圖對齊 | [tests/integration/test_chart_api.py](../../tests/integration/test_chart_api.py) | ✅ |
| AC3 | 無資料時的處理 | [tests/unit/test_chart_service.py](../../tests/unit/test_chart_service.py) | ✅ |

---

## User Story A-2: 圖表互動操作（Zoom/Pan/Crosshair）

**Spec Reference**: [spec.md#user-story-a-2](./spec.md)

> ⚠️ **延後至 Feature 002**：本 US 的前端實作在 [002-frontend-chart-interactions](../002-frontend-chart-interactions/traceability-index.md) 完成。

| AC ID | 描述 | 狀態 |
|-------|------|------|
| AC1 | 滑鼠滾輪縮放 | ↗️ 見 Feature 002 |
| AC2 | 拖曳平移 | ↗️ 見 Feature 002 |
| AC3 | 十字線資料顯示 | ↗️ 見 Feature 002 |

---

## User Story A-3: 小圖點擊放大檢視

**Spec Reference**: [spec.md#user-story-a-3](./spec.md)

> ⚠️ **延後至 Feature 002**：本 US 的前端實作在 [002-frontend-chart-interactions](../002-frontend-chart-interactions/traceability-index.md) 完成。

| AC ID | 描述 | 狀態 |
|-------|------|------|
| AC1 | 小圖點擊事件 | ↗️ 見 Feature 002 |
| AC2 | 放大後互動保留 | ↗️ 見 Feature 002 |
| AC3 | 返回 Grid 檢視 | ↗️ 見 Feature 002 |

---

## User Story A-4: 圖表載入狀態與錯誤處理

**Spec Reference**: [spec.md#user-story-a-4](./spec.md)

> ⚠️ **延後至 Feature 002**：本 US 的前端實作在 [002-frontend-chart-interactions](../002-frontend-chart-interactions/traceability-index.md) 完成。

| AC ID | 描述 | 狀態 |
|-------|------|------|
| AC1 | 載入中狀態 | ↗️ 見 Feature 002 |
| AC2 | 載入錯誤提示 | ↗️ 見 Feature 002 |
| AC3 | 部分圖表失敗不影響整體 | ↗️ 見 Feature 002 |

---

## User Story G-2: API Response 固定格式設計

**Spec Reference**: [spec.md#user-story-g-2](./spec.md)

### 程式碼對應

| 類型 | 檔案 | @spec-ac | 任務 ID |
|------|------|----------|---------|
| Model | [src/models/chart.py](../../src/models/chart.py#L1) | AC1, AC2, AC3 | T021 |
| API | [src/api/routes/chart.py](../../src/api/routes/chart.py#L1) | AC1, AC2, AC3 | T021 |
| Contract Doc | [specs/history/001-basic-chart-api/contracts/](./contracts/) | AC1, AC4 | T022 |

### AC 覆蓋

| AC ID | 描述 | 測試檔案 | 狀態 |
|-------|------|----------|------|
| AC1 | Response 必要欄位 | [tests/integration/test_api_contract.py](../../tests/integration/test_api_contract.py) | ✅ |
| AC2 | 擴充性設計 | —（架構設計文件） | ✅ |
| AC3 | 錯誤格式一致性 | [tests/integration/test_api_contract.py](../../tests/integration/test_api_contract.py) | ✅ |
| AC4 | Response 範例文件 | [specs/history/001-basic-chart-api/contracts/chart-api.md](./contracts/chart-api.md) | ✅ |
| AC5 | 向下相容性承諾 | —（架構設計文件） | ✅ |

---

## Issues

| 嚴重性 | 問題 | 說明 |
|--------|------|------|
| LOW | `tests/*` 無 @spec 註解 | 測試檔案缺少 @spec 標記，建議後續補充 |
| LOW | `src/main.py` 無 US 層級 @spec | 僅有 Feature 層級標記，無法對應至具體 User Story |

---

## 維護說明

- 本檔案由 `/flowkit.trace` 自動產生
- US A-2、A-3、A-4 前端實作請參考 [Feature 002 Traceability Index](../002-frontend-chart-interactions/traceability-index.md)
- Unify Flow 已完成，本 Feature 已封存至 `specs/history/001-basic-chart-api/`
