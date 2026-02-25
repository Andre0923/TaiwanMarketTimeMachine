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

### 1.5 Git Hash 基線記錄

**MUST** 在開始實作前記錄當前 git commit hash 到 spec.md YAML frontmatter：

```bash
git rev-parse HEAD
```

將結果寫入 `FEATURE_SPEC` 的 YAML frontmatter（若欄位已存在則更新）：

```yaml
---
implement_baseline_commit: "abc1234"  # ← 自動記錄
---
```

> 📌 此基線供 `pre-unify-check` 做 `git diff` 比對，自動偵測 implement 後的文件變更。

### 1.6 Feature Status 更新為 In Progress

**MUST** 在開始實作時，將 `FEATURE_SPEC` 的 Status 更新為 `In Progress`：

1. 更新 YAML frontmatter：`status: In Progress`
2. 更新 inline 標記：`> **Status**: In Progress`

> 📌 此狀態變更屬於**元資料管理**，不違反 SDD「MUST NOT 修改 spec 內容」原則。

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

3. Load and analyze the implementation context:
   - **REQUIRED**: Read tasks.md for the complete task list and execution plan
   - **REQUIRED**: Read plan.md for tech stack, architecture, and file structure
   - **IF EXISTS**: Read data-model.md for entities and relationships
   - **IF EXISTS**: Read contracts/ for API specifications and test requirements
   - **IF EXISTS**: Read research.md for technical decisions and constraints
   - **IF EXISTS**: Read quickstart.md for integration scenarios

4. **Project Setup Verification**:
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

5. Parse tasks.md structure and extract:
   - **Task phases**: Setup, Tests, Core, Integration, Polish
   - **Task dependencies**: Sequential vs parallel execution rules
   - **Task details**: ID, description, file paths, parallel markers [P]
   - **Execution flow**: Order and dependency requirements

6. Execute implementation following the task plan:
   - **Phase-by-phase execution**: Complete each phase before moving to the next
   - **Respect dependencies**: Run sequential tasks in order, parallel tasks [P] can run together  
   - **Follow TDD approach**: Execute test tasks before their corresponding implementation tasks
   - **File-based coordination**: Tasks affecting the same files must run sequentially
   - **Validation checkpoints**: Verify each phase completion before proceeding

### 6.5 測試標記指引（Test Markers）

**Python (pytest) 專案 MUST 遵守**：

寫測試時，根據以下規則標記測試，確保 code-check 能正確分批執行：

| 標記 | 用途 | 判斷準則 |
|------|------|----------|
| `@pytest.mark.slow` | 耗時測試 | 執行時間可能超過 30 秒（外部程式呼叫、大量資料處理、網路請求等） |
| `@pytest.mark.serial` | 不可並行測試 | 使用共享資源（DB、檔案 I/O、網路 port、全域狀態） |

**`@pytest.mark.serial` 判斷準則詳細說明**：

當測試符合以下任一情境，MUST 標記 `@pytest.mark.serial`：

1. **共享資料庫**：多個測試讀寫同一個 DB（非 in-memory）
2. **共享檔案**：多個測試讀寫同一個檔案或目錄（非 `tmp_path`）
3. **網路 port**：測試啟動 server 並綁定固定 port
4. **全域狀態**：修改環境變數、單例模式、全域設定
5. **外部服務互斥**：呼叫同一個外部 API 且有 rate limit

**不需要標記的情境**（可安全並行）：
- 使用 `tmp_path` fixture（pytest 自動隨機化）
- 使用 in-memory SQLite
- 各測試獨立建立自己的資源
- 純函式計算 / 轉換測試

**範例**：
```python
import pytest

@pytest.mark.serial
def test_write_to_shared_db(db_connection):
    """寫入共享 DB，不可並行。"""
    ...

@pytest.mark.slow
def test_process_large_audio_file(sample_audio):
    """處理大檔音訊，耗時超過 30 秒。"""
    ...

@pytest.mark.slow
@pytest.mark.serial
def test_external_api_heavy(api_client):
    """呼叫外部 API，既慢且有 rate limit。"""
    ...
```

> 📌 **自動標記**：`@pytest.mark.slow` 支援自動標記 —— conftest.py 會根據 `.artifacts/test-durations.json` 歷史耗時自動標記。但 `@pytest.mark.serial` 無法自動判斷，MUST 手動標記。

7. Implementation execution rules:
   - **Setup first**: Initialize project structure, dependencies, configuration
   - **Tests before code**: If you need to write tests for contracts, entities, and integration scenarios
   - **Core development**: Implement models, services, CLI commands, endpoints
   - **Integration work**: Database connections, middleware, logging, external services
   - **Polish and validation**: Unit tests, performance optimization, documentation

8. Progress tracking and error handling:
   - Report progress after each completed task
   - Halt execution if any non-parallel task fails
   - For parallel tasks [P], continue with successful tasks, report failed ones
   - Provide clear error messages with context for debugging
   - Suggest next steps if implementation cannot proceed
   - **IMPORTANT** For completed tasks, make sure to mark the task off as [X] in the tasks file.

### 8.5 Spec Delta Log 規格差異日誌（MUST）

**在實作過程中**，若發現實際情況與 spec/plan/tasks 不一致，MUST 記錄到 `FEATURE_DIR/spec-delta-log.md`（不中斷實作流程）：

> 📌 若檔案不存在，依範本 `.flowkit/templates/spec-delta-log.template.md` 建立。

```markdown
## Spec Delta Log

| ID | Stage | Phase | Type | Original (spec/plan) | Actual/Discovery | Impact | Action |
|----|-------|-------|------|---------------------|-----------------|--------|--------|
| D1 | implement | Phase 2 | 技術限制 | spec: 即時同步 | API 僅支援輪詢 | US-A-2 AC1 | 待 refine-loop |
```

**記錄規則**：
- Stage 欄位固定填 `implement`
- 不中斷實作流程：先記錄規格差異，繼續實作
- MUST NOT 修改 spec.md 的**規格內容**（SDD 原則），規格差異由後續 refine-loop 處理
  - **例外**：YAML frontmatter 元資料欄位（`status`、`implement_baseline_commit`、`updated`）的更新不受此限制
- 每個 Phase 結束時檢查是否有新規格差異需記錄
- 若無規格差異，不需建立此檔案

> 📌 此規格差異日誌供 `refine-loop`（修正）、`requirement-sync`（意圖判斷）、`pre-unify-check`（品質檢查）使用。

9. Completion validation:
   - Verify all required tasks are completed
   - Check that implemented features match the original specification
   - Validate that tests pass and coverage meets requirements
   - Confirm the implementation follows the technical plan
   - **更新 Feature Status 為 Implemented**：
     1. 更新 YAML frontmatter：`status: Implemented`
     2. 更新 inline 標記：`> **Status**: Implemented`
   - Report final status with summary of completed work

Note: This command assumes a complete task breakdown exists in tasks.md. If tasks are incomplete or missing, suggest running `/speckit.tasks` first to regenerate the task list.
