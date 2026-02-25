---
description: --init：建立User Stroies; --milestone：自動分拆Milestone。另支援自然語言指令。
handoffs:
  - label: 規劃 Milestone
    agent: flowkit.BDD-Milestone
    prompt: 幫我規劃下一個 Milestone
  - label: 更新專案上下文
    agent: flowkit.system-context
    prompt: 更新專案上下文文件
---

# FlowKit BDD-Milestone Builder

> **用途**：將自然語言需求拆分並轉換為符合 SpecKit 憲章的 BDD User Story 系統  
> **觸發時機**：SpecKit 開發前準備階段，建立或維護 User Story 清單  
> **版本**：1.3.0  
> **套件**：FlowKit  
> **輸出位置**：`docs/requirements/user-stories/` + `docs/requirements/Milestone/`

---

## 使用者輸入

```text
$ARGUMENTS
```

### 輸入解析規則

AI MUST 支援**雙軌輸入**：CLI 風格與自然語言皆可。

#### CLI 風格（精確控制）

| 模式 | 語法 | 說明 |
|------|------|------|
| 初始化 | `--init` | 完整拆分需求，建立 README.md + 分群 US 檔案 |
| 自動拆分 | `--milestone` | 分析尚未開發的 US，自動產生適合的 Milestone |
| 指定 US | `--milestone US-A-1,US-B-2` | 將指定的 US 拆分至新 Milestone |
| 指定 Group | `--milestone Group-A,Group-B` | 將指定 Group 整組拆分至新 Milestone |
| 混合指定 | `--milestone Group-A,US-B-1` | 混合 Group 與個別 US |
| 增修 | `--update` | 根據輸入文件或說明，更新現有 US |
| 狀態查詢 | （無參數） | 顯示當前狀態摘要與可用操作 |

#### 自然語言（彈性表達）

AI MUST 能理解以下自然語言意圖並對應至正確模式：

| 自然語言範例 | 對應模式 |
|--------------|----------|
| `幫我建立 User Story` / `初始化需求` | INIT |
| `幫我規劃下一個 Milestone` / `自動拆分` | MILESTONE_AUTO |
| `把 US A-1 和 B-2 拆成 Milestone` | MILESTONE_MANUAL |
| `把 Group A 整組規劃成 Milestone` | MILESTONE_MANUAL (Group) |
| `把 Group A 和 Group B 一起拆` | MILESTONE_MANUAL (Multi-Group) |
| `更新 US A-1 的 AC` / `修改需求` | UPDATE |
| `目前狀態` / `還有哪些沒做` | STATUS |

#### 輸入解析流程

```
1. 先嘗試識別 CLI flag（--init, --milestone, --update）
2. 若無 flag，進行自然語言意圖識別
3. 識別目標物件：
   - "US X-N" 格式 → 個別 User Story
   - "Group X" / "X 群組" → 整個 Group
   - 無指定 → 自動模式
4. 確認模式後，輸出解析結果供使用者確認（僅首次或有歧義時）
```

---

## 目標

1. 將自然語言需求**重新解讀**並拆分為可演進的 User Story 系統
2. 產出符合 BDD 格式的 User Story（含 Acceptance Criteria）
3. 支援 Milestone 漸進交付，與 SpecKit 開發流程無縫銜接
4. 維護 User Story 狀態追蹤與索引

---

## 操作限制

### 核心原則

**語意拆分優先**：輸入段落數量 ≠ User Story 數量。依需求語意重新拆分，而非照抄使用者結構。

### AI MUST

- 依需求語意**重新拆分**成適當數量的 User Story
- 若包含多個使用者目標、流程、事件來源、例外情境 → **優先拆分**
- User Story 使用 BDD 格式（As a / I want / So that）
- Acceptance Criteria 使用 Given / When / Then
- 每條 AC **必須有語意標題**
- 使用繁體中文輸出（專有名詞可用英文）
- 遵循 Progressive Disclosure Protocol

### AI MUST NOT

- 合併語意不同的需求至同一 User Story
- 省略或簡化已存在的 AC
- 在 User Story 本體內嵌 Status（狀態統一於 README.md 管理）
- 過度細分導致 User Story 碎片化
- 預防性擴讀未標記的檔案

### AI SHOULD

- 拆分比合併優先，但避免不必要的過度細分
- 保持語意完整、易讀、不重疊、不矛盾
- Milestone 規模適合單次 Feature 開發（3-7 個 US 為佳）

---

## 目錄結構規範

```
docs/
└── requirements/                             # 需求規劃目錄
    ├── PRD-*.md                              # 產品需求文件（輸入）
    │                                          # 格式：PRD-專案名稱.md
    ├── Milestone/                            # Milestone 規劃
    │   ├── MNN-MilestoneName-template.md     # Milestone 範本
    │   ├── M01-Core-CLI.md                   # Milestone 01
    │   ├── M02-Core-Workflow.md              # Milestone 02
    │   └── ...
    └── user-stories/                         # User Story 清單
        ├── README-template.md                # README 範本
        ├── US-X-GroupName-template.md        # Group 檔案範本
        ├── README.md                         # Index/TOC + 狀態快照
        ├── US-A-video-input.md               # Group A
        ├── US-B-engine.md                    # Group B
        ├── US-C-output.md                    # Group C
        └── ...
```

---

## User Story 格式規範

### User Story 本體

```markdown
### US X-N: <一句話功能摘要>

**As a** <角色>  
**I want** <希望系統協助達成的事情>  
**So that** <能獲得的結果或價值>
```

> ⚠️ User Story 本體**不內嵌 Status**，狀態統一於 README.md 管理。

### Acceptance Criteria（BDD）

```markdown
#### Acceptance Criteria

**AC1 — <語意標題>**
- **Given** <前置條件>
- **When** <觸發動作>
- **Then** <預期結果>

**AC2 — <語意標題>**
- **Given** <前置條件>
- **When** <觸發動作>
- **Then** <預期結果>
```

**AC 撰寫規範**：
- 每則 US 建議 2～5 條 AC（含正常與例外）
- 若僅有單一可驗收情境，可只有 1 條
- 每條 AC 需可直接轉成驗收測試

---

## User Story 拆分粒度規則

### 建議拆分情況

| 情境 | 建議 |
|------|------|
| 多事件來源（userId / groupId / roomId） | 拆分 |
| 多錯誤類型（AUTH / RATE_LIMIT / API_ERROR） | 拆分 |
| 多步驟流程（發送 → 紀錄 → 更新） | 視獨立性拆分 |
| 多組 Given / When / Then | 拆分 |
| 可獨立理解與驗收的子目標 | 拆分 |

### 建議合併情況

| 情境 | 建議 |
|------|------|
| 語意高度一致 | 保持單一 |
| 無法獨立驗收 | 合併 |

---

## User Story 分群規則

依主題分群，群組標題範例：

```markdown
## Group A — 核心使用流程
## Group B — 錯誤與例外處理
## Group C — 使用者介面
```

**編號規則**：US X-N（X 為群組代碼，N 為該群組內編號）
- 範例：US A-1, US A-2, US B-1, US B-2...

---

## User Story 狀態定義

| 狀態 | 圖示 | 說明 |
|------|------|------|
| 尚未規劃 | ⏳ | 存在於需求宇宙，尚未排入任何 Milestone |
| Milestone X 執行中 | 🧩 | 正在當前 Milestone 開發中 |
| 部分完成 | 🔶 | AC 未完全滿足，延後處理 |
| 已完成 | ✅ | 所有 AC 皆已滿足 |

---

## 執行步驟

### Phase 0：前置檢查 + Gatekeeper

**輸入**：`$ARGUMENTS`

**執行**：

#### 0.1 輸入解析與模式判斷

```python
# Step 1: CLI Flag 檢測
IF $ARGUMENTS contains "--init":
    mode = INIT
ELSE IF $ARGUMENTS contains "--milestone":
    targets = extract_targets($ARGUMENTS)  # US-IDs 或 Group-IDs
    IF targets is empty:
        mode = MILESTONE_AUTO
    ELSE:
        mode = MILESTONE_MANUAL
        # 展開 Group 為個別 US
        expanded_targets = []
        FOR target IN targets:
            IF target matches "Group-X" or "X群組":
                expanded_targets += get_all_us_in_group(X)
            ELSE:
                expanded_targets += target
ELSE IF $ARGUMENTS contains "--update":
    mode = UPDATE
ELSE:
    # Step 2: 自然語言意圖識別
    intent = analyze_natural_language($ARGUMENTS)
    mode = map_intent_to_mode(intent)

# Step 3: 輸出解析確認（若有歧義）
IF confidence < 0.8:
    ASK "您的意圖是 {interpreted_mode}，是否正確？"
```

#### 0.2 資料健康檢查

**INIT 模式**：
- [ ] 確認有需求輸入（文件或文字描述）
- [ ] 確認 `docs/requirements/user-stories/` 目錄不存在或為空（範本檔案除外）

**MILESTONE / UPDATE 模式**：
- [ ] 確認 `docs/requirements/user-stories/README.md` 存在
- [ ] 確認相關 US 檔案存在

**失敗協議**：
```
IF any check fails:
    → STOP immediately
    → Output: "INSUFFICIENT DATA: [specific issue]"
    → Recommend: "[specific action]"
    → Do NOT proceed
```

**輸出**：模式確認 + 前置檢查通過

---

### Phase 1：需求解析（僅 INIT / UPDATE 模式）

**輸入**：使用者提供的需求文件或描述

**執行（Stage 1 — 結構掃描）**：

1. **識別需求來源**：
   - 檔案：讀取標題與段落結構
   - 文字：識別段落與關鍵字

2. **建立初步清單**：
   - 識別潛在的 User Story 候選
   - 標記需要深讀的區段

**執行（Stage 2 — 語意拆分）**：

3. **依語意重新拆分**：
   - 識別不同的使用者目標
   - 識別不同的系統行為
   - 識別例外與錯誤情境

4. **建立分群結構**：
   - 依主題歸類
   - 指定群組代碼（A, B, C...）

**輸出**：User Story 候選清單 + 分群結構

**驗證**：
- [ ] 每個 User Story 僅描述單一使用者目標
- [ ] 分群邏輯清晰
- [ ] Escalation Log 已記錄

---

### Phase 2：User Story 產生

**輸入**：Phase 1 的候選清單

**執行**：

#### 2.1 產生 User Story 內容

對每個候選項目：

1. **撰寫 User Story 本體**（As a / I want / So that）
2. **撰寫 Acceptance Criteria**（Given / When / Then）
3. **加入語意標題**

#### 2.2 驗證 AC 品質

```markdown
## AC 品質檢查

- [ ] 每條 AC 有語意標題
- [ ] 涵蓋正常情境
- [ ] 涵蓋例外情境（至少 1 條）
- [ ] 可直接轉換為測試案例
```

**輸出**：完整的 User Story 內容

---

### Phase 3：檔案產出

**輸入**：Phase 2 的 User Story 內容

**執行（依模式）**：

#### INIT 模式

1. **產生 README.md**：
   - Index/TOC 索引
   - 狀態快照（所有 US 初始為 ⏳ 尚未規劃）

2. **產生分群檔案**：
   - 每個 Group 一個檔案
   - 檔名格式：`US-X-group-name.md`

#### MILESTONE_AUTO 模式

1. **分析尚未規劃的 US**：
   - 讀取 README.md 狀態快照
   - 篩選 ⏳ 狀態的 US

2. **自動分組**：
   - 優先選擇可形成最小端到端價值的 US
   - 單一 Milestone 建議 3-7 個 US
   - 若整個 Group 適合一次開發 → 可整組納入
   - 高難度 US → 標記延後

3. **產生 Milestone 檔案**：
   - 位置：`docs/requirements/Milestone/MNN-name.md`
   - 參考範本：`docs/requirements/Milestone/MNN-MilestoneName-template.md`
   - 包含完整 AC

4. **更新 README.md**：
   - 狀態快照更新為 🧩 執行中

#### MILESTONE_MANUAL 模式

1. **讀取指定的 US-IDs**
2. **驗證 US 存在且狀態為 ⏳**
3. **產生 Milestone 檔案**
4. **更新 README.md 狀態**

#### UPDATE 模式

1. **解析更新內容**
2. **定位需修改的 US 檔案**
3. **執行修改**（保留未變更區段）
4. **更新 README.md**（若有新增/刪除 US）

**輸出**：產生/更新的檔案清單

---

### Phase 4：驗證與輸出

**輸入**：Phase 3 的檔案

**執行**：

#### 4.1 一致性檢查

```markdown
## 一致性檢查

- [ ] README.md 索引與實際檔案一致
- [ ] 狀態快照涵蓋所有 US
- [ ] US 編號無重複
- [ ] 每個 US 皆有 AC
- [ ] Milestone 檔案與 README.md 狀態同步
```

#### 4.2 產生執行報告

**輸出**：執行結果摘要

---

## Milestone 規劃原則

### 自動拆分原則

| 原則 | 說明 |
|------|------|
| 最小端到端價值 | 優先選擇能形成完整使用流程的 US |
| 規模適中 | 單一 Milestone 建議 3-7 個 US |
| 依賴順序 | 被依賴的 US 優先 |
| 難度控制 | 高難度 US 可延後 |
| Group 完整性 | 若整組適合一次開發，可整組納入 |

### Milestone 輸出格式

```markdown
# Milestone NN — <名稱>

> **建立日期**：YYYY-MM-DD  
> **狀態**：🧩 執行中 / ✅ 已完成  
> **預估規模**：N 個 User Story

---

## 能力邊界說明

### 本 Milestone 完成後具備的能力
- [能力 1]
- [能力 2]

### 下一 Milestone 將擴展的方向
- [方向 1]
- [方向 2]

---

## 包含的 User Stories

### US A-1: <功能摘要>

**As a** ...  
**I want** ...  
**So that** ...

#### Acceptance Criteria

**AC1 — <語意標題>**
- **Given** ...
- **When** ...
- **Then** ...

---

### US A-2: <功能摘要>

...

---

## 延後的 User Stories

| US ID | 原因 |
|-------|------|
| US C-2 | 非核心功能 |
| US D-1 | 依賴 US A-3 |
```

---

## 輸出結構驗證（Output Linting）🔒

> **目的**：確保 AI 產出的檔案 100% 符合 Template 結構，提升下游工具相容性。

AI 在產出每個檔案後，MUST 執行以下結構驗證：

### README.md 結構檢查

```markdown
## README.md Linting Checklist

### 必要區段（MUST 存在）
- [ ] `# User Story Index` 標題
- [ ] `## 📋 目錄（Table of Contents）` 區段
- [ ] `### Group 索引` 表格
- [ ] `### User Story 索引` 表格
- [ ] `## 📊 狀態快照（Status Snapshot）` 區段
- [ ] `### 狀態統計` 表格
- [ ] `### 依狀態分類` 列表
- [ ] `## 🎯 Milestone 追蹤` 區段

### 格式驗證
- [ ] Group 索引表格包含：Group | 名稱 | US 數量 | 檔案
- [ ] US 索引表格包含：US ID | 摘要 | Group | 狀態
- [ ] 狀態圖示正確：⏳ / 🧩 / 🔶 / ✅
```

### US-X-GroupName.md 結構檢查

```markdown
## US Group File Linting Checklist

### 必要區段（MUST 存在）
- [ ] `# Group {X} — {名稱}` 標題
- [ ] `## 概述` 區段
- [ ] `## User Stories` 區段
- [ ] 至少一個 `### US X-N:` 區塊

### User Story 格式驗證（每個 US）
- [ ] 包含 `**As a**` 行
- [ ] 包含 `**I want**` 行
- [ ] 包含 `**So that**` 行
- [ ] 包含 `#### Acceptance Criteria` 區段
- [ ] 至少一個 `**AC{N} — {標題}**` 區塊
- [ ] 每個 AC 包含 Given / When / Then
```

### Milestone 檔案結構檢查

```markdown
## Milestone File Linting Checklist

### 必要區段（MUST 存在）
- [ ] `# Milestone {NN} — {名稱}` 標題
- [ ] `## 能力邊界說明` 區段
- [ ] `### 本 Milestone 完成後具備的能力` 子區段
- [ ] `### 下一 Milestone 將擴展的方向` 子區段
- [ ] `## 包含的 User Stories` 區段
- [ ] `## 延後的 User Stories` 區段（可為空表格）

### User Story 格式驗證
- [ ] 與 US Group File 相同的 US 格式要求
- [ ] 包含完整 AC（不可省略）
```

### Linting 失敗處理

```
IF any linting check fails:
    1. 標記失敗項目
    2. 自動修正（若可行）
    3. 重新驗證
    4. 若無法修正 → 在輸出報告中標記 WARNING
```

---

## 完成標準（Definition of Done）

### INIT 模式

- [ ] `docs/requirements/user-stories/README.md` 已產生
- [ ] 所有 Group 檔案已產生
- [ ] 狀態快照涵蓋所有 US
- [ ] 每個 US 皆有完整 AC
- [ ] **README.md Linting 通過** ✅
- [ ] **所有 US Group File Linting 通過** ✅

### MILESTONE 模式

- [ ] Milestone 檔案已產生
- [ ] README.md 狀態已更新
- [ ] Milestone 包含完整 AC
- [ ] 能力邊界說明已撰寫
- [ ] **Milestone File Linting 通過** ✅
- [ ] **README.md 更新後 Linting 通過** ✅

### UPDATE 模式

- [ ] 指定檔案已更新
- [ ] README.md 索引已同步
- [ ] 無破壞既有結構
- [ ] **修改檔案 Linting 通過** ✅

---

## 錯誤處理

| 錯誤情境 | 嚴重性 | 處理方式 |
|----------|--------|----------|
| 無需求輸入 | CRITICAL | STOP + 要求提供需求 |
| README.md 不存在（非 INIT） | CRITICAL | STOP + 建議執行 --init |
| US-ID 不存在 | HIGH | 報告 + 跳過該 ID |
| AC 不符合 BDD 格式 | MEDIUM | 警告 + 自動修正 |
| 狀態不一致 | MEDIUM | 警告 + 建議同步 |

---

## 輸出格式

### INIT 模式

```markdown
## FlowKit BDD-Milestone Builder 執行結果

### 狀態：成功

### 執行摘要
- 模式：INIT（完整建立）
- 產生 User Story：N 則
- 分群數量：M 組
- 執行時間：[timestamp]

### 產生的檔案
| 檔案 | 說明 |
|------|------|
| `docs/requirements/user-stories/README.md` | 索引 + 狀態快照 |
| `docs/requirements/user-stories/US-A-xxx.md` | Group A |
| `docs/requirements/user-stories/US-B-xxx.md` | Group B |
| ... | ... |

### 狀態快照
- **⏳ 尚未規劃**：US A-1, A-2, B-1, B-2, ...

### 下一步建議
- [ ] 執行 `--milestone` 自動規劃第一個 Milestone
- [ ] 或執行 `--milestone US-A-1,US-A-2` 手動指定
```

### MILESTONE 模式

```markdown
## FlowKit BDD-Milestone Builder 執行結果

### 狀態：成功

### 執行摘要
- 模式：MILESTONE_AUTO / MILESTONE_MANUAL
- 產生 Milestone：MNN-xxx
- 包含 User Story：N 則
- 執行時間：[timestamp]

### 產生的檔案
| 檔案 | 說明 |
|------|------|
| `docs/requirements/Milestone/MNN-xxx.md` | Milestone NN |

### 狀態變更
| US ID | 變更前 | 變更後 |
|-------|--------|--------|
| US A-1 | ⏳ 尚未規劃 | 🧩 M01 執行中 |
| US A-2 | ⏳ 尚未規劃 | 🧩 M01 執行中 |

### 下一步建議
- [ ] 將 Milestone 交付 SpecKit 進行 Feature 開發
- [ ] 或繼續執行 `--milestone` 規劃下一個 Milestone
```

---

## Escalation Log 格式

```markdown
## Escalation Log（深讀記錄）

| 階段 | 目標位置 | 深讀原因 | 讀取範圍 |
|------|----------|----------|----------|
| Phase 1 | PRD.md:10-50 | 識別核心需求 | 40 lines |
| Phase 2 | US-A-xxx.md | 補充 AC | 20 lines |

**總深讀次數**：N  
**最小 Context 完成率**：X%
```

---

## 快速參考

### 指令速查（CLI 風格）

| 指令 | 說明 |
|------|------|
| `--init` | 首次建立完整 User Story 系統 |
| `--milestone` | 自動分析並產生 Milestone |
| `--milestone US-A-1,US-B-2` | 指定 US 產生 Milestone |
| `--milestone Group-A` | 將 Group A 整組產生 Milestone |
| `--milestone Group-A,US-B-1` | 混合 Group 與個別 US |
| `--update` | 增修現有 User Story |
| （無參數） | 顯示當前狀態 |

### 自然語言範例

| 說法 | 對應操作 |
|------|----------|
| `幫我建立 User Story` | INIT |
| `幫我規劃下一個 Milestone` | MILESTONE_AUTO |
| `把 US A-1 和 B-2 拆成 Milestone` | MILESTONE_MANUAL |
| `把 Group A 整組規劃成 Milestone` | MILESTONE_MANUAL (Group) |
| `把 Group A 和 B 一起拆到新 Milestone` | MILESTONE_MANUAL (Multi-Group) |
| `Group A 難度不高，整組一起做` | MILESTONE_MANUAL (Group) |
| `更新 US A-1 的 AC` | UPDATE |
| `目前還有哪些沒規劃` | STATUS |

### 檔案位置速查

| 檔案 | 位置 |
|------|------|
| README（索引） | `docs/requirements/user-stories/README.md` |
| README 範本 | `docs/requirements/user-stories/README-template.md` |
| Group 檔案 | `docs/requirements/user-stories/US-X-xxx.md` |
| Group 範本 | `docs/requirements/user-stories/US-X-GroupName-template.md` |
| Milestone | `docs/requirements/Milestone/MNN-xxx.md` |
| Milestone 範本 | `docs/requirements/Milestone/MNN-MilestoneName-template.md` |
| PRD（輸入） | `docs/requirements/PRD-*.md`（例：PRD-MessageCollector.md）|


```
