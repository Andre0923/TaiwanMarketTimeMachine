# FlowKit Unify Flow 功能說明

> **指令名稱**：`/flowkit.unify-flow`  
> **Agent 檔案**：`flowkit/agents/flowkit.unify-flow.agent.md`  
> **相關檔案**：`traceability-index-template.md`（用於合併追溯索引）

---

## 1. 功能概述

### 1.1 這是什麼？

`/flowkit.unify-flow` 是一個**Feature Spec 統合工具**，用於將 Feature 分支開發完成的規格、設計、追溯索引等文件，統合回 System 層級，確保 System Spec 成為唯一真相（Single Source of Truth）。

### 1.2 解決什麼問題？

| 問題 | 解決方式 |
|------|----------|
| Feature 開發完成後，規格散落各處 | 自動合併回 System Spec |
| 不知道哪些設計文件需要更新 | 自動偵測並同步 Design 文件 |
| Feature 完成後難以追蹤歷史 | 自動封存至 history 目錄 |
| 追溯索引停留在 Feature 層 | 自動合併至 System 層追溯索引 |
| 合併後可能產生不一致 | 多重驗證確保品質 |

### 1.3 核心價值

```
「Feature 開發結束後，所有變更回歸系統，System Spec 是唯一真相」
```

---

## 2. 使用時機

### 2.1 何時執行？

```
/speckit.specify → /speckit.plan → /flowkit.consistency-check
                                            │
                                            ▼
                 /speckit.tasks → /speckit.implement
                                            │
                                            ▼
                              /flowkit.pre-unify-check
                                            │
                                            ▼
                                   /flowkit.trace
                                            │
                                            ▼
                              /flowkit.requirement-sync
                                            │
                                            ▼
                               /flowkit.unify-flow ◄── 在此執行
                                            │
                                            ▼
                                     準備發 PR
```

### 2.2 執行條件

| 條件 | 必要性 | 說明 |
|------|--------|------|
| Feature 分支 | REQUIRED | 必須在 feature 分支上執行 |
| Feature 目錄完整 | REQUIRED | 需有 spec.md、plan.md、tasks.md |
| System 層檔案存在 | REQUIRED | 需有 specs/system/ 目錄結構 |
| pre-unify-check 通過 | RECOMMENDED | 建議先執行前置檢查 |
| traceability-index.md | OPTIONAL | 若存在則會合併至 System 層 |

### 2.3 執行順序限制

> ⚠️ **重要**：在 Unify Flow 之外**不得直接修改** `specs/system/`

---

## 3. 輸入與輸出

### 3.1 輸入

| 來源 | 讀取內容 |
|------|----------|
| `FEATURE_DIR/spec.md` | User Stories、Requirements、變更標記 |
| `FEATURE_DIR/plan.md` | 技術決策、設計摘要 |
| `FEATURE_DIR/tasks.md` | 任務清單（用於驗證） |
| `FEATURE_DIR/traceability-index.md` | 追溯索引（若存在） |
| `specs/system/spec.md` | 現有 System Spec（合併基底） |
| `specs/system/*.md` | 現有 Design 文件 |

### 3.2 輸出

| 產出 | 位置 | 說明 |
|------|------|------|
| **System Spec** | `specs/system/spec.md` | 合併後的系統規格 |
| **Design 文件** | `specs/system/data-model.md` 等 | 同步更新的設計文件 |
| **追溯索引** | `specs/system/traceability-index.md` | 合併後的追溯索引 |
| **封存檔案** | `specs/history/` | Feature 歷史封存 |
| **統合摘要** | 終端輸出 | 可用於 PR 描述 |

---

## 4. 執行流程

```
┌──────────────────────────────────────────────────────────────┐
│                    /flowkit.unify-flow                        │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 0：前置條件檢查 + Gatekeeper                           │
│  • 確認 feature 分支                                          │
│  • 確認 Feature 目錄完整                                      │
│  • 確認 System 層檔案存在                                     │
│  • 資料健康檢查                                               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 1：解析 Feature Spec（低解析度掃描）                    │
│  • Stage 1：結構掃描（Headers、Change Markers）               │
│  • Stage 2：針對性深讀（僅變更區段）                           │
│  • 產出：Change Set 清單                                      │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 2：合併至 System Spec（漸進式合併）                     │
│  • 定位：掃描 System Spec 結構                                │
│  • 合併：僅處理 Change Set 涉及的區段                          │
│  • 保留：未涉及區段完整保留                                    │
│  • Git Checkpoint                                            │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 3：更新 System Design（最小範圍更新）                   │
│  • 條件觸發：僅更新受影響的 Design 文件                        │
│  • data-model.md、contracts/、flows.md、ui/                  │
│  • Git Checkpoint                                            │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 4：封存 Feature                                        │
│  • 移動整個 Feature 目錄至 specs/history/                      │
│  • 合併 Traceability Index 至 System 層                       │
│  • Git Checkpoint                                            │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 5：合併操作驗證                                        │
│  • Feature 內容整合驗證                                       │
│  • 保留區段完整性檢查                                         │
│  • Design 同步驗證                                           │
│  • Traceability 同步驗證                                     │
│  • 最多 3 次迭代                                              │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│  Phase 6：產生統合摘要                                        │
│  • 產生 PR 用摘要                                             │
│  • 最終 Git Checkpoint                                       │
└──────────────────────────────────────────────────────────────┘
```

---

## 5. 各 Phase 詳細說明

### Phase 0：前置條件檢查 + Gatekeeper

**目的**：確保所有必要條件滿足，資料健康

**檢查項目**：
- 當前分支是否為 feature 分支
- Feature 目錄是否包含 spec.md、plan.md、tasks.md
- System 層檔案是否存在
- 資料健康檢查（Change Markers、AC 完整性）

**失敗處理**：
- 任一檢查失敗 → **STOP**，不進行猜測
- 輸出具體缺失項目與修復建議

### Phase 1：解析 Feature Spec

**目的**：建立結構化的 Change Set

**漸進式揭露**：
1. **Stage 1（結構掃描）**：僅讀取 Headers、Change Markers
2. **Stage 2（針對性深讀）**：僅對有變更的區段深讀

**產出的 Change Set 分類**：

| 類別 | 說明 |
|------|------|
| User Stories | 新增/修改/刪除的 User Stories |
| 行為描述 | 修改或刪除的行為描述 |
| 介面變更 | Webhook / API / 操作流程 |
| 資料欄位 | 使用者可感知資料欄位 |
| 準則調整 | 成功準則 / 錯誤處理 |
| 其他影響 | 資料模型、介面契約、流程 |

### Phase 2：合併至 System Spec

**核心原則**：

| 原則 | 說明 |
|------|------|
| **基底優先** | 以 System Spec 為起點 |
| **衝突以 Feature 為準** | Feature 代表最新設計意圖 |
| **保留未涉及部分** | 未變更的內容必須保留 |
| **唯一真相** | 合併後 System Spec 是唯一真相 |

**合併操作**：

| 操作類型 | 處理方式 |
|----------|----------|
| 新增 | 加入 System Spec 的適當位置 |
| 修改 | 依 Feature Spec 調整被變更部分 |
| 衝突 | 以 Feature Spec 為準 |
| 保留 | 未提及的內容完整保留，不讀取不修改 |

### Phase 3：更新 System Design

**條件觸發**：僅更新受 Change Set 影響的檔案

| 檔案 | 觸發條件 |
|------|----------|
| `data-model.md` | 包含資料欄位變更 |
| `contracts/webhook.md` | 包含 Webhook 變更 |
| `contracts/api.md` | 包含 API 變更 |
| `flows.md` | 包含流程變更 |
| `ui/*.md` | 包含 UI 結構變更 |

### Phase 4：封存 Feature

**封存方式**：移動整個 Feature 目錄至 history

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

**Traceability Index 合併**（條件觸發）：

若 Feature 存在 `traceability-index.md`：
1. 讀取 Feature 的追溯索引
2. 讀取或建立 System 層的追溯索引
3. 合併追溯記錄
4. 更新覆蓋率統計

**合併規則**：

| 情況 | 處理方式 |
|------|----------|
| US 首次出現 | 直接新增至 System 層 |
| US 已存在 | 以 Feature 版本覆蓋（最新實作） |
| 舊 Feature 的 US | 保留（不刪除歷史追溯） |

### Phase 5：合併操作驗證

**驗證項目**：

| 類型 | 檢查內容 |
|------|----------|
| 無重複 | Change Set 未造成內容重複 |
| 無遺漏 | Change Set 全部已處理 |
| 無結構破壞 | 章節結構完整、Markdown 正確 |
| 保留區段完整 | 未涉及區段未被修改 |
| Design 同步 | 受影響 Design 已同步 |
| Traceability 同步 | 追溯索引已合併 |

**迭代規則**：
- 有失敗項目 → 返回對應 Phase 修正
- 最多 3 次迭代
- 超過 → ERROR「需人工介入」

### Phase 6：產生統合摘要

**摘要內容**（可用於 PR）：
- Feature 資訊（名稱、分支、版本號）
- 變更摘要
- 更新的文件清單
- 重大行為變更
- Traceability 狀態
- 驗證結果

---

## 6. 與其他指令的關係

### 6.1 流程位置圖

```
┌─────────────────────────────────────────────────────────────┐
│                      開發流程                                │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
   /flowkit               /speckit              /flowkit
   .BDD-Milestone         .specify →            .consistency
   (需求規劃)              plan → tasks         -check (Plan 後)
        │                     │                     │
        │                     ▼                     │
        │               /speckit.implement          │
        │                     │                     │
        │                     ▼                     │
        │               /flowkit.trace              │
        │               (產生追溯索引)               │
        │                     │                     │
        │                     ▼                     │
        │               /flowkit.pre-unify-check    │
        │               (Unify 前檢查)              │
        │                     │                     │
        │                     ▼                     │
        └────────────► /flowkit.unify-flow ◄───────┘
                       (本指令)
                              │
                              ▼
                         準備發 PR
```

### 6.2 前置指令

| 指令 | 必要性 | 說明 |
|------|--------|------|
| `/speckit.implement` | REQUIRED | 需有完成的實作 |
| `/flowkit.trace` | RECOMMENDED | 產生追溯索引 |
| `/flowkit.pre-unify-check` | RECOMMENDED | 前置品質檢查 |

### 6.3 後續操作

- 檢視統合摘要
- 提交 PR
- 等待 Review

---

## 7. 漸進式揭露協議（Progressive Disclosure Protocol）

### 7.1 核心原則

```
┌─────────────────────────────────────────────────────────────┐
│  資料不足 → 停止並報告，不猜測                                │
│  先低解析度掃描 → 再針對候選項目深讀                           │
│  每次深讀必須記錄原因（可審計）                               │
└─────────────────────────────────────────────────────────────┘
```

### 7.2 最小載入清單

| 來源 | 僅讀取 | 不讀取 |
|------|--------|--------|
| Feature Spec | Section Headers, User Stories, Change Markers | 實作細節, 測試策略 |
| System Spec | Section Headers, 被變更影響的對應區段 | 未涉及的區段 |
| Data Model | 被變更的 Entity/Field | 未涉及的 Entity |
| Contracts | 被變更的 Endpoint/Event | 未涉及的 API |
| Flows | 被變更的 Flow | 未涉及的 Flow |

### 7.3 Escalation Log

所有深讀必須記錄：

```markdown
| 階段 | 目標位置 | 深讀原因 | 讀取範圍 |
|------|----------|----------|----------|
| Phase 1 | feature/spec.md:L12-45 | User Story 抽取 | 34 lines |
| Phase 2 | system/spec.md:L100-120 | 合併衝突解析 | 21 lines |
```

---

## 8. 完成標準（Definition of Done）

```markdown
## Unify Flow DoD 檢查清單

### 必要條件
- [ ] specs/system/spec.md 完整反映本次變更
- [ ] specs/system/data-model.md 已同步更新（若涉及）
- [ ] specs/system/contracts/ 已同步更新（若涉及）
- [ ] specs/system/flows.md 已同步更新（若涉及）
- [ ] specs/system/ui/ 已同步更新（若涉及）
- [ ] specs/system/traceability-index.md 已合併更新（若存在）
- [ ] Feature 檔案已封存至 specs/history/
- [ ] Phase 5 合併操作驗證通過
- [ ] 統合摘要已產生
- [ ] Escalation Log 已完整記錄

### 禁止殘留
- [ ] 無未整合的 Feature Spec
- [ ] 無 Feature 名稱殘留於 System Spec
- [ ] 無實作細節洩漏至 System Spec
- [ ] 無預防性擴讀（非必要的深讀記錄）
```

---

## 9. 使用範例

### 9.1 基本使用

```
/flowkit.unify-flow 001-user-login
```

### 9.2 完整執行流程範例

**前提**：
- 已完成 Feature 開發（specify → plan → tasks → implement）
- 已執行 `/flowkit.trace` 產生追溯索引
- 已執行 `/flowkit.pre-unify-check` 通過

**執行**：
```
/flowkit.unify-flow 001-user-login
```

**輸出摘要**（可用於 PR）：
```markdown
## Unify Flow 統合摘要

### Feature 資訊
- Feature 名稱：001-user-login
- 分支：feature/001-user-login
- 版本號：v1.1.0

### 變更摘要
- 新增使用者登入功能
- 新增 JWT 驗證機制
- 新增登入 API endpoint

### 更新的文件
| 文件 | 更新類型 |
|------|----------|
| specs/system/spec.md | 合併 |
| specs/system/data-model.md | 更新 |
| specs/system/contracts/api.md | 更新 |
| specs/system/traceability-index.md | 合併 |

### Traceability 狀態
- 覆蓋率：100% (3/3 User Stories)
- 新增追溯：US1, US2, US3

### 驗證結果
- 合併操作驗證：✅ 通過
- 封存狀態：✅ 完成
```

---

## 10. 常見問題 FAQ

### Q1：什麼時候應該執行 Unify Flow？

**A**：Feature 分支開發完成、準備發 PR 合併至 main 之前。建議先執行 `/flowkit.pre-unify-check` 確保品質。

### Q2：如果 pre-unify-check 沒通過，可以執行 Unify Flow 嗎？

**A**：技術上可以，但強烈建議先修正 pre-unify-check 發現的問題。Unify Flow 僅驗證「合併操作本身」的正確性，不做完整的一致性檢查。

### Q3：Traceability Index 一定要先執行 /flowkit.trace 嗎？

**A**：不是必須，但建議執行。若 Feature 目錄存在 `traceability-index.md`，Unify Flow 會自動合併至 System 層。

### Q4：如果合併驗證失敗超過 3 次怎麼辦？

**A**：系統會 STOP 並回報「需人工介入」，此時需要人工檢視具體問題並手動處理。

### Q5：封存後原 Feature 目錄會被刪除嗎？

**A**：有兩種選項：
- 選項 A：在 FEATURE_DIR 中標記 Archived（保留）
- 選項 B：移除整個 FEATURE_DIR（清除）

預設行為可依團隊規範設定。

### Q6：System Spec 中「衝突以 Feature 為準」是什麼意思？

**A**：當 Feature Spec 和 System Spec 對同一項目有不同描述時，以 Feature Spec 的內容為準，因為 Feature 代表最新的設計意圖。

---

## 11. 錯誤處理

| 錯誤情境 | 嚴重性 | 處理方式 |
|----------|--------|----------|
| Feature 目錄不完整 | CRITICAL | ERROR + 指示執行缺少的 speckit 指令 |
| System 層檔案不完整 | CRITICAL | ERROR + 列出缺少的檔案 |
| 資料健康檢查失敗 | CRITICAL | STOP + 指出具體缺失，不進行猜測 |
| 合併驗證失敗（3次） | HIGH | ERROR + 列出具體問題，建議人工介入 |
| 憲法衝突 | CRITICAL | 必須在繼續前解決 |
| 非 feature 分支 | CRITICAL | ERROR + 必須在 feature 分支上執行 |

---

## 12. 版本歷史

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.0.0 | 2026-01-25 | 初始文件版本 |

---

## 13. 檔案位置索引

| 類型 | 位置 |
|------|------|
| Agent 指令檔 | `flowkit/agents/flowkit.unify-flow.agent.md` |
| 追溯索引 Template | `flowkit/templates/traceability-index-template.md` |
| 本功能說明 | `flowkit/docs/功能說明-flowkit.unify-flow.md` |

---

## 14. 心智模型

```
System Spec (v1.0)          Feature Spec (NNN-feature)
│                            │
│  ←──── 漸進式合併 ─────    │
│  (僅讀取變更涉及區段)       │
│  (衝突以 Feature 為準)      │
▼                            │
System Spec (v1.1)           │
(包含原有 + 本次變更)         → 封存至 history
                              │
                         Traceability Index
                              │
                              ▼
                    System Traceability Index
                    (合併後的追溯索引)
```

### 關鍵記憶

> **「Feature 開發完成 → Unify Flow → System Spec 是唯一真相」**
