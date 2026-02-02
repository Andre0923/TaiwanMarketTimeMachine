# Constitution Sync Impact Report

> **用途**：記錄 Constitution 每次修訂的影響範圍與同步狀態  
> **維護者**：speckit.constitution.agent  
> **更新時機**：每次 Constitution 更新後自動產生

---

## 報告格式

每次 Constitution 更新後，MUST 在此文件頂部新增一筆報告記錄。

---

## 報告範本

```markdown
### [日期] v[舊版本] → v[新版本]

**版本變更類型**：MAJOR / MINOR / PATCH

**變更原因**：
- [簡述本次修訂的主要原因]

#### 條款變更

| 類型 | 條款 | 說明 |
|------|------|------|
| ➕ 新增 | §X.X | [新增條款名稱] |
| ✏️ 修改 | §X.X | [舊名稱] → [新名稱] 或 [變更內容摘要] |
| ➖ 移除 | §X.X | [移除條款名稱] |

#### 依賴文件同步狀態

| 文件 | 狀態 | 備註 |
|------|------|------|
| `.specify/templates/plan-template.md` | ✅ 已同步 / ⚠️ 待更新 | [需調整項目] |
| `.specify/templates/spec-template.md` | ✅ 已同步 / ⚠️ 待更新 | [需調整項目] |
| `.specify/templates/tasks-template.md` | ✅ 已同步 / ⚠️ 待更新 | [需調整項目] |
| `README.md` | ✅ 已同步 / ⚠️ 待更新 | [需調整項目] |

#### 待辦事項

- [ ] [TODO 項目描述]

#### 建議 Commit 訊息

```
docs: amend constitution to vX.Y.Z ([變更摘要])
```

---
```

---

## 歷史記錄

### 2026-01-21 v0.x（草案） → v1.0.0

**版本變更類型**：MAJOR（首次正式版本）

**變更原因**：
- 將草案整理為正式版本
- 重新編排條款順序，提升邏輯一致性
- 精簡 Unify Flow 章節，細節移至獨立 prompt 文件
- 統一術語與格式

#### 條款變更

| 類型 | 條款 | 說明 |
|------|------|------|
| ✏️ 重編 | §1.1 | SDD 核心架構 → 合併 SDD 方法論與架構說明 |
| ✏️ 重編 | §1.2 | 目錄結構獨立成專條 |
| ✏️ 重編 | §1.3 | System Spec 層精簡 |
| ✏️ 重編 | §3.1 | Test-First 合併 §3.2.1 目錄規範 |
| ✏️ 重編 | §3.2 | Observability 合併日誌規範 |
| ✏️ 重編 | §3.6 | UI 行為治理（原 §3.7） |
| ✏️ 精簡 | §6.2 | Feature 合併限制（原 Unify Flow），細節移至 `unify-flow.prompt.md` |


#### 結構變更

| 舊結構 | 新結構 | 說明 |
|--------|--------|------|
| §1.1 SDD 核心架構 | §1.1 SDD 方法論 | 合併方法論說明 |
| §3.1 SDD + 驗收標準 | §1.1 整合 | 避免重複 |
| §3.7 UI 行為治理 | §3.6 UI 行為治理 | 編號調整 |
| §6.2 Unify Flow（完整） | §6.2 Feature 合併限制 | 精簡化 |


#### 依賴文件同步狀態

| 文件 | 狀態 | 備註 |
|------|------|------|
| `.specify/templates/plan-template.md` | ⚠️ 待評估 | Constitution Check 條款編號需對應 |
| `.specify/templates/spec-template.md` | ⚠️ 待評估 | 無直接影響，建議確認 |
| `.specify/templates/tasks-template.md` | ⚠️ 待評估 | 無直接影響，建議確認 |
| `unify-flow.prompt.md` | ✅ 獨立維護 | 已與 §6.2 解耦 |

#### 待辦事項

- [ ] 實際專案套用時，確認 plan-template.md 的 Constitution Check 引用正確
- [ ] 確認 speckit.analyze.agent.md 檢查邏輯與新編號對應

#### 建議 Commit 訊息

```
docs: 發布 Constitution 簡化版 v1.0.0 (結構重整 + Unify Flow 解耦)
```

---

## 維護指南

### 版本號規則（Semantic Versioning）

| 類型 | 說明 | 範例 |
|------|------|------|
| **MAJOR** | 不相容的治理/原則移除或重新定義 | v1.0.0 → v2.0.0 |
| **MINOR** | 新增原則/章節或實質擴充指引 | v1.0.0 → v1.1.0 |
| **PATCH** | 澄清、措辭、錯字修正、非語意調整 | v1.0.0 → v1.0.1 |

### 報告產生流程

1. Constitution 更新完成後
2. 在本文件頂部（歷史記錄區段）新增報告
3. 填寫所有變更項目與同步狀態
4. 若有待辦事項，記錄於報告中
5. 執行 Git 提交（包含 Constitution + 本報告）
