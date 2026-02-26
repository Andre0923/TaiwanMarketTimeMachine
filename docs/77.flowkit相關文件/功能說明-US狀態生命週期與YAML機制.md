# 功能說明：US 狀態生命週期與 YAML 機制

> **版本**：v1.0.0  
> **建立日期**：2026-02-26  
> **最後更新**：2026-02-26  
> **適用範圍**：SpecKit + FlowKit 全流程

---

## 1. 概述

本文件說明 User Story（US）與 Feature Spec 在 SDD 開發流程中的**狀態生命週期**，包含：

- US 狀態定義與轉換規則
- Feature Spec 狀態定義（YAML frontmatter）
- 各指令的狀態管理職責
- 狀態追蹤位置與同步機制

**核心設計**：`flowkit.BDD-Milestone`（⏳→🧩）與 `flowkit.unify-flow` Phase 4.5（🧩→✅/🔶）形成互補，完成 US 狀態全生命週期閉環。

---

## 2. US 狀態定義

### 2.1 四種狀態

| 狀態 | 圖示 | 說明 |
|------|------|------|
| 尚未規劃 | ⏳ | 存在於需求宇宙，尚未排入任何 Milestone |
| Milestone 執行中 | 🧩 | 已排入 Milestone，正在開發中 |
| 部分完成 | 🔶 | AC 未完全滿足，部分延後處理 |
| 已完成 | ✅ | 所有 AC 皆已滿足並通過驗證 |

### 2.2 狀態轉換規則

```
     BDD-Milestone              unify-flow Phase 4.5
         排入                       結案
  ⏳ ─────────→ 🧩 ─────────→ ✅  （全部 AC 滿足）
  尚未規劃         執行中      │
                              └──→ 🔶  （部分 AC 滿足，餘下延後）
```

| 轉換 | 觸發指令 | 觸發時機 | 強度 |
|------|----------|----------|------|
| ⏳ → 🧩 | `flowkit.BDD-Milestone` | US 被選入 Milestone 時 | MUST |
| 🧩 → ✅ | `flowkit.unify-flow` Phase 4.5 | Feature 封存且全部 AC 滿足 | SHOULD |
| 🧩 → 🔶 | `flowkit.unify-flow` Phase 4.5 | Feature 封存但部分 AC 未滿足 | SHOULD |

> **注意**：🔶 → ✅ 的轉換發生在後續 Feature 補完剩餘 AC 後，再次由 unify-flow Phase 4.5 處理。

---

## 3. Feature Spec 狀態定義（YAML Frontmatter）

### 3.1 YAML 結構

Feature Spec（`specs/features/NNN-*/spec.md`）使用 YAML frontmatter 管理狀態：

```yaml
---
milestone: M01-feature-name
system_context: false
status: Draft  # Draft | In Progress | Implemented | Unified
created: 2026-02-26
updated: 2026-02-26
---
```

### 3.2 四種 Feature 狀態

| Status | 觸發指令 | 觸發時機 | 說明 |
|--------|----------|----------|------|
| `Draft` | `speckit.specify` | Spec 建立時（初始值） | 規格草稿 |
| `In Progress` | `speckit.implement` | 實作開始時 | 開發中 |
| `Implemented` | `speckit.implement` | 實作全部完成後 | 已實作，待驗證合併 |
| `Unified` | `flowkit.unify-flow` | Phase 4 封存時 | 已統合至 System Spec |

### 3.3 Feature 狀態生命週期

```
specify        implement(開始)    implement(完成)    unify-flow
   │                │                  │                │
   ▼                ▼                  ▼                ▼
 Draft  ──→  In Progress  ──→  Implemented  ──→  Unified
```

### 3.4 同步規則

Feature status 更新時 MUST 同步兩處：
1. **YAML frontmatter** 的 `status:` 欄位
2. **Inline 標記** `> **Status**: XXX`（通常在 spec.md 標頭區）

---

## 4. 雙軌狀態：US 狀態 vs Feature 狀態

US 狀態與 Feature 狀態是**獨立但關聯**的兩套追蹤系統：

```
┌─────────────────────────────────────────────────────────────┐
│  US 狀態軌（需求層）                                         │
│  追蹤位置：docs/requirements/user-stories/README.md          │
│                                                             │
│  ⏳ → 🧩 → ✅/🔶                                            │
│  │      │      │                                            │
│  │      │      └─ unify-flow Phase 4.5 依 AC 滿足度決定     │
│  │      └──────── BDD-Milestone 排入時更新                   │
│  └─────────────── BDD-Milestone INIT 建立時初始化            │
├─────────────────────────────────────────────────────────────┤
│  Feature 狀態軌（開發層）                                    │
│  追蹤位置：specs/features/NNN-*/spec.md YAML frontmatter     │
│                                                             │
│  Draft → In Progress → Implemented → Unified                │
│  │          │              │             │                   │
│  │          │              │             └─ unify-flow       │
│  │          │              └─────────── implement 完成       │
│  │          └────────────────────────── implement 開始       │
│  └───────────────────────────────────── specify 建立        │
└─────────────────────────────────────────────────────────────┘
```

### 對應關係

| Feature Status | 對應 US 狀態 | 說明 |
|----------------|-------------|------|
| `Draft` | 🧩 執行中 | Feature 已建立，US 正在被設計 |
| `In Progress` | 🧩 執行中 | Feature 實作中 |
| `Implemented` | 🧩 執行中 | Feature 實作完成但尚未統合 |
| `Unified` | ✅ 或 🔶 | 統合後由 Phase 4.5 依 AC 滿足度結案 |

---

## 5. 狀態追蹤位置總覽

### 5.1 US 狀態（Markdown 表格追蹤）

| 追蹤位置 | 格式 | 管理者 |
|----------|------|--------|
| `docs/requirements/user-stories/README.md` — US 索引表格 | `\| US A-1 \| 摘要 \| A \| ⏳ \|` | BDD-Milestone / unify-flow |
| `docs/requirements/user-stories/README.md` — 狀態快照 | `\| ⏳ 尚未規劃 \| N \| X% \|` | BDD-Milestone / unify-flow |
| `docs/requirements/user-stories/README.md` — 依狀態分類 | `#### ✅ 已完成` 區段 | BDD-Milestone / unify-flow |

### 5.2 Milestone 狀態（Inline 標記追蹤）

| 追蹤位置 | 格式 | 管理者 |
|----------|------|--------|
| `docs/requirements/Milestone/MNN-*.md` 標頭 | `> **狀態**：🧩 執行中` | BDD-Milestone / unify-flow |
| `docs/requirements/user-stories/README.md` — Milestone 追蹤表格 | `\| M01 \| 名稱 \| 🧩 執行中 \| A-1, A-2 \|` | BDD-Milestone / unify-flow |

### 5.3 Feature Spec 狀態（YAML Frontmatter 追蹤）

| 追蹤位置 | 格式 | 管理者 |
|----------|------|--------|
| `specs/features/NNN-*/spec.md` YAML | `status: Draft` | specify / implement / unify-flow |
| `specs/features/NNN-*/spec.md` Inline | `> **Status**: Draft` | specify / implement / unify-flow |

---

## 6. 指令狀態管理職責

### 6.1 flowkit.BDD-Milestone

**職責**：US 狀態生命週期的**前半段**（⏳→🧩）

| 模式 | 狀態操作 | 更新位置 |
|------|----------|----------|
| `--init` | 所有新建 US 初始化為 ⏳ | README.md US 索引 |
| `--milestone` | 選入的 US 從 ⏳ → 🧩 | README.md US 索引 + 狀態快照 |

**驗證規則**：
- 僅允許 ⏳ 狀態的 US 被選入 Milestone
- 已為 🧩/✅/🔶 的 US 不可重複選入（需先確認）

### 6.2 flowkit.unify-flow（Phase 4.5）

**職責**：US 狀態生命週期的**後半段**（🧩→✅/🔶）

| 步驟 | 操作 | 判斷依據 |
|------|------|----------|
| 1 | 從 Feature Spec 抽取涉及的 US IDs | `milestone:` 欄位 + Spec 內容 |
| 2 | 更新 README.md US 狀態（🧩→✅ 或 🧩→🔶） | AC 測試通過率 |
| 3 | 評估 Milestone 完成度 | 所有 US 是否皆 ✅ |
| 4 | 若全部 US ✅ → MUST ASK 人類確認結案 | 人類決策 |

**條件觸發**：僅當 `docs/requirements/user-stories/README.md` 存在時執行

**強度等級**：SHOULD（Phase 4.5 失敗不阻擋 Unify Flow 完成）

**AC 滿足度判斷邏輯**：

| 情況 | 結果狀態 |
|------|----------|
| 該 US 所有 AC 均有對應測試且 PASS | ✅ 已完成 |
| 部分 AC 無對應測試或 FAIL | 🔶 部分完成 |

### 6.3 speckit.implement

**職責**：Feature Spec 狀態的中段管理

| 時機 | 狀態操作 | 更新位置 |
|------|----------|----------|
| 開始實作 | `Draft` → `In Progress` | spec.md YAML + Inline |
| 完成實作 | `In Progress` → `Implemented` | spec.md YAML + Inline |

### 6.4 其他指令

| 指令 | 狀態操作 |
|------|----------|
| `speckit.specify` | 建立 spec.md 時設為 `Draft` |
| `flowkit.unify-flow` Phase 4 | 封存前設為 `Unified` |
| `flowkit.code-check` | 不修改狀態（僅驗證） |
| `flowkit.refine-loop` | 不修改狀態（修正後仍為 `In Progress`） |

---

## 7. 全生命週期閉環圖

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        US 狀態全生命週期                                 │
│                                                                         │
│   BDD-Milestone        BDD-Milestone        unify-flow                  │
│    (--init)             (--milestone)       (Phase 4.5)                  │
│       │                     │                   │                       │
│       ▼                     ▼                   ▼                       │
│    建立 US ──────→  ⏳ ──────→  🧩 ──────→  ✅  全部 AC 通過            │
│    (初始化)       尚未規劃      執行中      │                            │
│                                            └──→  🔶  部分 AC 通過       │
│                                                   │                     │
│                                    後續 Feature    │                     │
│                                    補完 AC 後      ▼                     │
│                                              🔶 → ✅                     │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                    Feature Spec 狀態生命週期                              │
│                                                                         │
│  specify     implement    implement     unify-flow                      │
│  (建立)       (開始)       (完成)       (Phase 4)                        │
│     │           │           │              │                            │
│     ▼           ▼           ▼              ▼                            │
│  Draft ──→ In Progress ──→ Implemented ──→ Unified                      │
│                                                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                    Milestone 狀態生命週期                                 │
│                                                                         │
│  BDD-Milestone              unify-flow Phase 4.5                        │
│  (--milestone)             （所有 US ✅ + 人類確認）                      │
│       │                          │                                      │
│       ▼                          ▼                                      │
│  🧩 執行中 ──────────────→  ✅ 已完成                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 8. 狀態同步時序

以下為一個完整 Feature 開發流程中的狀態變化時序：

| 步驟 | 指令 | US 狀態 | Feature 狀態 | Milestone 狀態 |
|------|------|---------|-------------|---------------|
| 1a | BDD-Milestone `--init` | ⏳（建立） | — | — |
| 1b | BDD-Milestone `--milestone` | ⏳ → 🧩 | — | 🧩 執行中 |
| 3 | speckit.specify | 🧩 | `Draft` | 🧩 |
| 9 | speckit.implement（開始） | 🧩 | `In Progress` | 🧩 |
| 9 | speckit.implement（完成） | 🧩 | `Implemented` | 🧩 |
| 11 | unify-flow Phase 4 | 🧩 | `Unified` | 🧩 |
| 11 | unify-flow Phase 4.5 | 🧩 → ✅/🔶 | `Unified` | 🧩 或 ✅ |

---

## 9. 常見情境

### 9.1 一個 Milestone 包含多個 Feature

```
M01 包含 US A-1, A-2, A-3

Feature 001-auth（涵蓋 US A-1, A-2）完成 unify-flow：
  → US A-1: 🧩 → ✅
  → US A-2: 🧩 → ✅
  → US A-3: 仍為 🧩（不在此 Feature 範圍）
  → M01 狀態: 仍為 🧩（未全部完成）

Feature 002-profile（涵蓋 US A-3）完成 unify-flow：
  → US A-3: 🧩 → ✅
  → M01 狀態: 所有 US 皆 ✅ → ASK 人類確認結案 → ✅
```

### 9.2 部分完成的情況

```
Feature 001-auth（涵蓋 US A-1, A-2）
  → US A-1: 全部 AC 通過 → ✅
  → US A-2: AC2 未通過（延後至下一期）→ 🔶

後續 Feature 003-auth-v2（補完 US A-2 的 AC2）
  → US A-2: 🔶 → ✅
```

### 9.3 README.md 不存在時

若 `docs/requirements/user-stories/README.md` 不存在：
- BDD-Milestone `--init` 會自動建立
- unify-flow Phase 4.5 **不執行**（條件觸發，不阻擋流程）

---

## 10. 注意事項

### 10.1 人為手動修改

- US 狀態原則上由自動化管理，SHOULD NOT 手動修改
- 若必須手動修改，MUST 同步更新 README.md 中的三處：US 索引、狀態快照、依狀態分類

### 10.2 狀態一致性檢查

- `flowkit.system-health` 的 D3 維度（文件品質）MAY 檢查 US 狀態一致性
- 不一致時產生 WARNING 而非 ERROR

### 10.3 YAML vs Markdown 表格

| 追蹤對象 | 追蹤機制 | 原因 |
|----------|----------|------|
| Feature Spec 狀態 | YAML frontmatter | 單一檔案，結構化欄位適合機器讀取 |
| US 狀態 | README.md Markdown 表格 | 集中索引，多 US 跨 Group，表格適合人類瀏覽 |
| Milestone 狀態 | Milestone 檔案 inline 標記 + README.md 表格 | 分散但有中央索引 |

---

## 改版歷史

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.0.0 | 2026-02-26 | 初版建立：US 四種狀態定義、雙軌狀態系統、全生命週期閉環圖、指令職責分工 |
