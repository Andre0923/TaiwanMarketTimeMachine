# System Health Report — {PROJECT_NAME}

> **執行日期**：{DATE}  
> **執行模式**：{MODE}（Quick / Full / Custom）  
> **執行者**：AI（FlowKit System Health v1.0.0）  
> **專案技術棧**：{TECH_STACK}  
> **Git Branch**：{GIT_BRANCH}  
> **Git Commit**：{GIT_COMMIT}

---

## 整體評級

### {GRADE}（{SCORE}/100）

> 評級標準：A ≥ 90 | B ≥ 75 | C ≥ 60 | D ≥ 40 | F < 40 或 Hard Fail

**Hard Fail**：{HARD_FAIL_STATUS}  
**趨勢**：{TREND} vs 基線（{BASELINE_DATE}）

---

## Hard Fail 檢查

| 檢查項 | 結果 | 說明 |
|--------|------|------|
| D5 Critical 安全漏洞 | {RESULT} | {NOTE} |
| D1 測試惡化 > 20%（vs 基線） | {RESULT} | {NOTE} |
| Build 可執行 | {RESULT} | {NOTE} |
| P1 TD ≥ 3 未排程 | {RESULT} | {NOTE} |

---

## 評分明細

| 維度 | 分數 | 權重 | 加權分 | vs 基線 |
|------|------|------|--------|---------|
| D1: 測試健康度 | {D1_SCORE} | 30% | {D1_WEIGHTED} | {D1_TREND} |
| D2: 規格覆蓋度 | {D2_SCORE} | 20% | {D2_WEIGHTED} | {D2_TREND} |
| D3: 程式碼品質 | {D3_SCORE} | 20% | {D3_WEIGHTED} | {D3_TREND} |
| D4: Tech Debt | {D4_SCORE} | 15% | {D4_WEIGHTED} | {D4_TREND} |
| D5: 依賴健康度 | {D5_SCORE} | 15% | {D5_WEIGHTED} | {D5_TREND} |

> 未執行的維度標記為 `N/A`（Quick 模式下 D1、D2 不執行）

---

## D1: 測試健康度

> 僅 Full 模式或指定 D1 時執行

- **總測試數**：{TOTAL_TESTS}
- **通過**：{PASSED} | **失敗**：{FAILED} | **跳過**：{SKIPPED}
- **通過率（排除 skip）**：{PASS_RATE}%
- **vs 基線**：{DELTA_PASS_RATE}

### 失敗分析

| 類別 | 數量 | 說明 |
|------|------|------|
| 新增失敗 | {NEW_FAILURES} | 基線中不存在的失敗 |
| 已知失敗 | {KNOWN_FAILURES} | 基線中已記錄（skip / expected-fail） |
| 恢復的測試 | {RECOVERED} | 基線中失敗但現在通過 |

### 失敗詳情

| 測試路徑 | 錯誤摘要 | 分類 | TD Ref |
|----------|----------|------|--------|
| {TEST_PATH} | {ERROR_SUMMARY} | {CATEGORY} | {TD_REF} |

---

## D2: 規格覆蓋度

> 僅 Full 模式或指定 D2 時執行

- **總 AC 數**：{TOTAL_AC}
- **有對應測試的 AC**：{COVERED_AC}
- **無測試的 AC**：{UNCOVERED_AC}
- **AC 覆蓋率**：{AC_COVERAGE}%

### 未覆蓋 AC 清單

| Feature | AC ID | AC 標題 | 說明 |
|---------|-------|---------|------|
| {FEATURE} | {AC_ID} | {AC_TITLE} | {NOTE} |

---

## D3: 程式碼品質

- **Lint 警告數**：{LINT_WARNINGS}
- **Lint 錯誤數**：{LINT_ERRORS}
- **型別錯誤數**：{TYPE_ERRORS}
- **超長檔案數（>800 行）**：{LONG_FILES}
- **嚴重超長檔案（>1000 行）**：{CRITICAL_LONG_FILES}

### Lint 問題摘要

| 規則 | 數量 | 嚴重性 | 說明 |
|------|------|--------|------|
| {RULE} | {COUNT} | {SEVERITY} | {DESCRIPTION} |

### 超長檔案

| 檔案路徑 | 行數 | 狀態 | 建議 |
|----------|------|------|------|
| {FILE_PATH} | {LINES} | ⚠️/❌ | {SUGGESTION} |

---

## D4: Tech Debt 狀態

- **Open**：{OPEN_TD}
- **In Progress**：{IN_PROGRESS_TD}
- **Resolved**：{RESOLVED_TD}
- **Won't Fix**：{WONT_FIX_TD}
- **TD 密度**：{TD_DENSITY}（Open / Component）
- **P1 未排程**：{P1_UNSCHEDULED}

### 老化偵測

| TD ID | 標題 | Priority | 未處理 Milestone 數 | 建議 |
|-------|------|----------|---------------------|------|
| {TD_ID} | {TITLE} | {PRIORITY} | {MILESTONE_AGE} | {RECOMMENDATION} |

---

## D5: 依賴健康度

- **過期依賴數**：{OUTDATED_DEPS}
- **Critical 安全漏洞**：{CRITICAL_VULNS}
- **High 安全漏洞**：{HIGH_VULNS}
- **Medium 安全漏洞**：{MEDIUM_VULNS}

### 安全漏洞詳情

| 套件 | 版本 | 漏洞 | 嚴重性 | 建議版本 |
|------|------|------|--------|----------|
| {PACKAGE} | {VERSION} | {VULN_ID} | {SEVERITY} | {FIX_VERSION} |

### 過期依賴

| 套件 | 當前版本 | 最新版本 | 過期程度 |
|------|----------|----------|----------|
| {PACKAGE} | {CURRENT} | {LATEST} | {AGE} |

---

## 建議行動

| 優先級 | 行動 | 維度 | 自動登記至 TD? |
|--------|------|------|----------------|
| {PRIORITY} | {ACTION} | {DIMENSION} | {AUTO_TD} |

---

## 歷史趨勢

| 日期 | 模式 | 評級 | 分數 | 主要變化 |
|------|------|------|------|----------|
| {DATE} | {MODE} | {GRADE} | {SCORE} | {CHANGE_NOTE} |

---

## Escalation Log（深讀記錄）

| 階段 | 目標位置 | 深讀原因 | 讀取範圍 |
|------|----------|----------|----------|
| {PHASE} | {TARGET} | {REASON} | {RANGE} |

**總深讀次數**：{DEEP_READ_COUNT}  
**最小 Context 完成率**：{CONTEXT_RATE}%

---

## DoD 檢查結果

- [ ] 所有指定維度已執行
- [ ] Hard Fail 判定已執行
- [ ] 加權評分已計算
- [ ] 報告已產出
- [ ] TD 自動登記已完成（若啟用）
- [ ] 基線更新已處理（若啟用）

---

## 下一步

- [ ] {NEXT_ACTION_1}
- [ ] {NEXT_ACTION_2}
- [ ] {NEXT_ACTION_3}
