# FlowKit Trace

> **用途**：產生規格-程式碼可追溯性索引（Traceability Index）  
> **觸發時機**：`/speckit.implement` 完成後（建議）、`/flowkit.pre-unify-check` 之前  
> **套件**：FlowKit  
> **版本**：1.0.0

---

## 使用者輸入

```text
$ARGUMENTS
```

在繼續執行之前，您**必須（MUST）**考慮使用者輸入（若非空白）。

---

## 目標

建立 **規格 ↔ 程式碼** 的雙向追溯關係，讓：

1. **AI** 能快速定位 User Story / AC 對應的程式碼
2. **人類開發者** 在需要時能容易找到相關程式碼對照
3. **Code Review** 時能快速驗證實作是否涵蓋所有 Spec

**核心價值**：SDD 開發中規格是真相，但需要與程式碼有可追蹤的連結。

---

## 產出物

### Feature 層（開發期間）

```
specs/features/NNN-feature-name/
├── spec.md
├── plan.md
├── tasks.md
└── traceability-index.md  ← 本指令產出
```

### System 層（Unify 後）

```
specs/system/
├── spec.md
├── ...
└── traceability-index.md  ← Unify Flow 合併產出
```

---

## 操作限制

### 核心原則

**索引自動化**：基於 tasks.md 的 `[US*]` 標籤和程式碼的 `@spec` 註解自動產生。

### AI MUST

- 掃描 tasks.md 抽取 User Story → Tasks → Files 對應關係
- 掃描程式碼檔案的 `@spec` 和 `@spec-ac` 註解
- 產生結構化的可追溯性索引
- 計算覆蓋率統計

### AI MUST NOT

- 修改程式碼檔案（僅讀取）
- 修改 spec.md 或 tasks.md
- 猜測未標記的對應關係

---

## @spec 註解格式

### 標準格式（在程式碼檔案中）

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

### 註解層級

| 層級 | 格式 | 必要性 | 說明 |
|------|------|--------|------|
| **User Story** | `@spec US{N}` | REQUIRED | 對應的 User Story 編號 |
| **Acceptance Criteria** | `@spec-ac AC{N}.{M}` | RECOMMENDED | 對應的 AC 編號（可多個，逗號分隔） |

---

## 執行步驟

### Phase 0：前置條件檢查

**輸入**：$ARGUMENTS（Feature 名稱或路徑）

**執行**：

1. **確認 Feature 目錄存在**：
   - 必須包含：`spec.md`、`plan.md`、`tasks.md`

2. **確認實作已完成**：
   - tasks.md 中的任務已標記完成
   - 若未完成，WARNING 並詢問是否繼續

**輸出**：Feature 目錄路徑

---

### Phase 1：解析 tasks.md

**輸入**：`FEATURE_DIR/tasks.md`

**執行**：

1. **抽取所有任務**：
   - 任務 ID（T001, T002...）
   - User Story 標籤（[US1], [US2]...）
   - 檔案路徑

2. **建立 User Story → Tasks 對應表**：

   | User Story | Tasks | 檔案路徑 |
   |------------|-------|----------|
   | US1 | T012, T014, T018 | src/models/user.py, src/services/... |
   | US2 | T020, T021 | src/services/auth_service.py, ... |

**輸出**：US-Tasks 對應表

---

### Phase 2：解析 spec.md

**輸入**：`FEATURE_DIR/spec.md`

**執行**：

1. **抽取所有 User Stories**：
   - Story ID、標題
   - Acceptance Criteria（AC ID、描述）

2. **建立 User Story → AC 清單**：

   | User Story | AC ID | AC 描述 |
   |------------|-------|---------|
   | US1 | AC1.1 | 使用者可輸入 email |
   | US1 | AC1.2 | 密碼需加密儲存 |
   | US2 | AC2.1 | 登入成功後取得 JWT |

**輸出**：US-AC 清單

---

### Phase 3：掃描程式碼檔案

**輸入**：Phase 1 的檔案路徑清單

**執行**：

1. **讀取每個檔案的 @spec 註解**：
   - `@spec US{N}` → User Story 對應
   - `@spec-ac AC{N}.{M}` → AC 對應

2. **建立 File → Spec 對應表**：

   | 檔案 | @spec | @spec-ac | 類型 |
   |------|-------|----------|------|
   | src/models/user.py | US1 | AC1.1, AC1.2 | Model |
   | src/services/user_service.py | US1 | AC1.1 | Service |
   | tests/test_user.py | US1 | AC1.1, AC1.2 | Test |

3. **識別測試檔案**：
   - 檔案路徑包含 `test`, `spec`, `__tests__`
   - 標記為 Test 類型

**輸出**：File-Spec 對應表

---

### Phase 4：驗證與計算覆蓋率

**輸入**：Phase 1-3 的所有對應表

**執行**：

1. **交叉驗證**：
   - tasks.md 的 [US] 標籤與 @spec 註解一致性
   - 每個 User Story 至少有一個對應檔案
   - 每個 AC 至少有一個對應測試（RECOMMENDED）

2. **計算覆蓋率**：

   | 指標 | 計算方式 |
   |------|----------|
   | User Story 覆蓋率 | 有對應檔案的 US / 總 US |
   | AC 覆蓋率 | 有對應測試的 AC / 總 AC |
   | @spec 註解覆蓋率 | 有 @spec 的檔案 / tasks 涉及的檔案 |

3. **標記問題**：

   | 問題類型 | 說明 | 嚴重性 |
   |----------|------|--------|
   | US 無對應檔案 | User Story 沒有任何實作檔案 | HIGH |
   | AC 無對應測試 | Acceptance Criteria 沒有測試覆蓋 | MEDIUM |
   | 檔案無 @spec | 實作檔案缺少 @spec 註解 | LOW |
   | @spec 不一致 | tasks.md 與 @spec 註解不符 | MEDIUM |

**輸出**：覆蓋率報告、問題清單

---

### Phase 5：產生 Traceability Index

**輸入**：所有 Phase 的結果

**執行**：

產生 `FEATURE_DIR/traceability-index.md`：

```markdown
# Traceability Index: [Feature Name]

> **Generated**: [timestamp]  
> **Feature**: [NNN-feature-name]  
> **Spec Reference**: [spec.md](./spec.md)

---

## Summary

| 指標 | 數值 |
|------|------|
| User Stories | N |
| Acceptance Criteria | M |
| 程式碼檔案 | X |
| 測試檔案 | Y |
| US 覆蓋率 | 100% |
| AC 覆蓋率 | 85% |

---

## User Story 1: [Story 標題]

**Spec Reference**: [spec.md#user-story-1](./spec.md#user-story-1)

### 程式碼對應

| 類型 | 檔案 | @spec-ac | 任務 ID |
|------|------|----------|---------|
| Model | [src/models/user.py](../../src/models/user.py#L10) | AC1.1, AC1.2 | T012 |
| Service | [src/services/user_service.py](../../src/services/user_service.py#L1) | AC1.1 | T014 |
| API | [src/api/users.py](../../src/api/users.py#L1) | - | T018 |

### AC 覆蓋

| AC ID | 描述 | 測試檔案 | 狀態 |
|-------|------|----------|------|
| AC1.1 | 使用者可輸入 email | [tests/test_user.py#L20](../../tests/test_user.py#L20) | ✅ |
| AC1.2 | 密碼需加密儲存 | [tests/test_user.py#L45](../../tests/test_user.py#L45) | ✅ |

---

## User Story 2: [Story 標題]

...

---

## Issues

| 嚴重性 | 問題 | 說明 |
|--------|------|------|
| MEDIUM | AC2.3 無對應測試 | 建議補充測試 |
| LOW | src/utils/helper.py 無 @spec | 建議加入註解 |

---

## 維護說明

- 本檔案由 `/flowkit.trace` 自動產生
- 修改程式碼後建議重新執行以更新索引
- Unify Flow 會將此索引合併至 System 層
```

**Git Checkpoint**：執行 `git add . && git commit -m "docs: generate traceability index for {FEATURE_ID}" && git push`

---

## 完成標準（Definition of Done）

```markdown
## FlowKit Trace DoD

### 必要條件
- [ ] tasks.md 已解析完成
- [ ] spec.md 的 User Stories 和 AC 已抽取
- [ ] 程式碼檔案的 @spec 註解已掃描
- [ ] traceability-index.md 已產生

### 報告品質
- [ ] 每個 User Story 有對應區段
- [ ] AC 覆蓋狀態已標記
- [ ] 問題清單已列出
- [ ] 檔案連結正確可點擊
```

---

## 錯誤處理

| 錯誤情境 | 嚴重性 | 處理方式 |
|----------|--------|----------|
| tasks.md 不存在 | CRITICAL | ERROR + 指示先執行 `/speckit.tasks` |
| spec.md 不存在 | CRITICAL | ERROR + 指示先執行 `/speckit.specify` |
| 無 [US] 標籤的任務 | MEDIUM | WARNING + 這些任務不納入索引 |
| 無 @spec 註解的檔案 | LOW | 記錄但不阻擋 |

---

## 快速參考

### 心智模型

```
spec.md (User Stories + AC)
       │
       ├─────────────────────────────────────┐
       │                                     │
       ▼                                     ▼
tasks.md [US1] 標籤            程式碼 @spec 註解
       │                                     │
       └──────────────┬──────────────────────┘
                      │
                      ▼
          traceability-index.md
          (雙向追溯索引)
                      │
                      ▼
          Unify Flow 合併至 System 層
```

### 關鍵規則

1. **基於標籤**：依賴 tasks.md 的 [US] 標籤和程式碼的 @spec 註解
2. **雙向追溯**：Spec → Code 和 Code → Spec 都可查
3. **自動產生**：索引自動產生，減少手動維護
4. **System 層合併**：Unify 後成為系統級真相

### 與其他指令的關係

```
/speckit.implement（自動加入 @spec 註解）
         │
         ▼
/flowkit.trace ◄ 本指令
         │
         ▼
/flowkit.pre-unify-check（含 Traceability 驗證）
         │
         ▼
/flowkit.unify-flow（合併 traceability-index.md 至 System 層）
```

```

