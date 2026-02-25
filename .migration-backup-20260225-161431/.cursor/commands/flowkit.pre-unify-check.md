# FlowKit Pre-Unify Check

> **用途**：在執行 Unify Flow 之前，進行 Spec 品質驗證與非意圖性錯誤最終檢查  
> **觸發時機**：Unify Flow 執行前（實作完成後）  
> **套件**：FlowKit  
> **版本**：1.0.0

---

## 使用者輸入

```text
$ARGUMENTS
```

在繼續執行之前，您**必須（MUST）**考慮使用者輸入（若非空白）。

---

## 目標

在 Feature Spec 合併到 System Spec 之前，確保：

1. **Spec 品質**：Feature Spec 結構完整、格式正確
2. **實作對齊**：Spec 與實作結果一致
3. **最終攔截**：捕捉 consistency-check 後新增的非意圖性錯誤

**核心價值**：守護 System Spec 的品質，避免問題 Spec 污染系統文件。

### 與 consistency-check 的分工

| 工具 | 時機 | 檢查重點 |
|------|------|----------|
| `/flowkit.consistency-check` | Plan 後 | 規劃階段的非意圖錯誤（重複、遺漏複用等） |
| `/flowkit.pre-unify-check` | Unify 前 | Spec 品質 + 實作對齊 + 最終攔截 |

---

## 操作限制

### 核心原則

**STRICTLY READ-ONLY**：本指令不修改任何檔案，僅輸出分析報告。

**品質守門**：確保要合併的 Spec 達到品質標準。

### AI MUST

- 驗證 Feature Spec 的結構完整性
- 確認 Spec 與實作結果一致
- 檢查 ID、編號、引用的正確性
- 對全新功能調整檢查項目（標記 N/A）
- **遵循 Progressive Disclosure Protocol（漸進式揭露協議）**

### AI MUST NOT

- 修改任何檔案
- 將 Feature 的「意圖變更」視為錯誤
- 對全新功能強制檢查「與現有一致性」

---

## Progressive Disclosure Protocol

### 最小載入清單

> **System 層定義**：`specs/system/` 整個資料夾，包含：
> - `spec.md`（System Spec：WHAT）
> - `data-model.md`、`flows.md`、`contracts/`、`ui/`（System Design：HOW）

| 來源 | 僅讀取 | 不讀取 |
|------|--------|--------|
| **Feature spec.md** | 完整內容（需驗證品質） | - |
| **Feature plan.md** | Phase 狀態、實作結果摘要 | 詳細實作說明 |
| **Feature tasks.md** | 完成狀態 | 任務細節 |
| **System Spec** (`spec.md`) | 被 Feature 引用的區段、即將被修改的區段 | 未涉及區段 |
| **System Design** | 依 Feature 引用類別選擇性讀取（見下表） | 未涉及的檔案 |
| **src/** | Feature 新增/修改的檔案清單、關鍵函數簽名 | 完整程式碼 |

**System Design 分層讀取規則**：

| Feature 引用類別 | 讀取的 System Design 檔案 |
|-----------------|--------------------------|
| UI ID 引用 | `ui/*.md` 的相關定義 |
| Entity/Field 引用 | `data-model.md` 的相關 Entity |
| API/Webhook 引用 | `contracts/*.md` 的相關定義 |
| Flow 引用 | `flows.md` 的相關 Flow |

### 分階段解析度

#### Stage 1：結構驗證

- 讀取 Feature Spec 全文
- 檢查結構完整性和格式

#### Stage 2：引用驗證

- 僅對 Spec 中的引用進行深讀確認
- 檢查引用的元素是否存在

---

## 執行步驟

### Phase 0：前置條件檢查

**輸入**：$ARGUMENTS（Feature 名稱或路徑）

**執行**：

1. **確認 Feature 目錄存在**：
   - 必須包含：`spec.md`、`plan.md`、`tasks.md`

2. **確認 tasks.md 狀態**：
   - 所有必要任務應為 DONE
   - 若有未完成任務，警告並詢問是否繼續

3. **判斷 Feature 類型**：

   | 類型 | 判斷依據 | 對檢查的影響 |
   |------|----------|--------------|
   | **全新功能** | Spec 無「修改」標記 | 跳過「對齊檢查」中的部分項目 |
   | **修改功能** | Spec 有「修改」標記 | 完整檢查 |
   | **重構** | Spec 聲明為重構 | 強化影響範圍檢查 |

**輸出**：Feature 類型、檢查模式確認

---

### Phase 1：Spec 品質檢查

**輸入**：`FEATURE_DIR/spec.md`

**執行**：

#### 1.1 結構完整性

| ID | 檢查項目 | 必要性 | 說明 |
|----|----------|--------|------|
| Q1 | Metadata 完整 | REQUIRED | Feature ID、標題、狀態 |
| Q2 | Overview 存在 | REQUIRED | 功能概述 |
| Q3 | User Story 定義 | REQUIRED | 至少一個 User Story |
| Q4 | AC 定義 | REQUIRED | 每個 Story 有 Acceptance Criteria |
| Q5 | 變更標記 | REQUIRED | 新增/修改/刪除 標記明確 |
| Q6 | 影響範圍 | RECOMMENDED | 列出影響的模組/區域 |

#### 1.2 格式正確性

| ID | 檢查項目 | 嚴重性 |
|----|----------|--------|
| F1 | Markdown 語法正確 | MEDIUM |
| F2 | ID 格式符合規範 | HIGH |
| F3 | 標題層級正確 | LOW |
| F4 | 列表格式一致 | LOW |

#### 1.3 內容品質

| ID | 檢查項目 | 嚴重性 |
|----|----------|--------|
| C1 | AC 可測試（有明確條件） | HIGH |
| C2 | User Story 完整（Who/What/Why） | MEDIUM |
| C3 | 無模糊用語（「應該」「可能」） | MEDIUM |
| C4 | 技術細節充足（不過度 high-level） | MEDIUM |

**輸出**：Spec 品質報告

---

### Phase 2：引用正確性檢查

**輸入**：Feature Spec、System 層（specs/system/）、src/

**執行**：

#### 2.1 ID 引用驗證

| ID | 檢查項目 | 比對來源 | 說明 |
|----|----------|----------|------|
| R1 | UI ID 存在 | `ui/*.md` | Spec 引用的 UI ID 在 System UI 定義中存在 |
| R2 | Entity ID 存在 | `data-model.md` | Spec 引用的資料實體 ID 存在 |
| R3 | API 端點存在 | `contracts/api.md` | Spec 引用的 API 端點存在 |
| R4 | Webhook 事件存在 | `contracts/webhook.md` | Spec 引用的 Webhook 事件存在 |
| R5 | Flow 引用正確 | `flows.md` | Spec 引用的 Flow 名稱存在 |
| R6 | 模組路徑正確 | `src/` | Spec 提到的模組路徑有效 |

**全新功能時**：新定義的 ID 不需要在 System 中存在，標記為「新增項目」。

#### 2.2 命名一致性

| ID | 檢查項目 | 說明 |
|----|----------|------|
| N1 | 專有名詞一致 | Spec 使用的術語與 System 一致 |
| N2 | 命名慣例遵循 | 符合專案命名規範 |
| N3 | 大小寫正確 | 技術名詞大小寫正確 |

**輸出**：引用正確性報告

---

### Phase 3：Spec-實作對齊檢查

**輸入**：Feature Spec、Feature Plan、實作結果

**執行**：

#### 3.1 實作完成度

| ID | 檢查項目 | 說明 |
|----|----------|------|
| I1 | 所有 AC 有對應實作 | 每個 AC 在 Plan 中有對應 |
| I2 | Plan 的 Phase 狀態 | 所有 Phase 為 DONE |
| I3 | Tasks 完成狀態 | 必要任務已完成 |

#### 3.2 實作產物存在

| ID | 檢查項目 | 說明 |
|----|----------|------|
| P1 | 宣稱的檔案存在 | Plan 列出的新增檔案確實存在 |
| P2 | 修改的檔案存在 | Plan 列出要修改的檔案存在 |
| P3 | 測試檔案存在 | 對應的測試檔案存在（若要求） |

#### 3.3 變更追蹤

| ID | 檢查項目 | 適用類型 | 說明 |
|----|----------|----------|------|
| T1 | 修改範圍與 Spec 一致 | 修改功能 | 實際修改的檔案與 Spec 聲明一致 |
| T2 | 無遺漏的變更 | 修改功能 | Spec 聲明的變更都有實作 |
| T3 | 無額外變更 | 修改功能 | 實作沒有超出 Spec 範圍 |

**全新功能時**：T1-T3 標記 N/A（全新功能不存在「範圍對齊」問題）。

#### 3.4 Traceability 驗證（條件觸發）

**觸發條件**：Feature 目錄存在 `traceability-index.md`

| ID | 檢查項目 | 嚴重性 | 說明 |
|----|----------|--------|------|
| TR1 | User Story 覆蓋率 | MEDIUM | 每個 User Story 至少有一個對應檔案 |
| TR2 | AC 覆蓋率 | LOW | 每個 AC 至少有一個對應測試（若有 @spec-ac） |
| TR3 | @spec 註解一致性 | MEDIUM | 程式碼中的 @spec 與 tasks.md 一致 |

**若 traceability-index.md 不存在**：
- 標記為 INFO（非阻擋）
- 建議執行 `/flowkit.trace` 產生索引

**輸出**：對齊檢查報告

---

### Phase 4：最終攔截檢查

**目的**：捕捉 consistency-check 後到現在之間產生的新問題。

**輸入**：所有前述資料

**執行**：

#### 4.1 consistency-check 問題追蹤

1. **檢查是否有 consistency-check 報告**
2. **若有，確認報告中的問題已處理**：

   | 情況 | 處理 |
   |------|------|
   | 報告的問題已修正 | ✅ 通過 |
   | 報告的問題標記為「意圖內」 | ✅ 通過（需有說明） |
   | 報告的問題未處理 | ⚠️ 阻擋 |

#### 4.2 最終掃描

- 快速檢查 A-D 類別（與 consistency-check 相同）
- 僅檢查 HIGH 嚴重性項目
- 作為最後一道防線

---

### Phase 5：產生分析報告

**輸入**：所有檢測結果

**執行**：

```markdown
## FlowKit Pre-Unify Check 分析報告

### 基本資訊
- **Feature**：[NNN-feature-name]
- **Feature 類型**：[全新功能 / 修改功能 / 重構]
- **執行時間**：[timestamp]

### 檢查結果摘要

| 類別 | 通過 | 警告 | 失敗 | N/A |
|------|------|------|------|-----|
| Spec 品質 | N | N | N | N |
| 引用正確性 | N | N | N | N |
| Spec-實作對齊 | N | N | N | N |
| 最終攔截 | N | N | N | N |

### 阻擋性問題（必須處理）

| ID | 類別 | 說明 | 修正建議 |
|----|------|------|----------|
| ... | ... | ... | ... |

### 警告（建議處理）

| ID | 類別 | 說明 | 建議 |
|----|------|------|------|
| ... | ... | ... | ... |

### N/A 項目（因 Feature 類型不適用）

| ID | 類別 | 原因 |
|----|------|------|
| ... | ... | 全新功能，不需要檢查修改範圍對齊 |

### Unify 準備狀態

| 狀態 | 說明 |
|------|------|
| ✅ READY | 可以執行 `/flowkit.unify-flow` |
| ⚠️ READY_WITH_WARNINGS | 建議處理警告後再執行 |
| ❌ NOT_READY | 存在阻擋性問題，必須修正後重新檢查 |

**當前狀態**：[READY / READY_WITH_WARNINGS / NOT_READY]

### 下一步
- 若 READY → 執行 `/flowkit.unify-flow`
- 若 READY_WITH_WARNINGS → 處理警告或確認可忽略後執行
- 若 NOT_READY → 修正問題後重新執行本檢查
```

---

## 完成標準（Definition of Done）

```markdown
## Pre-Unify Check DoD

### 必要條件
- [ ] Spec 品質檢查通過（無 REQUIRED 項失敗）
- [ ] 引用正確性檢查通過（無 HIGH 嚴重性問題）
- [ ] Spec-實作對齊檢查通過（或全新功能標記 N/A）
- [ ] 最終攔截無阻擋性問題

### 報告品質
- [ ] 清楚標示 Unify 準備狀態
- [ ] 阻擋性問題與警告明確區分
- [ ] N/A 項目有說明原因
```

---

## 錯誤處理

| 錯誤情境 | 嚴重性 | 處理方式 |
|----------|--------|----------|
| spec.md 不存在 | CRITICAL | ERROR + 無法執行 |
| plan.md 不存在 | CRITICAL | ERROR + 無法執行 |
| tasks.md 不存在 | HIGH | WARNING + 無法驗證完成狀態 |
| System Spec 不存在 | HIGH | ERROR + 無法驗證引用 |
| 實作檔案不存在 | MEDIUM | WARNING + 標記為對齊問題 |

---

## 快速參考

### 心智模型

```
                  實作完成
                     │
                     ▼
          ┌─────────────────────┐
          │ Pre-Unify Check     │
          │                     │
          │ ┌─────────────────┐ │
          │ │ Spec 品質       │ │ ← 結構、格式、內容
          │ └─────────────────┘ │
          │ ┌─────────────────┐ │
          │ │ 引用正確性      │ │ ← ID、命名、路徑
          │ └─────────────────┘ │
          │ ┌─────────────────┐ │
          │ │ Spec-實作對齊   │ │ ← 完成度、產物、變更追蹤
          │ └─────────────────┘ │
          │ ┌─────────────────┐ │
          │ │ 最終攔截        │ │ ← 最後一道防線
          │ └─────────────────┘ │
          └─────────────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
     ✅ READY              ❌ NOT_READY
          │                     │
          ▼                     ▼
   /flowkit.unify-flow      修正問題
```

### 關鍵規則

1. **品質守門**：確保 Spec 達標準才能合併
2. **全新功能簡化**：自動跳過不適用的檢查
3. **狀態明確**：清楚告知是否可以 Unify
4. **最後防線**：捕捉遺漏的問題

### 與其他指令的關係

```
/speckit.plan → /flowkit.consistency-check → /speckit.tasks → /speckit.implement
                                                                      │
                                                                      ▼
                                           /flowkit.pre-unify-check ◄ 本指令
                                                                      │
                                                                      ▼
                                                         /flowkit.unify-flow
```

```

