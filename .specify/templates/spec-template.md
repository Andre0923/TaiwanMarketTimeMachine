---
milestone: null
system_context: false
created: {DATE}
updated: {DATE}
---

# Feature Specification: {FEATURE_NAME}

> **Feature ID**: {FEATURE_ID}  
> **Status**: Draft

---

## 1. Feature Overview

### 1.1 Problem Statement

<!-- 
描述要解決的問題：
- 目前的痛點是什麼？
- 為什麼需要這個 Feature？
- 影響範圍有多大？
-->

### 1.2 Goal

<!-- 
本 Feature 的目標：
- 完成後使用者可以做什麼？
- 系統會有什麼改變？
-->

### 1.3 Success Criteria

| 指標 | 目標值 | 驗證方式 |
|------|--------|----------|
| <!-- 指標名稱 --> | <!-- 目標數值或狀態 --> | <!-- 如何驗證 --> |

---

## 2. User Stories

### US1: [一句話功能摘要]

**As a** [角色]  
**I want** [我希望系統協助達成的事情]  
**So that** [我能獲得的結果或價值]

#### Acceptance Criteria

- **AC1 — [語意標題]**
    - Given [前置條件]
    - When [觸發動作]
    - Then [預期結果]

- **AC2 — [語意標題]**
    - Given [前置條件]
    - When [觸發動作]
    - Then [預期結果]

---

### US2: [一句話功能摘要]

**As a** [角色]  
**I want** [我希望系統協助達成的事情]  
**So that** [我能獲得的結果或價值]

#### Acceptance Criteria

- **AC1 — [語意標題]**
    - Given [前置條件]
    - When [觸發動作]
    - Then [預期結果]

---

## 3. Assumptions

1. <!-- 假設條件：開發時的前提假設 -->
2. <!-- 例如：現有程式碼保留 -->
3. <!-- 例如：最小化變更 -->

---

## 4. Key Entities

### 4.1 [實體名稱]

| 欄位 | 型別 | 說明 |
|------|------|------|
| <!-- 欄位名 --> | <!-- 資料型別 --> | <!-- 說明 --> |

---

## 5. Dependencies

- <!-- 外部依賴：需要的套件、服務 -->
- <!-- 內部依賴：需要的其他模組 -->

---

## 6. UI/UX 影響評估

> 評估本 Feature 對 UI 的影響程度，供 plan 階段規劃 UI 任務。
> 若專案無 UI（純 CLI/API），此區塊可標記「N/A」或移除。

| 項目 | 值 |
|------|-----|
| **UI Impact** | <!-- None / Low / High --> |
| **UI Maturity Target** | <!-- L0 / L1 --> |
| **涉及畫面** | <!-- [UI-SCR-###] 或 [UI-TBD: 描述] 或 N/A --> |
| **涉及模式** | <!-- [UI-PAT-###] 或 [UI-TBD: 描述] 或 N/A --> |
| **涉及狀態** | <!-- [UI-STATE-###] 或 [UI-TBD: 描述] 或 N/A --> |
| **UI Unknowns** | <!-- 最多 3 項，可用 [NEEDS CLARIFICATION] --> |

### UI References（若適用）

> 列出 User Stories 引用的 UI 設計元素。
> 詳細定義請見 `specs/system/ui/`。

| UI ID | 類型 | 說明 | 所屬 User Story |
|-------|------|------|------------------|
| <!-- [UI-SCR-001] --> | Screen | <!-- 說明 --> | <!-- US1 --> |
| <!-- [UI-PAT-003] --> | Pattern | <!-- 說明 --> | <!-- US2 --> |

---

## 7. Out of Scope

以下項目不在本 Feature 範圍內：

1. <!-- 明確排除的項目 -->
2. <!-- 避免範圍蔓延 -->
