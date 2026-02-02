# 規格-程式碼可追溯性（Traceability）功能規劃提案

> **提案日期**：2026-01-23  
> **實作完成日期**：2026-01-25  
> **狀態**：✅ 已實作  
> **相關功能**：一致性檢查（已完成）

---

## 1. 需求背景

### 1.1 用戶需求

1. **主要目的**：SDD 開發中，規格是真相。希望規格與程式碼之間有連結（索引）
2. **使用情境**：
   - AI 檢視時能快速找到 User Story 對應的程式碼/測試
   - 人類需要檢視時能容易找到對應關係

### 1.2 現有基礎

目前 `tasks.md` 已有 `[US1]`, `[US2]` 等 User Story 標籤：

```markdown
- [ ] T012 [P] [US1] Create User model in src/models/user.py
- [ ] T014 [US1] Implement UserService in src/services/user_service.py
```

**機會**：利用現有標籤系統，自動建立可追溯性索引。

---

## 2. 功能設計

### 2.1 核心機制

```
┌─────────────────────────────────────────────────────────────────┐
│  1. tasks.md 已有 [US1], [US2] 標籤                              │
│                    │                                            │
│                    ▼                                            │
│  2. implement 時，在程式碼檔案加入標準化註解                      │
│     # @spec US1 (001-feature/spec.md#user-story-1)              │
│                    │                                            │
│                    ▼                                            │
│  3. implement 完成後，自動產生 traceability-index.md            │
│     User Story → 程式碼檔案 → 測試檔案                           │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 索引格式設計

#### Feature 層索引（specs/features/NNN-feature/traceability-index.md）

```markdown
# Traceability Index: [Feature Name]

> **Generated**: [timestamp]  
> **Feature**: 001-user-management  
> **Spec**: [spec.md](./spec.md)

---

## User Story 1: 使用者註冊

**Spec Reference**: [spec.md#user-story-1](./spec.md#user-story-1)

| 類型 | 檔案 | 說明 | 任務 ID |
|------|------|------|---------|
| Model | [src/models/user.py](../../src/models/user.py#L10) | User entity | T012 |
| Service | [src/services/user_service.py](../../src/services/user_service.py#L1) | User CRUD | T014 |
| API | [src/api/users.py](../../src/api/users.py#L1) | REST endpoints | T018 |
| Test | [tests/test_user.py](../../tests/test_user.py#L1) | Unit tests | T013 |

**AC Coverage**:
| AC ID | 描述 | 測試檔案 | 狀態 |
|-------|------|----------|------|
| AC1.1 | 使用者可輸入 email | tests/test_user.py#L20 | ✅ |
| AC1.2 | 密碼需加密儲存 | tests/test_user.py#L45 | ✅ |

---

## User Story 2: 使用者登入

**Spec Reference**: [spec.md#user-story-2](./spec.md#user-story-2)

| 類型 | 檔案 | 說明 | 任務 ID |
|------|------|------|---------|
| Service | [src/services/auth_service.py](../../src/services/auth_service.py#L1) | Auth logic | T020 |
| Middleware | [src/middleware/auth.py](../../src/middleware/auth.py#L1) | JWT validation | T021 |
| Test | [tests/test_auth.py](../../tests/test_auth.py#L1) | Auth tests | T019 |

---

## Summary

| 指標 | 數值 |
|------|------|
| User Stories | 2 |
| 程式碼檔案 | 6 |
| 測試檔案 | 2 |
| AC 覆蓋率 | 100% |
```

### 2.3 程式碼標記格式

#### 標準化 Spec Reference 註解

```python
# Python
# @spec US1 (001-feature/spec.md#user-story-1)
# @spec-ac AC1.1, AC1.2

class User:
    """User entity for user management feature."""
    pass
```

```typescript
// TypeScript/JavaScript
// @spec US1 (001-feature/spec.md#user-story-1)
// @spec-ac AC1.1, AC1.2

export class User {
  // ...
}
```

```rust
// Rust
// @spec US1 (001-feature/spec.md#user-story-1)
// @spec-ac AC1.1, AC1.2

pub struct User {
    // ...
}
```

---

## 3. 實現方案

### 3.1 方案比較

| 方案 | 優點 | 缺點 | 複雜度 |
|------|------|------|--------|
| **A. 修改 implement** | 自動化、無額外步驟 | 需修改核心指令 | 中 |
| **B. 新增獨立指令** | 不影響現有流程、可選執行 | 需額外呼叫 | 低 |
| **C. 整合到 pre-unify-check** | 合併前驗證 | 時機較晚 | 低 |

**採用方案**：**方案 A + B + C 組合**
- A：修改 `/speckit.implement`（建立檔案時自動加入 @spec 註解）
- B：新增 `/flowkit.trace` 指令（主動產生索引）← 注意：改名為 flowkit 而非 speckit
- C：在 `/flowkit.pre-unify-check` 中加入覆蓋率檢查
- **額外**：在 `/flowkit.unify-flow` 中加入 traceability-index 合併邏輯

### 3.2 需要修改/新增的檔案

| 檔案 | 動作 | 說明 | 狀態 |
|------|------|------|------|
| `flowkit.trace.agent.md` | **新增** | 產生 traceability-index.md | ✅ 完成 |
| `speckit.implement.agent.md` | **修改** | 建立檔案時加入 @spec 註解 | ✅ 完成 |
| `tasks-template.md` | **修改** | 強化 [US] 標籤說明 | ✅ 完成 |
| `traceability-index-template.md` | **新增** | 索引檔案模板 | ✅ 完成 |
| `flowkit.pre-unify-check.agent.md` | **修改** | 加入 Spec 覆蓋率檢查（TR1-TR3） | ✅ 完成 |
| `flowkit.unify-flow.prompt.md` | **修改** | 加入 traceability-index 合併邏輯 | ✅ 完成 |

> **注意**：原提案使用 `speckit.trace`，實際實作改名為 `flowkit.trace`，因為追溯功能屬於開發流程（FlowKit）而非規格定義（SpecKit）。

---

## 4. 詳細設計

### 4.1 /flowkit.trace 指令規格（已實作）

> **實際檔案位置**：`flowkit/agents/flowkit.trace.agent.md`

```markdown
# FlowKit Trace

> **用途**：產生規格-程式碼可追溯性索引
> **觸發時機**：implement 完成後（可選）、pre-unify-check 之前

## 執行步驟

### Phase 1：解析 tasks.md
- 抽取所有 [US*] 標籤和對應的檔案路徑
- 建立 User Story → Tasks → Files 對應表

### Phase 2：掃描程式碼
- 掃描 tasks.md 中列出的檔案
- 抽取 @spec 和 @spec-ac 註解
- 驗證註解與 tasks.md 一致

### Phase 3：掃描測試檔案
- 識別測試檔案（tests/, *_test.*, *.spec.*）
- 抽取測試與 AC 的對應關係

### Phase 4：產生索引
- 建立 traceability-index.md
- 計算覆蓋率統計

## 輸出
- FEATURE_DIR/traceability-index.md
- 覆蓋率報告（哪些 User Story/AC 沒有對應程式碼）
```

### 4.2 speckit.implement 修改

在 Step 7（Execute implementation）中加入：

```markdown
**Spec Reference 註解規則**：

當建立新檔案時，若該任務有 [US*] 標籤：
1. 在檔案開頭加入 @spec 註解
2. 格式：`# @spec US{N} ({FEATURE_DIR}/spec.md#user-story-{N})`
3. 若任務描述提及特定 AC，加入 `# @spec-ac AC{N}.{M}`

範例：
```python
# @spec US1 (001-user-management/spec.md#user-story-1)
# @spec-ac AC1.1, AC1.2
# Generated by SpecKit Implement

class User:
    ...
```
```

### 4.3 tasks-template.md 強化

```markdown
## Task Checklist Format Reference

每個任務 MUST 遵循以下格式：

```
- [ ] T001 [P] [US1] Description with file path
      │     │    │    │
      │     │    │    └── 明確的任務描述，包含檔案路徑
      │     │    └─────── User Story 標籤（Phase 3+ 必須）← 用於 Traceability
      │     └──────────── [P] 可平行標記（選用）
      └────────────────── 任務 ID（T001, T002...）
```

### User Story 標籤用途

[US*] 標籤除了組織任務外，還用於：
1. **可追溯性索引**：自動建立 Spec → Code 對應關係
2. **覆蓋率計算**：確保每個 User Story 都有實作
3. **Code Review**：快速定位與 Spec 相關的程式碼
```

### 4.4 pre-unify-check 整合

在 Phase 3（Spec-實作對齊檢查）中加入：

```markdown
#### 3.4 Traceability 驗證（條件觸發）

**觸發條件**：存在 traceability-index.md

| ID | 檢查項目 | 說明 |
|----|----------|------|
| TR1 | User Story 覆蓋率 | 每個 User Story 至少有一個對應檔案 |
| TR2 | AC 覆蓋率 | 每個 AC 至少有一個對應測試 |
| TR3 | @spec 註解一致性 | 程式碼中的 @spec 與 tasks.md 一致 |

**若 traceability-index.md 不存在**：
- 標記為 WARNING（非阻擋）
- 建議執行 `/speckit.trace`
```

---

## 5. 使用流程

### 5.1 完整流程（含 Traceability）

```
/speckit.specify → /speckit.plan → /flowkit.consistency-check
                                            │
                                           PASS
                                            │
                                            ▼
/speckit.tasks → /speckit.implement（自動加入 @spec 註解）
                        │
                        ▼
               /flowkit.trace（產生索引）← 可選但建議
                        │
                        ▼
              /flowkit.pre-unify-check（含 Traceability 驗證）
                        │
                        ▼
              /flowkit.unify-flow（合併 traceability-index 至 System 層）
```

### 5.2 最小流程（不含 Traceability）

```
/speckit.specify → /speckit.plan → /speckit.tasks → /speckit.implement
                                                           │
                                                           ▼
                                              /flowkit.pre-unify-check
                                                           │
                                                           ▼
                                              /flowkit.unify-flow
```

---

## 6. 預期效益

| 效益 | 說明 | 受益者 |
|------|------|--------|
| **快速定位** | 從 Spec 快速找到對應程式碼 | AI、人類 |
| **覆蓋率可視化** | 清楚知道哪些 Spec 已實作 | 人類 |
| **Code Review 效率** | Review 時知道程式碼對應哪個需求 | 人類 |
| **一致性檢查強化** | 可以檢查「有程式碼但沒 spec」 | AI |
| **文件自動化** | 減少手動維護對應關係 | 人類 |

---

## 7. 實作路線圖

### Phase 1：基礎建設 ✅ 完成

- [x] 建立 `traceability-index-template.md`
- [x] 修改 `tasks-template.md`（強化 [US] 標籤說明）
- [x] 修改 `speckit.implement.agent.md`（加入 @spec 註解規則）

### Phase 2：核心功能 ✅ 完成

- [x] 建立 `flowkit.trace.agent.md`（原提案為 speckit.trace，已改名）
- [x] 定義索引產生邏輯（5 Phase 執行步驟）
- [x] 定義覆蓋率計算方式

### Phase 3：整合驗證 ✅ 完成

- [x] 修改 `flowkit.pre-unify-check.agent.md`（加入 TR1-TR3 檢查）
- [x] 修改 `flowkit.unify-flow.prompt.md`（加入 traceability-index 合併邏輯）
- [ ] 測試完整流程（待實際專案驗證）

---

## 8. 開放問題

### Q1：@spec 註解應該多細緻？

| 選項 | 範例 | 優點 | 缺點 |
|------|------|------|------|
| **User Story 層級** | `@spec US1` | 簡單、低維護成本 | 定位不夠精確 |
| **AC 層級** | `@spec-ac AC1.1` | 精確、可追蹤 AC 覆蓋率 | 維護成本較高 |

**建議**：User Story 層級為必要，AC 層級為選用（由開發者決定）。

### Q2：索引應該存放在哪裡？

| 選項 | 位置 | 優點 | 缺點 |
|------|------|------|------|
| **Feature 層** | `specs/features/NNN/traceability-index.md` | 與 Feature 綁定、封存一起 | 分散 |
| **System 層** | `specs/system/traceability-index.md` | 集中管理 | Unify 後需合併 |

**實作決定**：Feature 層產生，Unify 時**合併至 System 層**（單一真相來源）。

**合併規則**（已實作於 `flowkit.unify-flow.prompt.md` Phase 4）：
| 情況 | 處理方式 |
|------|----------|
| User Story 首次出現 | 直接新增至 System 層 |
| User Story 已存在 | 以 Feature 版本覆蓋（Feature 是最新實作） |
| 舊 Feature 的 US | 保留（不刪除歷史追溯） |

### Q3：AI 真的需要這個索引嗎？

**分析**：
- AI 可以透過 semantic search 找到相關程式碼
- 但 @spec 註解可以提供**明確的意圖**（「這段程式碼是為了實現 US1」）
- 在大型專案中，索引可以減少 AI 的搜尋範圍

**結論**：對 AI 有幫助但非必要；對人類很有價值。

---

## 9. 實作摘要

### 已建立/修改的檔案

| 檔案 | 位置 | 說明 |
|------|------|------|
| `flowkit.trace.agent.md` | `flowkit/agents/` | 新建，產生 traceability-index.md |
| `traceability-index-template.md` | `speckit/templates/` | 新建，索引模板 |
| `speckit.implement.agent.md` | `speckit/agents/` | 新增 Step 8 @spec 註解規則 |
| `tasks-template.md` | `speckit/templates/` | 新增 User Story 標籤用途說明 |
| `flowkit.pre-unify-check.agent.md` | `flowkit/agents/` | Phase 3.4 新增 TR1-TR3 檢查 |
| `flowkit.unify-flow.prompt.md` | `flowkit/prompt/` | Phase 4 新增 traceability-index 合併 |

### 下一步

1. 在實際專案中測試完整流程
2. 收集回饋並調整
3. 考慮是否需要 CLI 指令包裝

---

> **提案已完成實作** (2026-01-25)  
> 本提案的所有核心功能已實作完成，待實際專案驗證後可進行微調。
