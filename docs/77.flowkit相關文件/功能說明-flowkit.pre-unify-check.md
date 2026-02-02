# FlowKit Pre-Unify Check 功能說明

> **指令名稱**：`/flowkit.pre-unify-check`  
> **Agent 檔案**：`flowkit/agents/flowkit.pre-unify-check.agent.md`  
> **前置指令**：`/flowkit.consistency-check`（Plan 階段）

---

## 1. 功能概述

### 1.1 這是什麼？

`/flowkit.pre-unify-check` 是 **Unify Flow 前的最終攔截檢查工具**，在 Feature 實作完成後、合併回 System Spec 之前執行，確保：

1. Feature Spec 品質達標
2. 引用的 ID/路徑正確
3. 實作與 Spec 對齊
4. 無遺留的已知問題

### 1.2 與 consistency-check 的差異

| 面向 | consistency-check | pre-unify-check |
|------|-------------------|-----------------|
| **執行時機** | Plan 階段（實作前） | Implement 完成後（Unify 前） |
| **檢查重點** | 規劃決策的合理性 | 實作結果的正確性 |
| **有無程式碼** | 無（只有 Plan） | 有（實作完成） |
| **主要目的** | 避免錯誤延續到實作 | 確保可安全合併 |

### 1.3 核心價值

```
「Unify 前最後一道防線，確保合併品質」
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
                              /flowkit.pre-unify-check ◄── 在此執行
                                            │
                                    ┌───────┴───────┐
                                    │               │
                                 ✅ READY      ❌ NOT_READY
                                    │               │
                                    ▼               ▼
                           /flowkit.trace      修正後重新檢查
                                    │
                                    ▼
                      /flowkit.requirement-sync
                                    │
                                    ▼
                          /flowkit.unify-flow
```

### 2.2 執行條件

| 條件 | 必要性 | 說明 |
|------|--------|------|
| `spec.md` 存在 | REQUIRED | Feature Spec |
| `plan.md` 存在 | REQUIRED | Feature Plan |
| `tasks.md` 存在 | RECOMMENDED | 用於完成度檢查 |
| 程式碼已實作 | RECOMMENDED | 用於對齊檢查 |
| System Spec 存在 | REQUIRED | 用於引用驗證 |

---

## 3. 檢查項目總覽

### 3.1 五大檢查類別

| Phase | 類別 | 目的 |
|-------|------|------|
| Phase 1 | Spec 品質 | 確保 Feature Spec 本身品質達標 |
| Phase 2 | 引用正確性 | 確保 ID/路徑引用正確 |
| Phase 3 | Spec-實作對齊 | 確保實作與 Spec 一致 |
| Phase 4 | 最終攔截 | 確認已知問題已處理 |
| Phase 5 | 產生報告 | 輸出檢查結果 |

### 3.2 檢查項目清單

#### Phase 1：Spec 品質檢查

| ID | 檢查項目 | 嚴重性 | 說明 |
|----|----------|--------|------|
| S1 | User Stories 完整 | REQUIRED | 每個 US 有 AC |
| S2 | AC 可驗證 | REQUIRED | AC 有明確條件 |
| S3 | 範圍邊界清楚 | HIGH | 有明確的 In/Out Scope |
| F1 | Markdown 語法正確 | MEDIUM | 格式正確 |
| C1 | AC 可測試 | HIGH | 有明確測試條件 |

#### Phase 2：引用正確性檢查

| ID | 檢查項目 | 比對來源 | 嚴重性 |
|----|----------|----------|--------|
| R1 | UI ID 存在 | `specs/system/ui/*.md` | HIGH |
| R2 | Entity ID 存在 | `specs/system/data-model.md` | HIGH |
| R3 | API 端點存在 | `specs/system/contracts/api.md` | HIGH |
| R4 | Webhook 事件存在 | `specs/system/contracts/webhook.md` | HIGH |
| R5 | Flow 引用正確 | `specs/system/flows.md` | HIGH |
| R6 | 模組路徑正確 | `src/` | HIGH |

#### Phase 3：Spec-實作對齊檢查

| ID | 檢查項目 | 嚴重性 | 說明 |
|----|----------|--------|------|
| I1 | 所有 AC 有對應實作 | HIGH | AC 在 Plan 中有對應 |
| I2 | Plan Phase 狀態 | HIGH | 所有 Phase 為 DONE |
| I3 | Tasks 完成狀態 | HIGH | 必要任務已完成 |
| P1 | 宣稱的檔案存在 | HIGH | Plan 列出的檔案存在 |
| T1 | 修改範圍一致 | HIGH | 實際修改與 Spec 聲明一致 |
| TR1 | User Story 覆蓋率 | MEDIUM | 每個 US 有對應檔案 |
| TR2 | AC 覆蓋率 | LOW | 每個 AC 有對應測試 |
| TR3 | @spec 註解一致性 | MEDIUM | 程式碼註解與 tasks.md 一致 |

#### Phase 4：最終攔截檢查

| ID | 檢查項目 | 說明 |
|----|----------|------|
| - | consistency-check 問題追蹤 | 確認報告中的問題已處理 |
| - | 快速 A-D 類別掃描 | 作為最後一道防線 |

---

## 4. 執行流程

### Phase 0：前置條件檢查

```markdown
1. 確認 Feature 目錄完整
2. 確認 System 層檔案存在
3. 判斷 Feature 類型（全新/修改/重構）
```

### Phase 1：Spec 品質檢查

```markdown
1. 檢查結構完整性（S1-S3）
2. 檢查格式正確性（F1-F4）
3. 檢查內容品質（C1-C4）
```

### Phase 2：引用正確性檢查

```markdown
1. 掃描 Feature Spec 中的所有 ID 引用
2. 與 System 層對應檔案比對
3. 全新功能的新 ID 標記為「新增項目」
```

### Phase 3：Spec-實作對齊檢查

```markdown
1. 檢查實作完成度（I1-I3）
2. 檢查實作產物存在（P1-P3）
3. 檢查變更追蹤（T1-T3）
4. 檢查 Traceability（TR1-TR3，條件觸發）
```

### Phase 4：最終攔截檢查

```markdown
1. 確認 consistency-check 問題已處理
2. 快速 A-D 類別掃描
```

### Phase 5：產生報告

```markdown
1. 彙總所有檢查結果
2. 判定 Unify 準備狀態
3. 提供下一步建議
```

---

## 5. 輸出格式

### 5.1 檢查結果摘要

```markdown
## FlowKit Pre-Unify Check 分析報告

### 基本資訊
- **Feature**：001-user-management
- **Feature 類型**：全新功能
- **執行時間**：2026-01-25 14:30

### 檢查結果摘要

| 類別 | 通過 | 警告 | 失敗 | N/A |
|------|------|------|------|-----|
| Spec 品質 | 8 | 1 | 0 | 0 |
| 引用正確性 | 5 | 0 | 1 | 0 |
| Spec-實作對齊 | 6 | 2 | 0 | 3 |
| 最終攔截 | 2 | 0 | 0 | 0 |
```

### 5.2 Unify 準備狀態

| 狀態 | 說明 | 下一步 |
|------|------|--------|
| ✅ READY | 可以執行 Unify | `/flowkit.unify-flow` |
| ⚠️ READY_WITH_WARNINGS | 有警告但可執行 | 建議處理警告後執行 |
| ❌ NOT_READY | 有阻擋性問題 | 修正問題後重新檢查 |

---

## 6. System 層定義

### 6.1 什麼是 System 層？

`specs/system/` 整個資料夾，包含：

```
specs/system/                    # System 層（整體）
├── spec.md                      # System Spec（WHAT：外部行為）
├── data-model.md                # System Design（HOW）
├── flows.md                     # System Design
├── contracts/                   # System Design
│   ├── webhook.md
│   ├── api.md
│   └── schema.md
└── ui/                          # System Design
    ├── ui-structure.md
    └── ux-guidelines.md
```

### 6.2 分層讀取規則

| Feature 涉及類別 | 讀取的 System Design 檔案 |
|------------------|---------------------------|
| 資料欄位變更 | `data-model.md` 的相關 Entity |
| API/Webhook 變更 | `contracts/*.md` 的相關定義 |
| 流程變更 | `flows.md` 的相關 Flow |
| UI 變更 | `ui/*.md` 的相關 Screen/Pattern |

---

## 7. 與其他指令的關係

### 7.1 上游指令

| 指令 | 關係 |
|------|------|
| `/flowkit.consistency-check` | Plan 階段的檢查，本指令追蹤其報告 |
| `/speckit.implement` | 實作完成後才能執行本指令 |
| `/flowkit.trace` | 若有執行，本指令檢查 TR1-TR3 |

### 7.2 下游指令

| 指令 | 關係 |
|------|------|
| `/flowkit.unify-flow` | 本指令通過後才能執行 Unify |

### 7.3 與 consistency-check 的互補關係

```
┌─────────────────────────────────────────────────────────────────┐
│                        開發流程                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   Plan 階段                          Implement 後               │
│       │                                   │                     │
│       ▼                                   ▼                     │
│  ┌─────────────────────┐          ┌─────────────────────┐      │
│  │ consistency-check   │          │ pre-unify-check     │      │
│  ├─────────────────────┤          ├─────────────────────┤      │
│  │ • 重複實作檢查       │          │ • Spec 品質檢查      │      │
│  │ • 複用遺漏檢查       │          │ • 引用正確性檢查     │      │
│  │ • 非意圖變動檢查     │          │ • Spec-實作對齊      │      │
│  │ • 整合建議          │          │ • Traceability 驗證  │      │
│  └─────────────────────┘          │ • 最終攔截           │      │
│            │                      └─────────────────────┘      │
│            │                               │                    │
│            └───────────追蹤報告────────────┘                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. 使用範例

### 8.1 基本使用

```
/flowkit.pre-unify-check
```

自動偵測當前 Feature 目錄並執行檢查。

### 8.2 指定 Feature

```
/flowkit.pre-unify-check 001-user-management
```

### 8.3 輸出範例

```markdown
## FlowKit Pre-Unify Check 分析報告

### Unify 準備狀態

**當前狀態**：⚠️ READY_WITH_WARNINGS

### 阻擋性問題（必須處理）
（無）

### 警告（建議處理）

| ID | 類別 | 說明 | 建議 |
|----|------|------|------|
| TR2 | Traceability | AC2.3 無對應測試 | 建議補充測試 |
| C3 | 內容品質 | 有模糊用語「應該」 | 建議改為明確描述 |

### 下一步
- 建議處理警告後執行 `/flowkit.unify-flow`
- 或確認警告可忽略後直接執行
```

---

## 9. 常見問題

### Q1：一定要全部通過才能 Unify 嗎？

**A**：不一定。
- ❌ NOT_READY：必須修正阻擋性問題
- ⚠️ READY_WITH_WARNINGS：可以執行，但建議處理
- ✅ READY：可以直接執行

### Q2：全新功能的檢查項目會不同嗎？

**A**：是的。
- R1-R6（引用檢查）：新定義的 ID 標記為「新增項目」，非錯誤
- T1-T3（變更追蹤）：標記 N/A，全新功能不存在「範圍對齊」問題

### Q3：沒有執行 consistency-check 可以嗎？

**A**：可以，但不建議。Phase 4 會嘗試追蹤 consistency-check 報告，若不存在會跳過。

### Q4：Traceability 檢查（TR1-TR3）是必要的嗎？

**A**：非必要。僅當 Feature 目錄存在 `traceability-index.md` 時才觸發。

---

## 10. 版本歷史

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.0.0 | 2026-01-23 | 初始版本，從 Unify Flow 拆分 |
| 1.1.0 | 2026-01-25 | 新增 Traceability 驗證（TR1-TR3） |

---

## 附錄：檔案位置索引

| 檔案 | 路徑 |
|------|------|
| Agent 指令 | `flowkit/agents/flowkit.pre-unify-check.agent.md` |
| 相關指令：consistency-check | `flowkit/agents/flowkit.consistency-check.agent.md` |
| 相關指令：unify-flow | `flowkit/prompt/flowkit.unify-flow.prompt.md` |
