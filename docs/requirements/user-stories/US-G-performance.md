# Group G — 效能與快取機制

> **群組目標**：確保系統效能與可擴展性  
> **技術範疇**：查詢結果快取、API 格式設計  
> **依賴關係**：跨所有功能群組

---

## 概述

本群組實現「保險絲設計」，確保系統能夠：
- 避免重複計算相同查詢的結果
- 提供穩定的 API 格式,支援未來擴充
- 在高頻使用下維持效能

這是系統穩定性的基礎建設。

---

## User Stories

### US G-1: 查詢結果快取機制

**As a** 系統  
**I want** 快取重複查詢的結果  
**So that** 相同條件的查詢不需要重複計算,提升回應速度

#### Acceptance Criteria

**AC1 — 快取鍵值設計**
- **Given** 使用者執行一次查詢
- **When** 系統產生查詢結果
- **Then** 應計算快取鍵值 `hash(SQL + pre_days + post_days + horizons)` 並儲存結果

**AC2 — 快取命中判斷**
- **Given** 使用者執行查詢
- **When** 系統檢查快取
- **Then** 若快取鍵值存在且未過期，應直接回傳快取結果而非重新計算

**AC3 — 快取過期機制**
- **Given** 快取結果已儲存
- **When** 儲存時間超過 24 小時
- **Then** 該快取應失效，下次查詢需重新計算

**AC4 — 快取儲存位置**
- **Given** 系統設計快取機制
- **When** 選擇儲存方式
- **Then** 應使用資料庫表 `event_study_result_cache`（包含：cache_key, result_json, created_at）

**AC5 — 快取容量管理**
- **Given** 快取表逐漸累積大量資料
- **When** 表大小超過設定閾值（如 10GB）
- **Then** 應自動刪除最舊的快取記錄

**AC6 — 快取效能驗證**
- **Given** 相同查詢第二次執行
- **When** 系統從快取回傳結果
- **Then** 回應時間應 < 1 秒（相較於首次計算的 5-10 秒）

---

### US G-2: API Response 固定格式設計

**As a** 系統架構師  
**I want** API Response 有穩定的格式  
**So that** 未來新增功能時不需要修改前端解析邏輯

#### Acceptance Criteria

**AC1 — Response 必要欄位**
- **Given** 任何查詢 API 的回應
- **When** 前端接收 response
- **Then** 必須包含：`event_window` (pre/post), `horizons` (觀察期), `samples` (樣本清單), `metrics` (統計指標)

**AC2 — 擴充性設計**
- **Given** 未來需要新增統計指標（如 Sharpe Ratio）
- **When** 修改後端邏輯
- **Then** 只需在 `metrics` 物件內新增欄位，不影響既有欄位

**AC3 — 錯誤格式一致性**
- **Given** API 請求失敗（如 SQL 錯誤、逾時）
- **When** 系統回傳錯誤
- **Then** 應使用統一格式：`{ "error": { "code": "...", "message": "..." } }`

**AC4 — Response 範例文件**
- **Given** 開發者需要串接 API
- **When** 查閱 API 文件
- **Then** 應提供完整的 Response 範例（JSON）與欄位說明

**AC5 — 向下相容性承諾**
- **Given** 系統升級至新版本
- **When** API 新增功能
- **Then** 既有欄位的資料型別與語意不得改變（向下相容）

---

## 技術備註

- **快取實作**：使用 SQL Server 資料表 + TTL 機制
- **快取鍵值**：使用 `hashlib.sha256` 計算
- **API 格式**：使用 Pydantic Models 定義 Response Schema
- **監控**：記錄快取命中率（Cache Hit Rate）

---

## 依賴關係

- **被依賴於**：所有功能群組（基礎建設）
- **依賴於**：無（獨立基礎設施）
