# FlowKit Unify Flow

> **用途**：將 Feature Spec 統合回 System Spec，並同步更新 Design + 歷史封存  
> **觸發時機**：Feature 分支開發完成、準備發 PR 合併至 main 之前  
> **憲法依據**：Constitution §6.2（Feature 合併限制）  
> **套件**：FlowKit

---

## 使用者輸入

```text
$ARGUMENTS
```

> 💡 **`--default` 模式**：輸入 `--default` 等同於無額外指示，直接執行預設流程。

在繼續執行之前，您**必須（MUST）**考慮使用者輸入（若非空白或 `--default`）。

---

## 目標

將指定的 Feature Spec（Change Set）統合回 System Spec，確保：
1. System Spec 成為唯一真相（Single Source of Truth）
2. Design 文件同步更新
3. Feature 檔案正確封存
4. 合併操作通過驗證

---

## 操作限制

### 核心原則

System Spec 是基底，Feature Spec 是更新來源。

### AI MUST

- 以 System Spec 為起點進行合併
- 衝突時以 Feature Spec 為準（代表最新設計意圖）
- 完整保留 Feature Spec 未提及的 System Spec 內容
- 僅處理人類明確指定的 Feature
- **遵循 Progressive Disclosure Protocol（漸進式揭露協議）**

### AI MUST NOT

- 自行決定要合併哪個 Feature
- 刪除 System Spec 中未被 Feature 變更的內容
- 「發明」Feature Spec 未寫出的內容
- 從 `docs/` 目錄讀取規劃文件作為合併來源
- 跨過統合流程直接發 PR
- 在 Unify Flow 之外直接修改 `specs/system/`
- **預防性擴讀（在資料充足時讀取超出必要範圍的內容）**
- **在資料不足時進行推測或猜測**

---

## Progressive Disclosure Protocol（漸進式揭露協議）

> **本協議適用於整個 Unify Flow，確保 AI 行為可控、可追溯、可驗證。**

### 核心原則

```
┌─────────────────────────────────────────────────────────────┐
│  資料不足 → 停止並報告，不猜測                                │
│  先低解析度掃描 → 再針對候選項目深讀                           │
│  每次深讀必須記錄原因（可審計）                               │
└─────────────────────────────────────────────────────────────┘
```

### 最小載入清單（Minimal Load List）

**在各 Phase 執行時，僅讀取以下指定項目：**

| 來源 | 僅讀取 | 不讀取 |
|------|--------|--------|
| **Feature Spec** (`spec.md`) | Section Headers, User Stories (含 AC), Functional/Non-Functional Requirements (變更項目), Deletion/Modification Markers | 實作細節, 測試策略, 內部技術說明 |
| **System Spec** (`specs/system/spec.md`) | Section Headers (定位用), 被 Feature 變更影響的對應區段 | 未涉及的區段（不主動全文讀取） |
| **Data Model** (`data-model.md`) | 被 Feature 變更的 Entity/Field 名稱, 相關 Relationship 定義 | 未涉及的 Entity 完整內容 |
| **Contracts** (`contracts/*.md`) | 被 Feature 變更的 Endpoint/Event 定義 | 未涉及的 API/Webhook 完整內容 |
| **Flows** (`flows.md`) | 被 Feature 變更的 Flow 名稱與步驟 | 未涉及的 Flow 完整內容 |
| **UI** (`ui/*.md`) | 被 Feature 變更的 Screen/Pattern/State ID | 未涉及的 UI 定義完整內容 |

### 分階段解析度（Progressive Resolution）

#### Stage 1：結構掃描（Structural Scan）

**讀取範圍**：
- 所有檔案的 Headers / Section Titles
- Feature Spec 的 Change Markers（新增/修改/刪除）
- System Spec 的對應 Section 位置

**輸出**：
- Change Set 初步清單
- 待深讀候選區段清單

**約束**：
- 此階段不讀取段落內文
- 只建立對應關係地圖

#### Stage 2：針對性深讀（Targeted Deep Read）

**觸發條件**：僅對 Stage 1 標記的候選區段執行

**讀取範圍**：
- 候選區段的完整內容
- 相鄰 3-5 行（用於理解上下文）

**約束**：
- 每次深讀必須記錄至 Escalation Log
- 不擴展至未標記區段

### Escalation Log（升級日誌）

在最終輸出中**必須**包含：

```markdown
## Escalation Log（深讀記錄）

| 階段 | 目標位置 | 深讀原因 | 讀取範圍 |
|------|----------|----------|----------|
| Phase 1 | feature/spec.md:L12-45 | User Story 抽取 | 34 lines |
| Phase 2 | system/spec.md:L100-120 | 合併衝突解析 | 21 lines |
| ... | ... | ... | ... |

**總深讀次數**：N  
**最小 Context 完成率**：X%（在 Stage 1 即完成的項目佔比）
```

若整個流程在 Stage 1 即可完成所有必要操作，則記錄：
```markdown
## Escalation Log
Analysis and merge completed within minimal context constraints.
Total deep reads: 0
```

---

## 執行步驟

### Phase 0：前置條件檢查 + 資料健康檢查（Gatekeeper）

**輸入**：使用者指定的 Feature 名稱或路徑（$ARGUMENTS）

**執行**：

#### 0.1 環境檢查

1. **確認當前分支**：
   ```bash
   git branch --show-current
   ```
   - 若非 feature 分支 → ERROR「必須在 feature 分支上執行 Unify Flow」

2. **確認 Feature 目錄存在**：
   ```
   specs/features/<NNN-feature-name>/
   ```
   - 必須包含：`spec.md`、`plan.md`、`tasks.md`
   - 若缺少任一檔案 → ERROR「Feature 目錄不完整，請先完成 /speckit.tasks」

3. **確認 System 層檔案存在**：
   ```
   specs/system/spec.md
   specs/system/data-model.md
   specs/system/flows.md
   specs/system/contracts/
   specs/system/ui/              # 🆕 若 Feature UI Impact ≠ None
   ```
   - 若缺少必要檔案 → ERROR「System 層檔案不完整」
   - `specs/system/ui/` 為條件必要：僅當 Feature Spec 的 UI Impact ≠ None 時檢查

4. **載入憲法**：
   - 讀取 `.specify/memory/constitution.md`
   - 確認 Unify Flow 相關條款

#### 0.2 資料健康檢查（Gatekeeper）🔒

**在進入 Phase 1 之前，必須執行以下檢查：**

```markdown
### Data Health Check

**Feature Spec 完整性：**
- [ ] 存在明確的 Change Markers（新增/修改/刪除標記）
- [ ] User Stories 包含 Acceptance Criteria
- [ ] 變更項目有可衡量的完成條件

**System Spec 可操作性：**
- [ ] Section 結構清晰（可定位）
- [ ] 無未解決的 TODO/TKTK 標記在變更影響區

**Design 文件可操作性：**
- [ ] data-model.md 存在且結構可解析
- [ ] contracts/ 目錄結構完整
```

**失敗協議（Failure Protocol）：**

```
IF any check fails:
  → STOP immediately
  → Output: "INSUFFICIENT DATA: [specific issue]"
  → Recommend: "[specific action to fix]"
  → Do NOT proceed with guessing
```

**輸出**：前置條件檢查通過，記錄 FEATURE_DIR 路徑

**驗證**：
- [ ] 當前為 feature 分支
- [ ] Feature 目錄完整
- [ ] System 層檔案完整
- [ ] 憲法已載入
- [ ] 資料健康檢查通過

若任一項失敗 → 中止並報告具體缺失

---

### Phase 1：解析 Feature Spec（Change Set）—— 低解析度掃描

**輸入**：`FEATURE_DIR/spec.md`

**執行（遵循 Stage 1 規範）**：

#### 1.1 結構掃描（Headers Only）

1. **讀取 Feature Spec 結構**：
   ```
   specs/features/<NNN-feature-name>/spec.md
   ```
   - **僅讀取**：Section Headers、List Item 首行、明確的 Change Markers
   - **不讀取**：段落內文、詳細說明

2. **建立變更類別清單**（初步）：

   | 類別 | 是否有變更 | 候選區段 |
   |------|-----------|----------|
   | User Stories | Yes/No | [Section refs] |
   | 行為描述 | Yes/No | [Section refs] |
   | 介面變更 | Yes/No | [Section refs] |
   | 資料欄位 | Yes/No | [Section refs] |
   | UI 結構  | Yes/No | [Section refs] |
   | 準則調整 | Yes/No | [Section refs] |
   | 其他影響 | Yes/No | [Section refs] |

#### 1.2 針對性深讀（Triggered by Stage 1）

3. **僅對有變更的類別執行深讀**：
   - 讀取候選區段的完整內容
   - 記錄至 Escalation Log

4. **抽取差異資訊**（建立 Change Set）：

   | 類別 | 抽取內容 |
   |------|----------|
   | User Stories | 新增/修改/刪除的 User Stories 與 Acceptance Criteria |
   | 行為描述 | 修改或刪除的行為描述 |
   | 介面變更 | Webhook / API / 操作流程的變更 |
   | 資料欄位 | 使用者可感知資料欄位之新增/變更/移除 |
   | 準則調整 | 成功準則 / 錯誤處理之調整 |
   | 其他影響 | 資料模型、介面契約、流程的變更 |

5. **過濾排除項目**（不得寫入 System Spec）：
   - 實作細節（HOW）
   - 測試策略與代碼說明
   - 內部技術說明（應轉入 Design 層）

**輸出**：結構化的 Change Set 清單

**驗證**：
- [ ] Change Set 不包含實作細節
- [ ] 所有變更項目有明確分類
- [ ] 無遺漏的 User Stories
- [ ] Escalation Log 已記錄本 Phase 的深讀項目

---

### Phase 2：合併至 System Spec —— 漸進式合併

**輸入**：Change Set（來自 Phase 1）、`specs/system/spec.md`

**執行（遵循 Progressive Resolution 規範）**：

#### 2.1 定位階段（Stage 1）

1. **掃描 System Spec 結構**：
   ```
   specs/system/spec.md
   ```
   - **僅讀取**：Section Headers、子標題
   - 建立「Change Set 項目 ↔ System Spec 區段」對應表

2. **標記需要深讀的區段**：
   - 有對應 Change Set 項目的區段 → 標記為「待深讀」
   - 無對應的區段 → 標記為「保留（不讀取）」

#### 2.2 合併階段（Stage 2）

3. **僅對「待深讀」區段執行深讀並合併**：

   | 操作類型 | 處理方式 |
   |----------|----------|
   | **新增** | 將 Feature 的新功能加入 System Spec 的適當位置 |
   | **修改** | 依 Feature Spec 調整 System Spec 中被變更的部分 |
   | **衝突** | **以 Feature Spec 為準**，更新 System Spec |
   | **保留** | Feature Spec 未提及的內容 **MUST 完整保留，不讀取不修改** |

4. **整理結構**：
   - 按模組/情境整理，不原封貼入 Feature Spec 內容
   - 保持文件結構一致性、條列清晰、行為完整
   - 移除 Feature 名稱（System Spec 是整體規格）

**輸出**：更新後的 `specs/system/spec.md`

**驗證檢查清單**：

```markdown
## System Spec 合併驗證

- [ ] 所有 Change Set 項目已處理
- [ ] 無 Feature 名稱殘留
- [ ] 無實作細節洩漏
- [ ] 原有內容（未變更部分）完整保留（未讀取驗證）
- [ ] 文件結構一致
- [ ] 無「發明」的內容（非來自 Feature Spec）
- [ ] Escalation Log 記錄完整
```

**驗證流程**：
1. 逐項檢查上述清單
2. 若任一項失敗 → 記錄問題，進行修正
3. 重新執行驗證（最多 3 次迭代）
4. 若 3 次後仍失敗 → ERROR「合併驗證失敗」並列出具體問題

**Git Checkpoint**：完成 System Spec 合併後，執行 `git add . && git commit -m "docs: 合併 Feature Spec 至 System Spec [FEATURE_NAME]" && git push`。

---

### Phase 3：更新 System Design —— 最小範圍更新

**輸入**：Change Set（來自 Phase 1，僅處理涉及資料/流程/介面的變更）

**執行（遵循 Progressive Resolution 規範）**：

#### 3.0 前置判斷（Stage 1）

1. **根據 Change Set 判斷是否需要更新各 Design 檔案**：

   | 檔案 | 觸發條件 | 需要更新？ |
   |------|----------|-----------|
   | data-model.md | Change Set 包含資料欄位變更 | Yes/No |
   | contracts/webhook.md | Change Set 包含 Webhook 變更 | Yes/No |
   | contracts/api.md | Change Set 包含 API 變更 | Yes/No |
   | flows.md | Change Set 包含流程變更 | Yes/No |

2. **僅對「Yes」的檔案進入深讀更新**

#### 3.1 Data Model 更新（條件觸發）

**位置**：`specs/system/data-model.md`

**讀取範圍**：僅讀取 Change Set 涉及的 Entity / Field 區段

**更新項目**：
- 新增/修改/刪除欄位
- 欄位型別、預設值、驗證條件
- 關聯（Relationship）變更
- 不變條件（Invariants）更新

#### 3.2 Contracts 更新（條件觸發）

**位置**：`specs/system/contracts/`

| 檔案 | 更新內容 |
|------|----------|
| `webhook.md` | 新事件、新欄位、payload 調整 |
| `api.md` | 新 endpoint、參數變更 |
| `schema.md` | 資料表/欄位的變更（若適用） |

#### 3.3 Flows 更新（條件觸發）

**位置**：`specs/system/flows.md`

**讀取範圍**：僅讀取 Change Set 涉及的 Flow 區段

**更新項目**：
- 新增流程
- 調整既有流程
- 新的狀態遷移條件
- 新的決策樹或條件分支

#### 3.4 UI 文件更新（條件觸發）🆕

**位置**：`specs/system/ui/`

**觸發條件**：Change Set 包含 UI 結構變更

| 檔案 | 觸發條件 | 需要更新？ |
|------|----------|-----------|
| ui-structure.md | Change Set 包含新畫面/元件 | Yes/No |
| ux-guidelines.md | Change Set 包含新模式/狀態 | Yes/No |

**更新項目**：
- 新增/修改 Screen/Component 定義
- 新增/修改 Pattern/State 定義
- 更新 UI ID 索引
- 確保 Maturity 達 L1

**輸出**：更新後的 Design 檔案（僅變更涉及的檔案）

**驗證**：
- [ ] data-model.md 與 System Spec 一致（僅驗證變更區段）
- [ ] contracts/ 與 System Spec 一致（僅驗證變更區段）
- [ ] flows.md 與 System Spec 一致（僅驗證變更區段）
- [ ] 未涉及區段確認未被修改
- [ ] Escalation Log 記錄完整

**Git Checkpoint**：完成 System Design 更新後，執行 `git add . && git commit -m "docs: 更新 System Design [FEATURE_NAME]" && git push`。

---

### Phase 4：封存 Feature

**輸入**：FEATURE_DIR 路徑（來自 Phase 0）

**執行**：

0. **更新 Feature Status 為 Unified**：
   - 更新 `spec.md` YAML frontmatter：`status: Unified`
   - 更新 inline 標記：`> **Status**: Unified`
   - 此狀態變更屬於**封存前元資料更新**，確保歷史記錄反映最終狀態

1. **移動整個 Feature 目錄至 history**：
   ```bash
   # 將整個 Feature 目錄移至 history
   mv specs/features/NNN-feature-name specs/history/NNN-feature-name
   ```
   
   **封存後目錄結構**：
   ```
   specs/history/
   └── NNN-feature-name/           # 整個 Feature 目錄移入
       ├── spec.md
       ├── plan.md
       ├── tasks.md
       ├── quickstart.md            # 若有
       └── checklists/              # 若有
   ```

2. **驗證移動完成**：
   - 確認 `specs/features/NNN-feature-name/` 已不存在
   - 確認 `specs/history/NNN-feature-name/` 包含所有原始檔案

3. **合併 Traceability Index**（條件觸發）：

   **觸發條件**：Feature 目錄存在 `traceability-index.md`
   
   **執行步驟**：
   
   a. **讀取 Feature 的 traceability-index.md**
   
   b. **讀取或建立 System 層的 traceability-index.md**
      - 位置：`specs/system/traceability-index.md`
      - 若不存在，依據 `.flowkit/templates/traceability-index-template.md` 建立
   
   c. **合併追溯記錄**：
      - 將 Feature 的 User Story 追溯區塊合併至 System 層
      - 保留 System 層既有的其他 Feature 追溯記錄
      - 更新「最後更新時間」
   
   d. **更新覆蓋率統計**：
      - 重新計算整體覆蓋率（基於 System 層所有 User Stories）
      - 更新「未覆蓋項目清單」

   **合併規則**：
   | 情況 | 處理方式 |
   |------|----------|
   | User Story 首次出現 | 直接新增至 System 層 |
   | User Story 已存在 | 以 Feature 版本覆蓋（Feature 是最新實作） |
   | 舊 Feature 的 US | 保留（不刪除歷史追溯） |

**輸出**：Feature 目錄已移動至 history、Traceability Index 已同步

**驗證**：
- [ ] `specs/features/NNN-feature-name/` 已不存在
- [ ] `specs/history/NNN-feature-name/` 包含所有封存檔案
- [ ] Traceability Index 已合併至 System 層（若存在）

**Git Checkpoint**：完成 Feature 封存後，執行 `git add . && git commit -m "chore: 封存 Feature [FEATURE_NAME] 至 history" && git push`。

---

### Phase 4.5：Milestone / US 狀態更新

> ℹ️ **v1.5.0 新增**：Feature 封存後，自動更新 `docs/requirements` 層級的 US 和 Milestone 狀態

**觸發條件**：Phase 4（封存 Feature）完成後

**強度等級**：SHOULD（更新失敗不阻擋 Unify Flow 完成）

**條件觸發**：僅當 `docs/requirements/user-stories/README.md` 存在時執行，不存在則跳過並記錄原因

**輸入**：
- 已封存 Feature Spec 的 YAML frontmatter（`milestone` 欄位、涉及的 US IDs）
- `docs/requirements/user-stories/README.md`（當前狀態快照）
- `docs/requirements/Milestone/MNN-*.md`（對應 Milestone 檔案）

**執行**：

1. **抽取涉及的 US IDs**：
   - 從 Feature Spec 的 US 段落或 YAML 讀取 US 清單
   - 從 Feature Spec 的 YAML frontmatter 讀取 `milestone` 欄位

2. **更新 README.md 狀態快照**：
   - 每個涉及的 US 狀態 🧩→✅（若該 Feature 涵蓋其所有 AC）
   - 或 🧩→🔶（若 AC 未完全滿足 — 從 spec-delta-log 或 code-check 判斷）
   - 更新統計數字（已完成/部分完成/執行中/待規劃）
   - 更新版本號和最後更新日期

3. **評估 Milestone 完成度**：
   - 檢查該 Milestone 下所有 US 的狀態
   - 若全部 US 皆為 ✅ → 建議將 `MNN-*.md` 狀態標記為 ✅ 已完成
   - 若仍有 🧩 或 ⏳ 的 US → 維持 🧩（待後續 Feature 完成）
   - **MUST ASK** 人類確認 Milestone 結案決定

4. **更新 Milestone 檔案**（若已結案）：
   - 更新 `MNN-*.md` 頂部狀態：🧩 → ✅
   - 填入完成日期

**輸出**：README.md 和 Milestone 狀態已更新（或無需更新的說明）

**驗證**：
- [ ] README.md 狀態快照中涉及的 US 已更新
- [ ] README.md 統計數字正確
- [ ] Milestone 檔案狀態已更新（若 Milestone 全部完成）

**Git Checkpoint**：完成 Milestone/US 狀態更新後，執行 `git add . && git commit -m "docs: 更新 Milestone/US 狀態 [FEATURE_NAME]" && git push`。

---

### Phase 5：合併操作驗證

> **注意**：此階段僅驗證「合併操作本身」的正確性，非全系統一致性檢查。  
> 跨 Feature 的系統一致性應在 Unify Flow 之前由 `/flowkit.pre-unify-check` 完成。

**輸入**：Phase 2、Phase 3 的操作結果、Change Set（來自 Phase 1）

**執行**：

1. **Feature 內容整合驗證**：
   - 確認 Feature Spec 中的所有 User Stories 已整合至 System Spec
   - 確認 Feature Spec 中的所有 Requirements 已反映於 System Spec

2. **合併區段完整性檢查**：

   | 檢查項目 | 驗證內容 |
   |----------|----------|
   | 無重複 | Change Set 項目未造成 System Spec 內容重複 |
   | 無遺漏 | Change Set 項目全部已處理（對照 Phase 1 清單） |
   | 無結構破壞 | System Spec 的章節結構完整、Markdown 語法正確 |

3. **保留區段完整性檢查**：
   - 確認 Phase 2.2 中標記為「保留（不讀取）」的區段**未被修改**
   - 使用 Escalation Log 交叉驗證：僅深讀區段允許有變更

4. **Design 同步驗證**：

   | 檢查項目 | 驗證內容 |
   |----------|----------|
   | data-model.md | 若 Phase 3 觸發更新，確認已同步 |
   | contracts/ | 若 Phase 3 觸發更新，確認已同步 |
   | flows.md | 若 Phase 3 觸發更新，確認已同步 |
   | ui/ | 若 Phase 3 觸發更新，確認已同步 |

5. **Traceability 同步驗證**（條件觸發）：

   **觸發條件**：Feature 目錄存在 `traceability-index.md`
   
   | 檢查項目 | 驗證內容 |
   |----------|----------|
   | Feature Index 已合併 | System 層 traceability-index.md 包含 Feature 的所有 US 追溯 |
   | 覆蓋率已更新 | 覆蓋率數據反映合併後狀態 |
   | 格式正確 | 合併後的 Index 符合 Template 結構 |

6. **殘留檢查**：
   - 無 Feature 名稱殘留於 System Spec
   - 無實作細節洩漏至 System Spec
   - 無未處理的 Change Set 項目

**輸出**：合併操作驗證報告

**處理檢查結果**：

| 結果 | 處理方式 |
|------|----------|
| 全部通過 | 繼續 Phase 6 |
| 有失敗項目 | 返回對應 Phase 修正，最多 3 次迭代 |
| 3 次後仍失敗 | ERROR「合併驗證失敗，需人工介入」|

---

### Phase 6：產生統合摘要

**輸入**：所有 Phase 執行結果、Escalation Log

**執行**：

產生 Markdown 格式摘要，用於 PR 內容：

```markdown
## Unify Flow 統合摘要

### Feature 資訊
- **Feature 名稱**：[NNN-feature-name]
- **分支**：[branch-name]
- **版本號**：[vX.Y.Z]

### 變更摘要
- [列出主要變更項目]

### 更新的文件
| 文件 | 更新類型 | 說明 |
|------|----------|------|
| specs/system/spec.md | 合併 | [說明] |
| specs/system/data-model.md | 更新 | [說明] |
| specs/system/traceability-index.md | 合併 | [若有] |
| ... | ... | ... |

### 重大行為變更
- [若有重大變更，明確標注]

### Traceability 狀態（若有）
- 覆蓋率：[X/Y User Stories 已追溯]
- 新增追溯：[列出新增的 US 追溯]

### 驗證結果
- 合併操作驗證：✅ 通過
- 封存狀態：✅ 完成
```

**輸出**：統合摘要（可直接用於 PR）

**Git Checkpoint**：完成 Unify Flow 後，執行 `git add . && git commit -m "docs: 完成 Unify Flow [FEATURE_NAME] vX.Y.Z" && git push`。

---

### Phase 6.5：Feature Summary 自動產生

**目的**：將本次 Feature 的開發經驗萃取為結構化摘要，供後續 Feature 開發參考。

**執行**：

1. **建立目錄**（若不存在）：
   ```bash
   mkdir -p .flowkit/memory/learning/feature-summaries/
   ```

2. **產生 Feature Summary**：寫入 `.flowkit/memory/learning/feature-summaries/NNN-feature-name-summary.md`
   - 依範本 `.flowkit/templates/feature-summary.template.md` 產生

3. **資料來源**：
   - `spec.md`：US/AC 統計
   - `plan.md`：關鍵決策
   - `spec-delta-log.md`：規格差異記錄統計
   - `.refine/`：refine-loop 循環數
   - `code-check-report-*.md`：code-check 循環數
   - Escalation Log：Unify 過程商議記錄

4. **強度等級**：SHOULD（產生失敗不阻擋 Unify Flow 完成）

> 📌 Feature Summary 為經驗累積機制，後續可由 `plan` 階段參考，提升工時預估精準度。

---

### Phase 7：TD Reconciliation（技術債結案）

**目的**：比對 Feature 中的 TD Ref 標註與 `docs/technical-debt.md` 的 Open TD，提議結案。

**觸發條件**：本 Phase 在 System Spec 合併完成後、最終報告產出前執行。

**前置檢查**：
- **IF NOT EXISTS** `docs/technical-debt.md` → 跳過本 Phase（專案尚未建立 TD Registry）
- **IF** `docs/technical-debt.md` 無 Open / In Progress 項目 → 跳過本 Phase

**執行**：

1. **讀取現有 TD**：
   - 讀取 `docs/technical-debt.md` 中所有 Open / In Progress TD（ID、標題、Component、Dedup-Key）

2. **收集 TD Ref 標註**：
   - 讀取 Feature `spec.md` 中所有 `> TD Ref: TD-XXX` 標註
   - 建立對應關係：TD-XXX → US XX-N

3. **產出候選結案清單**：
   - **直接解決**：Feature US 有 TD Ref 標註 → 建議 Resolved
   - **附帶解決偵測**：取得本次 Feature 的 git diff 涉及的檔案清單，比對 Open TD 的 Component 欄位，若有交集但無 TD Ref → 建議人類確認

4. **MUST ASK 人類確認每一項結案決定**：
   ```markdown
   ## TD Reconciliation 候選清單

   | TD | 標題 | 結案方式 | 來源 US | 狀態 |
   |----|------|----------|---------|------|
   | TD-001 | XXX | Resolved | US A-1 | 待確認 |
   | TD-005 | YYY | 附帶解決？ | (偵測) | 待確認 |

   請確認每一項的結案決定，或調整為 Won't Fix / 維持 Open。
   ```

5. **確認後更新 `docs/technical-debt.md`**：
   - Status → Resolved / Won't Fix
   - 填入 `Resolved-By`：`Feature-NNN US XX-N`
   - 填入 `Resolved-Date`：當日日期
   - Won't Fix 填入 `Won't-Fix-Reason`
   - 從 Active Items 表移至 Resolved 表
   - 更新檔案頂部統計數字

6. **輸出結案摘要**（納入 Unify Report）：
   - N 項 Resolved、M 項 Won't Fix、K 項維持 Open

**強度等級**：SHOULD（TD Registry 不存在或無 Open 項目時自動跳過，不阻擋 Unify Flow 完成）

---

### Phase 7.5：README 專案狀態同步

> ℹ️ **v1.7.0 改版**：改為自然語言 README 生成機制，取代原 AUTO 標記方式

**觸發條件**：Phase 7（TD Reconciliation）完成後

**強度等級**：SHOULD（更新失敗不阻擋 Unify Flow 完成）

**條件觸發**：僅當根目錄 `README.md` 存在時執行

**輸入**：
- 根目錄 `README.md`（當前內容）
- `specs/system/spec.md`（已合併的 System Spec — User Stories 清單）
- `docs/requirements/user-stories/README.md`（US 狀態快照，若存在）
- `docs/requirements/Milestone/MNN-*.md`（Milestone 狀態，若存在）
- Phase 6 統合摘要（本次變更資訊）
- `pyproject.toml` 或 `package.json`（技術棧資訊）

**執行**：

1. **讀取專案上下文**：
   - 從 System Spec、Milestone 進度、已完成 Features、技術棧等來源收集專案狀態
   - 讀取 `README.md` 當前內容

2. **辨識保護區段**：
   - `<!-- README:FROZEN -->` ... `<!-- /README:FROZEN -->`：**完全凍結**，AI 不可修改此區塊內容
   - `<!-- README:SYNC-ONLY -->` ... `<!-- /README:SYNC-ONLY -->`：**僅同步更新**，AI 僅可調整編號、連結、版號等引用資訊，不可改寫段落內容
   - 無標記區段：AI 可根據專案狀態自由重寫

3. **以自然語言重寫 README.md**：
   README 風格應如一般開源專案，包含但不限於：
   - 專案名稱 + 一句話簡介
   - 專案描述（自然語言，2-3 段）
   - 功能亮點 / 已完成功能
   - 技術棧
   - 開發進度（Milestone 表格：名稱、狀態、完成度）
   - 安裝 / 使用指南
   - 專案結構（精簡版目錄樹）
   - 相關文件連結

   **重寫原則**：
   - 風格自然，像真實開源專案的 README
   - 不使用任何 AUTO 標記或結構化報表格式
   - 保留 FROZEN 區段原文不動
   - SYNC-ONLY 區段僅更新引用（編號、連結、數量）
   - 若現有 README 已夠完善，可選擇僅微調回饋本次 Feature 變更

4. **直接寫入 README.md**（不需人類確認）

**保護標記機制**：

| 標記 | 行為 | 用途 |
|------|------|------|
| `<!-- README:FROZEN -->` ... `<!-- /README:FROZEN -->` | AI 完全不修改此區塊 | 人類自訂內容、授權聲明等 |
| `<!-- README:SYNC-ONLY -->` ... `<!-- /README:SYNC-ONLY -->` | AI 僅更新引用資訊（編號、連結、版號） | 安裝指令、目錄結構等 |
| 無標記區段 | AI 可根據專案狀態自由重寫 | 專案描述、功能列表、進度表等 |

**輸出**：README.md 已更新為反映當前專案狀態的自然語言內容

**驗證**：
- [ ] README.md 內容反映當前專案狀態
- [ ] FROZEN 區段原文未被修改
- [ ] SYNC-ONLY 區段僅有引用更新
- [ ] 無 Markdown 語法破壞

**Git Checkpoint**：若有更新 README.md，納入後續的最終 commit。

---

## 完成標準（Definition of Done）
統合流程僅在下列條件**全部符合**時視為完成：

```markdown
## Unify Flow DoD 檢查清單

### 必要條件
- [ ] `specs/system/spec.md` 完整反映本次變更
- [ ] `specs/system/data-model.md` 已同步更新（若有涉及）
- [ ] `specs/system/contracts/` 已同步更新（若有涉及）
- [ ] `specs/system/flows.md` 已同步更新（若有涉及）
- [ ] `specs/system/ui/` 已同步更新（若有涉及）
- [ ] `specs/system/traceability-index.md` 已合併更新（若 Feature 有追溯索引）
- [ ] Feature 目錄已移動至 `specs/history/NNN-feature-name/`
- [ ] `specs/features/NNN-feature-name/` 已不存在
- [ ] Phase 5 合併操作驗證通過
- [ ] 統合摘要已產生
- [ ] TD Reconciliation 已執行（或無 Open TD 而跳過）
- [ ] Escalation Log 已完整記錄
- [ ] README.md US 狀態已更新（若涉及 `docs/requirements`）
- [ ] Milestone 檔案狀態已更新（若適用）
- [ ] README.md 已同步更新為反映專案狀態的自然語言內容（FROZEN/SYNC-ONLY 區段已保護）

### 禁止殘留
- [ ] 無未整合的 Feature Spec 留在 `specs/features/`
- [ ] 無 Feature 名稱殘留於 System Spec
- [ ] 無實作細節洩漏至 System Spec
- [ ] 無預防性擴讀（非必要的深讀記錄）
```

**最終驗證**：
1. 逐項檢查 DoD 清單
2. 若任一項失敗 → 返回對應 Phase 修正
3. 全部通過 → 報告完成，提供 PR 建議

---

## 錯誤處理

| 錯誤情境 | 嚴重性 | 處理方式 |
|----------|--------|----------|
| Feature 目錄不完整 | CRITICAL | ERROR + 指示執行缺少的 speckit 指令 |
| System 層檔案不完整 | CRITICAL | ERROR + 列出缺少的檔案 |
| 資料健康檢查失敗 | CRITICAL | STOP + 指出具體缺失欄位 + 不進行猜測 |
| 合併驗證失敗（3次） | HIGH | ERROR + 列出具體問題，建議人工介入 |
| 憲法衝突 | CRITICAL | 必須在繼續前解決 |

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
## Unify Flow 執行結果

### 狀態：[成功 / 失敗]

### 執行摘要
- Feature：[NNN-feature-name]
- 版本：[vX.Y.Z]
- 執行時間：[timestamp]

### Phase 執行結果
| Phase | 狀態 | 備註 |
|-------|------|------|
| Phase 0：前置檢查 + Gatekeeper | ✅/❌ | 資料健康檢查通過/失敗原因 |
| Phase 1：解析 Feature（低解析度掃描） | ✅/❌ | 抽取 N 項變更 |
| Phase 2：合併 System Spec（漸進式） | ✅/❌ | 迭代 M 次 |
| Phase 3：更新 Design（最小範圍） | ✅/❌ | 更新 X 個檔案 |
| Phase 4：封存 Feature | ✅/❌ | - |
| Phase 4.5：Milestone / US 狀態更新 | ✅/❌/➖ | 條件觸發 / 跳過 |
| Phase 5：合併操作驗證 | ✅/❌ | 迭代 K 次 |
| Phase 6：產生摘要 | ✅/❌ | - |
| Phase 7：TD Reconciliation | ✅/❌/➖ | N 項 Resolved / M 項 Won't Fix / 跳過 |
| Phase 7.5：README 專案狀態同步 | ✅/➖ | 自然語言重寫完成 / README 不存在跳過 |

### Escalation Log（深讀記錄）
| 階段 | 目標位置 | 深讀原因 | 讀取範圍 |
|------|----------|----------|----------|
| Phase 1 | feature/spec.md:L12-45 | User Story 抽取 | 34 lines |
| Phase 2 | system/spec.md:L100-120 | 合併衝突解析 | 21 lines |
| ... | ... | ... | ... |

**總深讀次數**：N  
**最小 Context 完成率**：X%

### DoD 檢查結果
[完整檢查清單，標記 ✅/❌]

### 下一步
- [ ] 檢視統合摘要
- [ ] 執行 `/flowkit.pr-review` 執行六維品質審查並建立 PR
```

---

## 快速參考

### 心智模型

```
System Spec (v1.0)          Feature Spec (NNN-feature)
│                            │
│  ←──── 漸進式合併 ─────    │
│  (僅讀取變更涉及區段)       │
│  (衝突以 Feature 為準)      │
▼                            │
System Spec (v1.1)           │
(包含原有 + 本次變更)         → 移動至 specs/history/NNN-feature/
```

### 關鍵規則

1. **基底優先**：以 System Spec 為起點
2. **衝突以 Feature 為準**：Feature 代表最新設計意圖
3. **保留未涉及部分**：未變更的內容必須保留
4. **僅處理指定 Feature**：不自行決定合併範圍
5. **驗證有上限**：每個驗證最多 3 次迭代
6. **唯一真相**：合併後 System Spec 是唯一真相
7. **漸進式揭露**：先低解析度掃描，再針對性深讀
8. **可審計性**：所有深讀必須記錄原因
9. **資料不足即停止**：Gatekeeper 檢查失敗時不猜測
