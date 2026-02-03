# Group F — AI 協作查詢

> **群組目標**：提供自然語言轉 SQL 的查詢能力  
> **技術範疇**：LangChain SQL Toolkit、Text-to-SQL、Guardrail  
> **依賴關係**：依賴 Group B（查詢執行）

---

## 概述

本群組實現「AI 協作」功能，讓不熟悉 SQL 的研究員能夠：
- 以自然語言描述策略條件
- 系統自動產生對應的 SQL 查詢
- 驗證生成的 SQL 合法性與安全性
- 讓 AI 成為策略研究的加速器

---

## User Stories

### US F-1: 自然語言轉 SQL 查詢

**As a** 策略研究員  
**I want** 用自然語言描述策略條件,系統自動產生 SQL  
**So that** 我不需要學習 SQL 語法也能進行複雜查詢

#### Acceptance Criteria

**AC1 — 自然語言輸入介面**
- **Given** 使用者在查詢介面
- **When** 選擇「AI 協作模式」
- **Then** 應顯示一個文字輸入框並提示範例（如「找出連續三天上漲且成交量放大的股票」）

**AC2 — AI 生成 SQL**
- **Given** 使用者輸入自然語言條件
- **When** 點擊「產生查詢」
- **Then** 系統應呼叫 LangChain SQL Toolkit，產生對應的 SQL 查詢

**AC3 — 生成的 SQL 顯示**
- **Given** AI 成功產生 SQL
- **When** 系統取得結果
- **Then** 應在介面顯示生成的 SQL，並提供「執行」與「編輯」選項

**AC4 — 生成失敗處理**
- **Given** AI 無法理解自然語言條件
- **When** 系統嘗試生成 SQL
- **Then** 應顯示錯誤訊息並建議：重新描述條件或切換至結構化查詢模式

**AC5 — 常見查詢模板**
- **Given** 使用者在 AI 協作模式
- **When** 檢視介面
- **Then** 應提供至少 3 個範例模板（如「突破新高」、「放量跌破支撐」等）

---

### US F-2: AI 生成 SQL 驗證與修正

**As a** 系統管理員  
**I want** 驗證 AI 生成的 SQL 不會造成安全問題或效能災難  
**So that** 系統能安全穩定地執行 AI 產生的查詢

#### Acceptance Criteria

**AC1 — SQL 注入防護**
- **Given** AI 生成的 SQL
- **When** 系統驗證 SQL
- **Then** 應檢查是否包含危險語句（如 DROP、DELETE、UPDATE）並拒絕執行

**AC2 — 資料表白名單**
- **Given** AI 生成的 SQL
- **When** 系統解析 SQL
- **Then** 應確認查詢的資料表在白名單內（僅允許 stock_daily, stock_events）

**AC3 — 查詢複雜度限制**
- **Given** AI 生成的 SQL
- **When** 系統分析查詢
- **Then** 應限制 JOIN 層數（≤ 3）與子查詢深度（≤ 2）

**AC4 — 執行逾時保護**
- **Given** AI 生成的 SQL 被執行
- **When** 查詢時間超過 30 秒
- **Then** 應強制中斷查詢並提示「查詢過於複雜,請簡化條件」

**AC5 — AI 自動修正建議**
- **Given** AI 生成的 SQL 驗證失敗
- **When** 系統偵測到問題（如缺少必要欄位）
- **Then** 應提供修正建議或自動修正並詢問使用者確認

---

## 技術備註

- **AI 模型**：使用 LangChain SQL Toolkit + OpenAI/Claude API
- **Guardrail**：使用 SQL Parser（如 `sqlparse`）進行語法分析
- **資料庫連線**：使用 Read-Only 連線執行 AI 生成的查詢
- **成本控制**：記錄 AI API 呼叫次數與成本

---

## 依賴關係

- **被依賴於**：無（增強功能）
- **依賴於**：Group B（查詢執行機制）
