---
description: Execute the implementation plan by processing and executing all tasks defined in tasks.md
handoffs:
  - label: 建立追溯索引
    agent: flowkit.trace
    prompt: 實作完成，建立規格-程式碼追溯索引
  - label: Debug / 微調
    agent: flowkit.refine-loop
    prompt: 實作完成後需要 debug 或微調
---

## User Input

```text
$ARGUMENTS
```

> 💡 **`--default` 模式**：輸入 `--default` 等同於無額外指示，直接執行預設流程。

You **MUST** consider the user input before proceeding (if not empty or `--default`).

## Outline

1. Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute. For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. **Check checklists status** (if FEATURE_DIR/checklists/ exists):
   - Scan all checklist files in the checklists/ directory
   - For each checklist, count:
     - Total items: All lines matching `- [ ]` or `- [X]` or `- [x]`
     - Completed items: Lines matching `- [X]` or `- [x]`
     - Incomplete items: Lines matching `- [ ]`
   - Create a status table:

     ```text
     | Checklist | Total | Completed | Incomplete | Status |
     |-----------|-------|-----------|------------|--------|
     | ux.md     | 12    | 12        | 0          | ✓ PASS |
     | test.md   | 8     | 5         | 3          | ✗ FAIL |
     | security.md | 6   | 6         | 0          | ✓ PASS |
     ```

   - Calculate overall status:
     - **PASS**: All checklists have 0 incomplete items
     - **FAIL**: One or more checklists have incomplete items

   - **If any checklist is incomplete**:
     - Display the table with incomplete item counts
     - **STOP** and ask: "Some checklists are incomplete. Do you want to proceed with implementation anyway? (yes/no)"
     - Wait for user response before continuing
     - If user says "no" or "wait" or "stop", halt execution
     - If user says "yes" or "proceed" or "continue", proceed to step 3

   - **If all checklists are complete**:
     - Display the table showing all checklists passed
     - Automatically proceed to step 3

3. **UI Gate Check (If UI Impact ≠ None)**:
   - Read spec.md's "UI/UX 影響評估" section
   - **IF UI Impact = None**: Skip this step entirely
   - **IF UI Impact = Low or High**:
     
     a. **Check [UI-TBD] and [NEEDS UI DEFINITION] Resolution**:
        - Scan spec.md and plan.md for any remaining `[UI-TBD]` markers
        - Scan for any remaining `[NEEDS UI DEFINITION]` markers
        - Each marker should have been resolved to a proper UI ID
        
     b. **Check UI Maturity (L1 Gate)**:
        - For each UI ID referenced, verify it exists in `specs/system/ui/`
        - Verify the definition is at **L1 (Buildable)** level, not L0 (Draft)
        - **L1 最低要求**（三項皆需符合）:
          1. Global States（loading/empty/error）有明確規則
          2. 不可逆操作已定義 confirmation policy
          3. 主要 Screen/Flow 有完整 catalog
     
     c. **Gate Decision**:
        - **PASS**: All markers resolved AND all UI IDs at L1 AND L1 prerequisites met
        - **FAIL**: Any unresolved markers OR any UI ID still at L0 OR L1 prerequisites missing
        
     d. **If Gate FAILS**:
        - Display unresolved items table
        - **STOP** and report:
          ```
          ❌ UI GATE FAILED
          
          Unresolved [UI-TBD] items:
          - [UI-TBD: description] → Please define in ui-structure.md and assign ID
          
          Unresolved [NEEDS UI DEFINITION] items:
          - [NEEDS UI DEFINITION: description] → Please complete definition
          
          UI IDs not at L1 (Buildable):
          - [UI-SCR-###] still at L0 → Please complete definition in ui-structure.md
          
          L1 Prerequisites Missing:
          - [ ] Global States 規則尚未定義
          - [ ] Confirmation policy 尚未定義
          - [ ] Screen/Flow catalog 不完整
          
          Recommended actions:
          1. Complete UI Discovery Tasks from plan.md
          2. Complete UI file update tasks from plan.md
          3. Ensure all UI IDs reach L1 maturity
          4. Re-run /speckit.implement
          ```
        - Wait for user to confirm proceed or fix issues
        
     e. **If Gate PASSES**:
        - Log "UI Gate: ✅ PASS (L1 Verified)" and proceed to step 4

4. Load and analyze the implementation context:
   - **REQUIRED**: Read tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **IF EXISTS**: Read data-model.md for entities and relationships
   - **IF EXISTS**: Read contracts/ for API specifications and test requirements
   - **IF EXISTS**: Read research.md for technical decisions and constraints
   - **IF EXISTS**: Read quickstart.md for integration scenarios
   - **IF EXISTS** (and UI Impact ≠ None): Read `specs/system/ui/` for UI specifications

5. **Project Setup Verification**:
   - **REQUIRED**: Create/verify ignore files based on actual project setup:

   **Detection & Creation Logic**:
   - Check if the following command succeeds to determine if the repository is a git repo (create/verify .gitignore if so):

     ```sh
     git rev-parse --git-dir 2>/dev/null
     ```

   - Check if Dockerfile* exists or Docker in plan.md → create/verify .dockerignore
   - Check if .eslintrc* exists → create/verify .eslintignore
   - Check if eslint.config.* exists → ensure the config's `ignores` entries cover required patterns
   - Check if .prettierrc* exists → create/verify .prettierignore
   - Check if .npmrc or package.json exists → create/verify .npmignore (if publishing)
   - Check if terraform files (*.tf) exist → create/verify .terraformignore
   - Check if .helmignore needed (helm charts present) → create/verify .helmignore

   **If ignore file already exists**: Verify it contains essential patterns, append missing critical patterns only
   **If ignore file missing**: Create with full pattern set for detected technology

   **Common Patterns by Technology** (from plan.md tech stack):
   - **Node.js/JavaScript/TypeScript**: `node_modules/`, `dist/`, `build/`, `*.log`, `.env*`
   - **Python**: `__pycache__/`, `*.pyc`, `.venv/`, `venv/`, `dist/`, `*.egg-info/`
   - **Java**: `target/`, `*.class`, `*.jar`, `.gradle/`, `build/`
   - **C#/.NET**: `bin/`, `obj/`, `*.user`, `*.suo`, `packages/`
   - **Go**: `*.exe`, `*.test`, `vendor/`, `*.out`
   - **Ruby**: `.bundle/`, `log/`, `tmp/`, `*.gem`, `vendor/bundle/`
   - **PHP**: `vendor/`, `*.log`, `*.cache`, `*.env`
   - **Rust**: `target/`, `debug/`, `release/`, `*.rs.bk`, `*.rlib`, `*.prof*`, `.idea/`, `*.log`, `.env*`
   - **Kotlin**: `build/`, `out/`, `.gradle/`, `.idea/`, `*.class`, `*.jar`, `*.iml`, `*.log`, `.env*`
   - **C++**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.so`, `*.a`, `*.exe`, `*.dll`, `.idea/`, `*.log`, `.env*`
   - **C**: `build/`, `bin/`, `obj/`, `out/`, `*.o`, `*.a`, `*.so`, `*.exe`, `Makefile`, `config.log`, `.idea/`, `*.log`, `.env*`
   - **Swift**: `.build/`, `DerivedData/`, `*.swiftpm/`, `Packages/`
   - **R**: `.Rproj.user/`, `.Rhistory`, `.RData`, `.Ruserdata`, `*.Rproj`, `packrat/`, `renv/`
   - **Universal**: `.DS_Store`, `Thumbs.db`, `*.tmp`, `*.swp`, `.vscode/`, `.idea/`

   **Tool-Specific Patterns**:
   - **Docker**: `node_modules/`, `.git/`, `Dockerfile*`, `.dockerignore`, `*.log*`, `.env*`, `coverage/`
   - **ESLint**: `node_modules/`, `dist/`, `build/`, `coverage/`, `*.min.js`
   - **Prettier**: `node_modules/`, `dist/`, `build/`, `coverage/`, `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
   - **Terraform**: `.terraform/`, `*.tfstate*`, `*.tfvars`, `.terraform.lock.hcl`
   - **Kubernetes/k8s**: `*.secret.yaml`, `secrets/`, `.kube/`, `kubeconfig*`, `*.key`, `*.crt`

6. Parse tasks.md structure and extract:
   - **Task phases**: Setup, Tests, Core, Integration, Polish
   - **Task dependencies**: Sequential vs parallel execution rules
   - **Task details**: ID, description, file paths, parallel markers [P]
   - **Execution flow**: Order and dependency requirements

7. Execute implementation following the task plan:
   - **Phase-by-phase execution**: Complete each phase before moving to the next
   - **Respect dependencies**: Run sequential tasks in order, parallel tasks [P] can run together  
   - **Follow TDD approach**: Execute test tasks before their corresponding implementation tasks
   - **File-based coordination**: Tasks affecting the same files must run sequentially
   - **Validation checkpoints**: Verify each phase completion before proceeding
   - **Spec Reference 註解**：建立新檔案時，若該任務有 [US*] 標籤，加入 @spec 註解（詳見下方規則）
   - **Git Checkpoint**: After completing each phase, execute `git add . && git commit -m "feat: {phase_name} (T00X-T00Y)" && git push`

8. **Spec Reference 註解規則**（用於 Traceability）：

   **觸發條件**：建立新檔案時，該任務有 `[US*]` 標籤
   
   **格式規範**：
   ```python
   # Python
   # @spec US1 (NNN-feature-name/spec.md#user-story-1)
   # @spec-ac AC1.1, AC1.2
   
   class MyClass:
       pass
   ```
   
   ```typescript
   // TypeScript/JavaScript
   // @spec US1 (NNN-feature-name/spec.md#user-story-1)
   // @spec-ac AC1.1, AC1.2
   
   export class MyClass { }
   ```
   
   ```rust
   // Rust/C/C++
   // @spec US1 (NNN-feature-name/spec.md#user-story-1)
   // @spec-ac AC1.1, AC1.2
   
   pub struct MyStruct { }
   ```
   
   **欄位說明**：
   - `@spec US{N}`：對應 spec.md 的 User Story 編號
   - `(NNN-feature-name/spec.md#user-story-{N})`：Spec 檔案的相對路徑與 anchor
   - `@spec-ac AC{N}.{M}`：（選用）對應的 Acceptance Criteria 編號

   **範例（從 tasks.md）**：
   ```markdown
   - [ ] T014 [US1] Implement UserService in src/services/user_service.py
   ```
   **產生的註解**：
   ```python
   # @spec US1 (001-user-management/spec.md#user-story-1)
   # Generated by SpecKit Implement
   
   class UserService:
       ...
   ```

9. Implementation execution rules:
   - **Setup first**: Initialize project structure, dependencies, configuration
   - **Tests before code**: If you need to write tests for contracts, entities, and integration scenarios
   - **Core development**: Implement models, services, CLI commands, endpoints
   - **Integration work**: Database connections, middleware, logging, external services
   - **Polish and validation**: Unit tests, performance optimization, documentation

10. Progress tracking and error handling:
   - Report progress after each completed task
   - Halt execution if any non-parallel task fails
   - For parallel tasks [P], continue with successful tasks, report failed ones
   - Provide clear error messages with context for debugging
   - Suggest next steps if implementation cannot proceed
   - **IMPORTANT** For completed tasks, make sure to mark the task off as [X] in the tasks file.

11. Completion validation:
   - Verify all required tasks are completed
   - Check that implemented features match the original specification
   - Validate that tests pass and coverage meets requirements
   - Confirm the implementation follows the technical plan
   - Report final status with summary of completed work

Note: This command assumes a complete task breakdown exists in tasks.md. If tasks are incomplete or missing, suggest running `/speckit.tasks` first to regenerate the task list.
