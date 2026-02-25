# FlowKit 版本歷史

> 本文件統一記錄所有 FlowKit Agent 的版本變更歷史，以減少指令化檔案的 token 使用量

---

## flowkit.BDD-Milestone

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.5.0 | 2025-07-12 | --milestone 模式新增 Tech Debt 納入建議：讀取 technical-debt.md，篩選 Open + Milestone-Candidate，產出 `[OPTIONAL] Tech Debt 納入建議` 區段，使用 US-TD-N 命名格式 |
| 1.4.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.3.0 | 2026-01-22 | 恢復 requirements 資料夾路徑結構 |
| 1.2.0 | 2026-01-22 | 更名為 FlowKit BDD-Milestone Builder，調整輸出路徑結構 |
| 1.1.0 | 2026-01-22 | 新增自然語言支援、Group 指定、輸出結構驗證 |
| 1.0.0 | 2026-01-22 | 初始版本，整合 BDD User Story Builder |

---

## flowkit.Milestone-context

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式，自動選擇最高編號 Milestone |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

## flowkit.system-context

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

## flowkit.consistency-check

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-02-14 | Phase 0 新增 Bugfix/Tech Debt 類型判斷；Phase 3 A 類新增 Change Set 排除規則（適用所有 Feature 類型）；Phase 3 C 類新增條件式模式過濾（UI 任務在 L0 場景降級為 INFO） |
| 1.0.1 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-23 | 初始版本，從 pre-unify-check 重新設計，聚焦非意圖性錯誤 |

---

## flowkit.pre-unify-check

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.2.0 | 2026-02-15 | 新增 §3.5 Spec Delta Log 交叉比對：利用 implement_baseline_commit 執行 git diff，交叉比對 spec-delta-log.md，偵測未追蹤的 spec 變更（提案 #3 實施） |
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-23 | 重新設計，聚焦 Spec 品質和最終攔截，移除與 consistency-check 重複的部分 |

---

## flowkit.trace

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-25 | 初始版本，支援 User Story + AC 層級追溯 |

---

## flowkit.refine-loop

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.5.0 | 2026-02-16 | Bug-Fix 模式：`--default` 模式新增 `.artifacts/bug-fix-list-feature-*.md` 優先讀取；Phase 0 新增 bug-fix 清單偵測，自動切換 Bug-Fix 模式（Classification=BUGFIX、Impact 限 code+tests、Scope 放寬）；支援 code-check 非功能回歸自動分流 |
| 1.4.0 | 2026-02-08 | 報告命名統一：`verify-report-feature-*` → `code-check-report-feature-*`，消除 agent 串接 glob 混淆 |
| 1.3.0 | 2026-02-03 | Handoff 重構（移除 trace、新增 code-check + pre-unify-check）、--default 模式支援 code-check 報告、Phase 0 整合 code-check 報告、Scope 檔案數門檻、Next Steps 修正、Phase 7 步驟編號修正 |
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

## flowkit.requirement-sync

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.4.0 | 2026-02-13 | 新增「C. 範圍裁切」與「D. 限縮合併」分類（六分類體系 A~F）；新增「需求保留原則」核心原則；Phase 3.2 判斷邏輯重構為 Step 1（保留類型優先檢測）+ Step 2（標準判斷流程）；Phase 4.1 新增 C/D 類自動保留流程；AI MUST NOT 強化刪除保護規則；DoD 新增 C/D 類保留驗證 |
| 1.3.0 | 2026-02-15 | Phase 0.1 新增 spec-delta-log.md 為輔助信號源；Phase 3.2 判斷邏輯新增 spec-delta-log.md 比對（提案 #3 實施） |
| 1.2.0 | 2026-02-08 | 多信號源意圖判斷：Phase 0.1 新增輔助信號源掃描（plan.md、refine-spec-delta.md）；Phase 3.1/3.2 增強判斷邏輯支援 refine-delta 變更記錄；新增階段性開發注意事項 |
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

## flowkit.unify-flow

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.4.0 | 2026-02-25 | Phase 4 新增 Step 0：封存前自動將 Feature Status 更新為 `Unified`（YAML frontmatter + inline 標記），確保歷史記錄反映最終狀態（Issue #4 實施） |
| 1.3.0 | 2026-02-15 | 新增 Phase 7 TD Reconciliation：Feature 完成時自動比對 TD Ref 標註與 Open TD，提議結案並更新 TD Registry（直接解決 + 附帶解決），含 MUST ASK 人類確認 |
| 1.2.0 | 2026-02-15 | 新增 Phase 6.5 Feature Summary 自動產生：將 Feature 開發經驗萃取為結構化摘要（品質指標、關鍵決策、學習點），儲存至 .flowkit/memory/learning/feature-summaries/（提案 #6A 實施） |
| 1.1.0 | 2026-02-01 | 新增 `--default` 模式支援 |
| 1.0.0 | 2026-01-XX | 初始版本 |

---

## flowkit.code-check

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.8.0 | 2026-02-16 | 非功能回歸分流（Bug-Fix Triage）：§2.5 新增四步法分類分流機制（FIXTURE-POLLUTION/TEST-DATA/API-CHANGE/ENV-TOOL）、成本評估（EASY/MEDIUM→refine-loop、HIGH→TD）、自動產出 `.artifacts/bug-fix-list-feature-*.md`、新增 Bug-Fix handoff 至 refine-loop；pytest-xdist 改為自動安裝 + 安裝失敗降級串行（取代不降級策略） |
| 1.7.0 | 2026-02-15 | pytest-xdist 未安裝改為自動安裝（不降級）、慢測試閾值調整為 30 秒（原 10 秒） |
| 1.6.0 | 2026-02-15 | 慢測試自動標記 + serial 標記：conftest.py `pytest_collection_modifyitems` 根據 `test-durations.json` 歷史耗時自動標記 `@pytest.mark.slow`、新增 `@pytest.mark.serial` 不可並行測試標記、分批策略更新為 `not slow and not serial` / `slow or serial`、pytest-xdist 加入範本必備依賴 |
| 1.5.0 | 2026-02-15 | L2 並行執行 + 慢測試分批：pytest-xdist (`-n auto`) 並行快速測試、`@pytest.mark.slow` 慢測試串行執行、conftest.py 慢測試候選自動偵測（>{SLOW_THRESHOLD_SECONDS}s） |
| 1.4.0 | 2025-07-12 | 新增 Tech Debt 自動登記：E2 LOW → P3 code-quality、E3 DEFERRED → P2 test-regression，含 Dedup-Key 去重機制 |
| 1.3.0 | 2026-02-11 | L4 E2E 策略分流：新增「策略 A — 專案定義的 E2E 測試」（優先，適用 Electron/Playwright），保留「策略 B — 瀏覽器自動化」作為 fallback |
| 1.2.0 | 2026-02-08 | 報告命名統一：輸出檔名 `verify-report-feature-*` → `code-check-report-feature-*`，消除檔名與內容標題的命名不一致 |
| 1.1.0 | 2026-02-03 | 唯讀描述精確化（允許 .artifacts/ 寫入）、回歸缺口補強（新失敗不匹配關鍵字 → CONDITIONAL）、Flake Detection（rerun once）、L3 Port 檢查防禦 |
| 1.0.0 | 2025-01-21 | 初始版本：五層驗證金字塔（L0-L4）、降級策略、回歸分析、結構化報告 |

---

## flowkit.pr-review

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.3.0 | 2026-02-15 | 新增 Phase 7.6 TD Closure Verification：PR Review 時驗證 TD 結案一致性（正向：TD Ref 未結案 → WARNING；反向：PR 修改 TD Component 但未結案 → INFO） |
| 1.2.0 | 2025-07-12 | §7.5 Tech Debt 登錄 Enhanced Schema：新增 Type/Source/Component/Milestone-Candidate/Feature-Origin/Last-Detected/Detection-Count/Dedup-Key/Evidence-Ref 欄位 + 去重機制 |
| 1.1.0 | 2026-02-12 | Phase 0.4 PR Tool Readiness（gh CLI 安裝/授權檢查 + 自動安裝引導）、Phase 7.5 Tech Debt 明確登錄流程（寫入 docs/technical-debt.md）、Phase 8.4 三層 PR 建立策略（Strategy A/B/C） |
| 1.0.0 | 2026-02-11 | 初始版本：六維品質審查、品質評級（A-F）、自動 PR 建立、AI 自主決策機制 |

---

## flowkit.system-health

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.0.0 | 2025-07-12 | 初始版本：五維度全專案健康檢查（D1~D5）、Quick/Full 模式、Hard Fail + 加權評分、基線機制、TD 自動登記（含 Dedup-Key 去重）、老化偵測 |

---

## 功能說明文件

### default-mode

| 版本 | 日期 | 變更說明 |
|------|------|----------|
| 1.1.0 | 2026-02-01 | 新增 Smart Defaults（specify/Milestone-context 特殊行為） |
| 1.0.0 | 2026-02-01 | 初始版本，所有指令支援 `--default` 模式 |

---

> **備註**：版本歷史詳細內容請參考此統一文件，各 Agent 檔案中不再保留版本歷史區塊