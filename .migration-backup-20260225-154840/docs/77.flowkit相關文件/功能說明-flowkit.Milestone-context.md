# 功能說明：flowkit.Milestone-context

> **FlowKit 套件文件**  
> **版本**：1.3.0  
> **最後更新**：2026-02-01

---

## 概述

`flowkit.Milestone-context` 是 FlowKit 套件中用於**擷取設計上下文**的指令化工具。它能從 PRD（產品需求文件）或其他指定文件中，擷取與目標 Milestone 相關的設計資訊，並檢測與現有 System 設計的潛在衝突。

---

## 使用場景

### 最佳使用時機

1. **Milestone 建立後**：在 BDD-Milestone 建立後，擷取 PRD 中預先設想的設計決策
2. **Plan 階段前**：在開始規劃 Feature 前，確保 AI 擁有完整設計脈絡
3. **衝突排查**：懷疑 PRD 設計與現有 System 不一致時

### 典型工作流程

```
PRD 撰寫完成
     ↓
執行 /flowkit.BDD-Milestone --init 建立 User Stories
     ↓                       🟡 僅首次 / PRD 變更時
執行 /flowkit.BDD-Milestone --milestone 規劃 Milestone
     ↓                       ← 每次 Feature 開發
執行 /flowkit.Milestone-context ← 本工具
     ↓
輸出至 docs/requirements/Milestone/MNN-context.md
     ↓
執行 /speckit.plan 開始規劃
```

---

## 核心功能

### 1. 設計上下文擷取

從 PRD 或指定文件中，針對目標 Milestone 的 User Story 擷取相關設計：

| 擷取類別 | 說明 | 對應 System 檔案 |
|----------|------|------------------|
| **DM** (Data Model) | 資料庫結構、Schema | `data-model.md` |
| **FL** (Flow) | 流程設計、狀態轉換 | `flows.md` |
| **CT** (Contract) | API 規格、介面契約 | `contracts/*.md` |
| **CF** (Config) | 設定檔規格 | `spec.md` |
| **UI** (UI Spec) | 畫面設計、元件規格 | `ui/*.md` |
| **TN** (Tech Note) | 技術備註、風險 | 無對應 |

### 2. 衝突檢測

自動比對擷取內容與 `specs/system/` 現有設計，發現不一致：

| 衝突類型 | 嚴重性 | 範例 |
|----------|--------|------|
| 結構衝突 | HIGH | 欄位名稱/型別不一致 |
| 語意衝突 | HIGH | 相同名稱但定義不同 |
| 約束衝突 | MEDIUM | 驗證規則不一致 |
| UI 衝突 | MEDIUM | 畫面設計不一致 |
| 擴展衝突 | LOW | PRD 新增功能與 System 類似 |

### 3. 衝突解決建議

衝突報告會提供兩種解決方案供人類決策：

- **方案 A**：按 PRD 設計，在新 Feature 中實作，後續透過 Unify Flow 更新 System
- **方案 B**：修改 PRD 文件，參照目前 System 已完成的設計

---

## 使用方式

### CLI 風格

```bash
# 基本用法（使用最新 Milestone，強制輸出至檔案）
/flowkit.Milestone-context

# 指定 Milestone
/flowkit.Milestone-context --milestone M01

# 自訂 PRD 路徑
/flowkit.Milestone-context --prd docs/requirements/PRD-MyProject.md

# 附加參考文件
/flowkit.Milestone-context --include api-spec.md,db-design.md

# 跳過衝突檢測
/flowkit.Milestone-context --skip-conflict

# 僅輸出至對話（除錯用，不建立檔案）
/flowkit.Milestone-context --output chat
```

### 自然語言

```
幫我擷取 M01 的相關設計
從 PRD 取出資料庫設計
把資料庫結構帶入 Plan
檢查 M02 跟現有設計有沒有衝突
參考這份文件規劃 [附檔]
```

---

## 輸出格式

### Milestone Context 文件

結構化的設計上下文，包含：

1. **Milestone 概要**：目標 Milestone 與包含的 User Story
2. **擷取摘要**：各類別的擷取統計
3. **詳細擷取內容**：依類別分組，標註來源
4. **衝突檢測結果**：若有衝突則包含報告

### 衝突報告

當發現衝突時，額外產生包含：

1. **衝突項目清單**：依嚴重性排序
2. **差異比對**：PRD vs System 的具體差異
3. **解決建議**：方案 A 與方案 B 的優缺點

---

## 與其他 FlowKit 工具的關係

| 工具 | 關係 | 說明 |
|------|------|------|
| `flowkit.BDD-Milestone` | 前置 | 先建立 User Stories (首次) 與 Milestone (每次)，再擷取上下文 |
| `speckit.plan` | 後續 | 擷取後開始規劃 Feature |
| `flowkit.consistency-check` | 互補 | 可用於進一步驗證一致性 |
| `flowkit.unify-flow` | 後續 | 解決衝突後執行 Unify |

---

## 核心概念

### System vs Milestone vs PRD

```
┌─────────────────────────────────────────────────────────────┐
│  specs/system/  = 已完成並通過驗證的系統設計（真相來源）      │
│  Milestone      = 預計未來要開發的 Feature                  │
│  PRD            = 產品需求文件（可能包含尚未實作的設計）       │
└─────────────────────────────────────────────────────────────┘
```

### 衝突處理原則

1. **AI 不主動修改**：衝突僅產生報告，由人類決策
2. **READ-ONLY**：本工具不修改 `specs/system/**`
3. **擴展非衝突**：System 沒有的新增定義不算衝突

---

## 部署位置

| 平台 | 位置 | 格式 |
|------|------|------|
| GitHub Copilot | `.github/agents/flowkit.Milestone-context.agent.md` | YAML frontmatter |
| Cursor | `.cursor/commands/flowkit.Milestone-context.md` | 純 Markdown |

### 範本位置

| 範本 | 位置 |
|------|------|
| 輸出範本 | `.flowkit/templates/Milestone-context-output.template.md` |
| 衝突報告範本 | `.flowkit/templates/Milestone-context-conflict-report.template.md` |

---

## 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 1.3.0 | 2026-02-01 | 預設輸出模式改為強制輸出至檔案（`file`），確保 SpecKit 後續階段可讀取 |
| 1.2.0 | 2026-01-26 | 輸出位置調整至 `docs/requirements/Milestone/MNN-context.md`，避免在 specify 前建立 feature 目錄 |
| 1.1.0 | 2025-01-21 | 新增 UI 規格比對支援、修正衝突檢測邏輯、重命名為 Milestone-context |
| 1.0.0 | 2025-01-20 | 初始版本 |

---

## 相關文件

- [SpecKit Plan 階段指南](../01.開發人員doc/03.SDD開發流程指南.md)
- [FlowKit BDD-Milestone 功能說明](./功能說明-flowkit.BDD-Milestone.md)
- [FlowKit Unify Flow 功能說明](./功能說明-flowkit.unify-flow.md)
