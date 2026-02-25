# FlowKit Requirement Sync 功能說明

> **指令名稱**：`/flowkit.requirement-sync`  
> **Agent 檔案**：`.github/agents/flowkit.requirement-sync.agent.md`  
> **執行時機**：Unify Flow 前（Pre-Unify Check 前或後）

---

## 1. 功能概述

### 1.1 這是什麼？

`/flowkit.requirement-sync` 是一個 **需求文件同步工具**，用於在 Feature 開發完成後、合併至 System 之前，將開發過程中的調整修正回寫至原始需求文件（PRD 與 User Stories）。

### 1.2 解決什麼問題？

| 問題 | 解決方式 |
|------|----------|
| Feature 開發中調整了需求，但 PRD 未更新 | 自動偵測差異並回寫 |
| User Stories 與 Feature Spec 不一致 | 同步 US/AC 內容 |
| 不確定哪些是刻意修正、哪些是遺漏 | 智慧分類 + 使用者確認 |
| 需求文件逐漸過時 | 保持需求-規格-實作一致性 |

### 1.3 核心價值

```
「需求文件是源頭，Feature 開發中的合理調整應回饋至需求，
確保 PRD 與 User Stories 始終反映最新的設計決策」
```

---

## 2. 使用時機

### 2.1 在流程中的位置

```
/speckit.specify → /speckit.plan → /flowkit.consistency-check
                                            │
                                            ▼
                 /speckit.tasks → /speckit.implement
                                            │
                                            ▼
                              /flowkit.code-check
                                            │
                                            ▼
                              /flowkit.pre-unify-check
                                            │
                                            ▼
                                   /flowkit.trace
                                            │
                                            ▼
                          /flowkit.requirement-sync ◄── 在此執行
                                            │
                                            ▼
                               /flowkit.unify-flow
```

### 2.2 與其他 FlowKit 指令的關係

| 指令 | 時機 | 關係 |
|------|------|------|
| `flowkit.consistency-check` | Plan 後 | 檢查 Plan 與 System 的一致性 |
| `flowkit.code-check` | Implement 後 | 程式碼品質驗證（Runtime 檢查） |
| `flowkit.pre-unify-check` | code-check 後 | 檢查 Spec 品質與實作對齊（步驟 10a） |
| `flowkit.trace` | pre-unify-check 後 | 建立 Spec-Code 追溯索引（步驟 10b） |
| `flowkit.requirement-sync` | trace 後 | 將 Feature 變更回寫至需求文件（**本指令**，步驟 10c） |
| `flowkit.unify-flow` | requirement-sync 後 | 合併 Feature 至 System（步驟 11） |

### 2.3 執行條件

| 條件 | 必要性 | 說明 |
|------|--------|------|
| Feature `spec.md` 存在 | REQUIRED | 需要 Feature Spec 作為比對來源 |
| Feature `plan.md` 存在 | RECOMMENDED | 用於理解變更意圖 |
| PRD-*.md 存在 | REQUIRED | 需求文件目標 |
| User Stories 目錄存在 | REQUIRED | 需求文件目標 |

---

## 3. 核心功能

### 3.1 變更偵測

比對 Feature Spec 與原始 PRD / User Stories 的差異：

| 比對項目 | 來源 | 目標 |
|----------|------|------|
| User Story 標題 | Feature spec.md | US-X-*.md |
| US 內容（As a / I want / So that） | Feature spec.md | US-X-*.md |
| Acceptance Criteria | Feature spec.md | US-X-*.md |
| 功能描述 | Feature spec.md | PRD-*.md |

### 3.2 意圖判斷

自動分類差異類型：

| 分類 | 判斷依據 | 處理方式 |
|------|----------|----------|
| **A. 刻意修正** | 有 `[MODIFIED]` 標記、Plan 有說明、Refine Delta 有記錄、Spec Delta Log 有對應 | 自動回寫 |
| **B. 澄清補充** | 內容更詳細但語意相同 | 建議回寫 |
| **C. 範圍裁切** | Feature 移除標記為「可選」的 AC/US、初版範圍裁剪、未實作但具未來價值 | 🔒 保留不動 |
| **D. 限縮合併** | Feature 收緊限制條件、合併多個 AC 為更嚴格的單一 AC | 🔒 保留原始 |
| **E. 非意圖不一致** | 無標記、無輔助信號、疑似遺漏 | 詢問使用者 |
| **F. 格式差異** | 僅格式不同 | 忽略 |

> 📌 **C/D 類保留原則**（v1.4.0 新增）：requirement-sync 的目的是「將本意修正寫回」。範圍裁切（暫不做 ≠ 永遠不做）與限縮合併（實作更嚴格 ≠ 需求應收窄）不屬於本意修正，原始需求應保留。

### 3.3 回寫同步

對確認的項目執行回寫：

| 變更類型 | 處理方式 |
|----------|----------|
| `[NEW]` US/AC | 在對應檔案中新增 |
| `[MODIFIED]` US/AC | 更新對應內容 |
| `[DELETED]` US/AC（永久移除） | 標記刪除或移除 |
| `[DELETED]` US/AC（範圍裁切） | 🔒 保留原始需求（未來 Milestone 候選） |
| 限制條件收緊 / AC 合併更嚴格 | 🔒 保留原始合理門檻 |
| 無標記但有差異 | 詢問後處理 |

---

## 4. 使用方式

### `--default` 模式

> 📝 詳細說明請參考 [功能說明-default-mode.md](./功能說明-default-mode.md)

```bash
# GitHub Copilot Agent 模式
@workspace /flowkit.requirement-sync --default

# 等同於
/flowkit.requirement-sync
```

### 4.1 CLI 風格

```bash
# 標準執行（互動模式）
/flowkit.requirement-sync

# 指定 Feature
/flowkit.requirement-sync --feature specs/features/001-xxx/

# 僅預覽，不修改
/flowkit.requirement-sync --dry-run

# 自動模式（刻意修正自動回寫）
/flowkit.requirement-sync --auto
```

### 4.2 自然語言

```
幫我同步需求文件
把 Feature 的變更回寫到 PRD
更新 User Stories 與 Feature 一致
檢查 Feature 與需求文件的差異
```

---

## 5. 執行流程

### Phase 0：前置條件檢查

```markdown
1. 確認 Feature 目錄存在（spec.md 必須）
2. 確認需求文件存在（PRD-*.md、User Stories）
3. 資料健康檢查
```

### Phase 1：建立對應關係

```markdown
1. 掃描 Feature Spec 結構（US IDs、AC IDs、變更標記）
2. 掃描需求文件結構（PRD 章節、US 檔案）
3. 建立 Feature US → 需求文件的對應表
```

### Phase 2：差異比對

```markdown
1. 對每個 MODIFIED 的 US 進行深讀比對
2. 比對 US 標題、內容、AC
3. 比對 PRD 中的功能描述
4. 記錄所有差異
```

### Phase 3：意圖判斷

```markdown
1. 根據變更標記、Plan 說明、Spec Delta Log 分類差異
2. 產生分類報告
3. 標記需要使用者確認的項目
```

### Phase 4：回寫執行

```markdown
1. 對「刻意修正」自動回寫
2. 對「非意圖不一致」詢問使用者
3. 執行 User Stories 和 PRD 的更新
4. 驗證回寫結果
```

### Phase 5：產生同步報告

```markdown
1. 統計回寫項目
2. 列出修改的檔案
3. 建議下一步操作
```

---

## 6. 輸出格式

### 6.1 同步報告結構

```markdown
## FlowKit Requirement Sync 報告

### 基本資訊
- **Feature**：001-feature-name
- **執行時間**：2026-01-26 10:30
- **執行模式**：標準

### 同步摘要

| 類別 | 數量 | 說明 |
|------|------|------|
| 刻意修正（已回寫） | 3 | 自動回寫完成 |
| 澄清補充（已回寫） | 1 | 經確認回寫 |
| 非意圖不一致（已處理） | 1 | 經使用者決策 |
| 格式差異（忽略） | 2 | 無需處理 |

### 修改的檔案

| 檔案 | 變更類型 | 變更項目 |
|------|----------|----------|
| docs/requirements/user-stories/US-A-xxx.md | 修改 | US-A-1 AC2 |
| docs/requirements/PRD-xxx.md | 修改 | 功能 A 描述 |

### 下一步建議
- [ ] 審閱修改的需求文件
- [ ] 執行 `/flowkit.unify-flow`
```

---

## 7. 錯誤處理

| 錯誤情境 | 嚴重性 | 處理方式 |
|----------|--------|----------|
| Feature spec.md 不存在 | CRITICAL | STOP，指出需要 spec.md |
| 需求文件目錄不存在 | CRITICAL | STOP，指出需要建立需求文件 |
| 無法建立對應關係 | HIGH | 警告，列出無法對應的項目 |
| 回寫時檔案唯讀 | HIGH | STOP，指出需要修改檔案權限 |

---

## 8. 部署位置

| 平台 | 檔案位置 |
|------|----------|
| GitHub Copilot Agent | `.github/agents/flowkit.requirement-sync.agent.md` |
| GitHub Copilot Prompt | `.github/prompts/flowkit.requirement-sync.prompt.md` |
| Cursor Command | `.cursor/commands/flowkit.requirement-sync.md` |

---

## 9. 版本歷史

| 版本 | 日期 | 說明 |
|------|------|------|
| 1.4.0 | 2026-02-13 | 新增「範圍裁切」與「限縮合併」分類（C/D 類保留原則），強化「需求保留原則」，優先檢測保留類型的判斷邏輯 |
| 1.3.0 | 2026-02-15 | 新增 spec-delta-log.md 為意圖判斷信號源（跨階段變更追蹤機制）|
| 1.2.0 | 2026-02-08 | 多信號源意圖判斷、流程圖補 code-check、階段性開發指引 |
| 1.0.0 | 2026-01-26 | 初版發布 |

---

## 10. 相關文件

- [FlowKit 功能說明總覽](./README.md)
- [功能說明-flowkit.pre-unify-check](./功能說明-flowkit.pre-unify-check.md)
- [功能說明-flowkit.unify-flow](./功能說明-flowkit.unify-flow.md)
- [SDD 開發流程圖](./SDD開發流程圖.md)
