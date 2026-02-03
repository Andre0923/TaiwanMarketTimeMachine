# `--default` 模式說明

> **版本**：1.1.0  
> **適用範圍**：SpecKit + FlowKit 所有指令

---

## 目的

解決 GitHub Copilot Agent 模式下「必須輸入 prompt 才能觸發指令」的限制。

在 Cursor 中，可以直接執行 `/speckit.plan` 不輸入任何參數；但在 GitHub Copilot 中，必須輸入一些內容才能觸發。`--default` 提供了一個明確的方式表達「我沒有額外指示，請執行預設流程」。

---

## 使用方式

在 GitHub Copilot Agent 模式下，輸入指令時加上 `--default`：

```
@workspace /speckit.plan --default
```

等同於在 Cursor 中直接執行：

```
/speckit.plan
```

---

## 行為定義

### 一般指令

`--default` = **空白輸入的同義詞**

- AI 會將 `--default` 視為「無額外使用者指示」
- 指令會依照原本定義的預設流程執行

### 特殊行為指令

以下指令的 `--default` 有特殊自動偵測行為：

| 指令 | `--default` 行為 |
|------|------------------|
| `/speckit.specify` | 自動尋找 `docs/requirements/Milestone/` 下編號最大的 `MNN-*.md` 作為 Feature 描述輸入 |
| `/flowkit.Milestone-context` | 等同 `--milestone`（不指定編號），自動取編號最大的 Milestone |

---

## 適用指令

### SpecKit 指令
- `/speckit.specify` ⭐ 特殊行為：自動找最大 Milestone
- `/speckit.clarify`
- `/speckit.plan`
- `/speckit.tasks`
- `/speckit.analyze`
- `/speckit.implement`
- `/speckit.constitution`
- `/speckit.checklist`
- `/speckit.taskstoissues`

### FlowKit 指令
- `/flowkit.Milestone-context` ⭐ 特殊行為：自動取最大 Milestone
- `/flowkit.system-context`
- `/flowkit.consistency-check`
- `/flowkit.pre-unify-check`
- `/flowkit.unify-flow`
- `/flowkit.trace`
- `/flowkit.requirement-sync`

### 不適用（需要明確輸入）
- `/flowkit.refine-loop`（需要變更描述）
- `/flowkit.BDD-Milestone`（需要模式指定）

---

## 設計原則

1. **最小幅度調整**：只在 User Input 區塊加一行說明
2. **向後相容**：不影響原有的空白輸入行為
3. **語意明確**：`--default` 比任意輸入更能表達「使用預設值」的意圖
4. **智慧預設**：特定指令有合理的自動偵測行為（如自動找最大 Milestone）
