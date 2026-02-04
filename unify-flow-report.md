# Unify Flow 統合摘要

## Feature 資訊
- **Feature 名稱**：001-basic-chart-api
- **分支**：1-basic-chart-api
- **版本號**：v0.2.0
- **執行日期**：2026-02-04

---

## 變更摘要

本次統合將 **Feature 001-basic-chart-api** 的規格與設計合併至 System 層，建立系統的核心圖表功能基礎。

**核心變更**：
1. 新增 2 個 System-level User Stories（US-SYS-1, US-SYS-2）
2. 定義 4 個核心資料模型（ChartDataPoint, ChartResponse, ChartMetadata, ErrorResponse）
3. 建立 API 錯誤碼規範（6 項錯誤碼）
4. 定義日 K 線聚合演算法與驗證規則
5. 建立圖表資料查詢 API 契約（GET /api/chart/daily）

---

## 更新的文件

| 文件 | 更新類型 | 說明 |
|------|----------|------|
| `specs/system/spec.md` | 合併 | 新增 US-SYS-1（K線查詢）、US-SYS-2（API格式）<br>新增錯誤碼規範、日期驗證規則<br>定義日K聚合演算法<br>版本：0.1.0 → 0.2.0 |
| `specs/system/data-model.md` | 更新 | 新增 4 個核心模型、1 個列舉（ErrorCode）<br>新增關聯圖<br>版本：0.1.0 → 0.2.0 |
| `specs/system/contracts/chart-api.md` | 新增 | 完整的圖表資料查詢 API 契約 |
| `specs/history/001-basic-chart-api/` | 封存 | Feature 目錄完整移動至 history |

---

## 重大行為變更

### 新增行為

#### 1. 日 K 線聚合演算法（Section 3.2）
- 從 1 分 K 線聚合為日 K 線
- 演算法：開盤取首筆、最高取最大、最低取最小、收盤取末筆、成交量加總
- 實作位置：`src/services/chart_service.py::_aggregate_to_daily()`

#### 2. API 錯誤碼規範（Section 5.1）
- 定義 6 項標準錯誤碼：
  - `INVALID_STOCK_CODE` (400)
  - `INVALID_DATE_RANGE` (400)
  - `INVALID_DATE_FORMAT` (400)
  - `NO_DATA` (200，非錯誤狀態)
  - `DATABASE_ERROR` (500)
  - `INTERNAL_ERROR` (500)

#### 3. 日期範圍驗證（Section 3.3）
- 必須為 ISO 8601 格式（YYYY-MM-DD）
- `start_date` ≤ `end_date`
- 不接受未來日期

---

## 資料模型變更

### 新增模型

| 模型名稱 | 用途 | 欄位數 |
|----------|------|--------|
| `ChartDataPoint` | 單一時間點的 OHLCV 資料 | 6 |
| `ChartResponse` | API 回應格式 | 3 |
| `ChartMetadata` | 查詢結果元資料 | 4 |
| `ErrorResponse` | 統一錯誤格式 | 3 |

### 新增列舉

| 列舉名稱 | 用途 | 值數量 |
|----------|------|--------|
| `ErrorCode` | 標準錯誤碼 | 6 |

---

## API 契約變更

### 新增 Endpoint

| Endpoint | Method | 用途 |
|----------|--------|------|
| `/api/chart/daily` | GET | 查詢日 K 線圖表資料 |

**Query Parameters**：
- `stock_code`: string (必填，4 位數字)
- `start_date`: date (必填，ISO 8601 格式)
- `end_date`: date (必填，ISO 8601 格式)

**Response**：
- 成功：HTTP 200，`ChartResponse` 格式
- 失敗：HTTP 4xx/5xx，`ErrorResponse` 格式

---

## 驗證結果

### Phase 5 合併操作驗證 ✅

#### Feature 內容整合驗證
- ✅ US A-1 → US-SYS-1（3 AC 完整整合）
- ✅ US G-2 → US-SYS-2（5 AC 完整整合）
- ✅ 錯誤碼規範完整移植（6 項）

#### 合併區段完整性
- ✅ 無重複內容
- ✅ 無遺漏項目
- ✅ 無結構破壞

#### Design 同步驗證
- ✅ data-model.md 已同步（4 模型 + 1 列舉）
- ✅ contracts/chart-api.md 已同步
- ⏭️ flows.md 未涉及（無流程變更）

#### 殘留檢查
- ✅ 無 Feature 名稱殘留
- ✅ 無實作細節洩漏
- ✅ 無未處理的 Change Set

**總計**：✅ 全部通過

---

## Escalation Log（深讀記錄）

| 階段 | 目標位置 | 深讀原因 | 讀取範圍 |
|------|----------|----------|----------|
| Phase 1 | feature/spec.md:L90-220 | User Story 抽取 | 131 lines |
| Phase 2 | system/spec.md:L1-100 | 定位合併區段 | 100 lines |
| Phase 3 | system/data-model.md:L1-50 | 確認模型狀態 | 50 lines |

**總深讀次數**：3  
**最小 Context 完成率**：100%（在 Stage 1 即完成所有必要定位）

---

## Git 提交記錄

| Commit | 說明 | Files Changed |
|--------|------|---------------|
| 74f54ea | docs: 合併 Feature Spec 至 System Spec [001-basic-chart-api] | specs/system/spec.md |
| 7261638 | docs: 更新 System Design [001-basic-chart-api] | specs/system/data-model.md<br>specs/system/contracts/chart-api.md |
| ccc3acf | chore: 封存 Feature [001-basic-chart-api] 至 history | specs/history/001-basic-chart-api/* |

---

## 下一步

### 1. 檢視統合摘要 ✅
- 本文件即為統合摘要

### 2. 提交 PR
```bash
# 建立 PR（手動操作）
gh pr create --base main --head 1-basic-chart-api \
  --title "feat: 實作 K 線圖表基礎功能與 API 格式規範" \
  --body-file unify-flow-report.md
```

### 3. PR 檢查清單
- [ ] 確認所有測試通過（61 tests, 89% coverage）
- [ ] 確認 System Spec 變更正確（US-SYS-1, US-SYS-2）
- [ ] 確認 Data Model 變更正確（4 模型 + 1 列舉）
- [ ] 確認 API 契約文件完整
- [ ] 確認 Feature 已封存至 history
- [ ] Code Review（建議至少 1 位 Reviewer）

### 4. 合併至 main
```bash
# 等待 PR 審核通過後
gh pr merge --squash
```

### 5. 後續 Feature 開發
- ✅ M01 基礎圖表功能（已完成 Backend）
- ⏭️ M02 前端互動功能（US A-2, A-3, A-4）
- ⏭️ M03 策略網格視圖
- ⏭️ M04 時間窗格功能

---

## 附錄：Unify Flow 遵從性檢查

### Progressive Disclosure Protocol 遵從性 ✅

| 原則 | 遵從狀態 | 說明 |
|------|----------|------|
| 資料不足即停止 | ✅ | Phase 0 Gatekeeper 完整執行 |
| 先低解析度掃描 | ✅ | Phase 1/2 Stage 1 僅讀取結構 |
| 針對性深讀 | ✅ | 僅對 3 個候選區段執行深讀 |
| 記錄深讀原因 | ✅ | Escalation Log 完整記錄 |
| 無預防性擴讀 | ✅ | 無超出必要範圍的讀取 |
| 無猜測行為 | ✅ | 所有內容來自 Feature Spec |

### Constitution 遵從性 ✅

| 條款 | 遵從狀態 | 說明 |
|------|----------|------|
| §6.2 Feature 合併限制 | ✅ | 透過 Unify Flow 合併 |
| §3 System Spec 保護 | ✅ | 僅在 Unify Flow 中修改 |
| §5 Test-First | ✅ | Feature 已有 61 tests |
| §9 Observability | ✅ | 完整 logging 輸出 |

---

**報告產生時間**：2026-02-04  
**Unify Flow 版本**：FlowKit v1.0  
**執行狀態**：✅ 成功完成
