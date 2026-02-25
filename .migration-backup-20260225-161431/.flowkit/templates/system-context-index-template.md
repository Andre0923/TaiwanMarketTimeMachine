# 📋 Context Index 範本 (Layer 1 - 精簡索引版)

> **用途**: 每次 AI 對話自動注入的精簡上下文  
> **目標篇幅**: 50-150 行（約 250-750 tokens）  
> **設計理念**: 只放索引，讓 AI 知道去哪裡找更多資訊  
> **產生指令**: `.flowkit.system-context`

---

## 範本正文

```markdown
# Context Index v{VERSION}

> 最後更新: {DATE} | 完整版: `.flowkit/memory/system-context.md`

## One-liner
{PROJECT_NAME}: {一句話描述專案本質與核心價值}

## Boundaries (模組邊界，禁止跨越)
- {module_a}/: {職責} | Owns: {資料/契約} | API: `{path}`
- {module_b}/: {職責} | Owns: {資料/契約} | API: `{path}`
- {module_c}/: {職責} | Owns: {資料/契約} | API: `{path}`
- {module_d}/: {職責} | Owns: {資料/契約} | API: `{path}`

## Entry Points (開發從這裡開始)
- CLI: `{path}` - {說明}
- API: `{path}` - {說明}
- UI: `{path}` - {說明}
- Core: `{path}` - {說明}
- Config: `{path}` - {說明}

## Shared Services (直接使用，勿重複實作)
- {Service A}: `{path}` → `{使用範例}`
- {Service B}: `{path}` → `{使用範例}`
- {Service C}: `{path}` → `{使用範例}`

## Golden Flows (核心流程路徑追蹤)
- {Flow 1}: {Layer} → {Layer} → {Layer} → {Layer}
- {Flow 2}: {Layer} → {Layer} → {Layer}

## Where-to-Look (遇到問題去哪找)
- {情境 A} → `{path}` → `{path}`
- {情境 B} → `{path}` → `{path}`
- {情境 C} → `{path}` → `{path}`
- {情境 D} → `{path}`

## NON-NEGOTIABLE (強制規範)
- {規範 1}: {MUST/NEVER} {具體規範}
- {規範 2}: {MUST/NEVER} {具體規範}
- {規範 3}: {MUST/NEVER} {具體規範}

## Known Pitfalls (常見陷阱)
- {陷阱 1}: {預防方式}
- {陷阱 2}: {預防方式}
- {陷阱 3}: {預防方式}

## Completed Features (已完成功能，避免重複實作)
- {Feature ID}: {名稱} - {核心能力}
- {Feature ID}: {名稱} - {核心能力}
- {Feature ID}: {名稱} - {核心能力}

## In Progress
- {Feature ID}: {名稱} - {核心能力}

## Full Context
See: `.flowkit/memory/system-context.md`
```

---

## 使用方式

### 方式 1：放入 Agent Context Manual 區塊

在 `.specify/agent-context.md` 的 Manual 區塊中放入精簡版內容：

```markdown
<!-- MANUAL ADDITIONS START -->
# Context Index v{VERSION}
...（精簡版內容）...
<!-- MANUAL ADDITIONS END -->
```

### 方式 2：作為獨立檔案

放在 `.flowkit/memory/context-index.md`，在 speckit.plan 或其他指令階段自動引用。

---

## 填寫指引

### One-liner
- 用一句話說明專案是什麼、做什麼
- 範例：`VideoNote: Video-first 知識萃取工具，將影片轉化為時間軸逐字稿`

### Boundaries
- 列出 4-7 個主要模組
- 每個模組標示：職責 + 擁有什麼 + Public API 路徑
- 這告訴 AI「這個模組負責什麼，邊界在哪」

### Entry Points
- 列出 4-6 個最常作為開發起點的檔案
- 幫助 AI 快速定位程式碼入口

### Shared Services
- 列出已經存在且應該被複用的模組
- 防止 AI 重複實作已有功能

### Golden Flows
- 列出 2-4 個最重要的流程
- 使用「→」表示資料/控制流向

### Where-to-Look
- 針對常見開發情境，指出應該去哪些檔案查找

### NON-NEGOTIABLE
- 列出 3-5 條絕對必須遵守的規範
- 使用 MUST/NEVER 關鍵字

### Known Pitfalls
- 列出 3-5 個過去踩過的坑
- 簡短說明預防方式

### Completed Features
- 列出已完成的 Feature 及其核心能力
- 幫助 AI 避免重複實作

---

## 與完整版的關係

| 層級 | 檔案 | 篇幅 | 用途 |
|------|------|------|------|
| **Layer 1** | `.flowkit/memory/system-context-index.md` | 50-150 行 | 每次 AI 對話自動注入 |
| **Layer 2** | `.flowkit/memory/system-context.md` | 300-700 行 | 需要深入了解時引用 |

Layer 1 是 Layer 2 的「摘要索引版」，當 AI 需要更多細節時，會去 Layer 2 查找。
