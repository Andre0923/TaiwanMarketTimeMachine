# FlowKit Refine Loop 功能說明

> **指令名稱**：`/flowkit.refine-loop`  
> **Agent 檔案**：`.github/agents/flowkit.refine-loop.agent.md`  
> **相關目錄**：`FEATURE_DIR/.refine/RC<NNN>/`（產物儲存）

---

## 1. 功能概述

### 1.1 這是什麼？

`/flowkit.refine-loop` 是一個**縮小版的 SpecKit 流程**，用於在 SpecKit 主流程已完成後，進行「debug / 微調 / 規格修正」的一次性處理，維持 spec.md / plan.md / tasks.md / code 的一致性。

### 1.2 解決什麼問題？

| 問題 | 解決方式 |
|------|----------|
| Bug 修正後規格不同步 | 強制 spec/plan/tasks/code 一致性 |
| 小幅調整要跑完整 SpecKit 太重 | 輕量化流程，單一指令完成 |
| 補丁式修補造成規格漂移 | 組件化更新，完整區塊處理 |
| 修改後難以追溯 | 產生可追蹤的 Change Set（RC001...） |
| 跨 Feature 的 bug 被 AI 拒絕修正 | BUGFIX 模式不受 Feature 邊界限制，任何位置的 bug 皆可修正 |
| UI 微調要走完整 SDD 流程太重 | UI_ADJUST 分類以輕量流程處理呈現層調整，同步更新 spec UI 描述 + 產出 ui-change-record.md 供 unify-flow 消費 |
| 跳過測試直接改 code | 強制 Test-First 原則 |

### 1.3 核心價值

```
「小幅修正也要維持規格一致性，先 Change Set → 再 delta → 再合併回主檔」
```

---

## 2. 使用時機

### 2.1 何時使用 Refine Loop？

**適用情境**：
- SpecKit 主流程已完成（specify → plan → tasks → implement）
- 發現 Bug 需要修正（**BUGFIX 模式不限於當前 Feature 範圍**）
- 需要微調行為或參數
- 需求小幅變更（< 5 個新 US）
- **UI 呈現層調整**（版面配置、樣式微調、互動細節、RWD、a11y——功能不變，僅調整呈現）
- **code-check 產出的 Bug-Fix 清單**（非功能回歸的 EASY/MEDIUM 修復，自動以 `--default` 模式接收）
- **pr-review 回報 NOT READY 或 REVIEW WITH CAUTION**（CRITICAL/HIGH/MEDIUM 問題，自動以 `--default` 模式接收）

**不適用情境**（改用完整 SpecKit）：
- 新增 User Stories > 5 個
- SPEC_CHANGE 類 RC > 5 個（BUGFIX 不計入）
- 涉及架構性變更（換框架、換 DB、大型外部整合）

### 2.2 在流程中的位置

```
/speckit.specify → /speckit.plan → /flowkit.consistency-check
                                            │
                                            ▼
                 /speckit.tasks → /speckit.implement
                                            │
                                            ▼
                              /flowkit.code-check
                                            │
                         ┌──────────────────┤
                         │                  │
                      ❌ FAIL            ✅ PASS
                         │                  │
                         ▼                  ▼
              /flowkit.refine-loop    /flowkit.pre-unify-check
              （修復後重跑                     │
               code-check）                  │
                         │                  ▼
                         │        /flowkit.trace
                         │                  │
                         │                  ▼
                         │      /flowkit.requirement-sync
                         │                  │
                         │                  ▼
                         │           /flowkit.unify-flow
                         │                  │
                         └──────────────────┤
                                            ▼
                                        準備發 PR
```
                                        準備發 PR
```

---

## 3. 輸入與輸出

### 3.1 輸入

| 來源 | 必要性 | 說明 |
|------|--------|------|
| 變更描述 | REQUIRED | 使用者輸入的修正需求 |
| `FEATURE_DIR/spec.md` | REQUIRED | 現有規格 |
| `FEATURE_DIR/plan.md` | REQUIRED | 現有計畫 |
| `FEATURE_DIR/tasks.md` | REQUIRED | 現有任務清單 |
| `src/` + `tests/` | REQUIRED | 現有實作與測試 |
| Constitution | OPTIONAL | `.specify/memory/constitution.md` |

### 3.2 輸出

| 產出 | 位置 | 說明 |
|------|------|------|
| **context.json** | `.refine/RC<NNN>/` | 執行上下文 |
| **change-set.md** | `.refine/RC<NNN>/` | 變更清單 |
| **candidates.md** | `.refine/RC<NNN>/` | 候選區段 |
| **refine-spec-delta.md** | `.refine/RC<NNN>/` | 規格變更片段 |
| **refine-plan.md** | `.refine/RC<NNN>/` | 精簡計畫 |
| **refine-analysis.md** | `.refine/RC<NNN>/` | 分析報告 |
| **ui-change-record.md** | `.refine/RC<NNN>/` | UI 變更記錄（僅 UI_ADJUST 時產出） |
| **spec.md** | `FEATURE_DIR/` | 更新後的規格（合併後） |
| **plan.md** | `FEATURE_DIR/` | 更新後的計畫（合併後） |
| **tasks.md** | `FEATURE_DIR/` | 更新後的任務（新增區段） |
| **src/ + tests/** | 專案目錄 | 更新的程式碼與測試 |

---

## 4. Change 分類系統

### 4.1 雙層分類

每個 RC 變更必須同時標記 **Type** 和 **Classification**。

#### Type（變更型態）

| Type | 說明 | 範例 |
|------|------|------|
| **[NEW]** | 新增 User Story / AC | 新增使用者登出功能 |
| **[MODIFIED]** | 修改現有 User Story / AC | 調整密碼長度限制 |
| **[DELETED]** | 刪除 User Story / AC | 移除舊版 API |
| **[FIXED]** | 修正錯誤（AC 沒錯，實作錯了） | 修正登入失敗訊息 |

#### Classification（變更性質）

| Classification | 說明 | 處理策略 |
|----------------|------|----------|
| **BUGFIX** | spec 正確，實作錯了 | 以 tests + code 修正為主；spec 只補充澄清 |
| **SPEC_CHANGE** | 需求/行為改變 | 先更新 spec → 再更新 plan/tasks → 再改 code/tests |
| **REFACTOR** | 不改外部行為 | spec 不變；plan/tasks 可更新；以測試保護行為 |
| **UI_ADJUST** | 功能正確，UI 呈現需調整 | 更新 spec 中 AC 的 UI 描述 → 產出 ui-change-record.md → 再改 UI code/tests |

**邊界案例**：若 spec 未定義該行為，預設歸類為 **SPEC_CHANGE**。

**UI_ADJUST 邊界**：若 UI 調整過程中發現需要新增 AC 或修改行為邏輯 → 自動升級為 **SPEC_CHANGE**。適用範圍：CSS/styling、版面配置、元件視覺微調、互動細節、RWD、a11y。

---

## 5. 執行流程

```
┌──────────────────────────────────────────────────────────────┐
│                    /flowkit.refine-loop                       │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  ⚡ Activation Gate（意圖分類 + 啟動確認）                      │
│  • 提問 → 直接回答（不進入 Phase）                          │
│  • 修正需求 → MUST 輸出啟動確認，鎖入 Phase 0-8           │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 0：Gatekeeper（前置條件 + 資料健康檢查）               │
│  • 確認 Feature 目錄存在                                      │
│  • 確認實作存在                                               │
│  • 建立 .refine/RC<NNN>/ 工作目錄                            │
│  • 載入 Constitution                                         │
│  • 產出：context.json                                        │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 1：Build Change Set                                    │
│  • 拆分為可執行變更單元（RC001, RC002...）                    │
│  • 標記 Type + Classification                                │
│  • 檢查 Scope Threshold                                      │
│  • 產出：change-set.md                                       │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 2：Progressive Scan（只定位，不深改）                  │
│  • Stage 1 掃描：spec.md / plan.md / tasks.md                │
│  • 取得 max(T###)                                            │
│  • 標記候選區段                                               │
│  • 產出：candidates.md                                       │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 3：Generate refine-spec-delta.md                       │
│  • Stage 2 深讀（僅「待深讀」區段）                            │
│  • 產生變更規格片段                                           │
│  • 使用 BDD 格式（Given/When/Then）                          │
│  • 產出：refine-spec-delta.md                                │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 4：Generate refine-plan.md                             │
│  • 識別技術影響                                               │
│  • 設計產物更新（data-model / contracts / flows）            │
│  • Constitution Compliance 檢查                              │
│  • Observability & Logging 規劃                              │
│  • 產出：refine-plan.md                                      │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 5：Update tasks.md                                     │
│  • 延續 T### 編號，帶 [RC<NNN>] 標記                          │
│  • Test-First 原則：tests/ 任務先於 src/ 任務                 │
│  • 直接附加至 tasks.md                                        │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 6：Refine Analyze（最多 3 次迭代）                     │
│  • 檢測通道 A-G                                               │
│  • 嚴重性分配                                                 │
│  • CRITICAL/HIGH → 返回修正                                  │
│  • 產出：refine-analysis.md                                  │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 7：Implement & Validate                                │
│  • 依 tasks.md 順序執行                                       │
│  • Test-First：先寫測試再實作                                 │
│  • 禁止使用 print，必須使用 logging                           │
│  • 完成的任務勾選                                             │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 8：Merge Back（回寫主檔）                              │
│  • 合併 refine-spec-delta.md 回 spec.md                      │
│  • 合併必要內容回 plan.md                                     │
│  • 移除所有變更標記                                           │
│  • 保留 .refine/RC<NNN>/ 追溯紀錄                            │
│  • 更新 context.json status 為 "merged"                      │
└──────────────────────────────────────────────────────────────┘
```

---

## 6. 各 Phase 詳細說明

### Phase 0：Gatekeeper

**目的**：確保前置條件滿足，建立工作目錄

**檢查項目**：
- `spec.md` 存在且包含至少 1 個 User Story
- `plan.md` 存在且包含技術棧定義
- `tasks.md` 存在且包含 T### 格式任務
- `src/` 與 `tests/` 有對應實作
- 使用者輸入非空白
- 若 `.artifacts/code-check-report-feature-*.md` 存在，讀取作為問題來源參考
- 若前兩層未觸發，檢查 `.artifacts/pr-review-report-*.md`：
  - 🔴 NOT READY / 🟠 REVIEW WITH CAUTION → 讀取 CRITICAL/HIGH/MEDIUM 問題作為變更描述來源
  - 🟢 READY FOR PR → 不觸發

**產出**：`context.json`
```json
{
  "feature_dir": "<path>",
  "rc_id": "RC001",
  "status": "draft",
  "available_docs": ["spec.md", "plan.md", "tasks.md", ...],
  "constitution_loaded": true,
  "timestamp": "2026-01-25T10:00:00Z"
}
```

### Phase 1：Build Change Set

**目的**：將變更需求拆分為可追蹤的單元

**產出**：`change-set.md`
```markdown
# Change Set — RC001

| RC ID | Type | Classification | Impact | UI Impact | Risk | Summary |
|-------|------|----------------|--------|-----------|------|---------|
| RC001 | [MODIFIED] | SPEC_CHANGE | spec, code, tests | None | Med | 調整密碼長度 |

## Scope Check
- [NEW] count: 0 ✅ (< 5)
- Total RC count: 1 ✅ (< 6)
- Architecture change: No ✅
```

**Scope Threshold**（超過即 STOP）：
- 新增 User Stories > 5
- SPEC_CHANGE 類 RC > 5（BUGFIX、UI_ADJUST 不計入）
- UI_ADJUST 類 RC > 10
- 涉及架構性變更
- 涉及檔案數 > 20（含所有類型合計）

### Phase 2：Progressive Scan

**目的**：定位受影響區段，取得任務 ID 脈絡

**關鍵輸出**：
- 候選區段對應表
- 最大 Task ID（用於 Phase 5）

**產出**：`candidates.md`
```markdown
## Tasks Context
- Max Task ID: T046
- Next Task ID: T047
```

### Phase 3：Generate Spec Delta

**目的**：產生規格變更片段（僅變更部分）

**規則**：
- 只包含「受影響的 User Stories」區塊
- 每個變更必須標記 `[NEW] [MODIFIED] [DELETED] [FIXED]`
- 使用 BDD 格式（Given/When/Then）
- 不重寫未受影響的 spec 章節

### Phase 4：Generate Plan

**目的**：產生精簡計畫，識別技術影響

**包含項目**：
- 變更摘要
- 技術決策（若有新決策）
- 設計產物更新（data-model / contracts）
- Constitution Compliance 對照
- Observability & Logging 規劃
- UI/UX 變更（若 UI Impact ≠ None）

### Phase 5：Update Tasks

**目的**：新增任務至 tasks.md

**關鍵規則**：
- 延續 T### 編號，帶 `[RC<NNN>]` 標記
- **Test-First**：同 RC 區塊內，`tests/` 任務必須在 `src/` 任務前
- 每個 RC 至少包含：Tests、Implementation、Verify

**任務格式**：
```
- [ ] T### [RC<NNN>] [US?] <動作描述> <檔案路徑>
```

### Phase 6：Refine Analyze

**目的**：一致性與覆蓋檢查

**檢測通道（A-G）**：

| 通道 | 檢測內容 |
|------|----------|
| A. Duplication | 變更之間是否衝突；[NEW] 是否與現有功能重複 |
| B. Ambiguity | AC 是否可測試、可驗證 |
| C. Underspecification | 是否有遺漏的 AC 或邊界條件 |
| D. Constitution Alignment | 是否符合憲法 MUST 原則 |
| E. Coverage Gaps | 每個 AC 是否有對應任務 |
| F. Inconsistency | 術語使用是否一致 |
| G. UI Consistency | UI ID 存在性、狀態覆蓋（僅 UI Impact ≠ None 時） |

**迭代規則**：
- CRITICAL/HIGH → 返回 Phase 1-5 修正
- 最多 3 次迭代
- 超過 → STOP「需要人工決策」

### Phase 7：Implement & Validate

**目的**：依任務執行實作與測試

**關鍵規則**：
- 優先 Tests → Implementation → Verify
- **禁止使用 print**，必須使用 logging 模組
- 不得以「快速 workaround」破壞架構一致性
- **新增/修改的程式碼必須包含 @spec 註解**（維持 Traceability）
- 完成的任務勾選（`- [x]`）

**UI 模擬驗證**（當 Change Set 涉及 UI 變更時）：
- 觸發條件：Classification = UI_ADJUST，或任一 RC 的 UI Impact ≠ None
- 依優先順序：專案 E2E 測試 → CDP 即時互動驗證 → Browser 工具手動驗證
- 截圖存放：`.artifacts/refine-ui-verify-<RC-ID>.png`
- 若不可行 → 記錄 Escalation Log

**@spec 註解要求**：
```python
# @spec US2 (001-feature/spec.md#user-story-2)
# @spec-ac AC2.1, AC2.2
def login(email: str, password: str) -> bool:
    ...
```

### Phase 8：Merge Back

**目的**：合併回主檔，維持單一真相

**合併規則**：
- 以「完整 User Story 區塊」為單位更新
- [NEW] → 插入適當位置
- [MODIFIED] / [FIXED] → 替換對應區段
- [DELETED] → 移除對應區段
- **移除所有變更標記**

**關鍵**：
- **不刪除** `.refine/RC<NNN>/` 目錄（保留追溯）
- 更新 `context.json` status 為 `"merged"`
- 若 Change Set 含 UI_ADJUST，產出 `ui-change-record.md` 記錄 Before/After/Reason/UI ID，標記 Unify-Flow 待同步項目

---

## 7. 四條核心憲法

> 來源：Operational Constraints 精華

| 原則 | 說明 |
|------|------|
| **Single Source of Truth** | 永遠合併回主檔，不留 refine-*.md 孤兒 |
| **Atomic Consistency** | 行為改變必須有 spec 覆蓋；BUGFIX = 讓 code 符合 spec；SPEC_CHANGE = 先改 spec 再改 code；UI_ADJUST = 更新 spec UI 描述 + 產出 ui-change-record.md |
| **Test-First** | 必須先產生/更新測試，再產生/更新實作 |
| **Logging** | 任何邏輯變更必須確保可觀測性（新分支/錯誤要有 log） |

---

## 8. 完成標準（Definition of Done）

```markdown
## Refine Loop DoD

- [ ] spec.md / plan.md / tasks.md 已合併回寫且一致
- [ ] tasks.md 任務格式符合 SpecKit（T###、[RC<NNN>]、checkbox、檔案路徑）
- [ ] refine-analysis.md 無 CRITICAL/HIGH
- [ ] 受影響行為已具備測試覆蓋
- [ ] Observability & Logging 已落地
- [ ] .refine/RC<NNN>/ 留存完整追溯
  - BUGFIX 模式：delta 與 plan MAY 以最小化驗證記錄替代
  - UI_ADJUST 模式：delta MUST 包含 UI 描述更新；ui-change-record.md MUST 產出
- [ ] 無變更標記殘留於 spec.md
- [ ] 無 TODO/FIXME 殘留於程式碼
- [ ] 新增/修改的程式碼包含 @spec 註解（維持 Traceability）
- [ ] （若 Feature 有 traceability-index.md）建議執行 `/flowkit.trace` 更新追溯索引
- [ ] 建議重跑 `/flowkit.code-check` 驗證修復結果
```

---

## 9. 使用範例

### 9.1 基本使用

```
/flowkit.refine-loop 調整密碼長度從 6 改為 8，並修正登入失敗訊息顯示錯誤
```

### 9.2 執行結果摘要

```markdown
# Refine Loop Result — RC001

## Status
- Overall: ✅ Success
- Iterations: 1
- Scope: Within threshold
- Merged back: Yes
- context.json status: merged

## Summary
- Change Requests Parsed: 2
- Change Set Items: 2
- Classification Breakdown: BUGFIX=1, SPEC_CHANGE=1

## Change Set (RC Items)
| RC ID | Type | Classification | Impact | Risk | Summary |
|-------|------|----------------|--------|------|---------|
| RC001 | [MODIFIED] | SPEC_CHANGE | spec, code, tests | Med | 調整密碼長度 |
| RC002 | [FIXED] | BUGFIX | code, tests | Low | 修正登入失敗訊息 |

## DoD Checklist
- [x] spec.md / plan.md / tasks.md 已合併回寫且一致
- [x] tasks.md 任務格式符合 SpecKit
- [x] refine-analysis.md 無 CRITICAL/HIGH
- [x] 受影響行為已具備測試覆蓋
- [x] .refine/RC001/ 留存完整追溯（BUGFIX 模式：delta / plan MAY 為最小化記錄）
- [x] 無變更標記殘留於 spec.md
```

---

## 10. 與其他指令的關係

### 10.1 比較：Refine Loop vs 完整 SpecKit

| 項目 | Refine Loop | 完整 SpecKit |
|------|-------------|--------------|
| 適用情境 | 小幅調整、Bug 修正 | 新功能開發、大改版 |
| 規模限制 | < 5 NEW、< 6 RC | 無限制 |
| 產物位置 | `.refine/RC<NNN>/` | Feature 目錄 |
| 合併回主檔 | 是（Phase 8） | 否（由 Unify Flow 處理） |
| 追溯保留 | `.refine/` 目錄 | `specs/history/` |

### 10.2 與 Trace 的關係

**執行 Refine Loop 後**：
- 若有新增程式碼檔案 → **必須**加入 `@spec` 註解
- 若有修改程式碼 → 確認既有 @spec 註解是否需要更新
- 若需要更新追溯索引 → 可重新執行 `/flowkit.trace`
- Refine Loop 本身**不自動執行** trace，但 DoD 建議在有追溯索引時更新

**@spec 註解格式**：
```python
# @spec US{N} ({feature-id}/spec.md#user-story-{n})
# @spec-ac AC{N}.{M}, AC{N}.{K}
```

### 10.3 流程選擇指南

```
┌──────────────────────────────────────────────────────────────┐
│  需要做什麼變更？                                             │
└──────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
         Bug 修正        小幅調整        新功能開發
         (< 3 項)        (< 5 US)       (> 5 US)
              │               │               │
              ▼               ▼               ▼
      /flowkit.refine   /flowkit.refine    完整 SpecKit
         -loop             -loop            流程
              │               │
              │      ┌───────┴───────┐
              │      │               │
              │      ▼               ▼
              │  UI 微調        行為微調
              │  (UI_ADJUST)    (SPEC_CHANGE)
```

---

## 11. 常見問題 FAQ

### Q1：什麼時候該用 Refine Loop，什麼時候該跑完整 SpecKit？

**A**：
- **Refine Loop**：Bug 修正、參數微調、小幅需求變更（< 5 個新 US）
- **完整 SpecKit**：新功能開發、架構變更、大規模需求調整

### Q2：Refine Loop 會修改 traceability-index.md 嗎？

**A**：不會自動修改。若變更涉及新檔案或 User Story 對應關係改變，建議手動更新或重新執行 `/flowkit.trace`。

### Q3：為什麼要保留 `.refine/RC<NNN>/` 目錄？

**A**：用於追溯。即使已合併回主檔，這些檔案記錄了變更的完整歷程，方便日後回顧。

### Q4：Scope Threshold 超過了怎麼辦？

**A**：系統會 STOP 並建議改跑完整 SpecKit。這表示變更規模已超出「微調」範疇。

### Q5：Phase 6 迭代超過 3 次怎麼辦？

**A**：系統會 STOP 並報告「需要人工決策」，此時需要人工檢視問題並決定處理方式。

### Q6：可以不執行 Phase 7 實作嗎？

**A**：不建議。但如果變更類型明確為「純文件修正且不影響行為」，可以跳過。一般情況下，必須完成實作與測試。

### Q7：Bug 屬於其他 Feature 時，Refine Loop 能修嗎？

**A**：可以。BUGFIX 模式下（spec 正確、code 錯誤），程式碼修正範圍不受 Feature 邊界限制。AI 不得以「此 bug 屬於其他 Feature」為由拒絕修正。若診斷後發現需要修改 spec，則自動升級為 SPEC_CHANGE，回歸 Feature 範疇規則。

### Q8：UI 微調（版面、樣式、互動細節）可以用 Refine Loop 嗎？

**A**：可以。使用 UI_ADJUST Classification。適用於功能已穩定但呈現層需調整的情境（CSS/styling、版面配置、元件視覺、互動細節、RWD、a11y）。spec.md 中 AC 的 UI 描述會同步更新，並產出 `ui-change-record.md` 供 unify-flow 將變更同步至 `specs/system/ui/*`。若調整過程中發現需新增 AC 或改變行為，則自動升級為 SPEC_CHANGE。

---

## 12. 錯誤處理

| 情境 | 嚴重性 | 處理方式 |
|------|--------|----------|
| 缺少 spec/plan/tasks | CRITICAL | STOP + 指示先完成 SpecKit 主流程 |
| Scope Threshold 超出 | CRITICAL | STOP + 建議改跑完整 SpecKit |
| 變更需求互相衝突 | HIGH | STOP + 列出衝突與決策選項 |
| 無法定位影響範圍 | HIGH | 回報缺口 + 列出澄清點 |
| Analyze 迭代超過 3 次 | CRITICAL | STOP + 請求人工決策 |
| 資料不足無法判斷 | HIGH | STOP + 列出需澄清項 |
| 任務格式不合規 | HIGH | ERROR + 提供修正指示 |

---

## 13. Escalation Log 格式

**用途**：記錄所有深讀操作，確保可審計

```markdown
| Seq | Phase | Trigger | File | Range | Why Needed | Key Findings | Decision / Next Step |
|-----|-------|---------|------|-------|------------|--------------|----------------------|
| 1 | Phase 3 | 產生 [MODIFIED] | spec.md:US2 | L50-80 | 需了解現有 AC | 密碼長度=6 | 更新 AC |
| 2 | Phase 4 | 識別技術影響 | plan.md | L20-40 | 確認技術棧 | 使用 bcrypt | 維持現有 |
```

---

## 14. 版本歷史

| 版本 | 日期 | 變更說明 |
|------|------|----------|| 2.3.0 | 2026-03-05 | Activation Gate 工具呼叫防護（Issue #20）：新增 ⛔ 工具呼叫前強制閘門（即將呼叫 file-mutation 工具且目標含 src/ 或 tests/ 時，必先確認本次對話已輸出啟動確認，否則立即 STOP）；Step 2.5 加入第三個自我検核問句（未啟動卻即將呼叫 file-mutation 工具 → 立即 STOP 回 Step 1） || 2.2.0 | 2026-04-01 | Activation Gate 強化（Issue #18）：將 Gate 移至 prompt 首位（User Input 後，優先於一切 Phase）；新增 Step 2.5 即時流程確認（輸出啟動確認後必須立即進入 Phase 0）；新增 ❌/✅ 反模式/正確流程示範；在 Operating Constraints MUST NOT 新增 Anti-Pattern Ad-hoc Fix 禁令（Phase 0-5 未完成前不得修改 src/tests） |
| 2.1.0 | 2026-03-02 | Phase 7 UI 模擬驗證（Issue #17）： UI_ADJUST 模式 Phase 7 新增實際 UI 渲染驗證，支援 Browser 工具串揥； Phase 7 三通道設計（Browser 驗證 / 政策限制讓步） |
| 2.0.0 | 2026-03-02 | UI_ADJUST Classification：新增第四種變更分類「UI_ADJUST」，適用於功能穩定但 UI 呈現層需調整的情境；同步更新 spec.md 中 AC 的 UI 描述 + Phase 8 產出 ui-change-record.md 供 unify-flow 消費；獨立 Scope 門檻（> 10 RC）；Phase 6 G 通道優先；Phase 4 plan 可最小化；安全邊界：需新增 AC 或改行為時自動升級為 SPEC_CHANGE |
| 1.9.0 | 2026-03-02 | Cross-Feature BUGFIX 範圍：BUGFIX 模式下程式碼修正不受 Feature 邊界限制，不得以「屬於其他 Feature」拒絕修正；新增 Operating Constraints Cross-Feature BUGFIX 子章節；Phase 0 Bug-Fix 模式新增跨 Feature 條款；Phase 2 spec 掃描改為可選；Progressive Disclosure BUGFIX 模式例外 |
| 1.8.0 | 2026-03-02 | Activation Gate 機制：強制意圖分類（提問/修正需求）+ 啟動確認輸出 + 流程鎖定，防止 AI 滑入 ad-hoc 修復模式；核心口訣提前至 Phase 0 前；DoD 新增 BUGFIX 模式例外條款（Issue #14/#16） |
| 1.7.0 | 2026-03-01 | Scope Threshold 改為僅計算 SPEC_CHANGE 類 RC（≤ 5），BUGFIX 類 RC 不計入閾值（仍受檔案數 ≤ 20 保護）；Phase 1 Scope Check 輸出格式更新為分離顯示 SPEC_CHANGE / BUGFIX 計數（Issue #13） |
| 1.6.0 | 2026-02-27 | PR-Review 修復模式：`--default` 新增第三層偵測 `.artifacts/pr-review-report-*.md`，若狀態為 NOT READY / REVIEW WITH CAUTION 則讀取 CRITICAL/HIGH/MEDIUM 問題作為變更描述來源；Phase 0 新增步驟 7 pr-review 報告偵測（Issue #10） |
| 1.5.0 | 2026-02-16 | Bug-Fix 模式：`--default` 新增 bug-fix-list 優先讀取、Phase 0 自動切換 Bug-Fix 模式、支援 code-check 非功能回歸分流 |
| 1.4.0 | 2026-02-08 | 報告命名統一：`verify-report-feature-*` → `code-check-report-feature-*` |
| 1.3.0 | 2026-02-03 | Handoff 重構（移除 trace、新增 code-check + pre-unify-check）、--default 模式、Phase 0 整合 code-check 報告、Scope 檔案數門檻 |
| 1.2.0 | 2026-01-25 | 初始文件版本 |

---

## 15. 檔案位置索引

| 類型 | 位置 |
|------|------|
| Agent 指令檔 | `.github/agents/flowkit.refine-loop.agent.md` |
| Refine 產物 | `FEATURE_DIR/.refine/RC<NNN>/` |
| 本功能說明 | `flowkit/docs/功能說明-flowkit.refine-loop.md` |

---

## 16. 關鍵規則速查

| 規則 | 說明 |
|------|------|
| 雙層分類 | Type（NEW/MODIFIED/DELETED/FIXED）+ Classification（BUGFIX/SPEC_CHANGE/REFACTOR/UI_ADJUST） |
| 任務 ID | 延續 T###，帶 `[RC<NNN>]` 標記 |
| Test-First | 同 RC 區塊內，`tests/` 任務必須在 `src/` 任務前 |
| 使用 logging | 禁止 print |
| **@spec 註解** | 新增/修改的程式碼必須包含 `@spec US{N}` 註解（維持 Traceability） |
| 驗證上限 | 最多 3 次迭代 |
| Scope 門檻 | [NEW] > 5 或 SPEC_CHANGE RC > 5 或 UI_ADJUST RC > 10 或架構性變更 或涉及檔案數 > 20 → STOP |
| 單一真相 | Phase 8 合併後，主檔為唯一權威 |
| 先掃描再深讀 | Stage 1 結構 → Stage 2 內容 |
| 深讀必記錄 | 每次深讀寫入 Escalation Log |
| 資料不足即停 | Gatekeeper 失敗 → STOP，不猜測 |

---

## 17. 心智模型

```
使用者變更需求
       │
       ▼
┌─────────────────────────────────────┐
│        Phase 0-1：建立 Change Set    │
│                                     │
│   變更需求 → RC001, RC002...        │
│   Type + Classification             │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│        Phase 2-4：產生 Delta 檔案    │
│                                     │
│   spec-delta.md（規格變更片段）      │
│   refine-plan.md（精簡計畫）         │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│        Phase 5-6：更新 Tasks + 分析  │
│                                     │
│   tasks.md（新增 T### 任務）         │
│   refine-analysis.md（品質檢查）     │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│        Phase 7：實作與測試           │
│                                     │
│   Test-First → Implementation       │
│   src/ + tests/ 更新                │
└─────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│        Phase 8：合併回主檔           │
│                                     │
│   spec.md ← 合併 delta              │
│   plan.md ← 合併必要內容             │
│   .refine/RC<NNN>/ ← 保留追溯       │
│                                     │
│   【Single Source of Truth】        │
└─────────────────────────────────────┘
```

### 關鍵記憶

> **「先 Change Set → 再 delta → 再合併回主檔；先 analyze 再 implement；所有深讀要可審計；最後只留一套真相」**
