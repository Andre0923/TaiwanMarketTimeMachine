# SDD 開發流程圖

> **最後更新**：2026-01-26  
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
| | 5 | `flowkit.system-context` | System | 已實作上下文 | **建議必要**（除非首個 Feature） |
| | 6 | `speckit.plan` | Spec, 上下文 | Plan | 制定實作計畫 |
| | 7 | `flowkit.consistency-check` | Plan, System | 檢查報告 | 確認覆用、不重做、整合建議 |
| **任務拆解** | 8a | `speckit.tasks` | Plan | Tasks | 拆解可驗收任務 |
| | 8b | `speckit.analyze` | Tasks, 程式碼 | 分析報告 | 確認 Feature 內一致性 |
| **實作** | 9 | `speckit.implement` | Tasks | 程式碼, 測試 | 實作程式碼 |
| | 9' | `flowkit.refine-loop` | 修正需求 | 更新 Spec/Code | 🔄 循環：需要時使用 |
| **驗證合併** | 10a | `flowkit.pre-unify-check` | 實作結果 | 檢查報告 | 確認可安全合併 |
| | 10b | `flowkit.trace` | Spec, Code | 追溯索引 | 建立規格-程式碼對照 |
| | 10c | `flowkit.requirement-sync` | Feature, PRD, US | 更新需求文件 | 回寫變更至 PRD / User Stories |
| | 11 | `flowkit.unify-flow` | Feature | System 更新 | 合併至 System Spec |

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
        REFINE["9️⃣' flowkit.refine-loop<br/>小幅修正循環"]
        
        IMPL --> IMPL_Check{需要修正？}
        IMPL_Check -->|是| REFINE
        IMPL_Check -->|否| PUC
        REFINE --> IMPL
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

    UNIFY --> NEXT["🔄 下一個 Feature"]
    NEXT -.-> BDD

    style Phase1 fill:#e3f2fd
    style Phase2 fill:#fff9c4
    style Phase3 fill:#ffe0b2
    style Phase4 fill:#e8f5e9
    style Phase5 fill:#f3e5f5
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
        I["implement"] -.-> I2["refine-loop"]
        I2 -.-> I
    end
    
    subgraph 驗證["✅ 驗證合併"]
        J["pre-unify-check"] --> J2["trace"]
        J2 --> K["requirement-sync"]
        K --> L["unify-flow"]
    end
    
    PRD --> A1
    B --> C
    F --> G
    H --> I
    I --> J
    L -.-> |"Next Feature"| A2
    
    style 輸入 fill:#e8eaf6
    style 需求 fill:#e3f2fd
    style 規格 fill:#fff9c4
    style 任務 fill:#ffe0b2
    style 實作 fill:#e8f5e9
    style 驗證 fill:#f3e5f5
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
    
    IMPL --> Check{完成？<br/>需要修正？}
    Check -->|需要修正| REFINE["flowkit.refine-loop<br/>小幅修正"]
    Check -->|完成| Next["→ Phase 5"]
    REFINE --> IMPL
```

**目的**：按照規格實作程式碼，必要時進行小幅調整

| 指令 | 核心任務 | 使用時機 |
|------|----------|----------|
| `implement` | 實作程式碼 | 主要實作流程 |
| `refine-loop` | 小幅修正 | 發現需要調整規格或程式碼時 |

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
| `unify-flow` | 合併 | System Spec 更新 |

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
