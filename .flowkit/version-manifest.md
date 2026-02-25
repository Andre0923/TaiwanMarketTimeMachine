# SpecKit + FlowKit 版號清單（Version Manifest）

> **用途**：記錄本範本所有指令化檔案的當前版號與對應 Git Commit  
> **更新時機**：每次修改 Agent / Command / Template / Constitution 後 MUST 同步更新本檔  
> **比對方式**：下游專案或其他範本可將此檔案與自身版本比對，快速識別差異  
> **來源範本**：`99.spec-kit-cross-platform-template`（通用跨平台版）  
> **Repo**：`https://github.com/DrDeer119/99.spec-kit-cross-platform-template.git`  
> **最後更新**：2026-02-25  
> **對應 Commit**：`1c245a2`

---

## FlowKit 指令版號

| 指令 | 版本 | 最後更新 | 對應 Commit | 說明 |
|------|------|----------|-------------|------|
| `flowkit.BDD-Milestone` | 1.5.0 | 2025-07-12 | — | BDD Milestone Builder |
| `flowkit.Milestone-context` | 1.3.0 | 2026-02-01 | — | Milestone 設計上下文擷取 |
| `flowkit.system-context` | 1.4.0 | 2026-02-01 | — | 系統上下文產生 |
| `flowkit.consistency-check` | 1.1.0 | 2026-02-14 | — | Plan 一致性檢查 |
| `flowkit.code-check` | 1.8.0 | 2026-02-16 | `ceb4710` | AI 五層驗證金字塔 |
| `flowkit.refine-loop` | 1.5.0 | 2026-02-16 | `ceb4710` | Debug / 微調 / Bug-Fix |
| `flowkit.pre-unify-check` | 1.2.0 | 2026-02-15 | — | Unify 前置檢查 |
| `flowkit.trace` | 1.0.0 | 2026-01-25 | — | 追溯索引 |
| `flowkit.requirement-sync` | 1.4.0 | 2026-02-15 | — | 需求回寫同步 |
| `flowkit.unify-flow` | 1.4.0 | 2026-02-25 | `1c245a2` | Feature 統合至 System |
| `flowkit.pr-review` | 1.3.0 | 2026-02-15 | — | PR 六維品質審查 |
| `flowkit.system-health` | 1.0.0 | 2025-07-12 | — | 全專案健康檢查 |

## SpecKit 指令版號

| 指令 | 版本 | 最後更新 | 對應 Commit | 說明 |
|------|------|----------|-------------|------|
| `speckit.specify` | 1.1.0 | 2026-02-25 | — | 建立 Feature Spec |
| `speckit.clarify` | 1.1.0 | 2026-02-25 | — | 需求釐清 |
| `speckit.plan` | 1.1.0 | 2026-02-25 | — | 技術規劃 |
| `speckit.tasks` | 1.1.0 | 2026-02-25 | — | 任務拆解 |
| `speckit.analyze` | 1.1.0 | 2026-02-25 | — | 品質分析 |
| `speckit.implement` | 1.5.0 | 2026-02-25 | `1c245a2` | 實作驅動（含 Status 自動管理） |
| `speckit.constitution` | 1.0.0 | 2026-01-21 | — | 憲法管理 |
| `speckit.checklist` | 1.0.0 | 2026-01-21 | — | 生成檢查清單 |
| `speckit.taskstoissues` | 1.0.0 | 2026-01-21 | — | 任務轉 GitHub Issue |

## 範本與規範版號

| 項目 | 版本 | 最後更新 | 對應 Commit | 說明 |
|------|------|----------|-------------|------|
| `constitution.md` | 1.1.0 | 2026-02-25 | `1c245a2` | 專案憲法 |
| `copilot-instructions.md` | 1.0.0 | 2026-01-21 | — | AI 全域規範 |
| `spec-template.md` | 1.1.0 | 2026-02-25 | `1c245a2` | Feature Spec 範本（含 Status） |
| `plan-template.md` | 1.0.0 | 2026-01-21 | — | Plan 範本 |
| `tasks-template.md` | 1.0.0 | 2026-01-21 | — | Tasks 範本 |

---

## 使用方式

### 下游專案版號比對

下游專案在同步更新後，SHOULD 將本檔案複製到專案中，並標記自身版本：

```markdown
<!-- 在下游專案的 .flowkit/version-manifest.md 中 -->
| `flowkit.code-check` | 1.8.0 | ... | ✅ 已同步 |
| `flowkit.refine-loop` | 1.4.0 | ... | ⚠️ 落後（上游 1.5.0） |
```

### 跨範本同步比對

同步前執行比對：
```powershell
# 比對兩邊版號清單
code --diff "$templatePath\.flowkit\version-manifest.md" "$targetPath\.flowkit\version-manifest.md"
```

---

> **備註**：SpecKit 原版指令（specify, clarify, plan, tasks, analyze, implement 等）原始版本無版號標記。  
> 自定義版本統一以 `1.0.0` 為基線，加入自定義功能後遞增至 `1.1.0`。  
> 詳細改版記錄見 `docs/76.改版歷史/`。

---

## 多範本識別說明

本 Manifest 的所有 Commit Hash 皆對應**本範本 Repo**：

| 範本名稱 | Repo | 說明 |
|----------|------|------|
| `99.spec-kit-cross-platform-template` | [DrDeer119/99.spec-kit-cross-platform-template](https://github.com/DrDeer119/99.spec-kit-cross-platform-template) | 通用跨平台版（本檔案來源） |
| `99.eletron-vite-speckit-flowkit` | [DrDeer119/99.eletron-vite-speckit-flowkit](https://github.com/DrDeer119/99.eletron-vite-speckit-flowkit) | Electron Vite 框架版 |

> 跨範本同步時，兩邊的 Manifest 各自記錄各自 Repo 的 Commit Hash。  
> 比對時以**版號（SemVer）**為主要依據，Commit Hash 為輔助追溯用。
