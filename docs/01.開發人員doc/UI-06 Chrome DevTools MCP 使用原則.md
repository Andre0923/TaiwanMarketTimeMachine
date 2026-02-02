**目的**
​
確保 UI 微調（layout / spacing / visual consistency）能在不破壞程式架構的前提下，
​
以「可視化調整 + AI 自動同步」的方式執行，使開發流程可控、可回溯、可測試。

---
## 6.1 適用情境（When to Use）
Chrome DevTools MCP（以下簡稱 DevTools-MCP）應在以下情況啟用：
1. **需要進行視覺微調（non-structural changes）時：**
    - margin / padding / gap
    - flex / grid 調整
    - font-size / color / border / shadow
    - spacing、對齊、版面細節
2. **AI 輸出的 UI 初稿不符合視覺預期，需要人工視覺調整。**
3. **Acceptance Criteria 涉及 UI 呈現、互動行為或 layout 穩定性。**
4. **開發者希望避免自然語言造成的版面幻覺或 AI 過度修改。**

---
## 6.2 禁止使用情境（When _Not_ to Use）
不得使用 DevTools-MCP 自動同步以下內容：
1. **Domain / Business Logic**
    - 與 UI 無關的邏輯不得透過 DevTools-MCP 更改。
2. **資料流、狀態管理架構（State / Store / Hooks）**
3. **API 結構、型別、資料 Schema**
4. **Tailwind config、Design Tokens、全域樣式定義**
若涉及上述修改，必須由 Spec Kit 與 AI 作為主流程，依據 Spec / AC 正式更新。

---
## 6.3 開發流程（Standard Workflow）
UI 變更需遵守以下步驟：
### Step 1：產生 UI 初稿
- 使用 Copilot / Claude 依據 User Story / AC 生成 component 或頁面骨架。
- 僅要求結構正確（sections / hierarchy），不追求最終視覺。
### Step 2：在瀏覽器開啟 DevTools
- 執行 `npm run dev` 或專案啟動指令。
- 開啟 Chrome → DevTools（F12）。
- 在 Elements / Styles / Layout 直接調整 CSS。
### Step 3：以 DevTools 微調視覺
允許調整：
- margin / padding / gap
- width / height / flex / grid
- font-size / line-height
- 色彩、投影、過渡
- breakpoints（僅限 layout，不含全域 tokens）
禁止：
- 刪除 component
- 重寫 HTML 結構
- 變更語義性元素（例如 div → button）
- 任意新增 JS 行為
### Step 4：由 DevTools-MCP 同步程式碼
微調完成後，由 AI 執行：
> 「使用 Chrome DevTools MCP，將目前 DevTools 中的 CSS / Style 變更同步回專案檔案，保持 Tailwind 與 component 結構一致。」
要求：
- 僅產生 **minimal diff**
- 不得重寫整段 component
- 不得改動 AC 以外的功能
- 不得新增 class / style 以外的程式碼
### Step 5：審查與 Commit
- 逐行檢查 diff
- 不符合規範的變更需退回並重跑微調
- Commit message 需描述 UI 調整原因，例如：
`UI: refine spacing for backtest summary panel (DevTools-MCP sync)`

---
## 6.4 UI 行為驗證（Optional, but Recommended）
若 Acceptance Criteria 涉及互動流程（Given/When/Then），
​
可透過 DevTools-MCP 指示 AI 進行 UI 驗證：
範例：
> 「使用 Chrome DevTools MCP，按照 US-004 的 AC 自動操作 UI，回報是否符合預期（包含 console error 檢查）。」
可用於：
- Drop-down 行為
- 表單輸入流程
- 切換 tab / 模組
- Backtest → 結果顯示流程
不可用於：
- 資料正確性（需單元測試驗證）
- 商業邏輯正確性
- 後端 API 整合行為（需 integration test）

---
## 6.5 版本控管規範
所有透過 DevTools-MCP 產生的變更需：
- 以最小化 diff commmit
- 不得合併多功能修改到同一 commit
- PR 需標示：
`[UI-MCP] Fine-tuned homepage layout spacing (Step 2.3)`
若 diff 超過 30 行，需人工審查是否構成「結構性修改」，
​
若是，必須退回由 Spec Kit 重產該 component。

---
## 6.6 安全規範 / 限制
- 不得使用 DevTools-MCP 操作非專案頁面（例如銀行、券商、Gmail）。
- 不得在 SCP 或私人系統中啟用自動化操作。
- 使用者需確認 Chrome instance 僅開啟與專案 UI 相關的頁面。

---
## 6.7 本章地位
本章屬《UI 開發準則》的延伸細則，
​
若與 System Architecture / UI Structure 章節衝突，
​
需以「系統架構規範」與「唯一真相文件」為優先。