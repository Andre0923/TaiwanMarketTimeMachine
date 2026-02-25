# UI Design Index

> **位置**：`specs/system/ui/`  
> **角色**：UI 文件索引 + 規則說明  
> **版本**：1.0.0  
> **最後更新**：<!-- 填入日期 -->

---

## Scope（適用範圍）

- **Clients**: <!-- Web / Desktop / Mobile / Embedded -->
- **SoT 關係**: CLI/API 為 SoT，UI 為 Client

---

## Documents（文件清單）

| 文件 | 說明 | 成熟度 |
|------|------|--------|
| [ui-structure.md](./ui-structure.md) | Screen/Flow/Component Catalog | L0→L1 |
| [ux-guidelines.md](./ux-guidelines.md) | States/Patterns/a11y | L0→L1 |

---

## ID Conventions（ID 命名規則）

| 類型 | 格式 | 範例 | 說明 |
|------|------|------|------|
| Screen | `[UI-SCR-###]` | `[UI-SCR-001]` | 獨立畫面 |
| Component | `[UI-CMP-###]` | `[UI-CMP-001]` | 可重用元件 |
| Pattern | `[UI-PAT-###]` | `[UI-PAT-001]` | 互動模式 |
| State | `[UI-STATE-###]` | `[UI-STATE-001]` | 狀態規則 |

---

## Maturity Levels（成熟度等級）

| Level | 名稱 | 定義 | Gate |
|-------|------|------|------|
| **L0** | Draft | 概念描述、未完整定義 | specify 可通過 |
| **L1** | Buildable | 完整定義、可直接實作 | implement 必須達到 |

### L0 → L1 升級標準

- **Screen (L1)**：Purpose、Entry Point、Regions、Key Interactions 皆已填寫
- **Component (L1)**：Responsibility、Inputs、Outputs、States 皆已定義
- **Pattern (L1)**：觸發時機、視覺表現、行為規則皆已明確
- **State (L1)**：觸發條件、視覺表現、處理邏輯皆已定義

---

## Change Policy（變更規則）

1. **UI 行為變更** → MUST 在 `specs/system/spec.md` 以 User Story + AC 記錄
2. **UI 結構變更** → SHOULD 更新本目錄文件，並從 spec.md 引用 UI ID
3. **純視覺變更** → MAY 不納入 SDD（可放 Design System / Figma）

---

## Authority Hierarchy（權威層級）

1. **Behavior SoT**：`specs/system/spec.md`（行為唯一真相）
2. **UI Design Authority**：`specs/system/ui/*`（UI 範圍權威）
3. **Contracts**：`specs/system/contracts/*`（介面契約）

> ⚠️ UI 文件 **不取代** `spec.md` 的行為定義。衝突時以 `spec.md` 為準。

---

## Prohibited Actions（禁止事項）

- ❌ 不得建立第二份「UI spec」取代 `spec.md` 的行為真相
- ❌ UI 文件不得複製 schema/contracts 欄位（只能連結）
- ❌ 不得實作 AC 未定義的 UI 行為

---

## Quick Links（快速連結）

- [System Spec](../spec.md)
- [Data Model](../data-model.md)
- [Flows](../flows.md)
- [Contracts](../contracts/)
