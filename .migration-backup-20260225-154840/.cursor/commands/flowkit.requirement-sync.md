# FlowKit Requirement Sync

> **用途**：將 Feature 開發過程中的調整修正，同步回寫至 PRD 與 User Stories 需求文件  
> **觸發時機**：Unify Flow 執行前（Pre-Unify Check 前或後）  
> **套件**：FlowKit  
> **版本**：1.0.0

---

## 使用者輸入

```text
$ARGUMENTS
```

在繼續執行之前，您**必須（MUST）**考慮使用者輸入（若非空白）。

支援的參數：
- `--feature <path>`：指定 Feature 目錄路徑
- `--dry-run`：僅分析不修改，輸出變更預覽
- `--auto`：自動合併所有刻意修正，不逐項確認

---

## 目標

在 Feature Spec 合併到 System Spec 之前，確保**需求文件的一致性**：

1. **變更偵測**：比對 Feature spec.md 與原始 PRD-*.md / User Stories 的差異
2. **意圖判斷**：區分「刻意修正」與「非意圖不一致」
3. **回寫同步**：將刻意修正回寫至需求文件，維持需求-規格-實作的一致性

### 核心價值

```
「需求文件是源頭，Feature 開發中的合理調整應回饋至需求，
確保 PRD 與 User Stories 始終反映最新的設計決策」
```

### 與其他 FlowKit 指令的關係

| 指令 | 時機 | 關係 |
|------|------|------|
| `/flowkit.consistency-check` | Plan 後 | 檢查 Plan 與 System 的一致性 |
| `/flowkit.requirement-sync` | Unify 前 | 將 Feature 變更回寫至需求文件（**本指令**） |
| `/flowkit.pre-unify-check` | Unify 前 | 檢查 Spec 品質與實作對齊 |
| `/flowkit.unify-flow` | 驗證通過後 | 合併 Feature 至 System |

---

## 操作限制

### 核心原則

**需求-規格雙向同步**：Feature 開發中的合理調整應回寫至需求文件，避免需求文件過時。

**最小變更原則**：僅回寫有變更的項目，未變更的內容保持原樣。

### AI MUST

- 比對 Feature Spec 與原始 PRD / User Stories 的差異
- 區分「刻意修正」與「非意圖不一致」
- 對刻意修正項目進行回寫
- 保留未涉及的需求內容不變
- **遵循 Progressive Disclosure Protocol（漸進式揭露協議）**
- 產生變更摘要報告

### AI MUST NOT

- 修改與 Feature 無關的需求內容
- 在不確定是否為刻意修正時自動回寫（應詢問使用者）
- 刪除 PRD / User Stories 中的內容（除非 Feature Spec 明確標記刪除）
- **預防性擴讀**（在資料充足時讀取超出必要範圍的內容）
- **在資料不足時進行推測或猜測**

### AI SHOULD

- 在回寫前顯示變更預覽
- 對可能有爭議的變更要求確認
- 建議後續執行 `/flowkit.pre-unify-check`

---

## Progressive Disclosure Protocol

### 最小載入清單

| 來源 | 僅讀取 | 不讀取 |
|------|--------|--------|
| **Feature spec.md** | User Stories、AC、變更標記 | 技術細節（除非涉及需求變更） |
| **Feature plan.md** | 變更決策摘要 | 實作細節 |
| **PRD-*.md** | Feature 相關的章節 | 無關章節 |
| **User Stories** | Feature 涉及的 US Group | 無關的 US Group |

### 分階段解析度

#### Stage 1：結構掃描（Structural Scan）

**讀取範圍**：
- Feature spec.md 的 User Story IDs、AC IDs
- PRD-*.md 的章節標題、功能清單
- User Stories 的 US ID、AC ID

**輸出**：
- 對應關係表（Feature US → PRD 章節 / US 檔案）
- 待深讀區段標記

**約束**：
- 此階段**不讀取**段落內文
- 只建立 ID 對應關係

#### Stage 2：針對性深讀（Targeted Deep Read）

**觸發條件**：僅對 Stage 1 標記的對應區段執行

**讀取範圍**：
- Feature spec.md 中的 User Story / AC 完整內容
- PRD-*.md 中對應功能的描述
- User Stories 中對應 US / AC 的完整內容

**約束**：
- 每次深讀**必須**記錄至 Escalation Log
- 不擴展至未標記區段

### Escalation Log 格式

```markdown
## Escalation Log（深讀記錄）

| 階段 | 目標位置 | 深讀原因 | 讀取範圍 |
|------|----------|----------|----------|
| Phase X | [file:section] | [具體原因] | N lines |

**總深讀次數**：N  
**最小 Context 完成率**：X%
```

---

## 執行步驟

### Phase 0：前置條件檢查 + 資料健康檢查（Gatekeeper）

**輸入**：$ARGUMENTS

**執行**：

#### 0.1 環境檢查

1. **確認 Feature 目錄存在**：
   - 必須包含：`spec.md`
   - 建議包含：`plan.md`（用於理解變更意圖）

2. **確認需求文件存在**：
   - `docs/requirements/PRD-*.md`（至少一個）
   - `docs/requirements/user-stories/`（目錄存在）

3. **讀取 Feature Spec 的基本資訊**：
   - Feature ID
   - 涉及的 User Story IDs
   - 變更類型（新增 / 修改 / 刪除）

#### 0.2 資料健康檢查（Gatekeeper）🔒

```markdown
### Data Health Check

**Feature Spec 完整性：**
- [ ] spec.md 存在且可讀取
- [ ] 包含至少一個 User Story 定義
- [ ] User Story 有明確的 AC 定義

**需求文件可操作性：**
- [ ] PRD-*.md 存在
- [ ] User Stories 目錄存在
- [ ] 檔案可寫入（非唯讀）
```

**失敗協議**：

```
IF any check fails:
  → STOP immediately
  → Output: "INSUFFICIENT DATA: [specific issue]"
  → Recommend: "[specific action to fix]"
  → Do NOT proceed with guessing
```

**輸出**：前置條件檢查通過、Feature 基本資訊

---

### Phase 1：建立對應關係 —— 低解析度掃描

**輸入**：Feature spec.md、PRD-*.md、User Stories

**執行（遵循 Stage 1 規範）**：

#### 1.1 掃描 Feature Spec 結構

1. **抽取 User Story 清單**：
   - US ID（如 US-A-1、US-B-2）
   - US 標題
   - AC IDs

2. **識別變更標記**：
   - `[NEW]`：新增
   - `[MODIFIED]`：修改
   - `[DELETED]`：刪除

#### 1.2 掃描需求文件結構

1. **PRD-*.md**：
   - 章節標題（## / ### 層級）
   - 功能清單項目

2. **User Stories**：
   - README.md 索引
   - US-X-*.md 檔案清單
   - 各檔案中的 US ID

#### 1.3 建立對應表

| Feature US | 變更類型 | 對應 PRD 章節 | 對應 US 檔案 | 對應狀態 |
|------------|----------|---------------|--------------|----------|
| US-A-1 | MODIFIED | PRD.md#功能A | US-A-xxx.md | ✅ 找到 |
| US-B-1 | NEW | - | - | ⚠️ 新增項目 |
| US-C-2 | DELETED | PRD.md#功能C | US-C-xxx.md | ⚠️ 待刪除 |

**輸出**：US-需求文件對應表、待深讀區段清單

---

### Phase 2：差異比對 —— 針對性深讀

**輸入**：對應表、標記為「待深讀」的區段

**執行（遵循 Stage 2 規範）**：

#### 2.1 逐項深讀比對

對每個「MODIFIED」的 US：

1. **讀取 Feature Spec 中的完整 US/AC 內容**
2. **讀取對應 User Story 檔案中的原始 US/AC 內容**
3. **比對差異**：

   | 比對項目 | 差異類型 |
   |----------|----------|
   | US 標題 | 相同 / 不同 |
   | As a / I want / So that | 相同 / 不同 |
   | AC 數量 | 相同 / 新增 / 減少 |
   | AC 內容（Given/When/Then） | 相同 / 不同 |

4. **記錄至 Escalation Log**

#### 2.2 PRD 對應檢查

對涉及 PRD 描述變更的項目：

1. **讀取 Feature Spec 中的相關描述**
2. **讀取 PRD 中的對應章節**
3. **比對差異**：
   - 功能描述是否一致
   - 範圍是否一致
   - 限制條件是否一致

**輸出**：差異清單（含具體內容差異）

---

### Phase 3：意圖判斷

**輸入**：差異清單

**執行**：

#### 3.1 差異分類

| 分類 | 判斷依據 | 處理方式 |
|------|----------|----------|
| **刻意修正** | Feature Spec 有明確變更標記、Plan 有說明、合理的設計調整 | 自動回寫 |
| **澄清補充** | 內容更詳細但語意相同 | 建議回寫 |
| **非意圖不一致** | 無變更標記、疑似遺漏或錯誤 | 詢問使用者 |
| **格式差異** | 僅格式不同，語意相同 | 忽略 |

#### 3.2 判斷邏輯

```
FOR each difference:
  IF Feature Spec 有 [MODIFIED] 標記:
    → 分類為「刻意修正」
  ELSE IF Plan 有相關變更說明:
    → 分類為「刻意修正」
  ELSE IF 差異為「更詳細」而非「不同」:
    → 分類為「澄清補充」
  ELSE IF 差異為純格式（空白、標點）:
    → 分類為「格式差異」
  ELSE:
    → 分類為「非意圖不一致」
```

#### 3.3 產生分類報告

```markdown
## 差異分類結果

### 刻意修正（自動回寫）
| 項目 | 原始內容摘要 | 修正後內容摘要 |
|------|--------------|----------------|
| US-A-1 AC2 | Given... | Given...（更新） |

### 澄清補充（建議回寫）
| 項目 | 原始內容摘要 | 補充內容摘要 |
|------|--------------|--------------|
| US-B-1 標題 | 功能描述 | 更詳細的描述 |

### 非意圖不一致（需確認）
| 項目 | 原始內容摘要 | Feature 內容摘要 | 建議 |
|------|--------------|------------------|------|
| US-C-1 AC1 | Given X | Given Y | 確認哪個正確 |
```

**輸出**：差異分類報告

---

### Phase 4：回寫執行

**輸入**：差異分類報告、使用者確認（若需要）

**執行**：

#### 4.1 確認流程

**若有「非意圖不一致」項目**：

```markdown
⚠️ 發現以下不一致需要您確認：

1. **US-C-1 AC1**
   - 原始：Given 使用者已登入
   - Feature：Given 使用者已驗證身份
   
   請選擇：
   - [A] 採用 Feature 版本（回寫至需求）
   - [B] 保留原始版本（Feature 應修正）
   - [S] 跳過此項目
```

**若使用 `--auto` 參數**：
- 「刻意修正」和「澄清補充」自動回寫
- 「非意圖不一致」跳過並記錄

#### 4.2 回寫操作

對每個確認要回寫的項目：

1. **User Stories 回寫**：
   - 定位對應的 US-X-*.md 檔案
   - 找到對應的 US / AC 區段
   - 以 Feature Spec 的內容取代原內容
   - 更新 README.md 索引（若 US 標題變更）

2. **PRD 回寫**：
   - 定位對應的 PRD-*.md 檔案
   - 找到對應的功能描述區段
   - 以 Feature 調整後的描述取代原內容

3. **新增項目處理**：
   - 若 Feature 有新的 US，在對應 US Group 檔案中新增
   - 若 Feature 涉及 PRD 新章節，在 PRD 中新增

4. **刪除項目處理**：
   - 若 Feature 標記刪除某 US，在需求文件中標記為「已移除」或刪除
   - 更新 README.md 索引

#### 4.3 回寫驗證

```markdown
## 回寫驗證檢查清單

- [ ] User Stories 檔案語法正確（Markdown）
- [ ] PRD 檔案語法正確（Markdown）
- [ ] 更新的 US ID 在 README.md 中正確索引
- [ ] 無意外刪除的內容
- [ ] 變更區段與預覽一致
```

**驗證流程**：
1. 逐項檢查上述清單
2. 若任一項失敗 → 記錄問題，進行修正
3. 重新執行驗證（最多 3 次迭代）

**輸出**：回寫完成確認

---

### Phase 5：產生同步報告

**輸入**：所有處理結果

**執行**：

```markdown
## FlowKit Requirement Sync 報告

### 基本資訊
- **Feature**：[NNN-feature-name]
- **執行時間**：[timestamp]
- **執行模式**：[標準 / dry-run / auto]

### 同步摘要

| 類別 | 數量 | 說明 |
|------|------|------|
| 刻意修正（已回寫） | N | 自動回寫完成 |
| 澄清補充（已回寫） | N | 經確認回寫 |
| 非意圖不一致（已處理） | N | 經使用者決策 |
| 非意圖不一致（跳過） | N | 需人工處理 |
| 格式差異（忽略） | N | 無需處理 |

### 修改的檔案

| 檔案 | 變更類型 | 變更項目 |
|------|----------|----------|
| docs/requirements/user-stories/US-A-xxx.md | 修改 | US-A-1 AC2 |
| docs/requirements/PRD-xxx.md | 修改 | 功能 A 描述 |

### Escalation Log
[深讀記錄]

### 待處理項目（若有）

| 項目 | 問題 | 建議 |
|------|------|------|
| US-C-1 | 需確認正確版本 | 人工審閱 |

### 下一步建議
- [ ] 審閱修改的需求文件
- [ ] 執行 `/flowkit.pre-unify-check`
- [ ] 執行 `/flowkit.unify-flow`
```

**輸出**：完整同步報告

---

## 完成標準（Definition of Done）

同步流程僅在下列條件**全部符合**時視為完成：

```markdown
## DoD 檢查清單

### 必要條件
- [ ] Feature Spec 與需求文件的 US/AC 對應關係已建立
- [ ] 所有「刻意修正」項目已回寫
- [ ] 所有「澄清補充」項目已處理（回寫或跳過）
- [ ] 「非意圖不一致」項目已決策或記錄
- [ ] 修改的檔案語法正確
- [ ] Escalation Log 已完整記錄

### 禁止殘留
- [ ] 無未處理的 MODIFIED 標記項目
- [ ] 無意外的內容刪除
- [ ] 無預防性擴讀（非必要的深讀記錄）
```

---

## 錯誤處理

| 錯誤情境 | 嚴重性 | 處理方式 |
|----------|--------|----------|
| Feature spec.md 不存在 | CRITICAL | STOP，指出需要 spec.md |
| 需求文件目錄不存在 | CRITICAL | STOP，指出需要建立需求文件 |
| 無法建立對應關係 | HIGH | 警告，列出無法對應的項目 |
| 回寫時檔案唯讀 | HIGH | STOP，指出需要修改檔案權限 |
| 回寫驗證失敗（3次） | HIGH | ERROR，列出問題，建議人工介入 |
| 資料健康檢查失敗 | CRITICAL | STOP，指出具體缺失 |

### 嚴重性定義

| 級別 | 定義 | 處理 |
|------|------|------|
| CRITICAL | 阻擋性問題，無法繼續 | 必須修正後重新執行 |
| HIGH | 重要問題，影響品質 | 必須處理，返回對應 Phase |
| MEDIUM | 中等問題 | 記錄，建議修正 |
| LOW | 輕微問題 | 記錄，可選修正 |

---

## 輸出格式

完成後，輸出以下結構：

```markdown
## FlowKit Requirement Sync 執行結果

### 狀態：[成功 / 部分成功 / 失敗]

### 執行摘要
- **Feature**：[NNN-feature-name]
- **執行時間**：[timestamp]
- **回寫項目數**：N
- **跳過項目數**：N

### Phase 執行結果
| Phase | 狀態 | 備註 |
|-------|------|------|
| Phase 0：前置檢查 | ✅/❌ | |
| Phase 1：建立對應關係 | ✅/❌ | |
| Phase 2：差異比對 | ✅/❌ | |
| Phase 3：意圖判斷 | ✅/❌ | |
| Phase 4：回寫執行 | ✅/❌ | |
| Phase 5：產生報告 | ✅/❌ | |

### Escalation Log
[深讀記錄]

### 修改的檔案清單
[檔案列表]

### DoD 檢查結果
[完整檢查清單]

### 下一步
- [ ] 執行 `/flowkit.pre-unify-check`
- [ ] 執行 `/flowkit.unify-flow`
```

---

## 快速參考

### CLI 用法

```bash
# 標準執行（互動模式）
/flowkit.requirement-sync

# 指定 Feature
/flowkit.requirement-sync --feature specs/features/001-xxx/

# 僅預覽，不修改
/flowkit.requirement-sync --dry-run

# 自動模式（刻意修正自動回寫）
/flowkit.requirement-sync --auto
```

### 自然語言用法

```
幫我同步需求文件
把 Feature 的變更回寫到 PRD
更新 User Stories 與 Feature 一致
檢查 Feature 與需求文件的差異
```

### 變更類型處理對照

| Feature Spec 標記 | 需求文件處理 |
|-------------------|--------------|
| `[NEW]` US/AC | 在對應檔案中新增 |
| `[MODIFIED]` US/AC | 更新對應內容 |
| `[DELETED]` US/AC | 標記刪除或移除 |
| 無標記但有差異 | 詢問使用者確認 |

### 檔案位置

| 用途 | 位置 |
|------|------|
| Feature Spec | `specs/features/NNN-xxx/spec.md` |
| PRD 文件 | `docs/requirements/PRD-*.md` |
| User Stories 索引 | `docs/requirements/user-stories/README.md` |
| User Stories 檔案 | `docs/requirements/user-stories/US-X-*.md` |
