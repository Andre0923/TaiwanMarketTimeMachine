# FlowKit 功能說明文件總覽

> **最後更新**：2025-07-12  
> **用途**：FlowKit 相關指令的功能說明索引

---

## 什麼是 FlowKit？

FlowKit 是 **開發流程工具套件**，提供 Feature 開發過程中的檢查、驗證、追溯等功能。

與 SpecKit（規格定義套件）互補：
- **SpecKit**：定義「做什麼」→ specify, clarify, plan, tasks, analyze, implement
- **FlowKit**：確保「做對」→ BDD-Milestone, Milestone-context, consistency-check, code-check, trace, pre-unify-check, unify-flow, refine-loop, system-context, pr-review, system-health

---

## 🚀 半自動化開發流程（`--default` 模式）

所有 SpecKit 與 FlowKit 指令皆支援 **`--default` 模式**，實現半自動化開發流程：

```
開發者觸發指令 → AI 載入合理預設 → 執行並產出結果 → 開發者審閱確認 → 下一階段
```

**核心價值**：
- 開發者只需「審閱並確認意圖」，無需重複輸入參數
- AI 自動偵測最新 Milestone，載入相關上下文
- 流程順暢地從一個階段推進到下一個階段

**Smart Defaults（特殊預設行為）**：

| 指令 | `--default` 行為 |
|------|-----------------|
| `speckit.specify --default` | 自動偵測 `docs/requirements/Milestone/` 中編號最高的 `MNN-*.md` 作為 Feature 描述 |
| `flowkit.Milestone-context --default` | 自動選擇編號最高的 Milestone 產生開發上下文 |

📖 **詳細說明**：[功能說明-default-mode.md](./功能說明-default-mode.md)

---

## 指令總覽

| 指令 | 執行時機 | 目的 | 阻擋性 |
|------|----------|------|--------|
| `/flowkit.BDD-Milestone` | 需求規劃階段 | PRD → User Stories（首次）、US → Milestone（每次）| - |
| `/flowkit.Milestone-context` | BDD-Milestone 後 / Plan 前 | 從 PRD 擷取設計上下文，檢測與 System 衝突 | 有衝突需決策 |
| `/flowkit.system-context` | Plan 前（後續 Feature） | 提供專案已實作部分的上下文 | - |
| `/flowkit.consistency-check` | Plan 後 | 檢查與System間：覆用、不重做、整合建議 | 有問題需修正 |
| `/flowkit.refine-loop` | Code Check FAIL 時 | 小幅修正的縮小版 SpecKit | - |
| `/flowkit.code-check` | Implement 後 | AI 驅動五層驗證金字塔（L0→L4） | L0/L1 FAIL 阻斷 |
| `/flowkit.trace` | Implement 後 | 建立 Spec-Code 追溯索引 | - |
| `/flowkit.requirement-sync` | Unify 前 | 將 Feature 變更回寫至 PRD / User Stories | - |
| `/flowkit.pre-unify-check` | Unify 前 | 檢查 Spec 品質與實作對齊 | 有問題需修正 |
| `/flowkit.unify-flow` | 驗證通過後 | 合併 Feature 至 System | - |
| `/flowkit.pr-review` | Unify 後 | 六維品質審查 + 自動 PR 建立 | C/H 阻擋、M 警告 |
| `/flowkit.system-health` | Milestone 前 / 定期 | 五維度全專案健康檢查 + TD 自動登記 | Advisory（不阻斷） |



---

## 開發流程總覽表

| 階段 | 步驟 | 指令 | 輸入 | 輸出 | 備註 |
|------|------|------|------|------|------|
| **需求規劃** | 1a | `flowkit.BDD-Milestone` | PRD | User Stories | 🟡 僅首次 / PRD 變更時 |
| | 1b | `flowkit.BDD-Milestone` | User Stories | Milestone | 每次 Feature 開發 |
| | 2 | `flowkit.Milestone-context` | PRD, Milestone, System | 設計上下文, 衝突報告 | 抽取相關內容 + 衝突檢測 |
| **規格定義** | 3 | `speckit.specify` | Milestone | Feature Spec, 新分支 | 建立 Feature 規格 |
| | 4 | `speckit.clarify` | Spec | 釐清後 Spec | 🟡 選擇性 |
| | 5 | `flowkit.system-context` | System | 已實作上下文 | 🟡 首個 Feature 可略過 |
| | 6 | `speckit.plan` | Spec, 上下文 | Plan | 制定實作計畫 |
| | 7 | `flowkit.consistency-check` | Plan, System | 檢查報告 | 🟡 首個 Feature 可略過 |
| **任務拆解** | 8a | `speckit.tasks` | Plan | Tasks | 拆解可驗收任務 |
| | 8b | `speckit.analyze` | Tasks, 程式碼 | 分析報告 | 確認 Feature 內一致性 |
| **實作** | 9 | `speckit.implement` | Tasks | 程式碼, 測試 | 實作程式碼 |
| | 9.5 | `flowkit.code-check` | 程式碼, 測試 | 驗證報告 | AI 五層驗證金字塔 |
| | 9' | `flowkit.refine-loop` | 修正需求 | 更新 Spec/Code | 🔄 循環：code-check FAIL 時使用 |
| **驗證合併** | 10a | `flowkit.pre-unify-check` | 實作結果 | 檢查報告 | 確認可安全合併 |
| | 10b | `flowkit.trace` | Spec, Code | 追溯索引 | 建立規格-程式碼對照 |
| | 10c | `flowkit.requirement-sync` | Feature, PRD, US | 更新需求文件 | 回寫變更至 PRD / User Stories |
| | 11 | `flowkit.unify-flow` | Feature | System 更新 | 合併至 System Spec |
| **PR 提交** | 12 | `flowkit.pr-review` | 全部產出 | PR Review 報告, PR | 六維品質審查 + 自動 PR |

---

## 開發流程中的位置

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                              SDD 開發流程                                         │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│  ┌─────────────────────────── 📋 Phase 1：需求規劃 ───────────────────────────┐   │
│  │                                                                           │   │
│  │  📘 PRD-*.md                                                              │   │
│  │       │                                                                   │   │
│  │       ▼                                                                   │   │
│  │  ┌─────────────────────────────────────────────────────────────────┐      │   │
│  │  │ 🟡 1️⃣a flowkit.BDD-Milestone（PRD → User Stories）               │      │   │
│  │  │     ※ 僅首次 / PRD 變更時執行                                    │      │   │
│  │  └─────────────────────────────────────────────────────────────────┘      │   │
│  │       │                                                                   │   │
│  │       ▼                                                                   │   │
│  │  📑 User Stories ◄─────────────────────────────────────────────────┐      │   │
│  │       │                                                            │      │   │
│  │       ▼                                                            │      │   │
│  │  1️⃣b flowkit.BDD-Milestone（User Stories → Milestone）              │      │   │
│  │       │                                                            │      │   │
│  │       ▼                                                            │      │   │
│  │  🎯 Milestone ───► 2️⃣ flowkit.Milestone-context                     │      │   │
│  │                          │                                         │      │   │
│  │                 ┌────────┴────────┐                                │      │   │
│  │                 │                 │                                │      │   │
│  │              有衝突            無衝突                              │      │   │
│  │                 │                 │                                │      │   │
│  │                 ▼                 │                                │      │   │
│  │            決策處理 ──────────────┘                                │      │   │
│  │                                                                    │      │   │
│  │  ◄─────────────────── 下一個 Feature ─────────────────────────────┘      │   │
│  │                                                                           │   │
│  └───────────────────────────────────────────┼───────────────────────────────┘   │
│                                              │                                   │
│                                              ▼                                   │
│  ┌─────────────────────────── 📝 Phase 2：規格定義 ───────────────────────────┐   │
│  │                                                                           │   │
│  │  3️⃣ speckit.specify ───► 4️⃣ speckit.clarify（選擇性）                      │   │
│  │         │                                                                 │   │
│  │         ▼                                                                 │   │
│  │  ┌─────────────────────────────────────────────────┐                      │   │
│  │  │ 5️⃣ flowkit.system-context                        │                      │   │
│  │  │   （建議必要，除非首個 Feature）                  │                      │   │
│  │  └─────────────────────────────────────────────────┘                      │   │
│  │         │                                                                 │   │
│  │         ▼                                                                 │   │
│  │  6️⃣ speckit.plan ───► 7️⃣ flowkit.consistency-check                        │   │
│  │                              │                                            │   │
│  │                     ┌────────┴────────┐                                   │   │
│  │                     │                 │                                   │   │
│  │                  有問題            通過                                   │   │
│  │                     │                 │                                   │   │
│  │                     ▼                 │                                   │   │
│  │                 修正 Plan ────────────┘                                   │   │
│  │                                                                           │   │
│  └───────────────────────────────────────────┼───────────────────────────────┘   │
│                                              │                                   │
│                                              ▼                                   │
│  ┌─────────────────────────── 📋 Phase 3：任務拆解 ───────────────────────────┐   │
│  │                                                                           │   │
│  │  8️⃣a speckit.tasks ───► 8️⃣b speckit.analyze                                │   │
│  │                              │                                            │   │
│  │                     ┌────────┴────────┐                                   │   │
│  │                     │                 │                                   │   │
│  │                  有問題            通過                                   │   │
│  │                     │                 │                                   │   │
│  │                     ▼                 │                                   │   │
│  │              修正 Tasks/Plan ─────────┘                                   │   │
│  │                                                                           │   │
│  └───────────────────────────────────────────┼───────────────────────────────┘   │
│                                              │                                   │
│                                              ▼                                   │
│  ┌─────────────────────────── 💻 Phase 4：實作 ───────────────────────────────┐   │
│  │                                                                           │   │
│  │  9️⃣ speckit.implement ◄─────────────────┐                                  │   │
│  │         │                               │                                 │   │
│  │         ▼                               │                                 │   │
│  │  9️⃣.5️⃣ flowkit.code-check（AI 五層驗證金字塔）                               │   │
│  │         │                                                                 │   │
│  │    ┌────┴────┐                                                            │   │
│  │    │         │                                                            │   │
│  │  PASS      FAIL ─────► 9️⃣' flowkit.refine-loop                            │   │
│  │    │                                                                      │   │
│  └────┼──────────────────────────────────────────────────────────────────────┘   │
│       │                                                                          │
│       ▼                                                                          │
│  ┌─────────────────────────── ✅ Phase 5：驗證合併 ───────────────────────────┐   │
│  │                                                                           │   │
│  │  🔟a flowkit.pre-unify-check ───► 🔟b flowkit.trace                        │   │
│  │                                         │                                 │   │
│  │                                         ▼                                 │   │
│  │                               🔟c flowkit.requirement-sync                 │   │
│  │                                         │                                 │   │
│  │                                         ▼                                 │   │
│  │                                   可合併？ ───────否────► 回 Phase 4 修正   │   │
│  │                                         │                                 │   │
│  │                                        是                                 │   │
│  │                                         ▼                                 │   │
│  │                               1️⃣1️⃣ flowkit.unify-flow                      │   │
│  │                                         │                                 │   │
│  └─────────────────────────────────────────┼─────────────────────────────────┘   │
│                                      │                                           │
│                                      ▼                                           ││  ┌─────────────────────────── 📤 Phase 6：PR 提交 ───────────────────────────┐   │
│  │                                                                           │   │
│  │  1️⃣2️⃣ flowkit.pr-review（六維品質審查 + 自動 PR）                           │   │
│  │         │                                                                 │   │
│  │    ┌────┴────┐                                                            │   │
│  │    │         │                                                            │   │
│  │  READY    NOT READY ─────► refine-loop / 回退前階段                    │   │
│  │    │                                                                      │   │
│  │    ▼                                                                      │   │
│  │  🔀 gh pr create                                                        │   │
│  │                                                                           │   │
│  └─────────────────────────────────────────┴─────────────────────────────────┘   │
│                                      │                                           │
│                                      ▼                                           ││                           🔄 下一個 Feature ◄────────────────────────────────────┤
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
```

> 📖 完整 Mermaid 版本流程圖請參考：[SDD開發流程圖.md](./SDD開發流程圖.md)

---

## 功能說明文件清單

| 指令 | 說明文件 |
|------|----------|
| `/flowkit.BDD-Milestone` | [功能說明-flowkit.BDD-Milestone.md](./功能說明-flowkit.BDD-Milestone.md) |
| `/flowkit.Milestone-context` | [功能說明-flowkit.Milestone-context.md](./功能說明-flowkit.Milestone-context.md) |
| `/flowkit.consistency-check` | [功能說明-flowkit.consistency-check.md](./功能說明-flowkit.consistency-check.md) |
| `/flowkit.trace` | [功能說明-flowkit.trace.md](./功能說明-flowkit.trace.md) |
| `/flowkit.requirement-sync` | [功能說明-flowkit.requirement-sync.md](./功能說明-flowkit.requirement-sync.md) |
| `/flowkit.pre-unify-check` | [功能說明-flowkit.pre-unify-check.md](./功能說明-flowkit.pre-unify-check.md) |
| `/flowkit.unify-flow` | [功能說明-flowkit.unify-flow.md](./功能說明-flowkit.unify-flow.md) |
| `/flowkit.refine-loop` | [功能說明-flowkit.refine-loop.md](./功能說明-flowkit.refine-loop.md) |
| `/flowkit.system-context` | [功能說明-flowkit.system-context.md](./功能說明-flowkit.system-context.md) |
| `/flowkit.code-check` | [功能說明-flowkit.code-check.md](./功能說明-flowkit.code-check.md) |
| `/flowkit.pr-review` | [功能說明-flowkit.pr-review.md](./功能說明-flowkit.pr-review.md) |
| `--default` 模式 | [功能說明-default-mode.md](./功能說明-default-mode.md) |
| 技術債生命週期管理 | [功能說明-技術債生命週期管理.md](./功能說明-技術債生命週期管理.md) |
| 測試策略與自動化機制 | [功能說明-測試策略與自動化機制.md](./功能說明-測試策略與自動化機制.md) |

---

## 相關 Template

| Template | 位置 | 用途 |
|----------|------|------|
| `traceability-index-template.md` | `.flowkit/templates/` | Trace 索引格式 |
| `system-context-template.md` | `.flowkit/templates/` | 完整版上下文範本 |
| `system-context-index-template.md` | `.flowkit/templates/` | 精簡版上下文範本 |
| `Milestone-context-output.template.md` | `.flowkit/templates/` | Milestone 上下文輸出範本 |
| `Milestone-context-conflict-report.template.md` | `.flowkit/templates/` | 衝突報告範本 |
| `refine-plan.template.md` | `.flowkit/templates/` | Refine Loop Plan 範本 |
| `refine-spec-delta.template.md` | `.flowkit/templates/` | Refine Loop Spec Delta 範本 |
| `code-check-report.template.md` | `.flowkit/templates/` | Code Check 驗證報告範本 |
| `spec-delta-log.template.md` | `.flowkit/templates/` | Spec Delta Log 規格差異日誌範本 |
| `feature-summary.template.md` | `.flowkit/templates/` | Feature Summary 經驗摘要範本 |
| `pr-review-report.template.md` | `.flowkit/templates/` | PR Review 審查報告範本 |
| `pr-description.template.md` | `.flowkit/templates/` | PR Description 範本 |

---

## 快速參考

### 我應該用哪個指令？

| 情境 | 使用指令 |
|------|----------|
| 從 PRD 建立 User Story 與 Milestone | `/flowkit.BDD-Milestone` |
| 抽取 PRD 相關上下文 + 衝突檢測 | `/flowkit.Milestone-context` |
| 取得專案已實作部分的上下文 | `/flowkit.system-context` |
| Plan 完成，確認覆用與整合建議 | `/flowkit.consistency-check` |
| Implement 完成，確認程式碼能跑 | `/flowkit.code-check` |
| 程式碼能跑後，確認 Spec 對齊 | `/flowkit.pre-unify-check` |
| 建立 Spec-Code 追溯索引 | `/flowkit.trace` |
| 合併 Feature 到 System | `/flowkit.unify-flow` |
| 審查品質 + 自動建立 PR | `/flowkit.pr-review` |
| 小幅修正（實作中發現問題） | `/flowkit.refine-loop` |

### 階段對照表

| 階段 | SpecKit 指令 | FlowKit 指令 | 關鍵產出 |
|------|-------------|--------------|----------|
| 需求規劃 | - | BDD-Milestone, Milestone-context | User Stories, Milestone, 設計上下文, 衝突報告 |
| 規格定義 | specify, clarify, plan, tasks | system-context, consistency-check | spec.md, plan.md, tasks.md |
| 實作 | analyze, implement | code-check, refine-loop | 程式碼, 測試, 驗證報告 |
| 驗證合併 | - | pre-unify-check, trace, requirement-sync, unify-flow | 檢查報告, 追溯索引, System 更新 |
| PR 提交 | - | pr-review | PR Review 報告, PR |

### FlowKit 檢查指令比較

| 面向 | consistency-check | code-check | pre-unify-check |
|------|-------------------|------------|------------------|
| 時機 | Plan 後 | Implement 後 | Code Check 後 |
| 檢查對象 | Plan 文件 vs System | 程式碼執行結果 | 實作結果 vs Spec |
| 目的 | 確認覆用、不重做、整合建議 | 確認程式碼能跑、零回歸 | 確認可安全合併 |
| 阻擋性 | 有問題需修正 Plan | L0/L1 FAIL 阻斷 | 有問題需修正實作 |

### 首個 Feature vs 後續 Feature

| 面向 | 首個 Feature | 後續 Feature |
|------|-------------|--------------|
| `system-context` | 可略過（System 尚空） | 需要（理解已實作功能） |
| 衝突檢測 | 通常無衝突 | 需仔細檢查 |
| `consistency-check` | 著重架構建立 | 著重覆用與整合 |

---

## 檔案結構

```
.github/agents/                       # Agent 指令檔（GitHub Copilot）
├── flowkit.BDD-Milestone.agent.md
├── flowkit.code-check.agent.md
├── flowkit.Milestone-context.agent.md
├── flowkit.consistency-check.agent.md
├── flowkit.pre-unify-check.agent.md
├── flowkit.refine-loop.agent.md
├── flowkit.requirement-sync.agent.md
├── flowkit.system-context.agent.md
├── flowkit.trace.agent.md
├── flowkit.unify-flow.agent.md
└── flowkit.pr-review.agent.md

.github/prompts/                      # Prompt 指令檔（GitHub Copilot）
├── flowkit.BDD-Milestone.prompt.md
├── flowkit.code-check.prompt.md
├── flowkit.Milestone-context.prompt.md
├── flowkit.consistency-check.prompt.md
├── flowkit.pre-unify-check.prompt.md
├── flowkit.refine-loop.prompt.md
├── flowkit.requirement-sync.prompt.md
├── flowkit.system-context.prompt.md
├── flowkit.trace.prompt.md
├── flowkit.unify-flow.prompt.md
└── flowkit.pr-review.prompt.md

.cursor/commands/                     # Command 指令檔（Cursor）
├── flowkit.BDD-Milestone.md
├── flowkit.code-check.md
├── flowkit.Milestone-context.md
├── flowkit.consistency-check.md
├── flowkit.pre-unify-check.md
├── flowkit.refine-loop.md
├── flowkit.requirement-sync.md
├── flowkit.system-context.md
├── flowkit.trace.md
├── flowkit.unify-flow.md
└── flowkit.pr-review.md

.flowkit/templates/                   # 範本檔案
├── traceability-index-template.md
├── system-context-template.md
├── system-context-index-template.md
├── Milestone-context-output.template.md
├── Milestone-context-conflict-report.template.md
├── refine-plan.template.md
├── refine-spec-delta.template.md
├── code-check-report.template.md
├── spec-delta-log.template.md
├── feature-summary.template.md
├── pr-review-report.template.md
└── pr-description.template.md

.flowkit/memory/                      # 產出檔案（AI 記憶）
├── system-context.md
└── system-context-index.md

docs/77.flowkit相關文件/              # 功能說明文件
├── README.md（本文件）
├── 功能說明-flowkit.BDD-Milestone.md
├── 功能說明-flowkit.code-check.md
├── 功能說明-flowkit.Milestone-context.md
├── 功能說明-flowkit.consistency-check.md
├── 功能說明-flowkit.pre-unify-check.md
├── 功能說明-flowkit.refine-loop.md
├── 功能說明-flowkit.requirement-sync.md
├── 功能說明-flowkit.system-context.md
├── 功能說明-flowkit.trace.md
├── 功能說明-flowkit.unify-flow.md
└── 功能說明-flowkit.pr-review.md
```
