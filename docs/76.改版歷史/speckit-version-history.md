# SpecKit 版本歷史

> 本文件統一記錄所有 SpecKit 指令與範本的版本變更歷史，以減少指令化檔案的 token 使用量

---

## 指令版本歷史

### speckit.specify

| 版本 | 日期 | 變更說明 |
|------|------|----------|| 1.3.0 | 2026-02-15 | 新增 TD Ref 標註（步驟 5.5/4.5）：specify 階段讀取 Open TD 並在相關 US 標註 `> TD Ref: TD-XXX`（SHOULD） || 1.2.0 | 2026-02-14 | 改進 Feature 編號邏輯：納入 `specs/history/` 計算（unify-flow 完成的 Feature）、搜尋所有 Feature 編號（全域唯一）而非僅匹配 short-name、移除 Bash 範例（PowerShell-only） |
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式，自動偵測最新 Milestone |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

### speckit.clarify

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.2.0 | 2026-02-15 | 新增 §8.5/§7.5 Spec 修訂標記自動注入（Auto-Marking）：clarify 修改 US/AC 後自動加上 [MODIFIED]/[NEW]/[DELETED]；新增 §8.6/§7.6 Spec Delta Log 規格差異日誌機制（提案 #3 實施） |
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

### speckit.plan

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

### speckit.tasks

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

### speckit.analyze

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.5.0 | 2026-02-27 | §7 Next Actions 以修正成本取代嚴重度作為分流準則；新增 Quick-Fix Triage 三級成本評估（Quick-Fix / Moderate / Heavy）；§6 報告結構新增 Quick-Fix List 區塊，匯總修正成本低的 LOW/MEDIUM findings（Issue #8） |
| 1.4.0 | 2026-02-14 | F 通道新增遞進精鍊感知規則（Progressive Refinement Awareness）；G 通道新增 L0 Maturity 降級機制（L0 場景 G1/G5/G6 降級）；E 通道新增 Affected Files 容差規則（間接影響檔案降級） |
| 1.3.0 | 2026-02-09 | §9.5/§8.5 從「提醒使用者」升級為「AI 自動注入標記」：Remediation 修改 US/AC 時自動加上 [MODIFIED]/[NEW]/[DELETED]（提案 #1 實施） |
| 1.2.0 | 2026-02-08 | 新增 Spec 修訂標記提醒（§9.5/§8.5）：Remediation 修改 US/AC 後提醒使用者加上 [MODIFIED]/[NEW]/[DELETED] 標記 |
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

### speckit.implement

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.5.0 | 2026-02-25 | Feature Status 自動管理（Issue #4）：新增 §1.6 開始實作時設定 `In Progress`；Step 11/9 完成後設定 `Implemented`；MUST NOT 規則新增元資料例外（status, implement_baseline_commit, updated）|
| 1.4.0 | 2026-02-15 | 測試標記指引更新：慢測試閾值調整為 30 秒（原 10 秒） |
| 1.3.0 | 2026-02-15 | 新增 §7.5/§6.5 測試標記指引（Test Markers）：Python pytest 專案 MUST 根據準則標記 `@pytest.mark.slow`（耗時）和 `@pytest.mark.serial`（不可並行），含判斷準則、範例、自動標記說明 |
| 1.2.0 | 2026-02-15 | 新增 §1.5 Git Hash 基線記錄（implement_baseline_commit）供 pre-unify-check git diff 比對；新增 §10.5/§8.5 Spec Delta Log 規格差異日誌（MUST）：實作中發現規格差異必須記錄（提案 #3 實施） |
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

### speckit.checklist

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

### speckit.constitution

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

### speckit.taskstoissues

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

## 範本版本歷史

### spec-template.md

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-01-XX | 新增 UI/UX 影響評估區塊、YAML frontmatter |
| 1.0.0 | 2026-01-XX | 初始版本 |

**位置**：`.specify/templates/spec-template.md`

---

### plan-template.md

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-01-XX | 新增 UI/UX Plan 區塊、Constitution Compliance Check |
| 1.0.0 | 2026-01-XX | 初始版本 |

**位置**：`.specify/templates/plan-template.md`

---

### tasks-template.md

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-01-XX | 新增 Traceability 說明、測試產物路徑提醒 |
| 1.0.0 | 2026-01-XX | 初始版本 |

**位置**：`.specify/templates/tasks-template.md`

---

### checklist-template.md

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.0.0 | 2026-01-XX | 初始版本 |

**位置**：`.specify/templates/checklist-template.md`

---

### agent-file-template.md

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.0.0 | 2026-01-XX | 初始版本 |

**位置**：`.specify/templates/agent-file-template.md`

---

## 版本命名規範

| 版本類型 | 說明 | 範例 |
|----------|------|------|
| Major (X.0.0) | 重大變更、不相容的修改 | 流程架構變更 |
| Minor (1.X.0) | 新功能、向後相容的修改 | 新增 `--default` 模式 |
| Patch (1.0.X) | Bug 修復、微調 | 修正錯字、調整描述 |

---

> **備註**：版本歷史詳細內容請參考此統一文件，各指令檔案中不再保留版本歷史區塊
