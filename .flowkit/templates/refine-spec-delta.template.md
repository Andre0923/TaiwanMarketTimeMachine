# Refine Spec Delta: {BRIEF_DESCRIPTION}

> **Refine ID**: RC{NNN}  
> **Created**: {DATE}  
> **Base Spec**: [spec.md](./spec.md)  
> **變更數量**: {N}

---

## 變更摘要

| 變更 ID | 類型 | 摘要 | 影響的 User Story | UI Impact |
|---------|------|------|------------------|-----------|
| RC001 | [NEW] | {摘要} | 新增 US{N} | None / Low / High |
| RC002 | [MODIFIED] | {摘要} | 調整 US{N} | None / Low / High |
| RC003 | [DELETED] | {摘要} | 移除 US{N} | N/A |
| RC004 | [FIXED] | {摘要} | 修正 US{N} | None / Low / High |

---

## UI/UX 影響評估（若 UI Impact ≠ None）

> 若所有變更的 UI Impact = None，此區塊標記「N/A」。

| 項目 | 值 |
|------|-----|
| **涉及畫面** | <!-- [UI-SCR-###] 或 [UI-TBD: 描述] --> |
| **涉及模式** | <!-- [UI-PAT-###] 或 [UI-TBD: 描述] --> |
| **涉及狀態** | <!-- [UI-STATE-###] 或 N/A --> |

---

## 變更詳細規格

### 變更 RC001：[NEW] {功能摘要}

#### US{N}: {一句話功能摘要} [NEW]

**As a** {角色}  
**I want** {我希望系統協助達成的事情}  
**So that** {我能獲得的結果或價值}

##### Acceptance Criteria

- **AC1 — {語意標題}**
    - **Given** {前置條件}
    - **When** {觸發動作}
    - **Then** {預期結果}

- **AC2 — {語意標題}**
    - **Given** {前置條件}
    - **When** {觸發動作}
    - **Then** {預期結果}

---

### 變更 RC002：[MODIFIED] {功能摘要}

#### US{N}: {現有功能摘要} [MODIFIED]

**變更說明**：{變更原因}

##### Acceptance Criteria（已調整）

- **AC1 — {標題}** [MODIFIED]
    - **Given** {前置條件}
    - **When** {動作}
    - **Then** {新的預期結果}

- **AC2 — {標題}**（保留）
    - _(若 AC 未變更，標記「保留」，不需重複撰寫內容)_

---

### 變更 RC003：[DELETED] {功能摘要}

#### ~~US{N}: {刪除功能摘要}~~ [DELETED]

**刪除原因**：{說明}

---

### 變更 RC004：[FIXED] {功能摘要}

#### US{N}: {現有功能摘要} [FIXED]

**修正說明**：{問題描述與修正方向}

##### Acceptance Criteria（已修正）

- **AC{N} — {標題}** [FIXED]
    - **Given** {前置條件}
    - **When** {動作}
    - **Then** {修正後的預期結果}

---

## 驗證檢查清單

- [ ] 所有變更項目已產生規格片段
- [ ] 變更類型標記正確（[NEW]/[MODIFIED]/[DELETED]/[FIXED]）
- [ ] 使用 BDD 格式（Given/When/Then）
- [ ] 無實作細節洩漏（如檔案名稱、函數名稱、技術選擇）
- [ ] 無與現有 spec.md 衝突
- [ ] [NEEDS CLARIFICATION] 不超過 3 個

---

## 附註

- **本文件為變更規格片段集合**，不是完整的 Feature Spec
- **Phase 6 整合時**，將本文件的變更合併回 spec.md，並移除所有變更標記
- **變更標記**（[NEW]/[MODIFIED]/[DELETED]/[FIXED]）僅在本文件中使用，最終 spec.md 不得殘留
