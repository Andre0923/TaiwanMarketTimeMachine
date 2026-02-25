# PR Review Report — Feature {FEATURE_ID}

> **Feature**：{FEATURE_NAME}  
> **執行時間**：{TIMESTAMP}  
> **執行者**：AI（FlowKit PR Review v1.0.0）  
> **Git Branch**：{GIT_BRANCH}  
> **Git Commit**：{GIT_COMMIT}

---

## 審查結論

### 最終狀態：{STATUS}

> 🟢 READY FOR PR / 🟠 REVIEW WITH CAUTION / 🔴 NOT READY

**說明**：{STATUS_REASON}

---

## 審查統計

| 嚴重性 | 數量 | 詳見 |
|--------|------|------|
| 🔴 CRITICAL | {CRITICAL_COUNT} | §3.1 |
| 🟠 HIGH | {HIGH_COUNT} | §3.2 |
| 🟡 MEDIUM | {MEDIUM_COUNT} | §3.3 |
| 🟢 LOW | {LOW_COUNT} | §3.4 |

### 阻擋規則判定

```
CRITICAL: {CRITICAL_COUNT} → {CRITICAL_BLOCK}
HIGH:     {HIGH_COUNT}     → {HIGH_BLOCK}
MEDIUM:   {MEDIUM_COUNT}   → {MEDIUM_WARN}
LOW:      {LOW_COUNT}      → {LOW_ACTION}
```

---

## D1 — 變更摘要

### 變更檔案清單

| 類別 | 新增 | 修改 | 刪除 | 說明 |
|------|------|------|------|------|
| `src/` | {SRC_ADD} | {SRC_MOD} | {SRC_DEL} | {SRC_NOTE} |
| `tests/` | {TEST_ADD} | {TEST_MOD} | {TEST_DEL} | {TEST_NOTE} |
| `specs/` | {SPEC_ADD} | {SPEC_MOD} | {SPEC_DEL} | {SPEC_NOTE} |
| `docs/` | {DOC_ADD} | {DOC_MOD} | {DOC_DEL} | {DOC_NOTE} |
| 其他 | {OTHER_ADD} | {OTHER_MOD} | {OTHER_DEL} | {OTHER_NOTE} |

### Feature 動機

{FEATURE_MOTIVATION}

### User Story 覆蓋率

| US | 摘要 | AC 覆蓋 | 狀態 |
|----|------|---------|------|
| {US_ID} | {US_SUMMARY} | {AC_COVERAGE} | {US_STATUS} |

---

## D2 — 程式碼品質

### 檔案長度檢查（憲法 §8.1）

| 檔案 | 行數 | 狀態 | 建議 |
|------|------|------|------|
| {FILE} | {LINES} | {STATUS} | {SUGGESTION} |

### 函式複雜度（憲法 §8.3）

| 檔案 | 函式 | 行數 | 狀態 | 建議 |
|------|------|------|------|------|
| {FILE} | {FUNC} | {LINES} | {STATUS} | {SUGGESTION} |

### 命名一致性

| 項目 | 問題 | 嚴重性 | 建議 |
|------|------|--------|------|
| {ITEM} | {ISSUE} | {SEVERITY} | {SUGGESTION} |

### Docstring 覆蓋（憲法 §8.5）

| 檔案 | 模組級 | 類別級 | 函式級 | 狀態 |
|------|--------|--------|--------|------|
| {FILE} | {MOD_DOC} | {CLS_DOC} | {FUNC_DOC} | {STATUS} |

### Dead Code / 重複

| 類型 | 檔案 | 說明 | 嚴重性 |
|------|------|------|--------|
| {TYPE} | {FILE} | {DESC} | {SEVERITY} |

---

## D3 — 架構 & 設計

### 單一職責檢查（憲法 §8.2）

| 模組 | 責任描述 | 是否單一職責 | 建議 |
|------|----------|-------------|------|
| {MODULE} | {RESPONSIBILITY} | {STATUS} | {SUGGESTION} |

### 介面-邏輯分離（憲法 §7）

| 模組 | 分離狀態 | 說明 |
|------|----------|------|
| {MODULE} | {STATUS} | {NOTE} |

### 模組耦合度

| 模組 A | 模組 B | 耦合類型 | 嚴重性 | 建議 |
|--------|--------|----------|--------|------|
| {MOD_A} | {MOD_B} | {TYPE} | {SEVERITY} | {SUGGESTION} |

### 設計決策評估

| # | 決策 | 評估 | 建議 |
|---|------|------|------|
| {N} | {DECISION} | {ASSESSMENT} | {SUGGESTION} |

---

## D4 — 跨 Feature 影響

### System Spec 衝突檢查

| 檢查項 | 結果 | 說明 |
|--------|------|------|
| 行為定義衝突 | {STATUS} | {NOTE} |
| 資料模型影響 | {STATUS} | {NOTE} |
| API 相容性 | {STATUS} | {NOTE} |
| 流程定義影響 | {STATUS} | {NOTE} |

### 共用模組影響

| 共用模組 | 修改內容 | 影響範圍 | 嚴重性 |
|----------|----------|----------|--------|
| {MODULE} | {CHANGE} | {IMPACT} | {SEVERITY} |

---

## D5 — 安全性 & 敏感資料

### 敏感資料掃描

| 檔案 | 發現 | 嚴重性 | 建議 |
|------|------|--------|------|
| {FILE} | {FINDING} | {SEVERITY} | {SUGGESTION} |

### 輸入驗證

| 入口點 | 驗證狀態 | 嚴重性 | 建議 |
|--------|----------|--------|------|
| {ENTRY} | {STATUS} | {SEVERITY} | {SUGGESTION} |

### 依賴安全

| 依賴 | 版本 | 已知漏洞 | 嚴重性 |
|------|------|----------|--------|
| {DEP} | {VER} | {VULN} | {SEVERITY} |

---

## D6 — SDD 合規性

### 流程完整性

| 階段 | 狀態 | 產物 | 說明 |
|------|------|------|------|
| specify | {STATUS} | spec.md | {NOTE} |
| plan | {STATUS} | plan.md | {NOTE} |
| tasks | {STATUS} | tasks.md | {NOTE} |
| analyze | {STATUS} | 分析報告 | {NOTE} |
| implement | {STATUS} | src/ + tests/ | {NOTE} |
| code-check | {STATUS} | 驗證報告 | {NOTE} |

### Test-First 合規

| 檢查項 | 結果 | 說明 |
|--------|------|------|
| 測試先於程式碼 | {STATUS} | {NOTE} |
| AC 覆蓋率 | {STATUS} | {NOTE} |

### Traceability

| 檢查項 | 結果 | 說明 |
|--------|------|------|
| @spec 註解存在 | {STATUS} | {NOTE} |
| traceability-index.md | {STATUS} | {NOTE} |
| 殘留變更標記 | {STATUS} | {NOTE} |

---

## 品質總評（AI 決策）

### 整體品質等級：{QUALITY_GRADE}

> A（優秀） / B（良好） / C（可接受） / D（需改善） / F（需重新規劃）

### AI 決策摘要

{AI_DECISION_SUMMARY}

### 品質評估（若為 D/F 等級）

> ⚠️ 若 AI 判定品質低落至需要回溯至更早階段：

| 評估項 | 說明 |
|--------|------|
| 回溯建議 | {BACKTRACK_SUGGESTION} |
| 建議回到階段 | {SUGGESTED_PHASE} |
| 理由 | {BACKTRACK_REASON} |
| 修正策略 | {FIX_STRATEGY} |

---

## 審查發現彙整

### 🔴 CRITICAL Issues（MUST 修正）

| # | 面向 | 檔案 | 問題描述 | 修正建議 |
|---|------|------|----------|----------|
| {N} | {DIM} | {FILE} | {DESC} | {FIX} |

### 🟠 HIGH Issues（MUST 修正）

| # | 面向 | 檔案 | 問題描述 | 修正建議 |
|---|------|------|----------|----------|
| {N} | {DIM} | {FILE} | {DESC} | {FIX} |

### 🟡 MEDIUM Issues（SHOULD 修正，警告）

| # | 面向 | 檔案 | 問題描述 | 修正建議 |
|---|------|------|----------|----------|
| {N} | {DIM} | {FILE} | {DESC} | {FIX} |

### 🟢 LOW Issues（AI 自主判斷修正）

| # | 面向 | 檔案 | 問題描述 | 修正成本 | AI 決策 |
|---|------|------|----------|----------|---------|
| {N} | {DIM} | {FILE} | {DESC} | {COST} | {DECISION} |

---

## Escalation Log（深讀記錄）

| 階段 | 目標位置 | 深讀原因 | 讀取範圍 |
|------|----------|----------|----------|
| {PHASE} | {TARGET} | {REASON} | {RANGE} |

**總深讀次數**：{TOTAL_DEEP_READS}  
**最小 Context 完成率**：{MIN_CONTEXT_RATE}%

---

## DoD 檢查結果

### 必要條件

- [ ] D1 變更摘要完整
- [ ] D2 程式碼品質掃描完成
- [ ] D3 架構設計審查完成
- [ ] D4 跨 Feature 影響分析完成
- [ ] D5 安全性掃描完成
- [ ] D6 SDD 合規性檢查完成
- [ ] 審查報告已產出至 `.artifacts/pr-review-report-{FEATURE_ID}.md`
- [ ] PR Description 已產出至 `.artifacts/pr-description-{FEATURE_ID}.md`
- [ ] 阻擋規則已判定
- [ ] AI 品質決策已完成

### 禁止殘留

- [ ] 無未判定嚴重性的問題
- [ ] 無 CRITICAL / HIGH 被略過
- [ ] MEDIUM 問題已記錄警告

---

## 下一步

| 狀態 | 行動 |
|------|------|
| 🟢 READY | AI 自動修正 LOW（若成本合理）→ 執行 PR |
| 🟠 CAUTION | MEDIUM 已警告 → AI 交由 `refine-loop` 或人類決策 |
| 🔴 NOT READY | CRITICAL/HIGH 存在 → AI 自動進入 `refine-loop` 修正 |
| ⛔ REPLAN | 品質 D/F → AI 建議回到 `plan` 或更早階段 |

### 具體行動項

1. {ACTION_1}
2. {ACTION_2}
3. {ACTION_3}
