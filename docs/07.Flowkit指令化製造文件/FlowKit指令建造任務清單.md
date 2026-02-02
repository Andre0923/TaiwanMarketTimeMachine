# FlowKit 指令建造任務清單

> **用途**：建立新的 FlowKit 指令化套件時，需完成的標準任務清單  
> **適用對象**：AI Agent 或人類開發者  
> **版本**：1.0.0  
> **最後更新**：2025-01-26

---

## 概述

當需要建立新的 FlowKit 指令時，請依照本清單逐項完成。所有任務皆為必要項目，除非明確標註為「選配」。

---

## 任務清單總覽

| 階段 | 任務 | 必要性 | 說明 |
|------|------|--------|------|
| **Phase 1** | 設計 Agent 指令內容 | MUST | 核心指令邏輯 |
| **Phase 2** | 建立 Template 檔案 | 選配 | 若指令需要產出特定格式文件 |
| **Phase 3** | 部署至 GitHub Copilot | MUST | Agent + Prompt 檔案 |
| **Phase 4** | 部署至 Cursor | MUST | Command 檔案 |
| **Phase 5** | 撰寫功能說明文件 | MUST | 使用者導向說明 |
| **Phase 6** | 更新索引與目錄文件 | MUST | 維護文件一致性 |
| **Phase 7** | 驗證與提交 | MUST | 確保部署完整 |

---

## Phase 1：設計 Agent 指令內容

### 1.1 確認指令需求

- [ ] 確認指令名稱（命名規範：`flowkit.{功能名稱}`）
- [ ] 確認指令用途與觸發時機
- [ ] 確認輸入參數（CLI 風格 + 自然語言支援）
- [ ] 確認輸出格式與位置

### 1.2 設計指令結構

參考既有指令結構，標準章節包含：

```markdown
# 標準章節結構

1. 使用者輸入（$ARGUMENTS）
2. 目標
3. 核心價值
4. 操作限制（AI MUST / MUST NOT / SHOULD）
5. 執行步驟（Phase 0 ~ N）
6. 完成標準（Definition of Done）
7. 錯誤處理
8. 快速參考
```

### 1.3 平台格式差異

| 平台 | 格式要求 |
|------|----------|
| **GitHub Copilot** | YAML frontmatter（`---` 包裹 `description` 和 `handoffs`），檔案副檔名 `.agent.md` |
| **Cursor** | YAML frontmatter（與 GitHub Copilot 相同格式），檔案副檔名 `.md` |

**GitHub Copilot Agent 範例**：

```markdown
---
description: 指令的一句話描述
handoffs:
  - label: 接續動作名稱
    agent: 目標 agent 名稱
    prompt: 傳遞給目標 agent 的提示
---

# FlowKit {指令名稱}
... 指令內容 ...
```

**Cursor Command 範例**：

```markdown
---
description: 指令的一句話描述
handoffs:
  - label: 接續動作名稱
    agent: 目標 agent 名稱
    prompt: 傳遞給目標 agent 的提示
---

# FlowKit {指令名稱}
... 指令內容（與 GitHub Copilot 相同）...
```

> **注意**：兩個平台的指令內容應保持一致，僅檔案位置和副檔名不同。

---

## Phase 2：建立 Template 檔案（選配）

### 2.1 判斷是否需要 Template

若指令會產出特定格式的文件，SHOULD 建立對應的 Template：

| 情境 | 是否需要 Template |
|------|-------------------|
| 指令產出結構化報告 | ✅ 需要 |
| 指令產出設定檔或規格文件 | ✅ 需要 |
| 指令僅執行檢查/驗證 | ❌ 不需要 |
| 指令僅輸出至對話 | ❌ 不需要 |

### 2.2 Template 檔案規範

**存放位置**：`.flowkit/templates/`

**命名規範**：`{指令名稱}-{用途}.template.md`

**範例**：
- `Milestone-context-output.template.md`
- `Milestone-context-conflict-report.template.md`
- `refine-spec-delta.template.md`

### 2.3 建立 Template 檔案

- [ ] 在 `.flowkit/templates/` 建立 Template 檔案
- [ ] Template 內容應包含：
  - 文件標頭（用途、版本）
  - 結構化章節
  - 佔位符（使用 `{PLACEHOLDER}` 格式）
  - 填寫說明（選配）

---

## Phase 3：部署至 GitHub Copilot

### 3.1 建立 Agent 檔案

**位置**：`.github/agents/flowkit.{指令名稱}.agent.md`

**格式要求**：
- [ ] 包含 YAML frontmatter（`---` 區塊）
- [ ] `description` 欄位：一句話描述指令用途
- [ ] `handoffs` 欄位：定義可接續的 Agent（選配）
- [ ] Markdown 內容：完整指令邏輯

### 3.2 建立 Prompt 檔案

**位置**：`.github/prompts/flowkit.{指令名稱}.prompt.md`

**格式**：

```markdown
```prompt
---
agent: flowkit.{指令名稱}
---

```
```

**說明**：
- Prompt 檔案是 Agent 的快捷呼叫方式
- 使用者可在 VS Code 中輸入 `/flowkit.{指令名稱}` 快速呼叫
- **此功能仍然有效**，是 GitHub Copilot 的標準功能

### 3.3 驗證 GitHub Copilot 部署

- [ ] Agent 檔案語法正確（YAML frontmatter 無錯誤）
- [ ] Prompt 檔案指向正確的 Agent 名稱
- [ ] 在 VS Code 中測試 `/flowkit.{指令名稱}` 能正確呼叫

---

## Phase 4：部署至 Cursor

### 4.1 建立 Command 檔案

**位置**：`.cursor/commands/flowkit.{指令名稱}.md`

**格式要求**：
- [ ] 包含 YAML frontmatter（與 GitHub Copilot 相同格式）
- [ ] 內容與 GitHub Copilot Agent 相同

### 4.2 驗證 Cursor 部署

- [ ] Command 檔案可被 Cursor 識別
- [ ] 在 Cursor 中測試指令能正確執行

---

## Phase 5：撰寫功能說明文件

### 5.1 建立功能說明文件

**位置**：`docs/77.flowkit相關文件/功能說明-flowkit.{指令名稱}.md`

**標準章節**：

```markdown
# 功能說明：flowkit.{指令名稱}

## 概述
## 使用場景
## 核心功能
## 使用方式
## 輸出格式
## 與其他 FlowKit 工具的關係
## 核心概念
## 部署位置
## 版本歷史
## 相關文件
```

### 5.2 功能說明內容要求

- [ ] 使用繁體中文撰寫
- [ ] 包含 CLI 用法範例
- [ ] 包含自然語言用法範例
- [ ] 說明與其他 FlowKit 指令的關係
- [ ] 列出部署位置（GitHub Copilot / Cursor / Templates）

---

## Phase 6：更新索引與目錄文件

### 6.1 更新 FlowKit README

**位置**：`docs/77.flowkit相關文件/README.md`

- [ ] 在指令清單中新增該指令
- [ ] 更新指令數量統計（若有）

### 6.2 更新目錄結構文件

**位置**：`docs/00.目錄結構.md`

- [ ] 若有新增 Template，在 `.flowkit/templates/` 區段新增
- [ ] 確認 `.github/agents/` 和 `.cursor/commands/` 區段涵蓋新指令

### 6.3 同步部署用備份（選配）

**位置**：`docs/77.flowkit相關文件/AI指令化檔案_部署用/agents/`

- [ ] 若需要保留部署用備份，複製 Agent 檔案至此目錄

---

## Phase 7：驗證與提交

### 7.1 完整性檢查清單

**必要檔案**：

| 檔案 | 位置 | 狀態 |
|------|------|------|
| Agent 檔案 | `.github/agents/flowkit.{名稱}.agent.md` | [ ] |
| Prompt 檔案 | `.github/prompts/flowkit.{名稱}.prompt.md` | [ ] |
| Cursor Command | `.cursor/commands/flowkit.{名稱}.md` | [ ] |
| 功能說明 | `docs/77.flowkit相關文件/功能說明-flowkit.{名稱}.md` | [ ] |

**選配檔案**：

| 檔案 | 位置 | 狀態 |
|------|------|------|
| Template 檔案 | `.flowkit/templates/{名稱}-*.template.md` | [ ] |
| 部署用備份 | `docs/77.flowkit相關文件/AI指令化檔案_部署用/agents/` | [ ] |

**文件更新**：

| 文件 | 位置 | 狀態 |
|------|------|------|
| FlowKit README | `docs/77.flowkit相關文件/README.md` | [ ] |
| 目錄結構 | `docs/00.目錄結構.md` | [ ] |

### 7.2 一致性檢查

- [ ] GitHub Copilot Agent 與 Cursor Command 內容一致（包含 YAML frontmatter）
- [ ] 所有文件使用相同的指令名稱
- [ ] 版本號一致

### 7.3 Git 提交

```bash
git add .
git commit -m "feat: 新增 flowkit.{指令名稱} 指令化套件

新增:
- .github/agents/flowkit.{名稱}.agent.md
- .github/prompts/flowkit.{名稱}.prompt.md
- .cursor/commands/flowkit.{名稱}.md
- docs/77.flowkit相關文件/功能說明-flowkit.{名稱}.md
- .flowkit/templates/{相關 template}（若有）

修改:
- docs/77.flowkit相關文件/README.md
- docs/00.目錄結構.md"

git push
```

---

## 快速參考

### 檔案位置對照表

| 用途 | 位置 |
|------|------|
| GitHub Copilot Agent | `.github/agents/flowkit.{名稱}.agent.md` |
| GitHub Copilot Prompt | `.github/prompts/flowkit.{名稱}.prompt.md` |
| Cursor Command | `.cursor/commands/flowkit.{名稱}.md` |
| Template 檔案 | `.flowkit/templates/{名稱}-*.template.md` |
| 功能說明文件 | `docs/77.flowkit相關文件/功能說明-flowkit.{名稱}.md` |
| FlowKit 索引 | `docs/77.flowkit相關文件/README.md` |
| 目錄結構 | `docs/00.目錄結構.md` |

### 命名規範

| 項目 | 規範 | 範例 |
|------|------|------|
| 指令名稱 | `flowkit.{kebab-case}` | `flowkit.Milestone-context` |
| Agent 檔案 | `flowkit.{名稱}.agent.md` | `flowkit.Milestone-context.agent.md` |
| Prompt 檔案 | `flowkit.{名稱}.prompt.md` | `flowkit.Milestone-context.prompt.md` |
| Command 檔案 | `flowkit.{名稱}.md` | `flowkit.Milestone-context.md` |
| Template 檔案 | `{名稱}-{用途}.template.md` | `Milestone-context-output.template.md` |
| 功能說明 | `功能說明-flowkit.{名稱}.md` | `功能說明-flowkit.Milestone-context.md` |

### GitHub Copilot Prompt 檔案說明

`.github/prompts/` 目錄下的 Prompt 檔案**仍然有效**，用途如下：

1. **快捷呼叫**：使用者可輸入 `/flowkit.{名稱}` 快速呼叫對應 Agent
2. **簡化語法**：Prompt 檔案只需指向 Agent，無需重複內容
3. **維護便利**：Agent 內容更新時，Prompt 自動指向最新版本

**格式範例**：

```markdown
```prompt
---
agent: flowkit.{指令名稱}
---

```
```

---

## 相關文件

- [FlowKit 功能說明總覽](../77.flowkit相關文件/README.md)
- [SDD 開發流程指南](./03.SDD開發流程指南.md)
- [Copilot Instructions](.github/copilot-instructions.md)
