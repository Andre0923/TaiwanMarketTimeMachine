# Copilot Repository Instructions

> **適用範圍**：所有 AI Agent 模式與 Chat 模式  
> **語言規範**：關鍵字（MUST / SHOULD / MAY / NEVER）維持英文，其餘使用繁體中文  
> **核心原則**：本規範為 AI 全域行為準則，搭配 SpecKit 開發憲法使用

---

## 1. 治理規範 🔴 NON-NEGOTIABLE

### 1.1 語言規範
- 回覆與文件敘述一律使用**繁體中文**
- 專有名詞與規範關鍵字維持英文：MUST / SHOULD / MAY / NEVER / STOP / ASK
### 1.2 不確定時 MUST 先詢問
若遇下列事項不明確或不確定時，MUST 先 ASK 人類，不得自行假設或直接修改：
- 需求、資料欄位、流程邏輯或架構決策
- 涉及刪除現有功能
### 1.3 重大變更需先提案
任何重大變更前 MUST 先提出變更提案，等待明確批准：
- 跨模組重構
- API / 行為調整
- 資料模型或格式變更
- 架構變更
## 1.4 「先討論再實作」模式
當人類說「先討論再實作」時，流程為：
 - 需求澄清 →提案（步驟、影響範圍、測試策略）→確認後再實作

**在此模式下**：
- 禁止貼出可直接覆蓋的大段程式碼
- 允許最小可驗證片段或偽碼以供討論
- 如有疑慮，先提問確認，不得自行假設

## 1.5 目錄規範
- log、test、程式碼、文件等檔案 MUST 放在對應目錄，
```
logs/        ← 日誌檔案
tests/       ← 測試檔案
src/         ← 程式碼
docs/        ← 專案文件
specs/       ← 規格文件
.artifacts/  ← 工具產生的可再生產物（coverage、build 等）
```

- 更詳細的目錄結構規範參考，請見 `docs/00.目錄結構.md`，當AI不確定位置時，MUST 依此文件規範執行。

### 1.5.1 測試產物規範（Artifacts）
- 所有測試產物（coverage、pytest cache、htmlcov 等）MUST 輸出到 `.artifacts/`
- `.artifacts/` MUST 被 `.gitignore` 排除
- 詳見 Constitution §1.2「測試與分析產物目錄規範」


### 1.6 改版歷史統一放置
所有套件與規範的改版歷史 MUST 統一放置於 `docs/76.改版歷史/`，以減少指令化檔案的 Token 使用量：
```
docs/76.改版歷史/
├── flowkit-version-history.md      ← FlowKit 套件改版歷史
├── constitution-sync-report.md     ← SpecKit Constitution 改版歷史
└── copilot-instructions-history.md ← Copilot Instructions 改版歷史（未來）
```
**MUST NOT**：在指令化檔案（`.github/agents/`、`.cursor/commands/`）內嵌版本歷史區塊。

---

## 2. SDD 核心提醒

本專案採用 **Specification-Driven Development（SDD）**，詳見 `.specify/memory/constitution.md`。

`speckit 流程: specify → plan → tasks → analyze → implement `
### 2.1 唯一真相來源
- **行為定義**：`specs/system/spec.md`
- **資料模型**：`specs/system/data-model.md`
- **介面契約**：`specs/system/contracts/`
- **流程設計**：`specs/system/flows.md`
- **UI 設計**：`specs/system/ui/`

### 2.2 AI 行為約束
- AI 以 `specs/system/*` 為已定案的行為真相
- AI 以 `specs/feature/NNN-feature-name/` 為本次開發增修的行為真相
- AI 不得以「程式碼現況」推翻 spec
- AI 不得從 `specs/history/` 推導現行行為

---

## 3. System Spec 保護 🔴 CRITICAL

```
NEVER 修改 specs/system/**，
除非指令中明確指出正在執行 UNIFY FLOW，
且清楚指定要修改的檔案與段落。
```

### 3.1 Unify Flow 規則
- System Spec 的唯一修改通道是 Unify Flow
- Feature 開發期間 MUST NOT 直接修改 `specs/system/**`
- 詳細流程見 `unify-flow.prompt.md`

---

## 4. User Story 格式 以 BDD 規格標準

### 4.1 User Story 格式（MUST）
```markdown
### US X-N: <一句話功能摘要>

**As a** <角色>  
**I want** <希望系統協助達成的事情>  
**So that** <能獲得的結果或價值>
```

### 4.2 Acceptance Criteria 格式（MUST）
```markdown
#### Acceptance Criteria

**AC1 — <語意標題>**
- **Given** <前置條件>
- **When** <觸發動作>
- **Then** <預期結果>
```

### 4.3 AC 撰寫規範
- AC 數量依情境而定，建議 1～5 條
- MUST 涵蓋正常與例外情境
---

## 5. Test-First 規範 🔴 NON-NEGOTIABLE

### 5.1 測試優先順序
1. MUST 先從對應 User Story 的 AC 衍生或更新測試案例
2. 在 `tests/` 新增或更新測試
3. 才可修改 `src/` 程式碼

### 5.2 測試要求
- 優先以「單元測試」，若單元測試不可行，MAY 以整合或端對端測試替代。
- 所有測試檔案 MUST 放在 `tests/`
- 測試名稱 SHOULD 標註對應的 US / AC 編號
- 重大變更不得僅修改 `src/`，不更新對應測試

---
## 6. Maintainability & Reusability First 🟡

 **設計決策** 及 **程式碼撰寫** 風格決策，優先考量系統的可維護性與可複用性。

**SHOULD 要求**:
- 優先選擇可維護性與可複用性高的方案
- 在成本差異不大時，選擇長期可維護的設計
- 功能應設計為獨立模組，具備清晰目的
**MUST 遵守**:
- 單一職責原則 (Single Responsibility Principle)
- 低耦合、高內聚 (Low Coupling, High Cohesion)
- 模組 MUST 自給自足、可獨立測試、具備文件
**成本權衡準則**:

| 成本差異   | 選擇        | 理由          |
| ------ | --------- | ----------- |
| < 20%  | ✅ 可維護方案   | 長期收益 > 短期成本 |
| 20-50% | 🟡 評估生命週期 | 長期維護建議可維護方案 |
| > 50%  | 🔴 團隊討論   | 技術債務追蹤      |

---
## 7.Interface-Logic Separation 🟡

**MUST 要求**:
- 明確分離介面層 (UI/API/CLI) 與業務邏輯層
- 確保修改介面不影響邏輯或資料流程
- 定義穩定的互動邊界 (DTO、輸入參數、事件物件)

**架構模式**:
```
┌────────────────┐
│ Interface      │ ← UI/API/CLI (可變動)
├────────────────┤
│ DTO/Events     │ ← 穩定契約
├────────────────┤
│ Business Logic │ ← 核心邏輯 (穩定)
└────────────────┘
```

---

## 8. 程式碼規範

### 8.1 檔案長度限制
- 一般模組：400～800 行
- 超過 800 行 SHOULD 拆分
- 超過 1000 行 MUST 拆分
### 8.2 單一職責原則
- 每個模組 MUST 有明確的責任範疇
- 不得讓單一檔案同時處理：資料模型 + 業務流程 + CLI
### 8.3 模組設計原則 
 - 低耦合、高內聚 (Low Coupling, High Cohesion)
 - 模組 MUST 自給自足、可獨立測試、具備文件
 - 模組間互動透過明確契約 (API/DTO/Event) 定義
 - 模組設計應優先考量可維護性與可複用性
### 8.3 函式長度
- 超過 50～70 行 SHOULD 拆分為子函式
- 同時操作多種資源的函式 MUST 拆分
### 8.4 最小變更原則
- 僅修改必要區塊，禁止 drive-by refactor
- 未經明確要求，不得進行：大規模重新命名、刪除檔案、刪除現有功能
### 8.5 Docstring 規範
- **模組級**：MUST 撰寫，簡述責任範疇與協作對象
- **類別級**：SHOULD 撰寫，說明責任與重要屬性
- **函式級**：依複雜度，簡單函式一行摘要，複雜函式需 Args/Returns/Raises

---

## 9. Observability 規範 🔴 NON-NEGOTIABLE

### 9.1 日誌要求
**MUST 要求**:
- 所有自動化流程 MUST 具備明確的 logging 輸出
- MUST 使用 logging 模組，禁止使用 `print` 作為日誌輸出
- 所有日誌 MUST 寫入 `logs/` 目錄
- 日誌命名格式：`YYYYMMDD_HHMMSS.log

**SHOULD 遵守**:
- 關鍵業務流程 SHOULD 記錄 start / end / error 事件
- 提供執行歷程追蹤機制

### 9.2 日誌等級
- `DEBUG`：詳細除錯資訊
- `INFO`：一般性訊息（流程 start/end）
- `WARNING`：警告訊息
- `ERROR`：錯誤訊息（需包含錯誤碼與上下文）
- `CRITICAL`：嚴重錯誤

---

## 10. UI 行為治理

> 僅適用於 UI Impact ≠ None 的 Feature

### 10.1 行為治理（MUST）
- UI 行為 MUST 以 User Story + AC 記錄
- 非同步 UI 行為的 AC，MUST 定義 Loading / Empty / Error 狀態
- 涉及不可逆操作的 AC，MUST 包含確認機制描述

### 10.2 UI ID 格式
- `[UI-SCR-###]`：Screen（畫面）
- `[UI-CMP-###]`：Component（元件）
- `[UI-PAT-###]`：Pattern（互動模式）
- `[UI-STATE-###]`：State（狀態規則）

### 10.3 禁止事項
- ❌ 不得建立第二份「UI spec」取代 AC 的行為真相
- ❌ 不得實作 AC 未定義的 UI 行為

---

## 11. Debug / Bug Fix 規範

### 11.1 優先處理方式
debug / Bug Fix 時，盡可能使用**refine-loop**，若沒有使用時請依序優先處理下列三項：
1. 程式碼修正
2. 測試補強
3. Feature 層級文件調整（不含 `specs/system/**`）

### 11.2 約束
- 不得以修 Bug 為理由修改 System Spec（需走 Unify Flow）
- Bug Fix 後 MUST 補測試，避免回歸

---

## 12. Git 提交規範

### 12.1 提交時機（MUST）

**階段性完成**，例如： 完成 Phase階段、Unify Flow、Bug Fix

**對話結束時**：
- 若有任何檔案增修，MUST 執行 git commit + push
- 若無增修，則不需提交

### 12.2 Commit Message 格式
```
<type>: <繁體中文摘要>

<詳細說明（選填）>

新增:
- <item>

修改:
- <item>

修復:
- <item>
```

**Type 類型**：
- `feat`：新功能
- `fix`：Bug 修復
- `refactor`：重構（不影響功能）
- `docs`：文件
- `test`：測試
- `chore`：雜項

---

## 13. Python 環境標準

> 僅適用於 Python 專案

### 13.1 工具要求（MUST）
- 使用 `uv` 作為唯一環境與依賴管理工具
- 維護 `uv.lock`

### 13.2 標準指令

| 操作     | 指令                       |
| ------ | ------------------------ |
| 安裝套件   | `uv add <package>`       |
| 建立虛擬環境 | `uv venv`（使用 `./.venv/`） |
| 初始化專案  | `uv init <project-name>` |
| 執行程式   | `uv run <script.py>`     |

### 13.3 禁止指令
`pip`, `python -m venv`, `pipenv`, `conda`, `poetry`, `pipx`

---

## 14. After Changes Checklist

每次修改完成後 MUST 執行：

- [ ] 說明已執行或應執行的 CHECKS（tests / lint / build）
- [ ] 清楚摘要「修改了什麼」以及「為什麼要這樣改」
- [ ] 執行 `git add . && git commit && git push`（若為階段性完成）
- [ ] 若涉及 UI，確認 UI 文件已同步

---

## 附錄：快速參考

### 文件位置對照

| 文件 | 位置 |
|------|------|
| Constitution | `.specify/memory/constitution.md` |
| System Spec | `specs/system/spec.md` |
| System Design | `specs/system/data-model.md`, `flows.md`, `contracts/`, `ui/` |
| Feature Spec | `specs/features/NNN-*/spec.md` |

### 指令化流程

| 流程 | 說明 |
|------|------|
| Unify Flow | Feature 完成後，合併至 System Spec |
| Refine Loop | Debug/優化循環 |
| Project Context | 專案上下文更新 |

### NON-NEGOTIABLE 條款速查

| 章節 | 條款 |
|------|------|
| §1 | 治理規範（語言、詢問、提案） |
| §3 | System Spec 保護 |
| §5 | Test-First |
| §9 | Observability |
| §13 | Python 環境（uv） |

---

**版本**：v1.0.0  
**日期**：2026-01-21  
