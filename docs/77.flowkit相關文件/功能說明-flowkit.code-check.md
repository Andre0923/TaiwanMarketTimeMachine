# FlowKit Code Check 功能說明

> **指令名稱**：`/flowkit.code-check`  
> **Agent 檔案**：`.github/agents/flowkit.code-check.agent.md`  
> **產物目錄**：`.artifacts/`（驗證報告與截圖）

---

## 1. 功能概述

### 1.1 這是什麼？

`/flowkit.code-check` 是一個 **AI 驅動的自動化驗證金字塔**，在 `implement` 完成後、`pre-unify-check` 之前執行。它透過五層逐級驗證（L0→L4）確認程式碼可正常運作，並產出結構化的驗證報告。

### 1.2 解決什麼問題？

| 問題 | 解決方式 |
|------|----------|
| Implement 後缺乏系統性驗證 | 五層金字塔自動執行 |
| 手動測試容易遺漏 | AI 自動涵蓋環境→編譯→測試→API→UI |
| 難以判斷回歸風險 | Feature 關鍵字 grep + 基線比對 |
| 驗證結果不可追溯 | 產出結構化報告至 `.artifacts/` |
| 工具不齊全時無法驗證 | 降級策略：跳過但不失敗 |

### 1.3 核心價值

```
「環境先查、編譯先過、測試不回歸、API 能回應、UI 能操作 — 五層金字塔，自動跑到底。」
```

---

## 2. 使用時機

### 2.1 何時使用 Code Check？

**適用情境**：
- Feature 所有 Phase 實作完成後
- 準備進入 Pre-Unify Check / Unify Flow 之前
- 重大修改或回歸修復後需要驗證

**不適用情境**：
- 實作進行中（先完成所有 tasks 再驗證）
- 想寫新測試（code-check 不寫測試，用 Test-First）
- 規格對齊檢查（用 `pre-unify-check`）
- 可追溯性驗證（用 `trace`）

### 2.2 在 SDD 流程中的位置

```
specify → plan → tasks → analyze → implement
                                       │
                                       ▼
                              ┌── code-check ──┐    ← 你在這裡
                              │                 │
                              │  L0 Gatekeeper  │
                              │  L1 Static      │
                              │  L2 Unit Tests  │
                              │  L3 Integration │
                              │  L4 E2E         │
                              │  L5 Report      │
                              │                 │
                              └────────┬────────┘
                                       │
                              ┌───────┴───────┐
                              │               │
                           ✅ PASS          ❌ FAIL
                              │               │
                              ▼               ▼
                      pre-unify-check   refine-loop
                              │               │
                              ▼               └──► implement
                          unify-flow            （重跑 code-check）
```

---

## 3. 驗證金字塔

### 3.1 金字塔結構

```
         ╱ L5: Manual Smoke ╲          ← 人類：Escalation Log
        ╱  L4: E2E (端對端)    ╲        ← AI：專案 E2E 測試 / 瀏覽器自動化
       ╱   L3: Integration     ╲       ← AI：API Smoke Test
      ╱    L2: Unit Tests       ╲      ← AI：測試 + 回歸分析
     ╱     L1: Static Analysis   ╲     ← AI：編譯 + 型別 + 語法
    ╱      L0: Gatekeeper         ╲    ← AI：環境 + 工具檢查
```

### 3.2 層級說明

| 層級 | 名稱 | 職責 | 失敗影響 |
|------|------|------|----------|
| L0 | Gatekeeper | 環境版本、工具可用性、Feature 偵測 | ❌ → STOP |
| L1 | Static Analysis | 編譯、型別、語法、lint | ❌ → STOP |
| L2 | Unit Tests + Regression | 測試通過 + 零 Feature 回歸 | ❤️ → STOP |
| L3 | Integration | API 端點 smoke test（含 port 檢查） | ❌ → 記錄，可 SKIP || L3.5 | Usability Gate | 啟動腳本可用性（U1）+ 首頁可及性（U2）+ 環境一致性（U3 WARNING）+ Zombie Port（U4 WARNING） | U1/U2 ❌ → FAIL；U3/U4 ⚠️ → WARNING || L4 | E2E | 端對端驗證（策略 A：專案 E2E 測試；策略 C：CDP 即時互動驗證；策略 B：Browser 工具） | ❌ → 記錄，可 SKIP |
| L5 | Manual Smoke | 人類處理 Escalation 項目 | 不影響自動判定 |

### 3.3 最終判定規則

| 條件 | 判定 | 後續行動 |
|------|------|----------|
| L0-L4 全 PASS（含 L3.5 PASS 或 SKIP） | ✅ PASS | 進入 pre-unify-check |
| L0-L2 PASS，L3/L3.5/L4 SKIP | 🟡 CONDITIONAL | 確認後可進入 |
| L3.5 FAIL（U1 或 U2 失敗） | ❌ FAIL | 進入 refine-loop 修復啟動路徑 |
| L0 或 L1 FAIL | ❌ FAIL | 進入 refine-loop 修復後重跑 code-check |

---

## 4. 輸入與輸出

### 4.1 輸入

| 來源 | 必要性 | 說明 |
|------|--------|------|
| `$ARGUMENTS` | OPTIONAL | Feature ID 或 `--default` |
| `src/` | REQUIRED | 程式碼（唯讀） |
| `tests/` | REQUIRED | 測試檔案 |
| `specs/features/NNN-*/` | OPTIONAL | Feature 關鍵字來源 |
| `package.json` / `pyproject.toml` | OPTIONAL | 技術棧偵測 |
| `.artifacts/test-failures-baseline.txt` | OPTIONAL | 回歸基線 |

### 4.2 輸出

| 產出 | 位置 | 說明 |
|------|------|------|
| 驗證報告 | `.artifacts/code-check-report-feature-<NNN>.md` | 完整結構化報告 |
| Bug-Fix 清單 | `.artifacts/bug-fix-list-feature-<NNN>.md` | 非功能回歸 bug-fix 清單（若有） |
| UI 截圖（L4） | `.artifacts/v4-ui-*.png` | E2E 驗證截圖 |
| 測試基線 | `.artifacts/test-failures-baseline.txt` | 回歸基線（通過後更新） |
| 測試耗時記錄 | `.artifacts/test-durations.json` | 各測試耗時（conftest.py 自動產生，供慢測試識別） |

---

## 5. 使用方式

### 5.1 指令範例

```
# 全自動模式（推薦）
/flowkit.code-check --default

# 指定 Feature
/flowkit.code-check 011

# 跳過 E2E（無 Web UI）
/flowkit.code-check 011 --skip-e2e

# 僅靜態分析 + 測試
/flowkit.code-check --layers L0,L1,L2
```

### 5.2 --default 模式

不需手動輸入任何參數，AI 自動：
1. 從 git branch 擷取 Feature ID
2. 從 spec 擷取 Feature 關鍵字
3. 偵測技術棧和可用工具
4. 執行所有可用層級

---

## 6. 工具需求

### 6.1 必要工具

| 工具 | 說明 |
|------|------|
| Terminal | VS Code 內建，永遠可用 |
| File System | VS Code 內建，永遠可用 |

### 6.2 增強工具（建議專案級配置）

| 工具 | 影響層級 | 降級策略 |
|------|----------|----------|
| Pylance MCP | L1 靜態分析 | 改用 `ast.parse()` 基本語法檢查 |
| Browser 工具 | L4 E2E（策略 B） | 降級至策略 C（CDP）或跳過 L4 + 記錄 Escalation |
| CDP 端點 | L4 E2E（策略 C） | Electron: `--remote-debugging-port=9222`；Web: Chrome DevTools MCP；不可用則降級至策略 B |

> **設計原則**：工具應在專案中**預先配置**，而非在驗證流程中安裝。
> 驗證流程中不安裝任何新依賴，確保「驗證環境 = 執行環境」。

---

## 7. 回歸分析機制

### 7.1 三步法

1. **基線載入**：讀取上次通過的失敗清單
2. **失敗比對**：本次失敗 vs 基線，找出新增項目
3. **Feature 關鍵字 grep**：新增失敗是否匹配 Feature 相關關鍵字

### 7.2 判定邏輯

```
新增失敗數 == 0              → 零回歸 ✅
新增失敗但不匹配 Feature 關鍵字 → 🟡 CONDITIONAL → 進入 §7.4 非功能回歸分流
新增失敗且匹配 Feature 關鍵字   → Feature 回歸 ❌
```

### 7.3 Flake Detection

新增失敗項目在判定 FAIL 前，會執行一次 rerun：
- 第二次通過 → flake suspicion，CONDITIONAL + Escalation
- 第二次仍失敗 → 照原判定遏輯

### 7.4 非功能回歸分流（Bug-Fix Triage）

當出現「新增失敗但不匹配 Feature 關鍵字」時，自動分類與分流：

1. **失敗分類**：依根因歸類為 FIXTURE-POLLUTION / TEST-DATA / API-CHANGE / ENV-TOOL
2. **成本評估**：EASY（≤20行單檔）/ MEDIUM（2-5檔≤50行）/ HIGH（>5檔或需架構調整）
3. **分流決策**：
   - 不需改 spec + 成本 ≤ MEDIUM → 加入 bug-fix 清單，交由 refine-loop 立即修復
   - 需改 spec 或 HIGH 成本 → 登記為 TD
4. **產出**：`.artifacts/bug-fix-list-feature-<NNN>.md`

> 此機制確保 EASY/MEDIUM 的純 bug-fix 問題不會累積成 TD，而是在當下自動修復。

---

## 8. Escalation Log

AI 無法自動處理的項目會記錄在驗證報告的 Escalation Log 中：

| 等級 | 意義 | 行動 |
|------|------|------|
| 🔴 HIGH | 阻斷性問題 | MUST 立即處理 |
| 🟡 LOW | 非功能性疑疵 | E2 BUGFIX Triage 分流（見下方） |
| 🔵 DEFERRED | 需人工/跨平台驗證 | E2 BUGFIX Triage 分流：成本 ≤ MEDIUM → BUGFIX；其餘 → TD |

### 8.1 E2 BUGFIX Triage（v1.10.0 擴充）

Phase 5 產出報告前，code-check 會對所有 🟡 LOW 和 🔵 DEFERRED 項目執行 BUGFIX Triage：

| 評估條件 | 分流結果 |
|----------|----------|
| 不需改 spec + 成本 EASY/MEDIUM | **BUGFIX** → 加入 `bug-fix-list-feature-NNN.md` |
| 需改 spec 或成本 HIGH | **DEFERRED** → 登記 TD |

BUGFIX 項目透過 `refine-loop --default` 的 Bug-Fix 模式在當前 Feature 閉環修復，不累積為技術債。

> 此機制與 §2.5 非功能回歸分流互補：§2.5 處理 L2 非功能測試失敗，E2 BUGFIX Triage 處理所有層級的 🟡 LOW 和 🔵 DEFERRED 項目。

---

## 9. 相關指令

| 指令 | 關係 | 說明 |
|------|------|------|
| `refine-loop` | 後置（FAIL 時） | FAIL 時進入 refine-loop 修復，修復後重跑 code-check |
| `pre-unify-check` | 後置 | PASS 後進入規格對齊檢查 |
| `unify-flow` | 最終 | 規格合併至 System Spec |
| `trace` | 後置 | 可追溯性驗證（與 code-check 互補） |

---

## 10. 與其他驗證指令的差異

| 面向 | code-check | pre-unify-check | trace |
|------|------------|-----------------|-------|
| 驗證目標 | 程式碼能跑 | Spec 品質對齊 | 可追溯性 |
| 執行方式 | 跑指令、看結果 | 讀 Spec、比對 | 讀文件、交叉比對 |
| 產物 | 驗證報告 + 截圖 | 品質報告 | 追溯矩陣 |
| 阻斷條件 | 編譯/測試失敗 | Spec 不完整 | 缺少追溯連結 |

---

## 版本歷史

| 版本 | 日期 | 說明 |
|------|------|------|
| v1.13.0 | 2026-04-02 | 移除 pytest-xdist 並行測試機制：改為單次串行執行、移除 serial 標記、簡化 L2 測試執行策略；新增 L4 Skip Quality Analysis + allowed-skips.md 白名單；L2 Lint Baseline；L3.5 用字修正 |
| v1.12.0 | 2026-04-01 | L3.5 Usability Gate（Issue #19）：新增第六層驗證—啟動腳本可用性（U1）、首頁可及性（U2）、環境一致性（U3 WARNING）、Zombie Process 債測（U4 WARNING）；U1/U2 FAIL 阻斷 L4；新增 `--skip-usability` 旗標；第四個進入條件新增 L3.5 SKIP 記錄 |
| v1.11.0 | 2026-03-02 | L4 策略 C （CDP 即時互動驗證）（Issue #17）：Flask/Web 應用透過 Chrome DevTools MCP 進行 CDP 連線、首頁驗證、截圖存檔；策略優先順序 A → C → B → SKIP |
| v1.10.0 | 2026-03-01 | E2 BUGFIX Triage 擴充：將 🔵 DEFERRED 項目納入 Triage 評估範圍，成本 ≤ MEDIUM 且不需改 spec 則分流為 BUGFIX（Issue #13） |
| v1.9.0 | 2026-02-27 | Phase 5 新增 E2 BUGFIX Triage：所有層級的 🟡 LOW 項目統一分流（BUGFIX → bug-fix-list / DEFERRED → TD），TD 登記排除 BUGFIX 項目，報告範本新增分流結果區段（Issue #7） |
| v1.8.0 | 2026-02-16 | 非功能回歸分流（Bug-Fix Triage） |
| v1.7.0 | 2026-02-15 | 慢測試閾值調整為 30 秒 |
| v1.6.0 | 2026-02-15 | 慢測試自動標記：conftest.py 根據歷史耗時自動標記 @pytest.mark.slow、implement 指令新增測試標記指引 |
| v1.5.0 | 2026-02-15 | L2 慢測試分批：@pytest.mark.slow 慢測試識別、conftest.py 慢測試候選自動偵測 |
| v1.2.0 | 2026-02-08 | 報告命名統一：`verify-report-feature-*` → `code-check-report-feature-*` |
| v1.1.0 | 2026-02-03 | 唯讀描述精確化、回歸缺口補強（CONDITIONAL）、Flake Detection、Port 檢查 |
| v1.0.0 | 2025-01-21 | 初始版本：五層驗證金字塔、降級策略、回歸分析 |