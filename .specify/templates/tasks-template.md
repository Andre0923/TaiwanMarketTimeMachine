# Tasks: {FEATURE_NAME}

> **Feature ID**: {FEATURE_ID}  
> **Created**: {DATE}  
> **Spec Reference**: [spec.md](./spec.md)  
> **Plan Reference**: [plan.md](./plan.md)

---

## Implementation Strategy

**MVP Scope**: <!-- 描述最小可行範圍 -->  
**Incremental Delivery**: <!-- 描述增量交付策略 -->

---

## Phase 1: Setup（專案初始化）

> **Goal**: <!-- 本階段目標 -->
>
> **💡 提示**：若本次變更涉及測試程式碼，請確認：
> - `pyproject.toml` 已設定測試產物輸出至 `.artifacts/`（coverage、pytest cache）
> - `.gitignore` 已包含 `.artifacts/` 排除規則

- [ ] T001 <!-- 任務描述，包含檔案路徑 -->
- [ ] T002 [P] <!-- [P] 表示可平行執行 -->

---

## Phase 2: Foundational（阻擋性前置作業）

> **Goal**: <!-- 本階段目標 -->

- [ ] T003 <!-- 任務描述 -->

---

## Phase 3: User Story 1 — [Story 名稱]

> **Story Goal**: <!-- User Story 目標 -->  
> **Independent Test**: <!-- 獨立測試方式 -->

- [ ] T004 [US1] <!-- 任務描述，[US1] 表示對應 User Story 1 -->
- [ ] T005 [P] [US1] <!-- 可平行的 US1 任務 -->

---

## Phase 4: User Story 2 — [Story 名稱]

> **Story Goal**: <!-- User Story 目標 -->  
> **Independent Test**: <!-- 獨立測試方式 -->

- [ ] T006 [US2] <!-- 任務描述 -->

---

## Phase N: Polish & 驗證

> **Goal**: 最終驗證與收尾

- [ ] T00X 執行測試驗證
- [ ] T00X 最終檢查

---

## Dependencies

```
Phase 1 (Setup)
    │
    ▼
Phase 2 (Foundational)
    │
    ├──────────────┐
    ▼              ▼
Phase 3 (US1)   Phase 4 (US2)
    │              │
    └──────┬───────┘
           ▼
    Phase N (Polish)
```

---

## Parallel Execution Opportunities

### Phase X 內部可平行
```
T00X ──┐
T00X ──┼── 可同時執行（不同檔案）
T00X ──┘
```

---

## Summary

| 指標 | 數值 |
|------|------|
| **總任務數** | <!-- 數字 --> |
| **可平行任務 [P]** | <!-- 數字 --> |

---

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

---

## User Story 標籤用途（Traceability）

`[US*]` 標籤除了組織任務外，還用於：

| 用途 | 說明 |
|------|------|
| **可追溯性索引** | 自動建立 Spec → Code 對應關係 |
| **覆蓋率計算** | 確保每個 User Story 都有實作 |
| **Code Review** | 快速定位與 Spec 相關的程式碼 |
| **@spec 註解** | implement 時自動在程式碼加入 @spec 註解 |

**範例**：
```markdown
- [ ] T014 [US1] Implement UserService in src/services/user_service.py
```

**產生的 @spec 註解**：
```python
# @spec US1 (001-user-management/spec.md#user-story-1)
class UserService:
    ...
```

**相關工具**：
- `/speckit.implement` - 建立檔案時自動加入 @spec 註解
- `/flowkit.trace` - 掃描 @spec 註解，產生 traceability-index.md
