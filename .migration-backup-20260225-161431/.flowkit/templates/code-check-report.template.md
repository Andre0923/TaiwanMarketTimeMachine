# Code Check Report — Feature {FEATURE_ID}

> **Feature**：{FEATURE_NAME}  
> **執行時間**：{TIMESTAMP}  
> **執行者**：AI（FlowKit Code Check v1.0.0）  
> **Git Branch**：{GIT_BRANCH}  
> **Git Commit**：{GIT_COMMIT}

---

## 驗證結論

### 最終判定：{VERDICT}

> ✅ PASS / 🟡 CONDITIONAL / ❌ FAIL

**說明**：{VERDICT_REASON}

---

## 驗證金字塔結果

| 層級 | 階段 | 結果 | 耗時 | 說明 |
|------|------|------|------|------|
| L0 | Gatekeeper | {L0_RESULT} | {L0_TIME} | {L0_NOTE} |
| L1 | Static Analysis | {L1_RESULT} | {L1_TIME} | {L1_NOTE} |
| L2 | Unit Tests + Regression | {L2_RESULT} | {L2_TIME} | {L2_NOTE} |
| L3 | Integration | {L3_RESULT} | {L3_TIME} | {L3_NOTE} |
| L4 | E2E | {L4_RESULT} | {L4_TIME} | {L4_NOTE} |

> 結果標記：✅ PASS / ❌ FAIL / ⏭️ SKIP（含原因）

---

## L0 — Gatekeeper 詳細結果

### 專案類型偵測

| 偵測項 | 結果 |
|--------|------|
| 主要語言 | {PRIMARY_LANG} |
| 框架 | {FRAMEWORKS} |
| 測試框架 | {TEST_FRAMEWORK} |
| 服務類型 | {SERVICE_TYPE} |

### 環境版本

| 工具 | 版本 | 狀態 |
|------|------|------|
| {TOOL_1} | {VERSION_1} | ✅/❌ |
| {TOOL_2} | {VERSION_2} | ✅/❌ |

### 工具可用性

| 工具 | 可用 | 影響層級 | 降級策略 |
|------|------|----------|----------|
| Pylance MCP | {YES/NO} | L1 | {DEGRADATION_NOTE} |
| Browser 工具 | {YES/NO} | L4 | {DEGRADATION_NOTE} |

### Feature 偵測

| 項目 | 值 |
|------|-----|
| Feature ID | {FEATURE_ID} |
| 來源 | {FEATURE_SOURCE}（git branch / 參數 / spec） |
| 關鍵字 | {KEYWORDS} |
| Spec 路徑 | {SPEC_PATH} |

---

## L1 — Static Analysis 詳細結果

### 編譯 / Build

| 項目 | 指令 | 結果 | 說明 |
|------|------|------|------|
| {BUILD_ITEM_1} | {BUILD_CMD_1} | ✅/❌ | {BUILD_NOTE_1} |

### 型別檢查

| 項目 | 結果 | 錯誤數 | 說明 |
|------|------|--------|------|
| {TYPE_CHECK_1} | ✅/❌ | {ERROR_COUNT} | {TYPE_NOTE_1} |

### Lint（若適用）

| 項目 | 結果 | Warnings | 說明 |
|------|------|----------|------|
| {LINT_1} | ✅/⚠️ | {WARNING_COUNT} | {LINT_NOTE_1} |

---

## L2 — Unit Tests + Regression 詳細結果

### 測試執行

| 指標 | 數值 |
|------|------|
| 測試總數 | {TOTAL_TESTS} |
| 通過 | {PASSED} |
| 失敗 | {FAILED} |
| 跳過 | {SKIPPED} |
| 執行時間 | {TEST_DURATION} |

### 回歸分析

| 步驟 | 結果 | 說明 |
|------|------|------|
| 基線載入 | {BASELINE_STATUS} | {BASELINE_NOTE} |
| 失敗清單比對 | {FAILURE_DIFF} | {DIFF_NOTE} |
| Feature 關鍵字 grep | {KEYWORD_MATCH} | {KEYWORD_NOTE} |

#### 新增失敗項（若有）

| # | 測試名稱 | 匹配 Feature 關鍵字 |
|---|----------|---------------------|
| {N} | {TEST_NAME} | {MATCHED_KEYWORD} |

---

## L3 — Integration 詳細結果

### 服務啟動

| 服務 | 啟動方式 | 狀態 | 說明 |
|------|----------|------|------|
| {SERVICE_1} | {START_CMD_1} | ✅/❌ | {SERVICE_NOTE_1} |

### 端點驗證

| 端點 | 方法 | 預期 | 實際 | 結果 |
|------|------|------|------|------|
| {ENDPOINT_1} | {METHOD_1} | {EXPECTED_1} | {ACTUAL_1} | ✅/❌ |

### 服務清理

| 服務 | 清理方式 | 結果 |
|------|----------|------|
| {SERVICE_1} | {CLEANUP_CMD_1} | ✅/❌ |

---

## L4 — E2E 詳細結果

### 頁面載入

| 頁面 | URL | 載入結果 | 截圖 |
|------|-----|----------|------|
| {PAGE_1} | {URL_1} | ✅/❌ | `.artifacts/{SCREENSHOT_1}` |

### UI 元素驗證

| 元素 | 存在 | 可互動 | 說明 |
|------|------|--------|------|
| {ELEMENT_1} | ✅/❌ | ✅/❌ | {ELEMENT_NOTE_1} |

### 互動流程

| # | 流程描述 | 結果 | 截圖 |
|---|----------|------|------|
| {N} | {FLOW_DESC} | ✅/❌ | `.artifacts/{SCREENSHOT_N}` |

### Console 訊息

| 類型 | 數量 | 說明 |
|------|------|------|
| Errors（功能性） | {FUNC_ERRORS} | {ERROR_NOTE} |
| Errors（裝飾性） | {DECO_ERRORS} | {DECO_NOTE} |
| Warnings | {WARNINGS} | {WARN_NOTE} |

---

## Escalation Log

| # | 等級 | 項目 | 說明 | 建議行動 |
|---|------|------|------|----------|
| E{N} | 🔴/🟡/🔵 | {ITEM} | {DESCRIPTION} | {ACTION} |

> 等級：🔴 HIGH（阻斷）/ 🟡 LOW（下次迭代）/ 🔵 DEFERRED（人工/跨平台）

---

## DoD 檢查結果

### 必要條件

- [ ] L0 Gatekeeper PASS
- [ ] L1 Static Analysis PASS（或 SKIP with reason）
- [ ] L2 Unit Tests PASS（零 Feature 回歸）
- [ ] L3 Integration PASS（或 SKIP with reason）
- [ ] L4 E2E PASS（或 SKIP with reason）
- [ ] 驗證報告已產出至 `.artifacts/code-check-report-feature-{FEATURE_ID}.md`
- [ ] 所有啟動的服務已關閉
- [ ] Escalation Log 已記錄需人類處理的項目
- [ ] 最終判定已明確（PASS / CONDITIONAL / FAIL）

### 禁止殘留

- [ ] 無未關閉的背景服務
- [ ] 無修改過的 src/ 或 specs/ 檔案
- [ ] 無遺漏的驗證層級（除明確 SKIP 外）

---

## 下一步建議

| 判定 | 建議行動 |
|------|----------|
| ✅ PASS | 進入 `/flowkit.pre-unify-check` → `/flowkit.unify-flow` |
| 🟡 CONDITIONAL | 確認 Escalation Log 後決定：進入 Unify 或先修復 |
| ❌ FAIL | 回到 implement 或執行 `/flowkit.refine-loop` 修復 |

### 具體行動項

1. {ACTION_1}
2. {ACTION_2}
3. {ACTION_3}
