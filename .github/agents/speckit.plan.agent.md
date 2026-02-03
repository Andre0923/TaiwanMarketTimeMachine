---
description: Execute the implementation planning workflow using the plan template to generate design artifacts.
handoffs: 
  - label: Create Tasks
    agent: speckit.tasks
    prompt: Break the plan into tasks
  - label: 確認plan與system一致性
    agent: flowkit.consistency-check
    prompt: Plan 完成，執行一致性檢查確認與現有系統無衝突
    send: true
  - label: Create Checklist
    agent: speckit.checklist
    prompt: Create a checklist for the following domain...
---

## User Input

```text
$ARGUMENTS
```

> 💡 **`--default` 模式**：輸入 `--default` 等同於無額外指示，直接執行預設流程。

You **MUST** consider the user input before proceeding (if not empty or `--default`).

## Outline

1. **Setup**: Run `.specify/scripts/powershell/setup-plan.ps1 -Json` from repo root and parse JSON for FEATURE_SPEC, IMPL_PLAN, SPECS_DIR, BRANCH. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Load context**: Read FEATURE_SPEC and `.specify/memory/constitution.md`. Load IMPL_PLAN template (already copied).

3. **Load Milestone Context (Optional)**:
   - **Read YAML Frontmatter**: Parse FEATURE_SPEC for YAML frontmatter field `milestone`
   - **IF** `milestone` field exists and not null (e.g., `milestone: M02`):
     - Construct context file path: `docs/requirements/Milestone/{milestone}-context.md`
     - **IF EXISTS** the context file:
       - Read Milestone context for technical constraints, architecture decisions, shared services
       - Use this context to align technical decisions with Milestone requirements
     - **IF NOT EXISTS**: Log info "No context file for {milestone}" and proceed
   - **IF** `milestone` is null or missing: Proceed without Milestone context (standalone Feature)
   - This step is non-blocking; missing context should not stop the planning flow

4. **Load System Context (Conditional)**:
   - **Read YAML Frontmatter**: Parse FEATURE_SPEC for `system_context` field
   - **IF** `system_context: true`:
     - Read `.flowkit/memory/system-context-index.md` to get system overview (modules, entry points, shared services)
     - Identify modules/components relevant to this Feature's scope
     - **IF need deeper understanding** of specific module:
       - Read corresponding section in `.flowkit/memory/system-context.md`
       - **IF need implementation details**: Read actual source files in `src/` or `specs/system/`
     - Use system context to:
       - Identify reusable components
       - Understand integration points
       - Avoid duplicating existing functionality
   - **IF** `system_context: false` or missing:
     - Log info "System context not loaded (system_context=false). Run /flowkit.system-context first if needed."
     - Proceed without system context (new project or first Feature)
   - This step is non-blocking; missing system context should not stop the planning flow

5. **Load UI Context (If UI Impact ≠ None)**:
   - Read spec.md's "UI/UX 影響評估" section to determine UI Impact and UI Maturity Target
   - **IF UI Impact = Low or High**:
     - **IF EXISTS**: `specs/system/ui/` directory
       - Read `specs/system/ui/ui-structure.md` for affected screens
       - Read `specs/system/ui/ux-guidelines.md` for interaction patterns
     - Identify all `[UI-TBD]` and `[NEEDS UI DEFINITION]` markers from spec.md
     - Plan UI definition tasks to resolve these items before implement
   - **Determine Maturity Gap**:
     - Current Maturity: 目前 UI 文件的完整度
     - Target Maturity: spec.md 中指定的 UI Maturity Target
     - **IF Target = L1 AND Current = L0**:
       - Generate UI Discovery Tasks in plan（見 step 6）
       - L1 最低要求：
         1. Global States（loading/empty/error）有明確規則
         2. 不可逆操作已定義 confirmation policy
         3. 主要 Screen/Flow 有完整 catalog

6. **Execute plan workflow**: Follow the structure in IMPL_PLAN template to:
   - Fill Technical Context (mark unknowns as "NEEDS CLARIFICATION")
   - Fill Constitution Check section from constitution
   - **Fill UI/UX Plan section** (if UI Impact ≠ None):
     - Fill UI Impact Summary（承接 spec 的 Impact/Maturity）
     - **Generate UI Discovery Tasks** (if Target = L1 and Current = L0):
       - [ ] 定義 Global States（loading/empty/error）規則
       - [ ] 定義不可逆操作 confirmation policy
       - [ ] 補齊 Screen/Flow catalog
     - List affected screens with current/target Maturity (L0→L1)
     - List new Pattern/State definitions needed
     - Generate UI file update tasks
     - Assign UI IDs to all `[UI-TBD]` items
   - Evaluate gates (ERROR if violations unjustified)
   - Phase 0: Generate research.md (resolve all NEEDS CLARIFICATION)
   - Phase 1: Generate data-model.md, contracts/, quickstart.md
   - Phase 1: Update agent context by running the agent script
   - Re-evaluate Constitution Check post-design

7. **Stop and report**: Command ends after Phase 2 planning. Report branch, IMPL_PLAN path, and generated artifacts.

## Phases

### Phase 0: Outline & Research

1. **Extract unknowns from Technical Context** above:
   - For each NEEDS CLARIFICATION → research task
   - For each dependency → best practices task
   - For each integration → patterns task

2. **Generate and dispatch research agents**:

   ```text
   For each unknown in Technical Context:
     Task: "Research {unknown} for {feature context}"
   For each technology choice:
     Task: "Find best practices for {tech} in {domain}"
   ```

3. **Consolidate findings** in `research.md` using format:
   - Decision: [what was chosen]
   - Rationale: [why chosen]
   - Alternatives considered: [what else evaluated]

**Output**: research.md with all NEEDS CLARIFICATION resolved

**Git Checkpoint**: After Phase 0 completes, execute `git add . && git commit -m "plan: phase0 research for {FEATURE_ID}" && git push`

### Phase 1: Design & Contracts

**Prerequisites:** `research.md` complete

1. **Extract entities from feature spec** → `data-model.md`:
   - Entity name, fields, relationships
   - Validation rules from requirements
   - State transitions if applicable

2. **Generate API contracts** from functional requirements:
   - For each user action → endpoint
   - Use standard REST/GraphQL patterns
   - Output OpenAPI/GraphQL schema to `/contracts/`

3. **Agent context update**:
   - Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType copilot`
   - These scripts detect which AI agent is in use
   - Update the appropriate agent-specific context file
   - Add only new technology from current plan
   - Preserve manual additions between markers

**Output**: data-model.md, /contracts/*, quickstart.md, agent-specific file

**Git Checkpoint**: After Phase 1 completes, execute `git add . && git commit -m "plan: phase1 design artifacts for {FEATURE_ID}" && git push`

## Key rules

- Use absolute paths
- ERROR on gate failures or unresolved clarifications
