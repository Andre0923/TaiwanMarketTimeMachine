# 功能說明 — flowkit.pr-review

> **版本**：1.4.0  
> **最後更新**：2026-02-28  
> **對應指令檔**：`.cursor/commands/flowkit.pr-review.md` / `.github/agents/flowkit.pr-review.agent.md`

---

## 1. 概述

### 一句話說明

在 Unify Flow 完成後、PR 提交前，以資深架構師視角進行六維程式碼審查，自動產出結構化報告與 PR Description，並依結果自主決策是否提交 PR。

### 解決的問題

| 問題 | 說明 |
|------|------|
| **品質缺口** | `code-check` 管 Runtime 可執行性，但不管程式碼品質、設計、安全性 |
| **PR 準備成本** | 手動撰寫 PR Description 耗時且格式不一 |
| **缺乏 Reviewer 引導** | 人類 Reviewer 不知道該重點關注哪些區域 |
| **全 AI 開發盲點** | AI 產出的程式碼缺少第二雙眼睛的審查 |

### 與現有指令的分工

```
code-check        →  「能跑嗎？測試過嗎？」
pre-unify-check   →  「規格一致嗎？引用正確嗎？」
trace             →  「每條 AC 都有對應程式碼嗎？」
requirement-sync  →  「需求文件同步了嗎？」
unify-flow        →  「System Spec 更新了嗎？」
┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
pr-review     🆕  →  「程式碼品質好嗎？設計合理嗎？安全嗎？可以 PR 嗎？」
┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄
人類 PR 審閱      →  「我同意這個設計決策嗎？」
```

---

## 2. 使用方式

### 基本用法

```
/flowkit.pr-review --default        # 自動偵測 Feature，執行完整審查
/flowkit.pr-review 011              # 指定 Feature 編號
/flowkit.pr-review --skip-security  # 跳過安全性掃描
/flowkit.pr-review --pr-only        # 僅產生 PR Description
```

### 前置條件

| 條件 | 說明 |
|------|------|
| `code-check` PASS | Runtime 品質已確認 |
| Feature Spec 存在 | `specs/features/NNN-*/spec.md` |
| Feature Plan 存在 | `specs/features/NNN-*/plan.md` |
| `gh` CLI 已安裝且已授權 | 自動 PR 建立所需（Phase 0.4 引導安裝/授權） |

### 觸發時機

```
implement → code-check → pre-unify-check → trace → requirement-sync → unify-flow
                                                                          │
                                                                          ▼
                                                                    pr-review ← 此指令
                                                                          │
                                                                     自動 PR / 修正
```

---

## 3. 審查六維金字塔

### 3.1 金字塔結構

```
         ╱╲
        ╱  ╲     D6：SDD 合規性
       ╱ D6 ╲    ← 規格流程完整性
      ╱──────╲
     ╱        ╲   D5：安全性
    ╱   D5     ╲  ← 注入、暴露、硬編碼
   ╱────────────╲
  ╱              ╲  D4：跨 Feature 影響
 ╱      D4       ╲  ← System 衝突、副作用
╱────────────────╲
╲                ╱  D3：架構設計
 ╲      D3     ╱  ← 模組邊界、耦合
  ╲──────────╱
   ╲        ╱  D2：程式碼品質
    ╲ D2  ╱  ← 命名、複雜度、重複
     ╲──╱
      ╲╱  D1：變更摘要
       ── ← PR Description 產生
```

### 3.2 各面向說明

| 面向 | 檢查內容 | 嚴重性範圍 |
|------|----------|------------|
| **D1 變更摘要** | 檔案清單、動機、US 覆蓋率、PR Description | — |
| **D2 程式碼品質** | 檔案長度、函式複雜度、命名、Docstring、Dead Code | LOW-HIGH |
| **D3 架構設計** | 單一職責、介面-邏輯分離、耦合度、設計決策 | MEDIUM-CRITICAL |
| **D4 跨 Feature 影響** | System 衝突、共用模組、API 相容性、資料模型 | HIGH-CRITICAL |
| **D5 安全性** | 敏感資料暴露、硬編碼憑證、輸入驗證、路徑穿越 | HIGH-CRITICAL |
| **D6 SDD 合規性** | 流程完整性、Test-First、@spec 註解、Traceability | MEDIUM-HIGH |

---

## 4. 阻擋規則與品質等級

### 4.1 嚴重性與阻擋（成本優先）

| 嚴重性 | 阻擋 PR | Quick-Fix / Moderate | Heavy |
|--------|---------|---------------------|-------|
| 🔴 CRITICAL | ✅ 阻擋（僅 Heavy） | ✅ 直接修正 | 🔴 NOT READY → refine-loop |
| 🟠 HIGH | ✅ 阻擋（僅 Heavy） | ✅ 直接修正 | 🔴 NOT READY → refine-loop |
| 🟡 MEDIUM | ⚠️ 警告（僅 Heavy） | ✅ 直接修正 | 🟠 CAUTION → refine-loop |
| 🟢 LOW | ❌ 不阻擋 | ✅ 直接修正 | Tech Debt → 放行 |

### 4.2 品質等級

| 等級 | 條件 | AI 決策 |
|------|------|---------|
| **A（優秀）** | 0 C/H/M，≤2 LOW | 🟢 成本評估 LOW → 直接修正 / Tech Debt → PR |
| **B（良好）** | 0 C/H，≤3 M，≤5 LOW | 🟠 成本評估 → Quick-Fix/Moderate 直接修正；Heavy M → refine-loop |
| **C（可接受）** | 0 C，≤2 H，≤5 M | 🔴 成本評估 → Quick-Fix/Moderate 直接修正；Heavy → refine-loop |
| **D（需改善）** | ≤2 C 或 >2 H 或 >5 M | ⛔ 建議回到 implement |
| **F（需重新規劃）** | >2 C 或架構性問題 | ⛔ 建議回到 plan/specify |

### 4.3 AI 自主決策流程（成本優先）

```
使用 pr-review ＝ 人類已決定要 PR
         │
    六維審查完成
         │
    品質等級判定
         │
    ──── 成本評估（所有嚴重性）────
         │
    ┌────┴────────────┬───────────┐
    │                  │             │
 Quick-Fix/         Heavy          D/F 等級
 Moderate           成本
    │                │              │
  直接修正       依嚴重性分流    建議回到
    │            ┌───┴───┐    plan/specify
  重跑         C/H/M    LOW      詢問人類
 pr-review     │        │       確認
             refine   Tech
             -loop    Debt
               │        │
               └──┬───┘
                  │
             🟢 PR（若無 Heavy C/H/M）
```

---

## 5. 產出物

| 產物 | 路徑 | 用途 |
|------|------|------|
| 審查報告 | `.artifacts/pr-review-report-{FEATURE_ID}.md` | 完整六維審查結果 |
| PR Description | `.artifacts/pr-description-{FEATURE_ID}.md` | 可直接用於 PR 的描述文件 |
| Tech Debt 登錄 | `docs/technical-debt.md` | LOW 放行項目登錄（僅有放行時） |
| PR URL | GitHub PR | 🟢 READY 時自動建立 |

---

## 6. 核心特色

### 6.1 比傳統 Code Review 更積極

- AI 開發時間大幅縮短 → **不需要為時間成本而放棄品質**
- 所有嚴重性問題皆先評估修正成本，**低成本問題當場修正**
- 僅有 Heavy 成本的 CRITICAL/HIGH/MEDIUM 才交由 refine-loop，**最大化即時修正比例**

### 6.2 全 AI 開發品質守門

- AI MUST 評估整體品質是否低落到需要**回溯至更早階段**
- 品質 D 等級 → 建議回到 `implement`
- 品質 F 等級 → 建議回到 `plan` 或 `specify`
- AI 直接決策並提出最佳建議，以利全 AI 開發作業

### 6.3 成本優先智慧判斷

- 所有嚴重性問題皆先評估修正成本（Quick-Fix / Moderate / Heavy）
- Quick-Fix（≤5 行）與 Moderate（6-20 行）→ AI 當場直接修正
- Heavy（>20 行）→ CRITICAL/HIGH/MEDIUM 交 refine-loop；LOW 登錄至 `docs/technical-debt.md`（TD-XXX 格式）

### 6.4 PR 建立三層策略

| 策略 | 前提 | 行為 |
|--------|------|------|
| **A — 全自動** | gh 已安裝 + 已授權 | commit → push → `gh pr create` → 回報 PR URL |
| **B — 引導後接續** | gh 已安裝但未授權 | commit + push → 引導 `gh auth login` → 授權後自動建 PR |
| **C — 手動輔助** | gh 不可用 | commit + push → 輸出 Compare URL + PR Description 供複製 |

---

## 7. 與團隊規模的適配

| 場景 | 核心價值 |
|------|----------|
| **個人開發** | AI 作為虛擬 Reviewer，補足無人類 Reviewer 的缺口 |
| **小型團隊** | 結構化報告減少 Review 時間，Reviewer Focus Areas 引導新手 |
| **中大型團隊** | 標準化 Review 流程，CRITICAL 自動攔截減少 Reviewer 負擔 |

---

## 8. FAQ

### Q：pr-review 和 code-check 有什麼不同？

| 面向 | code-check | pr-review |
|------|------------|-----------|
| 時機 | implement 後 | unify-flow 後 |
| 焦點 | Runtime 可執行性 | 程式碼品質 + 設計 |
| 執行方式 | 實際跑測試 | 靜態分析 + 架構審查 |
| 產出 | 驗證報告 | 審查報告 + PR Description |

### Q：一定要用 pr-review 嗎？

SHOULD 執行，但非強制（MUST）。個人專案可選擇跳過，但團隊開發強烈建議使用。

### Q：品質 F 等級時，真的要回到 plan 嗎？

AI 會提出建議，但最終由人類決定。AI 的建議是基於架構性問題的普遍程度判斷。

---

## 9. Phase 7.6 TD Closure Verification（TD 結案一致性驗證）

> ℹ️ **v1.2.0 新增**：PR Review 時驗證 TD 結案一致性

**目的**：在 PR 提交前驗證 TD 結案狀態的一致性，作為 unify-flow Phase 7 的驗證閘門。

**觸發條件**：
- `docs/technical-debt.md` 存在
- 若不存在 → 跳過

**驗證方式**：

| 方向 | 邏輯 | 輸出等級 |
|------|------|----------|
| **正向驗證** | spec.md 有 `> TD Ref: TD-XXX` 但該 TD 仍為 Open | ⚠️ WARNING |
| **反向驗證** | PR diff 修改了 Open TD 的 Component 相關程式碼，但 TD 未結案 | ℹ️ INFO |

**強度等級**：SHOULD（僅產生 WARNING/INFO，不阻擋 PR 建立）

**與 unify-flow Phase 7 的關係**：
- unify-flow Phase 7 是唯一的 TD 結案通道
- pr-review Phase 7.6 僅負責驗證，不修改 TD Registry
- 若 WARNING 出現，建議回到 unify-flow 補執行 Phase 7

---

## 版本歷史

| 版本 | 日期 | 說明 |
|------|------|------|
| 1.4.0 | 2026-02-28 | 成本優先分流架構：所有嚴重性問題皆先評估修正成本，Quick-Fix/Moderate 直接修正、Heavy 依嚴重性分流（Issue #12） |
| 1.2.0 | 2026-02-15 | 新增 Phase 7.6 TD Closure Verification：PR Review 時驗證 TD 結案一致性（正向/反向驗證） |
| 1.1.0 | 2026-02-12 | Phase 0.4 PR Tool Readiness（gh 安裝/授權檢查）、Phase 7.5 Tech Debt 明確登錄流程、Phase 8.4 三層 PR 建立策略 |
| 1.0.0 | 2026-02-11 | 初版：六維審查 + PR Description + AI 自主決策 |
