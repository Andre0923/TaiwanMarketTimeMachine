# Refine Plan: {BRIEF_DESCRIPTION}

> **Refine ID**: RC{NNN}  
> **Created**: {DATE}  
> **Base Plan**: [plan.md](./plan.md)  
> **變更規格**: [refine-spec-delta.md](./refine-spec-delta.md)

---

## 1. 變更摘要

| 變更 ID | 類型 | 摘要 | 技術影響 |
|---------|------|------|----------|
| RC001 | [NEW] | {摘要} | Entity: {Entity}, API: {endpoint} |
| RC002 | [MODIFIED] | {摘要} | Validation: {field} |
| RC003 | [DELETED] | {摘要} | Remove: {component} |
| RC004 | [FIXED] | {摘要} | Fix: {module} |

---

## 2. 技術決策（若有新決策）

> **注意**：僅記錄本次變更的新決策，不重複現有 plan.md 的決策。

| 項目 | 決策 | 理由 |
|------|------|------|
| {技術項目} | {決策內容} | {選擇理由} |

若無新決策，填入：
```
本次變更沿用現有 plan.md 的技術棧和架構決策，無新增技術決策。
```

---

## 3. 設計產物更新（若需要）

### 3.1 Data Model 變更

**是否需要更新 data-model.md？**
- [ ] 是 — 需填寫以下內容
- [ ] 否

**若需要更新：**

| Entity | 變更類型 | 變更內容 |
|--------|----------|----------|
| {Entity Name} | 新增/修改/刪除欄位 | {欄位名稱}: {型別} — {說明} |

---

### 3.2 Contracts 變更

**是否需要更新 contracts/？**
- [ ] 是 — 需填寫以下內容
- [ ] 否

**若需要更新：**

#### API 變更

| Endpoint | 變更類型 | 變更內容 |
|----------|----------|----------|
| {Method} {Path} | 新增/修改參數或回應 | {詳細說明} |

#### Webhook 變更（若適用）

| Event | 變更類型 | 變更內容 |
|-------|----------|----------|
| {event_name} | 新增/修改 payload | {詳細說明} |

---

### 3.3 Flows 變更

**是否需要更新 flows.md？**
- [ ] 是 — 需填寫以下內容
- [ ] 否

**若需要更新：**

| Flow Name | 變更類型 | 變更內容 |
|-----------|----------|----------|
| {Flow Name} | 新增/調整步驟 | {詳細說明} |

---

## 4. Constitution Compliance Check（🔴 必要）

> **依據 plan-template.md §2**：必須檢查本次變更是否符合憲法要求。

### 4.1 NON-NEGOTIABLE Requirements (🔴)

| 條款 | 要求 | 本計畫對應 | 狀態 |
|------|------|------------|------|
| §1.1 SDD 方法論 | 先定義規格再實作 | refine-spec-delta.md → refine-plan.md → tasks.md | ✅ |
| §3.1 Test-First | 先從 AC 衍生測試，再修改程式碼 | tasks.md 測試任務優先於實作任務 | ✅ |
| §3.2 Observability | 使用 logging 模組，禁止 print | 見 §5 Observability & Logging | ✅ |
| §5.1 文件一致性 | spec/plan/tasks 與程式碼語意一致 | 同一 PR 完成同步 | ✅ |

### 4.2 SHOULD Requirements (🟡)

| 條款 | 要求 | 本計畫對應 | 狀態 |
|------|------|------------|------|
| §3.3 | Maintainability & Reusability | {說明} | ✅/⚠️ |
| §3.5 | Minimalism & Clarity | {說明} | ✅/⚠️ |

### 4.3 條件性檢查 (🟡)（若 UI Impact ≠ None）

| 條款 | 要求 | 本計畫對應 | 狀態 |
|------|------|------------|------|
| §3.6.1 | UI 行為以 AC 記錄，定義 Loading/Empty/Error 狀態 | 見 §6 UI/UX 變更 | ⬜/N/A |
| §3.6.2 | UI Maturity 達 L1（若進入 implement） | {說明} | ⬜/N/A |

---

## 5. Observability & Logging（Constitution §3.2）🔴

> **此區塊為必填**：依據憲法 §3.2，所有 plan.md MUST 說明 logging 策略。

### 5.1 本次變更是否涉及自動化流程？

- [ ] **是** — 需填寫以下內容
- [ ] **否** — 請說明原因：{例如：純 UI 樣式調整、文件更新}

### 5.2 Logging 策略（若涉及自動化流程）

| 項目 | 說明 |
|------|------|
| **使用的 Logger 模組** | {例如：src/logger.py，沿用現有 plan.md} |
| **預期新增的 Log Event** | {例如：user_logout, password_validation_failed} |
| **Log Level 使用方式** | {例如：INFO 記錄登出，ERROR 記錄失敗} |
| **是否需擴充 Log Event 定義** | 是/否，{若是請說明} |

### 5.3 對應 System Design 檢查

- [ ] 已確認 `specs/system/flows.md` 的 logging 描述（如有）
- [ ] 本次變更 **不影響** / **需更新** `specs/system/data-model.md` 的 Log Event 定義

---

## 6. UI/UX 變更（Constitution §3.6）🟡

> 僅適用於 UI Impact ≠ None 的變更。若 UI Impact = None，此區塊標記「N/A」。

### 6.1 UI Impact Summary

| 項目 | 值 |
|------|---|
| **UI Impact** | <!-- None / Low / High --> |
| **涉及畫面** | <!-- [UI-SCR-###] 或 [UI-TBD: 描述] --> |
| **涉及模式** | <!-- [UI-PAT-###] 或 [UI-TBD: 描述] --> |
| **涉及狀態** | <!-- [UI-STATE-###] 或 N/A --> |

### 6.2 UI 文件更新任務（若 UI Impact ≠ None）

- [ ] 更新 `ui-structure.md`（若新增 Screen/Component）
- [ ] 更新 `ux-guidelines.md`（若新增 Pattern/State）
- [ ] 分配 UI ID 給所有 `[UI-TBD]` 項目
- [ ] 確認涉及的 AC 定義 Loading/Empty/Error 狀態（若適用）

---

## 7. 風險評估（僅高風險項）

> **注意**：僅記錄高風險項（可能性：高/中，影響：高/中）。

| 風險 | 可能性 | 影響 | 緩解措施 |
|------|--------|------|----------|
| {風險描述} | 高/中 | 高/中 | {緩解方式} |

若無高風險項，填入：
```
本次變更無識別出高風險項目。
```

---

## 8. 實作檢查清單

### Phase 1: 設計產物更新
- [ ] 更新 data-model.md（若需要）
- [ ] 更新 contracts/api.md（若需要）
- [ ] 更新 contracts/webhook.md（若需要）
- [ ] 更新 flows.md（若需要）

### Phase 2-N: 變更實作
- [ ] 依據 refine-tasks.md 執行所有任務
- [ ] 遵守 Test-First 原則
- [ ] 使用 logging 模組（若適用）

### Phase 4: 最終驗證
- [ ] 執行完整測試套件
- [ ] 驗證所有測試通過
- [ ] 驗證 logging 輸出正確（若適用）

---

## 附註

- **本文件為精簡版 plan**，僅包含變更相關的計畫內容
- **技術棧和架構決策**沿用現有 plan.md，除非有新決策
- **Phase 0 Research** 不包含在本文件中（Refine Loop 無需完整 research）
