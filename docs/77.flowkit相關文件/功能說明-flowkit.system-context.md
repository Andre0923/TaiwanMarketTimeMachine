# 功能說明：flowkit.system-context

> **FlowKit 套件文件**  
> **版本**：1.4.0  
> **最後更新**：2025-01-31

---

## 概述

`flowkit.system-context` 是 FlowKit 套件中用於**產生系統上下文文件**的指令化工具。它能從專案的 System Spec、程式碼結構等來源，產生兩層架構的上下文文件，幫助 AI 快速理解專案全貌。

---

## 使用場景

### 最佳使用時機

1. **Feature 開發期間**：specify 之後、plan 之前執行（**建議必要**，除非是第一個 Feature）
2. **Unify Flow 完成後**：選擇性更新（若規劃下一階段需要才執行，否則統一在下一個 Feature 的 spec 後執行）
3. **專案初始化後**：建立初始的系統上下文

### 典型工作流程

**推薦流程（Feature 開發期間）**：
```
執行 /speckit.specify
     ↓
執行 /flowkit.system-context ← **建議必要**
     ↓
執行 /speckit.plan
     ↓
...
```

**選擇性流程（Unify Flow 後）**：
```
Feature 開發完成
     ↓
執行 /flowkit.unify-flow 合併至 System
     ↓
執行 /flowkit.system-context ← 選擇性（可延後）
     ↓
AI 獲得最新的專案上下文
```

---

## 核心功能

### 1. 兩層架構設計

| 層級 | 檔案 | 篇幅 | 用途 |
|------|------|------|------|
| **Layer 1** | `.flowkit/memory/system-context-index.md` | 50-150 行 | 每次 AI 對話自動注入 |
| **Layer 2** | `.flowkit/memory/system-context.md` | 300-700 行 | 需要深入了解時引用 |

### 2. 解決的問題

| 問題 | 解決方式 |
|------|----------|
| AI 不了解專案架構 | 提供模組邊界、入口點清單 |
| AI 重複實作已有功能 | 提供共享服務清單、已完成 Feature 清單 |
| AI 不知道去哪找程式碼 | 提供 Where-to-Look 查找表 |
| AI 不遵守專案規範 | 提供 NON-NEGOTIABLE 強制規範 |
| AI 踩到已知的坑 | 提供 Known Pitfalls 陷阱清單 |

### 3. 完整版十大章節

| 章節 | 內容 | 來源 |
|------|------|------|
| 1. 專案定位 | 一句話描述、核心價值 | README + spec.md |
| 2. 系統架構 | 架構圖、模組邊界、入口點 | src/ 結構 |
| 3. Feature 清單 | 已完成/進行中的 Feature | specs/features/ |
| 4. 資料模型 | Entity 關係、關鍵欄位 | data-model.md |
| 5. 核心流程 | 主要流程路徑追蹤 | flows.md |
| 5.5 UI 設計摘要 | Screen/Pattern/State 索引 | specs/system/ui/ |
| 6. 技術棧與約定 | NON-NEGOTIABLE 清單 | pyproject.toml |
| 7. Where-to-Look | 依情境查找表 | 架構推導 |
| 8. 深入探索指引 | 文件路徑索引 | 文件結構 |
| 9. AI 開發提示 | Known Pitfalls、Checklist | 累積經驗 |
| 10. 版本歷史 | 更新記錄 | 自動產生 |

---

## 使用方式

### CLI 風格

```bash
# 更新現有系統上下文（預設）
/flowkit.system-context

# 初始化新專案的系統上下文
/flowkit.system-context --init
```

### 自然語言

```
幫我更新專案上下文
產生系統上下文文件
初始化專案的 AI 上下文
```

---

## 輸入來源

| 來源 | 讀取內容 |
|------|----------|
| `README.md` | 專案描述 |
| `specs/system/spec.md` | Overview、User Stories 摘要 |
| `specs/system/data-model.md` | Entity 標題、關係 |
| `specs/system/flows.md` | 流程標題 |
| `specs/system/ui/` | Screen/Pattern/State 索引 |
| `specs/features/` | Feature 清單與狀態 |
| `src/` | 目錄結構、模組邊界 |

---

## 輸出格式

### 完整版

結構化的系統上下文，包含十大章節，詳見範本。

### 精簡版

壓縮至 50-150 行的索引版本：

```markdown
# System Context Index v{VERSION}

## One-liner
{一句話描述}

## Boundaries
{模組邊界清單}

## Entry Points
{入口點清單}

## Shared Services
{共享模組清單}

## Golden Flows
{核心流程摘要}

## Where-to-Look
{情境查找表}

## NON-NEGOTIABLE
{強制規範}

## Known Pitfalls
{常見陷阱}

## Full Context
See: `.flowkit/memory/system-context.md`
```

---

## 與其他 FlowKit 工具的關係

| 工具 | 關係 | 說明 |
|------|------|------|
| `flowkit.unify-flow` | 前置 | Unify 完成後執行本工具更新上下文 |
| `speckit.plan` | 後續 | Plan 階段可參考系統上下文 |
| `speckit.specify` | 後續 | Specify 階段可參考系統上下文 |

---

## 部署位置

| 平台 | 位置 |
|------|------|
| GitHub Copilot Agent | `.github/agents/flowkit.system-context.agent.md` |
| GitHub Copilot Prompt | `.github/prompts/flowkit.system-context.prompt.md` |
| Cursor Command | `.cursor/commands/flowkit.system-context.md` |

### 範本位置

| 範本 | 位置 |
|------|------|
| 完整版範本 | `.flowkit/templates/system-context-template.md` |
| 精簡版範本 | `.flowkit/templates/system-context-index-template.md` |

### 產出位置

| 檔案 | 位置 |
|------|------|
| 完整版 | `.flowkit/memory/system-context.md` |
| 精簡版 | `.flowkit/memory/system-context-index.md` |

---

## 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 1.2.0 | 2025-01-26 | 重命名為 system-context（原 project-context） |
| 1.1.0 | 2025-01-20 | 新增 UI 設計摘要章節 |
| 1.0.0 | 2025-01-15 | 初始版本 |

---

## 相關文件

- [FlowKit 功能說明總覽](./README.md)
- [FlowKit Unify Flow 功能說明](./功能說明-flowkit.unify-flow.md)
- [SDD 開發流程指南](../01.開發人員doc/03.SDD開發流程指南.md)
