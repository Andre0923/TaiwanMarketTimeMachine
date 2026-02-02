# FlowKit Consistency Check 功能說明

> **指令名稱**：`/flowkit.consistency-check`  
> **Agent 檔案**：`flowkit/agents/flowkit.consistency-check.agent.md`  
> **執行時機**：Plan 完成後、Tasks 執行前

---

## 1. 功能概述

### 1.1 這是什麼？

`/flowkit.consistency-check` 是 **Plan 階段的一致性檢查工具**，在 Feature Plan 產出後、進入實作前執行，用於**儘早發現非意圖性錯誤**。

### 1.2 關鍵概念：「意圖」vs「錯誤」

| 類型 | 說明 | 是否檢查 |
|------|------|----------|
| **意圖內變更** | Feature Spec 聲明要修改 X | ❌ 不檢查（那是意圖） |
| **非意圖性錯誤** | 疏忽、手誤、遺漏複用 | ✅ 本工具檢查 |

**核心原則**：Feature Spec 是「更新來源」，它聲明的變更是「意圖」，不是錯誤。

### 1.3 解決什麼問題？

| 問題類型 | 範例 | 影響 |
|----------|------|------|
| **重複實作** | 設計了已存在的功能 | 浪費時間、維護困難 |
| **遺漏複用** | 未使用已存在的共享服務 | 程式碼重複 |
| **非意圖變動** | Plan 涉及 Spec 未聲明的區域 | 範圍溢出 |
| **細節誤用** | ID 引用錯誤、命名不一致 | 實作時出錯 |

### 1.4 核心價值

```
「Shift-Left 問題發現，在規劃階段攔截疏忽，降低後續修正成本」
```

---

## 2. 使用時機

### 2.1 何時執行？

```
/speckit.specify → /speckit.plan → /flowkit.consistency-check ◄── 在此執行
                                            │
                                   ┌────────┴────────┐
                                   │                 │
                               有問題             無問題
                                   │                 │
                                   ▼                 ▼
                              修正 Plan         /speckit.tasks
                                   │                 │
                                   └────────┬────────┘
                                            ▼
                                   /speckit.implement
```

### 2.2 與 pre-unify-check 的時機差異

| 時機點 | 指令 | 目的 |
|--------|------|------|
| Plan 完成後 | `/flowkit.consistency-check` | 檢查規劃決策 |
| Implement 完成後 | `/flowkit.pre-unify-check` | 檢查實作結果 |

### 2.3 執行條件

| 條件 | 必要性 | 說明 |
|------|--------|------|
| `spec.md` 存在 | REQUIRED | Feature Spec |
| `plan.md` 存在 | REQUIRED | Feature Plan |
| `system-context.md` 存在 | RECOMMENDED | 共享服務清單 |
| System Spec 存在 | HIGH | 用於範圍檢查 |
| `src/` 目錄存在 | RECOMMENDED | 用於重複檢查 |

---

## 3. 檢查項目總覽

### 3.1 五大檢查類別

| 類別 | 代號 | 目的 | 阻擋性 |
|------|------|------|--------|
| 重複實作 | A | 避免重做已有功能 | HIGH |
| 複用遺漏 | B | 確保使用共享服務 | HIGH |
| 非意圖變動 | C | 防止範圍溢出 | HIGH |
| 細節誤用 | D | 避免引用錯誤 | MEDIUM-HIGH |
| 整合建議 | E | 提供改善建議 | 非阻擋 |

### 3.2 檢查項目清單

#### A. 重複實作檢查

| ID | 檢查項目 | 嚴重性 | 說明 |
|----|----------|--------|------|
| A1 | 功能重複 | HIGH | Plan 規劃的功能與現有功能高度相似 |
| A2 | 模組重複 | MEDIUM | Plan 新增的模組名稱與現有模組相似 |
| A3 | 邏輯重複 | MEDIUM | Plan 的處理流程與現有流程雷同 |

**全新功能時**：標記為「適用：部分」，僅檢查是否有可複用的基礎設施。

#### B. 複用遺漏檢查

| ID | 檢查項目 | 嚴重性 | 說明 |
|----|----------|--------|------|
| B1 | 共享服務未使用 | HIGH | system-context.md 列出的共享服務未被引用 |
| B2 | 工具函數重寫 | MEDIUM | Plan 設計了已存在的工具函數 |
| B3 | 模式未遵循 | MEDIUM | Plan 未遵循專案既有的設計模式 |

**全新功能時**：B1 仍適用（應使用共享服務），B2-B3 視情況標記 N/A。

#### C. 非意圖變動檢查

| ID | 檢查項目 | 嚴重性 | 說明 |
|----|----------|--------|------|
| C1 | 範圍溢出 | HIGH | Plan 涉及 Spec 未聲明的變更區域 |
| C2 | 隱性依賴 | MEDIUM | Plan 的修改會影響未列出的模組 |
| C3 | 副作用風險 | MEDIUM | Plan 的架構決策可能影響現有功能 |

#### D. 細節誤用檢查

| ID | 檢查項目 | 嚴重性 | 說明 |
|----|----------|--------|------|
| D1 | ID 引用錯誤 | HIGH | 引用的 UI ID / Entity ID 不存在 |
| D2 | 命名不一致 | MEDIUM | 與專案命名慣例不符 |
| D3 | 路徑錯誤 | MEDIUM | Plan 中的檔案路徑格式錯誤 |
| D4 | 版本不符 | LOW | 引用的套件版本與專案不一致 |

#### E. 整合建議（非阻擋性）

| ID | 檢查項目 | 類型 | 說明 |
|----|----------|------|------|
| E1 | 更好的模組位置 | SUGGESTION | Plan 的新模組可放在更合適的位置 |
| E2 | 可抽象化機會 | SUGGESTION | Plan 的實作可抽象為共享服務 |
| E3 | 現有模式適用 | SUGGESTION | 可套用專案既有的設計模式 |

---

## 4. 執行流程

### Phase 0：前置條件檢查

```markdown
1. 確認 Feature 目錄存在（spec.md + plan.md）
2. 確認參考資料存在（system-context.md、System 層、src/）
3. 判斷 Feature 類型（全新/修改/重構）
```

### Phase 1：抽取 Plan 決策清單

```markdown
1. 抽取架構決策（技術/框架、新模組、修改模組）
2. 抽取檔案清單（新增/修改）
3. 抽取依賴關係（外部套件、內部模組）
```

### Phase 2：比對現有系統（漸進式）

```markdown
1. 模組邊界檢查（與 system-context.md 比對）
2. 功能重複檢查（與 src/ 結構比對）
3. 變更範圍檢查（與 Spec 聲明比對）
```

### Phase 3：一致性檢查（檢測通道）

```markdown
執行 A-E 五大類別檢查
```

### Phase 4：產生分析報告

```markdown
1. 分類：確定問題 / 待確認 / 整合建議
2. 判定下一步
```

---

## 5. 輸出格式

### 5.1 報告結構

```markdown
## FlowKit Consistency Check 分析報告

### 基本資訊
- **Feature**：001-user-management
- **Feature 類型**：全新功能
- **執行時間**：2026-01-25 10:30

### 檢查結果摘要

| 類別 | 確定問題 | 待確認 | N/A |
|------|----------|--------|-----|
| A. 重複實作 | 0 | 1 | 0 |
| B. 複用遺漏 | 1 | 0 | 0 |
| C. 非意圖變動 | 0 | 0 | 0 |
| D. 細節誤用 | 0 | 0 | 0 |
| E. 整合建議 | - | 2 | - |
```

### 5.2 問題分類說明

| 分類 | 說明 | 處理方式 |
|------|------|----------|
| **確定問題** | 明確需要修正的問題 | 必須修正 Plan |
| **待確認** | 需人工判斷是否為問題 | 確認是否為意圖 |
| **整合建議** | 非阻擋性的改善建議 | 可選擇採納 |

### 5.3 下一步指引

| 情況 | 下一步 |
|------|--------|
| 有「確定問題」 | 修正 Plan 後重新執行本檢查 |
| 僅有「待確認」 | 人工確認後可繼續 `/speckit.tasks` |
| 全部通過 | 執行 `/speckit.tasks` |

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

| Plan 涉及類別 | 讀取的 System Design 檔案 |
|---------------|---------------------------|
| 資料欄位變更 | `data-model.md` 的相關 Entity |
| API/Webhook 變更 | `contracts/*.md` 的相關定義 |
| 流程變更 | `flows.md` 的相關 Flow |
| UI 變更 | `ui/*.md` 的相關 Screen/Pattern |

---

## 7. 與其他指令的關係

### 7.1 上游指令

| 指令 | 關係 |
|------|------|
| `/speckit.plan` | 產生 plan.md 後才能執行本指令 |

### 7.2 下游指令

| 指令 | 關係 |
|------|------|
| `/speckit.tasks` | 本指令通過後執行 |
| `/flowkit.pre-unify-check` | 追蹤本指令的報告 |

### 7.3 與 pre-unify-check 的互補關係

```
┌─────────────────────────────────────────────────────────────────┐
│                   兩階段檢查設計                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌─────────────────────┐          ┌─────────────────────┐      │
│   │ consistency-check   │          │ pre-unify-check     │      │
│   │ (Plan 階段)         │          │ (Implement 後)      │      │
│   ├─────────────────────┤          ├─────────────────────┤      │
│   │                     │          │                     │      │
│   │ 「這個規劃合理嗎？」 │   ───►   │ 「這個實作對嗎？」   │      │
│   │                     │          │                     │      │
│   │ • 有沒有重複做       │          │ • Spec 品質達標嗎    │      │
│   │ • 有沒有忘記複用     │          │ • 引用都正確嗎       │      │
│   │ • 有沒有超出範圍     │          │ • 實作與 Spec 對齊嗎 │      │
│   │                     │          │ • 已知問題處理了嗎   │      │
│   └─────────────────────┘          └─────────────────────┘      │
│            │                               │                    │
│            └───────────追蹤報告────────────┘                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8. 使用範例

### 8.1 基本使用

```
/flowkit.consistency-check
```

自動偵測當前 Feature 目錄並執行檢查。

### 8.2 指定 Feature

```
/flowkit.consistency-check 001-user-management
```

### 8.3 輸出範例

```markdown
## FlowKit Consistency Check 分析報告

### 檢查結果摘要

| 類別 | 確定問題 | 待確認 | N/A |
|------|----------|--------|-----|
| A. 重複實作 | 0 | 1 | 0 |
| B. 複用遺漏 | 1 | 0 | 0 |
| C. 非意圖變動 | 0 | 0 | 0 |
| D. 細節誤用 | 0 | 0 | 0 |
| E. 整合建議 | - | 2 | - |

### 確定問題（必須處理）

| ID | 類別 | 嚴重性 | 說明 | 建議修正 |
|----|------|--------|------|----------|
| B1 | 複用遺漏 | HIGH | 未使用 LibraryManager | 引用 src/storage/library_manager.py |

### 待確認項目（需人工判斷）

| ID | 類別 | 說明 | 需確認的問題 |
|----|------|------|--------------|
| A2 | 重複實作 | Plan 新增 UserHandler 與現有 UserService 相似 | 這是意圖內的新設計嗎？ |

### 整合建議（非阻擋性）

| ID | 說明 | 效益 |
|----|------|------|
| E1 | UserHandler 可放在 src/handlers/ | 符合現有架構 |
| E3 | 可套用 Repository Pattern | 提高可測試性 |

### 下一步
- 修正 B1（複用遺漏）後重新執行本檢查
- 確認 A2 是否為意圖內設計
```

---

## 9. 常見問題

### Q1：什麼是「意圖內變更」？

**A**：Feature Spec 明確聲明要修改的內容。例如：
- Spec 說「修改 User Entity 加入 email 欄位」→ 修改 User 是意圖
- Plan 說「順便修改 Order Entity」→ Spec 沒提到，可能是非意圖變動

### Q2：全新功能需要做什麼檢查？

**A**：全新功能仍需檢查：
- A1-A3（重複實作）：部分適用，檢查是否有可複用的基礎設施
- B1（共享服務）：適用，應使用已存在的共享服務
- C1-C3（非意圖變動）：部分適用，因為是全新功能
- D1-D4（細節誤用）：適用，ID 引用錯誤還是錯誤

### Q3：沒有 system-context.md 可以執行嗎？

**A**：可以，但會跳過共享服務檢查（B1）並產生 WARNING。建議先執行 `/.flowkit.system-context` 建立。

### Q4：「待確認」項目一定要處理嗎？

**A**：不一定。待確認項目需要人工判斷：
- 若確認是意圖內設計 → 標記為「意圖內」，可繼續
- 若確認是問題 → 修正 Plan

---

## 10. 版本歷史

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.0.0 | 2026-01-23 | 初始版本，從 pre-unify-check 重新設計，聚焦非意圖性錯誤 |
| 1.0.1 | 2026-01-25 | 新增 System 層分層讀取規則 |

---

## 附錄：檔案位置索引

| 檔案 | 路徑 |
|------|------|
| Agent 指令 | `.github/agents/flowkit.consistency-check.agent.md` |
| 相關指令：pre-unify-check | `.github/agents/flowkit.pre-unify-check.agent.md` |
| 相關指令：system-context | `.github/agents/flowkit.system-context.agent.md` |
| 架構設計文件 | `docs/77.flowkit相關文件/design-proposals/consistency-check-architecture.md` |
