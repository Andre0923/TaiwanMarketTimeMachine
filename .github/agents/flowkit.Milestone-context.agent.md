---
description: 輸入 --Milestone 自動取編號最大的 Milestone MNN，從 PRD 或指定文件擷取與目標 Milestone 相關的設計上下文，並檢測與現有 System 設計的衝突。強制輸出至 docs/requirements/Milestone/MNN-context.md
handoffs:
  - label: 執行 Plan
    agent: speckit.plan
    prompt: 開始規劃實作方案
  - label: 檢查一致性
    agent: flowkit.consistency-check
    prompt: 檢查 Plan 與 System 的一致性
  - label: 建立 Milestone
    agent: flowkit.BDD-Milestone
    prompt: 幫我規劃下一個 Milestone
---

# FlowKit Milestone Context Extractor

> **用途**：從 PRD 或指定文件擷取與目標 Milestone 相關的設計上下文，並檢測與現有 System 設計的衝突  
> **觸發時機**：Milestone 建立後、SpecKit Plan 階段之前，需要補充設計脈絡時  
> **版本**：1.3.0  
> **套件**：FlowKit  
> **輸出位置**：`docs/requirements/Milestone/MNN-context.md`（強制輸出至檔案）

---

## 使用者輸入

```text
$ARGUMENTS
```

### 輸入解析規則

AI MUST 支援**雙軌輸入**：CLI 風格與自然語言皆可。

#### CLI 風格（精確控制）

| 參數 | 語法 | 說明 | 預設值 |
|------|------|------|--------|
| Milestone | `--milestone M01` | 指定目標 Milestone | 編號最大的 Milestone |
| PRD | `--prd <path>` | PRD 文件路徑 | 自動偵測 `docs/requirements/PRD-*.md` |
| 附加文件 | `--include <path1>,<path2>` | 額外參考文件（可多個） | 無 |
| 輸出模式 | `--output chat` | 輸出至對話（不建立檔案） | `file`（強制輸出至檔案） |
| 衝突檢查 | `--check-conflict` | 啟用衝突檢測 | 預設啟用 |
| 跳過衝突 | `--skip-conflict` | 跳過衝突檢測 | 不跳過 |

#### 自然語言（彈性表達）

AI MUST 能理解以下自然語言意圖並對應至正確模式：

| 自然語言範例 | 對應操作 |
|--------------|----------|
| `幫我擷取 M01 的相關設計` | 指定 M01 Milestone |
| `從 PRD 取出資料庫設計` | 擷取 PRD 的資料模型區段 |
| `把資料庫結構帶入 Plan` | 擷取資料模型並輸出 |
| `檢查 M02 跟現有設計有沒有衝突` | 衝突檢測模式 |
| `參考這份文件規劃` + 附檔 | 附加文件模式 |

---

## 目標

1. **擷取設計上下文**：從 PRD 或指定文件中，擷取與目標 Milestone 相關的設計資訊
2. **結構化輸出**：將擷取內容轉換為 SpecKit Plan 階段可直接引用的格式
3. **衝突檢測**：比對擷取內容與 `specs/system/` 現有設計，發現潛在衝突
4. **知識傳遞**：確保 AI 在 Plan 階段擁有開發者預先設想的設計意圖

---

## 核心價值

```
「將 PRD 中已設想的設計決策 → 結構化擷取 → 衝突檢測 → 供 Plan 階段使用」
```

### 解決的問題

| 問題 | 解決方式 |
|------|----------|
| Plan 階段只有純 BDD Spec，缺乏設計脈絡 | 擷取 PRD 中的資料結構、API 設計等 |
| PRD 與 System Spec 可能有不一致 | 衝突檢測並產出報告 |
| 開發者預設計的意圖未被 AI 理解 | 結構化擷取並傳遞給 Plan 階段 |
| 每次 Plan 都要重讀整份 PRD | 僅擷取與目標 Milestone 相關的部分 |

---

## 衝突檢測核心概念

### System 與 Milestone 的關係

```
┌─────────────────────────────────────────────────────────────┐
│  specs/system/  = 已完成並通過驗證的系統設計（真相來源）      │
│  Milestone      = 預計未來要開發的 Feature                  │
│  PRD            = 產品需求文件（可能包含尚未實作的設計）       │
└─────────────────────────────────────────────────────────────┘
```

### 衝突定義

**衝突發生於**：PRD 中的設計 與 `specs/system/`（已完成部分）存在不一致時

**衝突處理原則**：
- 衝突報告**僅供人類開發者決策**
- AI **不主動修改** System 或 PRD
- 開發者可選擇：
  - **在新 Feature 中修正**：按 PRD 設計，後續透過 Unify Flow 更新 System
  - **修改 PRD 文件**：參照目前 System 已完成的設計

---

## 操作限制

### 核心原則

**READ-ONLY 對 System**：本指令不修改 `specs/system/**`，僅讀取比對。

**Milestone 範圍優先**：擷取的內容必須與目標 Milestone 的 User Story 相關。

### AI MUST

- 以目標 Milestone 的 User Story ID 為過濾依據
- 擷取的設計資訊必須標註來源（檔案:行號 或 Section 名稱）
- 比對時區分「衝突」與「擴展」（新增不算衝突）
- 為每個衝突標記「確定衝突」或「待確認」
- **遵循 Progressive Disclosure Protocol（漸進式揭露協議）**

### AI MUST NOT

- 修改 `specs/system/**`（即使發現衝突）
- 擷取與目標 Milestone 無關的設計內容
- 在衝突未解決時建議直接覆蓋 System Spec
- 預防性擴讀（讀取超出 Milestone 範圍的內容）
- **自行決定衝突的解決方案**（應提交給人類決策）

### AI SHOULD

- 優先擷取：資料模型、API 契約、流程設計、設定檔規格、UI 規格
- 對於模糊的關聯性，標記「可能相關」供人工確認
- 衝突報告應包含具體的解決建議（但由人類決定）

---

## Progressive Disclosure Protocol（漸進式揭露協議）

### 最小載入清單（Minimal Load List）

| 來源 | 僅讀取 | 不讀取 |
|------|--------|--------|
| **Milestone 檔案** | 包含的 US ID、能力邊界、技術備註 | 完整 AC 內容 |
| **PRD.md** | Section Headers、目標 Milestone 相關區段 | 與目標 Milestone 無關的區段 |
| **附加文件** | 由使用者指定的區段或全文 | 未指定時不讀取 |
| **System spec.md** | Section Headers、被擷取內容涉及的區段 | 未涉及區段 |
| **System data-model.md** | Entity 名稱、涉及的 Entity 完整定義 | 未涉及的 Entity |
| **System flows.md** | Flow 名稱、涉及的 Flow 完整定義 | 未涉及的 Flow |
| **System contracts/** | 契約名稱、涉及的契約完整定義 | 未涉及的契約 |
| **System ui/** | Screen/Component 名稱、涉及的 UI 完整定義 | 未涉及的 UI |

### 分階段解析度（Progressive Resolution）

#### Stage 1：結構掃描（Structural Scan）

**讀取範圍**：
- Milestone 檔案的 US ID 清單
- PRD 的 Section Headers
- System 各檔案的 Section Headers / Entity 名稱

**輸出**：
- 「Milestone US ID ↔ PRD Section」對應表
- 「PRD 設計內容 ↔ System 現有定義」候選比對清單

**約束**：
- 此階段**不讀取**完整內容
- 只建立對應關係與候選清單

#### Stage 2：針對性深讀（Targeted Deep Read）

**觸發條件**：僅對 Stage 1 標記的候選項目執行

**讀取範圍**：
- PRD 中與 Milestone 相關的完整 Section
- System 中被涉及的完整定義

**約束**：
- 每次深讀**必須**記錄至 Escalation Log
- 不擴展至未標記區段

---

## 擷取類別定義

### 設計內容分類

| 類別代碼 | 類別名稱 | PRD 典型區段 | 對應 System 檔案 |
|----------|----------|--------------|------------------|
| **DM** | 資料模型 | 資料庫設計、Schema、Entity | `data-model.md` |
| **FL** | 流程設計 | 核心流程、Logic Flow、狀態轉換 | `flows.md` |
| **CT** | 契約定義 | API 規格、Webhook、介面契約 | `contracts/*.md` |
| **CF** | 設定規格 | YAML 設定檔、設定欄位定義 | `spec.md` 或獨立設定 |
| **UI** | UI 規格 | 畫面設計、UI 元件、UX 指引 | `ui/*.md` |
| **TN** | 技術備註 | 技術選型、風險、開發建議 | 無對應（純擷取） |

### 關聯性判斷規則

| 關聯類型 | 判斷依據 | 標記 |
|----------|----------|------|
| **直接關聯** | PRD 明確提及 Milestone 內的 US ID | ✅ 必須擷取 |
| **間接關聯** | PRD 提及的功能名稱與 US 摘要匹配 | 🟡 建議擷取 |
| **可能關聯** | PRD 區段名稱與 US 關鍵字有交集 | ⚪ 標記供確認 |
| **無關聯** | 無任何匹配 | ❌ 不擷取 |

---

## 執行步驟

### Phase 0：前置條件檢查 + 資料健康檢查（Gatekeeper）

**輸入**：$ARGUMENTS

**執行**：

#### 0.1 輸入解析

```python
# Step 1: CLI Flag 檢測
IF $ARGUMENTS contains "--milestone":
    milestone_id = extract_milestone_id($ARGUMENTS)
ELSE:
    milestone_id = find_latest_milestone()  # 預設最大編號

IF $ARGUMENTS contains "--prd":
    prd_path = extract_path($ARGUMENTS, "--prd")
ELSE:
    prd_path = auto_detect_prd("docs/requirements/PRD-*.md")  # 自動偵測 PRD-*.md

IF $ARGUMENTS contains "--include":
    additional_docs = extract_paths($ARGUMENTS, "--include")
ELSE:
    additional_docs = []

IF $ARGUMENTS contains "--skip-conflict":
    check_conflict = False
ELSE:
    check_conflict = True

IF $ARGUMENTS contains "--output":
    output_mode = extract_value($ARGUMENTS, "--output")  # "file" or "chat"
ELSE:
    output_mode = "chat"
```

#### 0.2 資料健康檢查（Gatekeeper）🔒

```markdown
### Data Health Check

**Milestone 完整性：**
- [ ] Milestone 檔案存在（`docs/requirements/Milestone/M{NN}-*.md`）
- [ ] Milestone 包含至少一個 US ID

**PRD 可操作性：**
- [ ] PRD 檔案存在且可讀取
- [ ] PRD 包含可識別的 Section 結構

**System 可比對性：**（若啟用衝突檢查）
- [ ] `specs/system/` 目錄存在
- [ ] 至少存在 `spec.md` 或 `data-model.md`
- [ ] （選配）`specs/system/ui/` 若存在則納入比對
```

**失敗協議（Failure Protocol）：**

```
IF Milestone 檔案不存在:
  → STOP immediately
  → Output: "INSUFFICIENT DATA: 找不到 Milestone 檔案"
  → Recommend: "請先執行 /flowkit.BDD-Milestone --milestone 建立 Milestone"
  → Do NOT proceed with guessing

IF PRD 檔案不存在:
  → STOP immediately
  → Output: "INSUFFICIENT DATA: 找不到 PRD 檔案"
  → Recommend: "請指定 --prd <路徑> 或建立 docs/requirements/PRD-專案名稱.md"
  → Do NOT proceed with guessing
```

**輸出**：前置條件檢查通過

---

### Phase 1：Milestone 範圍定義 —— 低解析度掃描

**輸入**：Milestone 檔案路徑

**執行（遵循 Stage 1 規範）**：

#### 1.1 結構掃描（Headers Only）

1. **讀取 Milestone 檔案**：
   - **僅讀取**：包含的 US ID、能力邊界說明、技術備註區段標題
   - **不讀取**：完整 AC 內容

2. **建立 US ID 清單**：

   ```markdown
   ## Milestone 範圍定義
   
   **目標 Milestone**：M01 - 核心基礎架構
   
   **包含的 US ID**：
   - US I-2: YAML 設定檔載入與驗證
   - US A-1: 閒置狀態偵測與備份觸發
   - US A-2: 輪詢排程與執行頻率控制
   - US B-1: 目標對象清單設定
   - US B-2: TargetId 自動產生與對照管理
   
   **關鍵字清單**（用於 PRD 匹配）：
   - YAML、設定檔、載入、驗證
   - 閒置、偵測、備份、觸發
   - 輪詢、排程、頻率
   - 目標、清單、群組、聯絡人
   - TargetId、編號、對照
   ```

**輸出**：Milestone US ID 清單 + 關鍵字清單

**驗證**：
- [ ] US ID 清單不為空
- [ ] 關鍵字清單已從 US 摘要中提取
- [ ] Escalation Log 已記錄本 Phase 的讀取

---

### Phase 2：PRD 關聯性分析 —— 漸進式處理

**輸入**：Milestone 範圍定義、PRD 路徑

**執行（遵循 Progressive Resolution 規範）**：

#### 2.1 定位階段（Stage 1）

1. **掃描 PRD 結構**：
   - **僅讀取**：Section Headers、子標題
   - 建立「PRD Section → Milestone 關聯性」對應表

2. **標記需要深讀的區段**：

   | PRD Section | 匹配的 US ID | 關聯類型 | 動作 |
   |-------------|--------------|----------|------|
   | 3.3 目標對象管理 | US B-1, B-2 | 直接關聯 | 待深讀 |
   | 4.1 資料庫設計 | US B-2 | 直接關聯 | 待深讀 |
   | 3.1 觸發機制 | US A-1 | 直接關聯 | 待深讀 |
   | 3.2 輪詢規則 | US A-2 | 直接關聯 | 待深讀 |
   | 6. 設定檔範例 | US I-2 | 直接關聯 | 待深讀 |
   | 5. 核心流程 | 多個 | 間接關聯 | 待深讀 |
   | 7. 開發階段規劃 | - | 可能相關 | 可選深讀 |

#### 2.2 擷取階段（Stage 2）

3. **僅對「待深讀」區段執行**：

   | 區段 | 擷取類別 | 擷取內容 |
   |------|----------|----------|
   | 資料庫設計 | DM | 完整 Schema、欄位定義、索引 |
   | 觸發機制 | FL | 閒置規則、中斷規則 |
   | 輪詢規則 | CF | 間隔設定、條件檢查 |
   | 目標對象管理 | DM + CF | TargetId 策略、設定欄位 |
   | 設定檔範例 | CF | YAML 結構、欄位說明 |
   | UI 相關區段 | UI | 畫面設計、元件規格 |
   | **保留區段** | - | **MUST 不讀取** |

4. **結構化擷取內容**：
   - 為每個擷取項目標註來源（檔案:Section:行號）
   - 分類整理為 DM / FL / CT / CF / UI / TN

**輸出**：結構化擷取結果

**驗證檢查清單**：

```markdown
## Phase 2 驗證

- [ ] 每個「直接關聯」區段皆已擷取
- [ ] 擷取內容皆有來源標註
- [ ] 未涉及區段確認未被讀取
- [ ] Escalation Log 記錄完整
```

---

### Phase 3：附加文件處理（若有）

**輸入**：`--include` 指定的附加文件

**執行**：

1. **判斷文件類型**：
   - Markdown → 依 Section 結構處理
   - YAML/JSON → 直接解析結構
   - 其他 → 全文掃描關鍵字

2. **關聯性分析**（同 Phase 2 Stage 1）

3. **擷取相關內容**（同 Phase 2 Stage 2）

**輸出**：附加文件擷取結果（併入主擷取結果）

---

### Phase 4：衝突檢測（若未 --skip-conflict）

**輸入**：Phase 2/3 的擷取結果、System 檔案

**執行**：

#### 4.1 System 結構掃描（Stage 1）

1. **讀取 System 檔案結構**：
   - `data-model.md`：Entity 名稱清單
   - `flows.md`：Flow 名稱清單
   - `contracts/`：契約檔案清單
   - `spec.md`：Section Headers
   - `ui/`：UI 規格檔案清單（若存在）

2. **建立比對候選清單**：

   | PRD 擷取項目 | 類別 | System 候選比對 |
   |--------------|------|-----------------|
   | LINE_目標對象 表 | DM | data-model.md Entity |
   | LINE_訊息紀錄 表 | DM | data-model.md Entity |
   | 閒置偵測流程 | FL | flows.md Flow |
   | 主畫面設計 | UI | ui/*.md Screen |

#### 4.2 衝突分析（Stage 2）

3. **僅對有候選比對的項目執行深讀**

4. **衝突判定規則**：

   | 情況 | 判定 | 處理 |
   |------|------|------|
   | System 無對應定義 | ✅ 擴展（非衝突） | 標記為「新增」 |
   | System 有定義，PRD 相同 | ✅ 一致 | 標記為「一致」 |
   | System 有定義，PRD 不同 | ⚠️ 潛在衝突 | 進入衝突分析 |
   | System 有定義，PRD 為超集 | 🟡 待確認 | 標記為「擴展待確認」 |

5. **衝突分類**：

   | 衝突類型 | 說明 | 嚴重性 |
   |----------|------|--------|
   | **結構衝突** | 欄位名稱/型別不一致 | HIGH |
   | **語意衝突** | 相同名稱但定義不同 | HIGH |
   | **約束衝突** | 驗證規則/約束條件不一致 | MEDIUM |
   | **擴展衝突** | PRD 新增欄位但 System 有類似功能 | LOW |
   | **UI 衝突** | 畫面/元件設計不一致 | MEDIUM |

**輸出**：衝突分析結果

---

### Phase 5：產生輸出

**輸入**：Phase 2/3/4 的結果

**執行**：

#### 5.1 產生 Milestone Context 文件

使用 **Milestone Context Output Template**（見 `.flowkit/templates/Milestone-context-output.template.md`）

#### 5.2 產生衝突報告（若有衝突）

使用 **Conflict Report Template**（見 `.flowkit/templates/Milestone-context-conflict-report.template.md`）

**衝突報告必須包含**：
- 衝突項目清單
- PRD 定義 vs System 定義的差異
- 建議解決方案（供人類選擇）：
  - **方案 A**：按 PRD 設計，在新 Feature 中實作，後續透過 Unify Flow 更新 System
  - **方案 B**：修改 PRD 文件，參照目前 System 已完成的設計

#### 5.3 輸出方式與路徑規範

**AI MUST 遵守的輸出路徑規範**：
- 產出的 .md 文件 **MUST** 放置在 `docs/requirements/Milestone/` 資料夾
- 檔案命名格式：`MNN-context.md`（例如 `M01-context.md`）
- 絕對路徑範例：`docs/requirements/Milestone/M01-context.md`

**輸出模式**（預設強制輸出至檔案）：
- **預設（未指定 `--output`）**：**MUST** 寫入 `docs/requirements/Milestone/MNN-context.md`
- `--output chat`：直接輸出至對話（不建立檔案）—— 僅供除錯或預覽用

**強制輸出原因**：
- SpecKit 的 specify 和 plan 階段會自動讀取此檔案
- 對話總結後輸出會遺失，無法供後續階段使用

**輸出**：完成的文件

---

## 完成標準（Definition of Done）

```markdown
## DoD 檢查清單

### 必要條件
- [ ] Milestone 範圍已定義
- [ ] PRD 相關區段已擷取
- [ ] 擷取內容皆有來源標註
- [ ] 衝突檢測已執行（或明確跳過）
- [ ] Escalation Log 已完整記錄

### 衝突處理
- [ ] 若有衝突：衝突報告已產生，包含解決方案建議
- [ ] 若無衝突：確認 System 與 PRD 一致或為純擴展

### 禁止殘留
- [ ] 無預防性擴讀（非必要的深讀記錄）
- [ ] 未修改任何 System 檔案
- [ ] 未自行決定衝突解決方案（僅提供建議）
```

---

## 錯誤處理

| 錯誤情境 | 嚴重性 | 處理方式 |
|----------|--------|----------|
| Milestone 檔案不存在 | CRITICAL | STOP + 建議先建立 Milestone |
| PRD 檔案不存在 | CRITICAL | STOP + 提示指定路徑 |
| PRD 無法解析 Section | HIGH | WARN + 嘗試全文關鍵字匹配 |
| System 檔案不存在 | MEDIUM | WARN + 跳過衝突檢測 |
| System UI 資料夾不存在 | LOW | INFO + 跳過 UI 比對 |
| 無法判斷關聯性 | LOW | 標記「可能相關」供人工確認 |
| 附加文件格式不支援 | LOW | WARN + 跳過該文件 |

---

## 快速參考

### 指令用法速查

| 用法 | 說明 |
|------|------|
| `/flowkit.Milestone-context` | 使用最新 Milestone，從 PRD 擷取 |
| `/flowkit.Milestone-context --milestone M01` | 指定 M01 |
| `/flowkit.Milestone-context --include api-spec.md` | 附加參考文件 |
| `/flowkit.Milestone-context --skip-conflict` | 跳過衝突檢測 |
| `/flowkit.Milestone-context --output file` | 輸出至檔案 |

### 擷取類別速查

| 代碼 | 類別 | 對應 System |
|------|------|-------------|
| DM | 資料模型 | data-model.md |
| FL | 流程設計 | flows.md |
| CT | 契約定義 | contracts/*.md |
| CF | 設定規格 | spec.md |
| UI | UI 規格 | ui/*.md |
| TN | 技術備註 | 無對應 |

### 衝突解決方案

| 方案 | 說明 | 適用情境 |
|------|------|----------|
| **A. 按 PRD 設計** | 在新 Feature 實作，後續 Unify Flow 更新 System | PRD 為較新/較完整的設計 |
| **B. 按 System 設計** | 修改 PRD 參照目前已完成的 System | System 設計已經過驗證 |

### 衝突嚴重性

| 級別 | 說明 | 處理 |
|------|------|------|
| CRITICAL | 阻擋性衝突 | 必須立即解決 |
| HIGH | 重大不一致 | 必須在 Plan 前解決 |
| MEDIUM | 中等差異 | 應在 Plan 中說明 |
| LOW | 輕微差異 | 可延後處理 |
