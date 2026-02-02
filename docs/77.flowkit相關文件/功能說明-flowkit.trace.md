# FlowKit Trace 功能說明

> **指令名稱**：`/flowkit.trace`  
> **Agent 檔案**：`flowkit/agents/flowkit.trace.agent.md`  
> **相關 Template**：`flowkit/templates/traceability-index-template.md`

---

## 1. 功能概述

### 1.1 這是什麼？

`/flowkit.trace` 是一個**規格-程式碼可追溯性索引產生工具**，用於建立 Spec 與實作程式碼之間的雙向追溯關係。

### 1.2 解決什麼問題？

| 問題 | 解決方式 |
|------|----------|
| 不知道某個 User Story 實作在哪 | 索引列出 US → Code 對應 |
| 不知道某段程式碼對應哪個需求 | @spec 註解 + 索引反查 |
| 無法確認所有需求都有實作 | 覆蓋率統計清楚顯示 |
| Code Review 時難以對照規格 | 索引提供快速定位 |

### 1.3 核心價值

```
「從 Spec 找到 Code，從 Code 追回 Spec」
```

---

## 2. 使用時機

### 2.1 何時執行？

```
/speckit.specify → /speckit.plan → /flowkit.consistency-check
                                            │
                                            ▼
                 /speckit.tasks → /speckit.implement
                                            │
                                            ▼
                              /flowkit.pre-unify-check
                                            │
                                            ▼
                                   /flowkit.trace ◄── 在此執行
                                            │
                                            ▼
                              /flowkit.requirement-sync
                                            │
                                            ▼
                                  /flowkit.unify-flow
```

### 2.2 執行條件

| 條件 | 必要性 | 說明 |
|------|--------|------|
| `spec.md` 存在 | REQUIRED | 需要 User Stories 來源 |
| `tasks.md` 存在 | REQUIRED | 需要 [US*] 標籤對應 |
| 程式碼已實作 | RECOMMENDED | 掃描 @spec 註解 |
| 測試已撰寫 | OPTIONAL | 用於 AC 覆蓋率計算 |

---

## 3. 輸入與輸出

### 3.1 輸入

| 來源 | 讀取內容 |
|------|----------|
| `FEATURE_DIR/spec.md` | User Stories、Acceptance Criteria |
| `FEATURE_DIR/tasks.md` | [US*] 標籤、檔案路徑 |
| `src/**/*.py` 等 | @spec、@spec-ac 註解 |
| `tests/**/*` | 測試與 AC 對應 |

### 3.2 輸出

| 產出 | 位置 | 說明 |
|------|------|------|
| **traceability-index.md** | `FEATURE_DIR/traceability-index.md` | 主要索引檔案 |
| **覆蓋率報告** | 終端輸出 | 顯示缺漏項目 |

---

## 4. 執行流程

### Phase 1：解析 Spec
- 抽取所有 User Stories
- 抽取所有 Acceptance Criteria
- 建立 US/AC 清單

### Phase 2：解析 Tasks
- 抽取 [US*] 標籤
- 對應 US → Task → 檔案路徑

### Phase 3：掃描程式碼
- 掃描 tasks.md 列出的檔案
- 抽取 @spec 和 @spec-ac 註解
- 建立 Code → US/AC 對應

### Phase 4：掃描測試
- 識別測試檔案
- 抽取測試與 AC 對應
- 計算 AC 測試覆蓋率

### Phase 5：產生索引
- 建立 traceability-index.md
- 計算覆蓋率統計
- 列出未覆蓋項目

---

## 5. @spec 註解格式

### 5.1 程式碼標記

```python
# Python
# @spec US1 (001-feature/spec.md#user-story-1)
# @spec-ac AC1.1, AC1.2

class UserService:
    pass
```

```typescript
// TypeScript/JavaScript
// @spec US1 (001-feature/spec.md#user-story-1)
// @spec-ac AC1.1, AC1.2

export class UserService { }
```

```rust
// Rust/C/C++
// @spec US1 (001-feature/spec.md#user-story-1)
// @spec-ac AC1.1, AC1.2

pub struct User { }
```

### 5.2 欄位說明

| 註解 | 必要性 | 格式 | 範例 |
|------|--------|------|------|
| `@spec US{N}` | REQUIRED | US + 數字 | `@spec US1` |
| `(path#anchor)` | REQUIRED | Spec 相對路徑 | `(001-feature/spec.md#user-story-1)` |
| `@spec-ac AC{N}.{M}` | OPTIONAL | 可多個，逗號分隔 | `@spec-ac AC1.1, AC1.2` |

---

## 6. 相關 Template

### 6.1 traceability-index-template.md

**位置**：`flowkit/templates/traceability-index-template.md`

**用途**：定義 traceability-index.md 的標準格式

**主要區段**：

| 區段 | 說明 |
|------|------|
| Summary | 覆蓋率統計摘要 |
| User Story N | 每個 US 的程式碼/測試對應 |
| AC 覆蓋 | 每個 AC 的測試對應狀態 |
| Issues | 覆蓋率問題清單 |

**範例結構**：

```markdown
# Traceability Index: {FEATURE_NAME}

## Summary
| 指標 | 數值 |
|------|------|
| US 覆蓋率 | 100% |
| AC 覆蓋率 | 85% |

## User Story 1: 使用者註冊

### 程式碼對應
| 類型 | 檔案 | @spec-ac | 任務 ID |
|------|------|----------|---------|
| Model | src/models/user.py | AC1.1 | T012 |

### AC 覆蓋
| AC ID | 描述 | 測試檔案 | 狀態 |
|-------|------|----------|------|
| AC1.1 | 可輸入 email | tests/test_user.py#L20 | ✅ |
```

---

## 7. 與其他指令的關係

### 7.1 上游指令

| 指令 | 關係 |
|------|------|
| `/speckit.implement` | 實作時自動加入 @spec 註解 |
| `/speckit.tasks` | 提供 [US*] 標籤對應 |

### 7.2 下游指令

| 指令 | 關係 |
|------|------|
| `/flowkit.pre-unify-check` | 檢查 Traceability 覆蓋率（TR1-TR3） |
| `/flowkit.unify-flow` | 合併 traceability-index.md 至 System 層 |

### 7.3 流程圖

```
tasks.md [US1] 標籤 ──────────┐
                              │
程式碼 @spec 註解 ────────────┼──► /flowkit.trace
                              │         │
測試檔案 ─────────────────────┘         │
                                        ▼
                              traceability-index.md
                                        │
                    ┌───────────────────┴───────────────────┐
                    ▼                                       ▼
          /flowkit.pre-unify-check              /flowkit.unify-flow
          (驗證 TR1-TR3)                        (合併至 System 層)
```

---

## 8. 使用範例

### 8.1 基本使用

```
/flowkit.trace
```

自動偵測當前 Feature 目錄並產生索引。

### 8.2 指定 Feature

```
/flowkit.trace 001-user-management
```

指定特定 Feature 目錄。

### 8.3 輸出範例

```markdown
## FlowKit Trace 執行結果

### 狀態：✅ 成功

### 覆蓋率統計
| 指標 | 數值 |
|------|------|
| User Stories | 3 |
| 已覆蓋 US | 3 (100%) |
| Acceptance Criteria | 8 |
| 已覆蓋 AC | 7 (87.5%) |

### 未覆蓋項目
| 類型 | ID | 說明 |
|------|----|----|
| AC | AC2.3 | 無對應測試 |

### 產出檔案
- traceability-index.md（已建立）
```

---

## 9. 常見問題

### Q1：@spec 註解是自動加入的嗎？

**A**：是的，`/speckit.implement` 在建立新檔案時會自動加入。若是既有檔案，需手動補充。

### Q2：不執行 trace 可以嗎？

**A**：可以。Traceability 是選用功能，不執行也能完成 Unify Flow。但建議執行以提升可追溯性。

### Q3：索引會在 Unify 後消失嗎？

**A**：不會。Feature 層的索引會封存至 history，同時合併至 System 層的 `traceability-index.md`。

### Q4：覆蓋率 100% 才能 Unify 嗎？

**A**：不需要。覆蓋率檢查（TR1-TR3）在 pre-unify-check 中是 MEDIUM/LOW 嚴重性，非阻擋性。

---

## 10. 版本歷史

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.0.0 | 2026-01-25 | 初始版本 |

---

## 附錄：檔案位置索引

| 檔案 | 路徑 |
|------|------|
| Agent 指令 | `flowkit/agents/flowkit.trace.agent.md` |
| Index Template | `flowkit/templates/traceability-index-template.md` |
| 功能提案 | `docs/design-proposals/traceability-feature-proposal.md` |
