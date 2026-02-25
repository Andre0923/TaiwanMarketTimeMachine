---
description: 在 Unify Flow 完成後，產生或更新系統上下文文件
handoffs:
  - label: 開始規格撰寫
    agent: speckit.specify
    prompt: 根據系統上下文開始撰寫 Feature Spec
  - label: 開始實作規劃
    agent: speckit.plan
    prompt: 根據已完成的 Spec 開始規劃實作
---

# FlowKit System Context

> **用途**：產生或更新系統上下文文件，為 Plan 階段準備專案全域上下文  
> **觸發時機**：  
> - **Feature 開發期間**：specify 之後、plan 之前（**建議必要**，除非是第一個 Feature）  
> - **Unify Flow 完成後**：選擇性更新（可延後到下一個 Feature 的 spec 後執行）  
> **版本**：1.4.0

---

## 使用者輸入

```text
$ARGUMENTS
```

> 💡 **`--default` 模式**：輸入 `--default` 等同於無額外指示，直接執行預設流程。

若 `$ARGUMENTS` 為空或 `--default`，預設執行「更新現有 system-context.md」；若包含 `--init`，則執行「初始化新系統上下文」。

---

## 目標

產生或更新兩層架構的系統上下文文件：

1. **完整版** (`.flowkit/memory/system-context.md`)：300-700 行，深入了解時引用
2. **精簡索引版** (`.flowkit/memory/system-context-index.md`)：50-150 行，每次 AI 對話自動注入

---

## 操作限制

### 核心原則

**索引優先、適度抽象**：提供足夠理解全貌的摘要，引導 AI 在需要時深入探索，而非複製完整規格內容。

### AI MUST

- 閱讀 `specs/system/spec.md`、`specs/system/data-model.md`、`specs/system/flows.md` 以收集資訊
- 掃描 `src/` 目錄結構以建立模組邊界表
- 掃描 `specs/features/` 以更新 Feature 清單
- 使用繁體中文撰寫所有內容
- 遵循 `.flowkit/templates/system-context-template.md` 的章節結構
- 在完整版附錄 A 產生精簡索引版
- 同步更新 `.flowkit/memory/system-context-index.md`
- **若在 Feature 開發期間執行**：更新當前 Feature 的 `spec.md` frontmatter，將 `system_context: false` 改為 `true`

### AI SHOULD

- 根據專案特性調整章節詳細程度
- 在「常見陷阱」中記錄本次 Feature 發現的新問題
- 在「共享模組清單」中補充新增的可複用服務
- 保持架構圖與實際程式碼結構一致

### AI MUST NOT

- 複製完整的 spec 內容（應只放索引路徑）
- 在精簡版中放入超過 150 行的內容
- 修改 `specs/system/` 下的任何檔案（本指令僅產出 context 文件）
- 忽略既有的 system-context.md 內容（應在其基礎上更新）

---

## 執行步驟

### Phase 0：前置檢查

**輸入**：`$ARGUMENTS`

**執行**：

1. **確認必要檔案存在**：
   - `specs/system/spec.md`
   - `specs/system/data-model.md`
   - `src/` 目錄
   - 若缺少 → WARNING 並盡可能繼續

2. **判斷執行模式**：
   - `--init` → 初始化模式（從範本建立）
   - 否則 → 更新模式（基於現有文件）

3. **載入現有 context（若存在）**：
   - 讀取 `.flowkit/memory/system-context.md`
   - 識別需要更新的章節

**輸出**：執行模式確認、需更新章節清單

---

### Phase 1：資訊收集（低解析度掃描）

**輸入**：專案檔案結構

**執行**：

#### 1.1 專案定位收集

- 讀取 `README.md` 的專案描述
- 讀取 `specs/system/spec.md` 的 Section 1 (Overview)

#### 1.2 架構資訊收集

- 掃描 `src/` 目錄結構（僅目錄名稱與主要檔案）
- 讀取 `specs/system/flows.md` 的流程標題

#### 1.3 Feature 清單收集

- 掃描 `specs/features/` 目錄
- 識別每個 Feature 的狀態（透過 ARCHIVED.md 或 spec.md）

#### 1.4 資料模型收集

- 讀取 `specs/system/data-model.md` 的 Entity 標題
- 識別核心實體關係

#### 1.5 UI 設計收集（若存在）

- 掃描 `specs/system/ui/` 目錄是否存在
- 若存在：
  - 讀取 `ui-structure.md` 的 Screen ID 與名稱
  - 讀取 `ux-guidelines.md` 的 Pattern/State ID
- 若不存在：標記「UI 設計尚未建立」

**輸出**：資訊收集清單（各類別的摘要）

---

### Phase 2：內容產生

**輸入**：Phase 1 收集的資訊

**執行**：

依照範本結構產生以下章節：

| 章節 | 內容來源 | 注意事項 |
|------|----------|----------|
| 1. 專案定位 | README + spec.md | 一句話描述須精煉 |
| 2. 系統架構 | src/ 結構 + flows.md | 架構圖使用 ASCII art |
| 3. Feature 清單 | specs/features/ | 標示狀態、核心能力 |
| 4. 資料模型 | data-model.md | 僅摘要，詳情引導至原文件 |
| 5. 核心流程 | flows.md | 包含路徑追蹤 |
| 5.5 UI 設計摘要 | specs/system/ui/ | 若存在，列出 Screen/Pattern/State 索引 |
| 6. 技術棧與約定 | pyproject.toml + .cursorrules | NON-NEGOTIABLE 清單 |
| 7. Where-to-Look | 根據架構推導 | 依情境查找表 |
| 8. 深入探索指引 | 文件路徑索引 | 只放路徑，不複製內容 |
| 9. AI 開發提示 | 累積的陷阱 + checklist | 更新時保留既有陷阱 |
| 10. 版本歷史 | 自動產生 | 記錄本次更新 |

**輸出**：完整版 system-context.md 內容

---

### Phase 3：精簡版產生

**輸入**：Phase 2 產生的完整版

**執行**：

從完整版提取以下區段，壓縮至 50-150 行：

```markdown
# System Context Index v{VERSION}

## One-liner
{一句話描述}

## Boundaries
{模組邊界清單，每行一個模組}

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

**輸出**：system-context-index.md 內容

---

### Phase 4：輸出與驗證

**輸入**：Phase 2 + Phase 3 的內容

**執行**：

1. **寫入完整版**：`.flowkit/memory/system-context.md`
2. **寫入精簡版**：`.flowkit/memory/system-context-index.md`
3. **執行驗證清單**

**驗證清單**：

```markdown
## System Context 驗證

### 完整版檢查
- [ ] 包含所有 10 個章節
- [ ] 架構圖與 src/ 結構一致
- [ ] Feature 清單與 specs/features/ 一致
- [ ] 所有路徑索引指向存在的檔案
- [ ] 篇幅在 300-700 行之間

### 精簡版檢查
- [ ] 包含所有必要區段
- [ ] 篇幅在 50-150 行之間
- [ ] 最後一行指向完整版路徑

### 一致性檢查
- [ ] 兩版本的 One-liner 相同
- [ ] 兩版本的 Boundaries 相同
- [ ] 版本號一致
```

**輸出**：驗證結果

---

## 完成標準 (Definition of Done)

統合流程僅在下列條件**全部符合**時視為完成：

### 必要條件
- [ ] `.flowkit/memory/system-context.md` 已產生/更新
- [ ] `.flowkit/memory/system-context-index.md` 已產生/更新
- [ ] 兩版本內容一致
- [ ] 版本歷史已更新
- [ ] **若在 Feature 開發期間執行：當前 Feature 的 `spec.md` frontmatter 中 `system_context: false` 已改為 `true`**

### 品質條件
- [ ] 完整版篇幅 300-700 行
- [ ] 精簡版篇幅 50-150 行
- [ ] 所有路徑索引有效

---

## 錯誤處理

| 錯誤情境 | 嚴重性 | 處理方式 |
|----------|--------|----------|
| spec.md 不存在 | HIGH | 警告並嘗試從 README 推導 |
| data-model.md 不存在 | MEDIUM | 略過資料模型章節，標記待補充 |
| src/ 結構異常 | HIGH | 報告問題，建議人工確認 |
| 現有 system-context.md 格式不符 | MEDIUM | 嘗試遷移，保留原始內容 |

---

## 輸出格式

完成後，輸出以下結構：

```markdown
## FlowKit System Context 執行結果

### 狀態：[成功 / 部分成功 / 失敗]

### 執行摘要
- 執行模式：[初始化 / 更新]
- 完整版位置：`.flowkit/memory/system-context.md`
- 精簡版位置：`.flowkit/memory/system-context-index.md`
- 完整版行數：[N] 行
- 精簡版行數：[N] 行
- **spec.md frontmatter 更新**：[是 / 否 / 不適用]  # 若在 Feature 開發期間執行

### 主要變更
- [變更項目 1]
- [變更項目 2]

### 驗證結果
[驗證清單，標記 ✅/❌]

### 建議下一步
- [ ] 將精簡版內容加入 Agent Context
- [ ] 確認架構圖與實際結構一致
- [ ] 補充遺漏的陷阱記錄
- [ ] 若在 Feature 開發中，繼續執行 `/speckit.plan` 以使用 system-context
```

---

## 範本與參考

- **完整版範本**：`.flowkit/templates/system-context-template.md`
- **精簡版範本**：`.flowkit/templates/system-context-index-template.md`
- **執行時機**：Unify Flow 完成後

