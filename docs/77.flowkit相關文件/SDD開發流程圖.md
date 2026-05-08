# SDD 開發流程圖

> **最後更新**：2026-02-16  
> **用途**：SpecKit + FlowKit 整體開發流程視覺化（Mermaid 版本）

---

## 流程總覽表

| 階段 | 步驟 | 指令 | 輸入 | 輸出 | 備註 |
|------|------|------|------|------|------|
| **需求規劃** | 1a | `flowkit.BDD-Milestone` | PRD | User Stories | 🟡 僅首次 / PRD 變更時 |
| | 1b | `flowkit.BDD-Milestone` | User Stories | Milestone | 每次 Feature 開發 |
| | 2 | `flowkit.Milestone-context` | PRD, Milestone, System | 設計上下文, 衝突報告 | 抽取相關內容 + 衝突檢測 |
| **規格定義** | 3 | `speckit.specify` | Milestone | Feature Spec, 新分支 | 建立 Feature 規格 |
| | 4 | `speckit.clarify` | Spec | 釐清後 Spec | 🟡 選擇性 |
| | 5 | `flowkit.system-context` | System | 已實作上下文 | **建議必要**🟡 首個 Feature 略過  |
| | 6 | `speckit.plan` | Spec, 上下文 | Plan | 制定實作計畫 |
| | 7 | `flowkit.consistency-check` | Plan, System | 檢查報告 | 確認覆用、不重做、整合建議 🟡 首個 Feature 略過  |
| **任務拆解** | 8a | `speckit.tasks` | Plan | Tasks | 拆解可驗收任務 |
| | 8b | `speckit.analyze` | Tasks, 程式碼 | 分析報告 | 確認 Feature 內一致性 |
| **實作** | 9 | `speckit.implement` | Tasks | 程式碼, 測試 | 實作程式碼 |
| | 9.5 | `flowkit.code-check` | 程式碼, 測試 | 驗證報告, Bug-Fix 清單 | AI 五層驗證金字塔 + 非功能回歸分流 |
| | 9' | `flowkit.refine-loop` | 修正需求 / Bug-Fix 清單 | 更新 Spec/Code | 🔄 循環：code-check FAIL 或 Bug-Fix 時使用 |
| **驗證合併** | 10a | `flowkit.pre-unify-check` | 實作結果 | 檢查報告 | 確認可安全合併 |
| | 10b | `flowkit.trace` | Spec, Code | 追溯索引 | 建立規格-程式碼對照 |
| | 10c | `flowkit.requirement-sync` | Feature, PRD, US | 更新需求文件 | 回寫變更至 PRD / User Stories |
| | 11 | `flowkit.unify-flow` | Feature | System 更新, TD 結案 | 合併至 System Spec + TD Reconciliation |
| **PR 提交** | 12 | `flowkit.pr-review` | 全部產出 | PR Review 報告, PR | 六維品質審查 + TD 驗證 + 自動 PR |
| **全專案健康** | — | `flowkit.system-health` | 全專案 | 健康報告, TD 登記 | 🟡 Advisory，隨時可執行（建議 Milestone 前） |

---

## 完整開發流程圖

```mermaid
flowchart TB
    subgraph Phase1["📋 Phase 1：需求規劃"]
        PRD[("PRD-*.md<br/>產品需求文件")]
        BDD["1️⃣ flowkit.BDD-Milestone<br/>拆解 User Stories + Milestone"]
        MC1["2️⃣ flowkit.Milestone-context<br/>抽取 PRD 上下文 + 衝突檢測"]
        
        PRD --> BDD
        BDD --> US[("User Stories<br/>+ Milestone")]
        US --> MC1
        MC1 --> MC1_Check{與 System<br/>有衝突？}
        MC1_Check -->|是| MC1_Resolve["決策處理<br/>（修改 PRD / System / 記錄例外）"]
        MC1_Check -->|否| SPEC_START
        MC1_Resolve --> SPEC_START
    end

    subgraph Phase2["📝 Phase 2：規格定義"]
        SPEC_START((" "))
        SPEC["3️⃣ speckit.specify<br/>建立 Feature Spec + 新分支"]
        CLARIFY["4️⃣ speckit.clarify<br/>釐清規格（選擇性）"]
        SC["5️⃣ flowkit.system-context<br/>建立專案上下文（建議必要）"]
        
        PLAN["6️⃣ speckit.plan<br/>制定實作計畫"]
        CC["7️⃣ flowkit.consistency-check<br/>檢查覆用、不重做、整合建議"]
        
        SPEC_START --> SPEC
        SPEC --> CLARIFY
        CLARIFY -.->|選擇性| SC
        SPEC --> SC
        SC --> PLAN
        PLAN --> CC
        CC --> CC_Check{規劃合理？}
        CC_Check -->|有問題| CC_Fix["修正 Plan"]
        CC_Check -->|通過| TASKS
        CC_Fix --> PLAN
    end

    subgraph Phase3["📋 Phase 3：任務拆解"]
        TASKS["8a️⃣ speckit.tasks<br/>拆解可驗收任務"]
        ANALYZE["8b️⃣ speckit.analyze<br/>確認 Feature 內一致性"]
        
        TASKS --> ANALYZE
        ANALYZE --> ANALYZE_Check{一致？}
        ANALYZE_Check -->|有問題| ANALYZE_Fix["修正 Tasks/Plan"]
        ANALYZE_Check -->|通過| IMPL
        ANALYZE_Fix --> TASKS
    end

    subgraph Phase4["💻 Phase 4：實作"]
        IMPL["9️⃣ speckit.implement<br/>實作程式碼 + 測試"]
        CODECHECK["9️⃣.5 flowkit.code-check<br/>AI 五層驗證金字塔"]
        REFINE["9️⃣' flowkit.refine-loop<br/>小幅修正循環"]
        TRIAGE{"非功能回歸<br/>Bug-Fix Triage"}
        REFINE_BF["9️⃣' refine-loop<br/>Bug-Fix 模式"]
        TD_REG["登記 TD<br/>（HIGH / 需改 Spec）"]
        
        IMPL --> CODECHECK
        CODECHECK --> CC_Result{PASS / FAIL？}
        CC_Result -->|❌ FAIL| REFINE
        CC_Result -->|✅ PASS| PUC
        CC_Result -->|🟡 非功能回歸| TRIAGE
        TRIAGE -->|EASY/MEDIUM| REFINE_BF
        TRIAGE -->|HIGH| TD_REG
        REFINE --> IMPL
        REFINE_BF --> CODECHECK
        TD_REG -.-> PUC
    end

    subgraph Phase5["✅ Phase 5：驗證合併"]
        PUC["🔟 a flowkit.pre-unify-check<br/>檢查實作正確性"]
        TRACE["🔟 b flowkit.trace<br/>建立 Spec-Code 追溯"]
        REQSYNC["🔟 c flowkit.requirement-sync<br/>回寫變更至 PRD / US"]
        UNIFY["1️⃣1️⃣ flowkit.unify-flow<br/>合併至 System Spec"]
        
        PUC --> PUC_Check{可合併？}
        PUC_Check -->|有問題| PUC_Fix["修正實作"]
        PUC_Check -->|通過| TRACE
        PUC_Fix --> IMPL
        TRACE --> REQSYNC
        REQSYNC --> UNIFY
    end

    subgraph Phase6["📤 Phase 6：PR 提交"]
        PRREVIEW["1️⃣2️⃣ flowkit.pr-review<br/>六維品質審查<br/>+ TD Closure Verification"]
        PRREVIEW --> PR_Check{品質通過？}
        PR_Check -->|"🟢 READY"| PR_CREATE["🔀 gh pr create"]
        PR_Check -->|"🔴 NOT READY"| PR_FIX["回退修正"]
        PR_FIX --> REFINE
    end

    UNIFY --> PRREVIEW
    PR_CREATE --> NEXT["🔄 下一個 Feature"]
    NEXT -.-> BDD

    style Phase1 fill:#e3f2fd
    style Phase2 fill:#fff9c4
    style Phase3 fill:#ffe0b2
    style Phase4 fill:#e8f5e9
    style Phase5 fill:#f3e5f5
    style Phase6 fill:#fce4ec
```

---

## 簡化線性流程（快速參考）

```mermaid
flowchart LR
    subgraph 輸入["📘 輸入"]
        PRD["PRD-*.md"]
    end
    
    subgraph 需求["📋 需求規劃"]
        A1["🟡 BDD-Milestone<br/>PRD → US"] --> A2["BDD-Milestone<br/>US → Milestone"]
        A2 --> B["Milestone-context"]
    end
    
    subgraph 規格["📝 規格定義"]
        C["specify"] --> C2["clarify<br/>（選擇性）"]
        C2 --> D["system-context<br/>（建議必要）"]
        D --> E["plan"]
        E --> F["consistency-check"]
    end
    
    subgraph 任務["📝 任務拆解"]
        G["tasks"] --> H["analyze"]
    end
    
    subgraph 實作["💻 實作"]
        I["implement"] --> I3["code-check"]
        I3 -.->|FAIL| I2["refine-loop"]
        I3 -.->|"🟡 非功能回歸"| I4["Bug-Fix Triage"]
        I4 -.->|"EASY/MEDIUM"| I2
        I2 -.-> I
    end
    
    subgraph 驗證["✅ 驗證合併"]
        J["pre-unify-check"] --> J2["trace"]
        J2 --> K["requirement-sync"]
        K --> L["unify-flow"]
    end
    
    subgraph PR["📤 PR 提交"]
        M["pr-review"]
    end
    
    PRD --> A1
    B --> C
    F --> G
    H --> I
    I3 -->|PASS| J
    L --> M
    M -.-> |"🔴 NOT READY"| I2
    M -->|"🟢 READY"| PR_OUT["🔀 gh pr create"]
    PR_OUT -.-> |"Next Feature"| A2
    
    style 輸入 fill:#e8eaf6
    style 需求 fill:#e3f2fd
    style 規格 fill:#fff9c4
    style 任務 fill:#ffe0b2
    style 實作 fill:#e8f5e9
    style 驗證 fill:#f3e5f5
    style PR fill:#fce4ec
```

> 🟡 **注意**：
> - `BDD-Milestone (PRD → US)` 僅在首次或 PRD 變更時執行，後續 Feature 開發直接從 `BDD-Milestone (US → Milestone)` 開始。
> - `Milestone-context` 固定在 BDD-Milestone 之後執行（spec 和 plan 皆可能需要）。
> - `system-context` **建議**在 specify 之後、plan 之前執行（**建議必要**，除非是第一個 Feature）。

---

## 指令分類視圖

```mermaid
mindmap
  root((SDD 開發套件))
    SpecKit【規格定義】
      specify
        建立 Feature Spec
        創建新分支
      clarify
        釐清規格細節
        選擇性執行
      plan
        制定實作計畫
        設計決策
      tasks
        拆解可驗收任務
      analyze
        確認一致性
      implement
        實作程式碼
        撰寫測試
    FlowKit【流程輔助】
      需求規劃
        BDD-Milestone
          拆解 User Stories
          規劃 Milestone
        Milestone-context
          抽取 PRD 上下文
          衝突檢測
      品質檢查
        consistency-check
          覆用檢查
          整合建議
        code-check
          AI 五層驗證金字塔
          implement 後執行
        pre-unify-check
          實作驗證
        trace
          追溯索引
      維護工具
        unify-flow
          合併至 System
        system-context
          更新專案上下文
        refine-loop
          小幅修正循環
      PR 提交
        pr-review
          六維品質審查
          自動 PR 建立
      全專案健康
        system-health
          五維度診斷 D1~D5
          TD 自動登記
          Advisory 隨時可執行
```

---

## 階段詳解

### Phase 1：需求規劃

```mermaid
flowchart TD
    subgraph Input["輸入"]
        PRD["PRD-*.md"]
        US_Exist["既有 User Stories"]
    end
    
    subgraph Process["處理"]
        direction TB
        BDD1["🟡 flowkit.BDD-Milestone<br/>PRD → User Stories<br/>（首次 / PRD 變更時）"]
        BDD2["flowkit.BDD-Milestone<br/>User Stories → Milestone<br/>（每次 Feature 開發）"]
        MC["flowkit.Milestone-context"]
    end
    
    subgraph Output["產出"]
        US["User Stories"]
        MS["Milestone"]
        CTX["設計上下文"]
        CR["衝突報告（若有）"]
    end
    
    PRD --> BDD1
    BDD1 --> US
    US --> BDD2
    US_Exist -.-> BDD2
    BDD2 --> MS
    MS --> MC
    PRD -.-> MC
    MC --> CTX
    MC --> CR
```

**目的**：將模糊的產品需求轉化為結構化的開發單位

| 指令 | 模式 | 執行時機 | 關鍵產出 |
|------|------|----------|----------|
| `BDD-Milestone` | PRD → US | 🟡 首次 / PRD 變更 | User Stories（BDD 格式）|
| `BDD-Milestone` | US → Milestone | 每次 Feature 開發 | Milestone 規劃 |
| `Milestone-context` | - | Milestone 建立後 | PRD 相關內容、衝突報告 |

---

### Phase 2：規格定義

```mermaid
flowchart TD
    subgraph Spec["規格建立"]
        SPECIFY["speckit.specify<br/>建立 Feature Spec"]
        CLARIFY["speckit.clarify<br/>（選擇性）"]
    end
    
    subgraph Context["上下文準備"]
        SC["system-context<br/>（建議必要，建立專案上下文）"]
    end
    
    subgraph Planning["規劃"]
        PLAN["speckit.plan"]
        CC["consistency-check"]
    end
    
    SPECIFY --> CLARIFY
    CLARIFY -.->|選擇性| SC
    SPECIFY --> SC
    SC --> PLAN
    PLAN --> CC
    
    CC --> Result{結果}
    Result -->|通過| Next["→ Phase 3"]
    Result -->|問題| Fix["修正 Plan"]
    Fix --> PLAN
```

**目的**：定義清晰的規格並制定善用現有系統的實作計畫

| 指令 | 核心任務 | 關鍵產出 |
|------|----------|----------|
| `specify` | 建立規格 | spec.md、新 Feature 分支 |
| `clarify` | 釐清細節 | 更精確的 spec（選擇性） |
| `system-context` | 建立專案上下文 | system-context-index.md（建議必要） |
| `plan` | 制定計畫 | plan.md |
| `consistency-check` | 確認覆用 | 檢查報告（覆用建議、整合建議） |

---

### Phase 3：任務拆解

```mermaid
flowchart TD
    TASKS["speckit.tasks<br/>拆解任務"]
    ANALYZE["speckit.analyze<br/>一致性分析"]
    
    TASKS --> ANALYZE
    ANALYZE --> Result{一致？}
    Result -->|是| Next["→ Phase 4"]
    Result -->|否| Fix["修正 Tasks/Plan"]
    Fix --> TASKS
```

**目的**：將計畫轉化為可執行、可驗收的任務清單

---

### Phase 4：實作

```mermaid
flowchart TD
    IMPL["speckit.implement<br/>實作程式碼"]
    CODECHECK["flowkit.code-check<br/>AI 五層驗證金字塔"]
    
    IMPL --> CODECHECK
    CODECHECK --> Check{PASS / FAIL？}
    Check -->|❌ FAIL| REFINE["flowkit.refine-loop<br/>小幅修正"]
    Check -->|✅ PASS| Next["→ Phase 5"]
    REFINE --> IMPL
```

**目的**：按照規格實作程式碼，透過 code-check 驗證品質，必要時進行小幅調整

| 指令 | 核心任務 | 使用時機 |
|------|----------|----------|
| `implement` | 實作程式碼 | 主要實作流程 |
| `code-check` | AI 五層驗證 | implement 完成後自動執行 |
| `refine-loop` | 小幅修正 | code-check FAIL 時修復問題 |

---

### Phase 5：驗證合併

```mermaid
flowchart TD
    PUC["flowkit.pre-unify-check<br/>實作驗證"]
    TRACE["flowkit.trace<br/>建立追溯"]
    REQSYNC["flowkit.requirement-sync<br/>同步需求文件"]
    UNIFY["flowkit.unify-flow<br/>合併至 System"]
    
    PUC --> Result{可合併？}
    Result -->|是| TRACE
    Result -->|否| Fix["← 回 Phase 4 修正"]
    TRACE --> REQSYNC
    REQSYNC --> UNIFY
    UNIFY --> Done["✅ Feature 完成"]
```

**目的**：確保實作品質、同步需求文件，並將 Feature 整合回 System

| 指令 | 核心任務 | 關鍵產出 |
|------|----------|----------|
| `pre-unify-check` | 實作驗證 | 檢查報告 |
| `trace` | 追溯建立 | Spec-Code 對照索引 |
| `requirement-sync` | 需求同步 | 更新 PRD / User Stories |
| `unify-flow` | 合併 + TD 結案 | System Spec 更新、TD Reconciliation |

---

## 技術債生命週期視圖

```mermaid
flowchart LR
    subgraph 登記["📝 登記通道"]
        CC_TD["code-check<br/>LOW 放行登記"]
        PR_TD["pr-review<br/>品質放行登記"]
        SH_TD["system-health<br/>五維度檢查登記"]
    end

    subgraph 追蹤["📅 追蹤規劃"]
        BDD_TD["BDD-Milestone<br/>建議納入 Milestone"]
    end

    subgraph 標註["🏷️ 標註"]
        SPEC_TD["specify<br/>TD Ref 標註"]
    end

    subgraph 結案["✅ 結案"]
        UNIFY_TD["unify-flow<br/>Phase 7<br/>TD Reconciliation"]
    end

    subgraph 驗證["🔍 驗證"]
        PRREV_TD["pr-review<br/>Phase 7.6<br/>TD Closure Verification"]
    end

    TD_REG[("📚 TD Registry<br/>docs/technical-debt.md")]

    CC_TD --> TD_REG
    PR_TD --> TD_REG
    SH_TD --> TD_REG
    TD_REG --> BDD_TD
    TD_REG --> SPEC_TD
    SPEC_TD -->|"> TD Ref: TD-XXX"| UNIFY_TD
    UNIFY_TD -->|"結案更新"| TD_REG
    UNIFY_TD --> PRREV_TD
    PRREV_TD -->|"一致性檢查"| PR_OUT["🔀 PR"]

    style 登記 fill:#e8f5e9
    style 追蹤 fill:#fff9c4
    style 標註 fill:#e3f2fd
    style 結案 fill:#f3e5f5
    style 驗證 fill:#fce4ec
```

> 📖 **詳細說明**：[技術債生命週期管理](./%E5%8A%9F%E8%83%BD%E8%AA%AA%E6%98%8E-%E6%8A%80%E8%A1%93%E5%82%B5%E7%94%9F%E5%91%BD%E9%80%B1%E6%9C%9F%E7%AE%A1%E7%90%86.md)

---

## 測試策略視圖

### 測試執行全景

```mermaid
flowchart TD
    subgraph Spec["📝 規格階段"]
        AC["Acceptance Criteria<br/>Given / When / Then"]
    end

    subgraph Implement["💻 實作階段"]
        WRITE_TEST["speckit.implement<br/>§7.5 測試標記指引<br/>撰寫測試 + 標記"]
        CONFTEST["tests/conftest.py<br/>marker 註冊<br/>+ 自動慢測試偵測"]
    end

    subgraph CodeCheck["🔍 code-check L2"]
        RUN_TESTS["uv run pytest tests/<br/>-q --tb=short<br/>（串行執行）"]
        MERGE["統計結果<br/>passed / failed / skipped"]
    end

    subgraph Artifacts["📂 產物"]
        DURATIONS[".artifacts/<br/>test-durations.json"]
        REPORT[".artifacts/<br/>code-check-report.md"]
    end

    AC -->|"衍生測試案例"| WRITE_TEST
    WRITE_TEST --> CONFTEST
    CONFTEST --> RUN_TESTS
    RUN_TESTS --> MERGE
    MERGE --> REPORT
    CONFTEST -->|"記錄耗時"| DURATIONS
    DURATIONS -->|"下次自動標記"| CONFTEST

    style Spec fill:#fff9c4
    style Implement fill:#e8f5e9
    style CodeCheck fill:#e3f2fd
    style Artifacts fill:#f3e5f5
```

### 測試標記與分批機制

```mermaid
flowchart LR
    subgraph Markers["🏷️ 測試標記"]
        SLOW["@pytest.mark.slow<br/>耗時 > 30 秒"]
        SERIAL["@pytest.mark.serial<br/>共享資源不可並行"]
        NONE["無標記<br/>快速 + 可並行"]
    end

    subgraph Auto["🤖 自動標記"]
        HISTORY["test-durations.json<br/>歷史耗時記錄"]
        AUTO_MARK["conftest.py<br/>超過 30s 自動標記"]
    end

    subgraph Execution["⚡ 分批執行"]
        FAST["Step 1（並行）<br/>pytest -n auto<br/>not slow and not serial"]
        SLOW_RUN["Step 2（串行）<br/>slow or serial"]
    end

    HISTORY --> AUTO_MARK
    AUTO_MARK -->|"自動加 @slow"| SLOW

    NONE --> FAST
    SLOW --> SLOW_RUN
    SERIAL --> SLOW_RUN

    style Markers fill:#e8f5e9
    style Auto fill:#fff9c4
    style Execution fill:#e3f2fd
```

### 測試在各階段的角色

| 階段 | 測試相關活動 | 關鍵指令 |
|------|------------|----------|
| **規格定義** | AC 撰寫（Given/When/Then） | `speckit.specify` |
| **任務拆解** | 測試任務識別 | `speckit.tasks` |
| **實作** | Test-First 撰寫測試 + 標記（slow/serial） | `speckit.implement` §7.5 |
| **驗證** | L2 分批執行 + 回歸分析 + 非功能回歸分流 | `flowkit.code-check` |
| **修正** | 測試失敗修復 + Bug-Fix 模式 | `flowkit.refine-loop` |
| **合併前** | AC↔測試覆蓋度檢查 | `flowkit.pre-unify-check` |
| **追溯** | @spec-ac 對照索引 | `flowkit.trace` |
| **健康檢查** | 測試通過率 + AC 覆蓋度評分 | `flowkit.system-health` |

> 📖 **詳細說明**：[測試策略與自動化機制](./%E5%8A%9F%E8%83%BD%E8%AA%AA%E6%98%8E-%E6%B8%AC%E8%A9%A6%E7%AD%96%E7%95%A5%E8%88%87%E8%87%AA%E5%8B%95%E5%8C%96%E6%A9%9F%E5%88%B6.md)

---

## 決策點詳解

### Milestone-context 衝突處理

```mermaid
flowchart TD
    MC["Milestone-context 執行"] --> Check{檢測結果}
    Check -->|無衝突| Continue["繼續至 specify"]
    Check -->|有衝突| Report["產生衝突報告"]
    Report --> Decision{決策選項}
    Decision -->|修改 PRD| UpdatePRD["調整需求<br/>→ 重跑 BDD-Milestone"]
    Decision -->|修改 System| UpdateSystem["記錄為 Feature 範圍<br/>→ 在 Plan 中處理"]
    Decision -->|新增為例外| AddException["記錄例外處理<br/>→ 繼續開發"]
    UpdatePRD --> MC
    UpdateSystem --> Continue
    AddException --> Continue
```

### consistency-check 覆用檢查

```mermaid
flowchart TD
    CC["consistency-check 執行"] --> Analyze["分析 Plan vs System"]
    Analyze --> Results["檢查項目"]
    
    Results --> R1["✅ 覆用建議<br/>哪些 System 功能可直接使用"]
    Results --> R2["⚠️ 重複風險<br/>哪些功能可能重做"]
    Results --> R3["💡 整合建議<br/>如何最佳整合"]
    
    R1 --> Decision{需要調整？}
    R2 --> Decision
    R3 --> Decision
    
    Decision -->|是| Fix["修正 Plan"]
    Decision -->|否| Pass["通過 → tasks"]
    Fix --> CC
```

---

## 上下文流動圖

```mermaid
flowchart LR
    subgraph Sources["📥 上下文來源"]
        PRD["PRD-*.md"]
        SYS["specs/system/*"]
    end
    
    subgraph Extract["📤 上下文抽取"]
        MC["Milestone-context<br/>抽取 PRD 相關內容<br/>（BDD-Milestone 之後）"]
        SC["system-context<br/>抽取已實作內容<br/>（specify 之後、plan 之前）"]
    end
    
    subgraph Use["📋 上下文使用"]
        SPEC["Specify 階段<br/>（使用 Milestone-context）"]
        PLAN["Plan 階段<br/>（使用 system-context）"]
        CC["consistency-check"]
    end
    
    PRD --> MC
    SYS --> SC
    SYS --> CC
    
    MC --> SPEC
    MC --> PLAN
    SC --> PLAN
    PLAN --> CC
```

---

## 首個 Feature vs 後續 Feature

| 面向 | 首個 Feature | 後續 Feature |
|------|-------------|--------------|
| `system-context` | 可略過（System 尚空） | 需要（理解已實作功能） |
| `Milestone-context` 衝突檢測 | 通常無衝突 | 需仔細檢查 |
| `consistency-check` | 著重架構建立 | 著重覆用與整合 |
| `pre-unify-check` | 基礎檢查 | 需確認與現有功能相容 |

---

## 使用說明

### 在 VS Code 中預覽

1. 安裝 Markdown Preview Mermaid Support 擴充套件
2. 開啟本文件
3. 按 `Ctrl+Shift+V` 預覽

### 在 GitHub 中檢視

GitHub 原生支援 Mermaid，直接在 Repository 中檢視即可。

### 匯出為圖片

1. 使用 [Mermaid Live Editor](https://mermaid.live/)
2. 貼上 Mermaid 程式碼
3. 下載 PNG/SVG
