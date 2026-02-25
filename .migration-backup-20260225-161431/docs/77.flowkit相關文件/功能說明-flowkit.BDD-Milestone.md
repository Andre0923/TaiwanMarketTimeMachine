# FlowKit BDD-Milestone Builder 功能說明

> **指令名稱**：`/flowkit.BDD-Milestone`  
> **Agent 檔案**：`flowkit/agents/flowkit.BDD-Milestone.agent.md`  
> **相關 Templates**：
> - `docs/requirements/user-stories/README-template.md`
> - `docs/requirements/user-stories/US-X-GroupName-template.md`
> - `docs/requirements/Milestone/MNN-MilestoneName-template.md`

---

## 1. 功能概述

### 1.1 這是什麼？

`/flowkit.BDD-Milestone` 是一個 **BDD User Story 系統建立與 Milestone 規劃工具**，具備**兩個獨立功能**：

| 功能 | 說明 | 執行時機 |
|------|------|----------|
| **PRD → User Stories** | 將 PRD 自然語言需求拆分為 BDD 格式 User Stories | 🟡 僅首次 / PRD 變更時 |
| **User Stories → Milestone** | 從已存在的 US 中規劃出本次開發的 Milestone | 每次 Feature 開發 |

### 1.2 解決什麼問題？

| 問題 | 解決方式 |
|------|----------|
| 需求描述雜亂，難以追蹤 | 轉換為結構化 BDD User Story |
| 不知道什麼時候開發什麼 | Milestone 漸進交付規劃 |
| AC 不夠具體，難以驗收 | BDD 格式（Given/When/Then） |
| 需求狀態不明 | 狀態追蹤（⏳🧩🔶✅） |
| 手動維護容易出錯 | 自動產生索引與同步更新 |

### 1.3 核心價值

```
「從自然語言需求 → BDD User Story → Milestone 規劃 → SpecKit 開發」
```

### 1.4 雙重功能說明

```
┌─────────────────────────────────────────────────────────────────┐
│  📘 PRD-*.md                                                    │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 🟡 功能 1a：PRD → User Stories（--init）                │    │
│  │     ※ 僅首次執行 或 PRD 內容有變更時執行                 │    │
│  └─────────────────────────────────────────────────────────┘    │
│       │                                                         │
│       ▼                                                         │
│  📑 User Stories                                                │
│       │                                                         │
│       ▼                                                         │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │ 功能 1b：User Stories → Milestone（--milestone）        │    │
│  │     ※ 每次 Feature 開發都需要執行                        │    │
│  └─────────────────────────────────────────────────────────┘    │
│       │                                                         │
│       ▼                                                         │
│  🎯 Milestone                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**重點**：後續 Feature 開發時，若 PRD 沒有變更，可**跳過功能 1a**，直接執行功能 1b 從既有 User Stories 規劃 Milestone。

---

## 2. 使用時機

### 2.1 在流程中的位置

```
┌──────────────────────────────────────────────────────────────┐
│                      需求規劃流程                             │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
                        PRD / 需求描述
                              │
        ┌─────────────────────┴─────────────────────┐
        │                                           │
        ▼                                           │
┌───────────────────────────────────┐               │
│  🟡 首次 / PRD 變更時             │               │
│  /flowkit.BDD-Milestone --init    │               │
│  （建立 User Story 系統）          │               │
└───────────────────────────────────┘               │
        │                                           │
        ▼                                           │
   📑 User Stories ◄────────────────────────────────┤
        │                                           │
        ▼                                           │
┌───────────────────────────────────┐               │
│  每次 Feature 開發                │               │
│  /flowkit.BDD-Milestone --milestone │             │
│  （規劃 Milestone）                │               │
└───────────────────────────────────┘               │
        │                                           │
        ▼                                           │
   🎯 Milestone                                     │
        │                                           │
        ▼                                           │
   交付 SpecKit                                     │
        │                                           │
        ▼                                           │
   /speckit.specify → plan → ...                   │
        │                                           │
        │（Feature 完成）                           │
        │                                           │
        └─────────── 下一個 Feature ────────────────┘
```

### 2.2 四種操作模式

| 模式 | 說明 | 使用時機 | 備註 |
|------|------|----------|------|
| **INIT** | 完整拆分需求，建立 US 系統 | 首次建立 User Story | 🟡 僅首次 / PRD 變更 |
| **MILESTONE_AUTO** | 自動分析並規劃 Milestone | 讓 AI 決定規劃 | 每次 Feature |
| **MILESTONE_MANUAL** | 指定 US 或 Group 規劃 | 手動控制範圍 | 每次 Feature |
| **UPDATE** | 更新現有 User Story | 需求變更時 | 🟡 PRD 變更時 |
| **STATUS** | 顯示當前狀態 | 查詢進度 | 任何時候 |

### 2.3 執行時機判斷

| 情境 | 執行指令 |
|------|----------|
| 專案首次開發，有 PRD | `--init` → `--milestone` |
| 後續 Feature，PRD 未變 | 僅 `--milestone` |
| PRD 有新增需求 | `--init` 或 `--update` → `--milestone` |
| PRD 修改現有需求 | `--update` → `--milestone` |

---

## 3. 輸入與輸出

### 3.1 輸入

| 來源 | 說明 |
|------|------|
| PRD / 需求文件 | `docs/requirements/PRD-*.md` 或使用者描述 |
| 現有 US 系統 | `docs/requirements/user-stories/` |
| CLI 參數 | `--init`、`--milestone`、`--update` |
| 自然語言 | 「幫我建立 User Story」等 |

### 3.2 輸出

| 產出 | 位置 | 說明 |
|------|------|------|
| **README.md** | `docs/requirements/user-stories/README.md` | 索引 + 狀態快照 |
| **US Group 檔案** | `docs/requirements/user-stories/US-X-xxx.md` | 分群的 US |
| **Milestone 檔案** | `docs/requirements/Milestone/MNN-xxx.md` | Milestone 規劃 |

---

## 4. 指令用法

### 4.1 CLI 風格（精確控制）

| 指令 | 說明 |
|------|------|
| `--init` | 完整拆分需求，建立 US 系統 |
| `--milestone` | 自動分析並產生 Milestone |
| `--milestone US-A-1,US-B-2` | 指定 US 產生 Milestone |
| `--milestone Group-A` | 將 Group A 整組產生 Milestone |
| `--milestone Group-A,US-B-1` | 混合 Group 與個別 US |
| `--update` | 更新現有 User Story |
| （無參數） | 顯示當前狀態 |

### 4.2 自然語言（彈性表達）

| 說法 | 對應操作 |
|------|----------|
| `幫我建立 User Story` | INIT |
| `初始化需求` | INIT |
| `幫我規劃下一個 Milestone` | MILESTONE_AUTO |
| `自動拆分` | MILESTONE_AUTO |
| `把 US A-1 和 B-2 拆成 Milestone` | MILESTONE_MANUAL |
| `把 Group A 整組規劃成 Milestone` | MILESTONE_MANUAL (Group) |
| `Group A 難度不高，整組一起做` | MILESTONE_MANUAL (Group) |
| `把 Group A 和 B 一起拆到新 Milestone` | MILESTONE_MANUAL (Multi) |
| `更新 US A-1 的 AC` | UPDATE |
| `目前還有哪些沒規劃` | STATUS |

---

## 5. User Story 格式規範

### 5.1 User Story 本體

```markdown
### US X-N: <一句話功能摘要>

**As a** <角色>  
**I want** <希望系統協助達成的事情>  
**So that** <能獲得的結果或價值>
```

> ⚠️ User Story 本體**不內嵌 Status**，狀態統一於 README.md 管理。

### 5.2 Acceptance Criteria（BDD 格式）

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
- 每條 AC **必須有語意標題**

### 5.3 分群規則

依主題分群，群組標題範例：

```markdown
## Group A — 核心使用流程
## Group B — 錯誤與例外處理
## Group C — 使用者介面
```

**編號規則**：US X-N（X 為群組代碼，N 為該群組內編號）
- 範例：US A-1, US A-2, US B-1, US B-2...

---

## 6. User Story 狀態定義

| 狀態 | 圖示 | 說明 |
|------|------|------|
| 尚未規劃 | ⏳ | 存在於需求宇宙，尚未排入任何 Milestone |
| Milestone X 執行中 | 🧩 | 正在當前 Milestone 開發中 |
| 部分完成 | 🔶 | AC 未完全滿足，延後處理 |
| 已完成 | ✅ | 所有 AC 皆已滿足 |

---

## 7. 執行流程

### 7.1 INIT 模式流程

```
┌──────────────────────────────────────────────────────────────┐
│  Phase 0：前置檢查 + Gatekeeper                               │
│  • 輸入解析（CLI / 自然語言）                                  │
│  • 確認有需求輸入                                             │
│  • 確認目錄不存在或為空                                       │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 1：需求解析                                            │
│  • Stage 1：結構掃描                                          │
│  • Stage 2：語意拆分                                          │
│  • 產出：US 候選清單 + 分群結構                               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 2：User Story 產生                                     │
│  • 撰寫 US 本體（As a / I want / So that）                    │
│  • 撰寫 AC（Given / When / Then）                             │
│  • AC 品質檢查                                                │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 3：檔案產出                                            │
│  • 產生 README.md（索引 + 狀態快照）                          │
│  • 產生分群檔案（US-A-xxx.md、US-B-xxx.md...）               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 4：驗證與輸出                                          │
│  • 一致性檢查                                                 │
│  • 輸出結構驗證（Linting）                                    │
│  • 產生執行報告                                               │
└──────────────────────────────────────────────────────────────┘
```

### 7.2 MILESTONE 模式流程

```
┌──────────────────────────────────────────────────────────────┐
│  Phase 0：前置檢查                                            │
│  • 確認 README.md 存在                                        │
│  • 確認相關 US 檔案存在                                       │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 3：檔案產出（MILESTONE 模式）                          │
│                                                               │
│  ┌─ MILESTONE_AUTO ─┐    ┌─ MILESTONE_MANUAL ─┐              │
│  │ 分析尚未規劃的 US │    │ 讀取指定的 US-IDs   │              │
│  │ 自動分組（3-7 個） │    │ 驗證 US 存在且 ⏳   │              │
│  └──────────────────┘    └────────────────────┘              │
│                              │                                │
│                              ▼                                │
│               產生 Milestone 檔案                             │
│               更新 README.md 狀態                             │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 4：驗證與輸出                                          │
│  • Milestone 結構驗證（Linting）                              │
│  • README.md 更新驗證                                         │
└──────────────────────────────────────────────────────────────┘
```

---

## 8. US 拆分粒度規則

### 8.1 建議拆分情況

| 情境 | 建議 |
|------|------|
| 多事件來源（userId / groupId / roomId） | 拆分 |
| 多錯誤類型（AUTH / RATE_LIMIT / API_ERROR） | 拆分 |
| 多步驟流程（發送 → 紀錄 → 更新） | 視獨立性拆分 |
| 多組 Given / When / Then | 拆分 |
| 可獨立理解與驗收的子目標 | 拆分 |

### 8.2 建議合併情況

| 情境 | 建議 |
|------|------|
| 語意高度一致 | 保持單一 |
| 無法獨立驗收 | 合併 |

### 8.3 核心原則

> **語意拆分優先**：輸入段落數量 ≠ User Story 數量。依需求語意重新拆分，而非照抄使用者結構。

---

## 9. Milestone 規劃原則

### 9.1 自動拆分原則

| 原則 | 說明 |
|------|------|
| 最小端到端價值 | 優先選擇能形成完整使用流程的 US |
| 規模適中 | 單一 Milestone 建議 3-7 個 US |
| 依賴順序 | 被依賴的 US 優先 |
| 難度控制 | 高難度 US 可延後 |
| Group 完整性 | 若整組適合一次開發，可整組納入 |

### 9.2 Milestone 檔案內容

```markdown
# Milestone NN — <名稱>

> **建立日期**：YYYY-MM-DD  
> **狀態**：🧩 執行中  
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

> ⚠️ **優先權宣告**：若本 Milestone 的 User Story 或 AC 
> 與 Full User Story List 有差異，**以本 Milestone 內容為準**。

### US A-1: <功能摘要>
（完整 BDD 格式）

---

## 延後的 User Stories

| US ID | 原因 |
|-------|------|
| US C-2 | 非核心功能 |
```

---

## 10. Templates 說明

### 10.1 README-template.md

**用途**：User Story 索引 + 狀態快照

**必要區段**：
- `# User Story Index` 標題
- `## 📋 目錄（Table of Contents）`
  - Group 索引表格
  - User Story 索引表格
- `## 📊 狀態快照（Status Snapshot）`
  - 狀態統計表格
  - 依狀態分類列表
- `## 🎯 Milestone 追蹤`

**檔案位置**：`docs/requirements/user-stories/README-template.md`

### 10.2 US-X-GroupName-template.md

**用途**：單一 Group 的 User Story 檔案

**必要區段**：
- `# Group {X} — {名稱}` 標題
- `## 概述`
- `## User Stories`
  - `### US X-N:` 區塊
  - As a / I want / So that
  - Acceptance Criteria
- `## Group 摘要`
- `## 相依關係`
- `## 變更記錄`

**檔案位置**：`docs/requirements/user-stories/US-X-GroupName-template.md`

### 10.3 MNN-MilestoneName-template.md

**用途**：單一 Milestone 規劃檔案

**必要區段**：
- `# Milestone {NN} — {名稱}` 標題
- `## 能力邊界說明`
  - 本 Milestone 完成後具備的能力
  - 下一 Milestone 將擴展的方向
- `## 包含的 User Stories`（完整 BDD 格式）
- `## 延後的 User Stories`
- `## 與 Full User Story List 差異對照`
- `## Milestone 摘要`
- `## 執行建議`

**檔案位置**：`docs/requirements/Milestone/MNN-MilestoneName-template.md`

---

## 11. 輸出結構驗證（Linting）

### 11.1 README.md 結構檢查

```markdown
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

### 11.2 US Group File 結構檢查

```markdown
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

### 11.3 Milestone 檔案結構檢查

```markdown
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

---

## 12. 與其他指令的關係

### 12.1 流程銜接

```
/flowkit.BDD-Milestone --init
        │
        ▼
/flowkit.BDD-Milestone --milestone
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  Milestone 檔案交付 SpecKit                          │
│                                                      │
│  /speckit.specify ← 以 Milestone 為輸入              │
│        │                                             │
│        ▼                                             │
│  /speckit.plan                                       │
│        │                                             │
│        ▼                                             │
│  /flowkit.consistency-check                          │
│        │                                             │
│        ▼                                             │
│  /speckit.tasks → implement → trace                  │
│        │                                             │
│        ▼                                             │
│  /flowkit.pre-unify-check                            │
│        │                                             │
│        ▼                                             │
│  /flowkit.unify-flow                                 │
└─────────────────────────────────────────────────────┘
        │
        ▼
更新 README.md 狀態為 ✅ 已完成
```

### 12.2 相關指令

| 指令 | 關係 |
|------|------|
| `/speckit.specify` | 下游：以 Milestone 為輸入開始開發 |
| `/flowkit.unify-flow` | 下游：完成後更新 US 狀態 |
| `/flowkit.refine-loop` | 平行：小幅調整時可用 |

---

## 13. 使用範例

### 13.1 首次建立 User Story 系統

**CLI 風格**：
```
/flowkit.BDD-Milestone --init
```

**自然語言**：
```
幫我建立 User Story
```

**輸出**：
```markdown
## FlowKit BDD-Milestone Builder 執行結果

### 狀態：成功

### 執行摘要
- 模式：INIT（完整建立）
- 產生 User Story：12 則
- 分群數量：3 組
- 執行時間：2026-01-25T10:30:00

### 產生的檔案
| 檔案 | 說明 |
|------|------|
| README.md | 索引 + 狀態快照 |
| US-A-CoreFlow.md | Group A |
| US-B-ErrorHandling.md | Group B |
| US-C-UserInterface.md | Group C |

### 狀態快照
- **⏳ 尚未規劃**：US A-1, A-2, A-3, B-1, B-2, B-3, ...

### 下一步建議
- [ ] 執行 `--milestone` 自動規劃第一個 Milestone
```

### 13.2 自動規劃 Milestone

**CLI 風格**：
```
/flowkit.BDD-Milestone --milestone
```

**自然語言**：
```
幫我規劃下一個 Milestone
```

### 13.3 指定 US 規劃 Milestone

**CLI 風格**：
```
/flowkit.BDD-Milestone --milestone US-A-1,US-A-2,US-B-1
```

**自然語言**：
```
把 US A-1、A-2 和 B-1 拆成 Milestone
```

### 13.4 指定 Group 整組規劃

**CLI 風格**：
```
/flowkit.BDD-Milestone --milestone Group-A
```

**自然語言**：
```
Group A 難度不高，整組一起做
```

---

## 14. 常見問題 FAQ

### Q1：INIT 模式和 UPDATE 模式有什麼差別？

**A**：
- **INIT**：首次建立，從 PRD 或需求描述產生完整 US 系統
- **UPDATE**：修改現有 US，例如增修 AC、調整描述

### Q2：Milestone 規模多大比較適合？

**A**：建議 3-7 個 User Story。太少可能價值不完整，太多可能開發週期過長。

### Q3：為什麼 US 本體不內嵌狀態？

**A**：狀態統一於 README.md 管理，避免「兩套帳本」的同步問題。README.md 是狀態的唯一真相。

### Q4：Milestone 中的 US 與 Group 檔案中的 US 有差異時，以誰為準？

**A**：**以 Milestone 內容為準**。Milestone 可能針對當次開發調整 AC，這是刻意設計的彈性。

### Q5：支援哪些自然語言？

**A**：支援繁體中文和常見英文表達。AI 會分析意圖並對應至正確模式，有歧義時會確認。

### Q6：如何查詢目前還有哪些 US 沒規劃？

**A**：
```
/flowkit.BDD-Milestone
```
或說「目前還有哪些沒規劃」，會顯示狀態快照。

---

## 15. 完成標準（Definition of Done）

### INIT 模式

- [ ] README.md 已產生
- [ ] 所有 Group 檔案已產生
- [ ] 狀態快照涵蓋所有 US
- [ ] 每個 US 皆有完整 AC
- [ ] README.md Linting 通過
- [ ] 所有 US Group File Linting 通過

### MILESTONE 模式

- [ ] Milestone 檔案已產生
- [ ] README.md 狀態已更新
- [ ] Milestone 包含完整 AC
- [ ] 能力邊界說明已撰寫
- [ ] Milestone File Linting 通過
- [ ] README.md 更新後 Linting 通過

### UPDATE 模式

- [ ] 指定檔案已更新
- [ ] README.md 索引已同步
- [ ] 無破壞既有結構
- [ ] 修改檔案 Linting 通過

---

## 16. 錯誤處理

| 錯誤情境 | 嚴重性 | 處理方式 |
|----------|--------|----------|
| 無需求輸入 | CRITICAL | STOP + 要求提供需求 |
| README.md 不存在（非 INIT） | CRITICAL | STOP + 建議執行 --init |
| US-ID 不存在 | HIGH | 報告 + 跳過該 ID |
| AC 不符合 BDD 格式 | MEDIUM | 警告 + 自動修正 |
| 狀態不一致 | MEDIUM | 警告 + 建議同步 |
| Linting 失敗 | MEDIUM | 標記 + 嘗試自動修正 |

---

## 17. 版本歷史

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.3.0 | 2026-01-22 | 恢復 requirements 資料夾路徑結構 |
| 1.2.0 | 2026-01-22 | 更名為 FlowKit BDD-Milestone Builder |
| 1.1.0 | 2026-01-22 | 新增自然語言支援、Group 指定、輸出結構驗證 |
| 1.0.0 | 2026-01-22 | 初始版本 |

---

## 18. 檔案位置索引

| 類型 | 位置 |
|------|------|
| Agent 指令檔 | `flowkit/agents/flowkit.BDD-Milestone.agent.md` |
| README Template | `docs/requirements/user-stories/README-template.md` |
| US Group Template | `docs/requirements/user-stories/US-X-GroupName-template.md` |
| Milestone Template | `docs/requirements/Milestone/MNN-MilestoneName-template.md` |
| 本功能說明 | `flowkit/docs/功能說明-flowkit.BDD-Milestone.md` |

---

## 19. 目錄結構規範

```
docs/
└── requirements/                             # 需求規劃目錄
    ├── PRD-*.md                              # 產品需求文件（輸入）
    │                                          # 例：PRD-MessageCollector.md
    ├── user-stories/                         # User Story 系統
    │   ├── README.md                         # 索引 + 狀態快照
    │   ├── README-template.md                # README 範本
    │   ├── US-A-CoreFlow.md                  # Group A
    │   ├── US-B-ErrorHandling.md             # Group B
    │   ├── US-X-GroupName-template.md        # US Group 範本
    │   └── ...
    └── Milestone/                            # Milestone 規劃
        ├── M01-CoreFeatures.md               # Milestone 01
        ├── M02-ExtendedFeatures.md           # Milestone 02
        ├── MNN-MilestoneName-template.md     # Milestone 範本
        └── ...
```
```

---

## 20. 心智模型

```
PRD / 需求描述
       │
       ▼
┌──────────────────────────────────────┐
│     /flowkit.BDD-Milestone --init    │
│                                      │
│   自然語言 → 語意拆分 → BDD 格式      │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  User Story 系統                      │
│                                      │
│  README.md ← 狀態統一管理             │
│       │                              │
│       ├── US-A-xxx.md                │
│       ├── US-B-xxx.md                │
│       └── ...                        │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  /flowkit.BDD-Milestone --milestone  │
│                                      │
│  選擇 US → 規劃 Milestone             │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Milestone 檔案                       │
│                                      │
│  M01-xxx.md                          │
│  （包含完整 AC，可直接交付 SpecKit）    │
└──────────────────────────────────────┘
       │
       ▼
    SpecKit 開發流程
```

### 關鍵記憶

> **「自然語言 → BDD User Story → Milestone → SpecKit 開發」**
