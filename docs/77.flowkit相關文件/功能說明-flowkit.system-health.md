# FlowKit System Health 功能說明

> **指令名稱**：`/flowkit.system-health`  
> **Agent 檔案**：`.github/agents/flowkit.system-health.agent.md`  
> **產物目錄**：`.artifacts/`（健康報告與基線）

---

## 🎯 30 秒快速指南

**一句話摘要**：system-health 就像「專案的健康檢查報告」— 你跑一次，它告訴你專案整體品質如何、哪裡有問題、什麼該優先修。

```
最常見的三種用法：

1. 快速看一下專案有沒有問題？
   → /flowkit.system-health
   （3~5 分鐘，不跑測試，掃程式碼 + 技術債 + 依賴）

2. Milestone 規劃前全面體檢？
   → /flowkit.system-health --full --auto-register-td
   （含跑測試 + 自動把發現的問題登記到技術債清單）

3. 只想看某個面向？
   → /flowkit.system-health --dimensions D4
   （只看技術債狀態）
```

> 💡 **system-health 是唯讀的**：它只看、只報告，不會改你的程式碼。唯一會寫入的是 `.artifacts/` 報告檔和 `docs/technical-debt.md`（僅在啟用 `--auto-register-td` 時）。

---

## 1. 功能概述

### 1.1 這是什麼？

`/flowkit.system-health` 是一個 **AI 驅動的全專案健康檢查工具**。

用白話說：它會從五個角度（測試、規格覆蓋、程式碼品質、技術債、依賴安全）掃描你的整個專案，然後產出一份結構化的評分報告（A~F 等級），讓你一目了然地知道「專案現在健不健康、哪裡需要優先改善」。

### 1.2 它跟其他工具有什麼不同？

| 我想做的事 | 該用什麼 | 為什麼不是 system-health？ |
|------------|----------|---------------------------|
| 驗證「這個 Feature」的程式碼品質 | `code-check` | code-check 只看單一 Feature |
| 審查 PR 品質，準備提交 | `pr-review` | pr-review 聚焦 PR 變更範圍 |
| 檢查規格是否對齊 | `pre-unify-check` | pre-unify-check 看 Feature vs System 一致性 |
| 了解「整個專案」的健康趨勢 | ✅ **system-health** | 這才是全專案視角的健康檢查 |
| 修復 Bug / 優化程式碼 | `refine-loop` | system-health 是唯讀的，不改程式碼 |

### 1.3 解決什麼問題？

| 問題 | 解決方式 |
|------|----------|
| TD 只在 Feature 層級被動發現 | 全專案主動五維度診斷 |
| 缺乏專案健康趨勢追蹤 | 基線比對 + 歷史趨勢 |
| TD 散落各處無統一治理 | 自動登記至 Technical Debt Registry + 去重 |
| Milestone 規劃缺乏品質輸入 | 健康報告 → BDD-Milestone 規劃參考 |
| 關鍵問題可能被忽略 | Hard Fail 機制（安全、測試惡化、P1 堆積） |
| TD 老化無人追蹤 | 自動偵測 + 升級建議 |

---

## 2. 使用時機 — 何時該跑 system-health？

### 2.1 典型情境對照

> 不確定該不該用？看看下面的情境，找到最接近你現在狀況的那一項。

| # | 你的情境 | 建議動作 | 說明 |
|---|----------|----------|------|
| 1 | 🗓️ 準備規劃下一個 Milestone | `--full --auto-register-td` | **最重要的使用時機**。全面體檢 + 自動登記問題，讓 BDD-Milestone 能讀取 TD 建議 |
| 2 | ✅ 剛完成一輪 Unify Flow | `--default` | 快速確認合併後整體品質沒退步 |
| 3 | ⚠️ code-check 連續出現 E3 DEFERRED | `--default` 或 `--dimensions D4` | 看看全專案的技術債是否累積過多 |
| 4 | 📅 固定週期（每月 / 每 2~3 個 Milestone） | `--full --auto-register-td` | 定期健檢，追蹤趨勢 |
| 5 | 🏗️ 重大技術決策前（重構、換框架） | `--full` | 評估現有技術債風險，作為決策依據 |
| 6 | 🔒 擔心依賴安全性 | `--dimensions D5` | 只掃依賴健康度（過期套件 + 安全漏洞） |
| 7 | 🐛 團隊覺得「專案品質變差了」 | `--full --update-baseline` | 全面檢查 + 建立新基線，作為改善起點 |

### 2.2 什麼時候「不需要」用 system-health？

- **正在開發 Feature 中** → 用 `code-check` + `refine-loop` 就夠了
- **準備提交 PR** → 用 `pr-review`
- **想修改程式碼** → system-health 是唯讀的，用 `refine-loop`
- **只是想檢查 Feature 與 System Spec 是否一致** → 用 `pre-unify-check`

### 2.3 在 SDD 流程中的位置

system-health 是 **Advisory（諮詢性質）** 的工具，不會阻斷任何開發流程。它獨立於主流程之外，通常在「開始新 Milestone 前」或「階段性結束後」使用：

```
    ┌─────────────────────────────────────────────────┐
    │  /flowkit.system-health（Advisory，隨時可執行）  │
    │  → 產出健康報告 + 自動登記 TD                    │
    └──────────────────────┬──────────────────────────┘
                           │ TD 建議
                           ▼
    PRD → BDD-Milestone ←──┘（讀取 TD 建議規劃 Milestone）
                │
                ▼
       specify → plan → tasks → analyze → implement
                                              │
                                              ▼
                              code-check → pre-unify → unify → pr-review
```

---

## 3. 核心功能

### 3.1 五維度診斷 — 它到底看什麼？

system-health 從五個角度（稱為「維度」D1~D5）檢查你的專案：

| 維度 | 名稱 | 白話說明 | Quick 模式 | Full 模式 |
|------|------|----------|------------|-----------|
| D1 | 測試健康度 | 跑測試看通過率，跟上次比有沒有變差 | — | ✅ |
| D2 | 規格覆蓋度 | 你寫的 AC 有多少有對應的測試？ | — | ✅ |
| D3 | 程式碼品質 | Lint 警告、型別錯誤、檔案是否太長 | ✅ | ✅ |
| D4 | 技術債 | TD 總數、老化天數、P1 是否堆積 | ✅ | ✅ |
| D5 | 依賴健康度 | 套件是否過期、有無安全漏洞 | ✅ | ✅ |

> **Quick vs Full 差在哪？**  
> Quick（預設）只跑 D3+D4+D5，約 3~5 分鐘，適合日常快看。  
> Full 額外跑 D1+D2（需要執行測試套件），比較完整但需要更多時間。

### 3.2 評分機制

**Step 1 — Hard Fail 檢查**（優先判定，任一命中即為 F 級）：

| Hard Fail 條件 | 觸發等級 |
|----------------|----------|
| 發現 Critical 安全漏洞 | → 直接 F |
| 測試通過率比基線惡化 > 20% | → 直接 F |
| Build 失敗 | → 直接 F |
| P1 技術債 ≥ 3 項未排程 | → 直接 F |

**Step 2 — 加權評分**（無 Hard Fail 時）：

| 維度 | 權重 |
|------|------|
| D1 測試健康度 | 30% |
| D2 規格覆蓋度 | 20% |
| D3 程式碼品質 | 20% |
| D4 技術債 | 15% |
| D5 依賴健康度 | 15% |

**等級對照**：A ≥ 90 ∣ B ≥ 75 ∣ C ≥ 60 ∣ D ≥ 40 ∣ F < 40

### 3.3 TD 自動登記

啟用 `--auto-register-td` 後，system-health 會：
1. 將發現的問題自動寫入 `docs/technical-debt.md`
2. 自動去重（Dedup-Key 比對），相同問題不會重複登記
3. 新項目自動指定 Priority（依嚴重程度映射）
4. 格式依循 Enhanced Schema（已在 `docs/technical-debt.md` 定義）

### 3.4 基線機制

基線 = 「上次完整檢查的分數快照」，用來追蹤趨勢（改善 or 惡化）。

- **建立基線**：首次以 `--full` 或 `--update-baseline` 執行即自動建立
- **趨勢比對**：後續每次執行都會跟基線比較，報告中標示 ↑ 改善 / ↓ 惡化
- **更新基線**：使用 `--update-baseline`，需人工確認後才更新

---

## 4. 使用方式

### 4.1 指令格式

```
/flowkit.system-health [參數]
```

### 4.2 參數總覽

| 參數 | 說明 | 範例 |
|------|------|------|
| `--default` 或不帶參數 | Quick 模式（D3+D4+D5），最快 | `/flowkit.system-health` |
| `--full` | Full 模式（D1~D5，含跑測試） | `/flowkit.system-health --full` |
| `--dimensions D1,D4` | 僅執行指定維度（可任意組合） | `/flowkit.system-health --dimensions D3,D5` |
| `--auto-register-td` | 自動把發現的問題登記到 TD | `/flowkit.system-health --auto-register-td` |
| `--update-baseline` | Full + 建立/更新基線快照 | `/flowkit.system-health --update-baseline` |

> 💡 參數可以組合使用，例如 `--full --auto-register-td` 同時啟用。

### 4.3 參數怎麼選？決策指南

不確定該用哪個參數組合？照這個流程走：

```
你的目的是什麼？
│
├─ 「快速看一下有沒有大問題」
│   → /flowkit.system-health
│   （Quick 模式，3~5 分鐘）
│
├─ 「準備規劃 Milestone，要全面了解現況」
│   → /flowkit.system-health --full --auto-register-td
│   （Full + 自動登記，最完整）
│
├─ 「我想建立基線 / 更新基線」
│   → /flowkit.system-health --update-baseline
│   （含 Full 檢查 + 更新基線快照）
│
├─ 「只想看特定面向」
│   ├─ 技術債狀態 → --dimensions D4
│   ├─ 依賴安全性 → --dimensions D5
│   ├─ 程式碼品質 → --dimensions D3
│   └─ 測試 + 覆蓋 → --dimensions D1,D2
│
└─ 「我想修程式碼」
    → ❌ 不是 system-health 的用途
    → 用 refine-loop 或 code-check
```

### 4.4 常見組合速查

| 場景 | 建議指令 | 耗時 | 說明 |
|------|----------|------|------|
| 日常快速檢查 | `--default` | 3~5 min | 不跑測試，看 D3+D4+D5 |
| Milestone 前全面檢查 | `--full --auto-register-td` | 5~15 min | 含測試 + 自動登記問題 |
| 建立/更新基線 | `--update-baseline` | 5~15 min | Full + 建立趨勢追蹤起點 |
| 只看技術債 | `--dimensions D4` | 1~2 min | 快速看 TD 老化狀態 |
| 只看安全性 | `--dimensions D5` | 1~2 min | 套件安全漏洞掃描 |
| Unify 後快速確認 | `--default` | 3~5 min | 確認合併沒搞壞什麼 |

---

## 5. 輸出格式

### 5.1 報告位置

- 報告：`.artifacts/system-health-report-YYYY-MM-DD.md`
- 基線：`.artifacts/system-health-baseline.md`
- 模板：`.flowkit/templates/system-health-report.template.md`

### 5.2 報告結構

```markdown
# System Health Report

> 整體評級：{GRADE}（{SCORE}/100）
> Hard Fail：{YES/NO}
> 趨勢：{TREND} vs 基線

## Hard Fail 檢查
## 評分明細（各維度加權分）
## D1~D5 各維度詳細結果
## 建議行動（優先級排序）
## TD 自動登記結果（若啟用）
## 歷史趨勢
## Escalation Log
## DoD 檢查結果
```

---

## 6. 與其他工具的關係

### 6.1 system-health 在生態系中的角色

```
         ┌─ code-check     → Feature 層級程式碼驗證
         │
         ├─ pr-review      → PR 層級品質審查
「品質」 ─┤
         ├─ system-health  → 全專案層級健康檢查 ← 你在這裡
         │
         └─ refine-loop    → 修復問題的循環
```

| 比較項目 | code-check | pr-review | system-health |
|----------|------------|-----------|---------------|
| **視角** | 單一 Feature | PR 變更範圍 | 整個專案 |
| **觸發時機** | implement 完成後 | unify-flow 後 | Milestone 前 / 定期 |
| **是否 Gate** | ✅ PASS/FAIL | ✅ READY/NOT READY | ❌ Advisory |
| **會改程式碼** | 否 | 否（產 PR） | 否 |
| **會寫 TD** | ✅ E3 DEFERRED | ✅ LOW 放行 | ✅ 自動登記 |

### 6.2 TD 治理閉環 — 問題從哪來、到哪去

```
問題來源：                       統一登記處：
┌─ code-check E3 DEFERRED ──→ ┐
│                              │
├─ pr-review LOW 放行 ────────→ ├─→ docs/technical-debt.md
│                              │
└─ system-health --auto-td ──→ ┘
                                        │
                                        ▼
                              BDD-Milestone --milestone
                              （讀取 TD 建議 → 規劃 US-TD-N）
                                        │
                                        ▼
                                Feature 開發 → 解決 TD
```

---

## 7. 重要限制

| 限制 | 說明 |
|------|------|
| **Advisory 性質** | 不產出 PASS/FAIL gate，不阻斷任何開發流程 |
| **唯讀原則** | 不修改 `src/`、`specs/`、`tests/`。僅寫入 `.artifacts/` 和 `docs/technical-debt.md`（限 `--auto-register-td`） |
| **老化偵測僅建議** | 在報告中標記建議，不自動修改 TD Priority |
| **改善行動由人決定** | 報告列出建議，但實際要不要修由人類判斷 |
| **Quick 模式不跑測試** | D1/D2 只在 Full 模式下執行，Quick 模式會跳過 |

---

## 8. 版本歷史

| 版本 | 日期 | 說明 |
|------|------|------|
| 1.0.0 | 2025-07-12 | 初版：五維度診斷 + Quick/Full 模式 + TD 自動登記 + 基線機制 |
