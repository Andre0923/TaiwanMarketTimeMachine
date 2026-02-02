# 通用型漸進式高遵從度 Prompt Template

> **撰寫時間**：2026-01-08  
> **參考來源**：  
> - 通用性AI高遵從度Prompt的關鍵特點分析.md  
> - 27.Copilot 最終認知-漸進式揭露最佳實踐_Opus4.5.md  
> **用途**：作為設計高遵從度 + 漸進式揭露 AI Prompt 的標準模板

---

## 模板設計理念

本模板整合兩大核心能力：

| 能力 | 來源 | 效果 |
|------|------|------|
| **高遵從度** | Spec Kit Agent 設計模式 | AI 行為穩定、可預測 |
| **漸進式揭露** | Progressive Disclosure Protocol | Token 高效、行為可審計 |

> **核心公式**：  
> 高遵從度 = MUST/MUST NOT + 結構化 Phase + 驗證迴圈 + 錯誤處理  
> 漸進式揭露 = Gatekeeper + 兩段解析度 + Escalation Log

---

## 部署平台格式說明

> ⚠️ **重要**：不同平台的 Agent 檔案格式不同，請依目標平台選擇正確格式。

### GitHub Copilot（`.github/agents/`）

GitHub Copilot Agent 需要 **YAML Frontmatter**，放在檔案最開頭：

```markdown
---
description: 一句話說明此 Agent 的用途
handoffs:
  - label: 相關操作的顯示名稱
    agent: 目標Agent名稱（不含.agent.md）
    prompt: 觸發該 Agent 的預設 prompt
---

# Agent 標題

[Agent 內容...]
```

**範例**：

```markdown
---
description: 從 PRD 擷取與目標 Milestone 相關的設計上下文
handoffs:
  - label: 執行 Plan
    agent: speckit.plan
    prompt: 開始規劃實作方案
  - label: 檢查一致性
    agent: flowkit.consistency-check
    prompt: 檢查 Plan 與 System 的一致性
---

# FlowKit Milestone Context Extractor

[Agent 內容...]
```

### Cursor（`.cursor/commands/`）

Cursor 命令檔案**不需要 YAML Frontmatter**，直接使用 Markdown：

```markdown
# Agent 標題

> **用途**：...
> **版本**：...

[Agent 內容...]
```

### 格式對照表

| 平台 | 路徑 | 檔名格式 | YAML Frontmatter |
|------|------|----------|------------------|
| GitHub Copilot | `.github/agents/` | `xxx.agent.md` | ✅ 必須 |
| Cursor | `.cursor/commands/` | `xxx.md` | ❌ 不需要 |
| 範本存放 | `77.repo-Template/docs/AI指令化檔案_部屬用/` | `xxx.agent.md` | 視需求 |

---

## 完整模板

```markdown
# [Prompt 名稱]

> **用途**：[一句話說明此 Prompt 的目的]  
> **觸發時機**：[何時使用此 Prompt]  
> **版本**：[版本號]

---

## 使用者輸入

```text
$ARGUMENTS
```

在繼續執行之前，您**必須（MUST）**考慮使用者輸入（若非空白）。

---

## 目標

[明確列出此 Prompt 要達成的目標]

1. [目標 1]
2. [目標 2]
3. [目標 3]

---

## 操作限制

### 核心原則

[一句話說明核心操作原則]

### AI MUST

- [強制要求 1]
- [強制要求 2]
- [強制要求 3]
- **遵循 Progressive Disclosure Protocol（漸進式揭露協議）**

### AI MUST NOT

- [禁止事項 1]
- [禁止事項 2]
- [禁止事項 3]
- **預防性擴讀（在資料充足時讀取超出必要範圍的內容）**
- **在資料不足時進行推測或猜測**

---

## Progressive Disclosure Protocol（漸進式揭露協議）

> **本協議確保 AI 行為可控、可追溯、可驗證。**

### 核心原則

```
┌─────────────────────────────────────────────────────────────┐
│  資料不足 → 停止並報告，不猜測                              │
│  先低解析度掃描 → 再針對候選項目深讀                        │
│  每次深讀必須記錄原因（可審計）                             │
└─────────────────────────────────────────────────────────────┘
```

### 最小載入清單（Minimal Load List）

**在各 Phase 執行時，僅讀取以下指定項目：**

| 來源 | 僅讀取 | 不讀取 |
|------|--------|--------|
| [檔案類型 1] | [指定欄位/區段] | [排除項目] |
| [檔案類型 2] | [指定欄位/區段] | [排除項目] |
| [檔案類型 3] | [指定欄位/區段] | [排除項目] |

### 分階段解析度（Progressive Resolution）

#### Stage 1：結構掃描（Structural Scan）

**讀取範圍**：
- Headers / Section Titles
- Metadata / IDs / Keywords
- Change Markers / Flags

**輸出**：
- 初步地圖 / 候選清單
- 待深讀區段標記

**約束**：
- 此階段**不讀取**段落內文
- 只建立對應關係

#### Stage 2：針對性深讀（Targeted Deep Read）

**觸發條件**：僅對 Stage 1 標記的候選項目執行

**讀取範圍**：
- 候選區段的完整內容
- 相鄰 3-5 行（上下文理解）

**約束**：
- 每次深讀**必須**記錄至 Escalation Log
- 不擴展至未標記區段

### Escalation Log 格式（必須包含於輸出）

```markdown
## Escalation Log（深讀記錄）

| 階段 | 目標位置 | 深讀原因 | 讀取範圍 |
|------|----------|----------|----------|
| Phase X | [file:line-range] | [具體原因] | N lines |
| ... | ... | ... | ... |

**總深讀次數**：N  
**最小 Context 完成率**：X%（Stage 1 即完成的項目佔比）
```

若無需深讀：
```markdown
## Escalation Log
Analysis completed within minimal context constraints.
Total deep reads: 0
```

---

## 執行步驟

### Phase 0：前置條件檢查 + 資料健康檢查（Gatekeeper）

**輸入**：$ARGUMENTS

**執行**：

#### 0.1 環境檢查

1. **[檢查項目 1]**：
   ```bash
   [檢查指令]
   ```
   - 若失敗 → ERROR「[錯誤訊息]」

2. **[檢查項目 2]**：
   - 必須存在：[檔案/目錄列表]
   - 若缺少 → ERROR「[錯誤訊息]」

#### 0.2 資料健康檢查（Gatekeeper）🔒

**在進入 Phase 1 之前，必須執行以下檢查：**

```markdown
### Data Health Check

**[資料類型 1] 完整性：**
- [ ] [檢查項目 1.1]
- [ ] [檢查項目 1.2]

**[資料類型 2] 可操作性：**
- [ ] [檢查項目 2.1]
- [ ] [檢查項目 2.2]
```

**失敗協議（Failure Protocol）：**

```
IF any check fails:
  → STOP immediately
  → Output: "INSUFFICIENT DATA: [specific issue]"
  → Recommend: "[specific action to fix]"
  → Do NOT proceed with guessing
```

**輸出**：前置條件檢查通過

**驗證**：
- [ ] 環境檢查通過
- [ ] 資料健康檢查通過

若任一項失敗 → 中止並報告具體缺失

---

### Phase 1：[階段名稱] —— 低解析度掃描

**輸入**：[輸入來源]

**執行（遵循 Stage 1 規範）**：

#### 1.1 結構掃描（Headers Only）

1. **[操作 1]**：
   - **僅讀取**：[指定項目]
   - **不讀取**：[排除項目]

2. **建立初步清單**：

   | 類別 | 是否相關 | 候選區段 |
   |------|----------|----------|
   | [類別 1] | Yes/No | [Section refs] |
   | [類別 2] | Yes/No | [Section refs] |

#### 1.2 針對性深讀（Triggered by Stage 1）

3. **僅對「Yes」的類別執行深讀**：
   - 讀取候選區段完整內容
   - 記錄至 Escalation Log

4. **[具體處理步驟]**：
   - [步驟描述]

**輸出**：[本階段產物]

**驗證**：
- [ ] [驗證項目 1]
- [ ] [驗證項目 2]
- [ ] Escalation Log 已記錄本 Phase 的深讀項目

---

### Phase 2：[階段名稱] —— 漸進式處理

**輸入**：[上一階段產物]

**執行（遵循 Progressive Resolution 規範）**：

#### 2.1 定位階段（Stage 1）

1. **掃描結構**：
   - **僅讀取**：Section Headers
   - 建立對應表

2. **標記需要深讀的區段**：
   - 有對應項目 → 標記「待深讀」
   - 無對應 → 標記「保留（不讀取）」

#### 2.2 處理階段（Stage 2）

3. **僅對「待深讀」區段執行**：

   | 操作類型 | 處理方式 |
   |----------|----------|
   | [操作 1] | [處理方式] |
   | [操作 2] | [處理方式] |
   | **保留** | **MUST 完整保留，不讀取不修改** |

**輸出**：[本階段產物]

**驗證檢查清單**：

```markdown
## [Phase 名稱] 驗證

- [ ] [驗證項目 1]
- [ ] [驗證項目 2]
- [ ] 未涉及區段確認未被修改
- [ ] Escalation Log 記錄完整
```

**驗證流程**：
1. 逐項檢查上述清單
2. 若任一項失敗 → 記錄問題，進行修正
3. 重新執行驗證（最多 3 次迭代）
4. 若 3 次後仍失敗 → ERROR「[錯誤訊息]」並列出具體問題

---

### Phase N：[最終階段]

[依照上述模式繼續...]

---

## 完成標準（Definition of Done）

統合流程僅在下列條件**全部符合**時視為完成：

```markdown
## DoD 檢查清單

### 必要條件
- [ ] [必要條件 1]
- [ ] [必要條件 2]
- [ ] [必要條件 3]
- [ ] Escalation Log 已完整記錄

### 禁止殘留
- [ ] [禁止項目 1]
- [ ] [禁止項目 2]
- [ ] 無預防性擴讀（非必要的深讀記錄）
```

**最終驗證**：
1. 逐項檢查 DoD 清單
2. 若任一項失敗 → 返回對應 Phase 修正
3. 全部通過 → 報告完成

---

## 錯誤處理

| 錯誤情境 | 嚴重性 | 處理方式 |
|----------|--------|----------|
| [錯誤 1] | CRITICAL | ERROR + [處理方式] |
| [錯誤 2] | HIGH | ERROR + [處理方式] |
| 資料健康檢查失敗 | CRITICAL | STOP + 指出具體缺失 + 不進行猜測 |
| 驗證失敗（3次） | HIGH | ERROR + 列出問題，建議人工介入 |

### 嚴重性定義

| 級別 | 定義 | 處理 |
|------|------|------|
| CRITICAL | 阻擋性問題，無法繼續 | 必須修正後重新執行 |
| HIGH | 重要問題，影響品質 | 必須修正，返回對應 Phase |
| MEDIUM | 中等問題 | 記錄，建議修正 |
| LOW | 輕微問題 | 記錄，可選修正 |

---

## 輸出格式

完成後，輸出以下結構：

```markdown
## [Prompt 名稱] 執行結果

### 狀態：[成功 / 失敗]

### 執行摘要
- [摘要項目 1]：[值]
- [摘要項目 2]：[值]
- 執行時間：[timestamp]

### Phase 執行結果
| Phase | 狀態 | 備註 |
|-------|------|------|
| Phase 0：前置檢查 + Gatekeeper | ✅/❌ | [備註] |
| Phase 1：[名稱] | ✅/❌ | [備註] |
| Phase 2：[名稱] | ✅/❌ | [備註] |
| ... | ... | ... |

### Escalation Log（深讀記錄）
| 階段 | 目標位置 | 深讀原因 | 讀取範圍 |
|------|----------|----------|----------|
| ... | ... | ... | ... |

**總深讀次數**：N  
**最小 Context 完成率**：X%

### DoD 檢查結果
[完整檢查清單，標記 ✅/❌]

### 下一步
- [ ] [建議行動 1]
- [ ] [建議行動 2]
```

---

## 快速參考

### 設計檢查清單

使用此模板設計 Prompt 時，確認包含：

**高遵從度要素**：
- [ ] 使用 MUST/MUST NOT 強制性語言
- [ ] Phase 結構化執行流程
- [ ] 每個 Phase 有輸入/執行/輸出/驗證
- [ ] 驗證迴圈（最多 N 次迭代）
- [ ] 錯誤處理表
- [ ] 嚴重性分級
- [ ] DoD 檢查清單
- [ ] 固定輸出格式

**漸進式揭露要素**：
- [ ] Gatekeeper（資料健康檢查）
- [ ] 最小載入清單（Minimal Load List）
- [ ] 兩段解析度（Stage 1 掃描 → Stage 2 深讀）
- [ ] Escalation Log 要求
- [ ] 禁止預防性擴讀
- [ ] 禁止資料不足時猜測

### 關鍵規則速查

| 規則 | 說明 |
|------|------|
| 資料不足即停止 | Gatekeeper 失敗 → STOP，不猜測 |
| 先掃描再深讀 | Stage 1 結構 → Stage 2 內容 |
| 深讀必記錄 | 每次深讀寫入 Escalation Log |
| 驗證有上限 | 最多 3 次迭代 |
| 錯誤有分級 | CRITICAL > HIGH > MEDIUM > LOW |
| 輸出有格式 | 使用固定模板 |
```

---

## 模板使用指南

### Step 1：複製模板

複製上方完整模板到新檔案。

### Step 2：填入基本資訊

- 替換 `[Prompt 名稱]`、`[用途]`、`[觸發時機]`
- 定義具體目標

### Step 3：設計操作限制

- 列出 MUST 和 MUST NOT
- 保留漸進式揭露相關的限制

### Step 4：定義最小載入清單

- 根據任務需求，明確哪些資料「僅讀取」
- 明確哪些資料「不讀取」

### Step 5：設計 Phase 流程

- Phase 0 必須包含 Gatekeeper
- 每個 Phase 遵循 Stage 1 → Stage 2 模式
- 每個 Phase 有驗證檢查清單

### Step 6：定義錯誤處理

- 窮舉可能的錯誤情境
- 為每個錯誤指定嚴重性和處理方式

### Step 7：設計輸出格式

- 確保包含 Escalation Log
- 確保包含 DoD 檢查結果

---

## 效益總結

| 效益 | 來源 | 說明 |
|------|------|------|
| 行為穩定 | 高遵從度設計 | MUST/MUST NOT 減少模糊空間 |
| 結果可預測 | 結構化 Phase | 每次執行流程一致 |
| Token 高效 | 漸進式揭露 | 只讀必要內容 |
| 行為可審計 | Escalation Log | 知道 AI 讀了什麼、為什麼 |
| 品質有保證 | 驗證迴圈 | 不通過會重試 |
| 錯誤可處理 | 錯誤處理表 | 預定義所有失敗情境 |
