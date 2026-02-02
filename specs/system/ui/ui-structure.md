# UI Structure — Screen & Component Catalog

> **位置**：`specs/system/ui/ui-structure.md`  
> **角色**：畫面/元件/區塊的結構定義  
> **版本**：1.0.0  
> **最後更新**：<!-- 填入日期 -->

---

## 1. Screen Map（畫面地圖）

> 列出所有系統畫面，每個畫面一個區塊。

### [UI-SCR-001] <!-- 畫面名稱 -->

| 項目 | 說明 |
|------|------|
| **Purpose** | <!-- 畫面目的 --> |
| **Entry Point** | <!-- 進入方式：URL / 導覽 / 條件 --> |
| **Primary User Goals** | <!-- 使用者主要目標 --> |
| **Maturity** | <!-- L0 / L1 --> |

#### Regions（區塊）

| ID | 名稱 | 職責 |
|----|------|------|
| AR-001 | <!-- 區塊名稱 --> | <!-- 職責說明 --> |
| AR-002 | <!-- 區塊名稱 --> | <!-- 職責說明 --> |

#### Key Interactions

- <!-- 互動描述 -->（連結至 [ux-guidelines.md](./ux-guidelines.md#ui-pat-001)）

#### Data Dependencies

- <!-- 連結至 data-model.md Entity 或 contracts/ API -->

#### Edge Cases

- <!-- 空態/錯誤/權限不足時的顯示 -->

---

### [UI-SCR-002] <!-- 第二個畫面 -->

<!-- 複製上方結構 -->

---

## 2. Component Catalog（元件清單）

> 列出可重用的 UI 元件，每個元件一個區塊。

### [UI-CMP-001] <!-- 元件名稱 -->

| 項目 | 說明 |
|------|------|
| **Responsibility** | <!-- 元件職責 --> |
| **Used In** | <!-- [UI-SCR-###], [UI-SCR-###] --> |
| **Maturity** | <!-- L0 / L1 --> |

#### Inputs（Props/State）

| 名稱 | 型別 | 必填 | 說明 |
|------|------|------|------|
| <!-- prop1 --> | <!-- type --> | <!-- Yes/No --> | <!-- 說明 --> |

#### Outputs（Events）

| Event | Payload | 說明 |
|-------|---------|------|
| <!-- EVT-UI-001 --> | <!-- DTO 結構 --> | <!-- 觸發時機與用途 --> |

#### States

| 狀態 | 條件 | 視覺表現 |
|------|------|----------|
| default | 預設 | <!-- 描述 --> |
| loading | 資料載入中 | <!-- 描述 --> |
| empty | 無資料 | <!-- 描述 --> |
| error | 發生錯誤 | <!-- 描述 --> |
| disabled | 不可操作 | <!-- 描述 --> |

#### Accessibility（a11y）

- **Keyboard**: <!-- Tab 順序、快捷鍵 -->
- **Screen Reader**: <!-- ARIA labels -->

---

### [UI-CMP-002] <!-- 第二個元件 -->

<!-- 複製上方結構 -->

---

## 3. Navigation（導覽結構）

### 3.1 Global Navigation

| 項目 | 說明 |
|------|------|
| **Entry Points** | <!-- 應用程式進入點 --> |
| **Navigation Model** | <!-- sidebar / tabs / router / command palette --> |
| **Deep Link Rules** | <!-- URL 結構、參數傳遞 --> |
| **Back/Forward Behavior** | <!-- 瀏覽器上下頁行為 --> |

### 3.2 Screen Flow

```
[UI-SCR-001] ──┬──→ [UI-SCR-002]
               │
               └──→ [UI-SCR-003]
```

---

## 4. ID Index（ID 索引）

> 快速查找所有已定義的 UI ID。

### Screens

| ID | 名稱 | Maturity |
|----|------|----------|
| [UI-SCR-001] | <!-- 名稱 --> | L0/L1 |

### Components

| ID | 名稱 | Maturity |
|----|------|----------|
| [UI-CMP-001] | <!-- 名稱 --> | L0/L1 |
