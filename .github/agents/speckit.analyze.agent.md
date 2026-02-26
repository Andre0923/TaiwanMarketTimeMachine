---
description: Perform a non-destructive cross-artifact consistency and quality analysis across spec.md, plan.md, and tasks.md after task generation.
handoffs:
  - label: 開始實作
    agent: speckit.implement
    prompt: 一致性分析通過，開始按照 Tasks 實作程式碼
  - label: 修正 Tasks
    agent: speckit.tasks
    prompt: --default
---

## User Input

```text
$ARGUMENTS
```

> 💡 **`--default` 模式**：輸入 `--default` 等同於無額外指示，直接執行預設流程。

You **MUST** consider the user input before proceeding (if not empty or `--default`).

## Goal

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation. This command MUST run only after `/speckit.tasks` has successfully produced a complete `tasks.md`.

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any follow-up editing commands would be invoked manually).

**Constitution Authority**: The project constitution (`.specify/memory/constitution.md`) is **non-negotiable** within this analysis scope. Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle. If a principle itself needs to change, that must occur in a separate, explicit constitution update outside `/speckit.analyze`.

## Execution Steps

### 1. Initialize Analysis Context

Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` once from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive absolute paths:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

Abort with an error message if any required file is missing (instruct the user to run missing prerequisite command).
For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From spec.md:**

- Overview/Context
- Functional Requirements
- Non-Functional Requirements
- User Stories
- Edge Cases (if present)

**From plan.md:**

- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md:**

- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- Referenced file paths

**From constitution:**

- Load `.specify/memory/constitution.md` for principle validation

### 3. Build Semantic Models

Create internal representations (do not include raw artifacts in output):

- **Requirements inventory**: Each functional + non-functional requirement with a stable key (derive slug based on imperative phrase; e.g., "User can upload file" → `user-can-upload-file`)
- **User story/action inventory**: Discrete user actions with acceptance criteria
- **Task coverage mapping**: Map each task to one or more requirements or stories (inference by keyword / explicit reference patterns like IDs or key phrases)
- **Constitution rule set**: Extract principle names and MUST/SHOULD normative statements

### 4. Detection Passes (Token-Efficient Analysis)

Focus on high-signal findings. Limit to 50 findings total; aggregate remainder in overflow summary.

#### A. Duplication Detection

- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

#### B. Ambiguity Detection

- Flag vague adjectives (fast, scalable, secure, intuitive, robust) lacking measurable criteria
- Flag unresolved placeholders (TODO, TKTK, ???, `<placeholder>`, etc.)

#### C. Underspecification

- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing files or components not defined in spec/plan

#### D. Constitution Alignment

- Any requirement or plan element conflicting with a MUST principle
- Missing mandated sections or quality gates from constitution

#### E. Coverage Gaps

- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Non-functional requirements not reflected in tasks (e.g., performance, security)

**Affected Files 容差規則**：

plan.md Affected Files 列出的檔案分為「主要修改檔案」（有專屬 task）和「間接影響檔案」（因依賴可能被觸及但無專屬 task）：

| 條件 | 判定 | 嚴重度 |
|------|------|--------|
| plan 列出的檔案有對應的 [US] 標籤 task | ✅ 已覆蓋 | 無 |
| plan 列出的檔案無 task，但位於已有 task 的相鄰模組（同目錄/同 package） | ⚠️ 可能間接觸及 | LOW（建議確認是否需要顯式 task） |
| plan 列出的檔案無 task，且不在任何 task 涉及的模組範圍 | ❌ 覆蓋缺口 | MEDIUM |

#### F. Inconsistency

**遞進精鍊感知規則（Progressive Refinement Awareness）**：

spec.md 的 Key Entities 與 `data-model.md` / `contracts/` 之間為「概念摘要 → 精鍊定義」的遞進關係（specify → plan 的自然演進），分析時 MUST 區分「精鍊展開」與「真正不一致」：

| 差異類型 | 判定 | 嚴重度 |
|----------|------|--------|
| data-model.md 比 spec.md 多出欄位 | ✅ 正常精鍊 | INFO（不列入報告） |
| data-model.md 修改了 spec.md 的欄位命名 | ⚠️ 精鍊改名 | LOW（建議 spec 加註「完整定義見 data-model.md」） |
| data-model.md 修改了 spec.md 的列舉值 | ⚠️ 精鍊擴充 | LOW（若為擴充）/ MEDIUM（若為刪減或語義衝突） |
| data-model.md 新增了 spec.md 未提到的全新 Entity | ⚠️ 需檢查 | MEDIUM（可能遺漏需求或過度設計） |
| spec.md 有 Entity 但 data-model.md 完全未定義 | ❌ 真正缺失 | HIGH |

偵測到精鍊展開差異時，報告 SHOULD 使用措辭：「spec.md §N 的 {Entity} 與 data-model.md 的精鍊版本存在 {差異類型}。data-model.md 為資料定義權威，建議在 spec.md 加註引用或在 remediation 時同步。」

- Terminology drift (same concept named differently across files)
- Data entities referenced in plan but absent in spec (or vice versa)
- Task ordering contradictions (e.g., integration tasks before foundational setup tasks without dependency note)
- Conflicting requirements (e.g., one requires Next.js while other specifies Vue)

#### G. UI Consistency (Conditional: UI Impact ≠ None)

**Trigger**: Only run if spec.md contains "UI Impact" = Low or High

| Check | Description | Severity |
|-------|-------------|----------|
| G1. ID Existence | UI IDs referenced in spec.md (`[UI-SCR-###]`, `[UI-PAT-###]`, `[UI-STATE-###]`) must exist in `specs/system/ui/` | HIGH |
| G2. TBD Resolution | All `[UI-TBD]` markers should have corresponding tasks in plan.md to resolve them | MEDIUM |
| G3. State Coverage | Loading/Error/Empty states should reference `[UI-STATE-###]` patterns | MEDIUM |
| G4. Confirmation Rules | Irreversible actions should follow ux-guidelines.md confirmation rules | MEDIUM |
| G5. Maturity Gate | If UI Maturity Target = L1, verify L1 prerequisites exist: (1) Global States 規則 (2) Confirmation policy (3) Screen/Flow catalog | HIGH |
| G6. NEEDS UI DEFINITION | All `[NEEDS UI DEFINITION]` markers must have resolution tasks in plan.md | HIGH |

**L0 Maturity 降級規則**：

若 spec.md 宣告 `UI Maturity Target = L0`，以下檢查項目 MUST 降級：

| Check | 原嚴重度 | L0 降級後 | 理由 |
|-------|----------|-----------|------|
| G1. ID Existence | HIGH | INFO | L0 允許 `specs/system/ui/` 不存在，UI ID 為占位預分配 |
| G5. Maturity Gate | HIGH | SKIP | L1 前提檢查僅在 Target = L1 時啟動 |
| G6. NEEDS UI DEFINITION | HIGH | INFO | L0 = Draft（Constitution §3.6.2），允許 `[UI-TBD]` 與 `[NEEDS UI DEFINITION]` 存在 |

其餘 G 通道檢查（G2/G3/G4）維持原嚴重度。當 Target = L0 時，報告 SHOULD 在 G channel 區塊前加註：「G channel 以 L0 模式執行（UI Maturity Target = L0）。部分檢查已降級。」

**Skip Condition**: If UI Impact = None, skip entire G channel and note "G channel skipped: UI Impact = None"

### 5. Severity Assignment

Use this heuristic to prioritize findings:

- **CRITICAL**: Violates constitution MUST, missing core spec artifact, or requirement with zero coverage that blocks baseline functionality
- **HIGH**: Duplicate or conflicting requirement, ambiguous security/performance attribute, untestable acceptance criterion
- **MEDIUM**: Terminology drift, missing non-functional task coverage, underspecified edge case
- **LOW**: Style/wording improvements, minor redundancy not affecting execution order

### 6. Produce Compact Analysis Report

Output a Markdown report (no file writes) with the following structure:

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements ... | Merge phrasing; keep clearer version |

(Add one row per finding; generate stable IDs prefixed by category initial.)

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|

**Constitution Alignment Issues:** (if any)

**Unmapped Tasks:** (if any)

**Metrics:**

- Total Requirements
- Total Tasks
- Coverage % (requirements with >=1 task)
- Ambiguity Count
- Duplication Count
- Critical Issues Count

### 7. Provide Next Actions

At end of report, output a concise Next Actions block:

- If CRITICAL issues exist: Recommend resolving before `/speckit.implement`
- If only LOW/MEDIUM: User may proceed, but provide improvement suggestions
- Provide explicit command suggestions: e.g., "Run /speckit.specify with refinement", "Run /speckit.plan to adjust architecture", "Manually edit tasks.md to add coverage for 'performance-metrics'"

### 8. Offer Remediation

Ask the user: "Would you like me to suggest concrete remediation edits for the top N issues?" (Do NOT apply them automatically.)

### 9. Git Checkpoint (If Remediation Applied)

**After user-approved remediation edits are applied**, execute `git add . && git commit -m "docs: Analyze 分析 [FEATURE_NAME]" && git push`.

### 9.5 Spec 修訂標記自動注入

**If remediation edits modified any US or AC in spec.md**, AI MUST automatically inject change markers **before** the Git Checkpoint (§9):

1. **修改既有 US/AC** → 在標題末尾加上 `[MODIFIED]`
2. **新增 US/AC** → 在標題末尾加上 `[NEW]`
3. **刪除 US/AC** → 在標題末尾加上 `[DELETED]`

**範例**：
```markdown
### US A-1: 使用者登入 [MODIFIED]
### US A-3: 密碼重設 [NEW]
### US A-2: 舊版登入 [DELETED]
```

**規則**：
- 標記 MUST 放在標題行末尾，格式為 ` [TAG]`（前面一個空格）
- 若標題已有標記，不重複加上
- 標記注入後，在報告的 Next Actions 區塊中簡述哪些 US/AC 被標記

> 📌 此自動標記確保下游 `/flowkit.requirement-sync` 能正確識別「刻意修正」。
> 若未有標記，requirement-sync 會將差異歸類為「非意圖不一致」並逐項詢問確認。

## Operating Principles

### Context Efficiency

- **Minimal high-signal tokens**: Focus on actionable findings, not exhaustive documentation
- **Progressive disclosure**: Load artifacts incrementally; don't dump all content into analysis
- **Token-efficient output**: Limit findings table to 50 rows; summarize overflow
- **Deterministic results**: Rerunning without changes should produce consistent IDs and counts

### Analysis Guidelines

- **NEVER modify files** (this is read-only analysis)
- **NEVER hallucinate missing sections** (if absent, report them accurately)
- **Prioritize constitution violations** (these are always CRITICAL)
- **Use examples over exhaustive rules** (cite specific instances, not generic patterns)
- **Report zero issues gracefully** (emit success report with coverage statistics)

## Context

$ARGUMENTS
